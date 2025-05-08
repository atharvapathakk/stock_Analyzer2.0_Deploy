from flask import Flask
from routes import main
from extensions import db, login_manager
from models import User
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the extensions
db.init_app(app)
login_manager.init_app(app)

# Register the blueprint with the URL prefix '/'
app.register_blueprint(main, url_prefix='/')

# Load user session for Flask-Login
@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
