from flask import Flask

from src.common.database import Database
from src.models.users.views import user_blueprint

app = Flask(__name__)
app.config.from_object("src.config")
app.secret_key = "123"


# Initialize the database
@app.before_first_request
def init_db():
    Database.initialize()


app.register_blueprint(user_blueprint, url_prefix="/users")
# Register the blue print with the prefix 'users'

