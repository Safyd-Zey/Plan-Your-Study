# Assignment 2 Deliverables

## 1. Automated Test Implementation

### Scope Table
| Module/Feature | High-Risk Function | Test Priority | Notes/Expected Outcome |
|---------------|-------------------|---------------|----------------------|
| Authentication | User registration | High | Must handle duplicate emails, validation |
| Authentication | User login | High | Must fail for invalid credentials |
| Courses | CRUD operations | High | Must be user-isolated |
| Assignments | Lifecycle management | High | Must track status changes |
| Progress | Statistics reporting | Medium | Must provide accurate counts |
| Schedule | Calendar endpoints | Medium | Must handle date queries |

### Test Cases Table
| Test Case ID | Module/Feature | Description | Input Data | Expected Result | Scenario Type | Notes |
|-------------|---------------|-------------|------------|----------------|---------------|-------|
| TC01 | Authentication | Valid registration | username, email, password | 200 OK, user created | Positive | N/A |
| TC02 | Authentication | Duplicate email registration | existing email | 400 Bad Request | Negative | Check error message |
| TC03 | Authentication | Valid login | email, password | 200 OK, token returned | Positive | N/A |
| TC04 | Authentication | Invalid password login | email, wrong password | 401 Unauthorized | Negative | Check error message |
| TC05 | Authentication | Nonexistent email login | invalid email, password | 401 Unauthorized | Negative | Check error message |
| TC06 | Courses | Create course authenticated | course data | 201 Created | Positive | N/A |
| TC07 | Courses | Create course unauthenticated | course data | 401 Unauthorized | Negative | Check auth required |
| TC08 | Assignments | Create assignment | course_id, title, deadline | 200 OK | Positive | N/A |
| TC09 | Assignments | Update assignment status | assignment_id, status | 200 OK | Positive | Check status change |
| TC10 | E2E | Registration workflow | user data | Dashboard access | Positive | Full UI flow |
| TC11 | E2E | Login workflow | credentials | Dashboard access | Positive | Full UI flow |
| TC12 | E2E | Invalid login | wrong credentials | Error message | Negative | Check UI display |
| TC13 | E2E | Course and assignment creation | course + assignment data | Visible in UI | Positive | Full workflow |

### Script Implementation Table
| Script ID | Module/Feature | Framework | Location | Status | Comments |
|-----------|---------------|-----------|----------|--------|----------|
| S01 | Authentication API | pytest | tests/integration/test_api_auth.py | Complete | 7 test cases, positive & negative |
| S02 | Courses API | pytest | tests/integration/test_api_course_assignment_subtask_progress.py | Complete | CRUD operations |
| S03 | Assignments API | pytest | tests/integration/test_api_course_assignment_subtask_progress.py | Complete | Lifecycle management |
| S04 | Progress API | pytest | tests/integration/test_api_course_assignment_subtask_progress.py | Complete | Statistics reporting |
| S05 | Schedule API | pytest | tests/integration/test_api_schedule.py | Complete | Calendar endpoints |
| S06 | E2E Registration | Playwright | frontend/tests/e2e.spec.ts | Complete | UI workflow test |
| S07 | E2E Login | Playwright | frontend/tests/e2e.spec.ts | Complete | UI workflow test |
| S08 | E2E Invalid Login | Playwright | frontend/tests/e2e.spec.ts | Complete | Negative scenario |
| S09 | E2E Course/Assignment | Playwright | frontend/tests/e2e.spec.ts | Complete | Full workflow |

### Version Control Table
| Commit ID | Date | Module/Feature | Description | Author |
|-----------|------|---------------|-------------|--------|
| 0255fbf | 2024-04-03 | Testing Framework | Setup QA environment: tests framework, GitHub Actions, fixtures | Student |

### Evidence Table
| Evidence ID | Module/Feature | Type | Description | File Location |
|-------------|---------------|------|-------------|---------------|
| E01 | Backend Tests | Log | Test execution results | evidence/test_execution_2024-04-03.log |
| E02 | Coverage | XML Report | Coverage metrics | evidence/coverage_report.xml |
| E03 | CI/CD | YAML | Pipeline configuration | .github/workflows/test.yml |
| E04 | E2E Tests | TypeScript | Test scripts | frontend/tests/e2e.spec.ts |
| E05 | API Tests | Python | Test scripts | tests/integration/ |

## 2. Quality Gate Definition & Integration

