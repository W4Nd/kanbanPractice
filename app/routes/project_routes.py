from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models.project import Project, Board, Column, Task, TaskLog
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('project', __name__)

def create_object(model_class, **kwargs):
    try:
        new_object = model_class(**kwargs)
        db.session.add(new_object)
        db.session.commit()
        return jsonify({'message': f'{model_class.__name__} created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/projects', methods=['POST'])
def create_project():
    data = request.form
    return create_object(Project, name=data['name'], description=data['description'], user_id=data['user_id'])

@bp.route('/boards', methods=['POST'])
def create_board():
    data = request.form
    return create_object(Board, name=data['name'], project_id=data['project_id'])

@bp.route('/columns', methods=['POST'])
def create_column():
    data = request.form
    return create_object(Column, name=data['name'], board_id=data['board_id'])

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.form
    return create_object(Task, title=data['title'], description=data['description'], status=data['status'], column_id=data['column_id'], assigned_user_id=data['assigned_user_id'])

@bp.route('/tasks/<int:task_id>/logs', methods=['POST'])
def create_task_log(task_id):
    data = request.form
    return create_object(TaskLog, task_id=task_id, event_type=data['event_type'], user_id=data['user_id'], details=data['details'])

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