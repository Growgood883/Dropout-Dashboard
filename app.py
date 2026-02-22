import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv("student_risk_output.csv")

st.title("🎓 Student Dropout Early Warning System")

# Sidebar Filter
st.sidebar.header("Filter Students")

risk_filter = st.sidebar.selectbox(
    "Select Risk Category",
    ["All","Low","Medium","High"]
)

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

fig,ax = plt.subplots()
ax.bar(risk_counts.index,risk_counts.values)
st.pyplot(fig)

# High Risk Students Table
st.subheader("🚨 High Risk Students")

st.dataframe(df[df["Alert_Flag"]=="YES"])