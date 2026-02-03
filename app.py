"""Flask CRUD application for Employee Management System."""
from flask import Flask, request, jsonify
import database
import sqlite3

app = Flask(__name__)


def error_response(message, status_code=400):
    """Create error response."""
    return jsonify({'success': False, 'error': message}), status_code


def success_response(data=None, message=None, status_code=200):
    """Create success response."""
    response = {'success': True}
    if data is not None:
        response['data'] = data
    if message is not None:
        response['message'] = message
    return jsonify(response), status_code


@app.before_request
def before_request():
    """Initialize database before first request."""
    database.init_db()


@app.route('/employees', methods=['POST'])
def create_employee():
    """Create a new employee.
    
    Expected JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "department": "IT"
    }
    """
    data = request.get_json()
    
    if not data:
        return error_response('No JSON data provided', 400)
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    department = data.get('department', '').strip()
    
    if not name or not email or not department:
        return error_response('Missing required fields: name, email, department', 400)
    
    try:
        employee_id = database.create_employee(name, email, department)
        employee = database.get_employee(employee_id)
        return success_response(employee, 'Employee created successfully', 201)
    except sqlite3.IntegrityError:
        return error_response('Email already exists', 409)
    except Exception as e:
        return error_response(f'Error creating employee: {str(e)}', 500)


@app.route('/employees', methods=['GET'])
def get_employees():
    """Get all employees."""
    try:
        employees = database.get_all_employees()
        return success_response(employees)
    except Exception as e:
        return error_response(f'Error fetching employees: {str(e)}', 500)


@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get employee by ID."""
    try:
        employee = database.get_employee(employee_id)
        if not employee:
            return error_response('Employee not found', 404)
        return success_response(employee)
    except Exception as e:
        return error_response(f'Error fetching employee: {str(e)}', 500)


@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update employee.
    
    Expected JSON (all fields optional):
    {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "department": "HR"
    }
    """
    try:
        existing = database.get_employee(employee_id)
        if not existing:
            return error_response('Employee not found', 404)
        
        data = request.get_json()
        if not data:
            return error_response('No JSON data provided', 400)
        
        name = data.get('name', '').strip() if 'name' in data else None
        email = data.get('email', '').strip() if 'email' in data else None
        department = data.get('department', '').strip() if 'department' in data else None
        
        if not any([name, email, department]):
            return error_response('At least one field must be provided', 400)
        
        try:
            database.update_employee(employee_id, name, email, department)
            updated_employee = database.get_employee(employee_id)
            return success_response(updated_employee, 'Employee updated successfully')
        except sqlite3.IntegrityError:
            return error_response('Email already exists', 409)
            
    except Exception as e:
        return error_response(f'Error updating employee: {str(e)}', 500)


@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete employee."""
    try:
        existing = database.get_employee(employee_id)
        if not existing:
            return error_response('Employee not found', 404)
        
        database.delete_employee(employee_id)
        return success_response(None, 'Employee deleted successfully', 200)
    except Exception as e:
        return error_response(f'Error deleting employee: {str(e)}', 500)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return success_response({'status': 'healthy'})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return error_response('Endpoint not found', 404)


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return error_response('Internal server error', 500)


if __name__ == '__main__':
    database.init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
