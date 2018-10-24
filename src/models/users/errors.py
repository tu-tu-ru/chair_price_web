
class UserErrors(Exception):
    def __init__(self, message):
        self.message = message

# 这两个 class 的功能都是一样的，所以可以创建一个公用的**父类**


class UserNotExistError(UserErrors):
    pass


class IncorrectPasswordError(UserErrors):
    pass

class UserAlreadyRegisterError(UserErrors):
    pass

class InvalidEmailError(UserErrors):
    pass