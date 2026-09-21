import pandas as pd

df = pd.read_csv("DATA/student_placement.csv")

print("Original dataset shape:")
print(df.shape)

# Remove student ID
df = df.drop("student_id", axis=1)

# Remove salary
df = df.drop("salary_package_lpa", axis=1)

# Clean text columns
text_columns = [
    "gender",
    "branch",
    "college_tier",
    "volunteer_experience",
    "placement_status"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()

# Convert placement status to lowercase
df["placement_status"] = df["placement_status"].str.lower()

# Convert placement status to 0 and 1
df["placement_status"] = df["placement_status"].map({
    "placed": 1,
    "not placed": 0
})

print("\nPlacement status after conversion:")
print(df["placement_status"].value_counts())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nCleaned dataset shape:")
print(df.shape)

# Save cleaned dataset
df.to_csv("DATA/students_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")