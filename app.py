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

st.title("🎓 Gujarat School Dropout Decision Support System")

st.markdown("""
This system helps officers to:
- Identify students at dropout risk
- Detect affected districts / schools
- Understand reason of risk
- Take recommended intervention action
""")

# ---------------- STATE DASHBOARD ---------------- #
def state_dashboard(df):

    st.header("📊 State Overview")

    c1,c2,c3 = st.columns(3)

    c1.metric("Total Students",len(df))
    c2.metric("High Risk Students",
              len(df[df["Risk_Category"]=="High"]))
    c3.metric("Immediate Intervention",
              len(df[df["Priority_Level"]=="Immediate"]))

    dist = df.groupby('District')['Risk_Score'].mean().reset_index()

    fig = px.bar(
        dist,
        x='District',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig,use_container_width=True)

    area = df.groupby('Area_Type')['Risk_Score'].mean().reset_index()

    fig2 = px.bar(
        area,
        x='Area_Type',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig2,use_container_width=True)

    std = df.groupby('Standard')['Risk_Score'].mean().reset_index()

    fig3 = px.bar(
        std,
        x='Standard',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig3,use_container_width=True)

# ---------------- DISTRICT DASHBOARD ---------------- #
def district_dashboard(df):

    st.header("📍 District Analysis")

    district = st.selectbox(
        "Select District",
        df['District'].unique()
    )

    ddf = df[df['District']==district]

    sch = ddf.groupby('School_ID')['Risk_Score'].mean().reset_index()

    fig4 = px.bar(
        sch,
        x='School_ID',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig4,use_container_width=True)

    support = ddf[
        (ddf["Risk_Category"]=="High") |
        (ddf["Risk_Category"]=="Medium")
    ]

    st.subheader("Students Needing Immediate Support")

    st.dataframe(
        support[
            ['Student_ID','School_ID','Area_Type',
             'Gender','Caste_Category','Standard',
             'Risk_Category',
             'Dropout_Reason','Recommended_Action']
        ]
    )

# ---------------- SCHOOL DASHBOARD ---------------- #
def school_dashboard(df):

    st.header("🏫 School Analysis")

    school = st.selectbox(
        "Select School",
        df['School_ID'].unique()
    )

    sdf = df[df['School_ID']==school]

    gen = sdf.groupby('Gender')['Risk_Score'].mean().reset_index()

    fig5 = px.bar(
        gen,
        x='Gender',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig5,use_container_width=True)

    caste = sdf.groupby('Caste_Category')['Risk_Score'].mean().reset_index()

    fig6 = px.bar(
        caste,
        x='Caste_Category',
        y='Risk_Score',
        color='Risk_Score',
        color_continuous_scale='RdYlGn_r'
    )

    st.plotly_chart(fig6,use_container_width=True)

    support = sdf[
        (sdf["Risk_Category"]=="High") |
        (sdf["Risk_Category"]=="Medium")
    ]

    st.subheader("Students Requiring Immediate Action")

    st.dataframe(
        support[
            ['Student_ID','Gender','Standard',
             'Risk_Category',
             'Dropout_Reason','Recommended_Action']
        ]
    )

# ---------------- INTERVENTION ---------------- #
def intervention_dashboard(df):

    st.header("🚨 Policy Intervention Required")

    st.subheader("Transport Support Needed")

    transport = df[
        (df['Transport_Available']=="No") &
        (df['Risk_Category']!="Low")
    ]

    st.dataframe(
        transport[
            ['Student_ID','District','School_ID',
             'Standard','Risk_Category',
             'Recommended_Action']
        ]
    )

    st.subheader("Scholarship Support Needed")

    sch = df[
        (df['Scholarship_Status']=="No") &
        (df['Risk_Category']!="Low")
    ]

    st.dataframe(
        sch[
            ['Student_ID','District','School_ID',
             'Standard','Risk_Category',
             'Recommended_Action']
        ]
    )

    st.subheader("Academic Counselling Needed")

    coun = df[
        (df['Dropout_Reason']=="Academic Disengagement") &
        (df['Risk_Category']!="Low")
    ]

    st.dataframe(
        coun[
            ['Student_ID','District','School_ID',
             'Standard','Risk_Category',
             'Recommended_Action']
        ]
    )

# ---------------- MENU ---------------- #
menu = st.sidebar.radio(
    "Select Dashboard View",
    ["🏠 State Overview",
     "📍 District Analysis",
     "🏫 School Analysis",
     "🚨 Intervention Required"]
)

if menu=="🏠 State Overview":
    state_dashboard(df)

elif menu=="📍 District Analysis":
    district_dashboard(df)

elif menu=="🏫 School Analysis":
    school_dashboard(df)

elif menu=="🚨 Intervention Required":
    intervention_dashboard(df)