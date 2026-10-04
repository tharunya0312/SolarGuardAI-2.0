import streamlit as st

st.set_page_config(
    page_title="SolarGuard AI",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ SolarGuard AI")
st.subheader("Industrial Solar PV Fault Intelligence Platform")

st.markdown("---")

st.header("Company Login")

company = st.text_input("Company / Plant Name")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login", type="primary"):
    if username and password:
        st.success("Login successful!")
        st.info("Proceed to Plant Selection from the sidebar.")
    else:
        st.warning("Please enter username and password.")