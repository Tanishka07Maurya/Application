from ..extensions import get_db_connection
from ..import create_app
import random
import pymysql
from flask import session
from datetime import datetime, timedelta
import uuid
import random
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired 

class QuestionForm(FlaskForm):
    pass 


def get_courses_for_teacher(teacher_id):
    """Fetches courses linked to the professor's department."""
    print(f"DEBUG: Fetching courses for Teacher ID: {teacher_id}") # 👈 Print ID
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # Join Employee -> School/Dept -> Program -> Course
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

# 1. Database Add Question               ❤️❤️❤️❤️❤️ 
def insert_question(form_data, teacher_id): 
    conn = get_db_connection()
    cursor = conn.cursor()

    DEFAULT_TYPE = "MCQ"
    DEFAULT_UNIT = 1
    DEFAULT_MARKS = int(form_data.get('marks', 1))
    # DEFAULT_COURSE_ID = 21 #for now

    # 1. GET THE SELECTED COURSE ID (Crucial Change)
    # This comes from the <select name="course_id"> in your React form
    course_id = form_data.get('course_id')

    if not course_id:
        raise ValueError("Course ID is required to add a question.")

    sql_insert_question_bank = """
        INSERT INTO question_bank (question_txt, question_type, unit, marks)
        VALUES (%s, %s, %s, %s)
    """

    sql_insert_options = """
        INSERT INTO answer_map (question_id, option_text, is_correct)
        VALUES (%s, %s, %s)
    """

    sql_link_question_to_course = """
        INSERT INTO question_course (question_id, course_id)
        VALUES (%s, %s)
    """

    # ✅ NEW: SQL to link question to the creator (teacher)
    sql_link_question_to_creator = """
        INSERT INTO question_employee (question_id, employee_id)
        VALUES (%s, %s)
    """
    
    # ✅ NEW: SQL to link question to the default course
    sql_link_question_to_course = """
        INSERT INTO question_course (question_id, course_id)
        VALUES (%s, %s)
    """

    try:
        cursor.execute(sql_insert_question_bank, (
            form_data['text'], 
            DEFAULT_TYPE,  
            DEFAULT_UNIT,  
            DEFAULT_MARKS,
        ))

        new_question_id = cursor.lastrowid
        # correct_index = int(form_data['correct_index'])

        if 'options' in form_data and isinstance(form_data['options'][0], dict):
             for opt in form_data['options']:
                cursor.execute(sql_insert_options, (
                    new_question_id,
                    opt['text'],
                    1 if opt['isCorrect'] else 0
                ))
        else:
            # Fallback to your old logic if using simple list + correct_index
            correct_index = int(form_data.get('correct_index', -1))
            for index, option_text in enumerate(form_data.get('options', [])):
                is_correct_flag = 1 if index == correct_index else 0
                cursor.execute(sql_insert_options, (new_question_id, option_text, is_correct_flag))

        # for index, option_text in enumerate(form_data['options']):
        #     is_correct_flag = 1 if index == correct_index else 0
        #     cursor.execute(sql_insert_options, (
        #         new_question_id,
        #         option_text,
        #         is_correct_flag,
        #     ))

        # ✅ NEW: Link question to the teacher
        cursor.execute(sql_link_question_to_creator, (new_question_id, teacher_id))

        # ✅ NEW: Link to Selected Course (The Fix)
        cursor.execute(sql_link_question_to_course, (new_question_id, course_id))
        
        # ✅ NEW: Link question to the default course
        # cursor.execute(sql_link_question_to_course, (new_question_id, DEFAULT_COURSE_ID))

        print(f"Inserted question ID: {new_question_id} with options.")

        conn.commit() 
        
    except Exception as e:
        conn.rollback() 
        print(f"Database error: {e}")
        raise

    finally:
        cursor.close()
        conn.close()

