class Error(Exception):
    pass


class AuthError(Error):

    def __init__(self, message):
        self.message = message


class KeyNotFound(Error):

    def __init__(self, key):
        self.message = f"Response body not contains {key}"


class UserNotFound(Error):

    def __init__(self, user):
        self.message = f"User {user} not found in config file"


class ConfigNotFound(Error):

    def __init__(self, path_to_config):
        self.message = f'Config not found in directory: {path_to_config}'


class EnvNotFound(Error):

    def __init__(self, var_name):
        self.message = f'Env variable not fount: {var_name}'


class StatusCodeWrong(Error):

    def __init__(self, status_code):
        self.message = f'Status code wrong: {status_code}'
