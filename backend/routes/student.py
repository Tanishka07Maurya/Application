from flask import Blueprint, session, redirect, url_for, flash, render_template, request, jsonify
from ..services import quiz_service
from functools import wraps

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('role') != 'student':
            return jsonify({"message": "Unauthorized. Please log in as a student."}), 403
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@student_bp.route('/')
@student_required
def home():
    return render_template('student_home.html')

@student_bp.route('/start_quiz', methods=['GET'])
@student_required
def start_quiz():
    student_id = session.get('id')
    quiz_data, error = quiz_service.generate_student_quiz_data(student_id)
    
    if error:
        flash(error, 'error')
        return redirect(url_for('student.home'))

    session['quiz_data'] = quiz_data 
    session['answers'] = [None] * len(quiz_data)
    session['questions_status'] = [0] * len(quiz_data)

    return redirect(url_for('student.question', question_number=0))

@student_bp.route('/question/<int:question_number>', methods=['GET', 'POST'])
@student_required
def question(question_number):
    quiz_data = session.get('quiz_data', [])
    
    if request.method == 'POST':
        if 'submit' in request.form:
            return redirect(url_for('student.result'))
        
        if 'next' in request.form:
            return redirect(url_for('student.question', question_number=question_number + 1))
    
    return render_template('main.html')

@student_bp.route('/result')
@student_required
def result():
    score = 0
    total_no_of_questions = len(session.get('quiz_data', []))
    student_id = session.get('id')

    quiz_service.save_quiz_result(student_id, score, total_no_of_questions)
    
    session.pop('quiz_data', None)
    session.pop('answers', None)
    session.pop('questions_status', None)
    
    return render_template('result.html', score=score, total=total_no_of_questions)

@student_bp.route('/results')
@student_required
def student_results():
    student_id = session.get('id')
    
    results = quiz_service.fetch_student_results(student_id)
    
    return render_template('student_results.html', results=results)
