import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from generator_model import (
    synchronous_generator_simulation,
    dc_generator_simulation
)

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="GeneratorSim Pro V3",
    page_icon="⚡",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
        color: white;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    .card {
        background: rgba(30, 41, 59, 0.85);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 0 18px rgba(0,0,0,0.25);
        text-align: center;
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .card h4 {
        color: #93c5fd;
        font-size: 1rem;
        margin-bottom: 10px;
    }

    .card h2 {
        color: white;
        font-size: 2rem;
        font-weight: bold;
    }

    .section-box {
        background: rgba(15, 23, 42, 0.7);
        padding: 14px 18px;
        border-radius: 16px;
        margin-bottom: 18px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .alert-box {
        background: rgba(127, 29, 29, 0.8);
        color: white;
        padding: 12px 16px;
        border-radius: 14px;
        border-left: 6px solid #ef4444;
        margin-bottom: 16px;
    }

    .good-box {
        background: rgba(20, 83, 45, 0.8);
        color: white;
        padding: 12px 16px;
        border-radius: 14px;
        border-left: 6px solid #22c55e;
        margin-bottom: 16px;
    }

    .health-badge {
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: bold;
        display: inline-block;
        margin-top: 8px;
    }

    .excellent {
        background: #14532d;
        color: #86efac;
    }

    .moderate {
        background: #78350f;
        color: #fde68a;
    }

    .critical {
        background: #7f1d1d;
        color: #fca5a5;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #1e293b;
        border-radius: 12px;
        color: white;
        padding: 10px 18px;
    }

    .stTabs [aria-selected="true"] {
        background: #2563eb !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
st.markdown('<div class="main-title">⚡ GeneratorSim Pro V3</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Advanced Generator Performance, Fault Analysis, Resistance Variation & Premium Visualization Dashboard</div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-box">
<b>Industrial Use Case:</b> Designed for electrical labs, academic projects, testing analysis, generator diagnostics, and machine performance simulation.
</div>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================
st.sidebar.header("🔧 Input Parameters")

mode = st.sidebar.radio("Select Mode", ["Single Generator Analysis", "Comparison Mode"])

generator_type = st.sidebar.selectbox(
    "Select Generator Type",
    ["Synchronous Generator", "DC Generator"]
)

voltage = st.sidebar.slider("Applied Voltage (V)", 100, 500, 220)

# =========================================
# SINGLE ANALYSIS MODE
# =========================================
if mode == "Single Generator Analysis":

    if generator_type == "Synchronous Generator":
        frequency = st.sidebar.slider("Supply Frequency (Hz)", 25, 100, 50)
        poles = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
        load_kw = st.sidebar.slider("Load Power (kW)", 1, 100, 20)
        excitation_factor = st.sidebar.slider("Excitation Factor", 0.8, 1.2, 1.0, step=0.05)
        field_resistance = st.sidebar.slider("Field Resistance (Ohm)", 0.5, 10.0, 2.0, step=0.1)

        st.sidebar.markdown("### ⚠ Fault Simulation")
        fault_mode = st.sidebar.selectbox(
            "Fault Scenario",
            ["Normal", "Voltage Drop", "Overload", "Over Frequency", "Under Excitation", "High Field Resistance"]
        )

        fault_voltage = voltage
        fault_load = load_kw
        fault_frequency = frequency
        fault_excitation = excitation_factor
        fault_field_res = field_resistance

        if fault_mode == "Voltage Drop":
            fault_voltage = voltage * 0.8
        elif fault_mode == "Overload":
            fault_load = load_kw * 1.4
        elif fault_mode == "Over Frequency":
            fault_frequency = frequency * 1.2
        elif fault_mode == "Under Excitation":
            fault_excitation = excitation_factor * 0.85
        elif fault_mode == "High Field Resistance":
            fault_field_res = field_resistance * 2

        result = synchronous_generator_simulation(
            fault_voltage, fault_frequency, poles, fault_load, fault_excitation, fault_field_res
        )

    else:
        speed = st.sidebar.slider("Speed (RPM)", 500, 3000, 1500)
        load_current = st.sidebar.slider("Load Current (A)", 1, 100, 20)
        field_factor = st.sidebar.slider("Field Factor", 0.8, 1.2, 1.0, step=0.05)
        armature_resistance = st.sidebar.slider("Armature Resistance (Ohm)", 0.1, 5.0, 0.5, step=0.1)
        field_resistance = st.sidebar.slider("Field Resistance (Ohm)", 0.5, 10.0, 2.0, step=0.1)

        st.sidebar.markdown("### ⚠ Fault Simulation")
        fault_mode = st.sidebar.selectbox(
            "Fault Scenario",
            ["Normal", "Voltage Drop", "Overload", "Overspeed", "Weak Field", "High Armature Resistance", "High Field Resistance"]
        )

        fault_voltage = voltage
        fault_speed = speed
        fault_current = load_current
        fault_field = field_factor
        fault_armature_res = armature_resistance
        fault_field_res = field_resistance

        if fault_mode == "Voltage Drop":
            fault_voltage = voltage * 0.8
        elif fault_mode == "Overload":
            fault_current = load_current * 1.4
        elif fault_mode == "Overspeed":
            fault_speed = speed * 1.2
        elif fault_mode == "Weak Field":
            fault_field = field_factor * 0.85
        elif fault_mode == "High Armature Resistance":
            fault_armature_res = armature_resistance * 2
        elif fault_mode == "High Field Resistance":
            fault_field_res = field_resistance * 2

        result = dc_generator_simulation(
            fault_voltage, fault_speed, fault_current, fault_field, fault_armature_res, fault_field_res
        )

    # =========================================
    # HEALTH / ALERT
    # =========================================
    health = result.get("Health Status", "Moderate")

    if fault_mode != "Normal":
        st.markdown(f"""
        <div class="alert-box">
            ⚠ <b>Fault Active:</b> {fault_mode} condition applied to the generator model.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="good-box">
            ✅ <b>System Normal:</b> Generator is operating under normal condition.
        </div>
        """, unsafe_allow_html=True)

    if health == "Excellent":
        badge_class = "excellent"
    elif health == "Moderate":
        badge_class = "moderate"
    else:
        badge_class = "critical"

    st.markdown(f"""
    <div class="health-badge {badge_class}">
        Health Status: {health}
    </div>
    """, unsafe_allow_html=True)

    # =========================================
    # KPI CARDS
    # =========================================
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    current_val = result.get("Current (A)", result.get("Load Current (A)", 0))
    power_val = result.get("Load Power (kW)", result.get("Output Power (kW)", 0))
    pf_val = result.get("Power Factor", "-")
    reg_val = result.get("Voltage Regulation (%)", 0)

    with col1:
        st.markdown(f'<div class="card"><h4>Type</h4><h2>{result["Generator Type"]}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="card"><h4>Speed</h4><h2>{result.get("Speed (RPM)", 0)}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="card"><h4>Current</h4><h2>{current_val}</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="card"><h4>Power</h4><h2>{power_val}</h2></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="card"><h4>Efficiency</h4><h2>{result.get("Efficiency (%)", 0)}</h2></div>', unsafe_allow_html=True)
    with col6:
        st.markdown(f'<div class="card"><h4>PF</h4><h2>{pf_val}</h2></div>', unsafe_allow_html=True)
    with col7:
        st.markdown(f'<div class="card"><h4>Regulation</h4><h2>{reg_val}</h2></div>', unsafe_allow_html=True)

    # =========================================
    # TABS
    # =========================================
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Graphs", "📁 Export"])

    # =========================================
    # TAB 1 - DASHBOARD
    # =========================================
    with tab1:
        st.markdown(f"### Active Scenario: **{fault_mode}**")

        st.markdown("## 🌀 Animated Generator Rotor")

        c1, c2, c3, c4, c5 = st.columns([1.5, 1, 1, 1, 1])

        with c1:
            rotor_fig = go.Figure(data=[go.Pie(
                values=[25, 25, 25, 25],
                hole=0.70,
                rotation=result.get("Speed (RPM)", 0) / 10,
                marker=dict(colors=["#38bdf8", "#facc15", "#22c55e", "#f97316"]),
                textinfo='none'
            )])

            rotor_fig.update_layout(
                showlegend=False,
                height=350,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=10),
                annotations=[dict(text="⚙", x=0.5, y=0.5, font_size=36, showarrow=False, font_color="white")]
            )
            st.plotly_chart(rotor_fig, use_container_width=True)
            st.caption("Rotor angle changes dynamically with machine speed.")

        with c2:
            rpm_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result.get("Speed (RPM)", 0),
                title={'text': "RPM"},
                gauge={'axis': {'range': [0, 3000]}}
            ))
            rpm_fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(rpm_fig, use_container_width=True)

        with c3:
            current_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=current_val,
                title={'text': "Current"},
                gauge={'axis': {'range': [0, 100]}}
            ))
            current_fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(current_fig, use_container_width=True)

        with c4:
            eff_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result.get("Efficiency (%)", 0),
                title={'text': "Efficiency"},
                gauge={'axis': {'range': [0, 100]}}
            ))
            eff_fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(eff_fig, use_container_width=True)

        with c5:
            volt_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result.get("Voltage (V)", 0),
                title={'text': "Voltage"},
                gauge={'axis': {'range': [0, 500]}}
            ))
            volt_fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(volt_fig, use_container_width=True)

        st.markdown("## 📄 Detailed Output Table")
        output_df = pd.DataFrame(result.items(), columns=["Parameter", "Value"])
        st.dataframe(output_df, use_container_width=True)

    # =========================================
    # TAB 2 - GRAPHS
    # =========================================
    with tab2:
        st.markdown("## 📈 Performance Graphs")

        if generator_type == "Synchronous Generator":
            # Graph 1
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            load_range = np.linspace(1, 100, 50)
            efficiencies = []
            for l in load_range:
                r = synchronous_generator_simulation(voltage, frequency, poles, l, excitation_factor, field_resistance)
                efficiencies.append(r["Efficiency (%)"])
            ax1.plot(load_range, efficiencies, linewidth=2)
            ax1.set_title("Efficiency vs Load Power")
            ax1.set_xlabel("Load Power (kW)")
            ax1.set_ylabel("Efficiency (%)")
            ax1.grid(True)
            st.pyplot(fig1)

            # Graph 2
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            exc_range = np.linspace(0.8, 1.2, 50)
            voltages = []
            for ex in exc_range:
                r = synchronous_generator_simulation(voltage, frequency, poles, load_kw, ex, field_resistance)
                voltages.append(r["Voltage (V)"])
            ax2.plot(exc_range, voltages, linewidth=2)
            ax2.set_title("Voltage vs Excitation Factor")
            ax2.set_xlabel("Excitation Factor")
            ax2.set_ylabel("Voltage (V)")
            ax2.grid(True)
            st.pyplot(fig2)

            # Graph 3
            fig3, ax3 = plt.subplots(figsize=(8, 5))
            freq_range = np.linspace(25, 100, 50)
            speeds = []
            for f in freq_range:
                r = synchronous_generator_simulation(voltage, f, poles, load_kw, excitation_factor, field_resistance)
                speeds.append(r["Speed (RPM)"])
            ax3.plot(freq_range, speeds, linewidth=2)
            ax3.set_title("Speed vs Frequency")
            ax3.set_xlabel("Frequency (Hz)")
            ax3.set_ylabel("Speed (RPM)")
            ax3.grid(True)
            st.pyplot(fig3)

            # Graph 4
            fig4, ax4 = plt.subplots(figsize=(8, 5))
            field_res_range = np.linspace(0.5, 10, 50)
            currents = []
            for fr in field_res_range:
                r = synchronous_generator_simulation(voltage, frequency, poles, load_kw, excitation_factor, fr)
                currents.append(r["Current (A)"])
            ax4.plot(field_res_range, currents, linewidth=2)
            ax4.set_title("Current vs Field Resistance")
            ax4.set_xlabel("Field Resistance (Ohm)")
            ax4.set_ylabel("Current (A)")
            ax4.grid(True)
            st.pyplot(fig4)

            # Graph 5
            fig5, ax5 = plt.subplots(figsize=(8, 5))
            field_res_range2 = np.linspace(0.5, 10, 50)
            regulation_vals = []
            for fr in field_res_range2:
                r = synchronous_generator_simulation(voltage, frequency, poles, load_kw, excitation_factor, fr)
                regulation_vals.append(r["Voltage Regulation (%)"])
            ax5.plot(field_res_range2, regulation_vals, linewidth=2)
            ax5.set_title("Voltage Regulation vs Field Resistance")
            ax5.set_xlabel("Field Resistance (Ohm)")
            ax5.set_ylabel("Voltage Regulation (%)")
            ax5.grid(True)
            st.pyplot(fig5)

            # Graph 6
            fig6, ax6 = plt.subplots(figsize=(8, 5))
            field_res_range3 = np.linspace(0.5, 10, 50)
            voltage_vals = []
            for fr in field_res_range3:
                r = synchronous_generator_simulation(voltage, frequency, poles, load_kw, excitation_factor, fr)
                voltage_vals.append(r["Voltage (V)"])
            ax6.plot(field_res_range3, voltage_vals, linewidth=2)
            ax6.set_title("Voltage vs Field Resistance")
            ax6.set_xlabel("Field Resistance (Ohm)")
            ax6.set_ylabel("Voltage (V)")
            ax6.grid(True)
            st.pyplot(fig6)

        else:
            # Graph 1
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            speed_range = np.linspace(500, 3000, 50)
            voltages = []
            for s in speed_range:
                r = dc_generator_simulation(voltage, s, load_current, field_factor, armature_resistance, field_resistance)
                voltages.append(r["Voltage (V)"])
            ax1.plot(speed_range, voltages, linewidth=2)
            ax1.set_title("Voltage vs Speed")
            ax1.set_xlabel("Speed (RPM)")
            ax1.set_ylabel("Voltage (V)")
            ax1.grid(True)
            st.pyplot(fig1)

            # Graph 2
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            current_range = np.linspace(1, 100, 50)
            efficiencies = []
            for c in current_range:
                r = dc_generator_simulation(voltage, speed, c, field_factor, armature_resistance, field_resistance)
                efficiencies.append(r["Efficiency (%)"])
            ax2.plot(current_range, efficiencies, linewidth=2)
            ax2.set_title("Efficiency vs Load Current")
            ax2.set_xlabel("Load Current (A)")
            ax2.set_ylabel("Efficiency (%)")
            ax2.grid(True)
            st.pyplot(fig2)

            # Graph 3
            fig3, ax3 = plt.subplots(figsize=(8, 5))
            field_range = np.linspace(0.8, 1.2, 50)
            emf_vals = []
            for ff in field_range:
                r = dc_generator_simulation(voltage, speed, load_current, ff, armature_resistance, field_resistance)
                emf_vals.append(r["Generated EMF (V)"])
            ax3.plot(field_range, emf_vals, linewidth=2)
            ax3.set_title("Generated EMF vs Field Factor")
            ax3.set_xlabel("Field Factor")
            ax3.set_ylabel("Generated EMF (V)")
            ax3.grid(True)
            st.pyplot(fig3)

            # Graph 4
            fig4, ax4 = plt.subplots(figsize=(8, 5))
            arm_res_range = np.linspace(0.1, 5.0, 50)
            terminal_voltages = []
            for ar in arm_res_range:
                r = dc_generator_simulation(voltage, speed, load_current, field_factor, ar, field_resistance)
                terminal_voltages.append(r["Voltage (V)"])
            ax4.plot(arm_res_range, terminal_voltages, linewidth=2)
            ax4.set_title("Terminal Voltage vs Armature Resistance")
            ax4.set_xlabel("Armature Resistance (Ohm)")
            ax4.set_ylabel("Voltage (V)")
            ax4.grid(True)
            st.pyplot(fig4)

            # Graph 5
            fig5, ax5 = plt.subplots(figsize=(8, 5))
            field_res_range = np.linspace(0.5, 10.0, 50)
            current_vals = []
            for fr in field_res_range:
                r = dc_generator_simulation(voltage, speed, load_current, field_factor, armature_resistance, fr)
                current_vals.append(r["Load Current (A)"])
            ax5.plot(field_res_range, current_vals, linewidth=2)
            ax5.set_title("Current vs Field Resistance")
            ax5.set_xlabel("Field Resistance (Ohm)")
            ax5.set_ylabel("Current (A)")
            ax5.grid(True)
            st.pyplot(fig5)

            # Graph 6
            fig6, ax6 = plt.subplots(figsize=(8, 5))
            field_res_range2 = np.linspace(0.5, 10.0, 50)
            eff_vals = []
            for fr in field_res_range2:
                r = dc_generator_simulation(voltage, speed, load_current, field_factor, armature_resistance, fr)
                eff_vals.append(r["Efficiency (%)"])
            ax6.plot(field_res_range2, eff_vals, linewidth=2)
            ax6.set_title("Efficiency vs Field Resistance")
            ax6.set_xlabel("Field Resistance (Ohm)")
            ax6.set_ylabel("Efficiency (%)")
            ax6.grid(True)
            st.pyplot(fig6)

    # =========================================
    # TAB 3 - EXPORT
    # =========================================
    with tab3:
        st.markdown("## 📥 Export Results")

        export_df = pd.DataFrame(result.items(), columns=["Parameter", "Value"])
        csv = export_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📁 Download Current Results as CSV",
            data=csv,
            file_name="generatorsim_results.csv",
            mime="text/csv"
        )

        st.info("You can export the current generator simulation result table as a CSV file.")

