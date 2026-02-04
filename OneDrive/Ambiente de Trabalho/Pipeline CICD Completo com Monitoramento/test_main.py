#!/usr/bin/env python3
"""
Comprehensive test suite for Flask API
Tests all 8 endpoints with validation and error handling
"""

import pytest
from main import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ===========================
# Health Check Tests
# ===========================

def test_home(client):
    """Test home endpoint returns service information"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['service'] == 'Pipeline CI/CD API'
    assert 'version' in data
    assert 'timestamp' in data


def test_health(client):
    """Test health check endpoint for Kubernetes liveness probe"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


def test_ready(client):
    """Test readiness probe endpoint for Kubernetes readiness checks"""
    response = client.get('/ready')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ready'
    assert 'timestamp' in data


# ===========================
# Task Creation Tests
# ===========================

def test_create_task(client):
    """Test creating a new task with required fields"""
    payload = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'status': 'pending'
    }
    response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['task']['title'] == 'Test Task'
    assert data['task']['id'] == 1
    assert 'created_at' in data['task']


def test_create_task_without_title(client):
    """Test creating a task without title returns error"""
    payload = {
        'description': 'No title provided'
    }
    response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'Title field is required' in data['message']


# ===========================
# Task Retrieval Tests
# ===========================

def test_get_tasks(client):
    """Test retrieving all tasks"""
    # Create a task first
    client.post('/tasks', json={'title': 'Task 1'})
    client.post('/tasks', json={'title': 'Task 2'})
    
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['count'] == 2
    assert len(data['tasks']) == 2


def test_get_task_by_id(client):
    """Test retrieving a specific task by ID"""
    # Create a task
    create_response = client.post('/tasks', json={'title': 'Specific Task'})
    task_id = create_response.get_json()['task']['id']
    
    # Retrieve the task
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['task']['title'] == 'Specific Task'
    assert data['task']['id'] == task_id


def test_get_nonexistent_task(client):
    """Test retrieving a task that doesn't exist"""
    response = client.get('/tasks/99999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'not found' in data['message'].lower()


# ===========================
# Task Update Tests
# ===========================

def test_update_task(client):
    """Test updating an existing task"""
    # Create a task
    create_response = client.post('/tasks', json={'title': 'Original Title', 'status': 'pending'})
    task_id = create_response.get_json()['task']['id']
    
    # Update the task
    update_payload = {
        'title': 'Updated Title',
        'status': 'completed'
    }
    response = client.put(f'/tasks/{task_id}', json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['task']['title'] == 'Updated Title'
    assert data['task']['status'] == 'completed'


# ===========================
# Task Deletion Tests
# ===========================

def test_delete_task(client):
    """Test deleting a task"""
    # Create a task
    create_response = client.post('/tasks', json={'title': 'Task to Delete'})
    task_id = create_response.get_json()['task']['id']
    
    # Delete the task
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'deleted successfully' in data['message']
    
    # Verify it's deleted
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404


# ===========================
# Metrics Tests
# ===========================

def test_metrics(client):
    """Test metrics endpoint returns application statistics"""
    # Create some tasks
    client.post('/tasks', json={'title': 'Task 1', 'status': 'pending'})
    client.post('/tasks', json={'title': 'Task 2', 'status': 'completed'})
    
    response = client.get('/metrics')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'metrics' in data
    assert 'total_tasks' in data['metrics']
    assert 'pending_tasks' in data['metrics']
    assert 'completed_tasks' in data['metrics']
    assert data['metrics']['api_version'] == '1.0.0'
