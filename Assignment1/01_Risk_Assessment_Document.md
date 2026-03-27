# Risk Assessment Document
## "Plan Your Study" System

**Project**: Plan Your Study - Study Planning & Task Management System  
**Date**: March 21, 2026  
**Team**: CSE-2507M (Assignment 1)  
**System Type**: Web Application (Frontend + Backend + Database)

---

## Executive Summary

This document identifies and prioritizes high-risk components of the "Plan Your Study" system based on probability of failure and impact on system functionality and user experience. Risk prioritization follows a matrix approach (Probability × Impact = Risk Level).

---

## 1. System Overview & Component Analysis

### System Architecture
- **Frontend**: React 18 + TypeScript (Port 3000)
- **Backend**: FastAPI (Port 8000)
- **Database**: SQLite (Study_planner.db)
- **Authentication**: JWT-based
- **Integration**: REST API communication

### Critical Components Identified

| Component | Type | Criticality | Users Affected |
|-----------|------|------------|-----------------|
| User Authentication | Backend/API | CRITICAL | All users |
| Course Management | Backend/API + Frontend | HIGH | All users |
| Assignment Management | Backend/API + Frontend | CRITICAL | All users |
| Subtask Management | Backend/API + Frontend | HIGH | Power users |
| Schedule/Calendar View | Frontend + API | MEDIUM | All users |
| Progress Tracking | Backend + Frontend | MEDIUM | All users |
| Database Layer | Infrastructure | CRITICAL | All users |
| API Endpoints | Backend | CRITICAL | All users |

---

## 2. Risk Assessment Matrix

### Risk Scoring Methodology
- **Probability**: 1 (Low) to 5 (High)
- **Impact**: 1 (Low) to 5 (Critical)
- **Risk Level** = Probability × Impact
  - 20-25: CRITICAL (High probability × High impact)
  - 12-16: HIGH (High probability × Medium impact OR Medium probability × High impact)
  - 6-11: MEDIUM
  - 1-5: LOW

---

## 3. CRITICAL RISK COMPONENTS (Priority 1)

