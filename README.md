# 🎯 App User Behavior Segmentation

---

## 📌 About the Project

This system analyzes mobile app user behavior data to automatically segment users into distinct behavioral groups using unsupervised machine learning. It processes raw usage telemetry — session patterns, engagement metrics, churn signals, and activity features — through a full data science pipeline, then serves the results via an interactive Streamlit dashboard backed by a MySQL database. Product managers, growth teams, and app developers can use this tool to understand their user base and craft targeted retention and engagement strategies.

---

## 🛠️ Development Process

### 1. 📥 Data Collection
- Loaded structured app usage data from a CSV file (`app_user_behavior_dataset.csv`) using `pandas.read_csv()`
- Dataset contains 25+ behavioral and demographic features per user including session metrics, engagement scores, churn risk, and subscription details

### 2. 🧹 Data Cleaning & Preprocessing
- Handled missing values by imputing `rating_given` with the column median
- Identified and treated outliers using the **IQR Capping** method across 11 behavioral columns: `sessions_per_week`, `avg_session_duration_min`, `feature_clicks_per_session`, `notifications_opened_per_week`, `in_app_search_count`, `crash_events_last_30_days`, `ads_clicked_last_30_days`, `content_downloads`, `social_shares`, `daily_active_minutes`, `engagement_score`
- Clipped extreme values to `[Q1 - 1.5×IQR, Q3 + 1.5×IQR]` bounds to preserve data without loss
- Reset the DataFrame index after cleaning for consistency

### 3. 🔍 Feature Selection
- Selected 17 high-signal behavioral features for clustering: session frequency, duration, daily activity, feature engagement, notifications, search behavior, page views, crash events, support interactions, login recency, ad clicks, downloads, shares, ratings, churn risk, engagement score, and account age
- Excluded demographic/categorical features (age, gender, country, device) to ensure the model segments purely on behavioral signals

### 4. ⚖️ Data Transformation
- Applied **StandardScaler** from scikit-learn to normalize all 17 features before clustering
- Ensured each feature contributes equally, preventing scale-dominant features from biasing the KMeans algorithm

### 5. 🤖 Model Building
- Trained a **KMeans clustering model** with `n_clusters=2`, `n_init=20`, `max_iter=500`, and `random_state=42` for reproducibility
- Chose 2 clusters based on the behavioral bimodality observed between light and heavy app users

### 6. 📏 Model Evaluation
- Computed the **Silhouette Score** on the scaled feature matrix to assess cluster separation quality
- Validated that clusters captured meaningful behavioral distinctions before labeling

### 7. 🏷️ Segmentation & Labeling
- Mapped cluster IDs to human-readable segment names:
  - **Cluster 0 → Casual Users**
  - **Cluster 1 → Power Users**
- Added `cluster` (integer) and `segment` (string) columns to the final DataFrame

### 8. 🗄️ Database Integration
- Auto-created a **MySQL** database (`User_Behavior_Segmentation`) and a fully-typed table (`User_Behavior_Details`) on first run using SQLAlchemy + `CREATE DATABASE IF NOT EXISTS`
- Used a session state flag (`data_inserted`) combined with a row count check to ensure data is inserted **only once**, preventing duplicates across reruns

### 9. 🖥️ Dashboard Development
- Built a **multi-page Streamlit app** using `st.session_state.page` for client-side navigation without Streamlit's native multi-page routing
- Applied custom CSS for styled buttons (hover animations, rounded cards, branded colors) and selectbox components

### 10. 📊 Visualization & Analysis
- Created 7 distinct analysis views spanning: cluster identification, segment distribution, behavioral KPI comparison, deep-dive scatter plots, country sunburst analysis, device-type grouped bars, and subscription-type horizontal bars
- All charts use **Plotly Express** and **Plotly Graph Objects** with consistent hover labels and layout theming

### 11. ⚡ Performance Optimization
- Used `@st.cache_data` to cache the full ML pipeline (`get_model_pipeline()`) and raw data load (`load_data()`)
- Used `@st.cache_resource` to cache the database engine (`setup_database()`) — preventing reconnection on every rerun
- Combined these strategies to eliminate redundant computation and DB calls

---

## 🔎 Key Features

### 🔎 Behavioral Segmentation Engine
Automatically clusters app users into **Casual Users** and **Power Users** using KMeans on 17 behavioral signals.

### 📊 Multi-View Analysis Dashboard
Seven dedicated analysis pages covering segment distribution, behavioral KPIs, country breakdowns, device types, and subscription plans.

