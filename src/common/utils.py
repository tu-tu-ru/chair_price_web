# coding=utf-8
#from passlib.hash import pbkdf2_sha512
from passlib.hash import sha256_crypt
import re

"""
用户输入一个正常的密码，然后encryption成长密码（如下），
```
import hashlib
m=hashlib.sha512()
m.update(b"123")
m.hexdigest()
```

然后hash成pbkdf2密码

"""


class Utils:

    @staticmethod
    def hash_password(password):
        """
        return a hashed password using pbkdf2_sha512
        :param password: a sha_512 hashed pw from web login form
        :return: a sha_512 -> pbkdf2_sha512 pw
        """
        #return passlib.hash.pbkdf2_sha512.encrypt(password)
        return sha256_crypt.hash(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        check the pw that user submit matches that of in the database
        the pw in database is encrypted
        :param password: sha512 hashed password
        :param hashed_password: pbkdf2_sha512 hashed pw
        :return: true if password matches
        """


        return sha256_crypt.verify(password,hashed_password)


    @staticmethod
    def is_valid_email(email):
        email_address_mathcer =re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        if email_address_mathcer.match(email):
            return True
        else:
            return False
        