# 2. Database fetch all questions
def fetch_questions(employee_id, fetch_scope='creator', course_id=None):
    """Fetches questions created by an employee. If course_id is provided, filters by course."""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if not employee_id and fetch_scope == 'creator':
        return {}

    try:
        emp_id = employee_id

        # Build query dynamically depending on whether a course filter was provided
        if course_id:
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
                JOIN
                    question_course qc ON qb.id = qc.question_id
                WHERE
                    qe.employee_id = %s 
                    AND qc.course_id = %s
            """
            cursor.execute(select_clause, (emp_id, course_id))
        else:
            # No course filter — return all questions created by this employee
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
# Vaidehi Changes

def get_question_by_id(question_id):
    """Fetches a single question and its options from the database by ID and returns course mapping."""
    conn = get_db_connection()
    # Use DictCursor to get results as dictionaries
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

        # Initialize the final question structure
        question_data = {
            # Use 'question_txt' from DB and map to 'text' for the frontend state
            'text': results[0]['question_txt'], 
            'options': [],
            'correct': '', # Will hold the index (0, 1, 2, 3) as a string
            'course_id': results[0].get('course_id') if results[0].get('course_id') else ''
        }
        
        # Collect options and find the correct one
        option_texts = []
        correct_text = None

        for row in results:
            option_texts.append(row['option_text'])
            if row['is_correct'] == 1:
                correct_text = row['option_text']

        # Ensure we have 4 options slots for the frontend form
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

# 3. Generate and Save Quiz  ❤️❤️❤️❤️❤️

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


def get_candidate_questions(teacher_id, course_id):
    """Return question IDs that would be used for a generated quiz (no DB writes).
    Tries teacher+course first, then falls back to course-wide pool."""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if not course_id:
            return { 'question_ids': [], 'used_teacher_filter': True, 'count': 0 }

        # teacher + course
        query_teacher_course = """
            SELECT qb.id FROM question_bank qb
            JOIN question_employee qe ON qb.id = qe.question_id
            JOIN question_course qc ON qb.id = qc.question_id
            WHERE qe.employee_id = %s AND qc.course_id = %s
            ORDER BY RAND() LIMIT 10
        """
        cursor.execute(query_teacher_course, (teacher_id, course_id))
        selected = cursor.fetchall()

        used_teacher_filter = True

        if not selected:
            # fallback
            fallback_query = """
                SELECT qb.id FROM question_bank qb
                JOIN question_course qc ON qb.id = qc.question_id
                WHERE qc.course_id = %s
                ORDER BY RAND() LIMIT 10
            """
            cursor.execute(fallback_query, (course_id,))
            selected = cursor.fetchall()
            used_teacher_filter = False

        ids = []
        for row in selected:
            if isinstance(row, dict):
                ids.append(row.get('id'))
            else:
                ids.append(row[0])

        return { 'question_ids': ids, 'used_teacher_filter': used_teacher_filter, 'count': len(ids) }

    except Exception as e:
        print(f"Error in get_candidate_questions: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def generate_and_save_quiz(teacher_id, course_id):
    """Generates a quiz using questions for the selected course.
    Prefer questions created by the teacher; if none exist, fall back to course-wide pool."""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if not course_id:
            print("DEBUG: generate_and_save_quiz called without course_id")
            return None

        # 1a. Try teacher + course questions first
        query_teacher_course = """
            SELECT qb.id FROM question_bank qb
            JOIN question_employee qe ON qb.id = qe.question_id
            JOIN question_course qc ON qb.id = qc.question_id
            WHERE qe.employee_id = %s AND qc.course_id = %s
            ORDER BY RAND() LIMIT 10
        """
        cursor.execute(query_teacher_course, (teacher_id, course_id))
        selected_questions = cursor.fetchall()

        print(f"DEBUG: teacher+course selected_questions count: {len(selected_questions)}; rows: {selected_questions}")

        used_teacher_filter = True

        # 1b. If none found, fall back to any question for the course
        if not selected_questions:
            print(f"DEBUG: No teacher-specific questions found for teacher_id={teacher_id}, course_id={course_id}. Falling back to course-wide pool.")
            fallback_query = """
                SELECT qb.id FROM question_bank qb
                JOIN question_course qc ON qb.id = qc.question_id
                WHERE qc.course_id = %s
                ORDER BY RAND() LIMIT 10
            """
            cursor.execute(fallback_query, (course_id,))
            selected_questions = cursor.fetchall()

            print(f"DEBUG: course-wide selected_questions count: {len(selected_questions)}; rows: {selected_questions}")

            used_teacher_filter = False

            if not selected_questions:
                print(f"DEBUG: No questions found for course_id={course_id} at all.")
                return None

        try:
            # 2. Generate unique token for the link
            quiz_token = str(uuid.uuid4())[:12]
            # This link points to your React route where the preview/quiz happens
            quiz_link = f"http://localhost:3000/take-quiz/{quiz_token}"

            # 3. Store Quiz Metadata (record whether teacher filter was used in quiz_status_note)
            insert_quiz = """
                INSERT INTO quizzes (teacher_id, course_id, quiz_title, quiz_link, quiz_token, quiz_status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_quiz,
                           (teacher_id,
                            course_id,
                            f"Quiz for Course {course_id}",
                            quiz_link,
                            quiz_token, "active"
                            ))
            quiz_id = cursor.lastrowid

            # 4. Save specific questions for this unique quiz instance
            for q in selected_questions:
                # row may have key 'id' or first column depending on cursor
                qid = q.get('id') if isinstance(q, dict) else q[0]
                print(f"DEBUG: Inserting quiz_questions_generated for quiz_id={quiz_id}, question_id={qid}")
                cursor.execute(
                    "INSERT INTO quiz_questions_generated (quiz_id, question_id) VALUES (%s, %s)",
                    (quiz_id, qid)
                )

            conn.commit()
            return {"id": quiz_id, "quiz_link": quiz_link, "token": quiz_token, "used_teacher_filter": used_teacher_filter, "question_count": len(selected_questions)}
        except Exception as e:
            conn.rollback()
            print(f"ERROR: Exception while saving quiz or questions: {e}")
            raise
    finally:
        cursor.close()
        conn.close()