### Quality Gate Table
| Quality Gate ID | Metric | Threshold | Importance | Notes |
|----------------|--------|-----------|------------|-------|
| QG01 | Code Coverage | ≥ 80% | High | Measured by pytest-cov |
| QG02 | Critical Defects | 0 | High | Must block deployment |
| QG03 | Test Execution Time | ≤ 10 min | Medium | For backend tests |
| QG04 | E2E Test Success | 100% | High | Critical workflows |
| QG05 | Linting | Zero major violations | Medium | Code quality |

### CI/CD Pipeline Table
| Steps | Tools | Trigger | Notes |
|-------|-------|---------|-------|
| Checkout code | Git | On push/PR | Latest code |
| Setup Python | actions/setup-python | Auto | Python 3.8-3.10 |
| Install dependencies | pip | Auto | Backend requirements |
| Run backend tests | pytest | On commit | With coverage |
| Check coverage | coverage | Auto | Fail if < 80% |
| Setup Node.js | actions/setup-node | Auto | Node 20 |
| Install frontend deps | npm | Auto | Frontend packages |
| Start services | uvicorn + vite | Auto | Backend + frontend |
| Run E2E tests | Playwright | On commit | UI tests |
| Generate reports | HTML/XML | Auto | Test results |
| Upload coverage | Codecov | Auto | Tracking |

### Alerting & Failure Handling Table
| Scenario/Event | Alert Type | Recipient | Action | Notes |
|---------------|------------|-----------|--------|-------|
| Test failure | GitHub Status | Dev Team | Investigate, fix | Blocks merge |
| Coverage below threshold | CI Failure | QA Lead | Update tests | Required for deployment |
| E2E failure | Slack/Email | Dev Team | Check UI changes | Immediate attention |
| Timeout | Pipeline log | DevOps | Optimize tests | Performance issue |

## 3. Metrics Collection

### Coverage Table
| Module/Feature | High-Risk Function | Automated? | Coverage % | Notes |
|---------------|-------------------|------------|------------|-------|
| Authentication | User auth | Yes | 91% | All auth flows |
| Courses | CRUD | Yes | 95% | Full operations |
| Assignments | Management | Yes | 81% | Most functions |
| Progress | Reporting | Yes | 100% | All endpoints |
| Schedule | Calendar | Yes | 68% | Core functions |
| **Total** | | | **86%** | Above threshold |

### Execution Time Table
| Module/Feature | Number of Test Cases | Execution Time per Test Case (sec) | Total Time | Notes |
|---------------|---------------------|-----------------------------------|------------|-------|
| Authentication | 7 | 0.2-0.5 | 2.5s | Fast API calls |
| Courses | 4 | 0.3-0.8 | 2.0s | DB operations |
| Assignments | 6 | 0.4-1.2 | 4.5s | Complex logic |
| Progress | 3 | 0.2-0.4 | 1.0s | Simple queries |
| Schedule | 2 | 0.8-1.5 | 2.0s | Date processing |
| **Total Backend** | **22** | | **8.17s** | Within limits |

### Defects Table
| Module/Feature | High-Risk Level | Expected Defects | Defects Found | Pass/Fail | Notes |
|---------------|----------------|------------------|---------------|-----------|-------|
| Authentication | High | 2 | 0 | Pass | Robust validation |
| Courses | High | 2 | 0 | Pass | Proper isolation |
| Assignments | High | 3 | 0 | Pass | Status tracking works |
| Progress | Medium | 1 | 0 | Pass | Accurate counts |
| Schedule | Medium | 1 | 0 | Pass | Date handling correct |

### Test Execution Log Table
| Test Case ID | Module/Feature | Execution Date/Time | Result | Defects | Execution Time | Notes |
|-------------|---------------|---------------------|--------|---------|----------------|-------|
| All API tests | Backend | 2024-04-03 | Pass | 0 | 8.17s | 22/22 passed |
| E2E tests | Frontend | 2024-04-03 | Pass | 0 | ~3min | 4/4 passed |

### Metrics Report
- **Bar Chart**: Coverage by module (Auth:91%, Courses:95%, Assignments:81%, Progress:100%, Schedule:68%)
- **Line Chart**: Execution times (Authentication:2.5s, Courses:2.0s, Assignments:4.5s, Progress:1.0s, Schedule:2.0s)
- **Pie Chart**: Test distribution (API:22 tests, E2E:4 tests)
- **Coverage Trend**: 86% overall, meeting 80% threshold

## 4. Documentation
See QA_Test_Strategy_Document.md for complete documentation.