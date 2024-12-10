import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from deep_translator import GoogleTranslator
import tensorflow_hub as hub

STOPWORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Fungsi preprocessing teks
def remove_URL(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)

def remove_HTML(text):
    return re.sub(r'<.*?>', '', text)

def remove_not_ASCII(text):
    return ''.join([char for char in text if char.isascii()])

def replace_abbrev(text):
    abbreviations = {"u": "you", "r": "are", "pls": "please", "msg": "message"}
    return ' '.join([abbreviations.get(word, word) for word in text.split()])

def remove_mention(text):
    return re.sub(r'@\w+', '', text)

def remove_all_punct(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_stopwords(text):
    return ' '.join(word for word in text.split() if word.lower() not in STOPWORDS)

def lemmatization(text):
    return ' '.join(lemmatizer.lemmatize(word) for word in text.split())

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def clean_text(text):
    text = text.lower()
    text = remove_URL(text)
    text = remove_HTML(text)
    text = remove_not_ASCII(text)
    text = replace_abbrev(text)
    text = remove_mention(text)
    text = remove_all_punct(text)
    text = remove_stopwords(text)
    return lemmatization(text)

def preprocess_user_input(text):
    translated_text = translate_to_english(text)
    return clean_text(translated_text)

def load_resources():
    return hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
