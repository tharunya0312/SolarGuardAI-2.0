import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.title("📄 Reports")
st.subheader("Solar PV fault and maintenance reports")

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
        action = (
            "Inspect the affected PV strings for early insulation "
            "degradation and abnormal leakage."
        )

    elif fault_stage == 2:
        severity = "Severe"
        confidence = 89
        action = (
            "Inspect the affected PV strings and combiner connections "
            "for insulation or grounding abnormalities."
        )

    elif fault_stage == 3:
        severity = "Critical"
        confidence = 94
        action = (
            "Immediately inspect the affected PV strings, DC cables "
            "and combiner sections."
        )

    else:
        severity = "Extreme"
        confidence = 98
        action = (
            "Isolate the affected PV section and perform immediate "
            "DC insulation and ground-fault inspection."
        )

    st.header("Plant Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Plant", "Solar Plant Alpha")

    with col2:
        st.metric("Report Status", "Fault Detected")

    with col3:
        st.metric(
            "Generated",
            datetime.now().strftime("%d-%m-%Y")
        )

    st.markdown("---")

    st.header("🚨 Fault Summary")

    st.write("**Fault Type:** DC Ground Fault")
    st.write(f"**Primary Inverter:** {primary_row['Inverter']}")
    st.write(f"**Primary Combiner:** {primary_row['Combiner']}")
    st.write(f"**Primary String:** {primary_row['String']}")
    st.write(f"**Affected Strings:** {len(selected_strings)}")
    st.write(f"**Severity:** {severity}")
    st.write(f"**AI Confidence:** {confidence}%")

    st.markdown("---")

    st.header("📍 Affected PV Strings")

    for string in selected_strings:
        st.write(f"🔴 {string}")

    st.markdown("---")

    st.header("🛠️ Recommended Action")

    st.warning(action)

    st.markdown("---")

    if st.button("📄 Generate Report", type="primary"):

        report_path = "SolarGuard_AI_Fault_Report.pdf"

        doc = SimpleDocTemplate(
            report_path,
            pagesize=A4
        )

        styles = getSampleStyleSheet()
        story = []

        story.append(
            Paragraph(
                "SolarGuard AI - Solar PV Fault Report",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                "Fault Summary",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"Plant: Solar Plant Alpha<br/>"
                f"Fault Type: DC Ground Fault<br/>"
                f"Primary Inverter: {primary_row['Inverter']}<br/>"
                f"Primary Combiner: {primary_row['Combiner']}<br/>"
                f"Primary String: {primary_row['String']}<br/>"
                f"Affected Strings: {len(selected_strings)}<br/>"
                f"Severity: {severity}<br/>"
                f"AI Confidence: {confidence}%",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                "Affected PV Strings",
                styles["Heading2"]
            )
        )

        for string in selected_strings:
            story.append(
                Paragraph(
                    f"- {string}",
                    styles["Normal"]
                )
            )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                "Recommended Maintenance Action",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                action,
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                "SolarGuard AI provides explainable fault detection, "
                "localization and maintenance guidance for solar PV systems.",
                styles["Normal"]
            )
        )

        doc.build(story)

        with open(report_path, "rb") as pdf_file:

            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_file,
                file_name="SolarGuard_AI_Fault_Report.pdf",
                mime="application/pdf"
            )

        st.success("✅ PDF report generated successfully.")

else:

    st.header("Plant Report")

    st.success("🟢 Plant operating normally")

    st.write("**Fault Type:** None detected")
    st.write("**Severity:** Normal")
    st.write("**Affected Strings:** 0")

    st.info(
        "No active fault is currently available for reporting. "
        "Start the fault simulation from the main application "
        "to generate a fault report."
    )
