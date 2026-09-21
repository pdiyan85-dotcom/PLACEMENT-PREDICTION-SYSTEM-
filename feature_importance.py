import pandas as pd
import joblib
import matplotlib.pyplot as plt


# ==========================================
# 1. LOAD MODEL AND PREPROCESSOR
# ==========================================

model = joblib.load(
    "MODELS/placement_model.pkl"
)

preprocessor = joblib.load(
    "MODELS/preprocessor.pkl"
)

print("Model and preprocessor loaded successfully!")


# ==========================================
# 2. GET FEATURE NAMES
# ==========================================

feature_names = preprocessor.get_feature_names_out()


# ==========================================
# 3. GET MODEL COEFFICIENTS
# ==========================================

coefficients = model.coef_[0]


# ==========================================
# 4. CREATE FEATURE IMPORTANCE DATAFRAME
# ==========================================

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})


# Absolute value shows strength of influence
importance_df["Importance"] = (
    importance_df["Coefficient"].abs()
)


# ==========================================
# 5. SORT FEATURES
# ==========================================

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)


# ==========================================
# 6. DISPLAY TOP 15 FEATURES
# ==========================================

print("\n========================================")
print("TOP 15 IMPORTANT FEATURES")
print("========================================")

print(
    importance_df[
        ["Feature", "Coefficient", "Importance"]
    ].head(15).to_string(index=False)
)


# ==========================================
# 7. SAVE RESULTS
# ==========================================

importance_df.to_csv(
    "DATA/feature_importance.csv",
    index=False
)

print("\nFeature importance saved!")
print("File: DATA/feature_importance.csv")


# ==========================================
# 8. PLOT TOP 15 FEATURES
# ==========================================

top_features = importance_df.head(15)

plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"][::-1],
    top_features["Coefficient"][::-1]
)

plt.title(
    "Top 15 Features Influencing Placement Prediction"
)

plt.xlabel("Logistic Regression Coefficient")
plt.ylabel("Feature")

plt.tight_layout()

plt.show()


print("\n========================================")
print("FEATURE IMPORTANCE COMPLETED!")
print("========================================")