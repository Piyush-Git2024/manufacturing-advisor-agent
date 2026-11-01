import streamlit as st
import requests

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Manufacturing Operations Control Tower",
    page_icon="🏭",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* -----------------------------------------------------
   GLOBAL APP
----------------------------------------------------- */

.stApp {
    background: #f8fafc;
}

/* -----------------------------------------------------
   HEADER
----------------------------------------------------- */

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #475569;
    font-size: 18px;
    margin-bottom: 25px;
}

/* -----------------------------------------------------
   KPI CARDS
----------------------------------------------------- */

[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e2e8f0;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
}

/* -----------------------------------------------------
   TEXT INPUT
----------------------------------------------------- */

.stTextInput input {
    background: white !important;
    color: #111827 !important;
    border-radius: 10px;
    border: 1px solid #cbd5e1 !important;
}

/* -----------------------------------------------------
   BUTTONS
----------------------------------------------------- */

.stButton button {
    background: linear-gradient(
        90deg,
        #2563eb,
        #0ea5e9
    );

    color: white !important;

    border: none;

    border-radius: 10px;

    font-weight: 600;

    width: 100%;
}

.stButton button:hover {

    background: linear-gradient(
        90deg,
        #1d4ed8,
        #0284c7
    );
}

/* -----------------------------------------------------
   TEXT
----------------------------------------------------- */

html, body, p, span, label {
    color: #334155 !important;
}

h1,h2,h3,h4,h5 {
    color: #0f172a !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class='main-title'>
🏭 Manufacturing Operations Control Tower
</div>

<div class='subtitle'>
AI Powered Manufacturing Intelligence Platform
</div>
""", unsafe_allow_html=True)

# =====================================================
# HERO BANNER
# =====================================================

st.info("""
### 🤖 AI Manufacturing Advisor

Analyze production performance, quality trends,
maintenance risks, machine health, operational incidents
and plant performance using AI-powered manufacturing intelligence.
""")

# =====================================================
# KPI SECTION
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Plants",
        "3"
    )

with c2:
    st.metric(
        "Highest Risk Plant",
        "PUN"
    )

with c3:
    st.metric(
        "Highest Risk Machine",
        "CNC101"
    )

with c4:
    st.metric(
        "Open Risks",
        "4"
    )

st.divider()

# =====================================================
# SESSION STATE
# =====================================================

if "question" not in st.session_state:
    st.session_state.question = ""

# =====================================================
# MAIN LAYOUT
# =====================================================

left_col, right_col = st.columns([1, 3])

# =====================================================
# LEFT PANEL
# =====================================================

with left_col:

    st.subheader("🏭 Plant Risk Ranking")

    st.markdown("""
🔴 **PUN** - HIGH RISK

🟠 **HYD** - MEDIUM RISK

🟢 **BLR** - LOW RISK
""")

    st.divider()

    st.subheader("⚡ Quick Questions")

    if st.button("🚨 Biggest Operational Risk"):
        st.session_state.question = \
            "What is the biggest operational risk today?"

    if st.button("🎯 Production Target Assessment"):
        st.session_state.question = \
            "Will we achieve production targets?"

    if st.button("📊 Executive Summary"):
        st.session_state.question = \
            "Provide executive summary of factory risks."

    if st.button("🏭 Plant Analysis"):
        st.session_state.question = \
            "Which plant requires immediate attention?"

    if st.button("🔧 Maintenance Analysis"):
        st.session_state.question = \
            "Provide maintenance analysis."

    if st.button("✅ Quality Analysis"):
        st.session_state.question = \
            "Provide quality analysis."

# =====================================================
# RIGHT PANEL
# =====================================================

with right_col:

    st.subheader("🤖 Manufacturing Advisor")

    question = st.text_input(
        "Ask a question",
        value=st.session_state.question,
        placeholder="What is the biggest operational risk today?"
    )

    if st.button("Analyze Factory Operations"):

        if not question.strip():
            st.warning("Please enter a question.")
            st.stop()

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
                "Analyzing production, quality, maintenance and operational risk..."
            ):

                response = requests.post(
                    "http://localhost:5001/",
                    json=payload,
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                answer = data["result"][
                    "artifacts"
                ][0]["parts"][0]["text"]

            st.success("✅ Analysis Complete")

            st.markdown("---")

            st.markdown(answer)

        except Exception as ex:

            st.error(
                f"Unable to connect to Manufacturing Advisor API.\n\n{str(ex)}"
            )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Manufacturing Advisor | LangChain | Ollama | SQLite | Pega | AI-Powered Operations Intelligence"
)