# Grafana Test Visualization 📊

Beautiful and interactive test metrics visualization using Grafana + InfluxDB.

## 🌟 Features

- 📊 **Real-time Dashboards** - Live test execution metrics
- 📈 **Coverage Trends** - Track code coverage over time
- 📉 **Test Performance** - Execution time analysis
- 🎨 **Beautiful UI** - Modern, responsive design
- 🔄 **Auto-refresh** - Updates every 30 seconds
- 🌐 **Browser-based** - Access from any device on network
- 🔐 **Secure** - Protected with authentication

## 🚀 Quick Start

### 1. Start the Monitoring Stack

```bash
# Make script executable
chmod +x start_grafana.sh

# Start Grafana and InfluxDB
./start_grafana.sh
```

This will:
- ✅ Start InfluxDB container
- ✅ Start Grafana container
- ✅ Auto-open Grafana in browser
- ✅ Show connection details

### 2. Login to Grafana

**Default Credentials:**
- **Username:** `admin`
- **Password:** `admin123`
- **URL:** http://localhost:3001

### 3. Run Tests and Collect Metrics

```bash
# Run tests and send metrics to InfluxDB
python test_metrics_collector.py
```

Or run pytest directly:
```bash
cd backend
pytest ../tests/ -v --cov=. --cov-report=xml
```

Then collect metrics:
```bash
python test_metrics_collector.py
```

### 4. View Dashboard

The dashboard will automatically appear in Grafana with:
- Test results summary (passed/failed/skipped)
- Code coverage percentage
- Execution time trends
- Test distribution pie chart

## 📊 Dashboard Panels

### 1. **Test Results Summary** 📋
Shows total number of passed tests with color coding:
- 🟢 Green: 80%+ pass rate
- 🟡 Yellow: 50-80% pass rate
- 🔴 Red: <50% pass rate

### 2. **Failed Tests** ❌
Tracks failed test count:
- 🟢 Green: 0 failures
- 🟡 Yellow: 1-5 failures
- 🔴 Red: 5+ failures

### 3. **Code Coverage** 📈
Shows code coverage percentage:
- 🟢 Green: 80%+ coverage
- 🟡 Yellow: 60-80% coverage
- 🔴 Red: <60% coverage

### 4. **Test Execution Time** ⏱️
Timeline graph showing execution duration trends over time

### 5. **Test Distribution** 🥧
Pie chart showing ratio of passed/failed/skipped tests

## 🔧 Configuration

### InfluxDB Details
- **Container Name:** `plan-study-influxdb`
- **Port:** 8086
- **Database:** `testmetrics`
- **User:** `admin`
- **Password:** `admin123`

### Grafana Details
- **Container Name:** `plan-study-grafana`
- **Port:** 3001 (internal 3000)
- **User:** `admin`
- **Password:** `admin123`
- **Plugin:** Pie chart support included

## 📝 Example Metrics Collected

```
coverage: 86.5%
test_run (backend): passed=22, failed=0, skipped=0, total=22
test_run (frontend): passed=5, failed=0, skipped=0, total=5
```

## 🛑 Stopping the Stack

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🐛 Troubleshooting

### ❌ Cannot connect to InfluxDB
```bash
# Check if container is running
docker ps | grep plan-study-influxdb

# Check logs
docker logs plan-study-influxdb

# Restart
docker-compose restart influxdb
```

### ❌ Grafana shows no data
1. Make sure you ran `python test_metrics_collector.py`
2. Check InfluxDB has data: `curl http://localhost:8086/query?db=testmetrics&q=SHOW%20MEASUREMENTS`
3. Reload Grafana dashboard (refresh page)

### ❌ Port already in use
Change port in `docker-compose.yml`:
```yaml
grafana:
  ports:
    - "3002:3000"  # Changed from 3001 to 3002
```

## 📚 Advanced Usage

### Custom Metrics

Edit `test_metrics_collector.py` to add custom metrics:

```python
# Example: Send module-specific metrics
self.send_to_influxdb("test_module", 
    {"passed": 15, "failed": 1},
    {"module": "auth"}
)
```

### Create Custom Dashboards

1. Login to Grafana (http://localhost:3001)
2. Click "+" → "Dashboard" → "Add Panel"
3. Select InfluxDB as datasource
4. Design your custom panels

### Queries

Example InfluxQL queries:

```
# Get latest test metrics
SELECT last(passed) FROM test_run WHERE suite = 'backend'

# Get average execution time
SELECT mean(duration_ms) FROM test_run

# Get coverage trend
SELECT percentage FROM coverage ORDER BY time DESC
```

## 🎨 Customization

### Change Dashboard Refresh Rate

In Grafana, top-right corner → Change refresh from 30s to desired interval

### Modify Colors

Edit dashboard → Edit panel → Display → Thresholds

### Export Dashboard

Dashboard → Share → Export as JSON

## 🔐 Security

For production use:
1. Change default passwords in `docker-compose.yml`
2. Enable authentication in InfluxDB
3. Run behind reverse proxy (nginx)
4. Use HTTPS
5. Set up firewall rules

## 📱 Mobile Access

Access Grafana from any device on your network:
```
http://<your-machine-ip>:3001
```

## 🚀 Performance Tips

- Limit data retention: Set up InfluxDB retention policies
- Use grafana datasource caching
- Aggregate old data to reduce storage

## 📞 Support

For issues:
1. Check Grafana logs: `docker logs plan-study-grafana`
2. Check InfluxDB logs: `docker logs plan-study-influxdb`
3. Verify connectivity: `curl http://localhost:8086/health`

---

**Made with ❤️ for beautiful test visualization**
