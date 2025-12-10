from flask import Blueprint, session, redirect, url_for, flash, jsonify, request
from ..services import quiz_service # Import the quiz logic
from ..services.auth_service import AuthService # Import to get user data if needed
from functools import wraps

professor_bp = Blueprint('professor', __name__, url_prefix='/prof') 

def professor_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # ⚠️ DIAGNOSTIC PRINTS START ⚠️
        print(f"DEBUG: Session contents: {session.items()}")
        print(f"DEBUG: Role found: '{session.get('role')}'")
        # ⚠️ DIAGNOSTIC PRINTS END ⚠️

        if session.get('role') != 'professor':
            return jsonify({"message": "Unauthorized"}), 403 # Return JSON for React
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# --- API Endpoints for React ---
# 1. API to check session and get user data
@professor_bp.route('/data', methods=['GET'])
@professor_required
def get_professor_data():
    email = session.get('email')
    user_record = AuthService().get_user_by_email(email) 
    
    if user_record:
        return jsonify({
            "isLoggedIn": True,
            "username": user_record['user_name'], 
            "email": email,
            "role": session.get('role'),
            # "quizzes_count": len(quiz_service.get_professor_quizzes(email))
        }), 200
    
    return jsonify({"message": "User not found"}), 404

# 2. API to view all quizzes 
@professor_bp.route('/quizzes', methods=['GET'])
@professor_required
def get_quizzes_api():
    try:
        teacher_id = session.get('id')
        if not teacher_id:
            return jsonify({"message": "User ID not found in session. Please log in again."}), 400
        
        quizzes = quiz_service.get_professor_quizzes(session.get(teacher_id))
        return jsonify(quizzes), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching quizzes: {str(e)}"}), 500

# 3. API to add a new question
@professor_bp.route('/add_questions', methods=['POST'])
@professor_required
def add_question_api():
    print("Received request to add question.")
    data = request.get_json() 
    print(f"Request data: {data}")
    
    # --- Data Validation Checks ---
    required_keys = ['text', 'options', 'correct_index']
    if not all(key in data for key in required_keys):
        return jsonify({"message": f"Missing required fields"}), 400

    try:
        teacher_id = session.get('id')
        if not teacher_id:
            return jsonify({"message": "User ID not found in session. Please log in again."}), 400
        
        # quiz_service.insert_questions(data, session.get('email'))
        quiz_service.insert_question(data, teacher_id)
        return jsonify({"message": "Question added successfully!"}), 201
        
    except Exception as e:
        print(f"Error during question insertion: {str(e)}")
        return jsonify({"message": "Internal server error during database operation."}), 500

# 4. API to generate a quiz
@professor_bp.route('/generate', methods=['POST'])
@professor_required
def generate_quiz_api():
    try:
        teacher_id = session.get('id')
        if not teacher_id:
            return jsonify({"message": "User ID not found in session. Please log in again."}), 400
        
        quiz_id = quiz_service.generate_and_save_quiz(teacher_id)
        return jsonify({
            "message": "Quiz generated and saved for review.",
            "quiz_id": quiz_id
        }), 201
    except Exception as e:
        return jsonify({"message": f"Quiz generation failed: {str(e)}"}), 500

# 5. API to fetch questions for quiz creation
@professor_bp.route('/questions', methods=['GET'])
@professor_required
def get_questions_api():
    try:
        employee_id = session.get('id')
        if not employee_id:
            return jsonify({"message": "User ID not found in session."}), 400

        questions = quiz_service.fetch_questions(employee_id, fetch_scope='creator')
        if questions is None:
            print("WARNING: quiz_service.fetch_questions returned None. Returning empty object {}")
            questions = {}
            
        return jsonify(questions), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching questions: {str(e)}"}), 500
    
# @professor_bp.route('/questions', methods=['GET'])
# def get_question_bank():
#     try:
#         employee_id = session.get('id')
#         if not employee_id:
#             return jsonify({"message": "User ID not found in session."}), 400
        
#         questions = quiz_service.fetch_questions(employee_id, fetch_scope='bank')
#         return jsonify(questions), 200
#     except Exception as e:
#         return jsonify({"message": f"Error fetching question bank: {str(e)}"}), 500

