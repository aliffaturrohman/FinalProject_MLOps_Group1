from predict import predict
import tensorflow_hub as hub
import numpy as np

# Fungsi untuk memuat sumber daya yang diperlukan
def load_resources():
    # Memuat tokenizer, model, dan label encoder
    # (Misalkan tokenizer dan model sudah ada, Anda dapat mengganti ini dengan kode yang relevan)
    embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    # Misalnya, menggunakan model prediksi atau label encoder dari file yang sudah ada
    return embedding_model

# Fungsi untuk memprediksi kategori
def predict_category(title, description, embedding_model):
    # Gabungkan title dan description
    text = title + " " + description
    
    # Menghitung embedding dari teks
    embedding = embedding_model([text]).numpy()
    
    # Prediksi kategori dan probabilitas
    predicted_category, predicted_probability = predict(text, embedding_model)
    
    return predicted_category, predicted_probability

# Fungsi utama
def main(title, description):
    # Memuat sumber daya
    embedding_model = load_resources()
    
    # Prediksi kategori berdasarkan title dan description
    predicted_category, predicted_probability = predict_category(title, description, embedding_model)
    
    # Menampilkan hasil prediksi
    print(f"Predicted Category: {predicted_category}")
    
    # Ambil probabilitas untuk kategori yang diprediksi
    predicted_prob = predicted_probability[np.argmax(predicted_probability)]
    print(f"Probability: {predicted_prob:.2f}")
