import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Gujarat Student Dropout Decision Support System",
    layout="wide"
)

# LOAD DATA
df = pd.read_csv("student_risk_dashboard(1).csv")

st.title("🎓 Gujarat School Dropout Decision Support System")
st.markdown(
"""
This dashboard helps education officers identify:
- Which students are at high risk of dropping out
- Where the risk is concentrated (District / School / Area)
- Why the risk is occurring
- What immediate intervention is required
"""
)

# SIDEBAR NAVIGATION
menu = st.sidebar.radio(
    "Select Dashboard View",
    ["🏠 State Overview",
     "📍 District Analysis",
     "🏫 School Analysis",
     "👧 Gender & Social Group",
     "🚨 Intervention Required"]
)

# ---------------- STATE OVERVIEW ---------------- #
if menu=="🏠 State Overview":

    st.header("State Level Situation")

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Students",len(df))
    col2.metric("High Risk Students",
                len(df[df["Risk_Category"]=="High"]))
    col3.metric("Immediate Intervention Required",
                len(df[df["Priority_Level"]=="Immediate"]))

    st.progress(
        len(df[df["Risk_Category"]=="High"])/len(df)
    )

    st.subheader("Districts with Highest Dropout Risk")
    st.bar_chart(df.groupby('District')['Risk_Score'].mean())

    st.subheader("Risk by Area Type")
    st.bar_chart(df.groupby('Area_Type')['Risk_Score'].mean())

    st.subheader("Risk by Academic Standard")
    st.bar_chart(df.groupby('Standard')['Risk_Score'].mean())

# ---------------- DISTRICT ---------------- #
elif menu=="📍 District Analysis":

    district = st.selectbox(
        "Select District",
        df['District'].unique()
    )

    ddf = df[df['District']==district]

    st.subheader(f"Dropout Risk in {district}")

    st.bar_chart(ddf.groupby('School_ID')['Risk_Score'].mean())
    st.bar_chart(ddf.groupby('Gender')['Risk_Score'].mean())
    st.bar_chart(ddf.groupby('Caste_Category')['Risk_Score'].mean())
    st.bar_chart(ddf.groupby('Standard')['Risk_Score'].mean())

    st.subheader("Students Requiring Immediate Support")

    high = ddf[ddf["Priority_Level"]=="Immediate"]

    st.dataframe(high[
    ['Student_ID','School_ID','Area_Type',
     'Gender','Caste_Category','Standard',
     'Dropout_Reason','Recommended_Action']
    ])

# ---------------- SCHOOL ---------------- #
elif menu=="🏫 School Analysis":

    school = st.selectbox(
        "Select School",
        df['School_ID'].unique()
    )

    sdf = df[df['School_ID']==school]

    st.bar_chart(sdf.groupby('Area_Type')['Risk_Score'].mean())
    st.bar_chart(sdf.groupby('Gender')['Risk_Score'].mean())
    st.bar_chart(sdf.groupby('Caste_Category')['Risk_Score'].mean())
    st.bar_chart(sdf.groupby('Standard')['Risk_Score'].mean())

    st.subheader("Students Needing Immediate Action")

    high = sdf[sdf["Priority_Level"]=="Immediate"]

    st.dataframe(high[
    ['Student_ID','Gender','Standard',
     'Dropout_Reason','Recommended_Action']
    ])

# ---------------- GENDER & CASTE ---------------- #
elif menu=="👧 Gender & Social Group":

    st.bar_chart(df.groupby('Gender')['Risk_Score'].mean())
    st.bar_chart(df.groupby('Caste_Category')['Risk_Score'].mean())

# ---------------- POLICY ---------------- #
elif menu=="🚨 Intervention Required":

    st.subheader("Transport Support Needed")

    st.dataframe(df[
    (df['Transport_Available']=="No") &
    (df['Priority_Level']=="Immediate")
    ][
    ['Student_ID','District','School_ID',
     'Standard','Recommended_Action']
    ])

    st.subheader("Scholarship Support Needed")

    st.dataframe(df[
    (df['Scholarship_Status']=="No") &
    (df['Priority_Level']=="Immediate")
    ][
    ['Student_ID','District','School_ID',
     'Standard','Recommended_Action']
    ])

    st.subheader("Academic Counselling Needed")

    st.dataframe(df[
    (df['Dropout_Reason']=="Academic Disengagement") &
    (df['Priority_Level']=="Immediate")
    ][
    ['Student_ID','District','School_ID',
     'Standard','Recommended_Action']
    ])