from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import project_routes
    from app.routes import user_routes
    app.register_blueprint(project_routes.bp)
    app.register_blueprint(user_routes.bp)

    return app
