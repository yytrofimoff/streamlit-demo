import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("📈 FX Rates vs Prediction")

# --- Load data ---
df = pd.read_csv("data/latest.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# --- Sidebar filters ---
currency = st.sidebar.selectbox(
    "Currency",
    sorted(df["currency"].unique())
)

base = st.sidebar.selectbox(
    "Base currency",
    sorted(df["base"].unique())
)

df_filtered = df[
    (df["currency"] == currency) &
    (df["base"] == base)
].sort_values("date")

# --- Get latest prediction ---
latest_row = df_filtered.iloc[-1]
prediction = latest_row["predicted_rate"]

# --- Layout ---
col1, col2 = st.columns([4, 1])

# --- Chart ---
with col1:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["rate"],
        mode="lines+markers",
        name="Actual",
        line=dict(width=3)
    ))

    fig.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["predicted_rate"],
        mode="lines+markers",
        name="Prediction",
        line=dict(dash="dash", width=3)
    ))

    fig.update_layout(
        height=500,
        title=f"{base} → {currency}",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Prediction box ---
with col2:
    st.markdown("### 🔮 Tomorrow")

    if pd.notnull(prediction):
        st.markdown(
            f"""
            <div style="color:red; font-size:28px; font-weight:bold;">
                {prediction:.4f}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='color:red;'>No prediction</div>",
            unsafe_allow_html=True
        )