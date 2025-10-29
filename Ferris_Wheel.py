import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Ferris Wheel Designer",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Session State Initialization ---
if 'step' not in st.session_state:
    st.session_state.step = 0  # 0: generation, 1: cabin geometry (was 2), 2: primary params (was 1), 3: rotation, 4: environment, 5: final
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
if 'capacities_calculated' not in st.session_state:
    st.session_state.capacities_calculated = False
if 'environment_data' not in st.session_state:
    st.session_state.environment_data = {}
if 'wind_rose_loaded' not in st.session_state:
    st.session_state.wind_rose_loaded = False
if 'wind_rose_file' not in st.session_state:
    st.session_state.wind_rose_file = None
if 'validation_errors' not in st.session_state:
    st.session_state.validation_errors = []

# --- Helper functions ---
def base_for_geometry(diameter, geometry):
    """If geometry is spherical use pi*d/5, else pi*d/4"""
    if geometry == "Spherical":
        return np.pi * diameter / 5.0
    else:
        return np.pi * diameter / 4.0

def calc_min_max_from_base(base):
    min_c = int(np.floor(base * 0.7))
    max_c = int(np.ceil(base * 1.2))
    min_c = max(3, min_c)
    max_c = max(min_c, max_c)
    return min_c, max_c

def calculate_capacity_per_hour_from_time(num_cabins, cabin_capacity, num_vip, rotation_time_minutes):
    """Capacity per hour considering VIP cabins hold (capacity-2)"""
    if rotation_time_minutes is None or rotation_time_minutes <= 0:
        return 0
    rotations_per_hour = 60.0 / rotation_time_minutes
    vip_cap = max(0, cabin_capacity - 2)
    regular_cabins = num_cabins - num_vip
    passengers_per_rotation = num_vip * vip_cap + regular_cabins * cabin_capacity
    return passengers_per_rotation * rotations_per_hour

def calc_ang_rpm_linear_from_rotation_time(rotation_time_min, diameter):
    if rotation_time_min and rotation_time_min > 0:
        sec = rotation_time_min * 60.0
        ang = 2.0 * np.pi / sec  # rad/s
        rpm = ang * 60.0 / (2.0 * np.pi)
        linear = ang * (diameter / 2.0)
        return ang, rpm, linear
    return 0.0, 0.0, 0.0

def create_component_diagram(diameter, height, capacity, motor_power):
    theta = np.linspace(0, 2*np.pi, 200)
    x_wheel = diameter/2 * np.cos(theta)
    y_wheel = diameter/2 * np.sin(theta) + height/2

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_wheel, y=y_wheel, mode='lines', line=dict(color='#2196F3', width=3), showlegend=False))
    fig.add_trace(go.Scatter(x=[0,0], y=[0,height/2], mode='lines', line=dict(color='#FF5722', width=6), showlegend=False))

    annotations = [
        dict(x=0, y=height + diameter*0.05 + 2, text=f"Height: {height} m", showarrow=False, font=dict(color='black')),
        dict(x=diameter/2 + 2, y=height/2, text=f"Diameter: {diameter} m", showarrow=False, font=dict(color='black')),
        dict(x=0, y=-5, text=f"Motor Power: {motor_power:.1f} kW", showarrow=False, font=dict(color='black')),
        dict(x=0, y=-8, text=f"Capacity: {capacity} passengers", showarrow=False, font=dict(color='black'))
    ]
    fig.update_layout(title=dict(text="Ferris Wheel Design Overview", font=dict(color='black')),
                      height=620, template="plotly_white", plot_bgcolor='white', paper_bgcolor='white',
                      annotations=annotations, margin=dict(l=80, r=80, t=80, b=80))
    return fig

# --- Navigation & validation ---
def select_generation(gen):
    st.session_state.generation_type = gen
    # go directly to cabin geometry page on single click
    st.session_state.step = 1

def go_back():
    st.session_state.step = max(0, st.session_state.step - 1)

