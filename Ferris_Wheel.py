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
    st.session_state.step = 0  # 0..6
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
if 'classification_data' not in st.session_state:
    st.session_state.classification_data = {}
if 'braking_acceleration' not in st.session_state:
    st.session_state.braking_acceleration = 0.7

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


def calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g=9.81):
    """Calculate acceleration components at a given angle theta (radians)"""
    radius = diameter / 2.0
    a_centripetal = radius * (angular_velocity ** 2)

    a_z_gravity = -g
    a_x_gravity = 0

    a_x_centripetal = -a_centripetal * (-np.cos(theta))
    a_z_centripetal = -a_centripetal * (-np.sin(theta))

    a_x_braking = -braking_accel * (-np.sin(theta))
    a_z_braking = -braking_accel * (np.cos(theta))

    a_x_total = a_x_gravity + a_x_centripetal + a_x_braking
    a_z_total = a_z_gravity + a_z_centripetal + a_z_braking

    a_total = np.sqrt(a_x_total**2 + a_z_total**2)

    return a_x_total, a_z_total, a_total


def calculate_dynamic_product(diameter, height, angular_velocity, braking_accel, g=9.81):
    theta_vals = np.linspace(0, 2*np.pi, 360)
    max_accel = 0

    for theta in theta_vals:
        _, _, a_total = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g)
        if a_total > max_accel:
            max_accel = a_total

    v = (diameter / 2.0) * angular_velocity
    n = max_accel / g
    p = v * height * n

    return p, n, max_accel


def classify_device(dynamic_product, is_design=True):
    if is_design:
        if 0.1 < dynamic_product <= 25:
            return 1
        elif 25 < dynamic_product <= 100:
            return 2
        elif 100 < dynamic_product <= 200:
            return 3
        else:
            return 4
    else:
        if 0.1 < dynamic_product <= 25:
            return 2
        elif 25 < dynamic_product <= 100:
            return 3
        elif 100 < dynamic_product <= 200:
            return 4
        else:
            return 5


def determine_restraint_area(ax, az):
    if ax > 1.2 and -0.2 <= az <= 0.2:
        return 1
    if -0.2 <= ax <= 0.2 and -0.7 <= az <= 0.2:
        return 2
    if -1.2 <= ax < -0.2 and -0.7 <= az <= 0.2:
        return 3
    if -1.2 <= ax and -1.8 <= az < -0.7:
        return 4
    if az > 0.2:
        return 5
    return 2


def plot_acceleration_envelope(diameter, angular_velocity, braking_accel, g=9.81):
    theta_vals = np.linspace(0, 2*np.pi, 360)
    ax_vals = []
    az_vals = []

    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g)
        ax_vals.append(a_x / g)
        az_vals.append(a_z / g)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ax_vals, y=az_vals, mode='lines', line=dict(color='#2196F3', width=3), name='Acceleration Envelope'))

    # area boxes
    fig.add_shape(type="rect", x0=1.2, y0=-0.2, x1=2.0, y1=0.2, line=dict(color="red", width=2, dash="dash"), fillcolor="rgba(255,0,0,0.1)")
    fig.add_shape(type="rect", x0=-0.2, y0=-0.7, x1=0.2, y1=0.2, line=dict(color="orange", width=2, dash="dash"), fillcolor="rgba(255,165,0,0.1)")
    fig.add_shape(type="rect", x0=-1.2, y0=-0.7, x1=-0.2, y1=0.2, line=dict(color="yellow", width=2, dash="dash"), fillcolor="rgba(255,255,0,0.1)")
    fig.add_shape(type="rect", x0=-1.2, y0=-1.8, x1=0, y1=-0.7, line=dict(color="green", width=2, dash="dash"), fillcolor="rgba(0,255,0,0.1)")
    fig.add_shape(type="rect", x0=-2.0, y0=0.2, x1=2.0, y1=1.5, line=dict(color="purple", width=2, dash="dash"), fillcolor="rgba(128,0,128,0.1)")

    fig.update_layout(title="Passenger Acceleration Envelope (ax vs az)", xaxis_title="Horizontal Acceleration ax [g]", yaxis_title="Vertical Acceleration az [g]", height=600, template="plotly_white", showlegend=True, xaxis=dict(range=[-2, 2], zeroline=True, zerolinewidth=2, zerolinecolor='black'), yaxis=dict(range=[-2, 1.5], zeroline=True, zerolinewidth=2, zerolinecolor='black'))
    return fig

