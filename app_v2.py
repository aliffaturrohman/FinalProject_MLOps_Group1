from flask import Flask, request, jsonify, render_template_string
import os
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import re
import string
import pickle
from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# Initialize Flask app
app = Flask(__name__)

# Matikan log verbose TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
tf.get_logger().setLevel('ERROR')

# Path ke model, tokenizer, dan label encoder
MODEL_PATH = r"notebook/keras(ANN).h5"
LABEL_ENCODER_PATH = r"notebook/label_encoder.pkl"

# Inisialisasi Universal Sentence Encoder
embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Memuat model yang sudah dilatih
model = load_model(MODEL_PATH)

# Memuat label encoder
with open(LABEL_ENCODER_PATH, 'rb') as file:
    label_encoder = pickle.load(file)

# Stopwords dan lemmatizer
STOPWORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Fungsi preprocessing teks
def clean_text(text):
    def remove_URL(text):
        url = re.compile(r'https?://\S+|www\.\S+')
        return url.sub(r'URL', text)

    def remove_HTML(text):
        html = re.compile(r'<.*?>')
        return html.sub(r'', text)

    def remove_not_ASCII(text):
        return ''.join([word for word in text if word in string.printable])

    def remove_mention(text):
        at = re.compile(r'@\S+')
        return at.sub(r'USER', text)

    def remove_number(text):
        num = re.compile(r'\d+')
        return num.sub(r'NUMBER', text)

    def remove_all_punct(text):
        table = str.maketrans('', '', string.punctuation)
        return text.translate(table)

    def remove_stopwords(text):
        return ' '.join([word for word in text.split() if word not in STOPWORDS])

    def lemmatization(text):
        return ' '.join([lemmatizer.lemmatize(word, pos='v') for word in text.split()])

    text = remove_URL(text)
    text = remove_HTML(text)
    text = remove_not_ASCII(text)
    text = remove_mention(text)
    text = remove_number(text)
    text = remove_all_punct(text)
    text = remove_stopwords(text)
    text = lemmatization(text)
    return text.lower().strip()

# Fungsi untuk menerjemahkan teks ke bahasa Inggris
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Terjadi kesalahan saat menerjemahkan: {e}")
        return text

# Fungsi untuk preprocessing dan embedding
def preprocess_and_embed(sentences, embed):
    embed_matrix = [np.array(embed([sent])[0]).tolist() for sent in sentences]
    return np.array(embed_matrix)

# Fungsi untuk melakukan prediksi
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")

    # Preprocessing teks
    translated_text = translate_to_english(text)
    cleaned_text = clean_text(translated_text)
    embedded_text = preprocess_and_embed([cleaned_text], embedding_model)

    # Prediksi
    prediction = model.predict(embedded_text)
    probabilities = prediction[0]
    predicted_label = label_encoder.inverse_transform([np.argmax(probabilities)])[0]

    return jsonify({
        "predicted_category": predicted_label,
        "probability": float(probabilities[np.argmax(probabilities)])
    })

# Route utama untuk tes
@app.route("/")
def index():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Text Prediction App</title>
    </head>
    <body>
        <h1>Welcome to Text Prediction App</h1>
        <p>Use the /predict endpoint to predict text categories.</p>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
