import streamlit as st

st.title("📍 Fault Localization")
st.subheader("Identify the exact PV section affected by the fault")

st.markdown("---")

fault_active = st.session_state.get("fault_active", False)
selected_strings = st.session_state.get("selected_strings", [])
plant = st.session_state.get("plant", None)

if fault_active and selected_strings and plant is not None:

    st.error("🔴 FAULT LOCATED")

    affected_rows = plant[
        plant["String"].isin(selected_strings)
    ]

    affected_inverters = affected_rows["Inverter"].unique()
    affected_combiners = affected_rows["Combiner"].unique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**Primary Inverter**")
        for inverter in affected_inverters:
            st.write(f"⚡ {inverter}")

    with col2:
        st.warning("**Combiner Box**")
        for combiner in affected_combiners:
            st.write(f"📦 {combiner}")

    with col3:
        st.error("**Affected Strings**")
        for string in selected_strings:
            st.write(f"🔴 {string}")

    st.markdown("---")

    st.header("📌 Fault Path")

    primary_row = affected_rows.iloc[0]

    st.code(
        f"{primary_row['Inverter']}\n"
        f"    ↓\n"
        f"{primary_row['Combiner']}\n"
        f"    ↓\n"
        f"{primary_row['String']}\n"
        f"    ↓\n"
        f"DC Cable / Ground Fault"
    )

    st.warning(
        "Recommended inspection area: "
        "affected PV strings, DC cables and associated combiner connections."
    )

else:

    st.success("🟢 NO FAULT CURRENTLY LOCALIZED")

    st.info(
        "When a fault is detected, SolarGuard AI will identify "
        "the affected inverter, combiner box and PV strings."
    )