# Digunakan untuk mengevaluasi performa model menggunakan dataset pengujian. Hal ini hanya relevan selama tahap pengembangan atau debugging, bukan untuk produksi.

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

def evaluate_model(model, X_test, y_test):
    """
    Mengevaluasi model menggunakan data pengujian.
    :param model: Model terlatih.
    :param X_test: Data input pengujian yang sudah diproses (tokenisasi dan padding).
    :param y_test: Label one-hot encoded untuk data pengujian.
    :return: Laporan evaluasi dan confusion matrix.
    """
    # Evaluasi model
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
    print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")

    # Prediksi kelas
    y_pred_probs = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred_probs, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)

    # Laporan klasifikasi
    report = classification_report(y_true_classes, y_pred_classes, target_names=None)
    print("\nClassification Report:")
    print(report)

    # Confusion Matrix
    cm = confusion_matrix(y_true_classes, y_pred_classes)
    print("\nConfusion Matrix:")
    print(cm)

    return test_loss, test_accuracy, report, cm
