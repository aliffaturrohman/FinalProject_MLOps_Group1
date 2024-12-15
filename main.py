# Import fungsi prediksi dari file predict.py
import os
# Matikan log verbose TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf

# Matikan logger TensorFlow
tf.get_logger().setLevel('ERROR')
from src.models.predict import predict
import tensorflow_hub as hub
import numpy as np

# Input teks dari pengguna
user_text = "Pelaksana Harian Direktur Jenderal Politik dan Pemerintahan Umum (Plh. Dirjen Polpum) Kementerian Dalam Negeri (Kemendagri) Syarmadani menjelaskan bahwa sebanyak 19 aparatur sipil negara (ASN) pelanggar netralitas Pilkada 2024 telah diberikan hukuman."

# Memuat Universal Sentence Encoder (USE) dari TensorFlow Hub
embedding_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Prediksi kategori dan probabilitas dari teks input
predicted_category, predicted_probability = predict(user_text, embedding_model)

# Menampilkan hasil prediksi
print(f"Predicted Category: {predicted_category}")

# Ambil probabilitas untuk kategori yang diprediksi
predicted_prob = predicted_probability[np.argmax(predicted_probability)]  # Ambil probabilitas untuk kategori terpilih
print(f"Probability: {predicted_prob:.2f}")