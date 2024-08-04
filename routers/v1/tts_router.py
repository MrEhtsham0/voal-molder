import os
import uuid
from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from TTS.api import TTS
from config.database import get_db
from services.user_services import UserService
from models.user_model import UserModel
from services.voice_services import VoiceService
from utils.logger import logging
# from pydub import AudioSegment

# Initialize the TTS model for multilingual support
model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model_name=model_name, progress_bar=False, gpu=False)

router = APIRouter(
    prefix='/tts',
    tags=['TTS']
)

# Ensure the outputs directory exists
output_dir = "outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

speaker_wav=os.path.join(output_dir,"4.wav")

@router.post("/")
async def generate_tts(
    text: str = Form(...),
    language: str = Form('en'),
    speed: float = Form(1.0),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(UserService.get_current_user)
):
    # Unique file name
    filename = os.path.join(output_dir, f"{uuid.uuid4()}_{language}.wav")
    try:
        # Generate the speech and save to file
        logging.info(f"Generating TTS for text: '{text}' in language: '{language}' with speed: {speed}")
        tts.tts_to_file(text=text,
                         file_path=filename,
                           language=language,
                           speaker_wav=speaker_wav,
                           speed=speed)
        logging.info(f"Saved TTS file: {filename}")
        # Adjust the speed of the audio file
        # if speed != 1.0:
        #     sound = AudioSegment.from_wav(filename)
        #     sound = sound.speedup(playback_speed=speed)
        #     sound.export(filename, format="wav")
        #     logging.info(f"Adjusted speed for file: {filename} to {speed}x")


        # Increment the voice generation count
        voice_service = VoiceService(db)
        voice_service.increment_voice_count(user_id=current_user.id)
        logging.info(f"Voice generation count incremented for user_id: {current_user.id}")

    except Exception as e:
        logging.error(f"Error generating TTS file for language '{language}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating TTS file: {str(e)}")

    # Check if the file was created
    if not os.path.exists(filename):
        raise HTTPException(status_code=500, detail="TTS file was not created.")

    # Return the audio file
    return FileResponse(filename, media_type='audio/wav', filename=os.path.basename(filename))