### 3.1 User Authentication & Authorization
**Risk Level: 24 (CRITICAL)**
- **Probability**: 4 (High) | **Impact**: 5 (Critical)
- **Description**: Authentication failure = Complete system lockout for users
- **Failure Scenarios**:
  - Login credentials not validated correctly
  - JWT token expiration not handled
  - Password not hashed securely (bcrypt failure)
  - User data isolation breach (users see other users' data)
  - Session hijacking vulnerabilities
- **Business Impact**: 
  - User data exposure
  - Loss of user trust
  - Regulatory compliance issues
  - Complete system unusability
- **Current Implementation Risk**:
  ✓ JWT implemented with HS256
  ✓ Bcrypt password hashing
  ⚠ No rate limiting on login attempts
  ⚠ No password complexity validation
  ⚠ Token refresh mechanism missing
- **Recommended Tests**:
  - SQL injection in login form
  - Invalid token handling
  - User isolation testing
  - Password hashing verification
  - Rate limiting tests

---

### 3.2 Assignment & Course Data Management
**Risk Level: 20 (CRITICAL)**
- **Probability**: 4 (High) | **Impact**: 5 (Critical)
- **Description**: Loss or corruption of user's academic data = Loss of core system value
- **Failure Scenarios**:
  - Assignment deletion without confirmation
  - Data loss due to database errors
  - Incomplete assignments not saved
  - Concurrent update conflicts
  - Database connection failures
- **Business Impact**:
  - Users lose their study plans
  - Loss of critical deadlines
  - Reduced system reliability
- **Current Implementation Risk**:
  ✓ Database models properly defined
  ✓ Cascading deletes configured
  ⚠ No transaction validation
  ⚠ No backup mechanism
  ⚠ No data recovery mechanism
- **Recommended Tests**:
  - Create, Read, Update, Delete operations
  - Concurrent modification handling
  - Database constraint violations
  - Large dataset handling
  - Data persistence verification

---

### 3.3 API Endpoint Validation & Error Handling
**Risk Level: 20 (CRITICAL)**
- **Probability**: 4 (High) | **Impact**: 5 (Critical)
- **Description**: API errors can crash application or expose sensitive data
- **Failure Scenarios**:
  - Invalid input not validated (injection attacks)
  - Missing error responses (500 errors)
  - Malformed deadline dates
  - Missing required fields not caught
  - API timeout handling
- **Business Impact**:
  - Security vulnerabilities
  - Poor user experience
  - Incorrect data processing
- **Current Implementation Risk**:
  ✓ Pydantic validation in place
  ⚠ Limited error messages
  ⚠ No request timeout handling
  ⚠ Limited input sanitization
- **Recommended Tests**:
  - Invalid data type inputs
  - Missing required fields
  - Boundary value testing
  - SQL injection attempts
  - XSS prevention

---

## 4. HIGH RISK COMPONENTS (Priority 2)

### 4.1 Database Layer & Persistence
**Risk Level: 16 (HIGH)**
- **Probability**: 4 (High) | **Impact**: 4 (High)
- **Description**: Database failures affect all data operations
- **Failure Scenarios**:
  - SQLite database locks (concurrent access)
  - Database file corruption
  - Connection pool exhaustion
  - Query timeout
- **Implementation Risk**:
  ✓ SQLAlchemy ORM used
  ⚠ SQLite has limited concurrency
  ⚠ No connection pooling configuration
  ⚠ No query timeout settings
- **Recommended Tests**:
  - Concurrent database access
  - Large transaction handling
  - Database connection reliability
  - Query performance under load

---

### 4.2 Frontend-Backend Communication
**Risk Level: 15 (HIGH)**
- **Probability**: 3 (Medium) | **Impact**: 5 (Critical)
- **Description**: Communication failures = Non-functional system
- **Failure Scenarios**:
  - Network timeout during data submission
  - Invalid JSON responses
  - CORS policy violations
  - Missing API response handling
  - Axios interceptor failures
- **Implementation Risk**:
  ✓ Axios with token injection
  ⚠ No retry mechanism
  ⚠ Limited error handling
  ⚠ No offline mode
- **Recommended Tests**:
  - Network failure simulation
  - Slow API response handling
  - CORS compliance
  - Invalid JSON handling
  - Timeout recovery

---

### 4.3 Form Validation & User Input
**Risk Level: 15 (HIGH)**
- **Probability**: 4 (High) | **Impact**: 4 (High)
- **Description**: Invalid input leads to system errors or data corruption
- **Failure Scenarios**:
  - Past deadlines accepted
  - Empty course names saved
  - Invalid email formats
  - Duplicate course creation
  - Special characters in text fields
- **Implementation Risk**:
  ✓ Pydantic schemas defined
  ⚠ Limited frontend validation
  ⚠ No duplicate prevention
  ⚠ No deadline validation
- **Recommended Tests**:
  - Valid/invalid email formats
  - Empty field submission
  - Special character handling
  - Duplicate detection
  - Date/time boundary testing

---

## 5. MEDIUM RISK COMPONENTS (Priority 3)

### 5.1 Schedule & Calendar Functionality
**Risk Level: 12 (MEDIUM-HIGH)**
- **Probability**: 3 (Medium) | **Impact**: 4 (High)
- **Description**: Calendar display errors could cause confusion
- **Failure Scenarios**:
  - Incorrect date calculations
  - Timezone handling issues
  - Missing assignments on calendar
  - Week navigation failures
- **Recommended Tests**:
  - Calendar date accuracy
  - Week navigation
  - Timezone handling
  - Assignment display completeness

---

### 5.2 Progress Tracking & Calculations
**Risk Level: 10 (MEDIUM)**
- **Probability**: 3 (Medium) | **Impact**: 3-4 (Medium-High)
- **Description**: Incorrect progress metrics mislead users
- **Failure Scenarios**:
  - Wrong completion percentage
  - Missing assignments in stats
  - Incorrect status counting
- **Recommended Tests**:
  - Completion percentage accuracy
  - Status counting accuracy
  - Upcoming deadline calculations

---

### 5.3 Frontend UI/UX Responsiveness
**Risk Level**: 8 (MEDIUM)
- **Probability**: 2 (Low-Medium) | **Impact**: 4 (High)
- **Description**: Poor UX reduces adoption
- **Failure Scenarios**:
  - Broken layouts on mobile
  - Unresponsive buttons
  - Poor form usability
  - Navigation issues
- **Recommended Tests**:
  - Responsive design testing (mobile, tablet, desktop)
  - Touch interactions
  - Navigation flow
  - Button functionality

---

## 6. LOW-MEDIUM RISK COMPONENTS (Priority 4)

### 6.1 Subtask Management
**Risk Level**: 9 (MEDIUM)
- **Probability**: 2 (Low-Medium) | **Impact**: 4 (High)
- **Failure Scenarios**:
  - Subtask order not preserved
  - Subtask status not updating
  - Subtask deletion errors
- **Recommended Tests**:
  - Add/edit/delete subtasks
  - Status transitions
  - Order preservation

---

## 7. RISK PRIORITIZATION MATRIX

### Priority 1: CRITICAL (Test Immediately)
1. **User Authentication** (Risk: 24)
2. **Assignment Data Management** (Risk: 20)
3. **API Validation & Error Handling** (Risk: 20)
4. **Database Layer** (Risk: 16)
5. **Frontend-Backend Communication** (Risk: 15)
6. **Form Validation** (Risk: 15)

### Priority 2: HIGH (Test Second)
7. Schedule & Calendar (Risk: 12)
8. Progress Tracking (Risk: 10)
9. Subtask Management (Risk: 9)
10. UI/UX Responsiveness (Risk: 8)

---

## 8. TESTING EFFORT ESTIMATION

### High-Risk Testing (60% effort)
- Authentication & Security: 30 hours
- API & Database Testing: 40 hours
- Integration Testing: 25 hours
- **Subtotal: 95 hours**

### Medium-Risk Testing (30% effort)
- Schedule/Calendar: 15 hours
- Progress Tracking: 10 hours
- UI/UX: 20 hours
- **Subtotal: 45 hours**

### Low-Risk Testing (10% effort)
- Documentation: 5 hours
- Exploratory: 5 hours
- **Subtotal: 10 hours**

**Total Estimated Effort: 150 hours**
**Reasonable for 2 weeks with team of 2: 75 hours/person**

---

## 9. MODULE DEPENDENCY MAP

```
┌─────────────────────────────────────┐
│    User Authentication (CRITICAL)   │
└──────────────────┬──────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │Courses │ │Assignments│Progress│
   │(HIGH)  │ │(CRITICAL)  │(MEDIUM)│
   └────────┘ └────────┘ └────────┘
        │          │          │
        └──────────┼──────────┘
                   ▼
        ┌──────────────────────┐
        │  Database (CRITICAL) │
        └──────────────────────┘
```

All components depend on Database & Authentication. Failure in these causes cascading failures.

---

## 10. ASSUMPTIONS & RISK MITIGATION

### Assumptions
1. SQLite is acceptable for this stage (not production)
2. Team has basic QA knowledge
3. Two-week timeline is realistic for identified scope
4. System is fully functional before testing begins

### Risk Mitigation Strategies
1. **Critical Components**: Automated test scripts with high coverage (>80%)
2. **Regression Prevention**: Version control and CI/CD pipeline
3. **Data Protection**: Database backup procedures
4. **Documentation**: Clear test cases for reproducibility

---

## 11. DELIVERABLES

This Risk Assessment Document identifies:
- ✅ 10 critical components ranked by risk
- ✅ 6 CRITICAL priority modules (test immediately)
- ✅ Testing scenarios and failure modes
- ✅ Estimated testing effort (150 hours)
- ✅ Dependency mapping for strategic testing
- ✅ Baseline for measuring test coverage improvement

---

## Sign-off

**Document Version**: 1.0  
**Date**: March 21, 2026  
**Team**: CSE-2507M Assignment 1  
**Status**: Ready for QA Environment Setup & Test Strategy

**Next Steps**: 
1. Use this Risk Assessment to guide test strategy
2. Focus 60% of testing effort on Critical components
3. Set up automated tests for high-risk modules
4. Create baseline metrics for research paper

---
