from src.datasource.db import UsersDb


users_db = UsersDb()


def hash_password(password: str):
    return "hashed" + password


def decode_token(token):
    """
    Function to get the username from the OAuth token. Since in this fake version the token IS the username, nothing more is necessary.
    Obviously, a real version would have a token generation, storage and validation/renovation flow.
    """
    return users_db.get_user(token)
