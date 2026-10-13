import pandas as pd
import os

# ============================================================
# AI SMART ATTENDANCE SYSTEM
# DATA CLEANING USING PYTHON AND PANDAS
# ============================================================

# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

input_file = "C:\\Users\\keert\\OneDrive\\Desktop\\DAV\\Data\\Final_AI_Assist_Attendance_DAV_Dataset.csv"
output_file = "C:\\Users\\keert\\OneDrive\\Desktop\\DAV\\Data\\cleaned_attendance_data.csv"

print("=" * 60)
print("AI SMART ATTENDANCE SYSTEM - DATA CLEANING")
print("=" * 60)


# ------------------------------------------------------------
# 2. Check whether input file exists
# ------------------------------------------------------------

if not os.path.exists(input_file):
    print(f"\nERROR: File not found: {input_file}")
    print("Make sure raw_attendance_data.csv is inside the Data folder.")
    exit()


# ------------------------------------------------------------
# 3. Load the raw dataset
# ------------------------------------------------------------

df = pd.read_csv(input_file)

print("\nDataset loaded successfully!")

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))


# ------------------------------------------------------------
# 4. Display basic information
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ORIGINAL DATASET INFORMATION")
print("=" * 60)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\nData types:")
print(df.dtypes)


# ------------------------------------------------------------
# 5. Check missing values
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing_values = df.isnull().sum()

print(missing_values)

total_missing = missing_values.sum()

print("\nTotal missing values:", total_missing)


# ------------------------------------------------------------
# 6. Remove completely empty rows
# ------------------------------------------------------------

before_empty_rows = len(df)

df = df.dropna(how="all")

after_empty_rows = len(df)

print("\nCompletely empty rows removed:",
      before_empty_rows - after_empty_rows)


# ------------------------------------------------------------
# 7. Remove duplicate records
# ------------------------------------------------------------

duplicates = df.duplicated().sum()

print("\nDuplicate records found:", duplicates)

df = df.drop_duplicates()

print("Duplicate records after cleaning:",
      df.duplicated().sum())


# ------------------------------------------------------------
# 8. Remove unnecessary spaces from text columns
# ------------------------------------------------------------

text_columns = df.select_dtypes(include="object").columns

for column in text_columns:
    df[column] = df[column].str.strip()


# ------------------------------------------------------------
# 9. Standardize important text columns
# ------------------------------------------------------------

columns_to_uppercase = [
    "Department",
    "Attendance_Status",
    "Detection_Result"
]

for column in columns_to_uppercase:
    if column in df.columns:
        df[column] = df[column].str.upper()


# ------------------------------------------------------------
# 10. Standardize attendance status
# ------------------------------------------------------------

if "Attendance_Status" in df.columns:

    status_mapping = {
        "PRESENT": "Present",
        "ABSENT": "Absent",
        "LATE": "Late"
    }

    df["Attendance_Status"] = (
        df["Attendance_Status"]
        .map(status_mapping)
        .fillna(df["Attendance_Status"])
    )


# ------------------------------------------------------------
# 11. Convert Date column to proper date format
# ------------------------------------------------------------

if "Date" in df.columns:

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    invalid_dates = df["Date"].isnull().sum()

    print("\nInvalid dates found:", invalid_dates)

    # Convert date to standard format
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")


# ------------------------------------------------------------
# 12. Convert numeric columns to numeric data types
# ------------------------------------------------------------

numeric_columns = [
    "Year",
    "Period",
    "Present_Flag",
    "Late_Flag",
    "Face_Recognition_Confidence"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ------------------------------------------------------------
# 13. Check valid attendance status
# ------------------------------------------------------------

if "Attendance_Status" in df.columns:

    valid_statuses = [
        "Present",
        "Absent",
        "Late"
    ]

    invalid_status = ~df["Attendance_Status"].isin(
        valid_statuses
    )

    print(
        "\nInvalid attendance status records:",
        invalid_status.sum()
    )

    # Replace invalid status with missing value
    df.loc[invalid_status, "Attendance_Status"] = pd.NA


# ------------------------------------------------------------
# 14. Validate Present_Flag
# ------------------------------------------------------------

if "Present_Flag" in df.columns:

    invalid_present_flag = ~df["Present_Flag"].isin([0, 1])

    print(
        "\nInvalid Present_Flag records:",
        invalid_present_flag.sum()
    )

    df.loc[invalid_present_flag, "Present_Flag"] = pd.NA


# ------------------------------------------------------------
# 15. Validate Late_Flag
# ------------------------------------------------------------

if "Late_Flag" in df.columns:

    invalid_late_flag = ~df["Late_Flag"].isin([0, 1])

    print(
        "Invalid Late_Flag records:",
        invalid_late_flag.sum()
    )

    df.loc[invalid_late_flag, "Late_Flag"] = pd.NA


# ------------------------------------------------------------
# 16. Validate face recognition confidence
# ------------------------------------------------------------

if "Face_Recognition_Confidence" in df.columns:

    invalid_confidence = (
        (df["Face_Recognition_Confidence"] < 0) |
        (df["Face_Recognition_Confidence"] > 1)
    )

    print(
        "\nInvalid face recognition confidence:",
        invalid_confidence.sum()
    )

    df.loc[
        invalid_confidence,
        "Face_Recognition_Confidence"
    ] = pd.NA


# ------------------------------------------------------------
# 17. Handle missing values
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("HANDLING MISSING VALUES")
print("=" * 60)

# Numeric columns → median
for column in numeric_columns:

    if column in df.columns:

        if df[column].isnull().sum() > 0:

            median_value = df[column].median()

            df[column] = df[column].fillna(median_value)

            print(
                f"{column}: missing values filled using median"
            )


# Categorical columns → mode
categorical_columns = [
    "Department",
    "Year",
    "Batch",
    "Subject",
    "Room_Number",
    "Block",
    "Attendance_Status",
    "Detection_Result"
]

for column in categorical_columns:

    if column in df.columns:

        if df[column].isnull().sum() > 0:

            mode_value = df[column].mode()

            if not mode_value.empty:

                df[column] = df[column].fillna(
                    mode_value[0]
                )

                print(
                    f"{column}: missing values filled using mode"
                )


# ------------------------------------------------------------
# 18. Check Student_ID
# ------------------------------------------------------------

if "Student_ID" in df.columns:

    missing_student_id = df["Student_ID"].isnull().sum()

    print(
        "\nMissing Student_ID records:",
        missing_student_id
    )

    # Student ID is important, so records without it
    # cannot be reliably identified.
    df = df.dropna(subset=["Student_ID"])


# ------------------------------------------------------------
# 19. Check Email format
# ------------------------------------------------------------

if "Email" in df.columns:

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    invalid_email = ~df["Email"].str.match(
        email_pattern,
        na=False
    )

    print(
        "\nInvalid email records:",
        invalid_email.sum()
    )


# ------------------------------------------------------------
# 20. Final duplicate check
# ------------------------------------------------------------

final_duplicates = df.duplicated().sum()

print(
    "\nDuplicate records remaining:",
    final_duplicates
)


# ------------------------------------------------------------
# 21. Final missing-value check
# ------------------------------------------------------------

final_missing = df.isnull().sum()

print("\nFinal missing values:")

print(final_missing[final_missing > 0])


# ------------------------------------------------------------
# 22. Save cleaned dataset
# ------------------------------------------------------------

df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 60)
print("CLEANING COMPLETED")
print("=" * 60)

print("\nCleaned dataset saved to:")

print(output_file)

print("\nFinal number of rows:", len(df))

print("Final number of columns:", len(df.columns))

print("\nCleaning process completed successfully!")