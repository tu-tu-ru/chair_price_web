import uuid

from src.common.database import Database


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
        user_data = Database.find_one(collection="users", query={"email":email})

        if user_data is None:
            # This user does not exist
            pass
        if Utils.check_hashed_passowrd(password, user_data["password"]) is not True:
            # Tell the user the pw is not correct
            pass

        return True