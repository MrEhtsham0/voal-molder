from sqlalchemy.orm import Session
from repository.user_repository import UserRepository

class VoiceService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def increment_voice_count(self, user_id: int):
        self.user_repository.increment_voice_count(user_id)
