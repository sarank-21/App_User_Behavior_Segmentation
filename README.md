# 📲 App User Behavior Segmentation System

## 📖 About the Project

The **App User Behavior Segmentation System** is an end-to-end Unsupervised Machine Learning and data analytics application that segments mobile app users into meaningful behavioral clusters. It combines data preprocessing, unsupervised machine learning, database integration, and interactive dashboards using Streamlit.

The system helps product managers, growth teams, and app developers make **data-driven retention and engagement decisions** by analyzing user activity patterns, churn risk scores, and behavioral signals.

---

## 🔨 Development Process

### 1. Data Collection
Imported an App User Behavior dataset containing user demographics, session activity, engagement metrics, notification interactions, device details, and subscription information.

### 2. Data Cleaning & Preprocessing
- Handled missing values using **median imputation** (e.g., `rating_given`)
- Detected and treated outliers using the **IQR method**:
  - **Capping** applied to session, click, notification, and crash-related columns
  - **Removal** applied to daily_active_minutes and engagement_score

### 3. Feature Selection
Identified the **3 strongest behavioral signals** for clustering:
- `engagement_score`
- `churn_risk_score`
- `daily_active_minutes`

### 4. Data Transformation
- Scaled numerical features using **StandardScaler** before clustering to ensure equal feature contribution

### 5. Model Building
- Applied **KMeans Clustering** with 4 clusters (`n_clusters=4`, `n_init=10`, `random_state=42`)
- Evaluated cluster quality using the **Silhouette Score**

### 6. Cluster Labeling
Mapped cluster IDs to meaningful business segment names:

| Cluster | Segment Name       | Description                                    |
|---------|--------------------|------------------------------------------------|
| 0       | At Risk Users      | High engagement but high churn — about to leave |
| 1       | High Churn Risk    | Low engagement + high churn — already disengaged |
| 2       | Casual Users       | Decent engagement, low churn, lower daily use  |
| 3       | Loyal Active Users | Most active daily + lowest churn — best users  |

### 7. Database Integration
- Connected to **MySQL** using **SQLAlchemy**
- Created the `User_Behavior_Segmentation` database and `User_Behavior_Details` table dynamically
- Stored the fully processed and segmented dataset for SQL-based analysis

### 8. Dashboard Development
- Built an interactive UI using **Streamlit**
- Designed KPI-styled navigation buttons and multi-page flow
- Added **custom CSS** for hover effects, styled selectboxes, and button animations

### 9. Visualization & Analysis
Used **Plotly** to create:
- Pie charts (segment distribution, engagement, daily usage)
- Bar charts (user count per segment, churn risk, device type, subscription type)
- Sunburst charts (country-wise segment breakdown)
- Scatter plots (engagement vs churn risk by segment)

Enabled multiple analytical views:
- Cluster-wise user identification
- Customer distribution per segment
- Behavioral analysis per segment
- Segment-wise deep dive
- Country, device, and subscription type analysis

### 10. Performance Optimization
Implemented caching using Streamlit:
```python
@st.cache_data
@st.cache_resource
```
Reduced re-computation and improved speed for data loading and model pipeline.

---

## ✨ Key Features

### 🔎 Real-Time User Segmentation
Automatically clusters app users into 4 behavioral segments using KMeans and key engagement signals.

### 📊 Interactive Multi-Page Dashboard
Provides dynamic visualizations and drill-down insights through an intuitive Streamlit interface.

### 🧠 Machine Learning Integration
Utilizes **KMeans Clustering** with **StandardScaler** for accurate and reproducible user grouping.

### 📉 Churn Risk Identification
Surfaces **High Churn Risk** and **At Risk** users to enable proactive retention strategies.

### 🧹 Automated Data Preprocessing
Handles missing values and outliers using IQR-based capping and removal strategies.

### 🗄️ Database Integration (MySQL)
Stores segmented data for scalable querying and SQL-powered analytical reporting.

### 📊 Advanced Visualizations
Includes pie charts, bar charts, sunburst charts, and scatter plots using Plotly Express and Graph Objects.

### 🎨 Custom UI/UX Design
Enhanced user experience with custom CSS styling for buttons, selectboxes, KPI cards, and hover animations.

### ⚡ Optimized Performance
Uses Streamlit caching to reduce computation time and improve responsiveness on every page load.

### 🔄 Multi-Page Navigation System
Smooth navigation between:
- 🏠 Home (Dataset Overview + Segment Distribution)
- 📶 Analysis Hub (7 analytical views)

---

## 🎯 Features

### 🧾 Dataset Overview
Displays the full processed and segmented dataset on the home page for immediate visibility.

### 🔮 Segment Distribution Pie Chart
Interactive pie chart showing the proportional distribution of all 4 user segments.

### 👥 Cluster-wise User Identification
Lists every user along with their assigned segment for individual-level tracking.

### 📊 Customer Distribution per Segment
Bar chart showing total user counts across segments for volume comparison.

### 🧠 Behavioral Analysis per Segment
Side-by-side comparison of:
- Average engagement score (pie chart)
- Average daily active minutes (donut chart)
- Average churn risk (bar chart)

### 🔍 Segment-wise Deep Dive
Scatter plot of engagement vs churn risk colored by segment, with filterable tables for each of the 4 segments.

### 🌍 Country Wise Segment Analysis
Sunburst chart showing segment distribution broken down by country for geographic insights.

### 📱 Device Type Segment Analysis
Grouped bar chart showing how segments are distributed across device types (iOS, Android, Web, etc.).

### 💳 Subscription Type Segment Analysis
Horizontal grouped bar chart showing segment behavior by subscription tier (Free, Premium, etc.).

### 🗃️ Database-Driven Insights
All analysis pages query the MySQL database in real time for consistent, live reporting.

