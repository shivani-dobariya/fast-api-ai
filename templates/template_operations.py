from fastapi import APIRouter

template_router = APIRouter()


@template_router.get("/")
async def read_users():
    return {"message": "List of users"}


@template_router.get("/{user_id}")
async def read_user(user_id: int):
    return {"message": f"User with ID {user_id}"}
