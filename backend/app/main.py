# similar to app/app.py on https://fastapi-users.github.io/fastapi-users/12.1/configuration/full-example/#__tabbed_1_3
from fastapi import FastAPI, Depends
from .auth import auth_backend, current_active_user, fastapi_users
from .schemas.user import UserCreate, UserRead, UserUpdate
from fastapi.middleware.cors import CORSMiddleware
from .routers.user import user_router
from .routers.post import post_router
from .routers.follow import follow_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include FastAPI-Users routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(user_router)
app.include_router(follow_router)
app.include_router(post_router)

# Protected route example
@app.get("/protected-route")
def protected_route(user = Depends(current_active_user)):
    return {"message": f"Hello {user.email}"}