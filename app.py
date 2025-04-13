from flask import Flask
from routes import main
from extensions import db, login_manager
from models import User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

# 👉 Add this line to tell Flask-Login where to redirect unauthenticated users
login_manager.login_view = 'main.login'

# Register blueprints
app.register_blueprint(main, url_prefix='/')

# Load user for session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)