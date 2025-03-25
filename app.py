from flask import Flask, render_template, request, url_for, jsonify
import os
import torch
import asyncio
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
from datetime import datetime
from gtts import gTTS  
from pygame import mixer
from googletrans import Translator
from functools import cache
from flask_compress import Compress

app = Flask(__name__)
Compress(app)  

# Directories
UPLOAD_FOLDER = "static/uploads"
AUDIO_FOLDER = "static/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER

# Speed optimizations
torch.backends.cudnn.benchmark = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model once
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning").to(device)
model = torch.compile(model) if torch.cuda.is_available() else model
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

gen_kwargs = {"max_length": 16, "num_beams": 4}
mixer.init()

def preprocess_image(image_path):
    with Image.open(image_path).convert("RGB") as img:
        img.thumbnail((128, 128), Image.LANCZOS)
        return feature_extractor(images=img, return_tensors="pt").pixel_values.to(device)

@cache
def predict_caption(image_path):
    pixel_values = preprocess_image(image_path)
    with torch.inference_mode():
        output_ids = model.generate(pixel_values, **gen_kwargs)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

def generate_audio(caption, lang="en"):
    filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".mp3"
    audio_path = os.path.join(AUDIO_FOLDER, filename)
    tts = gTTS(text=caption, lang=lang, slow=False)
    tts.save(audio_path)
    return url_for("static", filename=f"audio/{filename}")

async def generate_audio_async(caption, lang="en"):
    return await asyncio.to_thread(generate_audio, caption, lang)

def translate_caption(text, target_lang):
    try:
        translator = Translator()
        translated_text = translator.translate(text, dest=target_lang).text
        return translated_text
    except Exception as e:
        return f"Translation Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    caption = ""
    image_url = None  
    audio_url = None  

    if request.method == "POST":
        file = request.files.get("image")

        if file and file.filename:
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(image_path)
            caption = predict_caption(image_path)
            image_url = url_for("static", filename=f"uploads/{file.filename}")
            audio_url = asyncio.run(generate_audio_async(caption))

    return render_template("index.html", caption=caption, image_url=image_url, audio_url=audio_url)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text")
    lang = data.get("lang")

    if not text or not lang:
        return jsonify({"error": "Invalid input"}), 400

    translated_text = translate_caption(text, lang)
    return jsonify({"translated_text": translated_text})

@app.route("/generate_audio", methods=["POST"])
def generate_audio_endpoint():
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
    app.run(threaded=True)
