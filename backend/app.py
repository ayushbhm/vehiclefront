from flask import Flask, render_template
from config import Config
from database import db
from werkzeug.security import generate_password_hash
from models import User
from login_manager import login_manager


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    # db.create_all()
    if not User.query.filter_by(role='admin').first():
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created: username=admin, password=admin123")

@app.route('/')
def index():
    return render_template('index.html')

from controllers.admin_controller import *
from controllers.user_controller import *
from controllers.auth_controller import *
from controllers.apis import *

if __name__ == "__main__":
    app.run(debug=True)
