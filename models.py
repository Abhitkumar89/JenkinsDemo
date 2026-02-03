"""Employee model definition."""
from datetime import datetime


class Employee:
    """Employee data model."""

    def __init__(self, name, email, department, id=None):
        """Initialize employee.
        
        Args:
            name: Employee name
            email: Employee email
            department: Department name
            id: Optional auto-generated ID
        """
        self.id = id
        self.name = name
        self.email = email
        self.department = department
        self.created_at = datetime.now()

    def to_dict(self):
        """Convert employee to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @staticmethod
    def from_dict(data):
        """Create employee from dictionary."""
        return Employee(
            name=data.get('name'),
            email=data.get('email'),
            department=data.get('department'),
            id=data.get('id')
        )
