"""
Smart Industrial Energy Monitor
Author: Hedi Ennouri — ISET Rades
Description: Simulated single-phase AC energy monitoring dashboard built with Streamlit.
NOTE: All measurements are SIMULATED. This is not a real energy meter.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
import time
from datetime import datetime

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Energy Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: #1c1f26;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #2e3340;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: #00d4ff; }
    .metric-label { font-size: 0.85rem; color: #888; margin-top: 4px; }
    .alarm-box {
        background: #3d1515;
        border: 2px solid #ff4444;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        color: #ff6666;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .ok-box {
        background: #0f2e1a;
        border: 2px solid #00cc66;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        color: #00cc66;
        font-size: 1rem;
    }
    .sim-badge {
        background: #2a2200;
        border: 1px solid #ffaa00;
        border-radius: 6px;
        padding: 6px 14px;
        color: #ffaa00;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "timestamp", "voltage", "current", "power_factor",
        "active_power_w", "active_power_kw", "energy_kwh"
    ])
if "total_energy_kwh" not in st.session_state:
    st.session_state.total_energy_kwh = 0.0
if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()
if "running" not in st.session_state:
    st.session_state.running = False

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/lightning-bolt.png", width=60)
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

st.sidebar.subheader("📊 Simulation Parameters")
voltage_base = st.sidebar.slider("Nominal Voltage (V)", 200, 240, 220)
current_base = st.sidebar.slider("Nominal Current (A)", 1.0, 20.0, 8.0, 0.5)
noise_level  = st.sidebar.slider("Noise Level (%)", 0, 20, 5)

st.sidebar.markdown("---")
st.sidebar.subheader("🚨 Alarm Settings")
power_threshold = st.sidebar.number_input("Power Alarm Threshold (W)", 100, 10000, 2000, 100)

st.sidebar.markdown("---")
st.sidebar.subheader("💶 Cost Estimation")
tariff = st.sidebar.number_input("Electricity Tariff (TND/kWh)", 0.01, 1.0, 0.35, 0.01)
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 Control")
col_s1, col_s2 = st.sidebar.columns(2)
start = col_s1.button("▶ Start", use_container_width=True)
stop  = col_s2.button("⏹ Stop",  use_container_width=True)
reset = st.sidebar.button("🗑️ Reset Data", use_container_width=True)

if start: st.session_state.running = True
if stop:  st.session_state.running = False
if reset:
    st.session_state.history = pd.DataFrame(columns=[
        "timestamp","voltage","current","power_factor",
        "active_power_w","active_power_kw","energy_kwh"
    ])
    st.session_state.total_energy_kwh = 0.0
    st.session_state.last_time = time.time()

# ── SIMULATION FUNCTION ───────────────────────────────────────────────────────
def simulate_reading(v_base, i_base, noise_pct):
    """Generate simulated single-phase AC electrical measurements with noise."""
    noise = noise_pct / 100.0
    V  = v_base  * (1 + random.uniform(-noise, noise))
    I  = i_base  * (1 + random.uniform(-noise, noise))
    PF = random.uniform(0.80, 0.99)
    return round(V, 2), round(I, 3), round(PF, 3)

def calculate_power(V, I, PF):
    """P = V × I × PF  (single-phase AC active power)"""
    P_w  = V * I * PF
    P_kw = P_w / 1000.0
    return round(P_w, 2), round(P_kw, 4)

# ── MAIN LAYOUT ───────────────────────────────────────────────────────────────
st.markdown('<div class="sim-badge">⚠️ SIMULATION MODE — Not a real energy meter</div>', unsafe_allow_html=True)
st.title("⚡ Smart Industrial Energy Monitor")
st.caption("Single-phase AC power monitoring dashboard | Hedi Ennouri — ISET Rades")
st.markdown("---")

# ── LIVE READINGS ─────────────────────────────────────────────────────────────
placeholder = st.empty()

# Take one reading (or zeros if stopped)
if st.session_state.running:
    V, I, PF = simulate_reading(voltage_base, current_base, noise_level)
    P_w, P_kw = calculate_power(V, I, PF)

    # Energy accumulation: E = P_kw × Δt_hours
    now = time.time()
    delta_h = (now - st.session_state.last_time) / 3600.0
    st.session_state.last_time = now
    delta_e = P_kw * delta_h
    st.session_state.total_energy_kwh += delta_e

    # Append to history
    new_row = pd.DataFrame([{
        "timestamp":       datetime.now().strftime("%H:%M:%S"),
        "voltage":         V,
        "current":         I,
        "power_factor":    PF,
        "active_power_w":  P_w,
        "active_power_kw": P_kw,
        "energy_kwh":      st.session_state.total_energy_kwh
    }])
    st.session_state.history = pd.concat(
        [st.session_state.history, new_row], ignore_index=True
    ).tail(200)  # keep last 200 readings

else:
    # Use last reading if available, else zeros
    if len(st.session_state.history) > 0:
        last = st.session_state.history.iloc[-1]
        V, I, PF   = last.voltage, last.current, last.power_factor
        P_w, P_kw  = last.active_power_w, last.active_power_kw
    else:
        V, I, PF, P_w, P_kw = 0, 0, 0, 0, 0

E_kwh = st.session_state.total_energy_kwh
cost  = round(E_kwh * tariff, 4)

with placeholder.container():

    # STATUS
    status_col, _, info_col = st.columns([2, 1, 2])
    with status_col:
        if st.session_state.running:
            st.success("🟢 Monitoring ACTIVE")
        else:
            st.warning("🔴 Monitoring STOPPED — Press ▶ Start")

    with info_col:
        st.info(f"📋 Readings recorded: **{len(st.session_state.history)}**")

    st.markdown("---")

    # KPI METRICS
    st.subheader("📊 Live Measurements")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("⚡ Voltage",       f"{V:.1f} V",    delta=None)
    c2.metric("🔌 Current",       f"{I:.2f} A",    delta=None)
    c3.metric("📐 Power Factor",  f"{PF:.3f}",     delta=None)
    c4.metric("💡 Active Power",  f"{P_w:.1f} W",  delta=None)
    c5.metric("🔋 Energy",        f"{E_kwh:.4f} kWh", delta=None)
    c6.metric("💶 Est. Cost",     f"€{cost:.4f}",  delta=None)

    st.markdown("---")

    # ALARM
    st.subheader("🚨 Power Alarm")
    if P_w > power_threshold:
        st.markdown(f"""
        <div class="alarm-box">
            🚨 ALARM — Active power {P_w:.1f} W exceeds threshold of {power_threshold} W!
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="ok-box">
            ✅ Normal — Active power {P_w:.1f} W is within the {power_threshold} W threshold.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # CHARTS
    st.subheader("📈 Live Power Chart")

    if len(st.session_state.history) > 1:
        df = st.session_state.history.copy()

        # Power over time
        fig_power = go.Figure()
        fig_power.add_trace(go.Scatter(
            x=df["timestamp"], y=df["active_power_w"],
            mode="lines", name="Active Power (W)",
            line=dict(color="#00d4ff", width=2),
            fill="tozeroy", fillcolor="rgba(0,212,255,0.08)"
        ))
        fig_power.add_hline(
            y=power_threshold, line_dash="dash",
            line_color="#ff4444", annotation_text=f"Alarm: {power_threshold}W"
        )
        fig_power.update_layout(
            plot_bgcolor="#1c1f26", paper_bgcolor="#1c1f26",
            font_color="white", height=300,
            xaxis=dict(showgrid=False, tickangle=-45, nticks=10),
            yaxis=dict(gridcolor="#2e3340", title="Power (W)"),
            margin=dict(l=40, r=20, t=20, b=60),
            legend=dict(bgcolor="#1c1f26")
        )
        st.plotly_chart(fig_power, use_container_width=True)

        # Two-column charts: Voltage + Current | Energy accumulation
        ch1, ch2 = st.columns(2)

        with ch1:
            st.caption("Voltage & Current over time")
            fig_vi = go.Figure()
            fig_vi.add_trace(go.Scatter(
                x=df["timestamp"], y=df["voltage"],
                name="Voltage (V)", line=dict(color="#ffaa00", width=2)
            ))
            fig_vi.add_trace(go.Scatter(
                x=df["timestamp"], y=df["current"] * 10,  # scaled for visibility
                name="Current x10 (A)", line=dict(color="#00ff99", width=2)
            ))
            fig_vi.update_layout(
                plot_bgcolor="#1c1f26", paper_bgcolor="#1c1f26",
                font_color="white", height=260,
                xaxis=dict(showgrid=False, nticks=6, tickangle=-45),
                yaxis=dict(gridcolor="#2e3340"),
                margin=dict(l=40, r=20, t=10, b=60),
                legend=dict(bgcolor="#1c1f26", font=dict(size=10))
            )
            st.plotly_chart(fig_vi, use_container_width=True)

        with ch2:
            st.caption("Accumulated energy (kWh)")
            fig_e = go.Figure()
            fig_e.add_trace(go.Scatter(
                x=df["timestamp"], y=df["energy_kwh"],
                mode="lines", name="Energy (kWh)",
                line=dict(color="#cc66ff", width=2),
                fill="tozeroy", fillcolor="rgba(204,102,255,0.08)"
            ))
            fig_e.update_layout(
                plot_bgcolor="#1c1f26", paper_bgcolor="#1c1f26",
                font_color="white", height=260,
                xaxis=dict(showgrid=False, nticks=6, tickangle=-45),
                yaxis=dict(gridcolor="#2e3340", title="kWh"),
                margin=dict(l=40, r=20, t=10, b=60),
                legend=dict(bgcolor="#1c1f26", font=dict(size=10))
            )
            st.plotly_chart(fig_e, use_container_width=True)

        # Power factor gauge
        st.caption("Power Factor (latest reading)")
        fig_pf = go.Figure(go.Indicator(
            mode="gauge+number",
            value=PF,
            number={"font": {"color": "white"}},
            gauge={
                "axis": {"range": [0, 1], "tickcolor": "white"},
                "bar": {"color": "#00d4ff"},
                "bgcolor": "#1c1f26",
                "steps": [
                    {"range": [0, 0.7], "color": "#3d1515"},
                    {"range": [0.7, 0.9], "color": "#2a2200"},
                    {"range": [0.9, 1.0], "color": "#0f2e1a"},
                ],
                "threshold": {"line": {"color": "#00cc66", "width": 3}, "value": 0.9}
            }
        ))
        fig_pf.update_layout(
            paper_bgcolor="#1c1f26", font_color="white",
            height=220, margin=dict(l=30, r=30, t=20, b=10)
        )
        st.plotly_chart(fig_pf, use_container_width=True)

    else:
        st.info("Press ▶ Start to begin monitoring and see live charts.")

    st.markdown("---")

    # FORMULA EXPLANATION
    with st.expander("📐 Formulas Used"):
        st.markdown("""
        **Single-phase AC active power:**
        > P (W) = V (V) × I (A) × PF

        **Power in kilowatts:**
        > P (kW) = P (W) / 1000

        **Energy accumulated:**
        > E (kWh) = P (kW) × Δt (hours)

        **Estimated cost:**
        > Cost (€) = E (kWh) × Tariff (tnd/kWh)

        **Power Factor (PF):** ratio of active power to apparent power.
        A PF of 1.0 means all supplied power is consumed usefully.
        A PF below 0.9 is generally considered poor in industrial settings.
        """)

    # RAW DATA TABLE
    with st.expander("📋 Raw Data (last 20 readings)"):
        if len(st.session_state.history) > 0:
            st.dataframe(
                st.session_state.history.tail(20).reset_index(drop=True),
                use_container_width=True
            )
        else:
            st.info("No data yet — press Start.")

# ── AUTO-REFRESH ──────────────────────────────────────────────────────────────
if st.session_state.running:
    time.sleep(1)
    st.rerun()
