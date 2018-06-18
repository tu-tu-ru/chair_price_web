import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors


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
        user_data = Database.find_one(collection="users", query={"email": email})
        # The pw contained in user_data is already hashed to pbkdf2_sha512

        if user_data is None:
            # This user does not exist
            raise UserErrors.UserNotExistError("This user does not exist.")
        if Utils.check_hashed_password(password, user_data["password"]) is not True:
            # Tell the user the pw is not correct
            raise UserErrors.IncorrectPasswordError("Your pw is not correct.")

        return True