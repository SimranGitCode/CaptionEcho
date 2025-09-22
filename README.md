# CaptionEcho

**CaptionEcho** is a web application that generates captions for images, translates them into multiple languages, and converts them into audio, making visual content more interactive and accessible.

---

## Key Features

- **Image Captioning** – Automatically generates descriptive captions for any image using **BLIP**.  
- **Translation** – Translate captions into multiple languages including Hindi, Tamil, and Bengali.  
- **Audio Playback** – Captions and translations can be converted to MP3 audio using **gTTS**.  
- **Multi-language Support** – Read translated captions aloud.  
- **Web Interface** – Simple and clean UI built with **Flask**, optimized for speed using **PyTorch GPU acceleration** and **Flask-Compress**.

---

## How It Works

1. Upload an image via the web interface.  
2. BLIP (Salesforce) generates a descriptive caption.  
3. Optionally translate the caption into a selected language.  
4. Convert the caption (original or translated) into audio for playback or download.  

---

## Future Improvements

- Batch image uploads for faster processing.  
- Customizable TTS voice settings (speed, pitch, accent).  
- Cloud deployment for scalable usage.  
- Enhanced UI with drag-and-drop and responsive design.  

---

## Acknowledgements

- [Salesforce BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base) for image captioning  
- Google Translate API for translation  
- gTTS for text-to-speech  
- PyTorch & Flask for model serving and web interface