# --- Navigation & validation ---
def select_generation(gen):
    st.session_state.generation_type = gen
    st.session_state.step = 1


def select_geometry_and_advance(geom_label):
    # helper to choose geometry and go to primary params
    st.session_state.cabin_geometry = geom_label
    base = base_for_geometry(st.session_state.diameter, st.session_state.cabin_geometry)
    min_c, max_c = calc_min_max_from_base(base)
    # clamp cabins silently
    if st.session_state.num_cabins < min_c:
        st.session_state.num_cabins = min_c
    elif st.session_state.num_cabins > max_c:
        st.session_state.num_cabins = max_c
    st.session_state.capacities_calculated = False
    st.session_state.step = 2


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
    st.session_state.classification_data = {}
    st.session_state.braking_acceleration = 0.7


def validate_current_step_and_next():
    s = st.session_state
    errors = []

    if s.step == 0:
        if not s.generation_type:
            errors.append("Please select a generation.")
    elif s.step == 1:
        if not s.cabin_geometry:
            errors.append("Please select a cabin geometry.")
    elif s.step == 2:
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
    elif s.step == 5:
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

    if errors:
        s.validation_errors = errors
        for e in errors:
            st.error(e)
    else:
        s.validation_errors = []
        s.step = min(6, s.step + 1)


# --- UI ---
st.title("🎡 Ferris Wheel Designer")
total_steps = 7
st.progress(st.session_state.get('step', 0) / (total_steps - 1))
st.markdown(f"**Step {st.session_state.get('step', 0) + 1} of {total_steps}**")
st.markdown("---")

# Small helper to consistently render back/next controls at bottom of each step
def render_nav_buttons(back_enabled=True, next_enabled=True, back_key_suffix="", next_key_suffix=""):
    left_col, right_col = st.columns([1,1])
    with left_col:
        if back_enabled:
            st.button("⬅️ Back", on_click=go_back, key=f"back_btn{back_key_suffix}")
        else:
            st.button("⬅️ Back", disabled=True, key=f"back_btn_disabled{back_key_suffix}")
    with right_col:
        if next_enabled:
            st.button("Next ➡️", on_click=validate_current_step_and_next, key=f"next_btn{next_key_suffix}")
        else:
            st.button("Next ➡️", disabled=True, key=f"next_btn_disabled{next_key_suffix}")

# === STEP 0: Generation selection ===
if st.session_state.get('step', 0) == 0:
    st.header("Step 1: Select Ferris Wheel Generation")

    image_files = [
        "./git/assets/1st.jpg",
        "./git/assets/2nd_1.jpg",
        "./git/assets/2nd_2.jpg",
        "./git/assets/4th.jpg"
    ]
    captions = [
        "1st Generation (Truss type)",
        "2nd Generation (Cable type)",
        "2nd Generation (Pure cable type)",
        "4th Generation (Hubless centerless)"
    ]
    img_width = 180

    cols = st.columns(4, gap="small")
    for i, (col, img_path, caption) in enumerate(zip(cols, image_files, captions)):
        with col:
            try:
                st.image(img_path, width=img_width)
            except Exception:
                st.write(f"Image not found: {img_path}")
            st.caption(caption)
            st.button(f"Select\n{caption}", key=f"gen_btn_{i}", on_click=select_generation, args=(caption,))

    st.markdown("---")
    st.write("Just click the button under the image to select a generation. Or press Next to validate and proceed.")

    # show nav (Back disabled on first step)
    render_nav_buttons(back_enabled=False, next_enabled=True, next_key_suffix="_step0")

