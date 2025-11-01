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
    st.session_state.step = 0  # 0: generation, 1: cabin geometry, 2: primary params, 3: rotation, 4: environment, 5: device classification, 6: restraint type, 7: final
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
    fig.add_annotation(x=1.6, y=0, text="Area 1", showarrow=False, font=dict(size=10, color="red"))
    
    # Area 2 boundary (central)
    fig.add_shape(type="rect", x0=-0.2, y0=-0.7, x1=0.2, y1=0.2,
                  line=dict(color="orange", width=2, dash="dash"), fillcolor="rgba(255,165,0,0.1)")
    fig.add_annotation(x=0, y=-0.25, text="Area 2", showarrow=False, font=dict(size=10, color="orange"))
    
    # Area 3 boundary
    fig.add_shape(type="rect", x0=-1.2, y0=-0.7, x1=-0.2, y1=0.2,
                  line=dict(color="yellow", width=2, dash="dash"), fillcolor="rgba(255,255,0,0.1)")
    fig.add_annotation(x=-0.7, y=-0.25, text="Area 3", showarrow=False, font=dict(size=10, color="olive"))
    
    # Area 4 boundary
    fig.add_shape(type="rect", x0=-1.2, y0=-1.8, x1=0, y1=-0.7,
                  line=dict(color="green", width=2, dash="dash"), fillcolor="rgba(0,255,0,0.1)")
    fig.add_annotation(x=-0.6, y=-1.25, text="Area 4", showarrow=False, font=dict(size=10, color="green"))
    
    # Area 5 boundary (upper)
    fig.add_shape(type="rect", x0=-2.0, y0=0.2, x1=2.0, y1=1.5,
                  line=dict(color="purple", width=2, dash="dash"), fillcolor="rgba(128,0,128,0.1)")
    fig.add_annotation(x=0, y=0.85, text="Area 5", showarrow=False, font=dict(size=10, color="purple"))
    
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
    elif s.step == 5:
        # Device classification step - no validation needed, calculations are automatic
        pass
    elif s.step == 6:
        # Restraint type step - no validation needed, calculations are automatic
        pass
    # show errors or advance
    if errors:
        st.session_state.validation_errors = errors
        for e in errors:
            st.error(e)
    else:
        st.session_state.validation_errors = []
        st.session_state.step = min(7, st.session_state.step + 1)

# --- UI ---
st.title("🎡 Ferris Wheel Designer")
total_steps = 8
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

