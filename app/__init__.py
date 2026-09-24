from flask import Flask

from app.config import Config, validate_config
from app.extensions import configure_security


def create_app():
    validate_config()

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config.from_object(Config)

    configure_security(app)

    from app.routes.health import health_bp
    from app.routes.chat import chat_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)

    return app