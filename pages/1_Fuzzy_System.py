import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modules.fuzzy_system import build_fuzzy_system, predict_import
from modules.data_loader import load_anylogic_data
from modules.visualization import plot_mf, plot_fuzzy_surface
from io import BytesIO

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Fuzzy Import System",
    layout="wide"
)

st.title("📊 Import Requirement Forecasting Using a Fuzzy System")

# =========================================================
# BUILD FUZZY SYSTEM
# =========================================================
system, md, ps, pc, pi = build_fuzzy_system()

# =========================================================
# MEMBERSHIP FUNCTIONS (TOGGLE)
# =========================================================
st.subheader("📐 Membership Functions")

if "show_mf" not in st.session_state:
    st.session_state.show_mf = False

if st.button("📐 Show Membership Functions"):
    st.session_state.show_mf = not st.session_state.show_mf

if st.session_state.show_mf:
    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(
            plot_mf(
                md.universe,
                {k: md[k].mf for k in md.terms},
                "Market Demand"
            )
        )
        st.pyplot(
            plot_mf(
                ps.universe,
                {k: ps[k].mf for k in ps.terms},
                "Initial Stock"
            )
        )

    with col2:
        st.pyplot(
            plot_mf(
                pc.universe,
                {k: pc[k].mf for k in pc.terms},
                "Production Capacity"
            )
        )
        st.pyplot(
            plot_mf(
                pi.universe,
                {k: pi[k].mf for k in pi.terms},
                "Import Decision"
            )
        )

# =========================================================
# FUZZY SURFACE (3D)
# =========================================================
st.subheader("🧩 Fuzzy Surface (3D Visualization)")

if "show_surface" not in st.session_state:
    st.session_state.show_surface = False

if st.button("🧩 Show Fuzzy Surface"):
    st.session_state.show_surface = not st.session_state.show_surface

if st.session_state.show_surface:
    md_range = np.linspace(md.universe.min(), md.universe.max(), 30)
    ps_range = np.linspace(ps.universe.min(), ps.universe.max(), 30)

    fig_surface = plot_fuzzy_surface(
        system,
        md_range,
        ps_range,
        pc_fixed=100
    )

    st.pyplot(fig_surface)

# =========================================================
# DATA UPLOAD
# =========================================================
st.subheader("📂 Upload AnyLogic Data")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file:
    df = load_anylogic_data(uploaded_file)

    # =====================================================
    # STANDARDIZE TIME COLUMN
    # =====================================================
    df["Month"] = pd.to_datetime(df["Month"]).dt.to_period("M")

    # =====================================================
    # STANDARDIZE COLUMN NAMES (GLOBAL CONTRACT)
    # =====================================================
    df = df.rename(columns={
        "Demand": "Demand",
        "Stock": "Initial_Stock",
        "Production": "Production_Capacity"
    })

    required_cols = [
        "Month",
        "Demand",
        "Initial_Stock",
        "Production_Capacity"
    ]

    if not all(col in df.columns for col in required_cols):
        st.error("❌ Required columns are missing.")
        st.write("Detected columns:", list(df.columns))
        st.stop()

    st.success("✅ Data successfully uploaded and validated")
    st.dataframe(df, use_container_width=True)

    # =====================================================
    # RUN FUZZY PREDICTION
    # =====================================================
    if st.button("🔍 Run Fuzzy Prediction"):
        predictions = []

        for _, row in df.iterrows():
            pred = predict_import(
                system,
                row["Demand"],
                row["Initial_Stock"],
                row["Production_Capacity"]
            )
            predictions.append(pred)

        df["Fuzzy_Import"] = predictions

        # =================================================
        # SAVE ONLY STANDARDIZED OUTPUT TO SESSION
        # =================================================
        fuzzy_output = df[[
            "Month",
            "Demand",
            "Initial_Stock",
            "Fuzzy_Import"
        ]].copy()

        st.session_state["fuzzy_result"] = fuzzy_output

        st.success("✅ Fuzzy prediction results saved to session")
        st.dataframe(fuzzy_output, use_container_width=True)

        # =================================================
        # TIME SERIES VISUALIZATION
        # =================================================
        st.subheader("📉 Time Series of Fuzzy Import Prediction")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(
            fuzzy_output["Month"].astype(str),
            fuzzy_output["Fuzzy_Import"],
            marker="o"
        )
        ax.set_xlabel("Month")
        ax.set_ylabel("Import Quantity")
        ax.set_title("Fuzzy Import Prediction Over Time")
        ax.grid(True)
        plt.xticks(rotation=45)

        st.pyplot(fig)

        # =================================================
        # DOWNLOAD RESULTS
        # =================================================
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            fuzzy_output.to_excel(
                writer,
                index=False,
                sheet_name="Fuzzy_Result"
            )

        output.seek(0)

        st.download_button(
            label="⬇️ Download Fuzzy Results (Excel)",
            data=output,
            file_name="fuzzy_import_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
