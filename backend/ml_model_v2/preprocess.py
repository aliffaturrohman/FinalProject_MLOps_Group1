import numpy as np
import string
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from deep_translator import GoogleTranslator

# Inisialisasi stopwords dan lemmatizer
STOPWORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Fungsi untuk membersihkan URL
def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'', text)

# Fungsi untuk menghapus HTML tags
def remove_HTML(text):
    html = re.compile(r'<.*?>')
    return html.sub(r'', text)

# Fungsi untuk menghapus karakter non-ASCII
def remove_not_ASCII(text):
    return ''.join([word for word in text if word.isascii()])

# Fungsi untuk mengganti singkatan dengan arti sebenarnya
def word_abbrev(word):
    abbreviations = {
        "u": "you",
        "r": "are",
        "pls": "please",
        "msg": "message",
        # Tambahkan lebih banyak singkatan jika diperlukan
    }
    return abbreviations.get(word.lower(), word)

# Fungsi untuk mengganti semua singkatan
def replace_abbrev(text):
    return ' '.join([word_abbrev(word) for word in text.split()])

# Fungsi untuk menghapus mention (@username)
def remove_mention(text):
    at = re.compile(r'@\w+')
    return at.sub(r'', text)

# Fungsi untuk menghapus angka
def remove_number(text):
    num = re.compile(r'\b\d+\b')
    return num.sub(r'', text)

# Fungsi untuk mengganti smiley menjadi kata deskriptif
def transcription_emoticons(text):
    smiley = re.compile(r'[:;=8][\-~]?[)dDpP]')
    sadface = re.compile(r'[:;=8][\-~]?[(\\/]')
    heart = re.compile(r'<3')
    text = smiley.sub(' SMILE ', text)
    text = sadface.sub(' SADFACE ', text)
    text = heart.sub(' HEART ', text)
    return text

# Fungsi untuk mengurangi kata yang terlalu panjang (elongated words)
def remove_elongated_words(text):
    rep = re.compile(r'\b(\w*?)(\w)\2{2,}\b')
    return rep.sub(r'\1\2', text)

# Fungsi untuk menghapus semua tanda baca
def remove_all_punct(text):
    return re.sub(f"[{re.escape(string.punctuation)}]", '', text)

# Fungsi untuk menghapus stopwords
def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word.lower() not in STOPWORDS])

# Fungsi untuk lemmatization
def lemmatization(text):
    return ' '.join([lemmatizer.lemmatize(word, pos='v') for word in text.split()])

# Fungsi untuk menerjemahkan teks ke bahasa Inggris menggunakan deep-translator
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Terjadi kesalahan saat menerjemahkan: {e}")
        return text

# Fungsi utama untuk membersihkan teks
def clean_text(text):
    text = text.lower().strip()
    text = remove_URL(text)
    text = remove_HTML(text)
    text = remove_not_ASCII(text)
    text = transcription_emoticons(text)
    text = replace_abbrev(text)
    text = remove_mention(text)
    text = remove_number(text)
    text = remove_elongated_words(text)
    text = remove_all_punct(text)
    text = remove_stopwords(text)
    text = lemmatization(text)
    return re.sub(r'\s+', ' ', text).strip()  # Menghapus whitespace berlebih

# Fungsi untuk memproses input pengguna
def preprocess_user_input(text):
    translated_text = translate_to_english(text)
    cleaned_text = clean_text(translated_text)
    return cleaned_text

def preprocess_and_embed(sentences, embed):
    embed_matrix = []
    for sent in sentences:
        embed_matrix.append(np.array(embed([sent])[0]).tolist())
    return np.array(embed_matrix)

