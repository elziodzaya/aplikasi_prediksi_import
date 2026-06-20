import matplotlib.pyplot as plt
import streamlit as st


# ======================================================
# KPI METRIC CARDS
# ======================================================
def show_kpi_metrics(kpi):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📦 Total Import", f"{int(kpi['Total Import']):,}")
    col2.metric("💰 Total Cost", f"{int(kpi['Total Cost']):,}")
    col3.metric("📊 Avg Inventory", f"{int(kpi['Average Inventory']):,}")
    col4.metric("🎯 Service Level", f"{kpi['Service Level'] * 100:.1f}%")

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("⚠️ Stockout Rate", f"{kpi['Stockout Rate'] * 100:.1f}%")
    col6.metric("📈 Overstock Rate", f"{kpi['Overstock Rate'] * 100:.1f}%")
    col7.metric("💸 Cost / Unit Demand", f"{kpi['Cost per Unit Demand']:.2f}")
    col8.metric("🔁 Inventory Turnover", f"{kpi['Inventory Turnover']:.2f}")


# ======================================================
# INVENTORY PROFILE PLOT (FIXED)
# ======================================================
def plot_inventory_profile(df_policy):
    fig, ax = plt.subplots(figsize=(9, 4))

    ax.plot(
        df_policy["Month"].astype(str),
        df_policy["Ending_Stock"],
        marker="o"
    )

    ax.set_title("Inventory Level Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("Ending Stock")
    ax.grid(True)

    st.pyplot(fig)
