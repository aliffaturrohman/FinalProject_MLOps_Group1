from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Category Predictor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <div class="text-center mb-4">
                    <h1 class="display-4 fw-bold">Optimize News Data</h1>
                    <p class="lead">Get Accurate News Predictions Category in Seconds</p>
                </div>
                <div class="card shadow">
                    <div class="card-body">
                        <form id="predictionForm">
                            <!-- Input Title -->
                            <div class="mb-3">
                                <label for="title" class="form-label">Title</label>
                                <input type="text" class="form-control" id="title" placeholder="Enter news title here..." required>
                            </div>

                            <!-- Input Description -->
                            <div class="mb-3">
                                <label for="description" class="form-label">Description</label>
                                <textarea class="form-control" id="description" rows="3" placeholder="Enter news description here..." required></textarea>
                            </div>

                            <!-- Submit Button -->
                            <button type="submit" class="btn btn-primary w-100">Predict Category</button>
                        </form>

                        <!-- Loading Spinner -->
                        <div id="loadingSpinner" class="mt-3 text-center d-none">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <p class="mt-2">Loading...</p>
                        </div>

                        <!-- Result Section -->
                        <div id="resultSection" class="mt-4 d-none">
                            <p class="text-center fw-bold">Your news prediction is:</p>
                            <div class="alert alert-info text-center" id="predictedCategory"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('predictionForm').addEventListener('submit', async function (e) {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const description = document.getElementById('description').value;

            const loadingSpinner = document.getElementById('loadingSpinner');
            const resultSection = document.getElementById('resultSection');
            const predictedCategory = document.getElementById('predictedCategory');

            loadingSpinner.classList.remove('d-none');
            resultSection.classList.add('d-none');

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ title, description }),
                });

                if (response.ok) {
                    const data = await response.json();
                    predictedCategory.textContent = data.predicted_category;
                    resultSection.classList.remove('d-none');
                } else {
                    predictedCategory.textContent = 'Failed to fetch prediction';
                    resultSection.classList.remove('d-none');
                }
            } catch (error) {
                predictedCategory.textContent = 'Error occurred while fetching prediction';
                resultSection.classList.remove('d-none');
            } finally {
                loadingSpinner.classList.add('d-none');
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(html_template)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    tokenizer, model, label_encoder = load_resources()
    predicted_category = predict_category(
        title, description, tokenizer, model, label_encoder
    )
    return jsonify({"predicted_category": predicted_category})


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