def reset_design():
    st.session_state.step = 0
    st.session_state.generation_type = None
    st.session_state.diameter = 60
    st.session_state.num_cabins = 12
    st.session_state.cabin_capacity = 6
    st.session_state.num_vip_cabins = 1
    st.session_state.cabin_geometry = None
    st.session_state.rotation_time_min = None
    st.session_state.capacities_calculated = False
    st.session_state.environment_data = {}
    st.session_state.wind_rose_loaded = False
    st.session_state.wind_rose_file = None
    st.session_state.validation_errors = []

def validate_current_step_and_next():
    s = st.session_state
    errors = []

    if s.step == 0:
        if not s.generation_type:
            errors.append("Please select a generation.")
    elif s.step == 1:
        # cabin geometry step
        if not s.cabin_geometry:
            errors.append("Please select a cabin geometry.")
    elif s.step == 2:
        # primary params enforced 30-80
        if s.diameter is None or s.diameter < 30 or s.diameter > 80:
            errors.append("Diameter must be between 30 and 80 meters.")
        if s.num_cabins is None or s.num_cabins <= 0:
            errors.append("Set a valid number of cabins.")
        if s.cabin_capacity is None or s.cabin_capacity < 4 or s.cabin_capacity > 8:
            errors.append("Cabin capacity must be between 4 and 8.")
        if s.num_vip_cabins is None or s.num_vip_cabins < 0 or s.num_vip_cabins > s.num_cabins:
            errors.append("Number of VIP cabins must be between 0 and total cabins.")
        if not s.capacities_calculated:
            errors.append("Please click 'Calculate Capacities' before continuing.")
    elif s.step == 3:
        if s.rotation_time_min is None or s.rotation_time_min <= 0:
            errors.append("Enter valid rotation time (minutes per rotation).")
    elif s.step == 4:
        env = s.environment_data
        if not env.get('province'):
            errors.append("Select a province.")
        if not env.get('region_name'):
            errors.append("Enter region name.")
        if 'land_length' not in env or env['land_length'] < 10 or env['land_length'] > 150:
            errors.append("Land length must be between 10 and 150 meters.")
        if 'land_width' not in env or env['land_width'] < 10 or env['land_width'] > 150:
            errors.append("Land width must be between 10 and 150 meters.")
        if 'altitude' not in env or env['altitude'] is None:
            errors.append("Enter altitude.")
        if 'wind_max' not in env or env['wind_max'] is None:
            errors.append("Enter maximum wind speed (km/h).")
        if s.wind_rose_loaded and not s.wind_rose_file:
            errors.append("Wind rose enabled but no file uploaded.")
    # show errors or advance
    if errors:
        st.session_state.validation_errors = errors
        for e in errors:
            st.error(e)
    else:
        st.session_state.validation_errors = []
        st.session_state.step = min(5, st.session_state.step + 1)

# --- UI ---
st.title("🎡 Ferris Wheel Designer")
total_steps = 6
st.progress(st.session_state.step / (total_steps - 1))
st.markdown(f"**Step {st.session_state.step + 1} of {total_steps}**")
st.markdown("---")

# === STEP 0: Generation selection (single-click advances to geometry) ===
if st.session_state.step == 0:
    st.header("Step 1: Select Ferris Wheel Generation")
    c1, c2 = st.columns(2)
    with c1:
        st.button("🎡 1st Generation (Truss type)", key="gen_btn_1", on_click=select_generation, args=("1st Generation (Truss type)",))
    with c2:
        st.button("🎡 2nd Generation (Cable type)", key="gen_btn_2", on_click=select_generation, args=("2nd Generation (Cable type)",))
    c3, c4 = st.columns(2)
    with c3:
        st.button("🎡 2nd Generation (Pure cable type)", key="gen_btn_3", on_click=select_generation, args=("2nd Generation (Pure cable type)",))
    with c4:
        st.button("🎡 4th Generation (Hubless centerless)", key="gen_btn_4", on_click=select_generation, args=("4th Generation (Hubless centerless)",))

