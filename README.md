# Student Performance Analysis Dashboard

An interactive Streamlit dashboard for analyzing student academic performance, visualizing educational insights, and predicting student scores using **Linear Regression**.

## 🚀 Live Demo

Explore the deployed dashboard here:

👉 **[Student Performance Analysis Dashboard](https://divyateja949-student-performance-prediction-app.streamlit.app/)**

## 📊 Dashboard Sections

- **Academic Overview:** KPI cards, department bar chart, assessment donut chart, year/semester trend, and subject treemap.
- **Student & Subject Insights:** Score distribution, gender comparison, and student summary.
- **Teacher & Assessment Analytics:** Teacher comparison, assessment counts, and Linear Regression score prediction.

## ⚙️ How to Run Locally

1. Install Python 3.9 or above.
2. Extract the ZIP file and open a terminal in the project folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

## 📁 CSV Format

Upload a CSV file containing these columns:

`StudentID, Department, Subject, Year, Semester, Gender, AssessmentType, Category, Frequency, PassedCourse, StudyHours, Attendance, PreviousScore, Score, WeightedScore, FinalGrade, Teacher`

The included CSV contains synthetic sample data with 50 student IDs and eight sample records per student.

**Note:** The sample dataset is intended only for demonstration. Replace it with anonymized institutional data for actual analysis. Do not upload student names or other personally identifying information.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- Linear Regression

## 👨‍💻 Author

Developed as a Student Performance Analysis and Prediction project using Machine Learning and Data Visualization.
