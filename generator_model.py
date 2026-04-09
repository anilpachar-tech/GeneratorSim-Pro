import numpy as np


# =========================================
# HEALTH STATUS
# =========================================
def _health_status(efficiency, current, voltage, regulation=0, resistance=0):
    score = 0

    if efficiency < 50:
        score += 2
    elif efficiency < 75:
        score += 1

    if current > 40:
        score += 2
    elif current > 25:
        score += 1

    if voltage < 180 or voltage > 500:
        score += 2

    if abs(regulation) > 15:
        score += 1

    if resistance > 5:
        score += 1

    if score <= 1:
        return "Excellent"
    elif score <= 3:
        return "Moderate"
    else:
        return "Critical"


# =========================================
# SYNCHRONOUS GENERATOR MODEL
# =========================================
def synchronous_generator_simulation(
    voltage,
    frequency,
    poles,
    load_kw,
    excitation_factor,
    field_resistance
):
    ns = 120 * frequency / poles

    excitation_effect = excitation_factor * (1.0 - (field_resistance / 50))
    excitation_effect = max(0.6, excitation_effect)

    generated_voltage = voltage * excitation_effect

    pf = 0.85
    current = (load_kw * 1000) / (np.sqrt(3) * max(generated_voltage, 1) * pf)

    apparent_power = np.sqrt(3) * generated_voltage * current / 1000
    reactive_power = apparent_power * np.sin(np.arccos(pf))

    copper_loss = 0.08 * load_kw + (field_resistance * 0.02)
    iron_loss = 0.05 * load_kw
    mechanical_loss = 0.03 * load_kw
    field_loss = (generated_voltage ** 2) / (1000 * max(field_resistance, 0.1))

    total_loss = copper_loss + iron_loss + mechanical_loss + field_loss
    input_power = load_kw + total_loss

    efficiency = (load_kw / input_power) * 100 if input_power > 0 else 0
    voltage_regulation = ((generated_voltage - voltage) / voltage) * 100 if voltage != 0 else 0

    health = _health_status(
        efficiency,
        current,
        generated_voltage,
        voltage_regulation,
        field_resistance
    )

    return {
        "Generator Type": "Synchronous Generator",
        "Voltage (V)": round(generated_voltage, 2),
        "Frequency (Hz)": round(frequency, 2),
        "Poles": poles,
        "Excitation Factor": round(excitation_factor, 2),
        "Field Resistance (Ohm)": round(field_resistance, 2),
        "Speed (RPM)": round(ns, 2),
        "Load Power (kW)": round(load_kw, 2),
        "Current (A)": round(current, 2),
        "Power Factor": round(pf, 2),
        "Apparent Power (kVA)": round(apparent_power, 2),
        "Reactive Power (kVAr)": round(reactive_power, 2),
        "Copper Loss (kW)": round(copper_loss, 2),
        "Iron Loss (kW)": round(iron_loss, 2),
        "Mechanical Loss (kW)": round(mechanical_loss, 2),
        "Field Loss (kW)": round(field_loss, 2),
        "Total Loss (kW)": round(total_loss, 2),
        "Efficiency (%)": round(efficiency, 2),
        "Voltage Regulation (%)": round(voltage_regulation, 2),
        "Health Status": health
    }


# =========================================
# DC GENERATOR MODEL
# =========================================
def dc_generator_simulation(
    voltage,
    speed,
    load_current,
    field_factor,
    armature_resistance,
    field_resistance
):
    generated_emf = voltage * field_factor * (speed / 1500)

    terminal_voltage = generated_emf - (load_current * armature_resistance)
    terminal_voltage = max(0, terminal_voltage)

    output_power = terminal_voltage * load_current / 1000
    copper_loss = (load_current ** 2) * armature_resistance / 1000
    field_loss = (generated_emf ** 2) / (1000 * max(field_resistance, 0.1))
    mechanical_loss = 0.25
    iron_loss = 0.20

    total_loss = copper_loss + field_loss + mechanical_loss + iron_loss
    input_power = output_power + total_loss

    efficiency = (output_power / input_power) * 100 if input_power > 0 else 0
    voltage_regulation = ((generated_emf - terminal_voltage) / generated_emf) * 100 if generated_emf != 0 else 0

    health = _health_status(
        efficiency,
        load_current,
        terminal_voltage,
        voltage_regulation,
        field_resistance
    )

    return {
        "Generator Type": "DC Generator",
        "Voltage (V)": round(terminal_voltage, 2),
        "Generated EMF (V)": round(generated_emf, 2),
        "Speed (RPM)": round(speed, 2),
        "Load Current (A)": round(load_current, 2),
        "Field Factor": round(field_factor, 2),
        "Armature Resistance (Ohm)": round(armature_resistance, 2),
        "Field Resistance (Ohm)": round(field_resistance, 2),
        "Output Power (kW)": round(output_power, 2),
        "Copper Loss (kW)": round(copper_loss, 2),
        "Field Loss (kW)": round(field_loss, 2),
        "Mechanical Loss (kW)": round(mechanical_loss, 2),
        "Iron Loss (kW)": round(iron_loss, 2),
        "Total Loss (kW)": round(total_loss, 2),
        "Efficiency (%)": round(efficiency, 2),
        "Voltage Regulation (%)": round(voltage_regulation, 2),
        "Health Status": health
    }