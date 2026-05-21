import streamlit as st
import numpy as np

# Set up page styling
st.set_page_config(page_title="CorroSight", page_icon="⚓", layout="wide")

st.title("⚓ CorroSight: Subsea Pipeline Integrity Assessment")
st.markdown("### Evaluating the Role of Surface Corrosion Geometry in Governing Failure Limits")
st.write("This tool calculates the remaining burst pressure of corroded subsea pipelines using industry-standard analytical criteria to evaluate material sensitivity.")

st.markdown("---")

# Create two columns for clean UI separation
col_input, col_results = st.columns([1, 1.5])

with col_input:
    st.header("📋 Input Parameters")
    
    # 1. Pipeline Geometry Inputs
    st.subheader("1. Pipeline Geometry")
    D_o = st.number_input("Outer Diameter, D_o (mm)", value=508.0, help="Standard diameter for your transmission line profile.")
    t = st.number_input("Wall Thickness, t (mm)", value=12.7, help="Nominal un-corroded wall thickness.")
    
    # 2. Corrosion Geometry Inputs (The core of your thesis title!)
    st.subheader("2. Corrosion Defect Geometry")
    d = st.number_input("Corrosion Depth, d (mm)", value=3.5, min_value=0.0, max_value=float(t))
    L = st.number_input("Defect Longitudinal Length, L (mm)", value=200.0)
    
    # 3. Material Grade Selection (Addressing material sensitivity)
    st.subheader("3. Pipeline Steel Grade")
    material = st.selectbox("Select Material Grade", ["API 5L X52", "API 5L X65"])

# Assign exact material property baselines based on standard constraints
if material == "API 5L X52":
    Y_s = 360.0  # Yield Strength (MPa)
    UTS = 460.0  # Ultimate Tensile Strength (MPa)
elif material == "API 5L X65":
    Y_s = 450.0  # Yield Strength (MPa)
    UTS = 535.0  # Ultimate Tensile Strength (MPa)

# --- Core Assessment Mathematics ---
# 1. Intact burst pressure limit via standard Barlow's Formula
P_intact = (2 * Y_s * t) / D_o

# 2. Folias Bulging Factor (M) - captures geometric stress concentrations at defect boundaries
M = np.sqrt(1 + 0.8 * (L**2 / (D_o * t)))

# 3. ASME B31G Corroded Burst Pressure Estimation Logic
d_t_ratio = d / t

if d_t_ratio <= 0.8:
    # Parabolic approximation method for typical localized corrosion pits
    P_corroded = P_intact * ((1 - (2/3) * d_t_ratio) / (1 - (2/3) * d_t_ratio * (1 / M)))
else:
    # Extreme safety threshold limit for severe defect depth
    P_corroded = P_intact * (1 - d_t_ratio)

with col_results:
    st.header("📊 Analytical Failure Limits")
    
    # Display beautiful high-level summary cards
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Selected Steel Grade", value=material)
    c2.metric(label="Intact Strength (Barlow)", value=f"{P_intact:.2f} MPa")
    c3.metric(label="Predicted Burst Pressure", value=f"{P_corroded:.2f} MPa")
    
    st.markdown("---")
    
    # Dynamic Engineering Analysis Messages for your report screenshots
    st.subheader("🔍 Geometry Analysis Summary")
    st.write(f"• **Depth Ratio (d/t):** {d_t_ratio*100:.1f}% of the pipeline wall has been degraded.")
    st.write(f"• **Folias Bulging Factor (M):** {M:.3f} (Values > 1.0 indicate structural stress amplification due to defect length).")
    
    # Material sensitivity warning statement
    strength_loss = ((P_intact - P_corroded) / P_intact) * 100
    st.warning(f"**Structural Impact:** The specified corrosion geometry causes a **{strength_loss:.1f}% reduction** in the operational failure limit of this {material} pipeline segment.")
