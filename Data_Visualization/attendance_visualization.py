
import os
import pandas as pd
import matplotlib.pyplot as plt

# Define folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_DIR = os.path.join(BASE_DIR, "..", "Data_Analysis", "results")
OUTPUT_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 50)
print("AI SMART ATTENDANCE SYSTEM")
print("DATA VISUALIZATION")
print("=" * 50)


def save_chart(filename):
    """Save the current chart and close it."""
    output_path = os.path.join(OUTPUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {filename}")


# 1. Attendance Status Distribution
status_file = os.path.join(
    ANALYSIS_DIR, "attendance_status_summary.csv"
)

status_df = pd.read_csv(status_file)

plt.figure(figsize=(8, 6))
plt.bar(
    status_df.iloc[:, 0].astype(str),
    status_df.iloc[:, 1],
)

plt.title("Attendance Status Distribution")
plt.xlabel("Attendance Status")
plt.ylabel("Number of Records")
plt.xticks(rotation=0)

save_chart("attendance_distribution.png")


# 2. Department-wise Attendance Distribution
department_file = os.path.join(
    ANALYSIS_DIR, "department_analysis.csv"
)

department_df = pd.read_csv(department_file)

department_df["Attendance_Percentage"] = (
    (department_df["Present"] + department_df["Late"])
    / department_df["Total_Records"]
) * 100

plt.figure(figsize=(9, 7))

plt.pie(
    department_df["Total_Records"],
    labels=department_df["Department"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Distribution of Attendance Records by Department")

save_chart("department_attendance.png")

# 3. Year-wise Attendance
year_file = os.path.join(
    ANALYSIS_DIR, "year_analysis.csv"
)

year_df = pd.read_csv(year_file)

plt.figure(figsize=(8, 6))
plt.bar(
    year_df["Year"].astype(str),
    year_df["Attendance_Percentage"],
)

plt.title("Year-wise Attendance Percentage")
plt.xlabel("Academic Year")
plt.ylabel("Attendance Percentage (%)")

save_chart("year_attendance.png")




# 4. Daily Attendance Trend
date_file = os.path.join(
    ANALYSIS_DIR, "date_analysis.csv"
)

date_df = pd.read_csv(date_file)
date_df["Date"] = pd.to_datetime(date_df["Date"])
date_df = date_df.sort_values("Date")

# Use the attendance percentage already calculated
if "Attendance_Percentage" in date_df.columns:
    attendance_column = "Attendance_Percentage"
else:
    # Calculate attendance if the CSV has Present and Total_Records
    date_df["Attendance_Percentage"] = (
        date_df["Present"] / date_df["Total_Records"]
    ) * 100
    attendance_column = "Attendance_Percentage"

plt.figure(figsize=(12, 6))
plt.plot(
    date_df["Date"],
    date_df[attendance_column],
    marker="o",
)

plt.title("Daily Attendance Trend")
plt.xlabel("Date")
plt.ylabel("Attendance Percentage (%)")
plt.xticks(rotation=45)

save_chart("daily_attendance_trend.png")

# 5. Ten Students with Lowest Attendance
low_file = os.path.join(
    ANALYSIS_DIR, "low_attendance_students.csv"
)

low_df = pd.read_csv(low_file)

low_df = low_df.sort_values(
    "Attendance_Percentage", ascending=True
).head(10)

plt.figure(figsize=(10, 7))

plt.barh(
    low_df["Student_ID"].astype(str),
    low_df["Attendance_Percentage"]
)

plt.title("10 Students with Lowest Attendance")
plt.xlabel("Attendance Percentage (%)")
plt.ylabel("Student ID")
plt.gca().invert_yaxis()

save_chart("lowest_attendance_students.png")


print("\nAll visualization charts generated successfully!")
print(f"Charts are saved in: {OUTPUT_DIR}")

