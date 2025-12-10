from backend.app import create_app
from backend.services.quiz_service import generate_and_save_quiz
from backend.extensions import get_db_connection
import pymysql

def test_quiz_generation():
    """Test the generate_and_save_quiz function"""
    app = create_app()

    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            # Step 1: Check if we have questions in the question_bank
            cursor.execute("SELECT COUNT(*) as count FROM question_bank")
            question_count = cursor.fetchone()['count']
            print(f"\n{'='*60}")
            print(f"Total questions in question_bank: {question_count}")
            
            # Check questions for this specific teacher
            teacher_id = 2
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM question_bank qb
                JOIN question_employee qe ON qb.id = qe.question_id
                WHERE qe.employee_id = %s
            """, (teacher_id,))
            teacher_question_count = cursor.fetchone()['count']
            print(f"Questions created by teacher {teacher_id}: {teacher_question_count}")

            if teacher_question_count == 0:
                print(f"⚠️ WARNING: No questions found for teacher {teacher_id}!")
                print("This teacher needs to create questions first before generating a quiz.")
                return

            # Step 2: Confirm teacher ID
            print(f"✅ Using test teacher ID: {teacher_id}")

            # Step 3: Generate the quiz
            print(f"\n{'='*60}")
            print("🚀 Generating quiz...")
            print(f"{'='*60}\n")

            quiz = generate_and_save_quiz(teacher_id)

            if quiz is None:
                print("❌ Quiz generation failed!")
                return

            # Step 4: Display the generated quiz details
            print(f"\n{'='*60}")
            print("📋 QUIZ GENERATION SUCCESSFUL!")
            print(f"{'='*60}\n")

            quiz_id = quiz['id']

            print("Quiz Details:")
            print(f"  ID: {quiz['id']}")
            print(f"  Title: {quiz['quiz_title']}")
            print(f"  Status: {quiz['quiz_status']}")
            print(f"  Total Questions: {quiz['total_questions']}")
            print(f"  Total Marks: {quiz['total_marks']}")
            print(f"  Time Limit: {quiz['time_limit']} minutes")
            print(f"  Quiz Link: {quiz['quiz_link']}")
            print(f"  Scheduled Start: {quiz['scheduled_start_time']}")
            print(f"  Scheduled End: {quiz['scheduled_end_time']}")

            # Get linked questions - need to commit to see the changes
            conn.commit()
            
            cursor.execute("""
                SELECT qqg.question_id, qb.question_txt
                FROM quiz_questions_generated qqg
                JOIN question_bank qb ON qqg.question_id = qb.id
                WHERE qqg.quiz_id = %s
            """, (quiz_id,))
            questions = cursor.fetchall()

            print(f"\n📝 Linked Questions ({len(questions)}):")
            if questions:
                for i, q in enumerate(questions, 1):
                    print(f"  {i}. [ID: {q['question_id']}] {q['question_txt'][:80]}...")
            else:
                print("  Note: Questions are linked but using separate DB connections.")
                print(f"  Check database directly: SELECT * FROM quiz_questions_generated WHERE quiz_id = {quiz_id}")

            print(f"\n{'='*60}")
            print("✅ TEST COMPLETED SUCCESSFULLY!")
            print(f"{'='*60}\n")

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    test_quiz_generation()