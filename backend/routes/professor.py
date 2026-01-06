from flask import Blueprint, session, redirect, url_for, flash, jsonify, request
from ..services import quiz_service # Import the quiz logic
from ..services.auth_service import AuthService # Import to get user data if needed
from functools import wraps
from ..services.quiz_service import fetch_questions_by_course
from ..extensions import get_db_connection
import pymysql
import traceback

professor_bp = Blueprint('professor', __name__, url_prefix='/prof') 

# --- Decorator: Ensure User is a Professor ---
def professor_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('role') != 'professor':
            return jsonify({"message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# --- 1. Dashboard & Course Data Endpoints ---

@professor_bp.route('/my-courses', methods=['GET'])
@professor_required
def get_my_courses():
    teacher_id = session.get('id')
    courses = quiz_service.get_courses_for_teacher(teacher_id)
    return jsonify(courses), 200

@professor_bp.route('/schools', methods=['GET'])
@professor_required
def get_schools():
    conn = get_db_connection() 
    cursor = conn.cursor(pymysql.cursors.DictCursor) # Use DictCursor
    
    try:
        cursor.execute("SELECT id, school_name FROM school")
        data = cursor.fetchall()
        # Return list of dictionaries directly
        return jsonify(data), 200
    except Exception as e:
        print(f"Error fetching school: {e}")
        return jsonify({"message": "Database error fetching school."}), 500
    finally:
        cursor.close()
        conn.close()

@professor_bp.route('/programs', methods=['GET'])
@professor_required
def get_programs():
    school_id = request.args.get('school_id')
    if not school_id:
        return jsonify([]), 200
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        sql_query = """
            SELECT id, program_name 
            FROM program 
            WHERE school_id = %s
        """
        cursor.execute("SELECT id, program_name FROM program WHERE school_id = %s", (school_id,))
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        print(f"Error fetching programs: {e}")
        return jsonify({"message": "Database error fetching programs."}), 500
    finally:
        cursor.close()
        conn.close()

@professor_bp.route('/departments', methods=['GET'])
@professor_required
def fetch_departments_list_view(): 
    program_id_raw = request.args.get('program_id')
    print(f"DEBUG: Fetching departments for Program ID: {program_id_raw}")
    if not program_id_raw:
        return jsonify([]), 200
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """
            SELECT d.id, d.dept_name 
            FROM department d
            JOIN dept_program dp ON d.id = dp.dept_id
            WHERE dp.program_id = %s
        """
        cursor.execute(sql, (int(program_id_raw),))
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        print(f"!!! Error fetching departments: {e}")
        return jsonify({"message": "Database query error"}), 500
    finally:
        cursor.close()
        conn.close()

@professor_bp.route('/courses', methods=['GET'])
@professor_required
def fetch_courses_list_view():
    dept_id_raw = request.args.get('dept_id')
    semester_id_raw = request.args.get('semester')
    
    print(f"DEBUG: Courses req -> Dept: {dept_id_raw}, Sem: {semester_id_raw}")
    if not dept_id_raw or not semester_id_raw:
        return jsonify([]), 200
    conn = None
    cursor = None
    try:
        # Cast inputs to integers
        dept_id_int = int(dept_id_raw)
        semester_id_int = int(semester_id_raw)
        
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = """
            SELECT DISTINCT c.id, c.course_name 
            FROM course c
            JOIN semester_course sc ON c.id = sc.course_id
            JOIN department_semester ds ON sc.semester_id = ds.semester_id
            WHERE ds.dept_id = %s AND sc.semester_id = %s
        """     
        cursor.execute(sql, (dept_id_int, semester_id_int))
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        print(f"!!! FATAL SQL CRASH fetching courses: {e}")
        return jsonify({"message": "Database query failed"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- 2. Question Management Endpoints ---

@professor_bp.route('/questions', methods=['GET'])
@professor_required
def get_questions_api():
    try:
        employee_id = session.get('id')
        if not employee_id:
            return jsonify({"message": "User ID not found in session."}), 400

        # allow optional course filter via query param ?course_id=###
        course_id_raw = request.args.get('course_id')
        course_id = int(course_id_raw) if course_id_raw else None

        questions = quiz_service.fetch_questions(employee_id, fetch_scope='creator', course_id=course_id)
        if questions is None:
            print("WARNING: quiz_service.fetch_questions returned None. Returning empty object {}")
            questions = {}
            
        return jsonify(questions), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching questions: {str(e)}"}), 500

@professor_bp.route('/add_questions', methods=['POST'])
@professor_required
def add_question_api():
    print("Received request to add question.")
    data = request.get_json() 
    print(f"Request data: {data}")    
    required_keys = ['text', 'options', 'correct_index', 'course_id']
    if not all(key in data for key in required_keys):
        return jsonify({"message": "Missing required fields"}), 400
    try:
        teacher_id = session.get('id')
        if not teacher_id:
            return jsonify({"message": "User ID not found in session. Please log in again."}), 400  
        if not data.get('course_id'):
            return jsonify({"message": "course_id is required"}), 400
        quiz_service.insert_question(data, teacher_id)
        return jsonify({"message": "Question added successfully!"}), 201    
    except ValueError as ve:
        print(f"Validation Error: {ve}")
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        print(f"Error during question insertion: {str(e)}")
        return jsonify({"message": "Internal server error during database operation."}), 500

@professor_bp.route('/questions/<int:id>', methods=['GET', 'PUT'])
@professor_required
def handle_single_question(id):
    """Handles fetching (GET) and updating (PUT) a single question."""
    if request.method == 'GET':
        try:          
            question_data = quiz_service.get_question_by_id(id) 
            if not question_data:
                return jsonify({'message': 'Question not found'}), 404
            return jsonify(question_data), 200 
        except Exception as e:   
            print(f"!!! ERROR during GET for ID {id}: {e}") 
            return jsonify({'message': 'Internal Server Error during fetch.'}), 500
    elif request.method == 'PUT':
        try:
            data = request.get_json()            
            updated_q = quiz_service.update_question(id, data) 
            if not updated_q:
                return jsonify({'message': 'Question not found or update failed'}), 404
            return jsonify({'message': 'Question updated successfully', 'question': updated_q}), 200 
        except Exception as e:
            print(f"!!! ERROR during PUT for ID {id}: {e}")
            return jsonify({'message': 'Internal Server Error during update.'}), 500
    elif request.method == 'DELETE':
        try:
            success = quiz_service.delete_question(id) 
            if not success:
                return jsonify({'message': 'Question not found or deletion failed'}), 404   
            return jsonify({'message': 'Question deleted successfully'}), 200
        except Exception as e:
            print(f"!!! ERROR during DELETE for ID {id}: {e}")
            return jsonify({'message': 'Internal Server Error during deletion.'}), 500
    return jsonify({'message': 'Method not allowed'}), 405  

@professor_bp.route('/questions/by_course/<int:course_id>', methods=['GET'])
@professor_required
def fetch_questions_by_course_view(course_id):
    try:
        questions_list = quiz_service.fetch_questions_by_course(course_id)
        return jsonify(questions_list if questions_list else []), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal server error"}), 500

# --- 3. Quiz Management Endpoints ---

@professor_bp.route('/quizzes', methods=['GET'])
@professor_required
def get_quizzes_api():
    try:
        teacher_id = session.get('id')
        if not teacher_id:
            return jsonify({"message": "User ID not found in session. Please log in again."}), 400     
        quizzes = quiz_service.get_professor_quizzes(teacher_id)
        return jsonify(quizzes), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching quizzes: {str(e)}"}), 500

@professor_bp.route('/generate', methods=['POST'])
@professor_required
def generate_quiz_api():
    try:
        teacher_id = session.get('id')
        teacher_name = session.get('username', 'Professor')
        data = request.get_json()
        course_id = data.get('course_id') 
        if not teacher_id:
            return jsonify({"message": "User ID not found"}), 400    
        quiz_data = quiz_service.generate_and_save_quiz(teacher_id, course_id, teacher_name)
        if not quiz_data:
            return jsonify({"message": "No questions found for this course."}), 404
        response_payload = {
            "message": "Quiz generated and saved successfully.",
            "quiz_link": quiz_data['quiz_link'],
            "quiz_id": quiz_data['id'],
            "question_count": quiz_data.get('question_count', 0),
            "used_teacher_filter": quiz_data.get('used_teacher_filter', True)
        }
        if not response_payload['used_teacher_filter']:
            response_payload['message'] += " (Note: no teacher-specific questions found; used course-wide pool)"
        return jsonify(response_payload), 201
    except Exception as e:
        traceback.print_exc()
        print(f"DEBUG: Exception in generate_quiz_api: {e}")
        return jsonify({"message": f"Quiz generation failed: {str(e)}"}), 500

@professor_bp.route('/quiz-preview/<token>', methods=['GET'])
def quiz_preview(token):
    try:
        quiz_data = quiz_service.get_quiz_preview_details(token)
        
        if not quiz_data:
            return jsonify({"message": "Quiz not found or invalid token"}), 404     
        return jsonify(quiz_data), 200
    except Exception as e:
        print(f"Preview Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
