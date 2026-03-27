from flask import Flask
from backend.routes.users import users_bp
from backend.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)

    # app.secret_key = "test-secret-key" # needed for Flask sessions

    app.register_blueprint(users_bp,url_prefix = "/users")
    app.register_blueprint(auth_bp,url_prefix = "/auth")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=8080)
