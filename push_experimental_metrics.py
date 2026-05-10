#!/usr/bin/env python3
"""
Experimental Metrics Pusher
Reads results from performance/mutation/chaos JSON files and pushes
them into InfluxDB as new measurements for Grafana visualization.

Measurements created:
  - perf_scenario  (tags: scenario)  fields: median_ms, p95_ms, p99_ms, rps, error_rate_pct, users
  - mutation_module (tags: module)   fields: created, killed, survived, score
  - mutation_overall                  fields: total_created, total_killed, total_survived, overall_score
  - chaos_scenario (tags: scenario)  fields: availability_pct, mttr_s, graceful
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

INFLUXDB_URL = "http://localhost:8086"
DB = "testmetrics"
WRITE_URL = f"{INFLUXDB_URL}/write?db={DB}&u=admin&p=admin123"

ROOT = Path(__file__).parent


def write(lines: list[str]):
    payload = "\n".join(lines)
    r = requests.post(WRITE_URL, data=payload.encode(), timeout=10)
    if r.status_code not in (200, 204):
        print(f"  ERROR {r.status_code}: {r.text[:200]}")
        return False
    return True


def ts_now() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1_000_000_000)


def escape_tag(v: str) -> str:
    """Escape spaces and commas in InfluxDB tag values."""
    return str(v).replace(" ", "_").replace(",", "_").replace("=", "_")


# ─── Performance ─────────────────────────────────────────────────────────────

def push_performance():
    path = ROOT / "tests/performance/results/performance_results.json"
    if not path.exists():
        print("  SKIP: performance_results.json not found")
        return

    data = json.loads(path.read_text())
    lines = []
    ts = ts_now()

    for scenario in data:
        agg = scenario.get("aggregate", {})
        tag = escape_tag(scenario["scenario"])
        users = scenario["users"]
        median = agg.get("median_ms", 0)
        p95 = agg.get("p95_ms", 0)
        p99 = agg.get("p99_ms", 0)
        rps = agg.get("rps", 0)
        err = agg.get("error_rate_pct", 0)
        total_req = agg.get("requests", 0)
        total_fail = agg.get("failures", 0)

        lines.append(
            f"perf_scenario,scenario={tag} "
            f"median_ms={median},p95_ms={p95},p99_ms={p99},"
            f"rps={rps},error_rate_pct={err},"
            f"users={users}i,total_requests={total_req}i,total_failures={total_fail}i"
            f" {ts}"
        )
        ts += 1_000_000  # 1ms apart so Grafana sees them as separate points

    if write(lines):
        print(f"  ✓ Performance: {len(lines)} scenario(s) pushed")


# ─── Mutation ─────────────────────────────────────────────────────────────────

def push_mutation():
    path = ROOT / "tests/mutation/results/mutation_results.json"
    if not path.exists():
        print("  SKIP: mutation_results.json not found")
        return

    data = json.loads(path.read_text())
    ts = ts_now()

    # Aggregate by module
    from collections import defaultdict
    by_module: dict[str, dict] = defaultdict(lambda: {"created": 0, "killed": 0, "survived": 0})
    for m in data:
        mod = Path(m["module"]).stem  # auth, courses, assignments
        by_module[mod]["created"] += 1
        if m["status"] == "killed":
            by_module[mod]["killed"] += 1
        elif m["status"] == "survived":
            by_module[mod]["survived"] += 1

    lines = []
    total_c = total_k = total_s = 0
    for mod, stats in by_module.items():
        c, k, s = stats["created"], stats["killed"], stats["survived"]
        score = k / c * 100 if c > 0 else 0
        total_c += c; total_k += k; total_s += s
        lines.append(
            f"mutation_module,module={mod} "
            f"created={c}i,killed={k}i,survived={s}i,score={score:.1f}"
            f" {ts}"
        )
        ts += 1_000_000

    # Overall
    overall_score = total_k / total_c * 100 if total_c > 0 else 0
    lines.append(
        f"mutation_overall "
        f"total_created={total_c}i,total_killed={total_k}i,"
        f"total_survived={total_s}i,overall_score={overall_score:.1f}"
        f" {ts}"
    )

    if write(lines):
        print(f"  ✓ Mutation: {len(lines)-1} module(s) + overall pushed (score={overall_score:.1f}%)")


# ─── Chaos ────────────────────────────────────────────────────────────────────

def push_chaos():
    path = ROOT / "tests/chaos/results/chaos_results.json"
    if not path.exists():
        print("  SKIP: chaos_results.json not found")
        return

    data = json.loads(path.read_text())
    lines = []
    ts = ts_now()

    for r in data:
        tag = escape_tag(r["scenario"])
        avail = r.get("availability_pct", 0)
        mttr = r.get("mttr_s", 0)
        graceful = 1 if r.get("graceful_degradation") else 0
        lines.append(
            f"chaos_scenario,scenario={tag} "
            f"availability_pct={avail},mttr_s={mttr},graceful={graceful}i"
            f" {ts}"
        )
        ts += 1_000_000

    if write(lines):
        print(f"  ✓ Chaos: {len(lines)} scenario(s) pushed")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("Pushing experimental metrics to InfluxDB...")
    print(f"Target: {INFLUXDB_URL}/db={DB}\n")

    push_performance()
    push_mutation()
    push_chaos()

    print("\nDone. Refresh Grafana dashboard to see new panels.")


if __name__ == "__main__":
    main()
