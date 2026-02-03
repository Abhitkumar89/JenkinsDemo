"""Pytest tests for Employee CRUD API."""
import pytest
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app as app_module
import database


@pytest.fixture
def client():
    """Create test client."""
    # Clear database before each test
    database.clear_database()
    database.init_db()
    
    app_module.app.config['TESTING'] = True
    
    with app_module.app.test_client() as client:
        yield client
    
    # Clean up after test
    database.clear_database()


@pytest.fixture
def sample_employee():
    """Sample employee data."""
    return {
        'name': 'John Doe',
        'email': 'john@example.com',
        'department': 'IT'
    }


class TestHealth:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test health endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['status'] == 'healthy'


class TestCreateEmployee:
    """Test CREATE operations."""

    def test_create_employee_success(self, client, sample_employee):
        """Test successful employee creation."""
        response = client.post('/employees', 
                              json=sample_employee,
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'John Doe'
        assert data['data']['email'] == 'john@example.com'
        assert data['data']['department'] == 'IT'
        assert data['data']['id'] is not None

    def test_create_employee_missing_fields(self, client):
        """Test creation with missing fields."""
        incomplete_data = {'name': 'John'}
        response = client.post('/employees',
                              json=incomplete_data,
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_create_employee_empty_json(self, client):
        """Test creation with empty JSON."""
        response = client.post('/employees',
                              json={},
                              content_type='application/json')
        assert response.status_code == 400

    def test_create_employee_duplicate_email(self, client, sample_employee):
        """Test creation with duplicate email."""
        # Create first employee
        client.post('/employees',
                   json=sample_employee,
                   content_type='application/json')
        
        # Try to create with same email
        duplicate = {
            'name': 'Jane Doe',
            'email': 'john@example.com',
            'department': 'HR'
        }
        response = client.post('/employees',
                              json=duplicate,
                              content_type='application/json')
        assert response.status_code == 409

    def test_create_multiple_employees(self, client):
        """Test creating multiple employees."""
        employees = [
            {'name': 'John', 'email': 'john@example.com', 'department': 'IT'},
            {'name': 'Jane', 'email': 'jane@example.com', 'department': 'HR'},
            {'name': 'Bob', 'email': 'bob@example.com', 'department': 'Sales'}
        ]
        
        for emp in employees:
            response = client.post('/employees',
                                  json=emp,
                                  content_type='application/json')
            assert response.status_code == 201


class TestReadEmployee:
    """Test READ operations."""

    def test_get_all_employees_empty(self, client):
        """Test getting all employees when empty."""
        response = client.get('/employees')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data'] == []

    def test_get_all_employees(self, client, sample_employee):
        """Test getting all employees."""
        # Create employee
        client.post('/employees',
                   json=sample_employee,
                   content_type='application/json')
        
        response = client.get('/employees')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['data']) == 1
        assert data['data'][0]['name'] == 'John Doe'

    def test_get_employee_by_id(self, client, sample_employee):
        """Test getting employee by ID."""
        # Create employee
        create_response = client.post('/employees',
                                     json=sample_employee,
                                     content_type='application/json')
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Get employee
        response = client.get(f'/employees/{employee_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['id'] == employee_id
        assert data['data']['name'] == 'John Doe'

    def test_get_employee_not_found(self, client):
        """Test getting non-existent employee."""
        response = client.get('/employees/9999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False


class TestUpdateEmployee:
    """Test UPDATE operations."""

    def test_update_employee_name(self, client, sample_employee):
        """Test updating employee name."""
        # Create employee
        create_response = client.post('/employees',
                                     json=sample_employee,
                                     content_type='application/json')
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Update employee
        update_data = {'name': 'Jane Doe'}
        response = client.put(f'/employees/{employee_id}',
                             json=update_data,
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['name'] == 'Jane Doe'
        assert data['data']['email'] == 'john@example.com'

    def test_update_employee_email(self, client, sample_employee):
        """Test updating employee email."""
        # Create employee
        create_response = client.post('/employees',
                                     json=sample_employee,
                                     content_type='application/json')
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Update email
        update_data = {'email': 'john.doe@example.com'}
        response = client.put(f'/employees/{employee_id}',
                             json=update_data,
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['email'] == 'john.doe@example.com'

    def test_update_employee_department(self, client, sample_employee):
        """Test updating employee department."""
        # Create employee
        create_response = client.post('/employees',
                                     json=sample_employee,
                                     content_type='application/json')
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Update department
        update_data = {'department': 'Management'}
        response = client.put(f'/employees/{employee_id}',
                             json=update_data,
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['department'] == 'Management'

    def test_update_multiple_fields(self, client, sample_employee):
        """Test updating multiple fields."""
        # Create employee
        create_response = client.post('/employees',
                                     json=sample_employee,
                                     content_type='application/json')
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Update multiple fields
        update_data = {
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'department': 'HR'
        }
        response = client.put(f'/employees/{employee_id}',
                             json=update_data,
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['name'] == 'Jane Smith'
        assert data['data']['email'] == 'jane.smith@example.com'
        assert data['data']['department'] == 'HR'

    def test_update_employee_not_found(self, client):
        """Test updating non-existent employee."""
        update_data = {'name': 'New Name'}
        response = client.put('/employees/9999',
                             json=update_data,
                             content_type='application/json')
        assert response.status_code == 404

    def test_update_employee_empty_update(self, client, sample_employee):
        """Test updating with empty data."""
        # Create employee
        create_response = client.post('/employees',
                                     json=sample_employee,
                                     content_type='application/json')
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Try to update with empty data
        response = client.put(f'/employees/{employee_id}',
                             json={},
                             content_type='application/json')
        assert response.status_code == 400

    def test_update_employee_duplicate_email(self, client):
        """Test updating to duplicate email."""
        # Create two employees
        emp1 = {'name': 'John', 'email': 'john@example.com', 'department': 'IT'}
        emp2 = {'name': 'Jane', 'email': 'jane@example.com', 'department': 'HR'}
        
        resp1 = client.post('/employees', json=emp1, content_type='application/json')
        resp2 = client.post('/employees', json=emp2, content_type='application/json')
        
        emp2_id = json.loads(resp2.data)['data']['id']
        
        # Try to update emp2 email to emp1's email
        response = client.put(f'/employees/{emp2_id}',
                             json={'email': 'john@example.com'},
                             content_type='application/json')
        assert response.status_code == 409


class TestDeleteEmployee:
    """Test DELETE operations."""

    def test_delete_employee(self, client, sample_employee):
        """Test deleting employee."""
        # Create employee
        create_response = client.post('/employees',
                                     json=sample_employee,
                                     content_type='application/json')
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Delete employee
        response = client.delete(f'/employees/{employee_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        
        # Verify deletion
        get_response = client.get(f'/employees/{employee_id}')
        assert get_response.status_code == 404

    def test_delete_employee_not_found(self, client):
        """Test deleting non-existent employee."""
        response = client.delete('/employees/9999')
        assert response.status_code == 404

    def test_delete_and_recreate(self, client, sample_employee):
        """Test deleting employee and recreating with same email."""
        # Create employee
        create_response = client.post('/employees',
                                     json=sample_employee,
                                     content_type='application/json')
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Delete employee
        client.delete(f'/employees/{employee_id}')
        
        # Create with same email
        response = client.post('/employees',
                              json=sample_employee,
                              content_type='application/json')
        assert response.status_code == 201


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_crud_workflow(self, client):
        """Test complete CRUD workflow."""
        # CREATE
        create_data = {
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'department': 'Finance'
        }
        create_response = client.post('/employees',
                                     json=create_data,
                                     content_type='application/json')
        assert create_response.status_code == 201
        employee_id = json.loads(create_response.data)['data']['id']
        
        # READ
        get_response = client.get(f'/employees/{employee_id}')
        assert get_response.status_code == 200
        
        # UPDATE
        update_data = {'department': 'Accounting'}
        update_response = client.put(f'/employees/{employee_id}',
                                    json=update_data,
                                    content_type='application/json')
        assert update_response.status_code == 200
        
        # DELETE
        delete_response = client.delete(f'/employees/{employee_id}')
        assert delete_response.status_code == 200
        
        # Verify deletion
        final_get = client.get(f'/employees/{employee_id}')
        assert final_get.status_code == 404

    def test_list_multiple_operations(self, client):
        """Test listing after multiple operations."""
        employees = [
            {'name': 'Alice', 'email': 'alice@example.com', 'department': 'IT'},
            {'name': 'Bob', 'email': 'bob@example.com', 'department': 'HR'},
            {'name': 'Charlie', 'email': 'charlie@example.com', 'department': 'Sales'}
        ]
        
        ids = []
        for emp in employees:
            resp = client.post('/employees', json=emp, content_type='application/json')
            ids.append(json.loads(resp.data)['data']['id'])
        
        # Get all
        list_response = client.get('/employees')
        assert len(json.loads(list_response.data)['data']) == 3
        
        # Delete one
        client.delete(f'/employees/{ids[0]}')
        
        # Get all again
        list_response = client.get('/employees')
        assert len(json.loads(list_response.data)['data']) == 2
