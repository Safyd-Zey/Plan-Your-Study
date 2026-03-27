import pytest
from datetime import datetime, timedelta


def test_assignments_upcoming_overdue_and_by_date(authenticated_user, test_course_data):
    client, _ = authenticated_user

    course_resp = client.post('/api/courses', json=test_course_data)
    assert course_resp.status_code == 201
    course_id = course_resp.json()['id']

    now = datetime.utcnow()
    overdue_date = (now - timedelta(days=2)).isoformat()
    upcoming_date = (now + timedelta(days=4)).isoformat()
    by_date = (now + timedelta(days=1)).date().isoformat()

    # Overdue assignment
    overdue_payload = {
        'title': 'Overdue Task',
        'description': 'Done later',
        'deadline': overdue_date,
        'priority': 'high',
        'status': 'not_started',
        'course_id': course_id
    }
    r1 = client.post('/api/assignments', json=overdue_payload)
    assert r1.status_code == 200

    # Upcoming assignment
    upcoming_payload = {
        'title': 'Future Task',
        'description': 'Plan this week',
        'deadline': upcoming_date,
        'priority': 'medium',
        'status': 'not_started',
        'course_id': course_id
    }
    r2 = client.post('/api/assignments', json=upcoming_payload)
    assert r2.status_code == 200

    # Day target assignment
    target_payload = {
        'title': 'Daily Task',
        'description': 'For this day',
        'deadline': (now + timedelta(days=1)).isoformat(),
        'priority': 'low',
        'status': 'not_started',
        'course_id': course_id
    }
    r3 = client.post('/api/assignments', json=target_payload)
    assert r3.status_code == 200

    # upcoming endpoint
    resp_upcoming = client.get('/api/assignments/upcoming')
    assert resp_upcoming.status_code == 200
    assert any(a['title'] == 'Future Task' for a in resp_upcoming.json())

    # overdue endpoint
    resp_overdue = client.get('/api/assignments/overdue')
    assert resp_overdue.status_code == 200
    assert any(a['title'] == 'Overdue Task' for a in resp_overdue.json())

    # by-date endpoint
    resp_by_date = client.get(f'/api/assignments/by-date?date={by_date}')
    assert resp_by_date.status_code == 200
    assert any(a['title'] == 'Daily Task' for a in resp_by_date.json())


def test_schedule_calendar_endpoint(authenticated_user, test_course_data):
    client, _ = authenticated_user

    course_resp = client.post('/api/courses', json=test_course_data)
    course_id = course_resp.json()['id']

    now = datetime.utcnow()
    d1 = (now + timedelta(days=3)).replace(hour=14, minute=0, second=0, microsecond=0)

    assignment_payload = {
        'title': 'Calendar Assignment',
        'description': 'Check month',
        'deadline': d1.isoformat(),
        'priority': 'high',
        'status': 'not_started',
        'course_id': course_id
    }
    client.post('/api/assignments', json=assignment_payload)

    session_payload = {
        'title': 'Calendar Session',
        'description': 'Plan study',
        'start_time': d1.isoformat(),
        'end_time': (d1 + timedelta(hours=2)).isoformat(),
    }
    r = client.post('/api/schedule/study-sessions', json=session_payload)
    assert r.status_code == 200

    month = d1.strftime('%Y-%m')
    calendar_resp = client.get(f'/api/schedule/calendar?month={month}')
    assert calendar_resp.status_code == 200
    data = calendar_resp.json()
    assert data['month'] == month
    assert 'days' in data
    assert any(day['date'] == d1.date().isoformat() for day in data['days'])
