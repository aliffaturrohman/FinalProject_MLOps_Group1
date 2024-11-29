from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from models import load_resources, predict_category  # Mengimpor fungsi dari models.py

app = Flask(__name__)

CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    tokenizer, model, label_encoder = load_resources()
    predicted_category = predict_category(title, description, tokenizer, model, label_encoder)
    return jsonify({'predicted_category': predicted_category})

if __name__ == '__main__':
    app.run(debug=True)
