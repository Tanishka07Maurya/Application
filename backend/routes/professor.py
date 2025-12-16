from flask import Blueprint, session, redirect, url_for, flash, jsonify, request
from ..services import quiz_service # Import the quiz logic
from ..services.auth_service import AuthService # Import to get user data if needed
from functools import wraps
from ..services.quiz_service import fetch_questions_by_course
from ..extensions import get_db_connection
import pymysql

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

@professor_bp.route('/data', methods=['GET'])
@professor_required
def get_professor_data():
    user_id = session.get('id')
    if not user_id:
        return jsonify({"message": "User ID not found in session."}), 401
    
    user_record = AuthService().get_user_by_id(user_id)
    
    if user_record:
        return jsonify({
            "isLoggedIn": True,
            "username": user_record.username,
            "email": user_record.email,
            "role": session.get('role'),
        }), 200
    
    return jsonify({"message": "User not found"}), 404

# --- API Endpoints for React ---
# 1. API to check session and get user data
@professor_bp.route('/programs', methods=['GET'])
@professor_required
def get_programs_api_view(id=None): # Renamed to 'get_programs_api_view' to be safe
    school_id_raw = request.args.get('school_id')
    if not school_id_raw:
        return jsonify([]), 200
    
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    try:
        school_id_int = int(school_id_raw)
        
        # Ensure 'program' table name is correct based on your workbench image
        sql = "SELECT id, program_name FROM program WHERE school_id = %s"
        cursor.execute(sql, (school_id_int,))
        
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        print(f"Error fetching programs: {e}")
        return jsonify({"message": "Database error"}), 500
    finally:
        cursor.close()
        conn.close()

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
    
    #adding my code👌👌👌👌👌👌👌👌👌
    # --- PASTE THIS AT THE BOTTOM OF routes/professor.py ---
# Vaidehi Changes

# 6. API to fetch questions by course for quiz creation
@professor_bp.route('/questions/by_course/<int:course_id>', methods=['GET'])
@professor_required
def get_questions_by_course_api(course_id):
    try:
        # Call the new service function
        questions_list = fetch_questions_by_course(course_id)
        
        if not questions_list:
            return jsonify({"message": "No questions found for this course."}), 200
            
        return jsonify(questions_list), 200
    except Exception as e:
        print(f"Error fetching questions by course: {e}")
        return jsonify({"message": "Internal server error fetching questions."}), 500
# vaidehi

# 7. APIs to fetch schools, programs, departments, and courses for dropdowns
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
        conn.close()#vaidehi

    # cur = mysql.connection.cursor()
    # cur.execute("SELECT id, school_name FROM school") # Matches your image
    # data = cur.fetchall()
    # cur.close()
    
    # # Convert to list
    # school_list = [{'id': row[0], 'school_name': row[1]} for row in data]
    # return jsonify(school_list)

# @professor_bp.route('/departments', methods=['GET'])
# @professor_required
# def fetch_departments_list_view(): 
#     program_id_raw = request.args.get('program_id')
#     if not program_id_raw:
#         return jsonify([]), 200

#     conn = get_db_connection()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     try:
#         # 🚀 JOIN logic using confirmed junction table name: dept_program
#         sql = """
#             SELECT d.id, d.dept_name 
#             FROM department d
#             JOIN dept_program dp ON d.id = dp.dept_id
#             WHERE dp.program_id = %s
#         """
#         cursor.execute(sql, (int(program_id_raw),))
#         data = cursor.fetchall()
#         return jsonify(data), 200
#     except Exception as e:
#         print(f"!!! Error fetching departments: {e}")
#         return jsonify({"message": "Database query error"}), 500
#     finally:
#         cursor.close()
#         conn.close() # tanishka

@professor_bp.route('/departments', methods=['GET'])
@professor_required
def fetch_departments_list_view(): 
    # 1. Capture the selected program ID from the React frontend
    program_id_raw = request.args.get('program_id')
    
    if not program_id_raw:
        return jsonify([]), 200

    conn = None
    cursor = None
    try:
        program_id_int = int(program_id_raw)

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 🚀 THE JOIN FIX: 
        # We select the actual department data (d)
        # by joining with the junction table (dp) 
        # using the matching dept_id and the selected program_id.
        sql = """
            SELECT d.id, d.dept_name 
            FROM department d
            JOIN dept_program dp ON d.id = dp.dept_id
            WHERE dp.program_id = %s
        """
        
        cursor.execute(sql, (program_id_int,))
        data = cursor.fetchall()
        
        # This will return the list of departments to your frontend dropdown
        return jsonify(data), 200

    except Exception as e:
        print(f"!!! Error in fetch_departments_list_view: {e}")
        return jsonify({"message": "Database query error"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()#vaidehi

# 8. API to fetch courses based on department and semester
@professor_bp.route('/courses', methods=['GET'])
@professor_required
def fetch_courses_list_view():
    dept_id_raw = request.args.get('dept_id')
    semester_id_raw = request.args.get('semester')
    
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
        
        # 🚀 DEFINITIVE WORKING QUERY (Matches image_150ea3.jpg)
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
    #vaidehi

# def get_questions_by_course():
#     course_id = request.args.get('course_id')
    
#     cur = mysql.connection.cursor()
#     query = "SELECT id, question_text, option_1, option_2, option_3, option_4, correct_answer FROM questions WHERE course_id = %s"
#     cur.execute(query, (course_id,))
#     data = cur.fetchall()
#     cur.close()
    
#     questions_list = []
#     for row in data:
#         questions_list.append({
#             'id': row[0],
#             'text': row[1],
#             'options': [row[2], row[3], row[4], row[5]],
#             'correct': row[6]
#         })
        
#     return jsonify(questions_list)

# pri
# 10. API to fetch/update a single question
@professor_bp.route('/questions/<int:id>', methods=['GET', 'PUT'])
@professor_required
def handle_single_question(id):
    """
    Handles fetching (GET) and updating (PUT) a single question by ID.
    The GET method loads data into the edit form.
    The PUT method saves the form data back to the database.
    """
    
    # --- 1. GET Method: Fetch Question Data for Edit Form ---
    if request.method == 'GET':
        try:
            # Call the service layer to fetch the structured question data
            question_data = quiz_service.get_question_by_id(id) 
            
            if not question_data:
                # Returns 404 if the question ID is valid but not found in the DB
                return jsonify({'message': 'Question not found'}), 404
                
            # Success: Return the question data to pre-fill the React form
            return jsonify(question_data), 200 

        except Exception as e:
            # Catches database connection issues or query failures
            print(f"!!! ERROR during GET for question ID {id}: {e}") 
            return jsonify({'message': 'Internal Server Error during fetch.'}), 500

    # --- 2. PUT Method: Update Question Data from Edit Form ---
    elif request.method == 'PUT':
        try:
            # Get the JSON payload sent by the React form
            data = request.get_json()
            
            # Call the service layer to execute the database update transaction
            # This service function must handle updating the question_bank and answer_map.
            success = quiz_service.update_question(id, data) 
            
            if not success:
                # Returns 404 if the ID is not found or update transaction failed
                return jsonify({'message': 'Question not found or update failed.'}), 404
                
            # Success: Return confirmation
            return jsonify({'message': 'Question updated successfully!'}), 200

        except Exception as e:
            # Catches errors during update (e.g., transaction failure, invalid JSON)
            print(f"!!! ERROR during PUT for question ID {id}: {e}")
            return jsonify({'message': 'Internal Server Error during update.'}), 500

    # Fallback for methods not allowed (though Flask usually handles this)
    return jsonify({'message': 'Method not allowed'}), 405#vaidehi