### 🗄️ Persistent MySQL Backend
All segmented user data is stored in a structured MySQL table with automatic schema creation and single-insertion guard logic.

### ⚡ Fully Cached ML Pipeline
End-to-end pipeline from CSV ingestion to model output is cached with `@st.cache_data` and `@st.cache_resource` for instant reruns.

### 🌍 Country-Level Segment Analysis
Interactive sunburst chart reveals how Casual and Power Users are distributed across every country in the dataset.

### 📱 Device Type Analysis
Grouped bar chart compares segment composition across iOS, Android, and other device types.

### 💳 Subscription Tier Breakdown
Horizontal bar chart maps Free, Premium, and other subscription types to their segment distribution.

### 🎨 Custom UI Styling
Hand-crafted CSS delivers card-style buttons with hover lift effects and branded color schemes throughout the app.

### 🔄 Churn & Engagement KPI Tracking
Dedicated behavioral analysis page surfaces average engagement score, daily active minutes, and churn risk score per segment.

### 🔬 Scatter-Based Deep Dive
Interactive scatter plot of `engagement_score` vs `churn_risk_score` colored by segment for visual cluster validation.

---

## 📋 Features (Detailed)

### 🏠 Home Dashboard
- Displays the full `User_Behavior_Details` table loaded directly from MySQL
- Pie chart shows overall segment distribution (Casual Users vs Power Users)
- One-click navigation to the Analysis hub

### 📶 Analysis Hub
- Central navigation page with a styled selectbox offering 7 analysis topics
- Displays behavioral feature columns alongside cluster and segment labels
- Back button returns to the home dashboard

### 👥 Cluster-wise User Identification
- Table showing each `user_id` mapped to their assigned `segment`
- Useful for downstream CRM or re-engagement targeting

### 📊 Customer Distribution per Segment
- SQL aggregate query (`COUNT(*) GROUP BY segment`) displayed as a DataFrame
- Companion bar chart visualizes the user count split

### 📈 Behavioral Analysis per Segment
- SQL query computes `AVG(engagement_score)`, `AVG(daily_active_minutes)`, `AVG(churn_risk_score)` per segment
- Three charts: full pie (engagement), donut pie (daily usage), bar chart (churn risk)
- Side-by-side column layout for the two pie charts

### 🔬 Segment-wise Deep Dive
- Scatter plot of engagement vs churn risk, colored by segment
- Dropdown to filter and view raw records for **Casual Users** or **Power Users** independently

### 🌍 Country Wise Segment Analysis
- Sunburst chart with `country → segment` hierarchy weighted by user count
- Highlights geographic concentration of Power vs Casual Users

### 📱 Device Type Segment Analysis
- Grouped bar chart comparing segment sizes across device types
- Annotated with exact user counts using `text="Total_segment"`

### 💳 Subscription Type Segment Analysis
- Horizontal grouped bar chart mapping subscription tiers to segment sizes
- Allows product teams to correlate monetization tier with user engagement level

---

## 🧰 Tech Stack

### 🖥️ Frontend / UI
| Library | Purpose |
|---|---|
| `streamlit` | Multi-page interactive web app framework |
| Custom CSS | Hover-animated card buttons, styled selectbox |

### 🧠 Machine Learning
| Library | Purpose |
|---|---|
| `scikit-learn` (KMeans) | Unsupervised clustering — user segmentation |
| `scikit-learn` (StandardScaler) | Feature normalization before clustering |
| `scikit-learn` (silhouette_score) | Cluster quality evaluation |

### 📊 Data Processing & Analysis
| Library | Purpose |
|---|---|
| `pandas` | DataFrame operations, SQL querying via `read_sql` |
| `numpy` | IQR outlier capping, percentile calculation |

### 📈 Data Visualization
| Library | Purpose |
|---|---|
| `plotly.express` | Pie, bar, scatter, sunburst, donut charts |
| `plotly.graph_objects` | Advanced pie chart with `pull` and `textposition` |

### 🗄️ Database
| Library | Purpose |
|---|---|
| `sqlalchemy` | ORM engine creation, schema execution via `text()` |
| `mysql.connector` | MySQL driver backend for SQLAlchemy |
| MySQL | Relational storage for all segmented user records |

### ⚙️ Backend / Core Logic
| Library | Purpose |
|---|---|
| `warnings` | Suppressing non-critical runtime warnings |