# === STEP 1: Cabin Geometry ===
elif st.session_state.step == 1:
    st.header("Step 2: Cabin Geometry Selection")
    st.markdown("Choose a cabin shape. (Click the image's button to select.)")

    geom_images = [
        ("Square", "./git/assets/square.jpg"),
        ("Vertical Cylinder", "./git/assets/vertical.jpg"),
        ("Horizontal Cylinder", "./git/assets/horizontal.jpg"),
        ("Spherical", "./git/assets/sphere.jpg")
    ]
    cols = st.columns(4, gap="small")
    for i, (label, img_path) in enumerate(geom_images):
        with cols[i]:
            try:
                st.image(img_path, use_column_width=True)
            except Exception:
                st.write(f"Image not found: {img_path}")
            st.caption(label)
            # use on_click helper to ensure selection logic is identical and step advances
            st.button(f"Select\n{label}", key=f"geom_img_btn_{i}", on_click=select_geometry_and_advance, args=(label,))

    st.markdown("---")
    render_nav_buttons(back_enabled=True, next_enabled=True, back_key_suffix="_step1", next_key_suffix="_step1")

# === STEP 2: Primary parameters + Cabin capacity + VIP ===
elif st.session_state.step == 2:
    st.header("Step 3: Primary Parameters, Cabin Capacity & VIP")
    st.subheader(f"Generation: {st.session_state.generation_type}")
    st.markdown("---")

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
    if st.button("🔄 Calculate Capacities", key="calc_caps_btn"):
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
    render_nav_buttons(back_enabled=True, next_enabled=True, back_key_suffix="_step2", next_key_suffix="_step2")

# === STEP 3: Rotation Time & Derived Speeds ===
elif st.session_state.step == 3:
    st.header("Step 4: Rotation Time & Derived Speeds")
    st.markdown("Enter rotation time (minutes per full rotation). Angular speed (rad/s), rotational speed (rpm) and linear speed (m/s) at rim are shown (read-only).")
    st.markdown("---")

    diameter = st.session_state.diameter
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

    st.text_input("Angular speed (rad/s)", value=f"{ang:.6f}", disabled=True, key="ang_display")
    st.text_input("Rotational speed (rpm)", value=f"{rpm:.6f}", disabled=True, key="rpm_display")
    st.text_input("Linear speed at rim (m/s)", value=f"{linear:.6f}", disabled=True, key="linear_display")

    cap_per_hour = calculate_capacity_per_hour_from_time(
        st.session_state.num_cabins,
        st.session_state.cabin_capacity,
        st.session_state.num_vip_cabins,
        rotation_time_min
    )
    st.metric("Estimated Capacity per Hour (assuming full occupancy)", f"{cap_per_hour:.0f} passengers/hour")

    st.markdown("---")
    render_nav_buttons(back_enabled=True, next_enabled=True, back_key_suffix="_step3", next_key_suffix="_step3")

