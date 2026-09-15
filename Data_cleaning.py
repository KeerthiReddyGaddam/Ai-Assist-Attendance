import pandas as pd
import numpy as np

# Load Excel file
df = pd.read_excel(r"C:\Users\keert\OneDrive\Desktop\DAV\Data\AI_Smart_Attendance_500_Students.xlsx")

print("Dataset loaded successfully!")
print(df.head())


print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe())



print("\nMissing Values:")
print(df.isnull().sum())



print("Duplicate rows:", df.duplicated().sum())

df = df.drop_duplicates()

text_columns = [
    "Student ID",
    "Name",
    "Gender",
    "Age",
    "Email",
    "Department",
    "Batch",
    "Subject",
    "Classes Conducted",
    "Classes Attended",
    "CGPA",
    "Email"
    
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()




print(df["Department"].unique())

df["Department"] = df["Department"].str.upper()


department_mapping = {
    "CSE": "CSE",
    "CSE-AI": "CSE-AI",
    "COMPUTER SCIENCE": "CSE",
    "COMPUTER SCIENCE AND ENGINEERING": "CSE"
}

df["Department"] = df["Department"].replace(department_mapping)


department_mapping = {
    "CSE": "CSE",
    "CSE-AI": "CSE-AI",
    "COMPUTER SCIENCE": "CSE",
    "COMPUTER SCIENCE AND ENGINEERING": "CSE"
}

df["Department"] = df["Department"].replace(department_mapping)



print(df["Gender"].unique())


df["Gender"] = df["Gender"].str.strip().str.title()

df["Gender"] = df["Gender"].replace({
    "M": "Male",
    "F": "Female"
})



numeric_columns = [
    "Age",
    "Classes Conducted",
    "Classes Attended",
    "CGPA"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

print("Invalid ages:")

invalid_age = df[
    (df["Age"] < 15) |
    (df["Age"] > 30)
]

print(invalid_age)

invalid_attendance = df[
    (df["Classes Conducted"] <= 0) |
    (df["Classes Attended"] < 0) |
    (df["Classes Attended"] > df["Classes Conducted"])
]

print("Invalid attendance records:")
print(invalid_attendance)

df["Attendance Percentage"] = (
    df["Classes Attended"] /
    df["Classes Conducted"]
) * 100




df["Attendance Percentage"] = df[
    "Attendance Percentage"
].round(2)



df["CGPA"] = df["CGPA"].fillna(
    df["CGPA"].median()
)



df["Department"] = df["Department"].fillna(
    df["Department"].mode()[0]
)

df["Gender"] = df["Gender"].fillna(
    df["Gender"].mode()[0]
)



def attendance_category(attendance):
    if attendance >= 75:
        return "Good"
    elif attendance >= 60:
        return "Average"
    else:
        return "Low"

df["Attendance Category"] = (
    df["Attendance Percentage"]
    .apply(attendance_category)
)



print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\nFinal Duplicate Count:")
print(df.duplicated().sum())

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFinal Data Types:")
print(df.dtypes)


df.to_excel(
    "data/Cleaned_Attendance_Data.xlsx",
    index=False
)