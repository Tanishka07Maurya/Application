"""Models of the application."""

# User Object for Sign Up/In and Session
class User:
    def __init__(self, id, username, email, password_hash, role=None, master_id=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash 
        self.role = role
        self.master_id = master_id        # Field to hold employee_id or student_id
        
    def __repr__(self):
        return f'<User {self.username}>'

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['user_id'],
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            role=data.get('role'),
            master_id=data.get('master_id')      # Handle master_id if present
        )
