import streamlit as st
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Sales & Revenue Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales & Revenue Insights Dashboard")
st.markdown("Interactive dashboard to explore sales performance, revenue trends, and product insights.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv", parse_dates=["order_date"])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
regions = st.sidebar.multiselect("Select Region:", df["region"].unique(), default=df["region"].unique())
products = st.sidebar.multiselect("Select Product:", df["product"].unique(), default=df["product"].unique())
channels = st.sidebar.multiselect("Select Channel:", df["channel"].unique(), default=df["channel"].unique())
date_range = st.sidebar.date_input("Select Date Range:", [df["order_date"].min(), df["order_date"].max()])

# Filter data
filtered_df = df[
    (df["region"].isin(regions)) &
    (df["product"].isin(products)) &
    (df["channel"].isin(channels)) &
    (df["order_date"].between(date_range[0], date_range[1]))
]

# KPIs
total_revenue = filtered_df["revenue"].sum()
total_units = filtered_df["units_sold"].sum()
avg_order_value = filtered_df["revenue"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Total Units Sold", f"{total_units:,}")
col3.metric("💹 Avg Order Value", f"${avg_order_value:,.2f}")

# Charts
st.markdown("### 📈 Revenue Over Time")
revenue_chart = (
    alt.Chart(filtered_df)
    .mark_line(point=True)
    .encode(
        x="order_date:T",
        y="revenue:Q",
        color="region:N",
        tooltip=["order_date", "revenue", "region"]
    )
    .interactive()
)
st.altair_chart(revenue_chart, use_container_width=True)

st.markdown("### 🏆 Top 10 Products by Revenue")
top_products = (
    filtered_df.groupby("product")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
    .head(10)
)
bar_chart = alt.Chart(top_products).mark_bar().encode(
    x="revenue:Q", y=alt.Y("product:N", sort='-x'), color="product:N", tooltip=["product", "revenue"]
)
st.altair_chart(bar_chart, use_container_width=True)

st.markdown("### 🌎 Revenue by Region")
region_chart = alt.Chart(filtered_df).mark_bar().encode(
    x="region:N", y="revenue:Q", color="region:N", tooltip=["region", "revenue"]
)
st.altair_chart(region_chart, use_container_width=True)

# Download filtered data
st.markdown("### 📤 Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_sales_data.csv", "text/csv")

st.caption("© 2025 Sales & Revenue Insights Dashboard | Built with Streamlit, Pandas, and Altair")