# === STEP 4: Device Classification & Safety Analysis ===
elif st.session_state.step == 4:
    st.header("Step 5: Device Classification & Safety Analysis")
    st.markdown("Calculation per National Standard 8987")
    st.markdown("---")

    diameter = st.session_state.diameter
    height = diameter * 1.1
    rotation_time_min = st.session_state.rotation_time_min

    if rotation_time_min and rotation_time_min > 0:
        rotation_time_sec = rotation_time_min * 60.0
        angular_velocity = 2.0 * np.pi / rotation_time_sec
        rpm = angular_velocity * 60.0 / (2.0 * np.pi)
    else:
        angular_velocity = 0.0
        rpm = 0.0

    st.subheader("1. Braking Acceleration")
    st.markdown("Enter the design braking acceleration (tangential direction):")
    braking_accel = st.number_input(
        "Braking Acceleration (m/s²)",
        min_value=0.01,
        max_value=2.0,
        value=st.session_state.braking_acceleration,
        step=0.01,
        format="%.2f",
        key="braking_accel_input"
    )
    st.session_state.braking_acceleration = braking_accel

    st.markdown("---")
    st.subheader("2. Design Case Analysis")
    st.markdown("**Design parameters:** Speed = 1 rpm, Braking acceleration = 0.7 m/s²")

    omega_design = 1.0 * (2.0 * np.pi / 60.0)
    a_brake_design = 0.7

    p_design, n_design, max_accel_design = calculate_dynamic_product(diameter, height, omega_design, a_brake_design)
    class_design = classify_device(p_design, is_design=True)

    st.metric("Dynamic product (design)", f"{p_design:.2f}")
    st.metric("Max accel (design) [m/s²]", f"{max_accel_design:.2f}")
    st.metric("Classification (design)", f"Class {class_design}")

    st.markdown("---")
    st.subheader("3. Operating Case Analysis (current inputs)")
    p_oper, n_oper, max_accel_oper = calculate_dynamic_product(diameter, height, angular_velocity, braking_accel)
    class_oper = classify_device(p_oper, is_design=False)

    st.metric("Dynamic product (operating)", f"{p_oper:.2f}")
    st.metric("Max accel (operating) [m/s²]", f"{max_accel_oper:.2f}")
    st.metric("Classification (operating)", f"Class {class_oper}")

    fig_env = plot_acceleration_envelope(diameter, angular_velocity, braking_accel)
    st.plotly_chart(fig_env, use_container_width=True)

    st.markdown("---")
    render_nav_buttons(back_enabled=True, next_enabled=True, back_key_suffix="_step4", next_key_suffix="_step4")

# === STEP 5: Environment & Site Data ===
elif st.session_state.step == 5:
    st.header("Step 6: Environment & Site Data")
    st.markdown("Provide site and environmental inputs used for wind/loading checks.")
    st.markdown("---")

    env = st.session_state.environment_data
    province = st.selectbox("Province", ["", "Province A", "Province B"], index=0, key="province_select")
    env['province'] = province
    env['region_name'] = st.text_input("Region name", value=env.get('region_name', ''), key='region_name_input')
    env['land_length'] = st.number_input("Land length (m)", min_value=10, max_value=150, value=env.get('land_length', 50), key='land_length_input')
    env['land_width'] = st.number_input("Land width (m)", min_value=10, max_value=150, value=env.get('land_width', 50), key='land_width_input')
    env['altitude'] = st.number_input("Altitude (m)", value=env.get('altitude', 10), key='altitude_input')
    env['wind_max'] = st.number_input("Max wind (km/h)", value=env.get('wind_max', 50), key='wind_max_input')

    st.session_state.environment_data = env

    st.markdown("---")
    st.checkbox("Enable wind rose upload", key='wind_rose_toggle', value=st.session_state.wind_rose_loaded)
    if st.session_state.get('wind_rose_toggle'):
        uploaded = st.file_uploader("Upload wind rose (optional)", type=['png','jpg','csv'])
        if uploaded:
            st.session_state.wind_rose_file = uploaded
            st.session_state.wind_rose_loaded = True

    render_nav_buttons(back_enabled=True, next_enabled=True, back_key_suffix="_step5", next_key_suffix="_step5")

# === STEP 6: Final Summary & Export ===
elif st.session_state.step == 6:
    st.header("Step 7: Final Summary & Export")
    st.markdown("Review your configuration and export data.")
    st.markdown("---")

    st.json({
        'generation': st.session_state.generation_type,
        'geometry': st.session_state.cabin_geometry,
        'diameter': st.session_state.diameter,
        'num_cabins': st.session_state.num_cabins,
        'cabin_capacity': st.session_state.cabin_capacity,
        'num_vip': st.session_state.num_vip_cabins,
        'rotation_time_min': st.session_state.rotation_time_min,
        'environment': st.session_state.environment_data
    })

    c1, c2 = st.columns(2)
    with c1:
        st.button("Export JSON", key='export_json')
    with c2:
        st.button("Reset Design", on_click=reset_design, key='reset_design')

    # allow user to go back if they want to change something
    render_nav_buttons(back_enabled=True, next_enabled=False, back_key_suffix="_step6")


