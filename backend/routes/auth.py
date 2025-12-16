from flask import Blueprint, request, jsonify, session
from ..services.auth_service import AuthService

# Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Service
auth_service = AuthService()

# ✅ Mac compatibility - support both localhost and 127.0.0.1
ALLOWED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

# ----------------- Signup -----------------
@auth_bp.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        new_user_id = auth_service.register_user(name, email, password)
        return jsonify({
            "message": "User created successfully",
            "user_id": new_user_id
        }), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 409
    except Exception as e:
        print(f"Error during signup: {e}")
        return jsonify({"message": "An internal server error occurred"}), 500

# ----------------- Login -----------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"message": "Missing email or password"}), 400

    user = auth_service.authenticate_user(email, password)

    if user:
        master_id = getattr(user, 'master_id', None)
        user_id = master_id if master_id else getattr(user, 'id', None)

        # ⚠️ FIX: AGGRESSIVE SESSION CLEAR
        # This completely wipes the old session data before setting new keys, 
        # guaranteeing a fresh, small cookie.
        session.clear()
        
        session['logged_in'] = True
        session['id'] = user_id
        session['role'] = getattr(user, 'role', 'student')
        
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.master_id,
                "name": user.username,
                "role": session['role']
            }
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ----------------- Logout -----------------
@auth_bp.route('/logout', methods=['POST'])
def logout():
    
    session.clear()
    return jsonify({"message": "Logout successful"}), 200

# ----------------- Get Profile -----------------
@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    
    if session.get('logged_in'):
        user_id = session.get('id')
        if not user_id:
             return jsonify({"message": "User ID not found in session."}), 401
        
        user_details = auth_service.get_user_by_id(user_id)
        if user_details:
            return jsonify({
                "user_id": user_details.master_id, 
                "username": user_details.username,
                "email": user_details.email,
                "role": getattr(user_details, 'role', 'student'),
                "message": "User profile data retrieved."
            }), 200
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message": "Unauthorized"}), 401
