from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models.project import Project, Board, Column, Task, TaskLog

bp = Blueprint('project', __name__)

@bp.route('/projects', methods=['POST'])
def create_project():
    data = request.form
    new_project = Project(name=data['name'], description=data['description'], user_id=data['user_id'])
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201

@bp.route('/boards', methods=['POST'])
def create_board():
    data = request.form
    new_board = Board(name=data['name'], project_id=data['project_id'])
    db.session.add(new_board)
    db.session.commit()
    return jsonify({'message': 'Board created successfully'}), 201

@bp.route('/columns', methods=['POST'])
def create_column():
    data = request.form
    new_column = Column(name=data['name'], board_id=data['board_id'])
    db.session.add(new_column)
    db.session.commit()
    return jsonify({'message': 'Column created successfully'}), 201

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.form
    new_task = Task(title=data['title'], description=data['description'], status=data['status'], column_id=data['column_id'], assigned_user_id=data['assigned_user_id'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

@bp.route('/tasks/<int:task_id>/logs', methods=['POST'])
def create_task_log(task_id):
    data = request.form
    new_log = TaskLog(task_id=task_id, event_type=data['event_type'], user_id=data['user_id'], details=data['details'])
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Task log created successfully'}), 201


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