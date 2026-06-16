import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Forecasting Dashboard", layout="wide")

st.title("📈 Sales Forecasting Dashboard")
st.write("Analyze trends, filter data, and forecast future sales like someone who might get hired.")

# Load model
model = joblib.load("model.pkl")

# Load data
df = pd.read_csv("sales_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

df["day_index"] = np.arange(len(df))

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

show_rolling = st.sidebar.checkbox("Show 3-Day Rolling Average", True)

forecast_days = st.sidebar.slider("Forecast Days", 1, 30, 7)

# ---------------- FILTER DATA ----------------
start_date, end_date = date_range
filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) & 
                 (df["date"] <= pd.to_datetime(end_date))]

# ---------------- KPIs ----------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{filtered_df['sales'].sum():,.0f}")
col2.metric("Average Sales", f"{filtered_df['sales'].mean():,.0f}")
col3.metric("Max Sales", f"{filtered_df['sales'].max():,.0f}")

# ---------------- CHARTS ----------------
st.subheader("📉 Sales Analysis")

chart_col1, chart_col2 = st.columns(2)

# Left chart: historical
with chart_col1:
    fig1, ax1 = plt.subplots(figsize=(5,3))
    ax1.plot(filtered_df["date"], filtered_df["sales"], marker="o", label="Sales")

    if show_rolling:
        filtered_df["rolling"] = filtered_df["sales"].rolling(3).mean()
        ax1.plot(filtered_df["date"], filtered_df["rolling"], linestyle="--", label="Rolling Avg")

    ax1.set_title("Filtered Sales")
    ax1.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig1)

# ---------------- FORECAST ----------------
last_index = df["day_index"].max()

future_index = np.arange(last_index + 1, last_index + 1 + forecast_days)
future_preds = model.predict(future_index.reshape(-1, 1))

future_dates = pd.date_range(
    start=df["date"].max() + pd.Timedelta(days=1),
    periods=forecast_days
)

forecast_df = pd.DataFrame({
    "date": future_dates,
    "predicted_sales": future_preds
})

# Right chart: forecast
with chart_col2:
    fig2, ax2 = plt.subplots(figsize=(5,3))
    ax2.plot(df["date"], df["sales"], label="Actual")
    ax2.plot(forecast_df["date"], forecast_df["predicted_sales"], label="Forecast")

    ax2.set_title("Forecast vs Actual")
    ax2.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# ---------------- TABLE ----------------
st.subheader("📄 Forecast Data")
st.dataframe(forecast_df)

# ---------------- DOWNLOAD ----------------
csv = forecast_df.to_csv(index=False).encode()

st.download_button(
    "⬇️ Download Forecast CSV",
    csv,
    "forecast.csv",
    "text/csv"
)