import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline


# ==========================================
# 1. LOAD ENGINEERED DATASET
# ==========================================

df = pd.read_csv(
    "DATA/students_engineered.csv"
)

print("Engineered dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ==========================================
# 2. SEPARATE FEATURES AND TARGET
# ==========================================

X = df.drop("placement_status", axis=1)
y = df["placement_status"]

print("\nFeatures shape:", X.shape)
print("Target shape:", y.shape)


# ==========================================
# 3. CATEGORICAL COLUMNS
# ==========================================

categorical_columns = [
    "gender",
    "branch",
    "college_tier",
    "volunteer_experience"
]


# ==========================================
# 4. NUMERICAL COLUMNS
# ==========================================

numerical_columns = [
    column
    for column in X.columns
    if column not in categorical_columns
]


print("\nCategorical columns:")
print(categorical_columns)

print("\nNumber of numerical columns:")
print(len(numerical_columns))


# ==========================================
# 5. NUMERICAL PIPELINE
# ==========================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "scaler",
            StandardScaler()
        )
    ]
)


# ==========================================
# 6. CATEGORICAL PIPELINE
# ==========================================

categorical_pipeline = Pipeline(
    steps=[
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)


# ==========================================
# 7. CREATE PREPROCESSOR
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numerical_columns
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_columns
        )
    ]
)


# ==========================================
# 8. TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)


# ==========================================
# 9. FIT PREPROCESSOR
# ==========================================

preprocessor.fit(X_train)


# ==========================================
# 10. TRANSFORM DATA
# ==========================================

X_train_processed = preprocessor.transform(
    X_train
)

X_test_processed = preprocessor.transform(
    X_test
)


print("\nProcessed training data:")
print(X_train_processed.shape)

print("\nProcessed testing data:")
print(X_test_processed.shape)


# ==========================================
# 11. SAVE PREPROCESSOR
# ==========================================

joblib.dump(
    preprocessor,
    "MODELS/preprocessor.pkl"
)

print("\nPreprocessor saved successfully!")


# ==========================================
# 12. SAVE TRAIN/TEST DATA
# ==========================================

joblib.dump(
    (
        X_train,
        X_test,
        y_train,
        y_test
    ),
    "MODELS/train_test_data.pkl"
)

print("Train/test data saved successfully!")


print("\n========================================")
print("ENGINEERED DATA PREPROCESSING COMPLETED!")
print("========================================")