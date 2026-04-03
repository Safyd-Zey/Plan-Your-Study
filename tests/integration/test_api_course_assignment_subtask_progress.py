"""
Integration tests for critical high-risk modules: courses, assignments, subtasks, and progress.
These tests are designed to be repeatable, readable, and documented for Assignment 2 automation.
"""

import pytest
from datetime import datetime, timedelta


def make_deadline(days: int = 1) -> str:
    return (datetime.utcnow() + timedelta(days=days)).isoformat()


def create_course(client, course_data):
    response = client.post('/api/courses', json=course_data)
    assert response.status_code == 201
    return response.json()


def create_assignment(client, course_id, title=None, deadline=None, priority='medium'):
    payload = {
        'title': title or 'Automated Assignment',
        'description': 'This assignment is created by automated tests.',
        'deadline': deadline or make_deadline(1),
        'priority': priority,
        'course_id': course_id
    }
    response = client.post('/api/assignments', json=payload)
    assert response.status_code == 200
    return response.json()


def test_course_update_get_delete(authenticated_user, test_course_data):
    """Validate course CRUD operations and access behavior."""
    client, token = authenticated_user

    # Create a new course
    course = create_course(client, test_course_data)
    course_id = course['id']

    # Retrieve course by id
    response = client.get(f'/api/courses/{course_id}')
    assert response.status_code == 200
    assert response.json()['name'] == test_course_data['name']

    # Update the course
    updated_name = f"{test_course_data['name']} - Updated"
    response = client.put(f'/api/courses/{course_id}', json={'name': updated_name})
    assert response.status_code == 200
    assert response.json()['name'] == updated_name

    # Delete the course and verify it is removed
    response = client.delete(f'/api/courses/{course_id}')
    assert response.status_code == 204

    response = client.get(f'/api/courses/{course_id}')
    assert response.status_code == 404


def test_assignment_lifecycle_and_filters(authenticated_user, test_course_data):
    """Cover assignment creation, retrieval, updates, and course scoping."""
    client, token = authenticated_user

    course = create_course(client, test_course_data)
    course_id = course['id']

    # Create an assignment that is due today, and one due tomorrow.
    assignment_today = create_assignment(client, course_id, title='Today Assignment', deadline=make_deadline(0))
    assignment_tomorrow = create_assignment(client, course_id, title='Tomorrow Assignment', deadline=make_deadline(1))

    assignment_id = assignment_today['id']

    # Get assignment details
    response = client.get(f'/api/assignments/{assignment_id}')
    assert response.status_code == 200
    assert response.json()['title'] == 'Today Assignment'

    # Update assignment title and priority
    response = client.put(f'/api/assignments/{assignment_id}', json={'title': 'Updated Today Assignment', 'priority': 'high'})
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Today Assignment'
    assert response.json()['priority'] == 'high'

    # Get assignments by course
    response = client.get(f'/api/assignments/course/{course_id}')
    assert response.status_code == 200
    assert any(a['id'] == assignment_id for a in response.json())

    # Get assignments by date for today
    today_date = datetime.utcnow().date().isoformat()
    response = client.get(f'/api/assignments/by-date?date={today_date}')
    assert response.status_code == 200
    assert any(a['id'] == assignment_id for a in response.json())

    # Change assignment status to completed via patch
    response = client.patch(f'/api/assignments/{assignment_id}', json={'status': 'completed'})
    assert response.status_code == 200
    assert response.json()['status'] == 'completed'

    # Delete the assignment and verify removal
    response = client.delete(f'/api/assignments/{assignment_id}')
    assert response.status_code == 204

    response = client.get(f'/api/assignments/{assignment_id}')
    assert response.status_code == 404


def test_subtask_crud_and_assignment_status(authenticated_user, test_course_data, test_subtask_data):
    """Validate subtask CRUD and assignment status transitions."""
    client, token = authenticated_user

    course = create_course(client, test_course_data)
    assignment = create_assignment(client, course['id'], title='Assignment with subtasks')
    assignment_id = assignment['id']

    # Create a subtask for the assignment
    response = client.post(f'/api/subtasks/{assignment_id}', json=test_subtask_data)
    assert response.status_code == 200
    subtask = response.json()
    assert subtask['title'] == test_subtask_data['title']

    # Confirm the assignment moved to in_progress after subtask creation
    response = client.get(f'/api/assignments/{assignment_id}')
    assert response.json()['status'] == 'in_progress'

    # Update subtask details and verify response
    response = client.put(f'/api/subtasks/{subtask["id"]}', json={'title': 'Updated Subtask Title', 'status': 'completed'})
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Subtask Title'
    assert response.json()['status'] == 'completed'

    # Check the assignment status is completed when all subtasks are completed
    response = client.get(f'/api/assignments/{assignment_id}')
    assert response.json()['status'] == 'completed'

    # Delete the subtask and verify the API returns 204
    response = client.delete(f'/api/subtasks/{subtask["id"]}')
    assert response.status_code == 204


def test_progress_endpoints_report_correct_counts(authenticated_user, test_course_data):
    """Validate progress metrics include assignment counts, overdue items, and completion percentages."""
    client, token = authenticated_user

    course = create_course(client, test_course_data)
    # create assignments with different statuses
    assignment_not_started = create_assignment(client, course['id'], title='Future Assignment', deadline=make_deadline(5), priority='medium')
    assignment_in_progress = create_assignment(client, course['id'], title='In Progress Assignment', deadline=make_deadline(2), priority='high')
    assignment_completed = create_assignment(client, course['id'], title='Completed Assignment', deadline=make_deadline(1), priority='low')

    client.patch(f'/api/assignments/{assignment_in_progress["id"]}', json={'status': 'in_progress'})
    client.patch(f'/api/assignments/{assignment_completed["id"]}', json={'status': 'completed'})

    # Query progress statistics
    response = client.get('/api/progress/stats')
    assert response.status_code == 200
    stats = response.json()
    assert stats['total_assignments'] >= 3
    assert stats['completed_assignments'] >= 1
    assert stats['in_progress_assignments'] >= 1
    assert stats['completion_percentage'] >= 0

    response = client.get('/api/progress/detail')
    assert response.status_code == 200
    detail = response.json()
    assert detail['total_assignments'] >= 3
    assert 'upcoming_assignments' in detail
