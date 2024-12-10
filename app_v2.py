import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
from utils_v2 import preprocess_user_input, load_resources
from predictor_v2 import predict_category

# Inisialisasi aplikasi Flask
app = Flask(__name__)
CORS(app)

# Load resources saat aplikasi dimulai
embedding_model = load_resources()

@app.route('/predict', methods=['POST'])
def predict():
    # Ambil data input dalam format JSON
    data = request.get_json()

    # Validasi input
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    # Prediksi kategori
    try:
        predicted_category, predicted_probability = predict_category(title, description, embedding_model)
        return jsonify({
            'predicted_category': predicted_category,
            'probability': predicted_probability.tolist()
        })
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)
