# Data Collection

## Overview

The AI Smart Attendance System requires attendance data to record and analyze student attendance.

The collected dataset contains attendance records for students across different departments, years, batches, subjects, dates, periods, and classrooms.

## Dataset

The raw dataset contains 384,000 attendance records.

The dataset includes information related to:

* Student details
* Academic department
* Year and batch
* Subject
* Date and class period
* Classroom and block
* Attendance status
* Late attendance
* Face recognition confidence
* Detection result

## Columns

| Column                      | Description                            |
| --------------------------- | -------------------------------------- |
| Session_ID                  | Unique identifier for a class session  |
| Date                        | Date of the attendance session         |
| Day                         | Day of the week                        |
| Start_Time                  | Class starting time                    |
| End_Time                    | Class ending time                      |
| Period                      | Class period                           |
| Student_ID                  | Unique student identifier              |
| Student_Name                | Student name                           |
| Email                       | Student email address                  |
| Department                  | Student department                     |
| Year                        | Student academic year                  |
| Batch                       | Student batch                          |
| Subject                     | Subject for the class                  |
| Room_Number                 | Classroom number                       |
| Block                       | Academic block                         |
| Attendance_Status           | Present, Late, or Absent               |
| Present_Flag                | Numeric indicator for attendance       |
| Late_Flag                   | Numeric indicator for late attendance  |
| Face_Recognition_Confidence | Confidence score from face recognition |
| Detection_Result            | Face detection result                  |

## Purpose

The collected data will be used in the next stages of the project:

1. Data Cleaning
2. Data Analysis
3. Data Visualization
4. Interactive Dashboard

The original dataset is preserved as raw data so that the cleaning and analysis processes can be performed separately.
