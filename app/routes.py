from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import User, Project, Board, Column, Task, TaskLog
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('api', __name__)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    password_hash = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    new_project = Project(name=data['name'], description=data['description'], user_id=data['user_id'])
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201

@bp.route('/boards', methods=['POST'])
def create_board():
    data = request.get_json()
    new_board = Board(name=data['name'], project_id=data['project_id'])
    db.session.add(new_board)
    db.session.commit()
    return jsonify({'message': 'Board created successfully'}), 201

@bp.route('/columns', methods=['POST'])
def create_column():
    data = request.get_json()
    new_column = Column(name=data['name'], board_id=data['board_id'])
    db.session.add(new_column)
    db.session.commit()
    return jsonify({'message': 'Column created successfully'}), 201

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'], status=data['status'], column_id=data['column_id'], assigned_user_id=data['assigned_user_id'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

@bp.route('/tasks/<int:task_id>/logs', methods=['POST'])
def create_task_log(task_id):
    data = request.get_json()
    new_log = TaskLog(task_id=task_id, event_type=data['event_type'], user_id=data['user_id'], details=data['details'])
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Task log created successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@bp.route('/create_user', methods=['GET'])
def create_user_form():
    return render_template('create_user.html')

@bp.route('/create_project', methods=['GET'])
def create_project_form():
    return render_template('create_project.html')

@bp.route('/create_board', methods=['GET'])
def create_board_form():
    return render_template('create_board.html')

@bp.route('/create_column', methods=['GET'])
def create_column_form():
    return render_template('create_column.html')

@bp.route('/create_task', methods=['GET'])
def create_task_form():
    return render_template('create_task.html')

@bp.route('/create_task_log/<int:task_id>', methods=['GET'])
def create_task_log_form(task_id):
    return render_template('create_task_log.html', task_id=task_id)