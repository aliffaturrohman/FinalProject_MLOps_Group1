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

# HTML Template for the Form
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Category Predictor</title>
</head>
<body>
    <h1>News Category Predictor</h1>
    <form id="predictionForm">
        <label for="title">Title:</label><br>
        <input type="text" id="title" name="title" placeholder="Enter the news title" required><br><br>

        <label for="description">Description:</label><br>
        <textarea id="description" name="description" rows="5" cols="50" placeholder="Enter the news description" required></textarea><br><br>

        <button type="submit">Predict Category</button>
    </form>

    <h2>Predicted Category:</h2>
    <p id="result">Waiting for prediction...</p>

    <script>
        document.getElementById("predictionForm").addEventListener("submit", async function (event) {
            event.preventDefault();

            const title = document.getElementById("title").value;
            const description = document.getElementById("description").value;

            try {
                const response = await fetch("/predict", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ title, description }),
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch the API");
                }

                const data = await response.json();
                document.getElementById("result").textContent = data.predicted_category;
            } catch (error) {
                document.getElementById("result").textContent = "Error: " + error.message;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    tokenizer, model, label_encoder = load_resources()
    predicted_category = predict_category(title, description, tokenizer, model, label_encoder)
    return jsonify({'predicted_category': predicted_category})

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower().strip()
    return text

def translate_text(text):
    text = GoogleTranslator(source='auto', target='en').translate(text)
    return text

def load_resources():
    with open('models/tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    
    model = load_model('models/model2(balancing).h5')
    
    with open('models/label_encoder2.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    return tokenizer, model, label_encoder

def predict_category(title, description, tokenizer, model, label_encoder):
    text = title + description
    text = clean_text(text)
    text = translate_text(text)
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequences, maxlen=200, padding='post')
    prediction = model.predict(padded_sequence)
    predicted_class_index = np.argmax(prediction, axis=1)
    predicted_class = label_encoder.inverse_transform(predicted_class_index)
    
    return predicted_class[0]

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