# =========================================
# COMPARISON MODE
# =========================================
else:
    st.markdown("## ⚖️ Comparison Mode")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### Generator A")
        gen_a_type = st.selectbox("Generator A Type", ["Synchronous Generator", "DC Generator"], key="a_type")
        a_voltage = st.slider("Voltage A (V)", 100, 500, 220, key="a_voltage")

        if gen_a_type == "Synchronous Generator":
            a_frequency = st.slider("Frequency A (Hz)", 25, 100, 50, key="a_freq")
            a_poles = st.selectbox("Poles A", [2, 4, 6, 8], index=1, key="a_poles")
            a_load = st.slider("Load Power A (kW)", 1, 100, 20, key="a_load")
            a_exc = st.slider("Excitation A", 0.8, 1.2, 1.0, step=0.05, key="a_exc")
            a_field_res = st.slider("Field Resistance A (Ohm)", 0.5, 10.0, 2.0, step=0.1, key="a_field_res")
            result_a = synchronous_generator_simulation(a_voltage, a_frequency, a_poles, a_load, a_exc, a_field_res)
        else:
            a_speed = st.slider("Speed A (RPM)", 500, 3000, 1500, key="a_speed")
            a_current = st.slider("Load Current A (A)", 1, 100, 20, key="a_current")
            a_field = st.slider("Field Factor A", 0.8, 1.2, 1.0, step=0.05, key="a_field")
            a_arm_res = st.slider("Armature Resistance A (Ohm)", 0.1, 5.0, 0.5, step=0.1, key="a_arm_res")
            a_field_res = st.slider("Field Resistance A (Ohm)", 0.5, 10.0, 2.0, step=0.1, key="a_dc_field_res")
            result_a = dc_generator_simulation(a_voltage, a_speed, a_current, a_field, a_arm_res, a_field_res)

    with colB:
        st.markdown("### Generator B")
        gen_b_type = st.selectbox("Generator B Type", ["Synchronous Generator", "DC Generator"], key="b_type")
        b_voltage = st.slider("Voltage B (V)", 100, 500, 220, key="b_voltage")

        if gen_b_type == "Synchronous Generator":
            b_frequency = st.slider("Frequency B (Hz)", 25, 100, 50, key="b_freq")
            b_poles = st.selectbox("Poles B", [2, 4, 6, 8], index=1, key="b_poles")
            b_load = st.slider("Load Power B (kW)", 1, 100, 20, key="b_load")
            b_exc = st.slider("Excitation B", 0.8, 1.2, 1.0, step=0.05, key="b_exc")
            b_field_res = st.slider("Field Resistance B (Ohm)", 0.5, 10.0, 2.0, step=0.1, key="b_field_res")
            result_b = synchronous_generator_simulation(b_voltage, b_frequency, b_poles, b_load, b_exc, b_field_res)
        else:
            b_speed = st.slider("Speed B (RPM)", 500, 3000, 1500, key="b_speed")
            b_current = st.slider("Load Current B (A)", 1, 100, 20, key="b_current")
            b_field = st.slider("Field Factor B", 0.8, 1.2, 1.0, step=0.05, key="b_field")
            b_arm_res = st.slider("Armature Resistance B (Ohm)", 0.1, 5.0, 0.5, step=0.1, key="b_arm_res")
            b_field_res = st.slider("Field Resistance B (Ohm)", 0.5, 10.0, 2.0, step=0.1, key="b_dc_field_res")
            result_b = dc_generator_simulation(b_voltage, b_speed, b_current, b_field, b_arm_res, b_field_res)

    st.markdown("### 📊 Comparison Table")
    compare_df = pd.DataFrame({
        "Parameter": list(result_a.keys()),
        "Generator A": list(result_a.values()),
        "Generator B": [result_b.get(k, "-") for k in result_a.keys()]
    })
    st.dataframe(compare_df, use_container_width=True)

    st.markdown("### 📈 Efficiency Comparison")
    eff_a = result_a.get("Efficiency (%)", 0)
    eff_b = result_b.get("Efficiency (%)", 0)

    fig_cmp, ax_cmp = plt.subplots(figsize=(8, 5))
    ax_cmp.bar(["Generator A", "Generator B"], [eff_a, eff_b])
    ax_cmp.set_title("Efficiency Comparison")
    ax_cmp.set_ylabel("Efficiency (%)")
    ax_cmp.grid(axis="y")
    st.pyplot(fig_cmp)