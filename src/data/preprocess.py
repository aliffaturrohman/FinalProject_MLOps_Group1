import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from googletrans import Translator

# Stopwords dari NLTK
STOPWORDS = set(stopwords.words('english'))

# Inisialisasi lemmatizer dan translator
lemmatizer = WordNetLemmatizer()
translator = Translator()

def translate_to_english(text):
    """
    Menerjemahkan teks ke bahasa Inggris menggunakan Google Translate.
    :param text: String teks dalam bahasa apapun.
    :return: String teks yang diterjemahkan ke bahasa Inggris.
    """
    try:
        translated = translator.translate(text, dest='en')
        return translated.text
    except Exception as e:
        print(f"Terjadi kesalahan saat menerjemahkan: {e}")
        return text  # Kembalikan teks asli jika gagal diterjemahkan

def clean_text(text):
    """
    Membersihkan teks berita dengan preprocessing lengkap.
    :param text: String teks berita.
    :return: String teks yang sudah dibersihkan.
    """
    # Regex patterns
    whitespace = re.compile(r"\s+")
    user = re.compile(r"(?i)@[a-z0-9_]+")  # Remove mentions (@usernames)
    url = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")  # Remove URLs
    email = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')  # Remove emails
    repeated = re.compile(r'(.)\1{2,}')  # Replace repeated characters
    non_ascii = re.compile(r'[^\x00-\x7F]+')  # Remove non-ASCII characters

    # Substitusi dengan regex
    text = whitespace.sub(' ', text)  # Remove extra whitespaces
    text = user.sub('', text)  # Remove @user
    text = url.sub('', text)  # Remove URLs
    text = email.sub('', text)  # Remove email addresses
    text = repeated.sub(r'\1\1', text)  # Replace repeated characters (e.g., loooove -> loove)
    text = non_ascii.sub('', text)  # Remove non-ASCII characters
    text = re.sub(r"\d+", "", text)  # Remove digits
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lowercase

    # Removing stopwords
    text = [word for word in text.split() if word not in STOPWORDS]

    # Word lemmatization
    text = [lemmatizer.lemmatize(word, 'v') for word in text]

    # Gabungkan kembali teks
    text = ' '.join(text)

    # Final trim
    text = text.strip()
    return text

def preprocess_user_input(text):
    """
    Fungsi utama untuk preprocessing teks berita dari input user.
    :param text: String teks berita input dari user.
    :return: String teks yang sudah diterjemahkan dan dibersihkan.
    """
    # Terjemahkan teks ke bahasa Inggris
    translated_text = translate_to_english(text)
    # Preprocessing teks yang telah diterjemahkan
    cleaned_text = clean_text(translated_text)
    return cleaned_text