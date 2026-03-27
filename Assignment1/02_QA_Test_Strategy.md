# QA Test Strategy Document
## "Plan Your Study" System - Assignment 1

**Project**: Plan Your Study - Study Planning & Task Management System  
**Team**: CSE-2507M  
**Date**: March 21, 2026  
**Test Lead**: QA Team  
**Duration**: 2 Weeks

---

## 1. Executive Summary

This document outlines the comprehensive testing strategy for the "Plan Your Study" system. Based on the Risk Assessment, testing will focus on critical components (Authentication, API, Database) with 60% effort allocation, ensuring robust coverage of high-impact areas while establishing baseline metrics for the research paper.

---

## 2. Project Scope & Objectives

### 2.1 Scope Definition

**In Scope:**
- Backend API endpoints (20+ endpoints)
- Frontend UI/UX (all pages and components)
- Database persistence layer
- User authentication flow
- Data integrity & validation
- Integration testing (Frontend ↔ Backend)
- Security testing (basic)

**Out of Scope:**
- Performance/load testing (future assignment)
- Mobile app testing (N/A)
- Third-party integrations (none exist)
- Production deployment testing

### 2.2 Test Objectives
1. Validate core functionality (authentication, data management)
2. Ensure API contracts are honored
3. Verify data integrity and persistence
4. Identify defects in high-risk modules
5. Establish baseline metrics for research paper
6. Create reproducible test cases for future regression testing

### 2.3 Quality Criteria (Definition of Done)
- **Critical Components**: 80%+ test coverage
- **High-Risk Components**: 70%+ test coverage
- **Test Pass Rate**: >95% of tests should pass
- **Defect Severity**: 0 Critical/Blocker defects at end of testing
- **Documentation**: 100% of tests documented with expected results

---

## 3. Test Approach

### 3.1 Testing Strategy Overview

```
├── Manual Testing (40% effort)
│   ├── Exploratory testing
│   ├── UI/UX testing
│   ├── User flow testing
│   └── Edge case testing
│
├── Automated Testing (50% effort)
│   ├── API testing (Postman/Pytest)
│   ├── Unit tests (backend functions)
│   ├── Integration tests (Frontend ↔ Backend)
│   └── Database tests
│
└── Security Testing (10% effort)
    ├── Input validation
    ├── Authentication/Authorization
    └── Common vulnerabilities (OWASP Top 10 basics)
```

### 3.2 Testing Levels

#### Level 1: Unit Testing (Backend)
- **Target**: Individual API endpoints, database models
- **Tool**: Pytest
- **Coverage Goal**: 70%+
- **Examples**:
  - Test user registration with valid/invalid data
  - Test assignment creation with various priorities
  - Test password hashing function

#### Level 2: Integration Testing
- **Target**: Frontend ↔ Backend ↔ Database
- **Tool**: Postman, Pytest, Manual testing
- **Coverage Goal**: 75%+
- **Examples**:
  - Create course → Create assignment → View on dashboard
  - Login → Create assignment → Logout → Verify data persists
  - Edit assignment → Verify frontend reflects change

#### Level 3: System/E2E Testing
- **Target**: Complete user workflows
- **Tool**: Manual testing, Postman scripts
- **Coverage Goal**: 80%+
- **Examples**:
  - Complete user journey: Register → Create courses → Add assignments → View progress
  - Error scenarios: Network failure, invalid input, concurrent updates

#### Level 4: UI/UX Testing
- **Target**: Frontend components, responsiveness, usability
- **Tool**: Manual testing on multiple browsers/devices
- **Examples**:
  - Form submission handling
  - Navigation between pages
  - Mobile responsiveness (3+ screen sizes)

### 3.3 Test Types & Coverage

| Test Type | Level | Approach | Coverage % |
|-----------|-------|----------|------------|
| API Endpoint Tests | Unit/Integration | Automated (Pytest) | 80% (Critical APIs) |
| Authentication Tests | Unit/Integration | Automated (Pytest) | 85% (Critical) |
| Database Tests | Unit | Automated (Pytest) | 75% |
| Form Validation | Unit/System | Manual + Automated | 70% |
| UI/UX Tests | System | Manual | 80% (Critical flows) |
| Security Tests | System | Manual + Automated | 60% (OWASP) |
| Integration Tests | Integration | Automated (Postman/Pytest) | 75% |
| Regression Tests | All | Automated (CI/CD) | 80% |

