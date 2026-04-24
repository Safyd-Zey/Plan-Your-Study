#!/usr/bin/env python3
"""
Test Metrics Collector - Sends test results to InfluxDB for Grafana visualization
"""
import json
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    sys.exit(1)


class TestMetricsCollector:
    def __init__(self, influxdb_url="http://localhost:8086", db="testmetrics", 
                 username="admin", password="admin123"):
        self.influxdb_url = influxdb_url
        self.db = db
        self.username = username
        self.password = password
        self.write_url = f"{influxdb_url}/write?db={db}&u={username}&p={password}"
    
    def run_tests(self, test_dir="tests/"):
        """Run pytest and collect metrics"""
        print("🧪 Running tests...")
        cmd = [
            "pytest",
            test_dir,
            "-v",
            "--tb=short",
            "--cov=backend",
            "--cov-report=xml",
            "-q"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result
    
    def parse_junit_xml(self, xml_file="tests/junit.xml"):
        """Parse JUnit XML output from pytest"""
        if not Path(xml_file).exists():
            return None
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        metrics = {
            "total": int(root.get("tests", 0)),
            "passed": int(root.get("tests", 0)) - int(root.get("failures", 0)) - int(root.get("errors", 0)),
            "failed": int(root.get("failures", 0)) + int(root.get("errors", 0)),
            "skipped": int(root.get("skipped", 0)),
            "duration": float(root.get("time", 0))
        }
        return metrics
    
    def parse_coverage_xml(self, xml_file="coverage.xml"):
        """Parse coverage XML report"""
        if not Path(xml_file).exists():
            return None
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            coverage = float(root.get("line-rate", 0)) * 100
            return coverage
        except:
            return None
    
    def send_to_influxdb(self, metric_name, fields, tags={}, timestamp=None):
        """Send metric to InfluxDB"""
        if timestamp is None:
            timestamp = int(datetime.now(timezone.utc).timestamp() * 1000000000)
        
        # Format: measurement[,tag1=value1] field1=value1 timestamp
        tag_str = ",".join([f"{k}={v}" for k, v in tags.items()])
        field_str = ",".join([f"{k}={v}" for k, v in fields.items()])
        
        if tag_str:
            line = f"{metric_name},{tag_str} {field_str} {timestamp}"
        else:
            line = f"{metric_name} {field_str} {timestamp}"
        
        try:
            response = requests.post(self.write_url, data=line)
            if response.status_code == 204:
                print(f"✅ Sent {metric_name}: {fields}")
            else:
                print(f"⚠️  Warning: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Error: Cannot connect to InfluxDB at {self.influxdb_url}")
            print("   Make sure InfluxDB is running: docker-compose up -d influxdb")
    
    def collect_metrics(self):
        """Collect all metrics and send to InfluxDB"""
        print("\n📊 Collecting test metrics...\n")
        
        # Run tests
        result = self.run_tests()
        
        # Parse coverage
        coverage = self.parse_coverage_xml("coverage.xml")
        if coverage:
            self.send_to_influxdb("coverage", {"percentage": coverage})
            print(f"📈 Coverage: {coverage:.1f}%\n")
        
        # Parse test output
        output = result.stdout + result.stderr
        
        # Simple parsing
        if "passed" in output:
            # Extract numbers from pytest output
            import re
            match = re.search(r'(\d+) passed', output)
            passed = int(match.group(1)) if match else 0
            
            match = re.search(r'(\d+) failed', output)
            failed = int(match.group(1)) if match else 0
            
            match = re.search(r'(\d+) skipped', output)
            skipped = int(match.group(1)) if match else 0
            
            total = passed + failed + skipped
            
            # Send test metrics
            self.send_to_influxdb("test_run", 
                {"passed": passed, "failed": failed, "skipped": skipped, "total": total},
                {"suite": "backend"}
            )
            
            print(f"✅ Passed: {passed}")
            print(f"❌ Failed: {failed}")
            print(f"⏭️  Skipped: {skipped}")
            print(f"📊 Total: {total}")
        
        print("\n✨ Metrics sent to InfluxDB!")
        print("🌐 Open Grafana: http://localhost:3001 (admin/admin123)")


def main():
    collector = TestMetricsCollector()
    collector.collect_metrics()


if __name__ == "__main__":
    main()
