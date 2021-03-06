# About the blueprint

from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from src.models.users.user import User
from src.models.users.errors import UserErrors
# from src.models.users.errors import IncorrectPasswordError

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['POST', 'GET'])
def login_user():
    # 两种不同的 methods 对应不同的动作
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # Hashed pw from user input form

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors as e:
            return e.message

    return render_template("users/login.jinja2")


@user_blueprint.route('/register', methods=['GET','POST'])
def register_user():
    # If a user does not exist, register it and then log it in
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']  # Hashed pw from user input form

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors as e:
            return e.message

    return render_template('users/register.jinja2')


@user_blueprint.route('/alerts')
def user_alerts():
    """
    find user from the browser session, and find all the alerts with user's email
    :return: render_template; for the `alerts=alerts` parameter, the former one is render_template()'s para,
        the latter one is the alerts get from user
    """
    user = User.find_user_by_email(session['email'])
    alerts = user.get_alert()
    return render_template("users/alerts.jinja2", alerts=alerts)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))  # return the page back to Home; `'home'` is the home() function in app.py


# Check all the alerts for specific user
@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
