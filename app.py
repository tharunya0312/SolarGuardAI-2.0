import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="SolarGuard AI",
    page_icon="☀️",
    layout="wide"
)
st.title("☀️ SolarGuard AI")
st.caption("Explainable DC Fault Intelligence & Localization for Solar PV Systems")
# =========================================================
# CONFIGURATION
# =========================================================

INVERTERS = 3
COMBINERS_PER_INVERTER = 4
STRINGS_PER_COMBINER = 10

TOTAL_STRINGS = INVERTERS * COMBINERS_PER_INVERTER * STRINGS_PER_COMBINER


# =========================================================
# CREATE SIMULATED SOLAR PV PLANT
# =========================================================

def create_plant():

    rows = []

    for inv in range(1, INVERTERS + 1):

        for comb in range(1, COMBINERS_PER_INVERTER + 1):

            for string in range(1, STRINGS_PER_COMBINER + 1):

                rows.append({
                    "Inverter": f"INV-{inv}",
                    "Combiner": f"CB-{inv}-{comb:02d}",
                    "String": f"S-{inv}-{comb:02d}-{string:02d}",
                    "Voltage": np.random.normal(610, 7),
                    "Current": np.random.normal(8.5, 0.20),
                    "Power": np.random.normal(5.2, 0.12),
                    "Leakage": np.random.normal(0.15, 0.03)
                })

    return pd.DataFrame(rows)


# =========================================================
# SESSION STATE
# =========================================================

if "plant" not in st.session_state:
    st.session_state.plant = create_plant()

if "fault_active" not in st.session_state:
    st.session_state.fault_active = False

if "fault_stage" not in st.session_state:
    st.session_state.fault_stage = 0

if "fault_target" not in st.session_state:
    st.session_state.fault_target = st.session_state.plant.iloc[0]["String"]


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("☀️ SolarGuard AI")

st.sidebar.markdown("### Plant Control")

target = st.sidebar.selectbox(
    "Select PV String 1",
    st.session_state.plant["String"].tolist()
)

target2 = st.sidebar.selectbox(
    "Select PV String 2",
    st.session_state.plant["String"].tolist()
)

target3 = st.sidebar.selectbox(
    "Select PV String 3",
    st.session_state.plant["String"].tolist()
)

target4 = st.sidebar.selectbox(
    "Select PV String 4",
    st.session_state.plant["String"].tolist()
)

target5 = st.sidebar.selectbox(
    "Select PV String 5",
    st.session_state.plant["String"].tolist()
)

st.session_state.fault_target = target
st.session_state.selected_strings = [target, target2, target3, target4, target5]
st.sidebar.markdown("---")

if st.sidebar.button(
    "🚨 Start Fault Simulation",
    use_container_width=True
):

    st.session_state.fault_active = True
    st.session_state.fault_stage = 1

if st.sidebar.button(
    "➡️ Increase Fault Severity",
    use_container_width=True
):

    if st.session_state.fault_active:
        st.session_state.fault_stage = min(
            st.session_state.fault_stage + 1,
            4
        )

if st.sidebar.button(
    "✅ Reset Plant",
    use_container_width=True
):

    st.session_state.plant = create_plant()
    st.session_state.fault_active = False
    st.session_state.fault_stage = 0


st.sidebar.markdown("---")

st.sidebar.info(
    "Simulation mode: PV electrical signals are generated "
    "to demonstrate DC ground/insulation fault intelligence."
)


# =========================================================
# APPLY FAULT PROGRESSION
# =========================================================

plant = st.session_state.plant.copy()

if st.session_state.fault_active:

    selected_strings = [
        target,
        target2,
        target3,
        target4,
        target5
    ]

    stage = st.session_state.fault_stage

    fault_profiles = {

        1: {
            "voltage": 0.94,
            "current": 0.91,
            "power": 0.84,
            "leakage": 1.5
        },

        2: {
            "voltage": 0.86,
            "current": 0.78,
            "power": 0.67,
            "leakage": 3.2
        },

        3: {
            "voltage": 0.76,
            "current": 0.64,
            "power": 0.50,
            "leakage": 5.8
        },

        4: {
            "voltage": 0.68,
            "current": 0.55,
            "power": 0.38,
            "leakage": 8.8
        }
    }

    profile = fault_profiles[stage]

    fault_mask = plant["String"].isin(selected_strings)

    plant.loc[fault_mask, "Voltage"] *= profile["voltage"]
    plant.loc[fault_mask, "Current"] *= profile["current"]
    plant.loc[fault_mask, "Power"] *= profile["power"]
    plant.loc[fault_mask, "Leakage"] = profile["leakage"]
# =========================================================
# HEADER
# =========================================================


st.markdown(
    """
    ### Intelligent DC Fault Detection & Localization

    **Monitor → Detect Early → Localize → Explain → Prioritize**
    """
)

st.markdown("---")


# =========================================================
# PLANT STATUS
# =========================================================

total_power = plant["Power"].sum()
average_voltage = plant["Voltage"].mean()
maximum_leakage = plant["Leakage"].max()


