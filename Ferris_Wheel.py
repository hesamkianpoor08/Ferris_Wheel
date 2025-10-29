import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from functools import partial
import os
from PIL import Image
import math

# --- Page Configuration ---
st.set_page_config(
    page_title="Ferris Wheel Designer",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize Session State ---
if 'step' not in st.session_state:
    st.session_state.step = 0  # steps: 0 gen, 1 primary+capacity+vip, 2 cabin geometry, 3 rotation time confirm, 4 environment, 5 final
if 'generation_type' not in st.session_state:
    st.session_state.generation_type = None
if 'diameter' not in st.session_state:
    st.session_state.diameter = 60
if 'num_cabins' not in st.session_state:
    st.session_state.num_cabins = 12
if 'cabin_capacity' not in st.session_state:
    st.session_state.cabin_capacity = 6
if 'num_vip_cabins' not in st.session_state:
    st.session_state.num_vip_cabins = 1
if 'cabin_geometry' not in st.session_state:
    st.session_state.cabin_geometry = None
if 'rotation_time_min' not in st.session_state:
    st.session_state.rotation_time_min = None
if 'environment_data' not in st.session_state:
    st.session_state.environment_data = {}
if 'validation_errors' not in st.session_state:
    st.session_state.validation_errors = []
if 'capacities_calculated' not in st.session_state:
    st.session_state.capacities_calculated = False
if 'geometry_selected' not in st.session_state:
    st.session_state.geometry_selected = False
if 'wind_rose_loaded' not in st.session_state:
    st.session_state.wind_rose_loaded = False
if 'wind_rose_file' not in st.session_state:
    st.session_state.wind_rose_file = None

# --- Helper Functions ---
def calculate_cabin_range_from_base(base, diameter):
    """Given a base, return min/max cabin counts"""
    min_cabins = int(np.floor(base * 0.7))
    max_cabins = int(np.ceil(base * 1.2))
    # Protect against degenerate ranges
    min_cabins = max(3, min_cabins)
    max_cabins = max(min_cabins, max_cabins)
    return min_cabins, max_cabins

def base_for_geometry(diameter, geometry):
    """Return base cabin count formula depending on geometry.
       If geometry == 'Spherical' -> pi*d/5
       else -> pi*d/4
    """
    if geometry == "Spherical":
        base = np.pi * diameter / 5.0
    else:
        base = np.pi * diameter / 4.0
    return base

def calculate_capacity_per_hour_from_time(num_cabins, cabin_capacity, num_vip, rotation_time_minutes):
    """Calculate capacity per hour given rotation time (minutes) and VIP capacity rule (-2 per VIP cabin)."""
    if rotation_time_minutes is None or rotation_time_minutes <= 0:
        return 0
    rotations_per_hour = 60.0 / rotation_time_minutes
    vip_cap = max(0, cabin_capacity - 2)
    regular_cabins = num_cabins - num_vip
    passengers_per_rotation = num_vip * vip_cap + regular_cabins * cabin_capacity
    return passengers_per_rotation * rotations_per_hour

def calculate_linear_speed_from_v_and_d(v_linear, diameter):
    """Given linear speed and diameter (m), return angular speed rad/s and rpm."""
    radius = diameter / 2.0
    if radius <= 0:
        return 0.0, 0.0
    ang_rad_s = v_linear / radius
    rpm = ang_rad_s * 60.0 / (2.0 * np.pi)
    return ang_rad_s, rpm

def create_component_diagram(diameter, height, capacity, motor_power):
    fig = go.Figure()
    theta = np.linspace(0, 2*np.pi, 200)
    x_wheel = diameter/2 * np.cos(theta)
    y_wheel = diameter/2 * np.sin(theta) + height/2

    # wheel outline
    fig.add_trace(go.Scatter(
        x=x_wheel, y=y_wheel, mode='lines',
        name='Wheel Structure',
        line=dict(color='#2196F3', width=3),
        hoverinfo='skip',
        showlegend=False
    ))

    # support tower
    support_x = [0, 0]
    support_y = [0, height/2]
    support_color = '#FF5722'
    fig.add_trace(go.Scatter(
        x=support_x, y=support_y, mode='lines',
        name='Support Tower',
        line=dict(color=support_color, width=6),
        hoverinfo='skip',
        showlegend=False
    ))

    annotations = [
        dict(x=0, y=height + diameter*0.05 + 2, text=f"Height: {height} m", showarrow=False, font=dict(color='black')),
        dict(x=diameter/2 + 2, y=height/2, text=f"Diameter: {diameter} m", showarrow=False, font=dict(color='black')),
        dict(x=0, y=-5, text=f"Motor Power: {motor_power:.1f} kW", showarrow=False, font=dict(color='black')),
        dict(x=0, y=-8, text=f"Capacity: {capacity} passengers", showarrow=False, font=dict(color='black'))
    ]

    fig.update_layout(
        title=dict(text="Ferris Wheel Design Overview", font=dict(color='black')),
        height=620,
        template="plotly_white",
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        xaxis=dict(title="Width [m]", gridcolor='#E0E0E0', zeroline=True, linecolor='#000000', tickfont=dict(color='#000000')),
        yaxis=dict(title="Height [m]", gridcolor='#E0E0E0', zeroline=True, linecolor='#000000', tickfont=dict(color='#000000')),
        annotations=annotations,
        margin=dict(l=80, r=80, t=80, b=80),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='sans-serif',
            font_color='black',
            bordercolor='#2196F3'
        )
    )
    return fig

