from functools import wraps
from Weather import show_weather
from flask import Flask, request, render_template, session, redirect, url_for
from models import db, Users, Tasks
from config import Configuration
import json
import requests

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)

def login_required(route):
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return route(*args, **kwargs)

    return decorated_route


@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html')  # главная страница


def login_not_required(route):
    @wraps(route)
    def decorated_route(*args, **kwargs):
        if 'username' in session:
            return redirect(url_for('task'))
        return route(*args, **kwargs)

    return decorated_route


def registration_validation(userdata):
    user = Users.query.filter_by(username=userdata['username']).first()
    email = Users.query.filter_by(email=userdata['email']).first()
    if user is not None:
        return True
    if email is not None:
        return True


@app.route('/register', methods=["GET", "POST"])
@login_not_required
def register():
    if request.method == "POST":
        if registration_validation(request.form):
            return render_template('auth/register.html.html', title='Страница регистрации пользователя')
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = Users(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('task'))
    return render_template('auth/register.html', title='Страница регистрации пользователя')


@app.route('/task', methods=['GET'])
def task():
    x = show_weather()
    username = session.get('username')
    return render_template('to-do-page.html', username=username, temp=x.json['current']['temp_c'],city=x.json['location']['name'])


# Добавил проверку логина и пароля
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username, password=password).first()
        print(user.password, user.username)
        if user.password == password:
            session['username'] = username
            return redirect(url_for('task'))
        else:
            error = 'Invalid username or password'
            return render_template('auth/login.html', error=error)
    return render_template('auth/login.html')


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
    with app.app_context():
        db.create_all()
