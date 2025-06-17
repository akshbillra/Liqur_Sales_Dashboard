import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="Live Sales Dashboard", layout="wide")
st.title("📊 Live Product Sales Dashboard")

# Load Excel
def load_data():
    return pd.read_excel("Personal Aksh_Free.xlsx", header=3)

df = load_data()
df.columns = df.columns.str.strip().str.lower()

# Sidebar filters
st.sidebar.header("🔍 Apply Filters (Optional)")
clients = df['party name'].dropna().unique() if 'party name' in df.columns else []
months = df['month'].dropna().unique() if 'month' in df.columns else []

selected_client = st.sidebar.selectbox("Client", ["All"] + sorted(list(clients)))
selected_month = st.sidebar.selectbox("Month", ["All"] + sorted(list(months)))

# Apply filters
filtered_df = df.copy()
if selected_client != "All":
    filtered_df = filtered_df[filtered_df['party name'] == selected_client]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df['month'] == selected_month]

# Use filtered_df only (either full or filtered)
data_to_use = filtered_df

# Show table
with st.expander("📄 Show Data Used in Charts"):
    st.dataframe(data_to_use)

# --- Chart: Brand Sales ---
if "brand name" in data_to_use.columns and "total cases" in data_to_use.columns:
    sales_by_brand = data_to_use.groupby("brand name")["total cases"].sum().reset_index()
    fig_brand = px.bar(sales_by_brand, x="brand name", y="total cases", color="brand name", title="Total Sales by Brand")
    st.plotly_chart(fig_brand, use_container_width=True)

# --- Chart: Location Sales ---
if "bwh" in data_to_use.columns and "total cases" in data_to_use.columns:
    sales_by_bwh = data_to_use.groupby("bwh")["total cases"].sum().reset_index()
    fig_bwh = px.bar(sales_by_bwh, x="bwh", y="total cases", color="bwh", title="Sales by Location (BWH)")
    st.plotly_chart(fig_bwh, use_container_width=True)

# --- Chart: Daily Trend ---
if "date" in data_to_use.columns and "total cases" in data_to_use.columns:
    daily_sales = data_to_use.groupby("date")["total cases"].sum().reset_index()
    fig_date = px.line(daily_sales, x="date", y="total cases", title="📅 Daily Sales Trend")
    st.plotly_chart(fig_date, use_container_width=True)
