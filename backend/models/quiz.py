from ..extensions import db
from datetime import datetime
import uuid
# Vaidehi Canges
class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_title = db.Column(db.String(200), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    program = db.Column(db.String(200), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(300), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False, default=5)
    duration = db.Column(db.Integer, nullable=False, default=10)
    status = db.Column(db.String(20), default='Published')
    # Generate a unique link slug
    quiz_link = db.Column(db.String(200), default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'quiz_title': self.quiz_title,
            'title': self.quiz_title,
            'teacher': self.teacher,
            'school': self.school,
            'department': self.department,
            'program': self.program,
            'semester': self.semester,
            'course': self.course,
            'total_questions': self.total_questions,
            'totalQuestions': self.total_questions,
            'duration': self.duration,
            'status': self.status,
            'quiz_link': self.quiz_link,
            # Use isoformat for easy consumption by JavaScript
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Quiz {self.quiz_title}>'
