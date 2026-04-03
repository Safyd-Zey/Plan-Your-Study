#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing backend requirements..."
"$ROOT_DIR"/venv/bin/python -m pip install --upgrade pip
"$ROOT_DIR"/venv/bin/python -m pip install -r "$ROOT_DIR/backend/requirements.txt"

echo "Installing frontend dependencies..."
cd "$ROOT_DIR/frontend"
npm install
npm run test:e2e:install

echo "Running backend tests and coverage..."
cd "$ROOT_DIR"
"$ROOT_DIR"/venv/bin/python -m pytest --cov=backend --cov-report=term tests/integration/test_api_auth.py tests/integration/test_api_schedule.py tests/integration/test_api_course_assignment_subtask_progress.py

echo "Running Playwright E2E tests..."
cd "$ROOT_DIR/frontend"
npm run test:e2e

echo "All tests completed successfully."
