import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
import pickle
from src.data.preprocess import preprocess_user_input, preprocess_and_embed


# Path ke model, tokenizer, dan label encoder
MODEL_PATH = r"E:\Pembelajaran\Semester 5\PSO\FP\FinalProject_MLOps_Group1\notebook\keras(ANN).h5"
LABEL_ENCODER_PATH = r"E:\Pembelajaran\Semester 5\PSO\FP\FinalProject_MLOps_Group1\notebook\label_encoder.pkl"

# Memuat model yang sudah dilatih
model = load_model(MODEL_PATH)

# Memuat label encoder (pastikan Anda menyimpan label encoder setelah pelatihan)
with open(LABEL_ENCODER_PATH, 'rb') as file:
    label_encoder = pickle.load(file)

# Fungsi untuk melakukan prediksi pada input teks
def predict(text, embed_model):
    # Preprocess input teks menggunakan fungsi dari preprocess.py
    cleaned_text = preprocess_user_input(text)
    
    # Proses embedding teks yang telah dibersihkan
    embedded_text = preprocess_and_embed([cleaned_text], embed_model)
    
    # Membuat prediksi dengan model
    prediction = model.predict(embedded_text)
    
    # Menghitung probabilitas untuk setiap kategori
    probabilities = prediction[0]
    
    # Mendapatkan label kategori yang diprediksi
    predicted_label = label_encoder.inverse_transform([np.argmax(probabilities)])[0]
    
    return predicted_label, probabilities
