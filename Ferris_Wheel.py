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
    st.session_state.step = 0  # 0: generation, 1: cabin geometry, 2: primary params, 3: rotation, 4: classification, 5: environment, 6: final
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
    # Unit vectors
    # U_n = -cos(theta)i - sin(theta)k (normal/centripetal direction)
    # U_t = -sin(theta)i + cos(theta)k (tangential direction)
    
    # Centripetal acceleration magnitude
    radius = diameter / 2.0
    a_centripetal = radius * (angular_velocity ** 2)
    
    # Acceleration components
    # a = -g(k) - (d/2 * w^2)(U_n) - a_brake(U_t)
    # Breaking into horizontal (x) and vertical (z) components
    
    # Gravity contribution: -g in k direction (vertical)
    a_z_gravity = -g
    a_x_gravity = 0
    
    # Centripetal contribution: -(d/2 * w^2) * U_n
    a_x_centripetal = -a_centripetal * (-np.cos(theta))  # = a_centripetal * cos(theta)
    a_z_centripetal = -a_centripetal * (-np.sin(theta))  # = a_centripetal * sin(theta)
    
    # Braking contribution: -a_brake * U_t
    a_x_braking = -braking_accel * (-np.sin(theta))  # = braking_accel * sin(theta)
    a_z_braking = -braking_accel * (np.cos(theta))   # = -braking_accel * cos(theta)
    
    # Total accelerations
    a_x_total = a_x_gravity + a_x_centripetal + a_x_braking
    a_z_total = a_z_gravity + a_z_centripetal + a_z_braking
    
    # Total magnitude
    a_total = np.sqrt(a_x_total**2 + a_z_total**2)
    
    return a_x_total, a_z_total, a_total

def calculate_dynamic_product(diameter, height, angular_velocity, braking_accel, g=9.81):
    """Calculate dynamic product p = v * h * n"""
    # Sample angles around the wheel
    theta_vals = np.linspace(0, 2*np.pi, 360)
    max_accel = 0
    
    for theta in theta_vals:
        _, _, a_total = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g)
        if a_total > max_accel:
            max_accel = a_total
    
    # v = d/2 * w (linear velocity at rim)
    v = (diameter / 2.0) * angular_velocity
    
    # n = max_acceleration / g
    n = max_accel / g
    
    # p = v * h * n
    p = v * height * n
    
    return p, n, max_accel

def classify_device(dynamic_product, is_design=True):
    """Classify device based on dynamic product"""
    if is_design:
        if 0.1 < dynamic_product <= 25:
            return 1
        elif 25 < dynamic_product <= 100:
            return 2
        elif 100 < dynamic_product <= 200:
            return 3
        else:  # p > 200
            return 4
    else:  # actual/real operation
        if 0.1 < dynamic_product <= 25:
            return 2
        elif 25 < dynamic_product <= 100:
            return 3
        elif 100 < dynamic_product <= 200:
            return 4
        else:  # p > 200
            return 5

def determine_restraint_area(ax, az):
    """Determine restraint area based on ax and az accelerations (in units of g)"""
    # Based on the diagram provided
    # Area boundaries (approximate from the image)
    
    # Area 1: ax > 0, az between -0.2 and +0.2
    if ax > 1.2 and -0.2 <= az <= 0.2:
        return 1
    
    # Area 2: Central region, ax between -0.2 and +0.2, az between -0.7 and +0.2
    if -0.2 <= ax <= 0.2 and -0.7 <= az <= 0.2:
        return 2
    
    # Area 3: ax < 0, az between -0.7 and +0.2
    if -1.2 <= ax < -0.2 and -0.7 <= az <= 0.2:
        return 3
    
    # Area 4: ax < -0.2, az between -1.8 and -0.7 (if no lateral forces and duration < 0.2s)
    if -1.2 <= ax and -1.8 <= az < -0.7:
        return 4
    
    # Area 5: Upper regions, az > 0.2
    if az > 0.2:
        return 5
    
    # Default to Area 2 (most restrictive in central region)
    return 2

