import pandas as pd


# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv(
    "DATA/students_cleaned.csv"
)

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# ==========================================
# 2. TARGET DISTRIBUTION
# ==========================================

print("\n========================================")
print("TARGET DISTRIBUTION")
print("========================================")

print(
    df["placement_status"].value_counts()
)

print("\nPercentage:")

print(
    df["placement_status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


# ==========================================
# 3. NUMERICAL CORRELATION WITH TARGET
# ==========================================

print("\n========================================")
print("NUMERICAL FEATURE CORRELATION")
print("========================================")

numeric_columns = df.select_dtypes(
    include=["int64", "float64"]
).columns

correlation = (
    df[numeric_columns]
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
# 4. PLACEMENT RATE BY COLLEGE TIER
# ==========================================

print("\n========================================")
print("COLLEGE TIER VS PLACEMENT")
print("========================================")

print(
    df.groupby("college_tier")[
        "placement_status"
    ]
    .mean()
    .mul(100)
    .round(2)
)


# ==========================================
# 5. PLACEMENT RATE BY GENDER
# ==========================================

print("\n========================================")
print("GENDER VS PLACEMENT")
print("========================================")

print(
    df.groupby("gender")[
        "placement_status"
    ]
    .mean()
    .mul(100)
    .round(2)
)


# ==========================================
# 6. PLACEMENT RATE BY BRANCH
# ==========================================

print("\n========================================")
print("BRANCH VS PLACEMENT")
print("========================================")

print(
    df.groupby("branch")[
        "placement_status"
    ]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
    .round(2)
)


# ==========================================
# 7. PLACEMENT RATE BY VOLUNTEER EXPERIENCE
# ==========================================

print("\n========================================")
print("VOLUNTEER EXPERIENCE VS PLACEMENT")
print("========================================")

print(
    df.groupby("volunteer_experience")[
        "placement_status"
    ]
    .mean()
    .mul(100)
    .round(2)
)


# ==========================================
# 8. CGPA GROUPS
# ==========================================

print("\n========================================")
print("CGPA VS PLACEMENT")
print("========================================")

df["cgpa_group"] = pd.cut(
    df["cgpa"],
    bins=[
        0,
        5,
        6,
        7,
        8,
        9,
        10
    ],
    labels=[
        "<5",
        "5-6",
        "6-7",
        "7-8",
        "8-9",
        "9-10"
    ]
)

print(
    df.groupby(
        "cgpa_group",
        observed=False
    )["placement_status"]
    .agg(
        ["count", "mean"]
    )
    .assign(
        placement_percentage=lambda x:
        (x["mean"] * 100).round(2)
    )
)


# ==========================================
# 9. INTERNSHIPS VS PLACEMENT
# ==========================================

print("\n========================================")
print("INTERNSHIPS VS PLACEMENT")
print("========================================")

print(
    df.groupby("internships_count")[
        "placement_status"
    ]
    .agg(
        ["count", "mean"]
    )
    .assign(
        placement_percentage=lambda x:
        (x["mean"] * 100).round(2)
    )
)


# ==========================================
# 10. PROJECTS VS PLACEMENT
# ==========================================

print("\n========================================")
print("PROJECTS VS PLACEMENT")
print("========================================")

print(
    df.groupby("projects_count")[
        "placement_status"
    ]
    .agg(
        ["count", "mean"]
    )
    .assign(
        placement_percentage=lambda x:
        (x["mean"] * 100).round(2)
    )
)


# ==========================================
# 11. BACKLOGS VS PLACEMENT
# ==========================================

print("\n========================================")
print("BACKLOGS VS PLACEMENT")
print("========================================")

print(
    df.groupby("backlogs")[
        "placement_status"
    ]
    .agg(
        ["count", "mean"]
    )
    .assign(
        placement_percentage=lambda x:
        (x["mean"] * 100).round(2)
    )
)


print("\n========================================")
print("DIAGNOSIS COMPLETED!")
print("========================================")