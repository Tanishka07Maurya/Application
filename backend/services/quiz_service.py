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


# 1. Database Add Question
def insert_question(form_data, teacher_id): 
    conn = get_db_connection()
    cursor = conn.cursor()
    DEFAULT_TYPE = "MCQ"
    DEFAULT_UNIT = 1
    DEFAULT_MARKS = 1
    DEFAULT_COURSE_ID = 21 #for now

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
        correct_index = int(form_data['correct_index'])

        for index, option_text in enumerate(form_data['options']):
            is_correct_flag = 1 if index == correct_index else 0
            cursor.execute(sql_insert_options, (
                new_question_id,
                option_text,
                is_correct_flag,
            ))

        # ✅ NEW: Link question to the teacher
        cursor.execute(sql_link_question_to_creator, (new_question_id, teacher_id))
        
        # ✅ NEW: Link question to the default course
        cursor.execute(sql_link_question_to_course, (new_question_id, DEFAULT_COURSE_ID))

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
def fetch_questions(employee_id, fetch_scope='creator'):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) 
    
    if not employee_id and fetch_scope == 'creator':
        return []
    
    try:
        # Select the course_id from dropdown and connect here
        course_id = 21 # for now
        emp_id = employee_id
        # Fetch questions based on employee and course
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

        select_params = (emp_id, course_id)
        print(f"DEBUG: SQL Params: {select_params}, Types: {type(emp_id), type(course_id)}")

        cursor.execute(select_clause, (emp_id, course_id)) 
        results = cursor.fetchall()

    except Exception as e:
        print(f"Query failed to execute: {e}")
        return []
        
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
        
# 3. Generate and Save Quiz
def generate_and_save_quiz(teacher_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) 
    
    # teacher_id = None
    quiz_id = None

   
    try:    
        # ✅ Filter questions by the logged-in teacher
        cursor.execute("""
            SELECT qb.id 
            FROM question_bank qb
            JOIN question_employee qe ON qb.id = qe.question_id
            WHERE qe.employee_id = %s
        """, (teacher_id,))
        all_questions = cursor.fetchall()

        all_ids = [q['id'] for q in all_questions]
        SAMPLE_SIZE = 5
        
        print(f"DEBUG: Total questions available for teacher {teacher_id}: {len(all_ids)}")
        
        if not all_ids:
            print("WARNING: No questions found in question_bank!")
            return None 

        selected_ids = random.sample(all_ids, min(SAMPLE_SIZE, len(all_ids)))
        print(f"DEBUG: Selected question IDs: {selected_ids}")

        unique_link_id = str(uuid.uuid4())
        quiz_title = f"New Quiz - {datetime.now().strftime('%Y%m%d%H%M%S')}"

        sql_quiz = """
            INSERT INTO generated_quizzes 
                (teacher_id, quiz_title, quiz_status, total_questions, total_marks, time_limit, quiz_link, scheduled_start_time, scheduled_end_time)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        QUIZ_STATUS = 'DRAFT'
        TOTAL_QUESTIONS = len(selected_ids)
        TOTAL_MARKS = TOTAL_QUESTIONS * 10 
        TIME_LIMIT = 10 
        SCHEDULED_START = datetime.now()
        SCHEDULED_END = datetime.now() + timedelta(days=7) 

        cursor.execute(sql_quiz, (
            teacher_id,
            quiz_title,
            QUIZ_STATUS,
            TOTAL_QUESTIONS,
            TOTAL_MARKS,
            TIME_LIMIT,
            unique_link_id, 
            SCHEDULED_START,
            SCHEDULED_END
        ))
        quiz_id = cursor.lastrowid
        print(f"DEBUG: Created quiz with ID: {quiz_id}, Title: {quiz_title}")
        print(f"DEBUG: Quiz settings - Status: {QUIZ_STATUS}, Questions: {TOTAL_QUESTIONS}, Marks: {TOTAL_MARKS}, Time: {TIME_LIMIT} min")
        conn.commit()
        
        sql_link_questions = "INSERT INTO quiz_questions_generated (quiz_id, question_id) VALUES (%s, %s)"
        
        question_links = [(quiz_id, q_id) for q_id in selected_ids]

        cursor.executemany(sql_link_questions, question_links)
        conn.commit()
        print(f"DEBUG: Successfully linked {len(question_links)} questions to quiz {quiz_id}")
        
        # Fetch and return the complete quiz details
        cursor.execute("""
            SELECT * FROM generated_quizzes 
            WHERE id = %s
        """, (quiz_id,))
        quiz_details = cursor.fetchone()
        
        return quiz_details 
        
    finally:
        cursor.close()
        conn.close()

# if __name__ == "__main__":
#     app = create_app()
    # with app.app_context():
        # 🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬
        # Testing fetch_questions 
        # test_employee_id = 1
        # test_scope = 'creator'
        # print(fetch_questions(test_employee_id, test_scope))

        # 🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬
        # Example, Testing data
        # form_data = {
        #     'question_txt': 'What is the capital of Germany?', 
        #     'options': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg'],
        #     'correct': '0'
        # }
        
        # insert_question(form_data)

        # 🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬🥬
        # Testing generate_and_save_quiz
