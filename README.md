# Employee Management System (EMS)

A simple, Flask-based REST API for Employee CRUD operations with SQLite database and comprehensive pytest tests.

## Features

- **CRUD Operations**: Create, Read, Update, Delete employees
- **REST API**: Full REST endpoints for all operations
- **SQLite Database**: Lightweight, file-based database
- **Pytest Tests**: Comprehensive test coverage for all endpoints
- **Jenkins Compatible**: Minimal dependencies, easy CI/CD integration

## Tech Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite
- **Testing**: Pytest
- **Dependencies**: Listed in `requirements.txt`

## Project Structure

```
EMS/
├── app.py              # Flask application and API endpoints
├── database.py         # Database operations and initialization
├── models.py           # Employee data model
├── requirements.txt    # Python dependencies
├── employees.db        # SQLite database (auto-created)
├── tests/
│   └── test_app.py     # Pytest test suite
└── README.md           # This file
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Navigate to project directory**:

   ```bash
   cd EMS
   ```

2. **Create virtual environment (optional but recommended)**:

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the Flask server:

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Health check:

```bash
curl http://localhost:5000/health
```

## Running Tests

### Run all tests:

```bash
pytest
```

### Run tests with verbose output:

```bash
pytest -v
```

### Run tests with coverage report:

```bash
pytest --cov=. tests/
```

### Run specific test class:

```bash
pytest tests/test_app.py::TestCreateEmployee -v
```

### Run specific test function:

```bash
pytest tests/test_app.py::TestCreateEmployee::test_create_employee_success -v
```

## API Endpoints

### 1. Create Employee

**Endpoint**: `POST /employees`

**Request**:

```bash
curl -X POST http://localhost:5000/employees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "department": "IT"
  }'
```

**Response** (201 Created):

```json
{
  "success": true,
  "message": "Employee created successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "department": "IT",
    "created_at": "2024-01-15T10:30:00.123456"
  }
}
```

### 2. Get All Employees

**Endpoint**: `GET /employees`

**Request**:

```bash
curl http://localhost:5000/employees
```

**Response** (200 OK):

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "department": "IT",
      "created_at": "2024-01-15T10:30:00.123456"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "department": "HR",
      "created_at": "2024-01-15T10:31:00.123456"
    }
  ]
}
```

### 3. Get Employee by ID

**Endpoint**: `GET /employees/<id>`

**Request**:

```bash
curl http://localhost:5000/employees/1
```

**Response** (200 OK):

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "department": "IT",
    "created_at": "2024-01-15T10:30:00.123456"
  }
}
```

**Response** (404 Not Found):

```json
{
  "error": "Employee not found",
  "success": false
}
```

### 4. Update Employee

**Endpoint**: `PUT /employees/<id>`

**Request** (update all fields):

```bash
curl -X PUT http://localhost:5000/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "department": "Management"
  }'
```

**Request** (update specific field):

```bash
curl -X PUT http://localhost:5000/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "department": "HR"
  }'
```

**Response** (200 OK):

```json
{
  "success": true,
  "message": "Employee updated successfully",
  "data": {
    "id": 1,
    "name": "John Smith",
    "email": "john.smith@example.com",
    "department": "Management",
    "created_at": "2024-01-15T10:30:00.123456"
  }
}
```

### 5. Delete Employee

**Endpoint**: `DELETE /employees/<id>`

**Request**:

```bash
curl -X DELETE http://localhost:5000/employees/1
```

**Response** (200 OK):

```json
{
  "success": true,
  "message": "Employee deleted successfully"
}
```

**Response** (404 Not Found):

```json
{
  "error": "Employee not found",
  "success": false
}
```

## Example Workflows

### Create and List Employees

```bash
# Create first employee
curl -X POST http://localhost:5000/employees \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "email": "alice@example.com", "department": "Finance"}'

# Create second employee
curl -X POST http://localhost:5000/employees \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob Wilson", "email": "bob@example.com", "department": "Sales"}'

# List all employees
curl http://localhost:5000/employees
```

### Update Department

```bash
# Update employee 1's department
curl -X PUT http://localhost:5000/employees/1 \
  -H "Content-Type: application/json" \
  -d '{"department": "Accounting"}'
```

### Delete Employee

```bash
# Delete employee 2
curl -X DELETE http://localhost:5000/employees/2
```

## Database Details

### Schema

The application automatically creates a SQLite database with the following schema:

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_email ON employees(email);
```

### Database File

- **Location**: `employees.db` (in project root)
- **Auto-created**: Yes, on first application run
- **Backup**: No automatic backups

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK**: Successful GET/PUT/DELETE
- **201 Created**: Successful POST
- **400 Bad Request**: Missing required fields or invalid data
- **404 Not Found**: Employee not found
- **409 Conflict**: Email already exists
- **500 Internal Server Error**: Server error

## Testing

### Test Coverage

The test suite includes:

- **Health Check Tests**: API health endpoint
- **Create Tests**: Employee creation, validation, duplicate handling
- **Read Tests**: Get all employees, get by ID, not found handling
- **Update Tests**: Single and multiple field updates, validation, duplicates
- **Delete Tests**: Employee deletion, non-existent records
- **Integration Tests**: Full CRUD workflows

### Running Tests for Jenkins

```bash
# Simple pytest run
pytest

# With JUnit XML output for Jenkins
pytest --junit-xml=test-results.xml

# With coverage report
pytest --cov=. --cov-report=xml
```

## Troubleshooting

### Port Already in Use

If port 5000 is already in use:

```bash
# Run on different port (modify app.py)
# Change: app.run(port=5000)
# To: app.run(port=5001)
```

### Database Locked Error

Delete `employees.db` and restart:

```bash
rm employees.db
python app.py
```

### Import Errors

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## API Response Format

All responses follow a consistent JSON format:

**Success Response**:

```json
{
  "success": true,
  "data": {...},
  "message": "Optional message"
}
```

**Error Response**:

```json
{
  "success": false,
  "error": "Error message"
}
```

## Notes

- Email addresses must be unique across all employees
- All fields (name, email, department) are required for creation
- At least one field must be provided for updates
- The API runs on `0.0.0.0:5000` for Docker/Jenkins compatibility
- Debug mode is disabled in production

## Contributing

For improvements or bug fixes, follow these steps:

1. Create a new branch
2. Make changes with test coverage
3. Run full test suite: `pytest -v`
4. Commit with clear messages

## License

This project is provided as-is for testing and educational purposes.
