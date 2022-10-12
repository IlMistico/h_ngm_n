from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.datasource.db import UsersDb

from src.models.users import User, UserInDB

auth_router = APIRouter()

db = UsersDb()


def hash_password(password: str):
    return "hashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token):
    """
    Function to get the username from the OAuth token. Since in this fake version the token IS the username, nothing more is necessary.
    Obviously, a real version would have a token generation, storage and validation/renovation flow.
    """
    return db.get_user(token)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = db.get_user(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
