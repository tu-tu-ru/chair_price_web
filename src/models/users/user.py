import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from src.models.alerts.alert import Alert


class User:
    def __init__(self, email, password, _id):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        To verify whether the email/pw pair is valid.
        :param email: A string
        :param password: A (sha25) hashed password
        :return: True if valid, otherwise False
        """
        user_data = Database.find_one(collection=UserConstants.COLLECTION, query={"email": email})
        # The pw contained in user_data is already hashed to pbkdf2_sha512

        if user_data is None:
            # This user does not exist
            raise UserErrors.UserNotExistError("This user does not exist.")
        if Utils.check_hashed_password(password, user_data["password"]) is not True:
            # Tell the user the pw is not correct
            raise UserErrors.IncorrectPasswordError("Your pw is not correct.")

        return True

    @staticmethod
    def register_user(email, password):
        """
        To register a user with email and hashed password.
        src.common.utils will do the hash work
        :param email:
        :param password: hashed pw
        :return: True if register successfully, or False otherwise
        """

        user_data = Database.find_one(collection=UserConstants.COLLECTION, query={"email": email})

        if user_data is not None:
            # Tell user they are already registered
            raise UserErrors.UserAlreadyRegisterError('User already exists.')

        if not Utils.is_valid_email(email):
            # For these users who typed invalid email
            # Tell user the email is not correct
            # Using RegEx
            raise UserErrors.InvalidEmailError('Input email address invalid.')

        User(email=email, password=Utils.hash_password(password), _id=None).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_user_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))

    def get_alert(self):
        return Alert.find_alert_by_email(self.email)
