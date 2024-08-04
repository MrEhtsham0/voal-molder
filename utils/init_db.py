from config.database import Base, engine
from models.user_model import UserModel


def create_tables():
    UserModel.metadata.create_all(bind=engine)
