from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from routers import articles, categories, comments, users
from fastapi.middleware.cors import CORSMiddleware
from PYD.users import UserReturn
from auth import *

app = FastAPI()

app.include_router(categories.router)
app.include_router(articles.router)
app.include_router(comments.router)

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
) -> UserReturn:
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
    user.api_access_token=access_token
    db.commit()
    db.refresh(user)
    return user

@app.get('/verify-token/{token}')
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message":"Token is valid"}

# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user

# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]