# === STEP 5: Device Classification (NEW PAGE 1) ===
elif st.session_state.step == 5:
    st.header("Step 6: Device Classification")
    st.markdown("**Calculation per National Standard 8987**")
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
    
    st.subheader("Braking Acceleration Parameter")
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
    st.subheader("Design Case Analysis")
    st.markdown("**Design parameters:** Speed = 1 rpm, Braking acceleration = 0.7 m/s²")
    
    # Design case: 1 rpm, 0.7 m/s² braking
    omega_design = 1.0 * (2.0 * np.pi / 60.0)  # 1 rpm to rad/s
    a_brake_design = 0.7
    
    p_design, n_design, max_accel_design = calculate_dynamic_product(
        diameter, height, omega_design, a_brake_design
    )
    class_design = classify_device(p_design, is_design=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Max Acceleration", f"{max_accel_design:.3f} m/s²")
        st.caption(f"({n_design:.3f}g)")
    with col2:
        st.metric("Dynamic Product (p)", f"{p_design:.2f}")
    with col3:
        st.metric("Device Class (Design)", f"Class {class_design}")
    
    st.markdown("---")
    st.subheader("Actual Operation Analysis")
    st.markdown(f"**Actual parameters:** Speed = {rpm:.4f} rpm, Braking acceleration = {braking_accel} m/s²")
    
    # Actual case: current design speed and braking
    p_actual, n_actual, max_accel_actual = calculate_dynamic_product(
        diameter, height, angular_velocity, braking_accel
    )
    class_actual = classify_device(p_actual, is_design=False)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Max Acceleration", f"{max_accel_actual:.3f} m/s²")
        st.caption(f"({n_actual:.3f}g)")
    with col2:
        st.metric("Dynamic Product (p)", f"{p_actual:.2f}")
    with col3:
        st.metric("Device Class (Actual)", f"Class {class_actual}")
    
    st.markdown("---")
    st.info("**Classification Ranges:**\n- Design: Class 1 (0.1<p≤25), Class 2 (25<p≤100), Class 3 (100<p≤200), Class 4 (p>200)\n- Actual: Class 2 (0.1<p≤25), Class 3 (25<p≤100), Class 4 (100<p≤200), Class 5 (p>200)")
    
    # Store classification data
    st.session_state.classification_data = {
        'p_design': p_design,
        'class_design': class_design,
        'max_accel_design': max_accel_design,
        'n_design': n_design,
        'p_actual': p_actual,
        'class_actual': class_actual,
        'max_accel_actual': max_accel_actual,
        'n_actual': n_actual
    }
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 6: Restraint Type Selection (NEW PAGE 2) ===
elif st.session_state.step == 6:
    st.header("Step 7: Restraint Type Determination")
    st.markdown("**Based on acceleration analysis per National Standard 8987**")
    st.markdown("---")

    diameter = st.session_state.diameter
    rotation_time_min = st.session_state.rotation_time_min
    braking_accel = st.session_state.braking_acceleration
    
    # Convert rotation time to angular velocity
    if rotation_time_min and rotation_time_min > 0:
        rotation_time_sec = rotation_time_min * 60.0
        angular_velocity = 2.0 * np.pi / rotation_time_sec
    else:
        angular_velocity = 0.0
    
    st.subheader("Passenger Acceleration Analysis")
    st.markdown("Acceleration components in horizontal (ax) and vertical (az) directions:")
    
    # Calculate max ax and az values across all angles
    theta_vals = np.linspace(0, 2*np.pi, 360)
    max_ax = -float('inf')
    max_az = -float('inf')
    restraint_areas = []
    
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(
            theta, diameter, angular_velocity, braking_accel
        )
        a_x_g = a_x / 9.81
        a_z_g = a_z / 9.81
        
        if abs(a_x_g) > abs(max_ax):
            max_ax = a_x_g
        if abs(a_z_g) > abs(max_az):
            max_az = a_z_g
        
        area = determine_restraint_area(a_x_g, a_z_g)
        restraint_areas.append(area)
    
    # Determine predominant restraint area
    from collections import Counter
    area_counts = Counter(restraint_areas)
    predominant_area = area_counts.most_common(1)[0][0]
    
    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Max Horizontal Accel (ax)", f"{max_ax:.3f}g")
    with col2:
        st.metric("Max Vertical Accel (az)", f"{max_az:.3f}g")
    with col3:
        st.metric("Restraint Area", f"Area {predominant_area}")
    
    # Restraint type descriptions
    restraint_descriptions = {
        1: "Minimal restraint - Seat belt may be sufficient",
        2: "Standard restraint - Lap bar or seat belt required",
        3: "Enhanced restraint - Over-shoulder restraint recommended",
        4: "Special consideration - Harness system may be needed (if no lateral forces & duration < 0.2s)",
        5: "Maximum restraint - Full body harness required"
    }
    
    st.success(f"**Recommended Restraint Type:** {restraint_descriptions.get(predominant_area, 'Standard restraint')}")
    
    # Plot acceleration envelope
    st.markdown("---")
    st.subheader("Acceleration Envelope Diagram")
    fig_accel = plot_acceleration_envelope(diameter, angular_velocity, braking_accel)
    st.plotly_chart(fig_accel, use_container_width=True)
    
    st.markdown("""
    **Area Classifications:**
    - **Area 1** (Red): Right side, minimal vertical acceleration - Minimal restraint
    - **Area 2** (Orange): Central zone - Standard restraint (lap bar/seat belt)
    - **Area 3** (Yellow): Left side, backward acceleration - Enhanced restraint
    - **Area 4** (Green): Downward acceleration zone - Special consideration (harness if needed)
    - **Area 5** (Purple): Upward acceleration zone - Maximum restraint (full body harness)
    """)
    
    # Update classification data with restraint info
    st.session_state.classification_data.update({
        'restraint_area': predominant_area,
        'max_ax_g': max_ax,
        'max_az_g': max_az,
        'restraint_description': restraint_descriptions.get(predominant_area, 'Standard restraint')
    })
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 7: Final Design Overview & Visualization ===
elif st.session_state.step == 7:
    st.header("Step 8: Design Overview & Visualization")
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
    
    # Classification data
    if st.session_state.classification_data:
        st.markdown("**Safety Classification (NS 8987):**")
        class_data = st.session_state.classification_data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"• Design Class: {class_data.get('class_design','N/A')}")
            st.write(f"• Design Dynamic Product: {class_data.get('p_design',0):.2f}")
            st.write(f"• Design Max Accel: {class_data.get('n_design',0):.3f}g")
        with col2:
            st.write(f"• Actual Class: {class_data.get('class_actual','N/A')}")
            st.write(f"• Actual Dynamic Product: {class_data.get('p_actual',0):.2f}")
            st.write(f"• Actual Max Accel: {class_data.get('n_actual',0):.3f}g")
        with col3:
            st.write(f"• Restraint Area: Area {class_data.get('restraint_area','N/A')}")
            st.write(f"• Max Horizontal: {class_data.get('max_ax_g',0):.3f}g")
            st.write(f"• Max Vertical: {class_data.get('max_az_g',0):.3f}g")
        
        st.info(f"**Restraint Type:** {class_data.get('restraint_description', 'N/A')}")

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
