from flask import Flask, render_template, session
from app.controller.books_controller import bp as books_bp
from app.controller.auth_controller import bp as auth_bp
from app.model.user import db
from flask_login import LoginManager
from app.model.user import User, UserRepo

app = Flask(__name__, template_folder="app/view", static_folder="app/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flaskweb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "key1220__Botik__"
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    # Старый способ (устаревший):
    # return User.query.get(int(user_id))

    # Новый способ (рекомендуемый):
    with app.app_context():
        return db.session.get(User, int(user_id))


app.register_blueprint(books_bp)
app.register_blueprint(auth_bp)

with app.app_context():
    repo = UserRepo()
    if not repo.get_by_username('admin'):
        repo.add('admin', 'password123')


@app.get("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)