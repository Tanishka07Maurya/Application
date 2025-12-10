from argon2 import PasswordHasher, exceptions as argon2_exceptions
from ..extensions import get_db_connection
from ..models.user import User
import pymysql.cursors
import re

class AuthService:
    ROLE_MAPPING = {
        "student": 1,
        "professor": 2,
        "admin": 3,
    }

    def __init__(self):
        self.ph = PasswordHasher()
        # Email regex patterns
        self.ADMIN_EMAIL_PATTERN = r'^(admin-\d+|[a-zA-Z0-9.]+admin)@gsfcuniversity\.ac\.in$'
        self.PROFESSOR_EMAIL_PATTERN = r'^[a-zA-Z0-9.]+@gsfcuniversity\.ac\.in$'
        self.STUDENT_EMAIL_PATTERN = r'^\d+@gsfcuniversity\.ac\.in$'

    # Determine role based on email
    def _determine_role(self, email):
        role_name = None
        if re.match(self.ADMIN_EMAIL_PATTERN, email):
            role_name = "admin"
        elif re.match(self.STUDENT_EMAIL_PATTERN, email):
            role_name = "student"
        elif re.match(self.PROFESSOR_EMAIL_PATTERN, email):
            role_name = "professor"
        else:
            raise ValueError("Invalid university email format")
        return self.ROLE_MAPPING[role_name]

    def _validate_master_account(self, email, role_name, cursor):
        """Checks if the email exists in the respective master table and returns the master ID."""
        if role_name == 'professor' or role_name == 'admin':
            master_table = 'employee'
            id_column = 'id' # ⚠️ Assuming your employee table uses 'id' as primary key
        elif role_name == 'student':
            master_table = 'student'
            id_column = 'id' # ⚠️ Assuming your student table uses 'id' as primary key
        else:
            return None # Fallback for unknown roles

        sql = f"SELECT {id_column} AS master_id FROM {master_table} WHERE email=%s"
        cursor.execute(sql, (email,))
        master_record = cursor.fetchone()
        
        if not master_record:
            raise ValueError(f"Email not found in the {master_table} database. Cannot register.")
            
        return master_record['master_id']

    def _hash_password(self, password):
        return self.ph.hash(password)

    def _check_password(self, stored_hash, password):
        try:
            return self.ph.verify(stored_hash, password)
        except argon2_exceptions.VerifyMismatchError:
            return False   
        

    # ----------------- SIGNUP -----------------
    def register_user(self, user_name, email, password):
        password_hash = self._hash_password(password)
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            # Check if user exists
            cursor.execute("SELECT user_id FROM user_account WHERE email=%s", (email,))
            if cursor.fetchone():
                raise ValueError("User with this email already exists")

            # 2. Determine role based on email regex
            role_id = self._determine_role(email)
            role_name_map = {v: k for k, v in self.ROLE_MAPPING.items()}
            role_name = role_name_map[role_id]

            # 3. ✅ NEW: VALIDATE AGAINST MASTER TABLE --> throws error if email not in maters table
            master_id = self._validate_master_account(email, role_name, cursor)

            # 4. Insert into user_account
            sql = "INSERT INTO user_account (user_id, user_name, email, password_hash, role_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (master_id, user_name, email, password_hash, role_id))
            conn.commit()

            return master_id
        finally:
            cursor.close()
            conn.close()

    # ----------------- LOGIN -----------------
    def authenticate_user(self, email, password):
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            # 1. Fetch user record from user_account
            sql = "SELECT user_id, user_name, email, password_hash, role_id FROM user_account WHERE email=%s"
            cursor.execute(sql, (email,))
            user_record = cursor.fetchone()

            if not user_record:
                return None

            stored_hash = user_record.pop('password_hash')
            if not self._check_password(stored_hash, password):
                return None

            # 2. Map role_id to role name
            role_name_map = {v: k for k, v in self.ROLE_MAPPING.items()}
            db_role_id = user_record.pop('role_id')
            role_name = role_name_map.get(db_role_id, 'unknown')
            user_record['role'] = role_name
            user_record['username'] = user_record.pop('user_name')
            user_record['password_hash'] = stored_hash

            # 3. ✅ NEW: Look up the Master ID (employee_id/student_id)
            # This ID will be used for session['id'] and question ownership/filtering
            master_id = self._validate_master_account(email, role_name, cursor)
            user_record['master_id'] = master_id

            return User.from_dict(user_record)
        finally:
            cursor.close()
            conn.close()

    # ----------------- GET USER BY ID -----------------
    def get_user_by_id(self, user_id):
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            sql = "SELECT user_id, user_name, email, password_hash, role_id FROM user_account WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            user_record = cursor.fetchone()
            if not user_record:
                return None

            stored_hash = user_record.pop('password_hash')
            db_role_id = user_record.pop('role_id')
            role_name_map = {v: k for k, v in self.ROLE_MAPPING.items()}

            user_record['role'] = role_name_map.get(db_role_id, 'unknown')
            user_record['username'] = user_record.pop('user_name')
            user_record['password_hash'] = stored_hash

            role_name = user_record['role']
            master_id = self._validate_master_account(user_record['email'], role_name, cursor)
            user_record['master_id'] = master_id

            return User.from_dict(user_record)
        finally:
            cursor.close()
            conn.close()