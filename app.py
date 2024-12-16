from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
from deep_translator import GoogleTranslator
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "test fetch api"


@app.route("/predict", methods=["POST"])
def predict():
    title = request.form.get("title")
    description = request.form.get("description")
    tokenizer, model, label_encoder = load_resources()
    predicted_category = predict_category(
        title, description, tokenizer, model, label_encoder
    )
    return jsonify({"predicted_category": predicted_category})


@app.route("/predict_file", methods=["POST"])
def predict_file():
    # Mendapatkan file yang diunggah
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided."}), 400

    try:
        # Membaca file CSV
        df = pd.read_csv(file)
        predictions = []

        # Memuat model, tokenizer, dan label encoder
        tokenizer, model, label_encoder = load_resources()

        # Iterasi setiap baris dalam file CSV
        for _, row in df.iterrows():
            text = f"{row['title']} {row['description']}"
            cleaned_text = process_text(text)

            # Menyiapkan data untuk prediksi
            sequences = tokenizer.texts_to_sequences([cleaned_text])
            padded_sequence = pad_sequences(sequences, maxlen=200, padding="post")

            # Melakukan prediksi
            prediction = model.predict(padded_sequence)
            predicted_class_index = np.argmax(
                prediction
            )  # Index kelas dengan probabilitas tertinggi
            predicted_class = label_encoder.inverse_transform([predicted_class_index])[
                0
            ]
            probability = np.max(
                prediction
            )  # Probabilitas kelas dengan nilai tertinggi

            # Menambahkan hasil ke list
            predictions.append(
                {
                    "title": row["title"],
                    "description": row["description"],
                    "predicted_category": predicted_class,
                    "probability": float(
                        probability
                    ),  # Mengkonversi ke float agar bisa diserialisasi JSON
                }
            )

        return jsonify({"predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def process_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = text.lower().strip()
    text = GoogleTranslator(source="auto", target="en").translate(text)
    return text


def load_resources():
    with open("models/tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)

    model = load_model("models/model2(balancing).h5")

    with open("models/label_encoder2.pkl", "rb") as f:
        label_encoder = pickle.load(f)

    return tokenizer, model, label_encoder


def predict_category(title, description, tokenizer, model, label_encoder):
    text = title + description
    text = process_text(text)
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequences, maxlen=200, padding="post")
    prediction = model.predict(padded_sequence)
    predicted_class_index = np.argmax(prediction, axis=1)
    predicted_class = label_encoder.inverse_transform(predicted_class_index)

    return predicted_class[0]


if __name__ == "__main__":
    import logging

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Starting app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
