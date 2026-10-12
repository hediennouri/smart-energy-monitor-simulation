# ⚡ Smart Industrial Energy Monitor

> A simulated single-phase AC energy monitoring dashboard built with Python and Streamlit.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)

> ⚠️ **SIMULATION ONLY** — All measurements are generated in software. This is not a real energy meter. Do not connect improvised circuits to mains electricity.

---

## 📋 Overview

This project implements a real-time industrial energy monitoring dashboard using simulated electrical measurements. It demonstrates Industry 4.0 concepts — live KPI visualization, alarm management, and cost estimation — without requiring any physical hardware.

---

## 🖥️ Dashboard Features

| Feature | Description |
|---|---|
| **Live KPIs** | Voltage, Current, Power Factor, Active Power, Energy, Cost |
| **Power Alarm** | Configurable threshold with visual alert |
| **Cost Estimation** | User-defined tariff in €/kWh |
| **Live Charts** | Power over time, Voltage & Current, Energy accumulation, PF gauge |
| **Raw Data Table** | Last 20 readings with all calculated values |
| **Formula Panel** | Explains every calculation used |

---

## 📐 Formulas

**Single-phase AC active power:**
```
P (W) = V (V) × I (A) × PF
```

**Power in kilowatts:**
```
P (kW) = P (W) / 1000
```

**Energy accumulated:**
```
E (kWh) = P (kW) × Δt (hours)
```

**Estimated electricity cost:**
```
Cost (€) = E (kWh) × Tariff (€/kWh)
```

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/smart-energy-monitor.git
cd smart-energy-monitor
```

### 2. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
python -m streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## ⚙️ Configuration (sidebar)

| Parameter | Description | Default |
|---|---|---|
| Nominal Voltage | Base voltage for simulation (V) | 220 V |
| Nominal Current | Base current for simulation (A) | 8.0 A |
| Noise Level | Random variation (%) | 5% |
| Power Alarm Threshold | Alarm triggers above this (W) | 2000 W |
| Electricity Tariff | Cost per kWh (€) | €0.18 |

---

## 🗂️ Project Structure

```
smart-energy-monitor/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚠️ Limitations

- All measurements are **simulated** — values are generated using Python's `random` module with configurable noise
- Energy accumulation resets on page refresh unless session state is preserved
- No real sensor, PLC, or hardware connection of any kind
- Power factor is randomly varied between 0.80 and 0.99 per reading

---

## 👤 Author

**Hedi Ennouri**
Automation and Industrial Computing — ISET Rades
2026/2027
