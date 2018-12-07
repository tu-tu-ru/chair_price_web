from flask import Flask, render_template, redirect

from src.common.database import Database
from src.models.users.views import user_blueprint
from src.models.stores.views import store_blueprint
from src.models.alerts.views import alert_blueprint

app = Flask(__name__)
app.config.from_object("src.config")
app.secret_key = "123"


# Initialize the database
@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.jinja2')


app.register_blueprint(user_blueprint, url_prefix="/users")
# Register the blue print with the prefix 'users'
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")