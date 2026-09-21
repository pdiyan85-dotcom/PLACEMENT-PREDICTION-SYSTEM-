import pandas as pd

df = pd.read_csv("DATA/student_placement.csv")

print("========== PLACEMENT STATUS ==========")
print(df["placement_status"].value_counts())

print("\n========== PLACEMENT STATUS PERCENTAGE ==========")
print(df["placement_status"].value_counts(normalize=True) * 100)

print("\n========== GENDER ==========")
print(df["gender"].value_counts())

print("\n========== BRANCH ==========")
print(df["branch"].value_counts())

print("\n========== COLLEGE TIER ==========")
print(df["college_tier"].value_counts())

print("\n========== VOLUNTEER EXPERIENCE ==========")
print(df["volunteer_experience"].value_counts())

print("\n========== DATASET INFORMATION ==========")
print(df.info())

print("\n========== NUMERICAL SUMMARY ==========")
print(df.describe())