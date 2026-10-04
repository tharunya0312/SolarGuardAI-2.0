import streamlit as st

st.title("🧠 AI Diagnosis")
st.subheader("Explainable Solar PV Fault Analysis")

st.markdown("---")

fault_active = st.session_state.get("fault_active", False)
fault_stage = st.session_state.get("fault_stage", 0)
selected_strings = st.session_state.get("selected_strings", [])
plant = st.session_state.get("plant", None)

if fault_active and selected_strings and plant is not None:

    affected_rows = plant[
        plant["String"].isin(selected_strings)
    ]

    primary_row = affected_rows.iloc[0]

    if fault_stage == 1:
        severity = "Warning"
        confidence = 82
        anomaly_score = 4.2
    elif fault_stage == 2:
        severity = "Severe"
        confidence = 89
        anomaly_score = 6.4
    elif fault_stage == 3:
        severity = "Critical"
        confidence = 94
        anomaly_score = 8.7
    else:
        severity = "Extreme"
        confidence = 98
        anomaly_score = 9.6

    st.error("🔴 DC GROUND-FAULT CONDITION DETECTED")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("AI Confidence", f"{confidence}%")

    with col2:
        st.metric("Fault Severity", severity)

    with col3:
        st.metric("Anomaly Score", f"{anomaly_score}/10")

    st.markdown("---")

    st.header("🔎 Explainable Fault Evidence")

    st.write(
        "SolarGuard AI identified abnormal electrical behaviour "
        "in the selected PV strings."
    )

    st.write("🔴 DC voltage deviation")
    st.write("🔴 DC current deviation")
    st.write("🔴 DC power reduction")
    st.write("🔴 Abnormal leakage current")

    st.markdown("---")

    st.header("📍 AI Diagnosis")

    st.info(
        f"The electrical signature is consistent with a possible "
        f"DC insulation or ground-fault condition affecting "
        f"{len(selected_strings)} PV strings."
    )

    st.write("**Primary Location:**")
    st.write(
        f"{primary_row['Inverter']} → "
        f"{primary_row['Combiner']} → "
        f"{primary_row['String']}"
    )

    st.markdown("---")

    st.header("⚠️ AI Interpretation")

    if fault_stage <= 1:
        st.warning(
            "Early abnormal behaviour detected. "
            "Inspection is recommended before the condition worsens."
        )
    elif fault_stage <= 2:
        st.warning(
            "Fault indicators are increasing. "
            "The affected PV section should be inspected soon."
        )
    elif fault_stage <= 3:
        st.error(
            "Strong DC-side fault signature detected. "
            "Immediate inspection is recommended."
        )
    else:
        st.error(
            "Severe fault condition detected. "
            "The affected PV section should be isolated and inspected immediately."
        )

else:

    st.success("🟢 NO SIGNIFICANT FAULT DETECTED")

    st.write(
        "The monitored electrical parameters are currently "
        "within the expected operating range."
    )

    st.info(
        "Start the fault simulation from the main SolarGuard AI "
        "page to view the AI diagnosis."
    )