from sqlalchemy.orm import Session
from models.user_model import UserModel
from schemas.user_schema import UserInput, UserOutput
from typing import List, Optional


class UserRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_user(self, data: UserInput) -> UserOutput:
        new_user = UserModel(**data.model_dump())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return UserOutput.model_validate(new_user)
    def increment_voice_count(self, user_id: int):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user:
            user.generated_voices += 1
            self.db.commit()
            self.db.refresh(user)
            return user

    def user_exist_by_email(self, email: str) -> bool:
        return self.db.query(UserModel).filter(UserModel.email == email).first() is not None
    
    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter_by(username=username).first()