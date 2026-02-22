import streamlit as st
import pandas as pd

# Page Title
st.title("🎓 Student Dropout Early Warning System")

# Load Dataset
df = pd.read_csv("student_risk_dashboard.csv")

# Sidebar Filter
st.sidebar.header("Filter Students")

risk_filter = st.sidebar.selectbox(
    "Select Risk Category",
    ["All","Low","Medium","High"]
)

# Apply Filter
if risk_filter!="All":
    df = df[df["Risk_Category"]==risk_filter]

# KPI Section
st.subheader("Overall Statistics")

col1,col2,col3 = st.columns(3)

col1.metric("Total Students",len(df))
col2.metric("High Risk Students",
            len(df[df["Risk_Category"]=="High"]))
col3.metric("Alert Students",
            len(df[df["Alert_Flag"]=="YES"]))

# Risk Distribution Graph
st.subheader("Risk Distribution")

risk_counts = df["Risk_Category"].value_counts()

st.bar_chart(risk_counts)

# High Risk Students Table
st.subheader("🚨 High Risk Students Details")

high_risk = df[df["Alert_Flag"]=="YES"]

st.dataframe(high_risk[
['Student_ID',
 'School_ID',
 'Area_Type',
 'Gender',
 'Caste_Category',
 'Standard',
 'Risk_Score']
])