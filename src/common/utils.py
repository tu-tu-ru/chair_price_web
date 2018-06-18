from passlib.hash import pbkdf2_sha512


class Utils:

    @staticmethod
    def hash_password(password):
        """
        return a hashed password using pbkdf2_sha512
        :param password: a sha_512 hashed pw from web login form
        :return: a sha_512 -> pbkdf2_sha512 pw
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        check the pw that user submit matches that of in the database
        the pw in database is encrypted
        :param password: sha512 hashed password
        :param hashed_password: pbkdf2_sha512 hashed pw
        :return:
        """

        return pbkdf2_sha512.verify(password, hashed_password)
