from flask import Flask, request, jsonify
import os
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import re
import string
import pickle
import pandas as pd
from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from flask_cors import CORS
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Matikan log verbose TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
tf.get_logger().setLevel('ERROR')

# Path ke model, tokenizer, dan label encoder
MODEL_PATH = r"models/keras(ANN).h5"
LABEL_ENCODER_PATH = r"models/label_encoder.pkl"

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

    def remove_non_alpha(text):
        return ''.join([char.lower() for char in text if char in string.ascii_lowercase + " "])

    text = remove_URL(text)
    text = remove_HTML(text)
    text = remove_non_alpha(text)
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in STOPWORDS])

    return text

@app.route("/predict", methods=["POST"])
def predict_text():
    # Ambil data dari form
    title = request.form.get("title")
    description = request.form.get("description")

    # Validasi input
    if not title or not description:
        return jsonify({"error": "Both title and description are required."}), 400

    # Gabungkan teks untuk memprosesnya
    full_text = f"{title} {description}"
    cleaned_text = clean_text(full_text)
    embeddings = embedding_model([cleaned_text]).numpy()

    # Prediksi dengan model
    predictions = model.predict(embeddings)
    predicted_class = label_encoder.inverse_transform([np.argmax(predictions)])

    return jsonify({"predicted_category": predicted_class[0]})

@app.route("/predict_file", methods=["POST"])
def predict_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided."}), 400

    try:
        df = pd.read_csv(file)
        predictions = []

        # Iterasi setiap baris dalam file CSV
        for _, row in df.iterrows():
            text = f"{row['title']} {row['description']}"
            cleaned_text = clean_text(text)
            embeddings = embedding_model([cleaned_text]).numpy()

            # Melakukan prediksi
            prediction = model.predict(embeddings)
            predicted_class_index = np.argmax(prediction)  # Index kelas dengan probabilitas tertinggi
            predicted_class = label_encoder.inverse_transform([predicted_class_index])[0]
            probability = np.max(prediction)  # Probabilitas kelas dengan nilai tertinggi

            # Menambahkan hasil ke list
            predictions.append({
                "title": row['title'],
                "description": row['description'],
                "predicted_category": predicted_class,
                "probability": float(probability)  # Mengkonversi ke float agar bisa diserialisasi JSON
            })

        return jsonify({"predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)