# --- Validation ---
def validate_current_step():
    """Return (True/False, errors_list). Prevent moving to next step if False."""
    errors = []
    s = st.session_state
    step = s.step

    # Step 0: generation selection required
    if step == 0:
        if not s.generation_type:
            errors.append("Please select a Ferris wheel generation.")
    # Step 1: primary params + cabin capacity + vip
    elif step == 1:
        # diameter must be between 30 and 80
        if s.diameter is None or s.diameter < 30 or s.diameter > 80:
            errors.append("Diameter must be between 30 and 80 meters.")
        # land elsewhere? here just cabin inputs
        if s.num_cabins is None or s.num_cabins <= 0:
            errors.append("Please set a valid number of cabins.")
        if s.cabin_capacity is None or s.cabin_capacity < 4 or s.cabin_capacity > 8:
            errors.append("Cabin capacity must be between 4 and 8 passengers.")
        if s.num_vip_cabins is None or s.num_vip_cabins < 0 or s.num_vip_cabins > s.num_cabins:
            errors.append("Number of VIP cabins must be between 0 and total number of cabins.")
        # must have calculated capacities before moving on
        if not s.capacities_calculated:
            errors.append("Please click 'Calculate Capacities' to compute capacities before continuing.")
    # Step 2: cabin geometry page requires selection
    elif step == 2:
        if not s.cabin_geometry:
            errors.append("Please select a cabin geometry.")
    # Step 3: rotation time confirmation
    elif step == 3:
        if s.rotation_time_min is None or s.rotation_time_min <= 0:
            errors.append("Please enter a valid rotation time (minutes per rotation).")
    # Step 4: environment
    elif step == 4:
        env = s.environment_data
        if not env.get('province'):
            errors.append("Please select a province.")
        if not env.get('region_name'):
            errors.append("Please enter the region name.")
        # land coords and length/width checks
        if 'land_length' not in env or env['land_length'] < 10 or env['land_length'] > 150:
            errors.append("Land Length must be between 10 and 150 meters.")
        if 'land_width' not in env or env['land_width'] < 10 or env['land_width'] > 150:
            errors.append("Land Width must be between 10 and 150 meters.")
        if 'altitude' not in env or env['altitude'] is None:
            errors.append("Please enter the altitude (elevation).")
        # wind fields
        if 'wind_max' not in env or env['wind_max'] is None:
            errors.append("Please enter the maximum wind speed (km/h).")
        if s.wind_rose_loaded and not s.wind_rose_file:
            errors.append("Wind rose upload is enabled but no file was loaded.")
    return (len(errors) == 0, errors)


def next_with_validation():
    ok, errors = validate_current_step()
    st.session_state.validation_errors = errors
    if not ok:
        # show errors
        for e in errors:
            st.error(e)
    else:
        # move to next
        st.session_state.step = min(st.session_state.step + 1, 5)
        # reset UI errors for next page
        st.session_state.validation_errors = []

def go_back():
    st.session_state.step = max(st.session_state.step - 1, 0)

def select_generation(gen_type):
    st.session_state.generation_type = gen_type
    st.session_state.step = 1

def reset_design():
    # reset everything relevant
    st.session_state.step = 0
    st.session_state.generation_type = None
    st.session_state.diameter = 60
    st.session_state.num_cabins = 12
    st.session_state.cabin_capacity = 6
    st.session_state.num_vip_cabins = 1
    st.session_state.cabin_geometry = None
    st.session_state.rotation_time_min = None
    st.session_state.environment_data = {}
    st.session_state.validation_errors = []
    st.session_state.capacities_calculated = False
    st.session_state.geometry_selected = False
    st.session_state.wind_rose_loaded = False
    st.session_state.wind_rose_file = None

