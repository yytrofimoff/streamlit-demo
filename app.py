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
currency = st.sidebar.selectbox("Currency", sorted(df["currency"].unique()))

base = st.sidebar.selectbox("Base currency", sorted(df["base"].unique()))

df_filtered = df[(df["currency"] == currency) & (df["base"] == base)].sort_values(
    "date"
)

# --- Split historical vs future ---
df_hist = df_filtered[df_filtered["rate"].notna()]
df_future = df_filtered[df_filtered["rate"].isna()]

# --- Get tomorrow prediction ---
prediction = None
if not df_future.empty:
    prediction = df_future.iloc[-1]["predicted_rate"]

# --- Layout ---
col1, col2 = st.columns([4, 1])

# --- Chart ---
with col1:
    fig = go.Figure()

    # Actual values
    fig.add_trace(
        go.Scatter(
            x=df_hist["date"],
            y=df_hist["rate"],
            mode="lines+markers",
            name="Actual",
            line=dict(width=3),
        )
    )

    # Predictions aligned to history
    fig.add_trace(
        go.Scatter(
            x=df_hist["date"],
            y=df_hist["predicted_rate"],
            mode="lines+markers",
            name="Prediction",
            line=dict(dash="dash", width=3),
        )
    )

    # Future point (tomorrow)
    if not df_future.empty:
        fig.add_trace(
            go.Scatter(
                x=df_future["date"],
                y=df_future["predicted_rate"],
                mode="markers",
                name="Tomorrow",
                marker=dict(color="red", size=10),
            )
        )

    fig.update_layout(height=500, title=f"{base} → {currency}", template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

# --- Prediction box ---
with col2:
    st.markdown("### 🔮 Tomorrow")

    if prediction is not None:
        st.markdown(
            f"""
            <div style="color:red; font-size:28px; font-weight:bold;">
                {prediction:.4f}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='color:red;'>No prediction</div>", unsafe_allow_html=True
        )
