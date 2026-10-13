import pandas as pd
import os

# ============================================================
# AI SMART ATTENDANCE SYSTEM
# DATA ANALYSIS USING PYTHON AND PANDAS
# ============================================================

input_file = "C:\\Users\\keert\\OneDrive\\Desktop\\DAV\\Data\\cleaned_attendance_data.csv"
output_folder = "C:\\Users\\keert\\OneDrive\\Desktop\\DAV\\Data_Analysis\\results"

print("=" * 60)
print("AI SMART ATTENDANCE SYSTEM - DATA ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# 1. Check input file
# ------------------------------------------------------------

if not os.path.exists(input_file):
    print("\nERROR: Cleaned dataset not found.")
    print("Run the Data Cleaning program first.")
    exit()


# ------------------------------------------------------------
# 2. Create results folder
# ------------------------------------------------------------

os.makedirs(output_folder, exist_ok=True)


# ------------------------------------------------------------
# 3. Load cleaned dataset
# ------------------------------------------------------------

df = pd.read_csv(input_file)

print("\nDataset loaded successfully!")

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ------------------------------------------------------------
# 4. Overall attendance analysis
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("OVERALL ATTENDANCE")
print("=" * 60)

total_records = len(df)

present_count = (df["Attendance_Status"] == "Present").sum()
absent_count = (df["Attendance_Status"] == "Absent").sum()
late_count = (df["Attendance_Status"] == "Late").sum()


attendance_percentage = (
    (present_count + late_count) / total_records
) * 100



print("Total attendance records:", total_records)
print("Present:", present_count)
print("Absent:", absent_count)
print("Late:", late_count)

print(
    f"Overall attendance percentage: "
    f"{attendance_percentage:.2f}%"
)


# ------------------------------------------------------------
# 5. Attendance status summary
# ------------------------------------------------------------

status_summary = (
    df["Attendance_Status"]
    .value_counts()
    .reset_index()
)

status_summary.columns = [
    "Attendance_Status",
    "Count"
]

status_summary["Percentage"] = (
    status_summary["Count"] /
    total_records
) * 100

print("\nAttendance Status Summary:")
print(status_summary)

status_summary.to_csv(
    f"{output_folder}/attendance_status_summary.csv",
    index=False
)


# ------------------------------------------------------------
# 6. Department-wise analysis
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DEPARTMENT-WISE ATTENDANCE")
print("=" * 60)

department_analysis = (
    df.groupby("Department")
    .agg(
        Total_Records=("Student_ID", "count"),
        Present=("Present_Flag", "sum"),
        Late=("Late_Flag", "sum")
    )
    .reset_index()
)

department_analysis["Absent"] = (
    department_analysis["Total_Records"]
    - department_analysis["Present"]
)

department_analysis["Attendance_Percentage"] = (
    department_analysis["Present"] /
    department_analysis["Total_Records"]
) * 100

department_analysis[
    "Attendance_Percentage"
] = department_analysis[
    "Attendance_Percentage"
].round(2)

print(department_analysis)

department_analysis.to_csv(
    f"{output_folder}/department_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 7. Year-wise analysis
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("YEAR-WISE ATTENDANCE")
print("=" * 60)

year_analysis = (
    df.groupby("Year")
    .agg(
        Total_Records=("Student_ID", "count"),
        Present=("Present_Flag", "sum")
    )
    .reset_index()
)

year_analysis["Absent"] = (
    year_analysis["Total_Records"]
    - year_analysis["Present"]
)

year_analysis["Attendance_Percentage"] = (
    year_analysis["Present"] /
    year_analysis["Total_Records"]
) * 100

year_analysis[
    "Attendance_Percentage"
] = year_analysis[
    "Attendance_Percentage"
].round(2)

print(year_analysis)

year_analysis.to_csv(
    f"{output_folder}/year_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 8. Subject-wise analysis
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("SUBJECT-WISE ATTENDANCE")
print("=" * 60)

subject_analysis = (
    df.groupby("Subject")
    .agg(
        Total_Records=("Student_ID", "count"),
        Present=("Present_Flag", "sum")
    )
    .reset_index()
)

subject_analysis["Absent"] = (
    subject_analysis["Total_Records"]
    - subject_analysis["Present"]
)

subject_analysis["Attendance_Percentage"] = (
    subject_analysis["Present"] /
    subject_analysis["Total_Records"]
) * 100

subject_analysis[
    "Attendance_Percentage"
] = subject_analysis[
    "Attendance_Percentage"
].round(2)

print(subject_analysis)

subject_analysis.to_csv(
    f"{output_folder}/subject_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 9. Batch-wise analysis
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("BATCH-WISE ATTENDANCE")
print("=" * 60)

batch_analysis = (
    df.groupby("Batch")
    .agg(
        Total_Records=("Student_ID", "count"),
        Present=("Present_Flag", "sum")
    )
    .reset_index()
)

batch_analysis["Attendance_Percentage"] = (
    batch_analysis["Present"] /
    batch_analysis["Total_Records"]
) * 100

batch_analysis[
    "Attendance_Percentage"
] = batch_analysis[
    "Attendance_Percentage"
].round(2)

print(batch_analysis)

batch_analysis.to_csv(
    f"{output_folder}/batch_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 10. Student-wise attendance
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STUDENT-WISE ATTENDANCE")
print("=" * 60)

student_analysis = (
    df.groupby(
        [
            "Student_ID",
            "Student_Name",
            "Department",
            "Year",
            "Batch"
        ]
    )
    .agg(
        Total_Classes=("Student_ID", "count"),
        Present=("Present_Flag", "sum"),
        Late=("Late_Flag", "sum")
    )
    .reset_index()
)

student_analysis["Absent"] = (
    student_analysis["Total_Classes"]
    - student_analysis["Present"]
    - student_analysis["Late"]
)

student_analysis["Attendance_Percentage"] = (
    (student_analysis["Present"] + student_analysis["Late"]) /
    student_analysis["Total_Classes"]
) * 100

student_analysis[
    "Attendance_Percentage"
] = student_analysis[
    "Attendance_Percentage"
].round(2)

print(student_analysis.head(10))

student_analysis.to_csv(
    f"{output_folder}/student_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 11. Students below 75% attendance
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("LOW ATTENDANCE STUDENTS")
print("=" * 60)

low_attendance = student_analysis[
    student_analysis["Attendance_Percentage"] < 75
]

print(
    "Students below 75%:",
    len(low_attendance)
)

print(low_attendance.head(10))

low_attendance.to_csv(
    f"{output_folder}/low_attendance_students.csv",
    index=False
)


# ------------------------------------------------------------
# 12. Date-wise attendance trend
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATE-WISE ATTENDANCE")
print("=" * 60)

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

date_analysis = (
    df.groupby("Date")
    .agg(
        Total_Records=("Student_ID", "count"),
        Present=("Present_Flag", "sum")
    )
    .reset_index()
)

date_analysis["Attendance_Percentage"] = (
    date_analysis["Present"] /
    date_analysis["Total_Records"]
) * 100

date_analysis[
    "Attendance_Percentage"
] = date_analysis[
    "Attendance_Percentage"
].round(2)

print(date_analysis)

date_analysis.to_csv(
    f"{output_folder}/date_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 13. Face recognition confidence analysis
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FACE RECOGNITION CONFIDENCE")
print("=" * 60)

if "Face_Recognition_Confidence" in df.columns:

    average_confidence = (
        df["Face_Recognition_Confidence"]
        .mean()
    )

    minimum_confidence = (
        df["Face_Recognition_Confidence"]
        .min()
    )

    maximum_confidence = (
        df["Face_Recognition_Confidence"]
        .max()
    )

    print(
        f"Average confidence: "
        f"{average_confidence:.3f}"
    )

    print(
        f"Minimum confidence: "
        f"{minimum_confidence:.3f}"
    )

    print(
        f"Maximum confidence: "
        f"{maximum_confidence:.3f}"
    )


# ------------------------------------------------------------
# 14. Top and bottom departments
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DEPARTMENT COMPARISON")
print("=" * 60)

sorted_departments = department_analysis.sort_values(
    "Attendance_Percentage",
    ascending=False
)

print("\nHighest attendance departments:")

print(
    sorted_departments[
        [
            "Department",
            "Attendance_Percentage"
        ]
    ].head(5)
)

print("\nLowest attendance departments:")

print(
    sorted_departments[
        [
            "Department",
            "Attendance_Percentage"
        ]
    ].tail(5)
)


# ------------------------------------------------------------
# 15. Generate overall report
# ------------------------------------------------------------

report_file = (
    f"{output_folder}/analysis_report.txt"
)

with open(report_file, "w") as file:

    file.write(
        "AI SMART ATTENDANCE SYSTEM\n"
    )

    file.write(
        "DATA ANALYSIS REPORT\n"
    )

    file.write(
        "=" * 50 + "\n\n"
    )

    file.write(
        f"Total Records: {total_records}\n"
    )

    file.write(
        f"Present Records: {present_count}\n"
    )

    file.write(
        f"Absent Records: {absent_count}\n"
    )

    file.write(
        f"Late Records: {late_count}\n"
    )

    file.write(
        f"Overall Attendance: "
        f"{attendance_percentage:.2f}%\n\n"
    )

    file.write(
        "Students below 75% attendance: "
        f"{len(low_attendance)}\n"
    )


# ------------------------------------------------------------
# 16. Final message
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATA ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nResults saved inside:")

print(output_folder)

print("\nGenerated files:")

print("- attendance_status_summary.csv")
print("- department_analysis.csv")
print("- year_analysis.csv")
print("- subject_analysis.csv")
print("- batch_analysis.csv")
print("- student_analysis.csv")
print("- low_attendance_students.csv")
print("- date_analysis.csv")
print("- analysis_report.txt")

print("\nYou can now use these results for Task 5:")
print("DATA VISUALIZATION")