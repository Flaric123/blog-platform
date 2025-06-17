from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from routers import articles, categories, comments, likes
from fastapi.middleware.cors import CORSMiddleware
from PYD.users import UserReturn
from auth import *

app = FastAPI()
APP_PREFIX='/api'

app.include_router(categories.router, prefix=f'{APP_PREFIX}/posts')
app.include_router(articles.router, prefix=f'{APP_PREFIX}/articles')
app.include_router(comments.router, prefix=f'{APP_PREFIX}/comments')
app.include_router(likes.router, prefix=f'{APP_PREFIX}/likes')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get('/verify-token/{token}')
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message":"Token is valid"}

@app.get("/users/me/")
async def read_users_me(
    user: Annotated[UserReturn, Depends(RoleChecker(allowed_roles=['admin']))],
    db: Session=Depends(get_db)
):
    return user