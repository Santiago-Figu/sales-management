from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from app.application.services.user_service import UserService
from app.infrastructure.api.v1.schemas.user import(
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
    UserFind,
    UserDeleteResponse,
    UserUpdateResponse
)

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", response_model = UserResponseSchema)
def create_user(user: UserCreateSchema):
    user_data = user.model_dump()
    return UserService.create_user(user_data)

@router.get("/{user_id}", response_model = UserResponseSchema)
def read_user(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user

@router.get("/", response_model=List[UserResponseSchema])
def read_all_users():
    return UserService.get_all_users()

@router.put("/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: int, user: UserUpdateSchema):
    user_data = user.model_dump(exclude_unset=True)
    update_user = UserService.update_user(user_id, user_data)
    if not update_user:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user

@router.delete("/{user_id}", response_model=UserDeleteResponse)
def delete_user(user_id: int):
    success = UserService.delete_user(user_id)
    if not success:
        raise HTTPException(status_code = 404, detail = "User not found")
    response = {"message": "User deleted successfully"}
    return JSONResponse(content = response, status_code = 200)