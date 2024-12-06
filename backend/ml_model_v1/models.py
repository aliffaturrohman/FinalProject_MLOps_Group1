import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
from deep_translator import GoogleTranslator

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower().strip()
    return text

def translate_text(text):
    text = GoogleTranslator(source='auto', target='en').translate(text)
    return text

def load_resources():
    with open('backend/ml_model_v1/tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    
    model = load_model('backend/ml_model_v1/model2(balancing).h5')
    
    with open('backend/ml_model_v1/label_encoder2.pkl', 'rb') as f:
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

def main(title, description):
    tokenizer, model, label_encoder = load_resources()
    predicted_category = predict_category(title, description, tokenizer, model, label_encoder)
    print("Predicted category:", predicted_category)

if __name__ == "__main__":
    title = "Wanita yang Melaporkan Pria Black Bird-Watcher ke Polisi Kalah Gugatan Terhadap Mantan Majikannya"
    description = "Amy Cooper menuduh perusahaan investasi Franklin Templeton secara tidak adil memecatnya dan menandainya sebagai seorang rasis setelah video insiden Central Park menjadi viral."
    
    main(title, description)
