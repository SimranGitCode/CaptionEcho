# 📸 Caption Echo

**Caption Echo** is an image caption generator that takes an image and generates a human-like sentence describing it. It combines deep learning models from computer vision and natural language processing to understand and narrate visual content.

This project is ideal for exploring how machines can learn to "see" and "speak" using AI.

---

## 🔍 Features

- 🖼 Upload any image and get a descriptive caption.
- 🧠 Uses CNN for image feature extraction.
- ✍️ LSTM or Transformer model for generating captions.
- 🔊 Optional text-to-speech (TTS) feature to read captions aloud.
- 🌐 Simple and clean web interface built with Flask.

---

## 🧠 How It Works

1. The image is uploaded via the web interface.
2. A pre-trained CNN (e.g., InceptionV3 or VGG16) extracts features from the image.
3. These features are passed into a language model to generate a caption.
4. The caption is shown to the user, and optionally spoken aloud using TTS.

---

## 🧪 Example

**Input Image:**  
📷 `dog-running.jpg`

**Generated Caption:**  
*“A brown dog is running through the field.”*

**With Speech:**  
🗣️ *The system can speak this caption out loud using text-to-speech.*

---

## 💡 Future Improvements

- Support for multiple language captions
- Enhanced UI with drag-and-drop image upload
- Audio download feature
- Deploy to the web with Gradio or Streamlit

---

## 🙋 About Me

Hi, I'm **Simran**, a Computer Engineering student passionate about artificial intelligence and real-world applications of deep learning. This project helped me understand how to bridge visual recognition and language generation.

## 🙌 Acknowledgements

- [Flickr8k Dataset](https://www.kaggle.com/datasets/adityajn105/flickr8k)
- TensorFlow & Keras
- Hugging Face Transformers
- OpenAI for guidance and inspiration
