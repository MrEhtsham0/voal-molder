import os
import uuid
from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydub import AudioSegment
from TTS.api import TTS
from config.database import get_db
from services.user_services import UserService
from models.user_model import UserModel
from services.voice_services import VoiceService

# model_name = "tts_models/en/ljspeech/tacotron2-DDC"
# model_name = "tts_models/en/ljspeech/glow-tts"
model_name = "tts_models/en/ljspeech/tacotron2-DDC_ph"
try:
    tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
except KeyError:
    raise ValueError(f"Model '{model_name}' not found.")

router = APIRouter(
    prefix='/tts',
    tags=['TTS']
)

# Ensure the outputs directory exists
output_dir = "outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

@router.post("")
async def generate_tts(
    text: str = Form(...),
    speed: float = Form(1.0),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(UserService.get_current_user)
):
    # Unique file name
    filename = os.path.join(output_dir, f"{uuid.uuid4()}.wav")
    try:
        # Generate the speech and save to file
        tts.tts_to_file(text=text, file_path=filename, speaker_wav=os.path.join(output_dir, 'arabic-male-voice.wav'))
       
        # Adjust the speed of the audio file
        if speed != 1.0:
            sound = AudioSegment.from_wav(filename)
            sound = sound.speedup(playback_speed=speed)
            sound.export(filename, format="wav")

        # Increment the voice generation count
        voice_service = VoiceService(db)
        voice_service.increment_voice_count(user_id=current_user.id)
        
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error generating TTS file: {str(e)}")
    
    # Check if the file was created
    if not os.path.exists(filename):
        raise HTTPException(status_code=500, detail="TTS file was not created.")

    # Return the audio file
    return FileResponse(filename, media_type='audio/wav', filename=os.path.basename(filename))