### 🚀 Deployment & Optimization
| Decorator | Purpose |
|---|---|
| `@st.cache_data` | Caches `load_data()` and `get_model_pipeline()` |
| `@st.cache_resource` | Caches `setup_database()` DB engine across sessions |
| `st.session_state` | Client-side page navigation and insert-once flag |

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/app-user-behavior-segmentation.git
cd app-user-behavior-segmentation
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
Key libraries: `streamlit`, `pandas`, `numpy`, `plotly`, `scikit-learn`, `sqlalchemy`, `mysql-connector-python`

### 4. Setup the Database
Ensure MySQL is running locally. The app auto-creates the database and table on first launch using:
```
mysql+mysqlconnector://root:0007@localhost/User_Behavior_Segmentation
```
Update the connection string in the code if your MySQL credentials differ.

### 5. Prepare the Dataset
Place your dataset at:
```
D:\PROJECTS\Capstone_Project_4\App_User_Behavior_Segmentation\app_user_behavior_dataset.csv
```
Or update the `pd.read_csv()` path in `load_data()` to match your local file location.

### 6. Run the Application
```bash
streamlit run app.py
```
The app will open at `http://localhost:8501` in your browser.

### 7. Optional: Clear Cache
If you need to reset the pipeline or re-insert data, clear the Streamlit cache from the top-right menu → **Clear Cache**, then restart the app.

---

## 💡 Use Cases

1. **📉 Churn Prevention Targeting** — Identify Casual Users with high churn risk scores and serve them re-engagement campaigns before they lapse.
2. **💰 Upsell Funnel Design** — Locate Casual Users on Free subscriptions who exhibit rising engagement to target with Premium upgrade prompts.
3. **🌍 Regional Growth Strategy** — Use the Country Wise analysis to identify markets dominated by Casual Users and allocate localized onboarding improvements.
4. **📱 Device-Specific Optimization** — Analyze whether one device type skews toward Power Users to prioritize platform-specific feature releases.
5. **🎯 Power User Loyalty Programs** — Extract Power User IDs from the deep-dive table to enroll them in beta programs, referral incentives, or community channels.
6. **📊 Executive Reporting** — The KPI page provides at-a-glance average engagement, daily usage, and churn risk per segment for stakeholder presentations.

---

## 🔮 Future Enhancements

1. **Multi-Cluster Expansion** — Evaluate 3–5 cluster solutions (using Elbow Method and Silhouette plots) to discover sub-segments like "At-Risk Power Users" or "Occasional Explorers"
2. **Real-Time Data Ingestion** — Replace static CSV loading with a live database or streaming pipeline (Kafka / Kinesis) for continuously updated segmentation
3. **Explainability Layer** — Integrate SHAP values to surface which features (e.g., `days_since_last_login`) most strongly drive cluster membership for each user
4. **Automated PDF Reports** — Add a one-click export button that generates a formatted PDF summary of all analysis views for stakeholder distribution
5. **Predictive Churn Model** — Layer a supervised classification model (XGBoost or LightGBM) on top of the segments to generate individual-level churn probability scores
6. **User-Level Drill-Down** — Enable search by `user_id` to view a single user's full behavioral profile alongside their segment assignment and KPI benchmarks
7. **Time-Series Tracking** — Store historical segment snapshots to track users migrating between Casual and Power segments over time
8. **Automated Re-Segmentation Scheduler** — Schedule weekly pipeline reruns via Airflow or cron to keep segment labels current as user behavior evolves
---

## 📖 Project Overview

The App User Behavior Segmentation system is an end-to-end unsupervised machine learning application that classifies mobile app users into **Casual Users** and **Power Users** based on 17 behavioral telemetry features. The pipeline begins with IQR-based outlier capping across 11 numerical columns, followed by StandardScaler normalization, before training a KMeans model (`n_clusters=2`, `n_init=20`, `max_iter=500`) evaluated using the Silhouette Score. All segmented records — 27 columns per user — are persisted in a MySQL database (`User_Behavior_Details`) via SQLAlchemy, with a session-state insertion guard ensuring idempotent writes. The Streamlit dashboard provides seven interactive analysis views — from cluster identification and behavioral KPI comparisons to country-level sunburst charts and subscription-tier breakdowns — all powered by Plotly Express and Graph Objects with custom CSS styling. By combining behavioral segmentation with rich visual analytics, the system gives product and growth teams an actionable lens into who their users are and how to engage them more effectively.

---

⭐ **If you find this project useful, give it a star on GitHub and share your feedback!**
