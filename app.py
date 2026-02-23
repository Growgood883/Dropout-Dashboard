import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Gujarat Student Dropout DSS",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_data():
    return pd.read_csv("student_risk_dashboard.csv")

df = load_data()

# ---------------- TITLE ---------------- #
st.title("🎓 Gujarat School Dropout Decision Support System")

st.markdown("""
This system helps education officers to:
- Identify students at high risk of dropping out
- Detect which district or school needs intervention
- Understand WHY dropout risk is occurring
- Take immediate action using Recommended Policy Support
""")

# ---------------- NAVIGATION ---------------- #
menu = st.sidebar.radio(
    "Select Dashboard View",
    ["🏠 State Overview",
     "📍 District Analysis",
     "🏫 School Analysis",
     "👧 Gender & Social Group",
     "🚨 Intervention Required"]
)

# ---------------- OVERVIEW ---------------- #
if menu=="🏠 State Overview":

    st.header("📊 Gujarat State Situation")

    c1,c2,c3 = st.columns(3)

    c1.metric("Total Students",len(df))
    c2.metric("High Risk Students",
              len(df[df["Risk_Category"]=="High"]))
    c3.metric("Immediate Intervention",
              len(df[df["Priority_Level"]=="Immediate"]))

    st.subheader("Dropout Risk by District")

    dist = df.groupby('District')['Risk_Score'].mean().reset_index()

    fig = px.bar(
        dist,
        x='District',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("Dropout Risk by Area Type")

    area = df.groupby('Area_Type')['Risk_Score'].mean().reset_index()

    fig2 = px.bar(
        area,
        x='Area_Type',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig2,use_container_width=True)

    st.subheader("Risk by Academic Standard")

    std = df.groupby('Standard')['Risk_Score'].mean().reset_index()

    fig3 = px.line(
        std,
        x='Standard',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig3,use_container_width=True)

# ---------------- DISTRICT ---------------- #
elif menu=="📍 District Analysis":

    district = st.selectbox(
        "Select District",
        df['District'].unique()
    )

    ddf = df[df['District']==district]

    st.subheader(f"Dropout Risk in {district}")

    sch = ddf.groupby('School_ID')['Risk_Score'].mean().reset_index()

    fig4 = px.bar(
        sch,
        x='School_ID',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig4,use_container_width=True)

    st.subheader("Students Needing Immediate Support")

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

    st.subheader("Gender-wise Risk")

    gen = sdf.groupby('Gender')['Risk_Score'].mean().reset_index()

    fig5 = px.bar(
        gen,
        x='Gender',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig5,use_container_width=True)

    st.subheader("Caste-wise Risk")

    caste = sdf.groupby('Caste_Category')['Risk_Score'].mean().reset_index()

    fig6 = px.bar(
        caste,
        x='Caste_Category',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig6,use_container_width=True)

    st.subheader("Students Requiring Immediate Action")

    high = sdf[sdf["Priority_Level"]=="Immediate"]

    st.dataframe(high[
    ['Student_ID','Gender','Standard',
     'Dropout_Reason','Recommended_Action']
    ])

# ---------------- SOCIAL ---------------- #
elif menu=="👧 Gender & Social Group":

    g = df.groupby('Gender')['Risk_Score'].mean().reset_index()

    fig7 = px.bar(
        g,
        x='Gender',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig7,use_container_width=True)

    c = df.groupby('Caste_Category')['Risk_Score'].mean().reset_index()

    fig8 = px.bar(
        c,
        x='Caste_Category',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig8,use_container_width=True)

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