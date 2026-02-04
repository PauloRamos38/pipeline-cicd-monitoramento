#!/usr/bin/env python3
"""
Flask REST API with 8 endpoints for task management
Includes Kubernetes health checks and Prometheus metrics
"""

from flask import Flask, request, jsonify
from datetime import datetime
import logging
import os
from logging_config import setup_logging, get_logger

# Initialize Flask app
app = Flask(__name__)

# Configure logging
setup_logging(app, level=os.getenv("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)

# In-memory storage for tasks
tasks = []
task_id_counter = 0

# ===========================
# Health Check Endpoints
# ===========================

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with service status"""
    return jsonify({
        'status': 'success',
        'service': 'Pipeline CI/CD API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'environment': os.getenv('ENVIRONMENT', 'development')
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Kubernetes liveness probe endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/ready', methods=['GET'])
def ready():
    """Kubernetes readiness probe endpoint"""
    return jsonify({
        'status': 'ready',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# ===========================
# Task Management Endpoints
# ===========================

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    logger.info('GET /tasks - Retrieved all tasks')
    return jsonify({
        'status': 'success',
        'tasks': tasks,
        'count': len(tasks)
    }), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    
    # Validate input
    if not data or 'title' not in data:
        logger.warning('POST /tasks - Missing title field')
        return jsonify({
            'status': 'error',
            'message': 'Title field is required'
        }), 400
    
    global task_id_counter
    task_id_counter += 1
    
    new_task = {
        'id': task_id_counter,
        'title': data.get('title'),
        'description': data.get('description', ''),
        'status': data.get('status', 'pending'),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    tasks.append(new_task)
    logger.info(f'POST /tasks - Created task {task_id_counter}')
    
    return jsonify({
        'status': 'success',
        'task': new_task,
        'message': 'Task created successfully'
    }), 201


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        logger.warning(f'GET /tasks/{task_id} - Task not found')
        return jsonify({
            'status': 'error',
            'message': f'Task {task_id} not found'
        }), 404
    
    logger.info(f'GET /tasks/{task_id} - Retrieved task {task_id}')
    return jsonify({
        'status': 'success',
        'task': task
    }), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a specific task"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        logger.warning(f'PUT /tasks/{task_id} - Task not found')
        return jsonify({
            'status': 'error',
            'message': f'Task {task_id} not found'
        }), 404
    
    data = request.get_json()
    
    # Update fields if provided
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'status' in data:
        task['status'] = data['status']
    
    task['updated_at'] = datetime.utcnow().isoformat()
    
    logger.info(f'PUT /tasks/{task_id} - Updated task {task_id}')
    
    return jsonify({
        'status': 'success',
        'task': task,
        'message': 'Task updated successfully'
    }), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a specific task"""
    global tasks
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        logger.warning(f'DELETE /tasks/{task_id} - Task not found')
        return jsonify({
            'status': 'error',
            'message': f'Task {task_id} not found'
        }), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    logger.info(f'DELETE /tasks/{task_id} - Deleted task {task_id}')
    
    return jsonify({
        'status': 'success',
        'message': f'Task {task_id} deleted successfully'
    }), 200


@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return jsonify({
        'status': 'success',
        'metrics': {
            'total_tasks': len(tasks),
            'pending_tasks': len([t for t in tasks if t['status'] == 'pending']),
            'completed_tasks': len([t for t in tasks if t['status'] == 'completed']),
            'api_version': '1.0.0'
        }
    }), 200


# ===========================
# Error Handlers
# ===========================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'Internal Server Error: {error}')
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    logger.info('Starting Flask API server on port 5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
