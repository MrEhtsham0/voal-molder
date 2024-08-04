from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schema import UserInput, UserOutput
from services.user_services import UserService
from config.database import get_db
from typing import List
from utils.logger import logging  # Import the custom logger

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/", response_model=UserOutput)
def create_user(user: UserInput, db: Session = Depends(get_db)):
    services = UserService(db)
    # Log the user creation request
    logging.info(f"Received request to create user: {user}")
    try:
        # Create the user
        created_user = services.create(user)
        # Log the successful user creation
        logging.info(f"User created successfully: {created_user}")
        return created_user
    except Exception as e:
        # Log the error
        logging.error(f"Error creating user: {str(e)}")
        
        # Raise HTTPException with 500 status code
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