if not st.session_state.fault_active:

    status = "🟢 PLANT HEALTHY"
    stage_name = "Normal"
    status_description = "All monitored PV strings are operating normally."

elif st.session_state.fault_stage == 1:

    status = "🟡 EARLY WARNING"
    stage_name = "Warning"
    status_description = "Abnormal electrical behaviour detected."

elif st.session_state.fault_stage == 2:

    status = "🟠 SEVERE ANOMALY"
    stage_name = "Severe"
    status_description = "Fault indicators are increasing."

elif st.session_state.fault_stage == 3:

    status = "🔴 CRITICAL FAULT"
    stage_name = "Critical"
    status_description = "Strong DC-side fault signature detected."

else:

    status = "🚨 EXTREME FAULT"
    stage_name = "Extreme"
    status_description = "Severe ground/insulation abnormality detected."


affected_strings = 5 if st.session_state.fault_active else 0

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("Plant Status", status)

with c2:
    st.metric("DC Power", f"{total_power:.1f} kW")

with c3:
    st.metric("Average Voltage", f"{average_voltage:.1f} V")

with c4:
    st.metric("Max Leakage", f"{maximum_leakage:.2f} A")

st.caption(status_description)


# =========================================================
# FAULT INTELLIGENCE
# =========================================================

if st.session_state.fault_active:

    st.markdown("---")

    st.subheader("🤖 SolarGuard AI Fault Intelligence")

    target_row = plant[
        plant["String"] == st.session_state.fault_target
    ].iloc[0]

    # -----------------------------------------------------
    # ANOMALY CALCULATION
    # -----------------------------------------------------

    voltage_deviation = abs(
        1 - target_row["Voltage"] / 610
    )

    current_deviation = abs(
        1 - target_row["Current"] / 8.5
    )

    power_deviation = abs(
        1 - target_row["Power"] / 5.2
    )

    leakage_score = min(
        target_row["Leakage"] / 8.8,
        1
    )

    anomaly_score = (
        voltage_deviation * 0.20
        + current_deviation * 0.20
        + power_deviation * 0.25
        + leakage_score * 0.35
    )

    confidence = min(
        99,
        int(72 + anomaly_score * 27)
    )

    energy_at_risk = max(
        0,
        5.2 - target_row["Power"]
    )


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "AI Confidence",
            f"{confidence}%"
        )

    with m2:
        st.metric(
            "Fault Stage",
            stage_name
        )

    with m3:
        st.metric(
            "Energy at Risk",
            f"{energy_at_risk:.2f} kW"
        )

    with m4:
        st.metric(
            "Anomaly Score",
            f"{anomaly_score:.2f}"
        )


# =====================================================
# LOCALIZATION
# =====================================================

st.markdown("### 📍 Fault Localization")

l1, l2, l3 = st.columns(3)

if st.session_state.fault_active:

    selected_strings = [
        target,
        target2,
        target3,
        target4,
        target5
    ]

    affected_rows = plant[
        plant["String"].isin(selected_strings)
    ]

    affected_inverters = affected_rows["Inverter"].unique()
    affected_combiners = affected_rows["Combiner"].unique()

    with l1:
        st.info("**Primary Inverter**")

        for inverter in affected_inverters:
            inverter_strings = affected_rows[
                affected_rows["Inverter"] == inverter
            ]["String"].tolist()

            st.markdown(f"**{inverter}**")

            for string in inverter_strings:
                st.write(f"🔴 {string}")

    with l2:
        st.warning("**Primary Combiner Box**")

        for combiner in affected_combiners:
            combiner_strings = affected_rows[
                affected_rows["Combiner"] == combiner
            ]["String"].tolist()

            st.markdown(f"**{combiner}**")

            for string in combiner_strings:
                st.write(f"🔴 {string}")

    with l3:
        st.error("**Affected Strings**")

        for string in selected_strings:
            st.write(f"🔴 {string}")

else:

    with l1:
        st.info("**Primary Inverter**\n\nNo fault detected")

    with l2:
        st.warning("**Primary Combiner Box**\n\nNo fault detected")

    with l3:
        st.success("**Affected Strings**\n\nNone")

target_row = plant[
    plant["String"] == st.session_state.fault_target
].iloc[0]


# =====================================================
# EXPLAINABLE AI
# =====================================================

st.markdown("### 🔎 Explainable Fault Evidence")

evidence = pd.DataFrame({

    "Electrical Signal": [
        "DC Voltage",
        "DC Current",
        "DC Power",
        "Leakage Current"
    ],

    "Observed": [
        f"{target_row['Voltage']:.1f} V",
        f"{target_row['Current']:.2f} A",
        f"{target_row['Power']:.2f} kW",
        f"{target_row['Leakage']:.2f} A"
    ],

    "Normal Reference": [
        "≈ 610 V",
        "≈ 8.5 A",
        "≈ 5.2 kW",
        "< 0.5 A"
    ],

    "AI Interpretation": [
        "Voltage deviation detected",
        "Current deviation detected",
        "Power loss detected",
        "Abnormal leakage signature"
    ]
})

