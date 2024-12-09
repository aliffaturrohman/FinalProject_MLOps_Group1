import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from backend.ml_model_v2.models_v2 import load_resources, predict_category

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    # Menerima data inputan dalam format JSON
    data = request.get_json()

    # Mengambil title dan description dari request body
    title = data.get('title')
    description = data.get('description')

    # Memastikan input ada
    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    # Memuat sumber daya (tokenizer, model, label encoder)
    embedding_model = load_resources()  # Anda menggunakan model embedding di sini

    # Prediksi kategori berdasarkan judul dan deskripsi
    predicted_category, predicted_probability = predict_category(title, description, embedding_model)

    # Mengembalikan hasil prediksi dalam format JSON
    return jsonify({
        'predicted_category': predicted_category,
        'probability': predicted_probability.tolist()  # Mengubah numpy array ke list
    })

if __name__ == "__main__":
    # Port diatur berdasarkan variabel lingkungan 'PORT' untuk kompatibilitas dengan Azure
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
