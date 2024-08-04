from fastapi import HTTPException, status, Depends, Security
from typing import Optional
from sqlalchemy.orm import Session
from repository.user_repository import UserRepository
from config.database import get_db
from schemas.user_schema import UserInput, UserOutput
from models.user_model import UserModel
from utils.jwt_handler import verify_token
from utils.hashing import Hash
from fastapi.security.api_key import APIKeyHeader

api_header = APIKeyHeader(name="Authorization")

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.db = db  # Correctly assign the db parameter

    def create(self, data: UserInput) -> UserOutput:
        if self.user_repository.user_exist_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
            )
        data.password = Hash.hash_password(data.password)  # Ensure this method exists
        user = self.user_repository.create_user(data)
        return UserOutput.model_validate(user)  # Ensure correct return type

    # Services to authenticate a user
    def authenticate_user(self, username: str, password: str) -> Optional[UserModel]:
        user = self.user_repository.get_user_by_username(username)
        if not user or not Hash.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def get_current_user(db: Session = Depends(get_db), token: str = Security(api_header)) -> UserModel:
        payload = verify_token(token)
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user_repo = UserRepository(db)
        user = user_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
