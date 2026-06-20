import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modules.dp_model import dp_deterministic_horizon

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Dynamic Programming - Import Optimization",
    layout="wide"
)

st.title("⚙️ Import Optimization Using Dynamic Programming")

st.markdown("""
This page optimizes import decisions using a **Dynamic Programming (DP)** approach.
The **Fuzzy System output** is used as a constraint/reference for optimization.
""")

# =========================================================
# UPLOAD FUZZY RESULTS
# =========================================================
st.subheader("📂 Upload Fuzzy Prediction Results")

uploaded_file = st.file_uploader(
    "Upload Fuzzy Prediction Result File (Excel)",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # =====================================================
    # REQUIRED COLUMNS (OFFICIAL CONTRACT)
    # =====================================================
    required_cols = [
        "Month",
        "Demand",
        "Initial_Stock",
        "Fuzzy_Import"
    ]

    if not all(col in df.columns for col in required_cols):
        st.error("❌ Invalid file format.")
        st.write("Required columns:", required_cols)
        st.write("Detected columns:", list(df.columns))
        st.stop()

    # =====================================================
    # DATA PREVIEW
    # =====================================================
    df["Month"] = df["Month"].astype(str)

    st.success("✅ Fuzzy prediction data successfully loaded")
    st.dataframe(df, use_container_width=True)

    # =====================================================
    # DP PARAMETERS
    # =====================================================
    st.subheader("🎛️ Dynamic Programming Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        holding_cost = st.number_input(
            "Holding Cost per Unit",
            min_value=0.0,
            value=2.0
        )

    with col2:
        import_cost = st.number_input(
            "Import Cost per Unit",
            min_value=0.0,
            value=5.0
        )

    with col3:
        max_stock = st.number_input(
            "Maximum Warehouse Capacity",
            min_value=1,
            value=500
        )

    initial_stock = st.number_input(
        "Initial Stock Level",
        min_value=0,
        value=int(df["Initial_Stock"].iloc[0])
    )

    # =====================================================
    # RUN DP
    # =====================================================
    if st.button("⚙️ Run Dynamic Programming Optimization"):

        demand = df["Demand"].values
        fuzzy_import = df["Fuzzy_Import"].values

        results_dp, total_cost = dp_deterministic_horizon(
            demand=demand,
            fuzzy_import=fuzzy_import,
            holding_cost=holding_cost,
            import_cost=import_cost,
            max_stock=int(max_stock),
            initial_stock=int(initial_stock)
        )

        # =================================================
        # FINAL COLUMN STANDARDIZATION
        # =================================================
        results_dp = results_dp.rename(columns={
            "Impor_Optimal": "Optimal_Import",
            "Impor_Fuzzy": "Fuzzy_Import",
            "Stok_Awal": "Starting_Stock",
            "Stok_Akhir": "Ending_Stock",
            "Demand": "Demand"
        })

        # =================================================
        # ADD TIME INDEX
        # =================================================
        results_dp["Month"] = df["Month"].values
        results_dp["Initial_Stock"] = df["Initial_Stock"].values

        # =================================================
        # TOTAL COST
        # =================================================
        results_dp["Total_Cost"] = (
            results_dp["Holding_Cost"] +
            results_dp["Import_Cost"]
        )

        # =================================================
        # SAVE TO SESSION
        # =================================================
        st.session_state["dp_result"] = results_dp.copy()
        st.session_state["dp_total_cost"] = results_dp["Total_Cost"].sum()

        st.success("✅ Dynamic Programming optimization completed")

        # =================================================
        # RESULTS TABLE
        # =================================================
        st.subheader("📊 Dynamic Programming Results")
        st.dataframe(results_dp, use_container_width=True)

        st.metric(
            label="💰 Minimum Total Cost (Cumulative)",
            value=f"{results_dp['Total_Cost'].sum():,.2f}"
        )

        # =================================================
        # COMPARISON PLOT
        # =================================================
        st.subheader("📈 Fuzzy Import vs Optimal Import (DP)")

        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            results_dp["Month"],
            results_dp["Fuzzy_Import"],
            marker="o",
            label="Fuzzy Import"
        )

        ax.plot(
            results_dp["Month"],
            results_dp["Optimal_Import"],
            marker="s",
            label="Optimal Import (DP)"
        )

        ax.set_xlabel("Month")
        ax.set_ylabel("Import Quantity")
        ax.set_title("Comparison of Import Decisions")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # =================================================
        # DOWNLOAD RESULTS
        # =================================================
        output = "dp_optimization_results.xlsx"

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            results_dp.to_excel(
                writer,
                index=False,
                sheet_name="DP_Results"
            )

        with open(output, "rb") as f:
            st.download_button(
                label="⬇️ Download DP Results (Excel)",
                data=f,
                file_name=output,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