# 4. Fetch Quiz Preview Details ❤️❤️❤️❤️❤️
def get_quiz_preview_details(token):
    """Fetches quiz metadata and questions for the preview page."""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # Note: Using correct table casing based on your previous SQL
        sql = """
            SELECT 
                q.quiz_title, 
                qb.id as question_id, 
                qb.question_txt, 
                am.option_text, 
                am.is_correct
            FROM quizzes q
            JOIN Quiz_Questions_Generated qqg ON q.id = qqg.quiz_id
            JOIN Question_Bank qb ON qqg.question_id = qb.id
            JOIN Answer_Map am ON qb.id = am.question_id
            WHERE q.quiz_token = %s
        """
        cursor.execute(sql, (token,))
        results = cursor.fetchall()
        
        if not results:
            return None

        # Restructure data: Group options under questions
        quiz_data = {
            "title": results[0]['quiz_title'],
            "questions": {}
        }
        
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
            
        # Convert dictionary to list
        quiz_data['questions'] = list(quiz_data['questions'].values())
        return quiz_data
        
    finally:
        cursor.close()
        conn.close()
        
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
# def delete_question(question_id):
#     """Deletes a question and all related options and links in a transaction."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         # 1. Delete options from answer_map (due to foreign key constraints, this is necessary)
#         cursor.execute("DELETE FROM answer_map WHERE question_id = %s", (question_id,))
        
#         # 2. Delete links from question_course
#         cursor.execute("DELETE FROM question_course WHERE question_id = %s", (question_id,))
        
#         # 3. Delete the question itself
#         delete_count = cursor.execute("DELETE FROM question_bank WHERE id = %s", (question_id,))
        
#         # Commit the transaction if all deletions succeeded
#         conn.commit()
        
#         # Return True only if the question itself was deleted
#         return delete_count > 0

#     except Exception as e:
#         conn.rollback()
#         print(f"Transaction failed for question deletion (ID {question_id}): {e}")
#         return False
#     finally:
#         cursor.close()
#         conn.close()
# ==============================================================================================
# if __name__ == "__main__":
#     app = create_app()
#     with app.app_context():
#         🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬
#         Testing fetch_questions 
#         test_employee_id = 1
#         test_scope = 'creator'
#         print(fetch_questions(test_employee_id, test_scope))

#         🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬
#         Example, Testing data
#         form_data = {
#             'question_txt': 'What is the capital of Germany?', 
#             'options': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg'],
#             'correct': '0'
#         }
        
#         insert_question(form_data)

#         🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬
#         Testing generate_and_save_quiz