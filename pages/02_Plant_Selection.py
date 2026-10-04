import streamlit as st

st.title("🏭 Plant Selection")
st.subheader("Select the solar PV plant you want to monitor")

plants = {
    "Solar Plant Alpha": "Tamil Nadu",
    "Solar Plant Beta": "Karnataka",
    "Solar Plant Gamma": "Rajasthan"
}

selected_plant = st.selectbox(
    "Select Plant",
    list(plants.keys())
)

st.info(f"📍 Location: {plants[selected_plant]}")

if st.button("Open Plant", type="primary"):
    st.success(f"Connected to {selected_plant}")
    st.session_state["selected_plant"] = selected_plant