### 🎨 Interactive UI Experience
- Styled selectboxes with hover lift effects
- KPI-styled navigation buttons with smooth transitions
- Back-to-dashboard navigation on every page

### ⚡ Efficient Data Processing
- Optimized ML pipeline with `@st.cache_resource`
- One-time database insertion using `st.session_state` flags

---

## ⚙️ Tech Stack

### 🖥️ Frontend / UI
- **Streamlit** – Interactive web application framework for building dashboards
- **HTML/CSS (Custom Styling)** – Enhances UI components like buttons, selectboxes, and KPI-style cards

### 🧠 Machine Learning
- **Scikit-learn** – Model building, training, and evaluation
- **KMeans Clustering** – Core unsupervised segmentation algorithm
- **StandardScaler** – Feature normalization before clustering
- **Silhouette Score** – Cluster quality evaluation metric

### 📊 Data Processing & Analysis
- **Pandas** – Data manipulation and SQL query result handling
- **NumPy** – Numerical computations and IQR-based outlier detection

### 📈 Data Visualization
- **Plotly Express** – Quick interactive charts (bar, pie, scatter, sunburst)
- **Plotly Graph Objects** – Fine-grained control over chart styling

### 🗄️ Database
- **MySQL** – Data storage and SQL-based querying
- **SQLAlchemy** – Database connection and engine management
- **MySQL Connector** – Python-MySQL driver integration

### ⚙️ Backend / Core Logic
- **Python** – Core programming language for the entire application

### 🚀 Deployment & Optimization
**Streamlit Caching**
- `@st.cache_data` – Optimizes CSV data loading
- `@st.cache_resource` – Optimizes ML pipeline and database connection

### 🛠️ Development Tools
- **Jupyter Notebook / VS Code** – Development and experimentation
- **Git & GitHub** – Version control and project collaboration

---

## ⚙️ Setup & Installation

Follow these steps to run the App User Behavior Segmentation System locally:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/App-User-Behavior-Segmentation.git
cd App-User-Behavior-Segmentation
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv

# Activate the environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

Key libraries included:
- `streamlit`
- `pandas`, `numpy`
- `scikit-learn`
- `plotly`
- `sqlalchemy`, `mysql-connector-python`

### 4️⃣ Setup MySQL Database
Ensure MySQL is installed and running locally.

Default connection in code:
```
mysql+mysqlconnector://root:0007@localhost/User_Behavior_Segmentation
```

The app automatically creates:
- **Database:** `User_Behavior_Segmentation`
- **Table:** `User_Behavior_Details`

### 5️⃣ Prepare the Dataset
Place your dataset (`app_user_behavior_dataset.csv`) in the project folder.

Update the path in `load_data()` if needed:
```python
df = pd.read_csv(r"path/to/app_user_behavior_dataset.csv")
```

### 6️⃣ Run the Application
```bash
streamlit run app.py
```
Navigate between **Home** and **Analysis** pages using the dashboard buttons.

### 7️⃣ Optional: Re-run & Clear Cache
```bash
streamlit cache clear
```
Use this if the dataset or model changes and you need fresh results.

---

## 🎯 Use Case

The App User Behavior Segmentation System is designed for **product managers, data analysts, growth hackers, and app developers** who need actionable insights on their user base. Key use cases include:

### 1. Identify At-Risk and Churning Users
Pinpoint users with high churn probability before they leave. Target them with personalized re-engagement campaigns.

### 2. Reward and Retain Loyal Users
Identify **Loyal Active Users** — your most valuable segment. Design loyalty programs and early feature access for them.

### 3. Convert Casual Users
Understand the behavioral gap between Casual and Loyal users. Push targeted nudges (notifications, offers) to upgrade engagement.

### 4. Device and Country-Level Strategy
Analyze which segments dominate by country and device type to focus product improvements and marketing spend geographically.

### 5. Subscription Tier Optimization
Understand how segments map to subscription types. Use this to design better upgrade paths from Free to Premium tiers.

### 6. Data-Driven Product Decisions
Use behavioral cluster insights to prioritize features that improve daily active minutes and reduce churn risk across all segments.

---

## 🚀 Future Enhancements

1. **Advanced Clustering Algorithms** — Explore DBSCAN, Agglomerative Clustering, or Gaussian Mixture Models for more nuanced segments.
2. **Churn Prediction Model** — Add a supervised classification model to predict individual user churn probability.
3. **Real-Time Data Integration** — Connect with live app analytics platforms (Firebase, Mixpanel) for automatic user updates.
4. **Personalized User Recommendations** — Suggest tailored in-app actions based on a user's cluster to improve retention.
5. **Time-Series Trend Analysis** — Track how users migrate between segments over time to spot behavioral shifts.
6. **Automated Reporting** — Generate scheduled segment health reports for stakeholders.
7. **Enhanced Model Explainability** — Integrate SHAP values to explain what drives each user's cluster assignment.
8. **User Feedback Loop** — Incorporate actual churn events and re-engagement responses to continuously refine cluster definitions.
---

## 📋 Project Overview

The **App User Behavior Segmentation System** is an end-to-end unsupervised machine learning and analytics platform that segments app users into 4 behavioral clusters — **Loyal Active Users**, **Casual Users**, **At Risk Users**, and **High Churn Risk** — based on engagement score, churn risk, and daily active minutes. It combines automated data cleaning, KMeans clustering, MySQL storage, and an interactive Streamlit dashboard with Plotly visualizations to deliver actionable insights on user retention, device preferences, country-level behavior, and subscription patterns. The system empowers product and growth teams to make targeted, data-driven decisions that maximize user retention and lifetime value.

---

⭐ **If you find this project useful, give it a star on GitHub and share your feedback!**
