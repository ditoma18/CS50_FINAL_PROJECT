import streamlit as st
from project import get_combined_marine_forecast, simulate_gps, calculate_safety_flag

# 1. Page Setup
st.set_page_config(page_title="Lomé Marine Control", page_icon="⚓", layout="wide")
st.title("⚓ Lomé Port Maritime Command")

# 2. Sidebar Controls
st.sidebar.header("Navigation System")
if st.sidebar.button("Fetch Live Telemetry"):
    
    # 3. Fetch Data
    lat, lon = simulate_gps()
    st.sidebar.success(f"Tracking coordinates: {lat}, {lon}")
    
    data_payload = get_combined_marine_forecast(lat, lon)
    
    # 4. Handle Offline Warning Visually
    if not data_payload["is_live"]:
        st.error("⚠️ SATELLITE UPLINK FAILED: Displaying Offline Cached Data")
    else:
        st.success("🛰️ Live Satellite Connection Established")

    # 5. Display the Data in Columns
    st.subheader("Immediate Sea State")
    col1, col2, col3, col4 = st.columns(4)
    
    current_hour = data_payload["timeline"][0]
    
    # Visual Metrics
    col1.metric("Wind Speed", f"{current_hour['wind_speed']} m/s")
    col2.metric("Wave Height", f"{current_hour['wave_height']} m")
    col3.metric("Visibility", f"{current_hour['visibility']} km")
    
    # Safety Flag
    status = calculate_safety_flag(current_hour['wind_speed'], current_hour['wave_height'], current_hour['visibility'])
    col4.metric("SAFETY STATUS", status)

    # 6. Build a Chart (Streamlit makes this incredibly easy)
    st.subheader("24-Hour Wave & Wind Forecast")
    
    # Extract data for the chart
    hours = [item["hour"] for item in data_payload["timeline"]]
    waves = [item["wave_height"] for item in data_payload["timeline"]]
    
    # Display line chart
    st.line_chart(waves)
    
    # 7. Raw Data Table
    st.subheader("Detailed Timeline")
    st.dataframe(data_payload["timeline"], use_container_width=True)