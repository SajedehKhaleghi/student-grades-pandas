"""Combine student CSV files (info, quizzes, project, final exam) and compute final grades.

Scoring (out of 20):
    (Quiz1 + Quiz2) * 0.25 + Project * 0.10 + Final * 0.25 + group bonus, capped at 20
Quiz1 is out of 10, Quiz2 is a letter (A=10, B=8, C=6), Project is out of 100, Final is out of 20.
Group bonus: +1 if the student's group has an average project score above 80.
Missing quiz scores count as 0.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
QUIZ2_POINTS = {"A": 10, "B": 8, "C": 6}
BONUS_THRESHOLD = 80
MAX_SCORE = 20
# right-inclusive bands: (-inf,12] E, (12,14] D, (14,16] C, (16,18] B, (18,inf) A
GRADE_BINS = [float("-inf"), 12, 14, 16, 18, float("inf")]
GRADE_LABELS = ["E", "D", "C", "B", "A"]


def read_csv_file(name):
    return pd.read_csv(DATA_DIR / f"student_{name}.csv")


def group_bonus(project_df):
    """1 for students whose group's mean project score is above the threshold, else 0."""
    group_means = project_df.groupby("Group")["Project_Score"].mean()
    return (project_df["Group"].map(group_means) > BONUS_THRESHOLD).astype(int)


def load_students():
    info = read_csv_file("Information")
    quiz1 = read_csv_file("Quiz1").drop(columns=["Name", "Family"])
    quiz2 = read_csv_file("Quiz2").drop(columns=["Name", "Family"])
    project = read_csv_file("Project").drop(columns=["Name", "Family", "Group"])
    final = read_csv_file("Final_Exam").drop(columns=["Name", "Family"])

    quiz2["Quiz2_Score"] = quiz2["Quiz2_Grade"].map(QUIZ2_POINTS)
    quiz2 = quiz2.drop(columns=["Quiz2_Grade"])

    df = info
    for other in (quiz1, quiz2, project, final):
        df = df.merge(other, on="SID")

    df["Quiz_Score"] = df["Quiz1_Score"].fillna(0) + df["Quiz2_Score"].fillna(0)
    df["Group_Bonus"] = group_bonus(df)
    return df


def compute_grades(df):
    df = df.copy()
    df["Total"] = (df["Quiz_Score"] * 0.25
                   + df["Project_Score"] * 0.10
                   + df["FinalExam_Score"] * 0.25
                   + df["Group_Bonus"]).clip(upper=MAX_SCORE)
    df["Grade"] = pd.cut(df["Total"], bins=GRADE_BINS, labels=GRADE_LABELS)
    return df


def main():
    df = compute_grades(load_students())
    print(df[["SID", "Name", "Family", "Group", "Quiz_Score", "Project_Score",
              "FinalExam_Score", "Group_Bonus", "Total", "Grade"]].to_string(index=False))

    counts = df["Grade"].value_counts().reindex(GRADE_LABELS[::-1], fill_value=0)
    counts.plot.bar()
    plt.title("Grade distribution")
    plt.xlabel("Grade")
    plt.ylabel("Students")
    plt.show()


if __name__ == "__main__":
    main()
