"""
Performance Testing for Plan Your Study API
Uses Locust to simulate concurrent users and measure response times.

Tested modules (high-risk from midterm):
1. Authentication (POST /api/auth/register, /api/auth/login)
2. Courses CRUD (GET/POST /api/courses)
3. Assignments CRUD (GET/POST /api/assignments)
"""

import random
import string
import time
from locust import HttpUser, task, between, events
from locust.env import Environment


def random_suffix(n=8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


class PlanYourStudyUser(HttpUser):
    """Simulates a typical user of Plan Your Study application."""
    wait_time = between(0.5, 2)
    host = "http://127.0.0.1:8000"

    def on_start(self):
        """Register and login before starting tasks."""
        suffix = random_suffix()
        self.email = f"perfuser_{suffix}@test.com"
        self.username = f"perfuser_{suffix}"
        self.password = "PerfTest123!"
        self.token = None
        self.course_id = None
        self.assignment_id = None

        # Register
        resp = self.client.post(
            "/api/auth/register",
            json={
                "email": self.email,
                "username": self.username,
                "password": self.password,
            },
            name="/api/auth/register",
        )
        if resp.status_code == 200:
            self.token = resp.json().get("access_token")

        if not self.token:
            # Try login as fallback
            resp = self.client.post(
                "/api/auth/login",
                json={"email": self.email, "password": self.password},
                name="/api/auth/login",
            )
            if resp.status_code == 200:
                self.token = resp.json().get("access_token")

    def _auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    # ---------- AUTH tasks ----------
    @task(2)
    def login(self):
        self.client.post(
            "/api/auth/login",
            json={"email": self.email, "password": self.password},
            name="/api/auth/login",
        )

    @task(1)
    def login_wrong_password(self):
        with self.client.post(
            "/api/auth/login",
            json={"email": self.email, "password": "wrongpassword"},
            name="/api/auth/login [wrong_pw]",
            catch_response=True,
        ) as resp:
            if resp.status_code == 401:
                resp.success()

    # ---------- COURSES tasks ----------
    @task(3)
    def list_courses(self):
        self.client.get(
            "/api/courses",
            headers=self._auth_headers(),
            name="/api/courses [GET]",
        )

    @task(2)
    def create_course(self):
        resp = self.client.post(
            "/api/courses",
            json={
                "name": f"Course {random_suffix(4)}",
                "description": "Performance test course",
                "instructor": "Dr. Test",
            },
            headers=self._auth_headers(),
            name="/api/courses [POST]",
        )
        if resp.status_code == 201:
            self.course_id = resp.json().get("id")

    @task(1)
    def get_course_by_id(self):
        if self.course_id:
            with self.client.get(
                f"/api/courses/{self.course_id}",
                headers=self._auth_headers(),
                name="/api/courses/{id} [GET]",
                catch_response=True,
            ) as resp:
                if resp.status_code in (200, 404):
                    resp.success()

    # ---------- ASSIGNMENTS tasks ----------
    @task(3)
    def list_assignments(self):
        self.client.get(
            "/api/assignments",
            headers=self._auth_headers(),
            name="/api/assignments [GET]",
        )

    @task(2)
    def create_assignment(self):
        resp = self.client.post(
            "/api/assignments",
            json={
                "title": f"Assignment {random_suffix(4)}",
                "description": "Performance test assignment",
                "deadline": "2025-12-31T23:59:59",
                "priority": random.choice(["low", "medium", "high"]),
                "course_id": self.course_id,
            },
            headers=self._auth_headers(),
            name="/api/assignments [POST]",
        )
        if resp.status_code == 201:
            self.assignment_id = resp.json().get("id")

    # ---------- HEALTH ----------
    @task(1)
    def health_check(self):
        self.client.get("/health", name="/health")


class SpikeLoadUser(HttpUser):
    """Simulates spike load: rapid-fire requests without wait."""
    wait_time = between(0.1, 0.3)
    host = "http://127.0.0.1:8000"

    def on_start(self):
        suffix = random_suffix()
        self.email = f"spike_{suffix}@test.com"
        self.username = f"spike_{suffix}"
        self.password = "Spike123!"
        self.token = None
        resp = self.client.post(
            "/api/auth/register",
            json={"email": self.email, "username": self.username, "password": self.password},
            name="/api/auth/register [spike]",
        )
        if resp.status_code == 200:
            self.token = resp.json().get("access_token")

    def _auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(5)
    def list_courses_spike(self):
        self.client.get(
            "/api/courses",
            headers=self._auth_headers(),
            name="/api/courses [spike]",
        )

    @task(3)
    def health_spike(self):
        self.client.get("/health", name="/health [spike]")