---

## 4. Test Scope by Component

### 4.1 Critical Priority Components (60% effort)

#### Authentication Module (30 hours)
**Test Cases:**
- Registration: Valid email, invalid email, duplicate email, weak password, missing fields
- Login: Correct credentials, wrong password, non-existent user, locked account
- JWT: Token generation, token expiration, token refresh, invalid token
- User Isolation: User A cannot access User B's data
- Security: Password hashing verification, no plaintext passwords

**Tools**: Pytest, Postman
**Automation Level**: 100% automated

#### API Endpoints (25 hours)
**Test Cases:**
- Courses API: Create, Read, Update, Delete with role/ownership validation
- Assignments API: CRUD operations, priority handling, deadline validation
- Subtasks API: Add/remove/update subtasks, order persistence
- Progress API: Calculation accuracy, correct status counting
- Schedule API: Correct date grouping, deadline retrieval

**Tools**: Pytest, Postman
**Automation Level**: 95% automated

#### Database Layer (15 hours)
**Test Cases:**
- Data persistence: Create data, restart app, verify data exists
- Constraints: Unique constraints, foreign key constraints, default values
- Transactions: Multiple simultaneous writes, rollback scenarios
- Relationships: Course-Assignment links, Assignment-Subtasks links

**Tools**: Pytest, SQLite command-line
**Automation Level**: 80% automated

#### Form Validation (15 hours)
**Test Cases:**
- Required fields: All forms must validate required fields
- Data types: Email format, datetime format, numeric priority
- Duplicates: Prevent duplicate course names for same user
- Boundaries: Very long text, special characters, null values
- Timestamps: Past dates, far future dates, timezone handling

**Tools**: Manual testing, Postman (for API validation)
**Automation Level**: 60% manual, 40% automated

---

### 4.2 High-Risk Components (30% effort)

#### Frontend-Backend Communication (15 hours)
**Test Cases:**
- Network errors: Simulate timeout, 400/500 errors
- CORS: Verify correct CORS headers
- Retry logic: Verify failed requests don't break UI
- Error messages: User sees appropriate error feedback
- State consistency: UI reflects API changes correctly

**Tools**: Manual testing, Developer tools, Postman
**Automation Level**: 50% automated

#### Schedule & Calendar (10 hours)
**Test Cases:**
- Date calculations: Correct week grouping
- Navigation: Previous/Next week buttons work correctly
- Display: Assignments appear on correct dates and times
- Timezone: Verify no timezone issues (future consideration)

**Tools**: Manual testing
**Automation Level**: 30% automated

#### Progress Tracking (5 hours)
**Test Cases:**
- Percentage calculation: Correct completion percentage
- Status counts: Accurate counts of completed/pending/not-started
- Upcoming deadlines: Correct deadline retrieval and sorting

**Tools**: Manual testing, Postman verification
**Automation Level**: 40% automated

---

### 4.3 Medium-Risk Components (10% effort)

#### UI/UX & Responsiveness (10 hours)
**Test Cases:**
- Responsive design: Test on 3+ screen sizes (Desktop, Tablet, Mobile)
- Navigation: All navigation links functional
- Layout: No broken layouts, proper spacing
- Forms: Form submission works on all devices
- Loading states: Proper loading indicators shown

**Tools**: Manual testing on real devices/browsers
**Automation Level**: 20% automated (screenshot comparison)

---

## 5. Test Tools & Technology Stack

### 5.1 Testing Tools

| Tool | Purpose | Category | Status |
|------|---------|----------|--------|
| **Pytest** | Python unit/integration testing | Automation | ✓ To Install |
| **Postman** | API testing, documentation | Automation | ✓ To Install |
| **REST Client (VS Code)** | Quick API testing | Automation | ✓ To Install |
| **Selenium/Playwright** | Frontend automation (optional) | Automation | ⏳ Future |
| **GitHub Actions** | CI/CD pipeline | Automation | ✓ To Configure |
| **SQLite CLI** | Database testing | Tools | ✓ Command-line |
| **Browser DevTools** | Frontend debugging | Tools | ✓ Built-in |
| **Insomnia/Postman** | API documentation | Tools | ✓ To Install |

### 5.2 Testing Framework Structure

