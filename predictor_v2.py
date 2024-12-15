import numpy as np
from keras.models import load_model
import pickle
from utils_v2 import preprocess_user_input

MODEL_PATH = "models/keras(ANN).h5"
LABEL_ENCODER_PATH = "models/label_encoder.pkl"

# Load model dan label encoder
model = load_model(MODEL_PATH)
with open(LABEL_ENCODER_PATH, 'rb') as file:
    label_encoder = pickle.load(file)

def predict_category(title, description, embedding_model):
    # Gabungkan title dan description
    text = title + " " + description
    
    # Preprocess input
    cleaned_text = preprocess_user_input(text)
    
    # Embedding
    embedding = np.array(embedding_model([cleaned_text])[0]).reshape(1, -1)
    
    # Prediksi
    predictions = model.predict(embedding)
    predicted_label = label_encoder.inverse_transform([np.argmax(predictions)])[0]
    return predicted_label, predictions[0]
