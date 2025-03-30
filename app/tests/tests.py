import pytest
from unittest.mock import MagicMock, patch
from routes.project_routes import create_object, ValidationError
from sqlalchemy.exc import SQLAlchemyError

class MockDB:
    def __init__(self):
        self.session = MagicMock()

class MockModel:
    def __init__(self, **kwargs):
        if 'name' in kwargs and not kwargs['name']:
            raise ValidationError("Invalid data", field="name")
        self.id = 1
        self.data = kwargs

@pytest.fixture
def mock_db():
    return MockDB()

def test_create_object_success(mock_db):
    result = create_object(mock_db, MockModel, name="Valid Name")
    
    assert result[1] == 201
    assert "created successfully" in result[0]['message']
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()

def test_create_object_validation_error(mock_db):
    result = create_object(mock_db, MockModel, name="")  
    
    assert result[1] == 400
    assert result[0]['error'] == 'Validation error'
    assert result[0]['field'] == 'name'
    mock_db.session.rollback.assert_called_once()

def test_create_object_db_error(mock_db):
    mock_db.session.commit.side_effect = SQLAlchemyError("DB error")
    
    result = create_object(mock_db, MockModel, name="Test")
    
    assert result[1] == 500
    assert "Database error" in result[0]['error']
    mock_db.session.rollback.assert_called_once()

def test_create_object_session_always_closes(mock_db):
    mock_db.session.commit.side_effect = Exception("Any error")
    
    result = create_object(mock_db, MockModel, name="Test")
    
    mock_db.session.close.assert_called_once()
    assert result[1] == 500