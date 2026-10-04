import streamlit as st

st.title("🚨 Fault Center")
st.subheader("Real-time Solar PV fault monitoring")

st.markdown("---")

# Read fault state from the main SolarGuard AI application
fault_active = st.session_state.get("fault_active", False)
fault_stage = st.session_state.get("fault_stage", 0)
selected_strings = st.session_state.get("selected_strings", [])

if fault_active:

    st.error("🔴 ACTIVE DC FAULT")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Plant Status", "🔴 FAULT")

    with col2:
        st.metric("Active Faults", len(selected_strings))

    with col3:
        st.metric("Fault Stage", f"{fault_stage}/4")

    st.markdown("---")

    st.header("Fault Detection")

    st.warning(
        "Abnormal DC electrical behaviour detected. "
        "SolarGuard AI is analysing the affected PV strings."
    )

    st.header("Affected PV Strings")

    for string in selected_strings:
        st.write(f"🔴 {string}")

    st.markdown("---")

    st.header("System Monitoring")

    st.write("🔴 DC Voltage")
    st.write("🔴 DC Current")
    st.write("🔴 DC Power")
    st.write("🔴 Leakage Current")
    st.write("🟢 Inverter Status")

else:

    st.success("🟢 PLANT HEALTHY")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Plant Status", "🟢 HEALTHY")

    with col2:
        st.metric("Active Faults", "0")

    with col3:
        st.metric("Energy at Risk", "0 kW")

    st.info(
        "No abnormal ground-fault condition detected. "
        "Solar PV strings are operating within normal electrical limits."
    )

    st.header("System Monitoring")

    st.write("• DC Voltage")
    st.write("• DC Current")
    st.write("• DC Power")
    st.write("• Leakage Current")
    st.write("• Inverter Status")

    st.success("✅ Monitoring system is active")