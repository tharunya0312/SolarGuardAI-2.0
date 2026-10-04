import streamlit as st

st.title("🛠️ Maintenance")
st.subheader("AI-guided maintenance recommendations")

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

    if fault_stage <= 1:
        priority = "🟡 MEDIUM PRIORITY"
        action = (
            "Inspect the affected PV strings for early insulation "
            "degradation and abnormal leakage."
        )

    elif fault_stage == 2:
        priority = "🟠 HIGH PRIORITY"
        action = (
            "Inspect the affected PV strings and combiner connections "
            "for insulation or grounding abnormalities."
        )

    elif fault_stage == 3:
        priority = "🔴 CRITICAL PRIORITY"
        action = (
            "Immediately inspect the affected PV strings, DC cables "
            "and combiner sections."
        )

    else:
        priority = "🚨 URGENT"
        action = (
            "Isolate the affected PV section and perform immediate "
            "DC insulation and ground-fault inspection."
        )

    st.error("🔴 MAINTENANCE REQUIRED")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Priority", priority)

    with col2:
        st.metric("Fault Stage", f"{fault_stage}/4")

    with col3:
        st.metric("Affected Strings", len(selected_strings))

    st.markdown("---")

    st.header("📍 Maintenance Target")

    st.info(
        f"{primary_row['Inverter']} → "
        f"{primary_row['Combiner']} → "
        f"{primary_row['String']}"
    )

    st.markdown("---")

    st.header("Recommended Action")

    st.warning(action)

    st.markdown("---")

    st.header("🔧 Maintenance Checklist")

    st.checkbox("Inspect DC cable insulation")
    st.checkbox("Check cable connectors")
    st.checkbox("Inspect combiner connection")
    st.checkbox("Perform insulation resistance test")
    st.checkbox("Verify ground-fault condition")

else:

    st.success("🟢 NO MAINTENANCE ALERT")

    st.write(
        "No abnormal condition currently requires maintenance."
    )

    st.info(
        "Maintenance recommendations will appear automatically "
        "when SolarGuard AI detects a fault."
    )