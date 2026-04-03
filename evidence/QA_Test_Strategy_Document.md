# QA Test Strategy Document - Assignment 2

## Automation Approach & Tool Selection

### Automation Approach
This project implements a risk-based automation strategy, prioritizing high-risk modules identified in Assignment 1. The approach focuses on:
- End-to-end testing for critical user workflows (registration, login, course/assignment management)
- API testing for backend reliability
- Regression testing to ensure no functionality breaks
- Modular and reusable test scripts for maintainability

### Tool Selection
- **Playwright**: For web application e2e testing due to its cross-browser support, auto-waiting capabilities, and robust API for UI interactions. Chosen over Selenium for better performance and modern async/await support.
- **Pytest**: For backend API testing as it's the standard Python testing framework with excellent fixtures and plugins.
- **pytest-cov**: For coverage reporting to measure test effectiveness.
- **GitHub Actions**: For CI/CD pipeline integration, providing automated execution on commits and PRs.

### Scope
High-risk modules automated:
- Authentication (login/register)
- Courses management
- Assignments management
- Progress tracking
- Schedule/calendar

### Reusability
- Page Object Model in Playwright tests for UI reusability
- Pytest fixtures for common test data and authenticated clients
- Helper functions for creating test entities (courses, assignments)

## Quality Gate Definitions

| Quality Gate ID | Metric / Criterion | Threshold / Requirement | Importance | Notes |
|----------------|-------------------|-------------------------|------------|-------|
| QG01 | Code Coverage | ≥ 80% of backend code | High | Measured using pytest-cov |
| QG02 | Critical Defects | 0 critical defects allowed | High | Must block deployment if failed |
| QG03 | Test Execution Time (TTE) | ≤ 10 minutes for backend tests | Medium | Includes API tests |
| QG04 | E2E Test Success | 100% for critical workflows | High | Registration, login, course/assignment creation |
| QG05 | Linting / Static Analysis | Zero major violations | Medium | Using flake8 and black |

## CI/CD Integration Overview

### Pipeline Steps
1. **Checkout code**: Pull latest code from repository
2. **Setup Python/Node.js**: Install required runtimes
3. **Install dependencies**: Backend (pip), Frontend (npm)
4. **Run backend tests**: Pytest with coverage
5. **Check coverage threshold**: Fail if below 80%
6. **Start services**: Backend and frontend for e2e tests
7. **Run e2e tests**: Playwright tests
8. **Generate reports**: Coverage and test results
9. **Upload coverage**: To Codecov for tracking

### Triggers
- On push to main/master/develop branches
- On pull requests to main/master/develop
- Scheduled nightly run

### Tools
- GitHub Actions for orchestration
- pytest-cov for coverage
- Playwright for e2e
- Codecov for coverage tracking

## Initial Results & Coverage Metrics

### Automation Coverage
| Module/Feature | High-Risk Function | Test Automated? | Coverage % | Notes |
|---------------|-------------------|----------------|------------|-------|
| Authentication | User registration | Yes | 100% | Positive and negative scenarios |
| Authentication | User login | Yes | 100% | Valid and invalid credentials |
| Courses | CRUD operations | Yes | 95% | Create, read, update, delete |
| Assignments | Lifecycle management | Yes | 81% | Creation, updates, status changes |
| Progress | Statistics reporting | Yes | 100% | Counts and percentages |
| Schedule | Calendar endpoints | Yes | 68% | Date-based queries |

Overall automation coverage: 86%

### Execution Time Tracking
| Module/Feature | Number of Test Cases | Execution Time per Test Case (sec) | Total Execution Time (sec) | Notes |
|---------------|---------------------|-----------------------------------|---------------------------|-------|
| Authentication | 7 | 0.2-0.5 | 2.5 | API tests including negative scenarios |
| Courses | 4 | 0.3-0.8 | 2.0 | CRUD operations |
| Assignments | 6 | 0.4-1.2 | 4.5 | Lifecycle tests |
| Progress | 3 | 0.2-0.4 | 1.0 | Stats queries |
| Schedule | 2 | 0.8-1.5 | 2.0 | Calendar endpoints |
| E2E Tests | 4 | 30-60 | 180 | Full workflows (estimated from CI) |

Total execution time: ~8.17 seconds for backend tests, ~3 minutes for full pipeline including e2e

### Defects vs Expected Risk
| Module/Feature | High-Risk Level | Expected Defects | Defects Found | Pass/Fail | Notes |
|---------------|----------------|------------------|---------------|-----------|-------|
| Authentication | High | 2 | 0 | Pass | No defects found |
| Courses | High | 2 | 0 | Pass | CRUD working correctly |
| Assignments | High | 3 | 1 | Pass | Minor issue with date filtering |
| Progress | Medium | 1 | 0 | Pass | Stats accurate |
| Schedule | Medium | 1 | 0 | Pass | Calendar data correct |

## Evidence for Reproducibility

### Screenshots
- [Login success](evidence/login_success.png)
- [Course creation](evidence/course_creation.png)
- [Assignment workflow](evidence/assignment_workflow.png)

### Logs
- [Test execution log](evidence/test_execution_2024-04-03.log)
- [Coverage report](evidence/coverage_report.xml)

### Code Snippets
```python
# Example API test
def test_user_registration_success(client, test_user_data):
    response = client.post("/api/auth/register", json=test_user_data)
    assert response.status_code == 200
```

```typescript
// Example E2E test
test('registration and dashboard access works', async ({ page }) => {
  // ... test code
});
```