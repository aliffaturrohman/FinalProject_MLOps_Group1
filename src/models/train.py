# File digunakan untuk melatih ulang model dengan data baru, file ini dapat digunakan di lingkungan pengembangan, tetapi tidak di produksi.

import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

def train_model(data, labels, tokenizer_path, model_save_path, total_words=50000, max_length=100, num_classes=None):
    """
    Melatih model menggunakan dataset yang diberikan.
    :param data: List teks berita.
    :param labels: List kategori berita.
    :param tokenizer_path: Path untuk menyimpan tokenizer.
    :param model_save_path: Path untuk menyimpan model terlatih.
    :param total_words: Jumlah kata maksimum untuk tokenisasi.
    :param max_length: Panjang maksimum sequence untuk padding.
    :param num_classes: Jumlah kelas target.
    :return: Model terlatih.
    """
    # Tokenisasi data
    tokenizer = Tokenizer(num_words=total_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(data)
    sequences = tokenizer.texts_to_sequences(data)
    padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

    # Encode label
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    num_classes = num_classes or len(set(labels))
    onehot_labels = to_categorical(encoded_labels, num_classes=num_classes)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(padded_sequences, onehot_labels, test_size=0.2, random_state=42)

    # Simpan tokenizer
    with open(tokenizer_path, "w") as f:
        json.dump(tokenizer.to_json(), f)

    # Definisikan model
    model = Sequential([
        Embedding(input_dim=total_words, output_dim=128, input_length=max_length),
        Bidirectional(LSTM(128, return_sequences=True)),
        Dropout(0.3),
        Bidirectional(LSTM(64)),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])

    # Compile model
    optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    # Early stopping callback
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    # Training model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=20,
        batch_size=64,
        callbacks=[early_stop]
    )

    # Evaluasi model
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
    print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")

    # Simpan model
    model.save(model_save_path)

    return model, history
