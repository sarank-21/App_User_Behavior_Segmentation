import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")
from sqlalchemy import create_engine,text
import mysql.connector
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="App User Behavior Segmentation",
    page_icon="🎯",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
@st.cache_resource
def setup_database():
    engine = create_engine("mysql+mysqlconnector://root:0007@localhost")

    with engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS User_Behavior_Segmentation"))
        conn.commit()

    db_engine = create_engine("mysql+mysqlconnector://root:0007@localhost/User_Behavior_Segmentation")

    # Create table only once
    with db_engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS User_Behavior_Details(
               user_id INT PRIMARY KEY, 
               age INT, 
               gender VARCHAR(50), 
               country VARCHAR(50), 
               device_type VARCHAR(50), 
               app_version DECIMAL(5,2),
               sessions_per_week INT, 
               avg_session_duration_min DECIMAL(10,2), 
               daily_active_minutes DECIMAL(10,2),
               feature_clicks_per_session INT, 
               notifications_opened_per_week DECIMAL(10,2),
               in_app_search_count INT, 
               pages_viewed_per_session INT,
               crash_events_last_30_days DECIMAL(10,2),
               support_tickets_raised INT,
               days_since_last_login INT, 
               subscription_type VARCHAR(50),
               ads_clicked_last_30_days INT, 
               content_downloads INT, 
               social_shares INT,
               rating_given DECIMAL(5,1), 
               churn_risk_score DECIMAL(10,2),
               engagement_score DECIMAL(10,2),
               account_age_days INT, 
               marketing_source VARCHAR(50), 
               cluster INT, 
               segment VARCHAR(50)
                      )"""))
        conn.commit()
        return db_engine
db_engine = setup_database()
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\PROJECTS\Capstone_Project_4\App_User_Behavior_Segmentation\app_user_behavior_dataset.csv")
    return df


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

def App_user_Data_Cleaning(df):

    app_df = df.copy()

    app_df['rating_given'] = app_df['rating_given'].fillna(app_df['rating_given'].median())
        
    def Outlier_Detection(df, numerical_cols_clip):
        # Capping Outliers
        for col in numerical_cols_clip:
            Q1 = np.percentile(df[col], 25)
            Q3 = np.percentile(df[col], 75)
            
            IQR = Q3 - Q1
            lower_bound = Q1 - (1.5 * IQR)
            upper_bound = Q3 + (1.5 * IQR)
            
            df[col] = np.clip(df[col], lower_bound, upper_bound)
            
        return df
    Numerical_label_clip=["sessions_per_week","avg_session_duration_min",
                          "feature_clicks_per_session","notifications_opened_per_week","in_app_search_count",
                          "crash_events_last_30_days","ads_clicked_last_30_days","content_downloads",
                          "social_shares","daily_active_minutes","engagement_score"]
    
    clean_app_df = Outlier_Detection(app_df,Numerical_label_clip)

    clean_app_df.reset_index(drop=True, inplace=True)

    return clean_app_df


# --------------------------------------------------
# MODEL TRAINING
# --------------------------------------------------

def ML_model(Data):

    ML_App_df = Data.copy()

    # Fix 1: Use only the 3 strongest behavioral signals
    best_cols = [
        'sessions_per_week', 'avg_session_duration_min',
        'daily_active_minutes', 'feature_clicks_per_session',
        'notifications_opened_per_week', 'in_app_search_count',
        'pages_viewed_per_session', 'crash_events_last_30_days',
        'support_tickets_raised', 'days_since_last_login',
        'ads_clicked_last_30_days', 'content_downloads', 'social_shares',
        'rating_given', 'churn_risk_score', 'engagement_score',
        'account_age_days'
        ]
    X = ML_App_df[best_cols].copy()
    
    # Fix 2: Scale first
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    km = KMeans(n_clusters=2, random_state=42, n_init=20,max_iter=500)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)

    ML_App_df['cluster'] = labels

    cluster_names = {
         0: 'Casual Users',
         1: 'Power Users'
        }
    
    ML_App_df['segment'] = ML_App_df['cluster'].map(cluster_names)

    return ML_App_df
# --------------------------------------------------
# PIPELINE (CACHED)
# --------------------------------------------------

@st.cache_data
def get_model_pipeline():
    raw_df = load_data()
    App_user_df = App_user_Data_Cleaning(raw_df)
    final = ML_model(App_user_df)

    return final


# ✅ Call ONLY ONCE
final_df = get_model_pipeline()

# --------------------------------------------------
# INSERT ONLY ONCE
# --------------------------------------------------

if "data_inserted" not in st.session_state:

    count = pd.read_sql(
        "SELECT COUNT(*) AS cnt FROM User_Behavior_Details",
        db_engine
    ).iloc[0, 0]

    if count == 0:
        final_df.to_sql(
            "User_Behavior_Details",
            db_engine,
            if_exists="append",
            index=False
        )

    st.session_state.data_inserted = True

def css_Button():
    st.markdown("""
                <style>
                /* Main select container */
                div[data-testid="stSelectbox"] > div {
                background-color: #f0f2f6;
                border-radius: 15px;
                padding: 6px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                transition: 0.3s;
                }
                
                /* Hover effect */
                div[data-testid="stSelectbox"] > div:hover {
                transform: translateY(-3px);
                box-shadow: 0px 8px 18px rgba(0,0,0,0.15);
                }
                /* Selected text */
                div[data-testid="stSelectbox"] span {
                font-size: 16px;
                font-weight: 500;
                color: #1f77b4;
                }
                
                /* Dropdown arrow */
                div[data-testid="stSelectbox"] svg {
                color: #1f77b4;
                }
                /* 🔷 Apply KPI card style to buttons */
                div.stButton > button {
                background-color: #f0f2f6;
                padding: 25px;
                border-radius: 25px;
                text-align: center;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                height: 50px;
                width: 195px;
                font-size: 22px;
                font-weight: bold;
                color: #1f77b4;
                border: none;
                }
                div.stButton > button p {
                font-size: 15px !important;
                font-weight: bold!important;
                }
                /* 🔥 Hover effect same as KPI */
                
                div.stButton > button:hover {
                transform: translateY(-8px);
                box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
                background-color: #e8f0fe;
                color: #1f77b4;
                }
                /* Remove default focus outline */
                div.stButton > button:focus {
                outline: none;
                box-shadow: none;
                }               
                </style>
                """, unsafe_allow_html=True)
# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if st.session_state.page == "home":
    st.markdown("""
