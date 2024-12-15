import pandas as pd
import numpy as np
import string
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from deep_translator import GoogleTranslator

# Inisialisasi stopwords, lemmatizer dan translator
STOPWORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
translator = GoogleTranslator()

# Fungsi untuk membersihkan URL
def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'URL', text)

# Fungsi untuk menghapus HTML tags
def remove_HTML(text):
    html = re.compile(r'<.*?>')
    return html.sub(r'', text)

# Fungsi untuk menghapus karakter non-ASCII
def remove_not_ASCII(text):
    text = ''.join([word for word in text if word in string.printable])
    return text

# Fungsi untuk mengganti singkatan dengan arti sebenarnya
def word_abbrev(word):
    abbreviations = {
        "u": "you",
        "r": "are",
        # Tambahkan singkatan lainnya sesuai kebutuhan
    }
    return abbreviations[word.lower()] if word.lower() in abbreviations else word

# Fungsi untuk mengganti semua singkatan
def replace_abbrev(text):
    return ' '.join([word_abbrev(word) for word in text.split()])

# Fungsi untuk menghapus mention (@username)
def remove_mention(text):
    at = re.compile(r'@\S+')
    return at.sub(r'USER', text)

# Fungsi untuk menghapus angka
def remove_number(text):
    num = re.compile(r'\d+')
    return num.sub(r'NUMBER', text)

# Fungsi untuk mengganti smiley menjadi SADFACE
def transcription_sad(text):
    smiley = re.compile(r'[8:=;][\'\-]?[\\/]')
    return smiley.sub(r'SADFACE', text)

# Fungsi untuk mengganti smiley menjadi SMILE
def transcription_smile(text):
    smiley = re.compile(r'[8:=;][\'\-]?[)dDp]')
    return smiley.sub(r'SMILE', text)

# Fungsi untuk mengganti <3 dengan HEART
def transcription_heart(text):
    heart = re.compile(r'<3')
    return heart.sub(r'HEART', text)

# Fungsi untuk mengurangi kata yang terlalu panjang (elongated words)
def remove_elongated_words(text):
    rep = re.compile(r'\b(\S*?)([a-z])\2{2,}\b')
    return rep.sub(r'\1\2 ELONG', text)

# Fungsi untuk mengurangi tanda baca yang berulang
def remove_repeat_punct(text):
    rep = re.compile(r'([!?.]){2,}')
    return rep.sub(r'\1 REPEAT', text)

# Fungsi untuk menghapus semua tanda baca
def remove_all_punct(text):
    table = str.maketrans('', '', string.punctuation)
    return text.translate(table)

# Fungsi untuk menghapus stopwords
def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in STOPWORDS])

# Fungsi untuk lemmatization
def lemmatization(text):
    return ' '.join([lemmatizer.lemmatize(word, pos='v') for word in text.split()])

# Fungsi untuk menerjemahkan teks ke bahasa Inggris
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Terjadi kesalahan saat menerjemahkan: {e}")
        return text

# Fungsi utama untuk membersihkan teks
def clean_text(text):
    # Remove non-text characters
    text = remove_URL(text)
    text = remove_HTML(text)
    text = remove_not_ASCII(text)

    # Lowercase text and replace abbreviations
    text = replace_abbrev(text)
    text = remove_mention(text)
    text = remove_number(text)

    # Remove smileys
    text = transcription_sad(text)
    text = transcription_smile(text)
    text = transcription_heart(text)

    # Remove elongated words and repeated punctuation
    text = remove_elongated_words(text)
    text = remove_repeat_punct(text)

    # Remove all punctuation
    text = remove_all_punct(text)
    
    # Remove stopwords and lemmatize
    text = remove_stopwords(text)
    text = lemmatization(text)

    # Final trim and lowercase
    text = text.lower().strip()
    return text

# Fungsi untuk memproses input pengguna
def preprocess_user_input(text):
    translated_text = translate_to_english(text)
    cleaned_text = clean_text(translated_text)
    return cleaned_text

# Fungsi untuk melakukan preprocessing dan embedding
def preprocess_and_embed(sentences, embed):
    embed_matrix = []
    for sent in sentences:
        embed_matrix.append(np.array(embed([sent])[0]).tolist())
    return np.array(embed_matrix)
