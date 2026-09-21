import pandas as pd


# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

df = pd.read_csv(
    "DATA/students_cleaned.csv"
)

print("Dataset loaded successfully!")
print("Original shape:", df.shape)


# ==========================================
# 2. SKILL SCORE
# ==========================================

df["overall_skill_score"] = (
    df["coding_skill_score"]
    + df["aptitude_score"]
    + df["communication_skill_score"]
    + df["logical_reasoning_score"]
) / 4


# ==========================================
# 3. EXPERIENCE SCORE
# ==========================================

df["experience_score"] = (
    df["internships_count"]
    + df["projects_count"]
    + df["hackathons_participated"]
)


# ==========================================
# 4. PORTFOLIO SCORE
# ==========================================

df["portfolio_score"] = (
    df["projects_count"]
    + df["github_repos"]
    + df["certifications_count"]
)


# ==========================================
# 5. INTERVIEW READINESS
# ==========================================

df["interview_readiness"] = (
    df["mock_interview_score"]
    + df["communication_skill_score"]
    + df["logical_reasoning_score"]
) / 3


# ==========================================
# 6. ACADEMIC RISK
# ==========================================

df["academic_risk"] = (
    df["backlogs"]
    + (10 - df["cgpa"])
)


# ==========================================
# 7. ENGAGEMENT SCORE
# ==========================================

df["engagement_score"] = (
    df["attendance_percentage"]
    + df["extracurricular_score"]
    + df["leadership_score"]
) / 3


# ==========================================
# 8. STUDY PROFILE
# ==========================================

df["study_profile"] = (
    df["study_hours_per_day"]
    * df["attendance_percentage"]
) / 100


# ==========================================
# 9. DISPLAY NEW FEATURES
# ==========================================

new_features = [
    "overall_skill_score",
    "experience_score",
    "portfolio_score",
    "interview_readiness",
    "academic_risk",
    "engagement_score",
    "study_profile"
]

print("\n========================================")
print("NEW FEATURES")
print("========================================")

print(
    df[new_features].head()
)


# ==========================================
# 10. CHECK CORRELATION
# ==========================================

print("\n========================================")
print("NEW FEATURE CORRELATION WITH PLACEMENT")
print("========================================")

correlation = (
    df[new_features + ["placement_status"]]
    .corr()["placement_status"]
    .drop("placement_status")
    .sort_values(
        key=abs,
        ascending=False
    )
)

print(
    correlation.to_string()
)


# ==========================================
# 11. SAVE DATASET
# ==========================================

df.to_csv(
    "DATA/students_engineered.csv",
    index=False
)

print("\n========================================")
print("FEATURE ENGINEERING COMPLETED!")
print("========================================")

print(
    "New dataset saved:"
)

print(
    "DATA/students_engineered.csv"
)

print(
    "\nNew dataset shape:",
    df.shape
)