# === STEP 1: Cabin Geometry (moved to be the first page after generation) ===
elif st.session_state.step == 1:
    st.header("Step 2: Cabin Geometry Selection")
    # minimal UI: only buttons (no long explanations or calculation details)
    col1, col2, col3, col4 = st.columns(4)

    # Square
    with col1:
        if st.button("📦 Square", key="geom_square"):
            st.session_state.cabin_geometry = "Square"
            base = base_for_geometry(st.session_state.diameter, st.session_state.cabin_geometry)
            min_c, max_c = calc_min_max_from_base(base)
            # auto-clamp silently
            if st.session_state.num_cabins < min_c:
                st.session_state.num_cabins = min_c
            elif st.session_state.num_cabins > max_c:
                st.session_state.num_cabins = max_c
            st.session_state.capacities_calculated = False
            # advance to primary parameters
            st.session_state.step = 2

    # Vertical Cylinder
    with col2:
        if st.button("🔴 Vertical Cylinder", key="geom_vcyl"):
            st.session_state.cabin_geometry = "Vertical Cylinder"
            base = base_for_geometry(st.session_state.diameter, st.session_state.cabin_geometry)
            min_c, max_c = calc_min_max_from_base(base)
            if st.session_state.num_cabins < min_c:
                st.session_state.num_cabins = min_c
            elif st.session_state.num_cabins > max_c:
                st.session_state.num_cabins = max_c
            st.session_state.capacities_calculated = False
            st.session_state.step = 2

    # Horizontal Cylinder
    with col3:
        if st.button("🔵 Horizontal Cylinder", key="geom_hcyl"):
            st.session_state.cabin_geometry = "Horizontal Cylinder"
            base = base_for_geometry(st.session_state.diameter, st.session_state.cabin_geometry)
            min_c, max_c = calc_min_max_from_base(base)
            if st.session_state.num_cabins < min_c:
                st.session_state.num_cabins = min_c
            elif st.session_state.num_cabins > max_c:
                st.session_state.num_cabins = max_c
            st.session_state.capacities_calculated = False
            st.session_state.step = 2

    # Spherical
    with col4:
        if st.button("⚪ Spherical", key="geom_sphere"):
            st.session_state.cabin_geometry = "Spherical"
            base = base_for_geometry(st.session_state.diameter, st.session_state.cabin_geometry)
            min_c, max_c = calc_min_max_from_base(base)
            if st.session_state.num_cabins < min_c:
                st.session_state.num_cabins = min_c
            elif st.session_state.num_cabins > max_c:
                st.session_state.num_cabins = max_c
            st.session_state.capacities_calculated = False
            st.session_state.step = 2

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 2: Primary parameters + Cabin capacity + VIP (one page) ===
elif st.session_state.step == 2:
    st.header("Step 3: Primary Parameters, Cabin Capacity & VIP")
    st.subheader(f"Generation: {st.session_state.generation_type}")
    st.markdown("---")

    # Diameter (30-80)
    col1, col2 = st.columns(2)
    with col1:
        diameter = st.number_input(
            "Ferris Wheel Diameter (m)",
            min_value=30,
            max_value=80,
            value=int(st.session_state.diameter),
            step=1,
            key="diameter_input"
        )
        st.session_state.diameter = diameter

    # Base & cabin count: base depends on geometry if set, else default to pi*d/4
    geometry = st.session_state.cabin_geometry
    base = base_for_geometry(diameter, geometry) if geometry else (np.pi * diameter / 4.0)
    min_c, max_c = calc_min_max_from_base(base)

    num_cabins = st.number_input(
        "Number of Cabins",
        min_value=min_c,
        max_value=max_c,
        value=min(max(int(st.session_state.num_cabins), min_c), max_c),
        step=1,
        key="num_cabins_input"
    )
    st.session_state.num_cabins = num_cabins

    # Cabin capacity & VIP on same page
    c1, c2 = st.columns(2)
    with c1:
        cabin_capacity = st.number_input(
            "Cabin Capacity (passengers per cabin)",
            min_value=4,
            max_value=8,
            value=st.session_state.cabin_capacity,
            step=1,
            key="cabin_capacity_input"
        )
        st.session_state.cabin_capacity = cabin_capacity
    with c2:
        num_vip = st.number_input(
            "Number of VIP Cabins",
            min_value=0,
            max_value=st.session_state.num_cabins,
            value=min(st.session_state.num_vip_cabins, st.session_state.num_cabins),
            step=1,
            key="num_vip_input"
        )
        st.session_state.num_vip_cabins = num_vip

    st.markdown("---")
    if st.button("🔄 Calculate Capacities"):
        vip_cap = max(0, st.session_state.cabin_capacity - 2)
        vip_total = st.session_state.num_vip_cabins * vip_cap
        regular_total = (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity
        per_rotation = vip_total + regular_total
        c1, c2, c3 = st.columns(3)
        c1.metric("Per-rotation capacity", f"{per_rotation} passengers")
        c2.metric("VIP capacity (per rotation)", f"{vip_total} passengers (each VIP: {vip_cap})")
        c3.metric("Total cabins", f"{st.session_state.num_cabins}")
        st.success("Capacities calculated.")
        st.session_state.capacities_calculated = True

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 3: Rotation Time & Derived Speeds (only rotation time editable) ===
elif st.session_state.step == 3:
    st.header("Step 4: Rotation Time & Derived Speeds")
    st.markdown("Enter rotation time (minutes per full rotation). Angular speed (rad/s), rotational speed (rpm) and linear speed (m/s) at rim are shown (read-only).")
    st.markdown("---")

    diameter = st.session_state.diameter
    # default rotation time computed from circumference / 0.2 m/s
    circumference = np.pi * diameter
    default_rotation_time_min = (circumference / 0.2) / 60.0 if diameter > 0 else 1.0

    rotation_time_min = st.number_input(
        "Rotation time (minutes per full rotation)",
        min_value=0.01,
        max_value=60.0,
        value=st.session_state.rotation_time_min if st.session_state.rotation_time_min else float(default_rotation_time_min),
        step=0.01,
        format="%.2f",
        key="rotation_time_input"
    )
    st.session_state.rotation_time_min = rotation_time_min

    ang, rpm, linear = calc_ang_rpm_linear_from_rotation_time(rotation_time_min, diameter)

    # Display read-only values
    st.text_input("Angular speed (rad/s)", value=f"{ang:.6f}", disabled=True)
    st.text_input("Rotational speed (rpm)", value=f"{rpm:.6f}", disabled=True)
    st.text_input("Linear speed at rim (m/s)", value=f"{linear:.6f}", disabled=True)

    # capacity per hour
    cap_per_hour = calculate_capacity_per_hour_from_time(
        st.session_state.num_cabins,
        st.session_state.cabin_capacity,
        st.session_state.num_vip_cabins,
        rotation_time_min
    )
    st.metric("Estimated Capacity per Hour (assuming full occupancy)", f"{cap_per_hour:.0f} passengers/hour")

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 4: Environment Conditions (English labels) ===
elif st.session_state.step == 4:
    st.header("Step 5: Environment Conditions")
    st.markdown("---")

    iran_provinces = [
        "Tehran", "Isfahan", "Fars", "Khorasan Razavi", "East Azerbaijan", "West Azerbaijan",
        "Mazandaran", "Gilan", "Kerman", "Hormozgan", "Sistan and Baluchestan", "Kurdistan",
        "Lorestan", "Alborz", "Qom", "Markazi", "Yazd", "Chaharmahal and Bakhtiari", "Ardabil",
        "Zanjan", "Golestan", "North Khorasan", "South Khorasan", "Khuzestan", "Ilam", "Bushehr"
    ]

    c1, c2 = st.columns(2)
    with c1:
        province = st.selectbox("Province", options=iran_provinces, index=0, key="province_select")
    with c2:
        region_name = st.text_input("Region / Area name", value=st.session_state.environment_data.get('region_name', ''), key="region_name_input")

    st.markdown("---")
    st.subheader("Land Surface Area (meters)")
    l1, l2 = st.columns(2)
    with l1:
        land_length = st.number_input("Land Length (m)", min_value=10.0, max_value=150.0, value=st.session_state.environment_data.get('land_length', 100.0), key="land_length_input")
    with l2:
        land_width = st.number_input("Land Width (m)", min_value=10.0, max_value=150.0, value=st.session_state.environment_data.get('land_width', 100.0), key="land_width_input")
    st.metric("Total Land Area", f"{land_length * land_width:.2f} m²")

    st.markdown("---")
    st.subheader("Altitude and Temperature")
    a1, a2 = st.columns(2)
    with a1:
        altitude = st.number_input("Altitude (m)", value=st.session_state.environment_data.get('altitude', 0.0), key="altitude_input")
    with a2:
        temp_min = st.number_input("Minimum Temperature (°C)", value=st.session_state.environment_data.get('temp_min', -10.0), key="temp_min_input")
    temp_max = st.number_input("Maximum Temperature (°C)", value=st.session_state.environment_data.get('temp_max', 40.0), key="temp_max_input")

    st.markdown("---")
    st.subheader("Wind Information")
    w1, w2 = st.columns(2)
    with w1:
        wind_dir = st.selectbox("Wind Direction", options=["south", "west", "east", "north", "north-west", "north-east", "south-east", "south-west"], key="wind_dir_input")
    with w2:
        wind_max = st.number_input("Maximum Wind Speed (km/h)", min_value=0.0, value=st.session_state.environment_data.get('wind_max', 108.0), key="wind_max_input")
        wind_avg = st.number_input("Average Wind Speed (km/h)", min_value=0.0, value=st.session_state.environment_data.get('wind_avg', 54.0), key="wind_avg_input")

    st.markdown("---")
    load_wind = st.checkbox("Load wind rose (upload jpg/pdf)", value=st.session_state.wind_rose_loaded, key="load_wind_checkbox")
    st.session_state.wind_rose_loaded = load_wind
    wind_file = None
    if load_wind:
        wind_file = st.file_uploader("Wind rose file (jpg/pdf)", type=['jpg', 'jpeg', 'pdf'], key="wind_rose_uploader")
        st.session_state.wind_rose_file = wind_file

    # save environment data
    st.session_state.environment_data = {
        'province': province,
        'region_name': region_name,
        'land_length': land_length,
        'land_width': land_width,
        'land_area': land_length * land_width,
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
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 5: Final Design Overview & Visualization ===
elif st.session_state.step == 5:
    st.header("Step 6: Design Overview & Visualization")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Basic Parameters:**")
        st.write(f"• Generation: {st.session_state.generation_type}")
        st.write(f"• Diameter: {st.session_state.diameter} m")
        st.write(f"• Total Cabins: {st.session_state.num_cabins}")
        st.write(f"• VIP Cabins: {st.session_state.num_vip_cabins} (each -2 pax)")
        st.write(f"• Cabin Capacity (regular): {st.session_state.cabin_capacity}")
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
            st.write(f"• Wind Direction: {env.get('wind_direction','N/A')}")
            st.write(f"• Max Wind Speed: {env.get('wind_max',0)} km/h")

    st.markdown("---")
    # visualization
    height = st.session_state.diameter * 1.1
    vip_cap = max(0, st.session_state.cabin_capacity - 2)
    total_capacity_per_rotation = st.session_state.num_vip_cabins * vip_cap + (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity

    # estimate motor power (simple heuristic)
    ang = (2.0 * np.pi) / (st.session_state.rotation_time_min * 60.0) if st.session_state.rotation_time_min else 0.0
    total_mass = st.session_state.num_cabins * st.session_state.cabin_capacity * 80.0
    moment_of_inertia = total_mass * (st.session_state.diameter/2.0)**2
    motor_power = moment_of_inertia * ang**2 / 1000.0 if ang else 0.0

    fig = create_component_diagram(st.session_state.diameter, height, total_capacity_per_rotation, motor_power)
    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})

    st.info("🚧 Structural, electrical and safety analyses are not included in this simplified designer.")
    st.markdown("---")
    l, m, r = st.columns([1,0.5,1])
    with l:
        st.button("⬅️ Back", on_click=go_back)
    with m:
        st.button("🔄 New Design", on_click=reset_design)
    st.success("✅ Design Complete!")



