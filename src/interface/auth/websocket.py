# import secrets
# from fastapi import FastAPI, WebSocket, Depends, Request, HTTPException, Query
# from fastapi.responses import JSONResponse
# from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
# from pydantic import BaseModel

# from src.models.users import User

# app = FastAPI()


# class Settings(BaseModel):
#     authjwt_secret_key: str = "secret"


# @AuthJWT.load_config
# def get_config():
#     return Settings()


# @app.exception_handler(AuthJWTException)
# def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#     return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# @app.websocket("/ws")
# async def websocket(
#     websocket: WebSocket, token: str = Query(...), Authorize: AuthJWT = Depends()
# ):
#     await websocket.accept()
#     try:
#         Authorize.jwt_required("websocket", token=token)
#         # Authorize.jwt_optional("websocket",token=token)
#         # Authorize.jwt_refresh_token_required("websocket",token=token)
#         # Authorize.fresh_jwt_required("websocket",token=token)
#         await websocket.send_text("Successfully Login!")
#         decoded_token = Authorize.get_raw_jwt(token)
#         await websocket.send_text(f"Here your decoded token: {decoded_token}")
#     except AuthJWTException as err:
#         await websocket.send_text(err.message)
#         await websocket.close()


# @app.post("/login")
# def login(user: User, Authorize: AuthJWT = Depends()):
#     if not secrets.compare_digest(hashed_password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Bad username or password")

#     access_token = Authorize.create_access_token(subject=user.username, fresh=True)
#     refresh_token = Authorize.create_refresh_token(subject=user.username)
#     return {"access_token": access_token, "refresh_token": refresh_token}
