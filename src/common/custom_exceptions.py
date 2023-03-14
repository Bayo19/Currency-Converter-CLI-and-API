class UserNotFoundError(Exception):
    def __init__(self):
        self.message = "User not found"

    def __str__(self):
        return self.message
