"""
Performance Test Runner for Plan Your Study API
Runs three load scenarios and outputs metrics to JSON/CSV files.

Scenarios:
  1. Normal Load   – 10 users, 60 s
  2. Peak Load     – 50 users, 60 s
  3. Spike Load    – 100 users, 30 s  (with quick ramp)

Results saved to: tests/performance/results/
"""

import subprocess
import sys
import json
import os
import time
import statistics
from pathlib import Path
from datetime import datetime

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

BASE_URL = "http://127.0.0.1:8000"
LOCUSTFILE = str(Path(__file__).parent / "locustfile.py")


def run_locust_scenario(name: str, users: int, spawn_rate: int, run_time: str) -> dict:
    """Run a locust scenario headlessly and parse the CSV stats."""
    prefix = RESULTS_DIR / name.replace(" ", "_").lower()
    cmd = [
        sys.executable, "-m", "locust",
        "-f", LOCUSTFILE,
        "--headless",
        "--host", BASE_URL,
        "--users", str(users),
        "--spawn-rate", str(spawn_rate),
        "--run-time", run_time,
        "--csv", str(prefix),
        "--only-summary",
        "--loglevel", "WARNING",
    ]
    print(f"\n{'='*60}")
    print(f"Scenario: {name} | Users: {users} | Duration: {run_time}")
    print(f"{'='*60}")
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    print(f"Completed in {elapsed:.1f}s  (exit code {result.returncode})")
    if result.stderr:
        # print last few lines of stderr (locust summary)
        for line in result.stderr.strip().split("\n")[-15:]:
            print(line)
    return _parse_csv_stats(str(prefix) + "_stats.csv", name, users, run_time)


def _parse_csv_stats(csv_path: str, scenario: str, users: int, duration: str) -> dict:
    """Parse locust stats CSV into a metrics dict."""
    metrics = {
        "scenario": scenario,
        "users": users,
        "duration": duration,
        "endpoints": [],
        "aggregate": {},
    }
    try:
        with open(csv_path) as f:
            lines = f.readlines()
        if len(lines) < 2:
            return metrics
        headers = [h.strip() for h in lines[0].split(",")]
        for line in lines[1:]:
            row = dict(zip(headers, [v.strip() for v in line.split(",")]))
            endpoint = {
                "name": row.get("Name", ""),
                "type": row.get("Type", ""),
                "requests": int(row.get("Request Count", 0) or 0),
                "failures": int(row.get("Failure Count", 0) or 0),
                "median_ms": float(row.get("50%", 0) or 0),
                "avg_ms": float(row.get("Average (ms)", 0) or 0),
                "min_ms": float(row.get("Min (ms)", 0) or 0),
                "max_ms": float(row.get("Max (ms)", 0) or 0),
                "p95_ms": float(row.get("95%", 0) or 0),
                "p99_ms": float(row.get("99%", 0) or 0),
                "rps": float(row.get("Requests/s", 0) or 0),
                "error_rate_pct": 0,
            }
            if endpoint["requests"] > 0:
                endpoint["error_rate_pct"] = round(
                    endpoint["failures"] / endpoint["requests"] * 100, 2
                )
            if row.get("Name") == "Aggregated":
                metrics["aggregate"] = endpoint
            else:
                metrics["endpoints"].append(endpoint)
    except FileNotFoundError:
        print(f"  WARNING: CSV not found at {csv_path}")
    return metrics


def print_metrics_table(metrics: dict):
    """Pretty-print metrics as ASCII table."""
    agg = metrics.get("aggregate", {})
    if not agg:
        print("  (no aggregate data)")
        return
    print(f"\n  Scenario Summary: {metrics['scenario']}")
    print(f"  {'Metric':<30} {'Value':>12}")
    print(f"  {'-'*44}")
    rows = [
        ("Total Requests", agg.get("requests", 0)),
        ("Total Failures", agg.get("failures", 0)),
        ("Error Rate (%)", f"{agg.get('error_rate_pct', 0):.2f}%"),
        ("Avg Response Time (ms)", f"{agg.get('avg_ms', 0):.1f}"),
        ("Median Response Time (ms)", f"{agg.get('median_ms', 0):.1f}"),
        ("95th Percentile (ms)", f"{agg.get('p95_ms', 0):.1f}"),
        ("99th Percentile (ms)", f"{agg.get('p99_ms', 0):.1f}"),
        ("Max Response Time (ms)", f"{agg.get('max_ms', 0):.1f}"),
        ("Requests/sec (throughput)", f"{agg.get('rps', 0):.2f}"),
    ]
    for label, value in rows:
        print(f"  {label:<30} {str(value):>12}")


def main():
    print("\nPlan Your Study — Performance Test Suite")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Health check first
    import urllib.request
    try:
        urllib.request.urlopen(f"{BASE_URL}/health", timeout=5)
        print(f"\nBackend reachable at {BASE_URL}")
    except Exception as e:
        print(f"\nERROR: Backend not reachable — {e}")
        print("Start backend with: python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000")
        sys.exit(1)

    scenarios = [
        {"name": "Normal Load",  "users": 10,  "spawn_rate": 2,  "run_time": "60s"},
        {"name": "Peak Load",    "users": 50,  "spawn_rate": 5,  "run_time": "60s"},
        {"name": "Spike Load",   "users": 100, "spawn_rate": 50, "run_time": "30s"},
    ]

    all_results = []
    for s in scenarios:
        result = run_locust_scenario(**s)
        print_metrics_table(result)
        all_results.append(result)

    # Save combined JSON
    out_path = RESULTS_DIR / "performance_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n\nResults saved to: {out_path}")

    # Print summary table across scenarios
    print("\n\n--- CROSS-SCENARIO SUMMARY ---")
    print(f"{'Scenario':<15} {'Users':>6} {'Req/s':>8} {'Avg(ms)':>9} {'p95(ms)':>9} {'Errors%':>8}")
    print("-" * 60)
    for r in all_results:
        agg = r.get("aggregate", {})
        print(
            f"{r['scenario']:<15} {r['users']:>6} "
            f"{agg.get('rps', 0):>8.2f} "
            f"{agg.get('avg_ms', 0):>9.1f} "
            f"{agg.get('p95_ms', 0):>9.1f} "
            f"{agg.get('error_rate_pct', 0):>7.2f}%"
        )

    print("\nPerformance testing completed.")


if __name__ == "__main__":
    main()
