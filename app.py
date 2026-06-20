import streamlit as st
import base64
import streamlit.components.v1 as components

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Cement SCM Simulation",
    page_icon="🏭",
    layout="centered"
)

# =============================
# LOAD LOGO (BASE64)
# =============================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = img_to_base64("assets/LOGO-UTM.png")

# =============================
# FULL HTML – FINAL COVER UTHM
# =============================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin: 0;
    background: linear-gradient(180deg, #081826, #0b2239);
    font-family: "Times New Roman", Georgia, serif;
    color: #e5e7eb;
}}

.container {{
    max-width: 1000px;
    margin: 40px auto 60px auto;
}}

.hero {{
    background: linear-gradient(180deg, #102a43, #0b2239);
    border-left: 6px solid #3b82f6;
    padding: 48px 40px;
    border-radius: 16px;
    box-shadow: 0 14px 38px rgba(0,0,0,0.45);
}}

.hero-title {{
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.5;
    text-transform: uppercase;
}}

.hero-subtitle {{
    text-align: center;
    font-size: 15px;
    color: #cbd5e1;
    margin-top: 18px;
    letter-spacing: 0.5px;
}}

.author {{
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    margin-top: 28px;
    letter-spacing: 0.6px;
    color: #f8fafc;
}}

/* UNIVERSITY CARD (OFFICIAL) */
.uni-card {{
    margin-top: 38px;
    background: #0f2a44;
    padding: 40px 36px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 10px 18px rgba(0,0,0,0.35);
}}

.uni-logo {{
    margin-bottom: 22px;
}}

.uni-logo img {{
    width: 80px;   /* LOGO LEBIH LEBAR */
    max-width: 100%;
}}

.uni-degree {{
    font-weight: 700;
    font-size: 16px;
    color: #ffffff;
    margin-bottom: 16px;
}}

.uni-text {{
    font-size: 15px;
    line-height: 1.8;
    color: #e2e8f0;
}}

.year {{
    text-align: center;
    margin-top: 18px;
    color: #cbd5e1;
    font-size: 14px;
    letter-spacing: 0.4px;
}}

.declaration {{
    margin-top: 44px;
    background: #081a2c;
    padding: 30px 34px;
    border-radius: 14px;
    font-size: 13.5px;
    line-height: 1.8;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}}

.declaration-title {{
    text-align: center;
    font-weight: 700;
    margin-bottom: 18px;
    color: #ffffff;
    letter-spacing: 0.5px;
}}
</style>
</head>

<body>
<div class="container">

    <div class="hero">
        <div class="hero-title">
            Dynamic System Model to Improve the Ratio and Efficiency in the Supply Chain
            Management (SCM) Distribution of the Cement Industry
        </div>

        <div class="hero-subtitle">
            At Banten Province, Indonesia
        </div>

        <div class="author">
            YUDI MAULANA
        </div>

        <div class="uni-card">
            <div class="uni-logo">
                <img src="data:image/png;base64,{logo}">
            </div>

            <div class="uni-degree">
                Doctor of Philosophy in Mechanical Engineering
            </div>

            <div class="uni-text">
                Faculty of Mechanical and Manufacturing Engineering<br>
                Universiti Tun Hussein Onn Malaysia
            </div>
                <div class="year">
                January 2026
            </div>
        </div>
        <div class="declaration">
            <div class="declaration-title">STUDENT DECLARATION</div>
    
            “I hereby declare that the work in this thesis is my own except for quotations
            and summaries which have been duly acknowledged.”<br><br>
    
            <b>Student:</b> Yudi Maulana<br>
            <b>Date:</b> 22 January 2026<br><br>
    
            <b>Supervisor:</b> Prof. Ir. Ts. Dr. Bukhari Bin Manshoor<br>
            <b>Supervisor:</b> Ir. Dr.-Eng. Mairiza Zainuddin
        </div>
    </div>
</div>
</body>
</html>
"""

components.html(html_code, height=1150)

# =============================
# RUN SIMULATION BUTTON
# =============================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Run Simulation", use_container_width=True):
        st.switch_page("pages/1_Fuzzy_System.py")










