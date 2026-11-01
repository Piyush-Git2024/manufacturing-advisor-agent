import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import sqlite3
from datetime import datetime

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Manufacturing Operations Control Hub",
    page_icon="🏭",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f6f9fc;
}

.main-title {
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:#0F172A;
}

.sub-title {
    text-align:center;
    color:#475569;
    margin-bottom:20px;
}

.hero {
    background: white;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #2563EB;
    padding: 12px 20px;
    border-radius: 12px;
    color: #0F172A;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

.metric-card {
    background:white;
    padding:20px;
    border-radius:15px;
}

.chat-answer {
    background:white;
    padding:20px;
    border-radius:10px;
    border-left:5px solid #2563EB;
}

button[data-baseweb="tab"] {

    font-size: 18px !important;

    font-weight: 600 !important;

    padding: 12px 30px !important;

    height: 60px !important;

    border-radius: 10px !important;
}

button[data-baseweb="tab"]:hover {
    background-color: #eef4ff;
}

button[aria-selected="true"] {
    background-color: #2563EB !important;
    color: white !important;
}

.block-container {
    padding-top: 1rem;
}

[data-testid="metric-container"]{

    background:white;

    border-radius:15px;

    padding:15px;

    border:1px solid #e5e7eb;

    box-shadow:0px 2px 8px rgba(0,0,0,0.05);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
}

.stTabs [data-baseweb="tab"] {
    height: 60px;
    font-size: 18px;
    font-weight: 600;
    padding: 10px 25px;
}

.stTabs [aria-selected="true"] {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HERO
# ==========================================================

st.markdown("""
<div class="main-title">
🏭 Manufacturing Operations Control Hub
</div>

<div class="sub-title">
AI Powered Manufacturing Intelligence Platform
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">

<h2> Manufacturing Advisor</h2>

Executive Risk Analysis • Production Intelligence • Quality Analytics • Maintenance Insights

Powered by LangChain

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ==========================================================
# KPI SECTION
# ==========================================================

# ==========================================================
# KPI SECTION
# ==========================================================

conn = sqlite3.connect("factory_v2.db")

plants_cnt = pd.read_sql_query(
    "SELECT COUNT(*) cnt FROM Plants",
    conn
).iloc[0]["cnt"]

lines_cnt = pd.read_sql_query(
    "SELECT COUNT(*) cnt FROM ProductionLines",
    conn
).iloc[0]["cnt"]

machines_cnt = pd.read_sql_query(
    "SELECT COUNT(*) cnt FROM Machines",
    conn
).iloc[0]["cnt"]

incident_cnt = pd.read_sql_query(
    "SELECT COUNT(*) cnt FROM OperationalIncidents",
    conn
).iloc[0]["cnt"]

risk_machine_df = pd.read_sql_query(
    """
    SELECT
        MachineID,
        AVG(Temperature) AvgTemp,
        AVG(Vibration) AvgVibration
    FROM MachineHealthHistory
    GROUP BY MachineID
    """,
    conn
)

quality_alerts_df = pd.read_sql_query(
    """
    SELECT
        LineID,
        AVG(DefectRate) AvgDefectRate
    FROM QualityHistory
    GROUP BY LineID
    """,
    conn
)

conn.close()

risk_machine_df["RiskScore"] = (
    risk_machine_df["AvgTemp"] * 0.6
    +
    risk_machine_df["AvgVibration"] * 8
)

highest_risk_machine = (
    risk_machine_df
    .sort_values("RiskScore", ascending=False)
    .iloc[0]["MachineID"]
)

high_risk_assets = len(
    risk_machine_df[
        risk_machine_df["RiskScore"]
        > risk_machine_df["RiskScore"].mean()
    ]
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.metric("Plants", plants_cnt)

with c2:
    st.metric("Lines", lines_cnt)

with c3:
    st.metric("Machines", machines_cnt)

with c4:
    st.metric("High Risk Assets", high_risk_assets)

with c5:
    st.metric("Top Risk Machine", highest_risk_machine)

with c6:
    st.metric("Incidents", incident_cnt)

st.divider()

# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Executive Dashboard",
    "🤖 AI Advisor",
    "🏭 Production",
    "✅ Quality",
    "🔧 Maintenance",
    "🗄️ Data Explorer"
])

# ==========================================================
# EXECUTIVE DASHBOARD
# ==========================================================
with tab1:

    st.success(
        "🏭 Live Executive Dashboard powered by Manufacturing Advisor Analytics"
    )

    conn = sqlite3.connect("factory_v2.db")

    plant_risk_df = pd.read_sql_query(
        """
        SELECT
            PlantID,
            AVG(DefectRate) AvgDefectRate
        FROM QualityHistory
        GROUP BY PlantID
        ORDER BY AvgDefectRate DESC
        """,
        conn
    )

    machine_risk_df = pd.read_sql_query(
        """
        SELECT
            MachineID,
            AVG(Temperature) AvgTemp,
            AVG(Vibration) AvgVibration
        FROM MachineHealthHistory
        GROUP BY MachineID
        """,
        conn
    )

    production_gap_df = pd.read_sql_query(
        """
        SELECT
            LineID,
            AVG(TargetProduction - ActualProduction) AvgGap
        FROM ProductionHistory
        GROUP BY LineID
        ORDER BY AvgGap DESC
        """,
        conn
    )

    conn.close()

    machine_risk_df["RiskScore"] = (
        machine_risk_df["AvgTemp"] * 0.6 +
        machine_risk_df["AvgVibration"] * 8
    )

    machine_risk_df = machine_risk_df.sort_values(
        "RiskScore",
        ascending=False
    )

    top_machine = machine_risk_df.iloc[0]["MachineID"]

    worst_line = production_gap_df.iloc[0]["LineID"]

    left, right = st.columns([1, 2])

    with left:

        st.subheader("🏭 Plant Risk Ranking")

        for idx, row in plant_risk_df.iterrows():

            if idx == 0:
                icon = "🔴"
            elif idx == 1:
                icon = "🟠"
            else:
                icon = "🟢"

            st.markdown(
                f"{icon} **{row['PlantID']}**  \n"
                f"Defect Rate: {round(row['AvgDefectRate'],2)}%"
            )

        st.subheader("📋 Priority Actions")

        st.markdown(f"""
✅ Immediate review of **{top_machine}**

✅ Recovery plan for **{worst_line}**

✅ Monitor highest-risk plant

✅ Continue quality improvement initiatives

✅ Review operational incidents
""")

    with right:

        fig = px.bar(
            plant_risk_df,
            x="PlantID",
            y="AvgDefectRate",
            color="AvgDefectRate",
            title="Plant Risk Comparison"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info(f"""
### 🤖 Executive Summary

Current manufacturing analytics indicate elevated operational risk around machine **{top_machine}**.

Production performance analysis shows the greatest performance gap on **{worst_line}**.

Plant risk ranking is derived from actual quality performance data.

Recommended leadership focus areas:

• Machine reliability

• Production target recovery

• Quality improvement

• Incident prevention

• Proactive maintenance planning
""")
# ==========================================================
# AI CHAT
# ==========================================================

with tab2:

    st.subheader("AI Manufacturing Advisor")

    example_questions = [
        "What is the biggest operational risk today?",
        "Will we achieve production targets?",
        "Provide executive summary of factory risks.",
        "Which plant requires attention?",
        "Provide maintenance analysis."
    ]

    selected = st.selectbox(
        "Quick Questions",
        [""] + example_questions
    )

    question = st.text_input(
        "Ask Manufacturing Advisor",
        value=selected
    )

    if st.button("Analyze Factory"):

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "message/send",
            "params": {
                "message": {
                    "parts": [
                        {
                            "text": question
                        }
                    ]
                }
            }
        }

        try:

            with st.spinner(
                "Analyzing operational data..."
            ):

                response = requests.post(
                    "http://localhost:5001/",
                    json=payload,
                    timeout=120
                )

                result = response.json()

                answer = result["result"][
                    "artifacts"
                ][0]["parts"][0]["text"]

            st.success("Analysis Complete")

            st.markdown(
                f"""
<div class="chat-answer">
{answer}
</div>
""",
                unsafe_allow_html=True
            )

        except Exception as ex:

            st.error(str(ex))

# ==========================================================
# PRODUCTION TAB
# ==========================================================

with tab3:

    st.subheader("🏭 Production Analytics")

    import sqlite3

    conn = sqlite3.connect("factory_v2.db")

    production_df = pd.read_sql_query(
        """
        SELECT
            ProductionDate,
            TargetProduction,
            ActualProduction,
            PlantID,
            LineID
        FROM ProductionHistory
        ORDER BY ProductionDate
        """,
        conn
    )

    conn.close()

    production_df["ProductionDate"] = pd.to_datetime(
        production_df["ProductionDate"]
    )

    # Target vs Actual Production

    st.markdown("### Target vs Actual Production")

    fig = px.line(
        production_df,
        x="ProductionDate",
        y=[
            "TargetProduction",
            "ActualProduction"
        ],
        title="Production Performance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Production Gap

    production_df["Gap"] = (
        production_df["TargetProduction"]
        - production_df["ActualProduction"]
    )

    st.markdown("### Production Gap")

    gap_df = (
        production_df
        .groupby("LineID")["Gap"]
        .mean()
        .reset_index()
        .sort_values(
            "Gap",
            ascending=False
        )
    )

    fig2 = px.bar(
        gap_df,
        x="LineID",
        y="Gap",
        color="Gap",
        title="Average Production Gap by Line"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("### Raw Production Data")

    st.dataframe(
        production_df.tail(20),
        use_container_width=True
    )
# ==========================================================
# QUALITY TAB
# ==========================================================

with tab4:

    st.subheader("✅ Quality Analytics")

    import sqlite3

    conn = sqlite3.connect("factory_v2.db")

    quality_df = pd.read_sql_query(
        """
        SELECT
            InspectionDate,
            PlantID,
            LineID,
            DefectRate,
            ScrapRate,
            ReworkRate,
            TotalDefects
        FROM QualityHistory
        ORDER BY InspectionDate
        """,
        conn
    )

    conn.close()

    quality_df["InspectionDate"] = pd.to_datetime(
        quality_df["InspectionDate"]
    )

    # ==========================================
    # Defect Rate Trend
    # ==========================================

    st.markdown("### 📈 Defect Trend")

    fig1 = px.line(
        quality_df,
        x="InspectionDate",
        y="DefectRate",
        color="LineID",
        title="Defect Rate by Production Line"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # ==========================================
    # Scrap & Rework
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        fig2 = px.line(
            quality_df,
            x="InspectionDate",
            y="ScrapRate",
            color="LineID",
            title="Scrap Rate"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    with col2:

        fig3 = px.line(
            quality_df,
            x="InspectionDate",
            y="ReworkRate",
            color="LineID",
            title="Rework Rate"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # ==========================================
    # Highest Defect Lines
    # ==========================================

    st.markdown("### 🚨 Highest Defect Lines")

    defect_summary = (
        quality_df
        .groupby("LineID")
        .agg(
            AvgDefectRate=("DefectRate", "mean"),
            TotalDefects=("TotalDefects", "sum")
        )
        .reset_index()
        .sort_values(
            "AvgDefectRate",
            ascending=False
        )
    )

    fig4 = px.bar(
        defect_summary,
        x="LineID",
        y="AvgDefectRate",
        color="AvgDefectRate",
        title="Average Defect Rate by Line"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.markdown("### 📊 Quality Summary")

    st.dataframe(
        defect_summary,
        use_container_width=True
    )

# ==========================================================
# MAINTENANCE TAB
# ==========================================================

with tab5:

    st.subheader("🔧 Machine Health & Maintenance Analytics")

    import sqlite3

    conn = sqlite3.connect("factory_v2.db")

    machine_df = pd.read_sql_query(
        """
        SELECT
            ReadingTime,
            MachineID,
            Temperature,
            Vibration,
            RuntimeHours,
            LoadPercentage
        FROM MachineHealthHistory
        ORDER BY ReadingTime
        """,
        conn
    )

    conn.close()

    machine_df["ReadingTime"] = pd.to_datetime(
        machine_df["ReadingTime"]
    )

    # ------------------------------------------------
    # Risk Score
    # ------------------------------------------------

    risk_df = (
        machine_df
        .groupby("MachineID")
        .agg(
            AvgTemperature=("Temperature", "mean"),
            AvgVibration=("Vibration", "mean"),
            AvgRuntime=("RuntimeHours", "mean")
        )
        .reset_index()
    )

    risk_df["RiskScore"] = (
        (risk_df["AvgTemperature"] * 0.6)
        +
        (risk_df["AvgVibration"] * 8)
    )

    risk_df = risk_df.sort_values(
        "RiskScore",
        ascending=False
    )

    st.markdown("### 🚨 Machine Risk Ranking")

    fig1 = px.bar(
        risk_df.head(10),
        x="MachineID",
        y="RiskScore",
        color="RiskScore",
        title="Highest Risk Machines"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )
# ==========================================================
# DATA EXPLORER
# ==========================================================

with tab6:

    st.subheader(
        "🗄️ Manufacturing Database Explorer"
    )

    conn = sqlite3.connect("factory_v2.db")

    tables = [
        "Plants",
        "ProductionLines",
        "Machines",
        "ProductionHistory",
        "QualityHistory",
        "MachineHealthHistory",
        "MaintenanceHistory",
        "OperationalIncidents"
    ]

    selected_table = st.selectbox(
        "Select Table",
        tables
    )

    df = pd.read_sql_query(
        f"SELECT * FROM {selected_table}",
        conn
    )

    st.metric(
        "Total Records",
        len(df)
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Columns",
            len(df.columns)
        )

    with col2:
        st.metric(
            "Rows",
            len(df)
        )

    st.markdown("### Columns")

    st.write(list(df.columns))

    st.markdown("### Sample Data")

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )

    if st.checkbox(
        "Show Data Types"
    ):

        st.write(
            pd.DataFrame(
                df.dtypes,
                columns=["Data Type"]
            )
        )

    conn.close()
    # ------------------------------------------------
    # Machine Selection
    # ------------------------------------------------

    selected_machine = st.selectbox(
        "Select Machine",
        sorted(
            machine_df["MachineID"]
            .unique()
        )
    )

    machine_history = machine_df[
        machine_df["MachineID"]
        == selected_machine
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### 🌡 Temperature Trend"
        )

        fig2 = px.line(
            machine_history,
            x="ReadingTime",
            y="Temperature",
            title=f"{selected_machine} Temperature"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    with col2:

        st.markdown(
            "### 📈 Vibration Trend"
        )

        fig3 = px.line(
            machine_history,
            x="ReadingTime",
            y="Vibration",
            title=f"{selected_machine} Vibration"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    st.markdown("### 📊 Machine Health Data")

    st.dataframe(
        machine_history.tail(20),
        use_container_width=True
    )

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    f"""
Manufacturing Operations Control Hub |
LangChain |
SQLite |
Ollama |
Pega |
Generated on {datetime.now().strftime("%d-%b-%Y %H:%M")}
"""
)