from flask import Blueprint, request, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from app.models.project import Project, Board, Column, Task, TaskLog
from sqlalchemy.exc import SQLAlchemyError
from app import db

bp = Blueprint('project', __name__)

class ValidationError(Exception):

    def __init__(self, message, field=None):
        super().__init__(message)
        self.message = message
        self.field = field

    def __str__(self):
        if self.field:
            return f"Validation error in field '{self.field}': {self.message}"
        return f"Validation error: {self.message}"


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            db.session.rollback()
            return {'error': 'Validation error', 'details': str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'Database error', 'details': str(e)}, 500
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal error', 'details': str(e)}, 500
        finally:
            db.session.close()
    return wrapper

@handle_errors
def create_object(db, model_class, **kwargs):
    if 'name' in kwargs and not kwargs['name']:
        raise ValidationError("Name cannot be empty", field="name")
    
    new_object = model_class(**kwargs)
    db.session.add(new_object)
    db.session.commit()
    return {'message': f'{model_class.__name__} created'}, 201

MODELS_MAPPING = {
    'projects': Project,
    'boards': Board,
    'columns': Column,
    'tasks': Task,
    'task_log': TaskLog,
}

def get_model_by_name(model_name):
    return MODELS_MAPPING.get(model_name.lower())

@bp.route('/<model_name>', methods=['POST'])
def create_entity(model_name):
    data = request.form
    model_class = get_model_by_name(model_name)
    
    if not model_class:
        return {'error': 'Invalid model name'}, 404

    required_fields = {
        'Project': ['name', 'description', 'user_id'],
        'Board': ['name', 'project_id'],
        'Column': ['name', 'board_id'],
        'Task': ['title', 'column_id'],
        'TaskLog': ['event_type', 'user_id', 'task_id']
    }
    
    missing_fields = [field for field in required_fields.get(model_name, []) if field not in data]
    if missing_fields:
        return {'error': f'Missing fields: {missing_fields}'}, 400

    return create_object(db, model_class, **data)

form_configs = {
    'project': {'fields': ['name', 'description', 'user_id']},
    'board': {'fields': ['name', 'project_id']},
    'column': {'fields': ['name', 'board_id']},
    'task': {'fields': ['title', 'description', 'column_id']},
    'task_log': {'fields': ['event_type', 'user_id', 'details'], 'extra': {'task_id': 'task_id'}},
}

@bp.route('/create/<form_type>', methods=['GET'])
def show_form(form_type):
    config = form_configs.get(form_type)
    if not config:
        abort(404)
    template_name = f'create_{form_type}.html'
    return render_template(template_name, **config)