```
tests/
├── unit/
│   ├── test_auth.py              # Authentication unit tests
│   ├── test_models.py            # Database model tests
│   └── test_schemas.py           # Pydantic schema tests
├── integration/
│   ├── test_api_courses.py       # Course endpoint integration tests
│   ├── test_api_assignments.py   # Assignment endpoint tests
│   ├── test_api_auth.py          # Auth flow tests
│   └── test_database.py          # Database integration tests
├── e2e/
│   ├── test_user_workflows.py    # End-to-end user journeys
│   └── test_data_flow.py         # Cross-module data flow
├── security/
│   ├── test_injection.py         # SQL injection, XSS tests
│   └── test_auth_security.py     # Authentication security tests
├── conftest.py                   # Pytest fixtures and configuration
└── README.md                     # Test documentation
```

### 5.3 Test Execution Flow

```
┌─────────────────────────────────────┐
│   Developer: Code Changes           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Git Push → GitHub                 │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   GitHub Actions CI/CD Triggers     │
└──────────────┬──────────────────────┘
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
   Lint    Unit Tests  Integration
               │        │
      ┌────────┴────────┘
      ▼
   All Pass? → Yes → Deploy to Staging → Run E2E
               └─→ No → Report Failure
```

---

## 6. Test Hardware & Software Requirements

### 6.1 System Requirements
- **OS**: Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- **RAM**: 8GB minimum (4GB for tests)
- **Storage**: 2GB for tools and test data
- **Python**: 3.8+
- **Node.js**: 16+

### 6.2 Required Software
- Git
- Python 3.8+
- Node.js 16+
- Visual Studio Code (recommended)
- Postman or Insomnia
- Chrome/Firefox browsers

---

## 7. Test Data Strategy

### 7.1 Test Data Sets

**Dataset 1: Happy Path**
- 3 courses (Math, CS, Physics)
- 5 assignments total
- 2-3 subtasks per assignment
- Complete workflow: Register → Create → View → Update → Mark Complete

**Dataset 2: Edge Cases**
- Very long assignment names (>200 chars)
- Special characters in descriptions
- Past deadlines
- Concurrent assignment creation
- Large number of subtasks (>50)

**Dataset 3: Error Cases**
- Missing required fields
- Invalid email formats
- Duplicate course names
- Negative priorities
- Null values in critical fields

### 7.2 Test Data Maintenance
- Each test creates fresh data
- Automatic cleanup after test completion
- Separate test database (can reset)
- No deletion of test evidence for analysis

---

## 8. CI/CD Pipeline Configuration

### 8.1 Automated Testing Pipeline Goals
1. **On Each Commit**: Run unit tests (5 min max)
2. **On Each PR**: Run unit + integration tests (15 min max)
3. **On Merge to Main**: Full test suite (30 min max)
4. **Daily Schedule**: Full regression suite (60 min max)

### 8.2 Pipeline Stages

```yaml
# GitHub Actions Workflow
name: QA Test Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt pytest pytest-cov
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov
      - name: Run integration tests
        run: pytest tests/integration/ -v
      - name: Generate coverage report
        run: pytest --cov=. --cov-report=html
```

---

## 9. Metrics & KPIs for Research Paper

### 9.1 Metrics to Collect (Baseline)

| Metric | Purpose | Collection Method |
|--------|---------|-------------------|
| **Test Coverage %** | Code coverage | Pytest --cov |
| **Pass Rate %** | Test reliability | Test results count |
| **# Test Cases** | Testing scope | Count of test files |
| **# Critical Defects** | Quality baseline | Defect log |
| **# High Defects** | Quality baseline | Defect log |
| **Test Execution Time** | Efficiency | Pipeline logs |
| **Defect Detection Rate** | Effectiveness | Found defects / potential |
| **API Response Time** | Performance | API logs (ms) |

### 9.2 Baseline Metrics (Week 1-2)
- **Planned Test Cases**: 120+
- **Target Coverage**: 75%+ (critical), 60%+ (overall)
- **Expected Defect Rate**: 10-15 defects (acceptance testing level)
- **Planned Effort**: 150 hours
- **Team Size**: 2 people

---

## 10. Risk-Based Testing Approach

### 10.1 Testing Priority Matrix
```
               ▲
      Impact   │      Critical     High
               │    (Test first)  (Test second)
               │
               │    High          Medium
               │    (Test 3rd)    (Test 4th)
               ├─────────────────────────────► Probability
               │ Low   Medium   High
```

