import streamlit as st
import base64
import streamlit.components.v1 as components

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="SCM Cement Dashboard",
    page_icon="🏭",
    layout="wide"
)

# =====================================
# LOAD LOGO
# =====================================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = img_to_base64("assets/logo.png")

# =====================================
# DASHBOARD HTML
# =====================================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>

body {{
    margin:0;
    background:#f4f7fa;
    font-family: 'Segoe UI', sans-serif;
}}

.container {{
    max-width:1400px;
    margin:auto;
}}

.header {{
    background: linear-gradient(135deg,#0f172a,#1e3a8a);
    color:white;
    padding:40px;
    border-radius:20px;
    margin-top:20px;
}}

.header-flex {{
    display:flex;
    align-items:center;
    justify-content:space-between;
}}

.logo img {{
    width:90px;
}}

.title {{
    flex:1;
    padding-left:30px;
}}

.title h1 {{
    margin:0;
    font-size:36px;
}}

.title p {{
    margin-top:10px;
    color:#cbd5e1;
    font-size:16px;
}}

.kpi-container {{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:20px;
    margin-top:30px;
}}

.kpi {{
    background:white;
    padding:25px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 5px 15px rgba(0,0,0,0.08);
}}

.kpi-title {{
    color:#64748b;
    font-size:14px;
}}

.kpi-value {{
    font-size:30px;
    font-weight:bold;
    color:#0f172a;
    margin-top:10px;
}}

.section {{
    margin-top:30px;
}}

.card-container {{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:20px;
}}

.card {{
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0 5px 15px rgba(0,0,0,0.08);
}}

.card h3 {{
    margin-top:0;
    color:#1e3a8a;
}}

.card p {{
    color:#475569;
    line-height:1.7;
}}

.footer {{
    margin-top:40px;
    text-align:center;
    color:#64748b;
    font-size:14px;
}}

</style>
</head>

<body>

<div class="container">

    <div class="header">

        <div class="header-flex">

            <div class="logo">
                <img src="data:image/png;base64,{logo}">
            </div>

            <div class="title">
                <h1>Cement Supply Chain Dashboard</h1>
                <p>
                    Intelligent Decision Support System for Supply Chain Management,
                    Distribution Optimization, Inventory Monitoring and Dynamic Simulation.
                </p>
            </div>

        </div>

    </div>

    <div class="kpi-container">

        <div class="kpi">
            <div class="kpi-title">Distribution Efficiency</div>
            <div class="kpi-value">95%</div>
        </div>

        <div class="kpi">
            <div class="kpi-title">Inventory Accuracy</div>
            <div class="kpi-value">98%</div>
        </div>

        <div class="kpi">
            <div class="kpi-title">Service Level</div>
            <div class="kpi-value">92%</div>
        </div>

        <div class="kpi">
            <div class="kpi-title">Supply Reliability</div>
            <div class="kpi-value">97%</div>
        </div>

    </div>

    <div class="section">

        <div class="card-container">

            <div class="card">
                <h3>📊 SCM Analytics</h3>
                <p>
                    Analyze production, inventory, transportation,
                    and demand patterns in real-time.
                </p>
            </div>

            <div class="card">
                <h3>🔮 Fuzzy Decision System</h3>
                <p>
                    Support decision making using fuzzy inference
                    and intelligent forecasting models.
                </p>
            </div>

            <div class="card">
                <h3>⚙️ Dynamic Simulation</h3>
                <p>
                    Simulate supply chain scenarios to evaluate
                    operational performance and future strategies.
                </p>
            </div>

        </div>

    </div>

    <div class="footer">
        SCM Optimization Platform © 2026
    </div>

</div>

</body>
</html>
"""

components.html(html_code, height=700)

# =====================================
# ACTION BUTTONS
# =====================================
st.markdown("### 🚀 Quick Access")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Run Simulation", use_container_width=True):
        st.switch_page("pages/1_Fuzzy_System.py")

with col2:
    st.button("View Analytics", use_container_width=True)

with col3:
    st.button("Generate Report", use_container_width=True)
