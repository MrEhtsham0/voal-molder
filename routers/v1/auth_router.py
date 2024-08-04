from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.user_schema import TokenSchema, AuthOutput
from services.user_services import UserService
from utils.jwt_handler import create_access_token
from config.database import get_db
from utils.logger import logging  # Import the custom logger

router = APIRouter(
    tags=['Profile']
)

@router.post("/token", response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logging.info(f"Login attempt for user: {form_data.username}")
    
    user_service = UserService(db)
    user_auth = user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user_auth:
        logging.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user_auth.username})
    logging.info(f"User logged in successfully: {form_data.username}")
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=AuthOutput)
def get_current_user(current_user=Depends(UserService.get_current_user)):
    logging.info(f"Fetching current user: {current_user.username}")
    return current_user