### 10.2 Test Execution Order
1. **Phase 1** (Days 1-3): Critical components (Authentication, API, Database)
2. **Phase 2** (Days 4-7): High-risk components (Communication, Validation)
3. **Phase 3** (Days 8-11): Medium-risk components (UI, Schedule)
4. **Phase 4** (Days 12-14): Regression testing & data collection

---

## 11. Quality Gates & Acceptance Criteria

### 11.1 Exit Criteria (Must Pass)
- ✅ All CRITICAL tests pass (100%)
- ✅ Authentication security verified
- ✅ No data loss scenarios found
- ✅ API contracts validated
- ✅ Database integrity verified
- ✅ 75%+ code coverage for critical modules

### 11.2 Suspension Criteria (Stop & Fix)
- ❌ Critical defect found (blocks other tests)
- ❌ Authentication broken
- ❌ Database corruption
- ❌ Complete feature failure
- ❌ Security vulnerability discovered

---

## 12. Test Deliverables & Documentation

### 12.1 Deliverables
1. ✅ Test Plan (this document)
2. ✅ Test Cases repository (in GitHub)
3. ✅ Test Scripts (Pytest files)
4. ✅ Postman Collection (API tests)
5. ✅ Test Reports (HTML coverage, JUnit XML)
6. ✅ Defect Log (with severity, status, resolution)
7. ✅ Baseline Metrics Report
8. ✅ Screenshots & Evidence

### 12.2 Test Documentation Standards
- Every test case includes:
  - ID (TC-001, TC-002, etc.)
  - Title & description
  - Preconditions
  - Test steps
  - Expected results
  - Actual results
  - Pass/Fail status
  - Evidence (screenshots if applicable)

---

## 13. Roles & Responsibilities

| Role | Responsibility | Hours |
|------|-----------------|-------|
| QA Lead | Test strategy, coordination, reporting | 20 |
| Test Automation Engineer | Pytest, CI/CD setup | 35 |
| Manual Tester | UI/UX, exploratory testing | 35 |
| QA Engineer 2 | Integration, API testing | 35 |
| Backend Developer Support | Debugging, investigation | 10 |
| **Total** | | **135 hours** |

---

## 14. Schedule & Timeline

### Week 1
| Day | Activity | Deliverable |
|-----|----------|-------------|
| Day 1 | Environment setup, tool installation | QA Environment Report |
| Day 2 | Write authentication tests | test_auth.py (20 tests) |
| Day 3 | Write API tests (courses, assignments) | test_api_*.py (40 tests) |
| **Week 1 Exit** | Execute tests, identify defects | Initial defect report |

### Week 2
| Day | Activity | Deliverable |
|-----|----------|-------------|
| Day 4-5 | Integration & E2E testing | 30+ integration tests passing |
| Day 6-7 | Security & validation testing | Security report, validation tests |
| Day 8 | UI/UX manual testing | Test results, screenshots |
| Day 9-10 | Regression testing, final checks | Final test report |
| **Week 2 Exit** | Complete metrics & documentation | Research paper data ready |

---

## 15. Risk Mitigation

### Risks & Mitigation Strategies

| Risk | Probability | Mitigation |
|------|-------------|-----------|
| System changes mid-testing | Medium | Version-controlled tests, separate branches |
| Test environment instability | Medium | Containerize with Docker |
| Incomplete requirement understanding | Low | Weekly check-ins, requirement review |
| Tool learning curve | Medium | Pre-setup, team training |
| Data loss during testing | Low | Backup test database before/after runs |

---

## 16. Success Criteria for Assignment 1

**This strategy is successful if:**
- ✅ 120+ test cases created
- ✅ 75%+ critical module coverage achieved
- ✅ CI/CD pipeline functional
- ✅ Baseline metrics documented
- ✅ 0 unresolved Critical defects
- ✅ All deliverables submitted
- ✅ Research paper foundation ready (data, screenshots, methodology)

---

## Sign-off

**Document Version**: 1.0  
**Date**: March 21, 2026  
**Approved by**: QA Team  
**Next Document**: QA Environment Setup Report

**Ready to proceed with**: 
1. QA Environment Setup
2. Tool Installation
3. Test Development

---
