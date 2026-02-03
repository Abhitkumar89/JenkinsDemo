"""Database operations for Employee CRUD."""
import sqlite3
import os
from contextlib import contextmanager

DB_PATH = 'employees.db'


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_connection():
    """Context manager for database connections."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize database with employees table."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_email ON employees(email)
        ''')


def create_employee(name, email, department):
    """Create a new employee.
    
    Args:
        name: Employee name
        email: Employee email (unique)
        department: Department name
        
    Returns:
        Inserted employee ID
        
    Raises:
        sqlite3.IntegrityError: If email already exists
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO employees (name, email, department) VALUES (?, ?, ?)',
            (name, email, department)
        )
        return cursor.lastrowid


def get_employee(employee_id):
    """Get employee by ID.
    
    Args:
        employee_id: Employee ID
        
    Returns:
        Employee dict or None
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_all_employees():
    """Get all employees.
    
    Returns:
        List of employee dicts
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees ORDER BY id')
        return [dict(row) for row in cursor.fetchall()]


def update_employee(employee_id, name=None, email=None, department=None):
    """Update employee.
    
    Args:
        employee_id: Employee ID
        name: New name (optional)
        email: New email (optional)
        department: New department (optional)
        
    Returns:
        Number of rows updated
        
    Raises:
        sqlite3.IntegrityError: If email already exists
    """
    updates = []
    params = []
    
    if name is not None:
        updates.append('name = ?')
        params.append(name)
    if email is not None:
        updates.append('email = ?')
        params.append(email)
    if department is not None:
        updates.append('department = ?')
        params.append(department)
    
    if not updates:
        return 0
    
    params.append(employee_id)
    query = f'UPDATE employees SET {", ".join(updates)} WHERE id = ?'
    
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.rowcount


def delete_employee(employee_id):
    """Delete employee.
    
    Args:
        employee_id: Employee ID
        
    Returns:
        Number of rows deleted
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        return cursor.rowcount


def delete_all_employees():
    """Delete all employees (for testing)."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM employees')


def clear_database():
    """Clear database file (for testing)."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
