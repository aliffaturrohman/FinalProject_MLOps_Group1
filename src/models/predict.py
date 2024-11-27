import numpy as np
import json
import pickle
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from data.preprocess import preprocess_user_input

# Path ke model, tokenizer, dan label encoder
MODEL_PATH = r"E:\Pembelajaran\Semester 5\PSO\FP\FinalProject_MLOps_Group1\notebook\model2(balancing).h5"
TOKENIZER_PATH = r"E:\Pembelajaran\Semester 5\PSO\FP\FinalProject_MLOps_Group1\notebook\tokenizer.json"
LABEL_ENCODER_PATH = r"E:\Pembelajaran\Semester 5\PSO\FP\FinalProject_MLOps_Group1\notebook\label_encoder2.pkl"


# Muat model
model = load_model(MODEL_PATH)

# Muat tokenizer dari file JSON
with open(TOKENIZER_PATH, "r") as f:
    tokenizer_data = json.load(f)
tokenizer = tokenizer_from_json(tokenizer_data)

# Muat label encoder
with open(LABEL_ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

def predict_category(user_text, max_length=130):
    """
    Melakukan prediksi kategori berita berdasarkan teks input pengguna.
    :param user_text: String input teks berita.
    :param max_length: Panjang maksimum sequence untuk padding.
    :return: Tuple (kategori prediksi, probabilitas kategori).
    """
    # Preprocessing teks input
    cleaned_text = preprocess_user_input(user_text)

    # Tokenisasi dan padding
    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded_sequence = pad_sequences(sequence, maxlen=max_length, padding='post', truncating='post')

    # Prediksi kategori
    prediction_probs = model.predict(padded_sequence)
    predicted_class_index = np.argmax(prediction_probs, axis=-1)[0]  # Indeks kategori
    predicted_category = label_encoder.inverse_transform([predicted_class_index])[0]  # Label kategori

    # Probabilitas kategori
    predicted_probability = prediction_probs[0][predicted_class_index]

    return predicted_category, predicted_probability
