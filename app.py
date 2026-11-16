import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Student Performance Analysis", page_icon="🎓", layout="wide")
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#edf5ff 0%,#f8fbff 100%);}
.block-container {padding-top:1rem; padding-bottom:1rem;}
[data-testid="stMetric"] {background:white; border:1px solid #dce9fb; padding:16px 18px; border-radius:18px; box-shadow:0 4px 12px #174c8520;}
[data-testid="stVerticalBlockBorderWrapper"] {background:white;}
h1,h2,h3 {color:#123f78;}
section[data-testid="stSidebar"] {background:#f8fbff;}
div[data-testid="stPlotlyChart"] {background:white; border-radius:16px; padding:8px; border:1px solid #dce9fb;}
</style>
""", unsafe_allow_html=True)

st.title("🎓 Student Performance Analysis")
st.caption("Academic overview • Student and subject insights • Teacher and assessment analytics")

@st.cache_data
def load_default():
    return pd.read_csv("student_performance.csv")

uploaded = st.sidebar.file_uploader("Upload your student CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = load_default()

required = ["StudentID","Department","Subject","Year","Semester","Gender","AssessmentType",
            "Category","Frequency","PassedCourse","StudyHours","Attendance","PreviousScore",
            "Score","WeightedScore","FinalGrade","Teacher"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error("Your CSV is missing required columns: " + ", ".join(missing))
    st.info("Download the sample CSV to see the required format.")
    st.stop()

st.sidebar.markdown("### 🔎 FILTERS")
def filter_select(label, col):
    vals = ["All"] + sorted(df[col].dropna().astype(str).unique().tolist())
    return st.sidebar.selectbox(label, vals)
year = filter_select("Year", "Year")
semester = filter_select("Semester", "Semester")
gender = filter_select("Gender", "Gender")
assessment = filter_select("AssessmentType", "AssessmentType")
category = filter_select("Category", "Category")
frequency = filter_select("Frequency", "Frequency")
passed = filter_select("PassedCourse", "PassedCourse")

f = df.copy()
for col, val in [("Year",year),("Semester",semester),("Gender",gender),
                 ("AssessmentType",assessment),("Category",category),
                 ("Frequency",frequency),("PassedCourse",passed)]:
    if val != "All":
        f = f[f[col].astype(str) == val]
if f.empty:
    st.warning("No records match these filters. Adjust the filters.")
    st.stop()
if st.sidebar.button("↻ Clear All", use_container_width=True):
    st.rerun()
csv_sample = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button("⬇ Download Sample CSV", csv_sample, "student_performance_sample.csv", "text/csv")

tab1, tab2, tab3 = st.tabs(["📊 Academic Overview", "👩‍🎓 Student & Subject Insights", "🧑‍🏫 Teacher & Assessment Analytics"])

with tab1:
    total = f["StudentID"].nunique()
    avg = f["Score"].mean()
    pass_rate = (f["PassedCourse"].astype(str).str.lower() == "yes").mean()*100
    common_grade = f["FinalGrade"].mode().iloc[0]
    weighted = f["WeightedScore"].mean()
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Students", f"{total:,}")
    c2.metric("Average Score", f"{avg:.2f}")
    c3.metric("Pass Rate", f"{pass_rate:.2f}%")
    c4.metric("Most Common Grade", common_grade)
    c5.metric("Average Weighted Score", f"{weighted:.2f}")

    left,right = st.columns([1.55,1])
    with left:
        st.subheader("Average Score by Department and Final Grade")
        dept = f.groupby("Department",as_index=False)["Score"].mean().sort_values("Score",ascending=False)
        fig = px.bar(dept,x="Department",y="Score",text_auto=".2f",color="Score",
                     color_continuous_scale=["#9bd4ff","#0876cf"])
        fig.update_layout(height=330,margin=dict(l=10,r=10,t=10,b=60),showlegend=False,
                          coloraxis_showscale=False,xaxis_title="",yaxis_title="Average score")
        fig.update_yaxes(range=[0,100])
        st.plotly_chart(fig,use_container_width=True)
    with right:
        st.subheader("Average Score by Assessment Type")
        assess = f.groupby("AssessmentType",as_index=False)["Score"].mean()
        fig = px.pie(assess,names="AssessmentType",values="Score",hole=.58,
                     color_discrete_sequence=["#064b91","#3699e6","#91cafa"])
        fig.update_traces(textinfo="label+percent",textposition="outside")
        fig.update_layout(height=330,margin=dict(l=15,r=15,t=10,b=10),showlegend=True)
        st.plotly_chart(fig,use_container_width=True)

    left,right = st.columns([1.55,1])
    with left:
        st.subheader("Average Score by Year and Semester")
        trend = f.groupby(["Year","Semester"],as_index=False)["Score"].mean()
        trend["Period"] = trend["Semester"] + " " + trend["Year"].astype(str)
        trend = trend.sort_values(["Year","Semester"])
        fig = px.line(trend,x="Period",y="Score",markers=True,
                      color_discrete_sequence=["#2795e8"])
        fig.update_layout(height=300,margin=dict(l=10,r=10,t=10,b=70),xaxis_title="",yaxis_title="Average score")
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(fig,use_container_width=True)
    with right:
        st.subheader("Average Score by Subjects")
        sub = f.groupby("Subject",as_index=False)["Score"].mean()
        fig = px.treemap(sub,path=["Subject"],values="Score",color="Score",
                         color_continuous_scale=["#9bd4ff","#075092"])
        fig.update_layout(height=300,margin=dict(l=5,r=5,t=5,b=5),coloraxis_showscale=False)
        st.plotly_chart(fig,use_container_width=True)

with tab2:
    st.subheader("Student & Subject Insights")
    a,b = st.columns(2)
    with a:
        st.markdown("**Student score distribution**")
        fig = px.histogram(f,x="Score",nbins=15,color_discrete_sequence=["#268fe0"])
        fig.update_layout(height=320,xaxis_title="Score",yaxis_title="Number of assessments")
        st.plotly_chart(fig,use_container_width=True)
    with b:
        st.markdown("**Average score by gender**")
        g = f.groupby("Gender",as_index=False)["Score"].mean()
        fig = px.bar(g,x="Gender",y="Score",text_auto=".2f",color="Gender",
                     color_discrete_sequence=["#258fdf","#f2a84b"])
        fig.update_layout(height=320,showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
    st.markdown("**Student performance details**")
    student = f.groupby("StudentID",as_index=False).agg(
        AverageScore=("Score","mean"), Attendance=("Attendance","mean"),
        StudyHours=("StudyHours","mean"), Assessments=("Score","count"))
    st.dataframe(student.sort_values("AverageScore",ascending=False),use_container_width=True)

with tab3:
    st.subheader("Teacher & Assessment Analytics")
    a,b = st.columns(2)
    with a:
        st.markdown("**Average score by teacher**")
        t = f.groupby("Teacher",as_index=False)["Score"].mean().sort_values("Score",ascending=False)
        fig = px.bar(t,x="Teacher",y="Score",color="Score",color_continuous_scale=["#a6d9ff","#075092"])
        fig.update_layout(height=330,coloraxis_showscale=False)
        st.plotly_chart(fig,use_container_width=True)
    with b:
        st.markdown("**Assessment count by type**")
        counts = f["AssessmentType"].value_counts().rename_axis("AssessmentType").reset_index(name="Count")
        fig = px.pie(counts,names="AssessmentType",values="Count",hole=.55,
                     color_discrete_sequence=["#075092","#2795e8","#9bd4ff"])
        fig.update_layout(height=330)
        st.plotly_chart(fig,use_container_width=True)

    st.markdown("### Linear Regression – Student Score Prediction")
    features = ["StudyHours","Attendance","PreviousScore"]
    model_data = f[features+["Score"]].dropna()
    if len(model_data) >= 10:
        X_train,X_test,y_train,y_test = train_test_split(
            model_data[features],model_data["Score"],test_size=.2,random_state=42)
        model = LinearRegression().fit(X_train,y_train)
        pred = model.predict(X_test)
        m1,m2,m3 = st.columns(3)
        m1.metric("R² Score",f"{r2_score(y_test,pred):.3f}")
        m2.metric("MAE",f"{mean_absolute_error(y_test,pred):.2f}")
        m3.metric("RMSE",f"{mean_squared_error(y_test,pred)**.5:.2f}")
        p1,p2,p3 = st.columns(3)
        hours = p1.number_input("Study hours per day",0.0,16.0,4.0,.5)
        att = p2.number_input("Attendance (%)",0.0,100.0,80.0,1.0)
        prev = p3.number_input("Previous score",0.0,100.0,65.0,1.0)
        estimate = float(model.predict(pd.DataFrame([[hours,att,prev]],columns=features))[0])
        st.success(f"Predicted student score: {np.clip(estimate,0,100):.2f} / 100")
        coef = pd.DataFrame({"Feature":features,"Coefficient":model.coef_})
        st.dataframe(coef,use_container_width=True)
    else:
        st.info("At least 10 complete rows are required to train the Linear Regression model.")

st.caption("Note: The included CSV is synthetic demonstration data. Use your institution's anonymized data for real project analysis.")
