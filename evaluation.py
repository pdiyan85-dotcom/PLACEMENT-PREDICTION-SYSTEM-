import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)


# ==========================================
# 1. LOAD DATA
# ==========================================

X_train, X_test, y_train, y_test = joblib.load(
    "MODELS/train_test_data.pkl"
)

preprocessor = joblib.load(
    "MODELS/preprocessor.pkl"
)

model = joblib.load(
    "MODELS/placement_model.pkl"
)

print("Data and model loaded successfully!")


# ==========================================
# 2. PREPROCESS TEST DATA
# ==========================================

X_test_processed = preprocessor.transform(X_test)

print("Test data processed successfully!")


# ==========================================
# 3. MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(X_test_processed)

y_probability = model.predict_proba(
    X_test_processed
)[:, 1]


# ==========================================
# 4. CALCULATE METRICS
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n========================================")
print("MODEL EVALUATION")
print("========================================")

print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))
print("ROC-AUC  :", round(roc_auc, 4))


# ==========================================
# 5. CLASSIFICATION REPORT
# ==========================================

print("\n========================================")
print("CLASSIFICATION REPORT")
print("========================================")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Not Placed",
            "Placed"
        ]
    )
)


# ==========================================
# 6. CONFUSION MATRIX
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\n========================================")
print("CONFUSION MATRIX")
print("========================================")

print(cm)


ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[
        "Not Placed",
        "Placed"
    ]
).plot()

plt.title("Placement Prediction - Confusion Matrix")
plt.show()


# ==========================================
# 7. ROC CURVE
# ==========================================

RocCurveDisplay.from_predictions(
    y_test,
    y_probability
)

plt.title("Placement Prediction - ROC Curve")
plt.show()


print("\n========================================")
print("EVALUATION COMPLETED!")
print("========================================")