import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="Live Sales Dashboard", layout="wide")

st.title("📊 Live Product Sales Dashboard")

# Add auto-refresh every 60 seconds
countdown = st.empty()
time.sleep(1)


# Read Excel File
def load_data():
    return pd.read_excel("Personal Aksh_Free.xlsx",  header=3)

df = load_data()
df.columns = df.columns.str.strip().str.lower()
# Show Raw Data
with st.expander("📄 Show Raw Data"):
    st.dataframe(df)

st.subheader("📌 Total Sales by Cases")

# Now use lowercase column names
sales_by_product = df.groupby("brand name")["total cases"].sum().reset_index()

fig_product = px.bar(
    sales_by_product,
    x="brand name",
    y="total cases",
    color="brand name",  # no 'Product' column anymore
    title="Total Quantity Sold by Brand"
)

st.plotly_chart(fig_product, use_container_width=True)

# Grouping by 'bwh' if exists
if "bwh" in df.columns and "total cases" in df.columns:
    sales_by_location = df.groupby("bwh")["total cases"].sum().reset_index()

    import plotly.express as px
    fig = px.bar(
        sales_by_location,
        x="bwh",
        y="total cases",
        color="bwh",
        title="📍 Total Sales by Location (BWH)"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ 'bwh' or 'total cases' column missing!")

if 'date' in df.columns and 'total cases' in df.columns:
    daily_sales = df.groupby('date')['total cases'].sum().reset_index()

    import plotly.express as px
    fig = px.line(daily_sales, x='date', y='total cases', title='Daily Sales Over Time')
    st.plotly_chart(fig)
else:
    st.warning("Required columns 'date' or 'total cases' not found.")

# Refresh Instruction
st.info("🔄 To auto-refresh the dashboard, press **R** in your browser or refresh manually after Excel update.")

