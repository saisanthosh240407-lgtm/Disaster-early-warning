import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# CRITICAL FOR V1.5.7.0: This must be the absolute first Streamlit command
st.set_page_config(page_title="IMD-EWS Dashboard", layout="wide")

# App Header
st.title("🚨 Intelligent Multi-Hazard Early Warning System (IMD-EWS)")
st.markdown("### Situational Awareness & Automated Threat Analysis Dashboard")
st.markdown("---")

# --- BACKEND: DATA SIMULATION & PROCESSING ---

@st.cache_data # Caching works efficiently to keep older version responsive
def generate_sensor_data():
    # Simulating data ingestion from local IoT sensors (Seismic, Water, Gas)
    np.random.seed(42)
    data_size = 1000
    
    df = pd.DataFrame({
        # FIXED: Changed freq='H' to freq='h' to satisfy new Pandas constraints
        'Timestamp': pd.date_range(start='2026-01-01', periods=data_size, freq='h'),
        'Seismic_Activity': np.random.lognormal(0, 0.5, data_size),
        'Water_Level_Meters': np.random.uniform(1.0, 15.0, data_size),
        'Gas_Levels_PPM': np.random.normal(250, 50, data_size),
        'Region': np.random.choice(['Zone_North', 'Zone_South', 'Zone_East', 'Zone_West'], data_size)
    })
    
    # Advanced Numerical Analysis (The "Hazard Index")
    weights = {'seismic': 0.5, 'water': 0.3, 'gas': 0.2}
    
    # Vectorized computation for low-latency assessment
    df['Threat_Score'] = (df['Seismic_Activity'] * weights['seismic']) + \
                         (df['Water_Level_Meters'] * weights['water']) + \
                         ((df['Gas_Levels_PPM'] / 100) * weights['gas'])
    return df

# Load the data
df = generate_sensor_data()

# Calculate Automated Alert Threshold (Mean + 2 * Standard Deviation)
alert_threshold = df['Threat_Score'].mean() + (2 * df['Threat_Score'].std())

# --- FRONTEND: USER INTERFACE LAYOUT ---

# Sidebar for controls
st.sidebar.header("📊 System Controls")
selected_region = st.sidebar.selectbox("Filter by Region Location", ['All Regions', 'Zone_North', 'Zone_South', 'Zone_East', 'Zone_West'])

# Filter data based on sidebar selection
if selected_region != 'All Regions':
    filtered_df = df[df['Region'] == selected_region]
else:
    filtered_df = df

# Metric Cards Layout
st.subheader("📈 Real-Time Critical Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Current Alert Threshold", value=f"{alert_threshold:.2f}")
with col2:
    # Find how many active threats cross the safety line
    total_alerts = df[df['Threat_Score'] > alert_threshold].shape[0]
    st.metric(label="🚨 Active System-Wide Anomalies", value=total_alerts, delta="Immediate Action Required" if total_alerts > 0 else "Normal")
with col3:
    highest_zone = df.groupby('Region')['Threat_Score'].mean().idxmax()
    st.metric(label="📍 Highest Risk Zone (Pre-position Supplies)", value=highest_zone)

st.markdown("---")

# Main Visualizations Tabs
st.subheader("🔍 Analytical Framework")
tab1, tab2, tab3 = st.tabs(["🗺️ Regional Hotspots", "📉 Temporal Spike Analysis", "📋 Raw Sensor Log Data"])

with tab1:
    st.markdown("#### Average Hazard Risk per Localized Zone (Strategic Resource Allocation)")
    
    # Create the Bar Plot
    fig, ax = plt.subplots(figsize=(10, 4))
    # FIXED: Handled explicit palette assignment safety for older rendering backend
    sns.barplot(data=df, x='Region', y='Threat_Score', estimator=np.mean, palette=sns.color_palette("rocket"), ax=ax)
    ax.set_title("Average Hazard Risk per Localized Zone")
    st.pyplot(fig)
    
    st.info("💡 *Operational Insight:* Emergency vehicles and critical relief items should be pre-positioned in the zones showing the highest bars to maximize situational readiness.")

with tab2:
    st.markdown("#### Real-Time Multi-Hazard Monitoring & Threshold Crossings")
    
    # Create the Line Plot
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=filtered_df, x='Timestamp', y='Threat_Score', hue='Region', ax=ax2)
    ax2.axhline(alert_threshold, color='red', linestyle='--', label='Alert Level Threshold')
    ax2.set_title("IMD-EWS Real-Time Situational Awareness Dashboard")
    plt.legend()
    st.pyplot(fig2)
    
    st.warning("⚠️ *Low Latency Alert Protocol:* Any spikes peaking above the red dashed threshold automatically bypass human intervention to trigger automated warnings (MQTT/Firebase text blasts).")

with tab3:
    st.markdown("#### Ingested IoT Telemetry Node Data Stream")
    # Highlight high threat rows instantly in the frontend UI dashboard view
    st.dataframe(filtered_df.style.highlight_max(axis=0, subset=['Threat_Score']))