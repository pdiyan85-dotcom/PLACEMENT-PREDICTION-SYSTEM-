import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
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

print("Data loaded successfully!")


# ==========================================
# 2. PREPROCESS DATA
# ==========================================

X_train_processed = preprocessor.transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# Convert sparse matrix to dense if necessary
if hasattr(X_train_processed, "toarray"):
    X_train_processed = X_train_processed.toarray()

if hasattr(X_test_processed, "toarray"):
    X_test_processed = X_test_processed.toarray()

print("Data preprocessing completed!")

print(
    "Processed training shape:",
    X_train_processed.shape
)

print(
    "Processed testing shape:",
    X_test_processed.shape
)


# ==========================================
# 3. DEFINE MODELS
# ==========================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    ),

    "Hist Gradient Boosting": HistGradientBoostingClassifier(
        max_iter=100,
        learning_rate=0.1,
        max_leaf_nodes=31,
        random_state=42
    )
}


# ==========================================
# 4. TRAIN MODELS
# ==========================================

results = {}

trained_models = {}


for name, model in models.items():

    print("\n================================")
    print("Training:", name)
    print("================================")

    model.fit(
        X_train_processed,
        y_train
    )

    trained_models[name] = model

    # Predictions
    y_pred = model.predict(
        X_test_processed
    )

    # Probability
    y_probability = model.predict_proba(
        X_test_processed
    )[:, 1]

    # Metrics
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

    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    }

    print(
        "Accuracy :",
        round(accuracy, 4)
    )

    print(
        "Precision:",
        round(precision, 4)
    )

    print(
        "Recall   :",
        round(recall, 4)
    )

    print(
        "F1 Score :",
        round(f1, 4)
    )

    print(
        "ROC-AUC  :",
        round(roc_auc, 4)
    )


# ==========================================
# 5. MODEL COMPARISON
# ==========================================

print("\n\n========================================")
print("MODEL COMPARISON")
print("========================================")

for name, metrics in results.items():

    print("\n", name)

    for metric, value in metrics.items():

        print(
            metric,
            ":",
            round(value, 4)
        )


# ==========================================
# 6. SELECT BEST MODEL
# ==========================================

best_model_name = max(
    results,
    key=lambda model: results[model]["ROC-AUC"]
)

best_model = trained_models[
    best_model_name
]


print("\n========================================")
print("BEST MODEL")
print("========================================")

print(
    "Best model:",
    best_model_name
)

print(
    "Best ROC-AUC:",
    round(
        results[best_model_name]["ROC-AUC"],
        4
    )
)

print(
    "Best F1 Score:",
    round(
        results[best_model_name]["F1 Score"],
        4
    )
)


# ==========================================
# 7. SAVE BEST MODEL
# ==========================================

joblib.dump(
    best_model,
    "MODELS/placement_model.pkl"
)

print("\nBest model saved successfully!")

print(
    "File: MODELS/placement_model.pkl"
)


# ==========================================
# 8. SAVE MODEL RESULTS
# ==========================================

joblib.dump(
    results,
    "MODELS/model_results.pkl"
)

print(
    "Model comparison saved!"
)

print(
    "File: MODELS/model_results.pkl"
)


print("\n========================================")
print("MODEL TRAINING COMPLETED!")
print("========================================")