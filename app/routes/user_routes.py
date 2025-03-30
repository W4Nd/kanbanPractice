from flask import Blueprint, request, jsonify, render_template
from app.services.password_service import PasswordService
from app.repositories.user_repository import UserRepository

user_bp = Blueprint('user', __name__)

def validate_user_data(user_data: dict) -> str:
    if not user_data:
        return "Request data is empty"
    
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in user_data:
            return f"Missing required field: {field}"
        
        if not isinstance(user_data[field], str) or not user_data[field].strip():
            return f"Field {field} must be a non-empty string"

    if '@' not in user_data['email'] or '.' not in user_data['email'].split('@')[-1]:
        return "Invalid email format"

    if len(user_data['password']) < 8:
        return "Password must be at least 8 characters long"
    
    if not user_data['username'].replace('_', '').isalnum():
        return "Username can only contain letters, numbers and underscores"
    
    if len(user_data['username']) < 3:
        return "Username must be at least 3 characters long"
    
    return None


@user_bp.route('/users', methods=['POST'])
def api_create_user():
    user_data = request.get_json()
    
    if error := validate_user_data(user_data):
        return jsonify({"error": error}), 400
    
    if UserRepository.get_by_username(user_data["username"]):
        return jsonify({"error": "Username already exists"}), 409
    
    password_hash = PasswordService.hash_password(user_data["password"])
    user = UserRepository.create_user(user_data["username"], user_data["email"], password_hash)
    
    return jsonify({"id": user.id, "message": "User created"}), 201


@user_bp.route('/create_user', methods=['GET', 'POST'])
def create_user_form():
    if request.method == 'POST':
        user_data = {
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        
        if error := validate_user_data(user_data):
            return render_template('create_user.html', error=error)
            
        if UserRepository.get_by_username(user_data["username"]):
            return render_template('create_user.html', error="Username already exists")
            
        password_hash = PasswordService.hash_password(user_data["password"])
        UserRepository.create_user(user_data["username"], user_data["email"], password_hash)
        
        return render_template('create_user.html', success="User created successfully!")
    
    return render_template('create_user.html')