<style>

/* 🔷 Apply KPI card style to buttons */
div.stButton > button {
    background-color: #f0f2f6;
    padding: 25px;
    border-radius: 25px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    transition: all 0.3s ease;

    height: 75px;
    width: 200px;

    font-size: 22px;
    font-weight: bold;
    color: #1f77b4;
    border: none;
}
    div.stButton > button p {
    font-size: 22px !important;
    font-weight: bold!important;
}

/* 🔥 Hover effect same as KPI */
div.stButton > button:hover {
    transform: translateY(-8px);
    box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
    background-color: #e8f0fe;
    color: #1f77b4;
}

/* Remove default focus outline */
div.stButton > button:focus {
    outline: none;
    box-shadow: none;
}

</style>
""", unsafe_allow_html=True)

    st.title("🎯 App User Behavior Segmentation")
    
    if st.button("📶 Analysis"):
        st.session_state.page = "Analysis"
        st.rerun()
        
    st.subheader("Dataset Overview")
    query = """ SELECT * from user_behavior_details"""
        
    df = pd.read_sql(query, db_engine)
    st.dataframe(df, use_container_width=True)

    fig = px.pie(
        final_df,
        names="segment",
        title="Segment Distribution"
    )

    fig.update_layout(title_x=0.3,title_font=dict(size=40),
                          width=500,     # increase width
                          height=550  ,    # increase height
                              hoverlabel=dict(
                              bgcolor="#5EFABE",
                              font_size=14,
                              font_color="black"))
    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
#  Analysis
# --------------------------------------------------
elif st.session_state.page == "Analysis":
    
    css_Button()

    st.title("App User Behavior Segmentation Analysis")
    query = """ select sessions_per_week, avg_session_duration_min,
        daily_active_minutes, feature_clicks_per_session,
        notifications_opened_per_week, in_app_search_count,
        pages_viewed_per_session, crash_events_last_30_days,
        support_tickets_raised, days_since_last_login,
        ads_clicked_last_30_days, content_downloads, social_shares,
        rating_given, churn_risk_score, engagement_score,
        account_age_days,cluster,segment from user_behavior_details;"""
        
    df = pd.read_sql(query, db_engine)
    st.dataframe(df, use_container_width=True)

    topic = st.selectbox(
            "Select Analysis",
            [
                "Select Analysis",
                "Cluster-wise User Identification",
                "Customer Distribution per Segment",
                "Behavioral Analysis per Segment",
                "Segment-wise Deep Dive",
                "Country Wise Segment Analysis",
                "Device type Segment Analysis",
                "Subscription type Segment Analysis"
                ])
    if  topic == "Cluster-wise User Identification":
        st.session_state.page = "Cluster-wise User Identification"

    elif topic == "Customer Distribution per Segment":
        st.session_state.page = "Customer Distribution per Segment"

    elif topic == "Behavioral Analysis per Segment": 
        st.session_state.page = "Behavioral Analysis per Segment"

    elif topic == "Segment-wise Deep Dive":
        st.session_state.page = "Segment-wise Deep Dive"

    elif topic == "Country Wise Segment Analysis":
        st.session_state.page = "Country Wise Segment Analysis"

    elif topic == "Device type Segment Analysis" :
        st.session_state.page ="Device type Segment Analysis"

    elif topic == "Subscription type Segment Analysis" :
        st.session_state.page ="Subscription type Segment Analysis"

    if topic != "Select Analysis":
        st.rerun()

    elif st.button("⬅ Back to Dashboard"):
        st.session_state.page = "home"
        st.rerun()

# ----------------------------------------------
#  Cluster-wise User Identification Analysis
# ----------------------------------------------
elif st.session_state.page == "Cluster-wise User Identification":
    css_Button()
    
    st.header("Cluster-wise User Identification")
    
    query = """ SELECT user_id, segment 
    FROM user_behavior_details;"""
        
    df = pd.read_sql(query, db_engine)
    st.dataframe(df, use_container_width=True)

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Analysis"
        st.rerun()

# ----------------------------------------------
# Customer Distribution per Segment Analysis
# ----------------------------------------------
elif st.session_state.page == "Customer Distribution per Segment":
    css_Button()

    st.header("Customer Distribution per Segment")
    query = """
    SELECT COUNT(*) AS total_users, segment  
    FROM user_behavior_details
    GROUP BY segment order by total_users; """
        
    df = pd.read_sql(query, db_engine)
    st.dataframe(df, use_container_width=True)
    fig = px.bar(data_frame=df,x="segment",y="total_users",color="segment",
                 title= "Users Wise Segment ")
    fig.update_layout(title_x=0.25,title_font=dict(size=30),
                    width=500,     # increase width
                    height=550,    # increase height
                    hoverlabel=dict(
                    bgcolor="#5EFABE",
                    font_size=14,
                    font_color="black"))
    st.plotly_chart(fig,use_container_width=True)
    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Analysis"
        st.rerun()

# ----------------------------------------------
#  Behavioral Analysis per Segment Analysis
# ----------------------------------------------

elif st.session_state.page == "Behavioral Analysis per Segment":
    css_Button()
    st.header("Behavioral Analysis per Segment")
    query ="""SELECT 
            AVG(engagement_score) AS avg_engagement,
            AVG(daily_active_minutes) AS avg_daily_usage,
            AVG(churn_risk_score) AS avg_churn_risk,
            segment 
            FROM user_behavior_details
            GROUP BY segment order by avg_churn_risk;"""
                
    df = pd.read_sql(query, db_engine)
    st.dataframe(df, use_container_width=True)
    fig1 = go.Figure(data=[go.Pie(labels=df["segment"], values=df["avg_engagement"], pull=[0, 0, 0, 0.1])])
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    fig1.update_layout(title=dict(text="Segment VS Engagement",x=0.4, xanchor="center"),title_font=dict(size=25),
                        width=600,     # increase width
                        height=500  ,    # increase height
                        hoverlabel=dict(
                        bgcolor="#9325FB",   # Background color
                        font_size=14,
                        font_color="white"))
    fig2 = px.pie(data_frame=df,values="avg_daily_usage",names="segment",
                 title="Segment VS App Daily Usage",hole=0.5,color_discrete_sequence=px.colors.sequential.RdBu)
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(title_x=0.1,title_font=dict(size=25),
                        width=600,     # increase width
                        height=500  ,    # increase height
                        hoverlabel=dict(
                        bgcolor="#9325FB",   # Background color
                        font_size=14,
                        font_color="white"))
    col1,col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1,use_container_width=False)
    with col2:
        st.plotly_chart(fig2,use_container_width=False)
    fig3 = px.bar(data_frame=df,x="segment",y="avg_churn_risk",color="segment",title= "Segment Vs Churn Risk")
                
    fig3.update_layout(title_x=0.4,title_font=dict(size=40),
                        width=500,     # increase width
                        height=550  ,    # increase height
                        hoverlabel=dict(
                        bgcolor="#5EFABE",
                        font_size=14,
                        font_color="black"))
    st.plotly_chart(fig3,use_container_width=True)

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Analysis"
        st.rerun()
# ----------------------------------------------
#  Segment-wise Deep Dive Analysis
# ----------------------------------------------

elif st.session_state.page == "Segment-wise Deep Dive":
    css_Button()

    st.header("Segment-wise Deep Dive Analysis")

    
    fig = px.scatter(final_df,
    x="engagement_score",
    y="churn_risk_score",
    color="segment",
    title="User Segmentation"
    )
    st.plotly_chart(fig, use_container_width=True)

    topic = st.selectbox(
            "Select Analysis",
            [
                "Select Analysis",
                "Casual Users",
                "Power Users"
                ])
    
    if topic == "Casual Users":
        st.subheader("Segment 1 - Casual Users")
        query = """
            SELECT * 
            FROM user_behavior_details
            WHERE segment = "Casual Users"; """
        
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

    if topic == "Power Users":
        st.subheader("Segment 2 - Power Users")
        query = """
            SELECT * FROM user_behavior_details
            WHERE segment = "Power Users"; """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Analysis"
        st.rerun()

# ----------------------------------------------
#  Country Wise Segment Analysis
# ----------------------------------------------

elif st.session_state.page == "Country Wise Segment Analysis":
    css_Button()
    
    st.header("Country Wise Segment Analysis")
    
    query = """ SELECT count(*) as Total_segment ,country, 
    segment from user_behavior_details 
    group by country,segment order by Total_segment;"""
        
    df = pd.read_sql(query, db_engine)
    st.dataframe(df, use_container_width=True)

    fig = px.sunburst(df,path=["country", "segment"],values="Total_segment",title="Country Wise Segment Analysis",)
    fig.update_traces(textinfo="label+percent parent",textfont_size=15)
    fig.update_layout(title_x=0.25,title_font=dict(size=40),
                        width=1200,     # increase width
                        height=800 ,    # increase height
                        hoverlabel=dict(
                        bgcolor="#9325FB",   # Background color
                        font_size=14,
                        font_color="white"))
    st.plotly_chart(fig, use_container_width=True)

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Analysis"
        st.rerun()

# ----------------------------------------------
#  Device type  Segment Analysis
# ----------------------------------------------

elif st.session_state.page == "Device type Segment Analysis":
    css_Button()
    
    st.header("Device type Segment Analysis")
    
    query = """ SELECT count(*) as Total_segment ,device_type, 
    segment from user_behavior_details group by device_type,
    segment order by Total_segment;"""
        
    df = pd.read_sql(query, db_engine)
    st.dataframe(df, use_container_width=True)
    
    fig = px.bar(data_frame=df,x="segment",y="Total_segment", text="Total_segment",color="device_type",
                 barmode="group",title= "Device type Segment Analysis")
    fig.update_traces(textposition='outside')        
    fig.update_layout(title_x=0.4,title_font=dict(size=40),
                        width=500,     # increase width
                        height=550  ,    # increase height
                        hoverlabel=dict(
                        bgcolor="#5EFABE",
                        font_size=14,
                        font_color="black"))
    st.plotly_chart(fig,use_container_width=True)


    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Analysis"
        st.rerun()

# ----------------------------------------------
#  Subscription type  Segment Analysis
# ----------------------------------------------

elif st.session_state.page == "Subscription type Segment Analysis":
    css_Button()
    st.header("Subscription type Segment Analysis")
    
    query = """ SELECT count(*) as Total_segment ,subscription_type, 
    segment from user_behavior_details group by subscription_type,
    segment order by Total_segment;"""
        
    df = pd.read_sql(query, db_engine)
    st.dataframe(df, use_container_width=True)
    
    fig = px.bar(data_frame=df,x="Total_segment",y="segment", text="Total_segment",color="subscription_type",
                  orientation='h',barmode="group",title= "Subscription type Segment Analysis")
    fig.update_traces(textposition='outside')        
    fig.update_layout(title_x=0.32,title_font=dict(size=40),
                        width=500,     # increase width
                        height=550  ,    # increase height
                        hoverlabel=dict(
                        bgcolor="#5EFABE",
                        font_size=14,
                        font_color="black"))
    st.plotly_chart(fig,use_container_width=True)


    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "Analysis"
        st.rerun()

