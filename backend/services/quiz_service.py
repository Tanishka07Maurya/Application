from ..extensions import get_db_connection
from ..import create_app
import random
import pymysql
from flask import session
from datetime import datetime, timedelta
import uuid
import random
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired 

# 1. Fetch Teacher's Courses
def get_courses_for_teacher(teacher_id):
    """Fetches courses linked to the professor's department."""
    print(f"DEBUG: Fetching courses for Teacher ID: {teacher_id}") # 👈 Print ID
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """
            SELECT DISTINCT c.id, c.course_name
            FROM course c
            JOIN semester_course sc ON c.id = sc.course_id
            JOIN department_semester ds ON sc.semester_id = ds.semester_id
            JOIN employee_school_department esd ON ds.dept_id = esd.dept_id
            WHERE esd.employee_id = %s
            ORDER BY c.course_name
        """
        cursor.execute(sql, (teacher_id,))
        results = cursor.fetchall()
        print(f"DEBUG: Found {len(results)} courses: {results}") # 👈 Print Results
        return results
    except Exception as e:
        print(f"Error fetching teacher courses: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# 2. Add a New Question           ❤️❤️❤️❤️❤️ 
# 2. Add a New Question
def insert_question(form_data, teacher_id): 
    conn = get_db_connection()
    cursor = conn.cursor()

    DEFAULT_TYPE = "MCQ"
    DEFAULT_UNIT = 1
    DEFAULT_MARKS = int(form_data.get('marks', 1))

    course_id = form_data.get('course_id')
    if not course_id:
        raise ValueError("Course ID is required to add a question.")

    try:
        # Insert into Question Bank
        sql_insert_question = """
            INSERT INTO question_bank (question_txt, question_type, unit, marks)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_insert_question, (
            form_data['text'], 
            DEFAULT_TYPE,  
            DEFAULT_UNIT,  
            DEFAULT_MARKS,
        ))
        new_question_id = cursor.lastrowid

        # Insert Options
        sql_insert_options = """
            INSERT INTO answer_map (question_id, option_text, is_correct)
            VALUES (%s, %s, %s)
        """
        
        # Handle options (flexible for list of dicts or list of strings)
        if 'options' in form_data and isinstance(form_data['options'][0], dict):
             for opt in form_data['options']:
                cursor.execute(sql_insert_options, (
                    new_question_id,
                    opt['text'],
                    1 if opt['isCorrect'] else 0
                ))
        else:
            correct_index = int(form_data.get('correct_index', -1))
            for index, option_text in enumerate(form_data.get('options', [])):
                is_correct_flag = 1 if index == correct_index else 0
                cursor.execute(sql_insert_options, (new_question_id, option_text, is_correct_flag))

        # Link Question to Teacher
        sql_link_creator = "INSERT INTO question_employee (question_id, employee_id) VALUES (%s, %s)"
        cursor.execute(sql_link_creator, (new_question_id, teacher_id))

        # Link Question to Course
        sql_link_course = "INSERT INTO question_course (question_id, course_id) VALUES (%s, %s)"
        cursor.execute(sql_link_course, (new_question_id, course_id))

        conn.commit() 
    except Exception as e:
        conn.rollback() 
        print(f"Database error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# 3. Fetch All Questions (Creator Scope)
def fetch_questions(employee_id, fetch_scope='creator', course_id=None):
    """Fetches questions created by an employee. If course_id is provided, filters by course."""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if not employee_id and fetch_scope == 'creator':
        return {}

    try:
        emp_id = employee_id
        if course_id:
            select_clause = """
                SELECT 
                    qb.id AS question_id,
                    qb.question_txt,
                    qb.unit, 
                    am.id AS option_id,
                    am.option_text,
                    am.is_correct
                FROM question_bank qb
                JOIN answer_map am ON qb.id = am.question_id
                JOIN question_employee qe ON qb.id = qe.question_id
                JOIN question_course qc ON qb.id = qc.question_id
                WHERE
                    qe.employee_id = %s 
                    AND qc.course_id = %s
            """
            cursor.execute(select_clause, (emp_id, course_id))
        else:
            select_clause = """
                SELECT 
                    qb.id AS question_id,
                    qb.question_txt,
                    qb.unit, 
                    am.id AS option_id,
                    am.option_text,
                    am.is_correct
                FROM
                    question_bank qb
                JOIN
                    answer_map am ON qb.id = am.question_id
                JOIN
                    question_employee qe ON qb.id = qe.question_id
                WHERE
                    qe.employee_id = %s
            """
            cursor.execute(select_clause, (emp_id,))
        results = cursor.fetchall()
    except Exception as e:
        print(f"Query failed to execute: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()
    questions_with_options = {}
    for row in results:
        q_id = row['question_id']

        if q_id not in questions_with_options:
            questions_with_options[q_id] = {
                'question_id': q_id,
                'question_txt': row['question_txt'],
                'unit': row['unit'],
                'options': []
            }
        questions_with_options[q_id]['options'].append({
            'option_id': row['option_id'],
            'option_text': row['option_text'],
            'is_correct': row['is_correct']
        })
    print(questions_with_options)
    return questions_with_options

# 4. Get Single Question by ID
def get_question_by_id(question_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)    
    try:
        # SQL to join the question with all its options and correct flag and course mapping
        sql = """
            SELECT 
                qb.id AS question_id,
                qb.question_txt, 
                am.option_text,
                am.is_correct,
                qc.course_id
            FROM question_bank qb
            JOIN answer_map am ON qb.id = am.question_id
            LEFT JOIN question_course qc ON qb.id = qc.question_id
            WHERE qb.id = %s
        """
        cursor.execute(sql, (question_id,))
        results = cursor.fetchall()

        if not results:
            return None # Question not found
        question_data = {
            'text': results[0]['question_txt'], 
            'options': [],
            'correct': '', # Will hold the index (0, 1, 2, 3) as a string
            'course_id': results[0].get('course_id') if results[0].get('course_id') else ''
        }        
        option_texts = []
        correct_text = None
        for row in results:
            option_texts.append(row['option_text'])
            if row['is_correct'] == 1:
                correct_text = row['option_text']
        while len(option_texts) < 4:
            option_texts.append("")
        question_data['options'] = option_texts
        # Find the index of the correct text and store it as a string
        if correct_text in option_texts:
            correct_index = option_texts.index(correct_text)
            question_data['correct'] = str(correct_index)
        else:
             question_data['correct'] = '' # Failsafe
        
        return question_data

    except Exception as e:
        print(f"Database error in get_question_by_id: {e}")
        return None
    finally:
        cursor.close()
        conn.close()    

# 5. Update Question
def update_question(question_id, data):
    """Updates the question text and re-saves all options/answers in a transaction.
    Also updates the question->course mapping if 'course_id' is provided in the payload."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Update the question text in question_bank
    sql_update_question = """
        UPDATE question_bank SET question_txt = %s WHERE id = %s
    """
    
    # 2. Delete existing answers/options from answer_map
    sql_delete_options = """
        DELETE FROM answer_map WHERE question_id = %s
    """
    
    # 3. Insert the new/updated options into answer_map
    sql_insert_options = """
        INSERT INTO answer_map (question_id, option_text, is_correct)
        VALUES (%s, %s, %s)
    """

    # 4. SQL for updating course mapping
    sql_delete_qc = """
        DELETE FROM question_course WHERE question_id = %s
    """
    sql_insert_qc = """
        INSERT INTO question_course (question_id, course_id) VALUES (%s, %s)
    """

    try:
        # Start Transaction
        conn.begin()
        
        # --- Update Question Bank ---
        cursor.execute(sql_update_question, (data['text'], question_id))

        # --- Delete Old Options ---
        cursor.execute(sql_delete_options, (question_id,))

        # --- Insert New Options ---
        correct_index = int(data.get('correct_index', -1))
        
        # Note: We use data['options'] which includes the empty strings for up to 4 options
        for index, option_text in enumerate(data['options']):
            # Skip inserting empty options if they were not provided
            if not option_text.strip():
                continue
                
            is_correct_flag = 1 if index == correct_index else 0
            
            cursor.execute(sql_insert_options, (
                question_id,
                option_text,
                is_correct_flag,
            ))

        # --- Update course mapping if provided ---
        if 'course_id' in data and data['course_id']:
            cursor.execute(sql_delete_qc, (question_id,))
            cursor.execute(sql_insert_qc, (question_id, data['course_id']))
            
        # Commit all changes if successful
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback() # Revert all changes if any step failed
        print(f"Database error during question update: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

# 6. Fetch Questions by Course ID
def fetch_questions_by_course(course_id):
    """Fetches full question details for a specific course ID.
    Returns list of objects: { question_id, question_txt, options: [{option_text,is_correct}, ...] }
    """
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # JOIN linking question text to their options and correct status
        sql = """
            SELECT 
                qb.id AS question_id,
                qb.question_txt,
                am.option_text,
                am.is_correct
            FROM question_bank qb
            JOIN answer_map am ON qb.id = am.question_id
            JOIN question_course qc ON qb.id = qc.question_id
            WHERE qc.course_id = %s
        """
        cursor.execute(sql, (course_id,))
        results = cursor.fetchall()

        # Restructure results into nested format for React
        questions = {}
        for row in results:
            q_id = row['question_id']
            if q_id not in questions:
                questions[q_id] = {
                    'question_id': q_id,
                    'question_txt': row['question_txt'],
                    'options': []
                }
            questions[q_id]['options'].append({
                'option_text': row['option_text'],
                'is_correct': row['is_correct']
            })
        return list(questions.values())
    except Exception as e:
        print(f"Database crash during question fetch: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# 7. Generate Quiz  ❤️❤️❤️❤️❤️
def get_professor_quizzes(teacher_id):
    """Returns a list of quizzes created by the professor with basic metadata."""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = """
            SELECT id, quiz_title, quiz_link, quiz_token, course_id, quiz_status, created_at
            FROM quizzes WHERE teacher_id = %s ORDER BY id DESC
        """
        cursor.execute(sql, (teacher_id,))
        rows = cursor.fetchall()
        quizzes = []
        for r in rows:
            quizzes.append({
                'id': r['id'],
                'quiz_title': r.get('quiz_title'),
                'quiz_link': r.get('quiz_link'),
                'token': r.get('quiz_token'),
                'course_id': r.get('course_id'),
                'status': r.get('quiz_status'),
                'created_at': r.get('created_at')
            })
        return quizzes
    except Exception as e:
        print(f"Error fetching professor quizzes: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# 8. Get Quiz Preview ❤️❤️❤️❤️❤️
def get_quiz_preview_details(token):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # 1. Get the Quiz ID from the Token
        cursor.execute("SELECT id, quiz_title FROM quizzes WHERE quiz_token = %s", (token,))
        quiz = cursor.fetchone()
        
        if not quiz:
            print(f"DEBUG: Quiz not found for token: {token}")
            return None
        
        # 2. Fetch Questions using the Quiz ID (NOT the token)
        sql = """
            SELECT 
                qb.id as question_id, 
                qb.question_txt, 
                am.option_text, 
                am.is_correct
            FROM quiz_questions_generated qqg
            JOIN question_bank qb ON qqg.question_id = qb.id
            JOIN answer_map am ON qb.id = am.question_id
            WHERE qqg.quiz_id = %s 
        """
        # ⚠️ FIX: Pass quiz['id'], not token
        cursor.execute(sql, (quiz['id'],)) 
        results = cursor.fetchall()        
        if not results:
            return {"title": quiz['quiz_title'], "questions": []}
        # 3. Restructure Data
        quiz_data = {"title": quiz['quiz_title'], "questions": {}}   
        for row in results:
            q_id = row['question_id']
            if q_id not in quiz_data['questions']:
                quiz_data['questions'][q_id] = {
                    "id": q_id, 
                    "text": row['question_txt'], 
                    "options": []
                }
            quiz_data['questions'][q_id]['options'].append({
                "text": row['option_text'], 
                "is_correct": row['is_correct']
            })
            
        quiz_data['questions'] = list(quiz_data['questions'].values())
        return quiz_data

    except Exception as e:
        print(f"Error fetching preview: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# 9. Delete Question
def delete_question(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete related data first due to foreign key constraints
        cursor.execute("DELETE FROM answer_map WHERE question_id = %s", (question_id,))
        cursor.execute("DELETE FROM question_course WHERE question_id = %s", (question_id,))
        # Delete the question itself
        delete_count = cursor.execute("DELETE FROM question_bank WHERE id = %s", (question_id,))
        
        conn.commit()
        return delete_count > 0

    except Exception as e:
        conn.rollback()
        print(f"Transaction failed for question deletion (ID {question_id}): {e}")
        return False
    finally:
        cursor.close()
        conn.close()
