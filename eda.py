import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("DATA/students_cleaned.csv")

print("Dataset shape:")
print(df.shape)

print("\nPlacement distribution:")
print(df["placement_status"].value_counts())

# -------------------------------
# 1. Placement Distribution
# -------------------------------

plt.figure(figsize=(8, 5))

df["placement_status"].value_counts().rename(
    index={1: "Placed", 0: "Not Placed"}
).plot(kind="bar")

plt.title("Placement Status Distribution")
plt.xlabel("Placement Status")
plt.ylabel("Number of Students")
plt.xticks(rotation=0)

plt.show()


# -------------------------------
# 2. CGPA vs Placement
# -------------------------------

plt.figure(figsize=(8, 5))

df.boxplot(
    column="cgpa",
    by="placement_status"
)

plt.title("CGPA vs Placement")
plt.suptitle("")
plt.xlabel("Placement Status (0 = Not Placed, 1 = Placed)")
plt.ylabel("CGPA")

plt.show()


# -------------------------------
# 3. Coding Skill vs Placement
# -------------------------------

plt.figure(figsize=(8, 5))

df.boxplot(
    column="coding_skill_score",
    by="placement_status"
)

plt.title("Coding Skill Score vs Placement")
plt.suptitle("")
plt.xlabel("Placement Status")
plt.ylabel("Coding Skill Score")

plt.show()


# -------------------------------
# 4. Internship Count vs Placement
# -------------------------------

plt.figure(figsize=(8, 5))

pd.crosstab(
    df["internships_count"],
    df["placement_status"]
).plot(kind="bar")

plt.title("Internships vs Placement")
plt.xlabel("Number of Internships")
plt.ylabel("Number of Students")
plt.legend(["Not Placed", "Placed"])

plt.show()


# -------------------------------
# 5. Projects Count vs Placement
# -------------------------------

plt.figure(figsize=(8, 5))

pd.crosstab(
    df["projects_count"],
    df["placement_status"]
).plot(kind="bar")

plt.title("Projects vs Placement")
plt.xlabel("Number of Projects")
plt.ylabel("Number of Students")
plt.legend(["Not Placed", "Placed"])

plt.show()


# -------------------------------
# 6. Attendance vs Placement
# -------------------------------

plt.figure(figsize=(8, 5))

df.boxplot(
    column="attendance_percentage",
    by="placement_status"
)

plt.title("Attendance vs Placement")
plt.suptitle("")
plt.xlabel("Placement Status")
plt.ylabel("Attendance Percentage")

plt.show()


# -------------------------------
# 7. Aptitude Score vs Placement
# -------------------------------

plt.figure(figsize=(8, 5))

df.boxplot(
    column="aptitude_score",
    by="placement_status"
)

plt.title("Aptitude Score vs Placement")
plt.suptitle("")
plt.xlabel("Placement Status")
plt.ylabel("Aptitude Score")

plt.show()


# -------------------------------
# 8. Communication Score vs Placement
# -------------------------------

plt.figure(figsize=(8, 5))

df.boxplot(
    column="communication_skill_score",
    by="placement_status"
)

plt.title("Communication Skill vs Placement")
plt.suptitle("")
plt.xlabel("Placement Status")
plt.ylabel("Communication Score")

plt.show()


# -------------------------------
# 9. College Tier vs Placement
# -------------------------------

plt.figure(figsize=(8, 5))

pd.crosstab(
    df["college_tier"],
    df["placement_status"],
    normalize="index"
).plot(kind="bar")

plt.title("College Tier vs Placement")
plt.xlabel("College Tier")
plt.ylabel("Placement Proportion")

plt.legend(["Not Placed", "Placed"])
plt.xticks(rotation=0)

plt.show()


# -------------------------------
# 10. Backlogs vs Placement
# -------------------------------

plt.figure(figsize=(8, 5))

pd.crosstab(
    df["backlogs"],
    df["placement_status"]
).plot(kind="bar")

plt.title("Backlogs vs Placement")
plt.xlabel("Number of Backlogs")
plt.ylabel("Number of Students")

plt.legend(["Not Placed", "Placed"])

plt.show()

print("\nEDA completed successfully!")