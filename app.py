from flask import Flask, render_template, request, url_for, jsonify
import os, torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from datetime import datetime
from gtts import gTTS
from pygame import mixer
from flask_compress import Compress
 
from translate import translate_caption

app = Flask(__name__)
Compress(app)
 
UPLOAD_FOLDER = "static/uploads"
AUDIO_FOLDER = "static/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER
 
torch.backends.cudnn.benchmark = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
 
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)

mixer.init()
 
def predict_caption(image_path):
    raw_image = Image.open(image_path).convert("RGB")
    inputs = processor(raw_image, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model.generate(**inputs, max_length=20)
    return processor.decode(out[0], skip_special_tokens=True)
 
def generate_audio(caption, lang="en"):
    filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".mp3"
    path = os.path.join(AUDIO_FOLDER, filename)
    tts = gTTS(text=caption, lang=lang, slow=False)
    tts.save(path)
    return url_for("static", filename=f"audio/{filename}")
 
@app.route("/", methods=["GET", "POST"])
def index():
    caption, image_url, audio_url = "", None, None
    if request.method == "POST":
        file = request.files.get("image")
        if file and file.filename:
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(image_path)
            caption = predict_caption(image_path)
            image_url = url_for("static", filename=f"uploads/{file.filename}")
            audio_url = generate_audio(caption)
    return render_template(
        "index.html",
        caption=caption,
        image_url=image_url,
        audio_url=audio_url
    )

@app.route("/translate", methods=["POST"])
def translate():
    """Translate caption into selected language."""
    data = request.get_json()
    text = data.get("text")
    lang = data.get("lang")
    if not text or not lang:
        return jsonify({"error": "Invalid input"}), 400
    translated = translate_caption(text, lang)
    return jsonify({"translated_text": translated})

@app.route("/generate_audio", methods=["POST"])
def generate_audio_endpoint():
    """Generate audio for translated captions."""
    data = request.get_json()
    text = data.get("text")
    lang = data.get("lang", "en")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    try:
        audio_url = generate_audio(text, lang)
        return jsonify({"audio_url": audio_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