def plot_acceleration_envelope(diameter, angular_velocity, braking_accel, g=9.81):
    """Plot the ax vs az acceleration envelope"""
    theta_vals = np.linspace(0, 2*np.pi, 360)
    ax_vals = []
    az_vals = []
    
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g)
        # Convert to g units
        ax_vals.append(a_x / g)
        az_vals.append(a_z / g)
    
    fig = go.Figure()
    
    # Plot acceleration envelope
    fig.add_trace(go.Scatter(
        x=ax_vals, 
        y=az_vals, 
        mode='lines',
        line=dict(color='#2196F3', width=3),
        name='Acceleration Envelope'
    ))
    
    # Add area boundaries (simplified representation)
    # Area 1 boundary
    fig.add_shape(type="rect", x0=1.2, y0=-0.2, x1=2.0, y1=0.2,
                  line=dict(color="red", width=2, dash="dash"), fillcolor="rgba(255,0,0,0.1)")
    
    # Area 2 boundary (central)
    fig.add_shape(type="rect", x0=-0.2, y0=-0.7, x1=0.2, y1=0.2,
                  line=dict(color="orange", width=2, dash="dash"), fillcolor="rgba(255,165,0,0.1)")
    
    # Area 3 boundary
    fig.add_shape(type="rect", x0=-1.2, y0=-0.7, x1=-0.2, y1=0.2,
                  line=dict(color="yellow", width=2, dash="dash"), fillcolor="rgba(255,255,0,0.1)")
    
    # Area 4 boundary
    fig.add_shape(type="rect", x0=-1.2, y0=-1.8, x1=0, y1=-0.7,
                  line=dict(color="green", width=2, dash="dash"), fillcolor="rgba(0,255,0,0.1)")
    
    # Area 5 boundary (upper)
    fig.add_shape(type="rect", x0=-2.0, y0=0.2, x1=2.0, y1=1.5,
                  line=dict(color="purple", width=2, dash="dash"), fillcolor="rgba(128,0,128,0.1)")
    
    fig.update_layout(
        title="Passenger Acceleration Envelope (ax vs az)",
        xaxis_title="Horizontal Acceleration ax [g]",
        yaxis_title="Vertical Acceleration az [g]",
        height=600,
        template="plotly_white",
        showlegend=True,
        xaxis=dict(range=[-2, 2], zeroline=True, zerolinewidth=2, zerolinecolor='black'),
        yaxis=dict(range=[-2, 1.5], zeroline=True, zerolinewidth=2, zerolinecolor='black')
    )
    
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
    st.session_state.classification_data = {}
    st.session_state.braking_acceleration = 0.7

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
        # classification step - no specific validation needed, calculations are automatic
        pass
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
    # show errors or advance
    if errors:
        st.session_state.validation_errors = errors
        for e in errors:
            st.error(e)
    else:
        st.session_state.validation_errors = []
        st.session_state.step = min(6, st.session_state.step + 1)

# --- UI ---
st.title("🎡 Ferris Wheel Designer")
total_steps = 7
st.progress(st.session_state.get('step', 0) / (total_steps - 1))
st.markdown(f"**Step {st.session_state.get('step', 0) + 1} of {total_steps}**")
st.markdown("---")

# --- moved header: show Step 1 header only here, directly under the main title ---
if st.session_state.get('step', 0) == 0:
    st.header("Step 1: Select Ferris Wheel Generation")

# === STEP 0: Generation selection (images + buttons under each image for single-click) ===
if st.session_state.get('step', 0) == 0:
    # show images with captions and a button under each - single-click will select even the first one
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
            # button under each image to select that generation (single click)
            st.button(f"Select\n{caption}", key=f"gen_btn_{i}", on_click=select_generation, args=(caption,))

    st.markdown("---")
    st.write("Just click the button under the image to select a generation and go to the next step.")


# === STEP 1: Cabin Geometry (now also shows the 4 new images you requested) ===
elif st.session_state.step == 1:
    st.header("Step 2: Cabin Geometry Selection")
    st.markdown("Choose a cabin shape. (Click the image's button to select.)")
    # display images you asked for: horizontal.jpg, sphere.jpg, square.jpg, vertical.jpg
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
            # unique keys for these buttons (avoid collisions with previous keys)
            if st.button(f"Select\n{label}", key=f"geom_img_btn_{i}"):
                st.session_state.cabin_geometry = label if label != "Spherical" else "Spherical"
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

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        # If user wants to skip selection and go next (not recommended), validate will catch missing geometry
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

# === STEP 4: Device Classification & Safety Analysis (NEW) ===
elif st.session_state.step == 4:
    st.header("Step 5: Device Classification & Safety Analysis")
    st.markdown("Calculation per National Standard 8987")
    st.markdown("---")

    diameter = st.session_state.diameter
    height = diameter * 1.1  # Height of ferris wheel
    rotation_time_min = st.session_state.rotation_time_min
    
    # Convert rotation time to angular velocity (rad/s)
    if rotation_time_min and rotation_time_min > 0:
        rotation_time_sec = rotation_time_min * 60.0
        angular_velocity = 2.0 * np.pi / rotation_time_sec  # rad/s
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
    
    # Design case: 1 rpm, 0.7 m/s² braking
    omega_design = 1.0 * (2.0 * np.pi / 60.0)  # 1 rpm to rad/s
    a_brake_design = 0.7

