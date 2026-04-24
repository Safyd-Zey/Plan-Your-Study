#!/bin/bash
# Start Grafana monitoring stack

echo "🚀 Starting Grafana monitoring stack..."
echo ""

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! docker-compose --version &> /dev/null; then
    echo "❌ docker-compose is not installed. Using 'docker compose' instead..."
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Start containers
echo "📦 Starting InfluxDB and Grafana containers..."
$DOCKER_COMPOSE up -d influxdb grafana

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check if services are running
echo "🔍 Checking service health..."
if curl -s http://localhost:8086/health &> /dev/null; then
    echo "✅ InfluxDB is running on http://localhost:8086"
else
    echo "⚠️  InfluxDB might still be starting..."
fi

if curl -s http://localhost:3001 &> /dev/null; then
    echo "✅ Grafana is running on http://localhost:3001"
else
    echo "⚠️  Grafana might still be starting..."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 GRAFANA DASHBOARD"
echo ""
echo "   URL: http://localhost:3001"
echo "   Login: admin / admin123"
echo ""
echo "🗄️  INFLUXDB"
echo ""
echo "   URL: http://localhost:8086"
echo "   Database: testmetrics"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 After running tests, collect metrics:"
echo ""
echo "   python test_metrics_collector.py"
echo ""
echo "🛑 To stop the services:"
echo ""
echo "   $DOCKER_COMPOSE down"
echo ""

# Try to open in browser
if command -v xdg-open &> /dev/null; then
    echo "🌐 Opening Grafana in browser..."
    xdg-open http://localhost:3001 &
elif command -v open &> /dev/null; then
    echo "🌐 Opening Grafana in browser..."
    open http://localhost:3001 &
else
    echo "📱 Please open http://localhost:3001 in your browser"
fi

echo ""
echo "✨ Setup complete! Grafana is ready for test visualization."
