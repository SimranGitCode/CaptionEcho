 
from datetime import datetime
from gtts import gTTS
import os

language = 'en'

def save_audio(caption, lang='en'): 
    os.makedirs("static/audio", exist_ok=True)
    filename = datetime.now().strftime("%Y%m%d-%H%M%S_%f") + ".mp3"
    audio_path = os.path.join("static", "audio", filename)
    tts = gTTS(text=caption, lang=lang, slow=False)
    tts.save(audio_path) 
    return audio_path
