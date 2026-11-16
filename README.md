# Student Performance Analysis Dashboard

A Streamlit dashboard styled around the supplied dashboard reference image, with Linear Regression score prediction.

## Dashboard sections
- Academic Overview: KPI cards, department bar chart, assessment donut chart, year/semester trend, subject treemap.
- Student & Subject Insights: score distribution, gender comparison, student summary.
- Teacher & Assessment Analytics: teacher comparison, assessment counts, Linear Regression prediction.

## Run
1. Install Python 3.9+.
2. Extract the ZIP and open a terminal in this folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run:
   `streamlit run app.py`

## CSV format
Upload a CSV with these columns:
`StudentID, Department, Subject, Year, Semester, Gender, AssessmentType, Category, Frequency, PassedCourse, StudyHours, Attendance, PreviousScore, Score, WeightedScore, FinalGrade, Teacher`

The included CSV is synthetic sample data with 50 student IDs and eight sample records per student. It is only for demonstrating the dashboard. Replace it with anonymized institutional data for actual analysis. Do not upload student names or other identifying information.
