from fastapi import FastAPI, Depends
from .auth import auth_backend, current_active_user, fastapi_users
from .schemas.user import UserCreate, UserRead

app = FastAPI()

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

# Protected route example
@app.get("/protected-route")
def protected_route(user = Depends(current_active_user)):
    return {"message": f"Hello {user.email}"}