# --- UI ---
st.title("🎡 Ferris Wheel Designer")

total_steps = 6
progress = st.session_state.step / (total_steps - 1)
st.progress(progress)
st.markdown(f"**Step {st.session_state.step + 1} of {total_steps}**")
st.markdown("---")

# === STEP 0: Generation Type Selection ===
if st.session_state.step == 0:
    st.header("Step 1: Select Ferris Wheel Generation")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎡 1st Generation (Truss type)", key="gen1_btn"):
            select_generation("1st Generation (Truss type)")
    with col2:
        if st.button("🎡 2nd Generation (Cable type)", key="gen2_btn"):
            select_generation("2nd Generation (Cable type)")

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🎡 2nd Generation (Pure cable type)", key="gen2_2_btn"):
            select_generation("2nd Generation (Pure cable type)")
    with col4:
        if st.button("🎡 4th Generation (Hubless centerless)", key="gen4_btn"):
            select_generation("4th Generation (Hubless centerless)")

    if st.session_state.generation_type:
        st.success(f"✅ Selected: {st.session_state.generation_type}")

    # Next only after selection (validation will enforce)
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", key="back_from_gen", on_click=go_back)
    with right_col:
        st.button("Next ➡️", key="next_from_gen", on_click=next_with_validation)

# === STEP 1: Primary Parameters + Cabin Capacity + VIP (merged) ===
elif st.session_state.step == 1:
    st.header("Step 2: Ferris Wheel Primary Parameters, Cabin Capacity & VIP")
    st.subheader(f"Generation: {st.session_state.generation_type}")
    st.markdown("---")

    # Diameter: enforce min=30 max=80
    col1, col2 = st.columns(2)
    with col1:
        diameter = st.number_input(
            "Ferris Wheel Diameter (m)",
            min_value=30,
            max_value=80,
            value=int(st.session_state.diameter),
            step=1,
            help="Diameter of the Ferris wheel in meters (30-80).",
            key="diameter_input_step1"
        )
        st.caption("Unit: meters [m] — must be between 30 and 80")
    with col2:
        # Determine base using default assumption (non-spherical -> pi*d/4)
        default_base = base_for_geometry(diameter, geometry=None)
        base_cabins_guess = int(np.pi * diameter / 4.0)
        st.caption("Note: base cabin-count is estimated using π×d/4 until you choose cabin geometry.")

    # Update diameter
    st.session_state.diameter = diameter

    # Cabin count: compute a reasonable min/max using default formula (pi*d/4)
    min_cabins, max_cabins = calculate_cabin_range_from_base(default_base, diameter)
    num_cabins = st.number_input(
        "Number of Cabins",
        min_value=min_cabins,
        max_value=max_cabins,
        value=min(max(int(st.session_state.num_cabins), min_cabins), max_cabins),
        step=1,
        help=f"Number of passenger cabins (enforced between {min_cabins} and {max_cabins})",
        key="num_cabins_input_step1"
    )
    st.session_state.num_cabins = num_cabins

    # Cabin capacity (per cabin)
    col1, col2 = st.columns(2)
    with col1:
        cabin_capacity = st.number_input(
            "Cabin Capacity (passengers per cabin)",
            min_value=4,
            max_value=8,
            value=st.session_state.cabin_capacity,
            step=1,
            help="Passengers per cabin (4-8).",
            key="cabin_capacity_input_merged"
        )
        st.session_state.cabin_capacity = cabin_capacity
    with col2:
        # VIP cabins input on same page
        num_vip_cabins = st.number_input(
            "Number of VIP Cabins",
            min_value=0,
            max_value=st.session_state.num_cabins,
            value=min(st.session_state.num_vip_cabins, st.session_state.num_cabins),
            step=1,
            help=f"VIP cabins (each VIP cabin holds 2 fewer passengers).",
            key="num_vip_input_merged"
        )
        st.session_state.num_vip_cabins = num_vip_cabins

    st.markdown("---")
    st.write("When VIP cabins exist, each VIP cabin has capacity = (cabin capacity - 2).")
    st.write("Click **Calculate Capacities** to compute total capacities; after that you can proceed to next step.")

    if st.button("🔄 Calculate Capacities", key="calc_caps_merged"):
        # compute capacities according to VIP rule
        vip_cap = max(0, st.session_state.cabin_capacity - 2)
        total_capacity = st.session_state.num_cabins * st.session_state.cabin_capacity  # raw if all same
        vip_total = st.session_state.num_vip_cabins * vip_cap
        regular_total = (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity
        effective_total_per_rotation = vip_total + regular_total

        cap_col1, cap_col2, cap_col3 = st.columns(3)
        cap_col1.metric("Per-rotation capacity", f"{effective_total_per_rotation} passengers")
        cap_col2.metric("VIP cabins capacity (per rotation)", f"{vip_total} passengers (each VIP: {vip_cap})")
        cap_col3.metric("Total cabins", f"{st.session_state.num_cabins} cabins")

        st.success("Capacities calculated. You can now proceed to the next step.")
        st.session_state.capacities_calculated = True

    # Navigation: Back always, Next only via next_with_validation which checks capacities_calculated
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", key="back_from_step1", on_click=go_back)
    with right_col:
        st.button("Next ➡️", key="next_from_step1", on_click=next_with_validation)

# === STEP 2: Cabin Geometry Selection (dedicated page) ===
elif st.session_state.step == 2:
    st.header("Step 3: Cabin Geometry Selection")
    st.markdown("Choose cabin geometry. After choosing, base cabin-count formula will update accordingly.")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📦 Square", key="geom_square"):
            st.session_state.cabin_geometry = "Square"
            st.session_state.geometry_selected = True
    with col2:
        if st.button("🔴 Vertical Cylinder", key="geom_vcyl"):
            st.session_state.cabin_geometry = "Vertical Cylinder"
            st.session_state.geometry_selected = True
    with col3:
        if st.button("🔵 Horizontal Cylinder", key="geom_hcyl"):
            st.session_state.cabin_geometry = "Horizontal Cylinder"
            st.session_state.geometry_selected = True
    with col4:
        if st.button("⚪ Spherical", key="geom_sphere"):
            st.session_state.cabin_geometry = "Spherical"
            st.session_state.geometry_selected = True

    if st.session_state.cabin_geometry:
        st.success(f"✅ Selected Geometry: {st.session_state.cabin_geometry}")

        # After geometry selection, recompute base and valid cabin range; if current num_cabins is out of new range, warn user
        base = base_for_geometry(st.session_state.diameter, st.session_state.cabin_geometry)
        min_c, max_c = calculate_cabin_range_from_base(base, st.session_state.diameter)
        st.write(f"Using geometry = **{st.session_state.cabin_geometry}**, base = {base:.1f}. Acceptable cabins: {min_c} to {max_c}.")

        if st.session_state.num_cabins < min_c or st.session_state.num_cabins > max_c:
            st.warning(f"Current number of cabins ({st.session_state.num_cabins}) is outside the acceptable range for the chosen geometry. Please go back and adjust the cabin count.")
            # Prevent forward movement until adjusted (validation will block)
    st.markdown("---")

    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", key="back_from_geom", on_click=go_back)
    with right_col:
        st.button("Next ➡️", key="next_from_geom", on_click=next_with_validation)

# === STEP 3: Rotation Time Confirmation (only rotation time editable) ===
elif st.session_state.step == 3:
    st.header("Step 4: Rotation Time & Derived Speeds")
    st.markdown("We assume linear speed v = 0.2 m/s as default for initial estimates. You can confirm or change the **rotation time** (minutes per rotation). Other values will be updated automatically.")
    st.markdown("---")

    diameter = st.session_state.diameter
    radius = diameter / 2.0
    assumed_v = 0.2  # m/s as per specification

    # computed from assumed velocity
    ang_from_v, rpm_from_v = calculate_linear_speed_from_v_and_d(assumed_v, diameter)
    st.write(f"Assumed linear speed: **{assumed_v:.3f} m/s** → angular speed = **{ang_from_v:.4f} rad/s**, rpm = **{rpm_from_v:.3f} rpm** (based on diameter).")

    # Default rotation time based on circumference / v
    circumference = np.pi * diameter
    default_rotation_time_seconds = circumference / assumed_v if assumed_v > 0 else None
    default_rotation_time_min = default_rotation_time_seconds / 60.0 if default_rotation_time_seconds else None

    # rotation time editable box (minutes per rotation) - this is the only editable box in this page
    rotation_time_min = st.number_input(
        "Rotation time (minutes per full rotation)",
        min_value=0.01,
        max_value=60.0,
        value=st.session_state.rotation_time_min if st.session_state.rotation_time_min else float(default_rotation_time_min if default_rotation_time_min else 1.0),
        step=0.01,
        format="%.2f",
        key="rotation_time_input"
    )
    st.session_state.rotation_time_min = rotation_time_min

    # Derived quantities from user-provided rotation time
    rotation_time_sec = rotation_time_min * 60.0
    if rotation_time_sec > 0:
        ang_from_time = 2.0 * np.pi / rotation_time_sec  # rad/s
        rpm_from_time = ang_from_time * 60.0 / (2.0 * np.pi)
        linear_speed_from_time = ang_from_time * radius
    else:
        ang_from_time = rpm_from_time = linear_speed_from_time = 0.0

    st.write(f"Derived from rotation time: angular speed = **{ang_from_time:.4f} rad/s**, rpm = **{rpm_from_time:.3f} rpm**, linear speed = **{linear_speed_from_time:.3f} m/s**.")

    # Capacity per hour based on rotation_time and VIP rule
    cap_per_hour = calculate_capacity_per_hour_from_time(
        st.session_state.num_cabins,
        st.session_state.cabin_capacity,
        st.session_state.num_vip_cabins,
        rotation_time_min
    )
    st.metric("Estimated Capacity per Hour (assuming full occupancy)", f"{cap_per_hour:.0f} passengers/hour")

    st.markdown("If you adjust rotation time, the derived speeds and capacity/hour will update automatically. When satisfied, click Next.")
    st.markdown("---")

    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", key="back_from_rotation", on_click=go_back)
    with right_col:
        st.button("Next ➡️", key="next_from_rotation", on_click=next_with_validation)

# === STEP 4: Environment Conditions ===
elif st.session_state.step == 4:
    st.header("Step 5: Environment Conditions")
    st.markdown("---")

    # Provide provinces of Iran list (short list; extend if needed)
    iran_provinces = [
        "Tehran", "Isfahan", "Fars", "Khorasan Razavi", "East Azerbaijan", "West Azerbaijan",
        "Mazandaran", "Gilan", "Kerman", "Hormozgan", "Sistan and Baluchestan", "Kurdistan",
        "Lorestan", "Alborz", "Qom", "Markazi", "Yazd", "Chaharmahal and Bakhtiari", "Ardabil",
        "Zanjan", "Golestan", "North Khorasan", "South Khorasan", "Khuzestan", "Ilam", "Bushehr"
    ]

    col1, col2 = st.columns(2)
    with col1:
        province = st.selectbox("Province (استان)", options=iran_provinces, index=0, key="province_input")
    with col2:
        region_name = st.text_input("Region / Area name (نام منطقه)", value=st.session_state.environment_data.get('region_name',''), key="region_input")

    st.markdown("---")
    st.subheader("📏 Land Surface Area (meters)")
    col1, col2 = st.columns(2)
    with col1:
        land_length = st.number_input(
            "Land Length (m)",
            min_value=10.0,
            max_value=150.0,
            value=st.session_state.environment_data.get('land_length', 100.0),
            step=1.0,
            key="land_length_input_env"
        )
    with col2:
        land_width = st.number_input(
            "Land Width (m)",
            min_value=10.0,
            max_value=150.0,
            value=st.session_state.environment_data.get('land_width', 100.0),
            step=1.0,
            key="land_width_input_env2"
        )
    land_area = land_length * land_width
    st.metric("Total Land Area", f"{land_area:.2f} m²")

    st.markdown("---")
    st.subheader("📈 Altitude and Temperature")
    col1, col2 = st.columns(2)
    with col1:
        altitude = st.number_input("Altitude (m)", value=st.session_state.environment_data.get('altitude', 0.0), key="altitude_input")
    with col2:
        temp_min = st.number_input("Minimum Temperature (°C)", value=st.session_state.environment_data.get('temp_min', -10.0), key="temp_min_env")
    temp_max = st.number_input("Maximum Temperature (°C)", value=st.session_state.environment_data.get('temp_max', 40.0), key="temp_max_env")

    st.markdown("---")
    st.subheader("🌬️ Wind Information")
    col1, col2 = st.columns(2)
    with col1:
        wind_dir = st.selectbox("Wind Direction", options=["south", "west", "east", "north", "north-west", "north-east", "south-east", "south-west"], index=0, key="wind_dir_env")
    with col2:
        # ask wind in km/h as requested
        wind_max = st.number_input("Maximum Wind Speed (km/h)", min_value=0.0, value=st.session_state.environment_data.get('wind_max', 108.0), step=1.0, key="wind_max_env")
        wind_avg = st.number_input("Average Wind Speed (km/h)", min_value=0.0, value=st.session_state.environment_data.get('wind_avg', 54.0), step=1.0, key="wind_avg_env")

    st.markdown("---")
    # Upload wind rose optional checkbox
    load_wind_rose = st.checkbox("Load wind rose (upload jpg/pdf)", value=st.session_state.wind_rose_loaded, key="load_wind_rose_checkbox")
    st.session_state.wind_rose_loaded = load_wind_rose
    wind_rose_file = None
    if load_wind_rose:
        wind_rose_file = st.file_uploader("Wind rose file (jpg or pdf)", type=['jpg','jpeg','pdf'], key="wind_rose_uploader")
        st.session_state.wind_rose_file = wind_rose_file

    # Save environment_data to session
    st.session_state.environment_data = {
        'province': province,
        'region_name': region_name,
        'land_length': land_length,
        'land_width': land_width,
        'land_area': land_area,
        'altitude': altitude,
        'temp_min': temp_min,
        'temp_max': temp_max,
        'wind_direction': wind_dir,
        'wind_max': wind_max,
        'wind_avg': wind_avg
    }

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", key="back_from_env", on_click=go_back)
    with right_col:
        st.button("Next ➡️", key="next_from_env", on_click=next_with_validation)

# === STEP 5: Final Design Overview & Visualization ===
elif st.session_state.step == 5:
    st.header("Step 6: Design Overview & Visualization")
    st.markdown("---")

    # Display comprehensive design summary
    st.subheader("📋 Design Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Basic Parameters:**")
        st.write(f"• Generation: {st.session_state.generation_type}")
        st.write(f"• Diameter: {st.session_state.diameter} m")
        st.write(f"• Total Cabins: {st.session_state.num_cabins}")
        st.write(f"• VIP Cabins: {st.session_state.num_vip_cabins} (each -2 pax)")
        st.write(f"• Cabin Capacity (regular): {st.session_state.cabin_capacity} passengers")
        if st.session_state.cabin_geometry:
            st.write(f"• Cabin Geometry: {st.session_state.cabin_geometry}")
    with col2:
        st.markdown("**Environment Conditions:**")
        env = st.session_state.environment_data
        if env:
            st.write(f"• Province: {env.get('province','N/A')}")
            st.write(f"• Region: {env.get('region_name','N/A')}")
            st.write(f"• Land Area: {env.get('land_area',0):.2f} m²")
            st.write(f"• Altitude: {env.get('altitude','N/A')} m")
            st.write(f"• Temperature: {env.get('temp_min',0)}°C to {env.get('temp_max',0)}°C")
            st.write(f"• Wind: {env.get('wind_max',0)} km/h (max), {env.get('wind_avg',0)} km/h (avg), dir: {env.get('wind_direction','N/A')}")
            if st.session_state.wind_rose_loaded and st.session_state.wind_rose_file:
                st.write("• Wind rose: Uploaded")
            elif st.session_state.wind_rose_loaded:
                st.write("• Wind rose: (enabled but no file uploaded)")

    st.markdown("---")
    # Component diagram
    st.subheader("🎡 Ferris Wheel Design Visualization")

    height = st.session_state.diameter * 1.1
    vip_cap = max(0, st.session_state.cabin_capacity - 2)
    total_capacity_per_rotation = st.session_state.num_vip_cabins * vip_cap + (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity

    # Estimate motor power (simple heuristic)
    angular_speed = (2.0 * np.pi) / (st.session_state.rotation_time_min * 60.0) if st.session_state.rotation_time_min else 0.0
    total_mass = st.session_state.num_cabins * st.session_state.cabin_capacity * 80.0
    moment_of_inertia = total_mass * (st.session_state.diameter/2.0)**2
    motor_power = moment_of_inertia * angular_speed**2 / 1000.0 if angular_speed else 0.0

    fig = create_component_diagram(st.session_state.diameter, height, total_capacity_per_rotation, motor_power)
    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})

    st.info("🚧 Structural, electrical and safety analyses are beyond this simplified designer and will be added later.")

    left_col, mid_col, right_col = st.columns([1,0.5,1])
    with left_col:
        st.button("⬅️ Back", key="back_from_final", on_click=go_back)
    with mid_col:
        st.button("🔄 New Design", key="reset_from_final", on_click=reset_design)
    st.success("✅ Design Complete!")