st.dataframe(
    evidence,
    use_container_width=True,
    hide_index=True
)
# =====================================================
# RECOMMENDED MAINTENANCE ACTION
# =====================================================

st.markdown("### 🛠️ Recommended Maintenance Action")

if st.session_state.fault_stage <= 1:
    maintenance_priority = "🟡 MEDIUM PRIORITY"
    maintenance_action = (
        "Inspect the selected PV string for early insulation degradation "
        "and abnormal leakage."
    )

elif st.session_state.fault_stage <= 2:
    maintenance_priority = "🟠 HIGH PRIORITY"
    maintenance_action = (
        "Inspect the selected PV string and combiner connections "
        "for insulation or grounding abnormalities."
    )

elif st.session_state.fault_stage <= 3:
    maintenance_priority = "🔴 CRITICAL PRIORITY"
    maintenance_action = (
        "Immediately inspect the affected PV string, DC cable "
        "and combiner section."
    )

else:
    maintenance_priority = "🚨 URGENT"
    maintenance_action = (
        "Isolate the affected PV string and perform immediate "
        "DC insulation and ground-fault inspection."
    )

st.success(
    f"""
**Priority: {maintenance_priority}**

{maintenance_action}

**Target:**
{target_row['Inverter']} → {target_row['Combiner']} → {target_row['String']}
"""
)

# =========================================================
# FAULT PROGRESSION GRAPH
# =========================================================

st.markdown("---")

st.subheader("📈 Fault Progression Monitor")

st.caption(
    "Illustrative fault-development trend for the selected PV string."
)

if st.session_state.fault_active:

    stages = [
        "Normal",
        "Warning",
        "Severe",
        "Critical"
    ]

    values = [0, 25, 50, 75]

    current_stage = st.session_state.fault_stage

    values[current_stage - 1] = 25 * current_stage

    visible_stages = stages[:current_stage + 1]
    visible_values = values[:current_stage + 1]

else:

    visible_stages = ["Normal"]
    visible_values = [0]


fig_trend = go.Figure()

fig_trend.add_trace(
    go.Scatter(
        x=visible_stages,
        y=visible_values,
        mode="lines+markers",
        name="Anomaly progression"
    )
)

fig_trend.update_layout(
    xaxis_title="Fault Condition",
    yaxis_title="Anomaly Level",
    yaxis=dict(range=[0, 100]),
    height=350
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# =========================================================
# DIGITAL PLANT MAP
# =========================================================

st.markdown("---")

st.subheader("🗺️ Digital PV Plant Map")

display_df = plant[
    [
        "Inverter",
        "Combiner",
        "String",
        "Voltage",
        "Current",
        "Power",
        "Leakage"
    ]
].copy()

# Add status columns AFTER selecting the original plant columns
display_df["Status"] = "🟢 Normal"
display_df["Priority"] = "Normal"

if st.session_state.fault_active:

    selected_strings = [
        target,
        target2,
        target3,
        target4,
        target5
    ]

    fault_mask = display_df["String"].isin(
        selected_strings
    )
    display_df.loc[
        fault_mask,
        "Status"
    ] = "🔴 FAULT DETECTED"

    display_df.loc[
        fault_mask,
        "Priority"
    ] = "🚨 HIGH PRIORITY"

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# POWER CHART
# =========================================================

st.markdown("---")

st.subheader("📊 String-Level Power Monitoring")

chart_df = plant.copy()

selected_strings = [
    target,
    target2,
    target3,
    target4,
    target5
]

chart_df["Status"] = "Normal"

if st.session_state.fault_active:

    chart_df.loc[
        chart_df["String"].isin(selected_strings),
        "Status"
    ] = "Fault"

fig_power = go.Figure()

bar_colors = [
    "lightblue"
    if st.session_state.fault_active and s in selected_strings
    else "royalblue"
    for s in chart_df["String"]
]

fig_power.add_trace(
    go.Bar(
        x=chart_df["String"],
        y=chart_df["Power"],
        name="PV String Power",
        marker_color=bar_colors
    )
)

fig_power.update_layout(
    title="PV String DC Power",
    xaxis_title="PV String",
    yaxis_title="Power (kW)",
    height=450
)

st.plotly_chart(
    fig_power,
    use_container_width=True
)
# =========================================================
# SYSTEM ARCHITECTURE
# =========================================================

with st.expander("🧠 SolarGuard AI Architecture"):

    st.markdown(
        """
        **PV Electrical Data**

        ↓

        **Signal Monitoring**

        Voltage • Current • Power • Leakage

        ↓

        **Anomaly Detection**

        Compare measured behaviour with expected operating behaviour

        ↓

        **Fault Classification**

        Identify abnormal DC-side ground/insulation behaviour

        ↓

        **Hierarchical Localization**

        Inverter → Combiner → String

        ↓

        **Explainable AI**

        Show the electrical evidence supporting the alert

        ↓

        **Risk & Maintenance Intelligence**

        Severity • Energy at Risk • Inspection Priority
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "SolarGuard AI  "
    "Explainable DC Fault Intelligence & Localization"
)
