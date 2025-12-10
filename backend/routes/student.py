from flask import Blueprint, session, redirect, url_for, flash, render_template, request, jsonify
from ..services import quiz_service
# from ..services.auth_service import AuthService # Use if you need to fetch user name
# from app import app # Only if necessary

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    def wrap(*args, **kwargs):
        if session.get('role') != 'student':
            flash('Unauthorized access. Please log in as a student.', 'warning')
            return redirect(url_for('auth.auth'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# 1. Student Home
@student_bp.route('/')
@student_required
def home():
    # Renders the HTML template where the React frontend loads.
    # The React app will then call a separate API to get student-specific data.
    return render_template('student_home.html')

# 2. Start Quiz
@student_bp.route('/start_quiz', methods=['GET'])
@student_required
def start_quiz():
    # 1. Generate quiz data via the service layer
    quiz_data, error = quiz_service.generate_student_quiz_data(session.get('email'))
    
    if error:
        flash(error, 'error')
        return redirect(url_for('student.home'))

    # 2. Store the generated data in the session
    session['quiz_data'] = quiz_data 
    session['answers'] = [None] * len(quiz_data)
    session['questions_status'] = [0] * len(quiz_data)

    return redirect(url_for('student.question', question_number=0))

# 3. Question Navigation and Submission
@student_bp.route('/question/<int:question_number>', methods=['GET', 'POST'])
@student_required
def question(question_number):
    # This entire function's logic (navigation, POST handling, session updates)
    # is identical to what you had in app_sub2.py, but you must ensure it points 
    # to 'student.result' or 'student.question' for redirect URLs.
    
    quiz_data = session.get('quiz_data', [])
    # ... (rest of the question navigation/submission logic from app_sub2.py) ...
    
    if request.method == 'POST':
        # ... (POST handling logic from app_sub2.py) ...
        
        if 'submit' in request.form:
             # Check if all questions answered...
             return redirect(url_for('student.result'))
        
        # ... (Next/Back redirects) ...
        if 'next' in request.form:
            return redirect(url_for('student.question', question_number=question_number + 1))
    
    return render_template('main.html', # This is where the student takes the quiz
                           # ... pass necessary variables ...
                          )

# 4. Result Calculation and Saving
@student_bp.route('/result')
@student_required
def result():
    # ... (Score calculation logic from app_sub2.py) ...
    score = 0
    total_no_of_questions = len(session.get('quiz_data', []))
    email = session.get('email')

    # 1. Save results via the service layer (PyMySQL)
    quiz_service.save_quiz_result(email, score, total_no_of_questions)
    
    # 2. Clear session
    session.pop('quiz_data', None)
    # ... (clear other session keys) ...
    
    return render_template('result.html', score=score, total=total_no_of_questions)

# 5. Student View Results
@student_bp.route('/results')
@student_required
def student_results():
    email = session.get('email')
    
    # Fetch results via the service layer (PyMySQL)
    results = quiz_service.fetch_student_results(email)
    
    # NOTE: The results are PyMySQL dictionaries, which is perfect for rendering.
    return render_template('student_results.html', results=results)