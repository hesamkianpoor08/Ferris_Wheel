# full_streamlit_ferris_designer_v2.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from collections import Counter

# --- Page Configuration ---
st.set_page_config(
    page_title="Ferris Wheel Designer",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Session State Initialization ---
if 'step' not in st.session_state:
    st.session_state.step = 0
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
if 'soil_type' not in st.session_state:
    st.session_state.soil_type = None
if 'importance_group' not in st.session_state:
    st.session_state.importance_group = None
if 'carousel_orientation' not in st.session_state:
    st.session_state.carousel_orientation = None
if 'orientation_confirmed' not in st.session_state:
    st.session_state.orientation_confirmed = False

# --- Province Data ---
TERRAIN_CATEGORIES = {
    "Gilan": {"category": "0", "z0": 0.003, "zmin": 1, "desc": "Sea or coastal area exposed to the open sea"},
    "Mazandaran": {"category": "0", "z0": 0.003, "zmin": 1, "desc": "Sea or coastal area exposed to the open sea"},
    "Golestan": {"category": "0", "z0": 0.003, "zmin": 1, "desc": "Sea or coastal area exposed to the open sea"},
    "Bushehr": {"category": "0", "z0": 0.003, "zmin": 1, "desc": "Sea or coastal area exposed to the open sea"},
    "Hormozgan": {"category": "0", "z0": 0.003, "zmin": 1, "desc": "Sea or coastal area exposed to the open sea"},
    "Khuzestan": {"category": "0", "z0": 0.003, "zmin": 1, "desc": "Sea or coastal area exposed to the open sea"},
    "Sistan and Baluchestan": {"category": "0", "z0": 0.003, "zmin": 1, "desc": "Sea or coastal area exposed to the open sea (coastal parts)"},
    "Yazd": {"category": "I", "z0": 0.01, "zmin": 1, "desc": "Flat or desert area with negligible vegetation"},
    "Semnan": {"category": "I", "z0": 0.01, "zmin": 1, "desc": "Flat or desert area with negligible vegetation"},
    "Qom": {"category": "I", "z0": 0.01, "zmin": 1, "desc": "Flat or desert area with negligible vegetation"},
    "South Khorasan": {"category": "I", "z0": 0.01, "zmin": 1, "desc": "Flat or desert area with negligible vegetation"},
    "Kerman": {"category": "I", "z0": 0.01, "zmin": 1, "desc": "Flat or desert area with negligible vegetation"},
    "Qazvin": {"category": "II", "z0": 0.05, "zmin": 2, "desc": "Low vegetation, scattered trees or buildings"},
    "Zanjan": {"category": "II", "z0": 0.05, "zmin": 2, "desc": "Low vegetation, scattered trees or buildings"},
    "Hamedan": {"category": "II", "z0": 0.05, "zmin": 2, "desc": "Low vegetation, scattered trees or buildings"},
    "Markazi": {"category": "II", "z0": 0.05, "zmin": 2, "desc": "Low vegetation, scattered trees or buildings"},
    "North Khorasan": {"category": "II", "z0": 0.05, "zmin": 2, "desc": "Low vegetation, scattered trees or buildings"},
    "Khorasan Razavi": {"category": "II", "z0": 0.05, "zmin": 2, "desc": "Semi-arid plains, mixed low vegetation"},
    "East Azerbaijan": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "West Azerbaijan": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Ardabil": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Kurdistan": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Kermanshah": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Ilam": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Lorestan": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Chaharmahal and Bakhtiari": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Kohgiluyeh and Boyer-Ahmad": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Fars": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Isfahan": {"category": "III", "z0": 0.3, "zmin": 5, "desc": "Regular vegetation or rural/forested terrain"},
    "Tehran": {"category": "IV", "z0": 1.0, "zmin": 10, "desc": "Densely built-up urban area"},
    "Alborz": {"category": "IV", "z0": 1.0, "zmin": 10, "desc": "Densely built-up urban area"}
}

SEISMIC_HAZARD = {
    "Very High": ["Tehran", "Alborz", "Kermanshah", "Kohgiluyeh and Boyer-Ahmad", "Lorestan", "West Azerbaijan", "East Azerbaijan", "Fars", "Hormozgan"],
    "High": ["Kurdistan", "Ilam", "Chaharmahal and Bakhtiari", "Bushehr", "Mazandaran", "Gilan", "Khorasan Razavi", "South Khorasan"],
    "Moderate": ["Qazvin", "Zanjan", "Semnan", "Markazi", "Isfahan", "Kerman"],
    "Low": ["Qom", "Yazd", "Khuzestan", "Golestan", "North Khorasan", "Sistan and Baluchestan"]
}
# reverse mapping
SEISMIC_BY_PROVINCE = {}
for k, lst in SEISMIC_HAZARD.items():
    for p in lst:
        SEISMIC_BY_PROVINCE[p] = k

# --- Helper functions ---
def base_for_geometry(diameter, geometry):
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
        ang = 2.0 * np.pi / sec
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

# --- IMPORTANT: az positive = downward ---
def calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g=9.81):
    """
    Returns (a_x, a_z, a_total) in m/s^2
    Convention:
      - x positive to right
      - z positive downward (gravity -> +g)
      - theta measured around wheel (0 at +x)
    """
    radius = diameter / 2.0
    a_centripetal = radius * (angular_velocity ** 2)

    # gravity contribution: +g in downward (z positive)
    a_z_gravity = +g
    a_x_gravity = 0.0

    # Centripetal contribution: -(a_centripetal) * U_n
    # U_n = -cos(theta) i - sin(theta) k
    # a_x_centripetal = a_centripetal * cos(theta)
    a_x_centripetal = a_centripetal * np.cos(theta)
    # a_z_centripetal = a_centripetal * np.sin(theta)
    a_z_centripetal = a_centripetal * np.sin(theta)

    # Braking contribution: -a_brake * U_t
    # U_t = -sin(theta) i + cos(theta) k
    a_x_braking = braking_accel * np.sin(theta)
    a_z_braking = -braking_accel * np.cos(theta)

    a_x_total = a_x_gravity + a_x_centripetal + a_x_braking
    a_z_total = a_z_gravity + a_z_centripetal + a_z_braking

    a_total = np.sqrt(a_x_total**2 + a_z_total**2)
    return a_x_total, a_z_total, a_total

def calculate_dynamic_product(diameter, height, angular_velocity, braking_accel, g=9.81):
    theta_vals = np.linspace(0, 2*np.pi, 360)
    max_accel = 0.0
    for theta in theta_vals:
        _, _, a_total = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g)
        if a_total > max_accel:
            max_accel = a_total
    v = (diameter / 2.0) * angular_velocity
    n = max_accel / g
    p = v * height * n
    return p, n, max_accel

def classify_device(dynamic_product):
    if 0.1 < dynamic_product <= 25:
        return 2
    elif 25 < dynamic_product <= 100:
        return 3
    elif 100 < dynamic_product <= 200:
        return 4
    elif dynamic_product > 200:
        return 5
    else:
        return None

# ---------------------------
# Determination: AS standard
# ---------------------------
def determine_restraint_area_as(ax, az):
    """AS zones (ax,az in g), based on user's zone definitions (interpreted).
       az positive = downward.
       Returns zone int (1..5) according to user's 'Zone' labels.
    """
    m = -0.2 / 0.7

    # Zone 5 (top/upper/left/wedge)
    if ax < -1.8:
        return 5
    if ax <= 0 and az <= 0:
        return 5
    if ax >= 0.7 and az <= -0.2:
        return 5
    if 0 < ax < 0.7 and az < (m * ax):
        return 5

    # Zone 4 (left-down/bands)
    # interpret "for -0.7<ax<0 -> 0<az < (-0.2/0.7) *ax"
    if -0.7 < ax < 0 and 0 < az < (m * ax):
        return 4
    # -1.2 < ax <= -0.7 and 0 < az < 0.2
    if -1.2 < ax <= -0.7 and 0 < az < 0.2:
        return 4
    # -1.8 < ax <= -1.2 and az > 0
    if -1.8 < ax <= -1.2 and az > 0:
        return 4

    # Zone 3
    if -0.7 < ax < 0.7 and az > (m * ax):
        return 3
    if ax > 0.7 and -0.2 < az < 0.2:
        return 3
    if -1.2 < ax <= -0.7 and az > 0.2:
        return 3

    # Zone 2: interpret as central-down region (fallback)
    # (user's text had ambiguities; using a reasonable interpretation:)
    # put central-right-down candidates here
    if -0.2 <= ax <= 0.2 and az > 0.2:
        return 2

    # Region 1 (user said "Region 1: ax > 0.2 -> az>0.2")
    if ax > 0.2 and az > 0.2:
        return 1

    # fallback: Zone 3
    return 3

# ---------------------------
# Determination: ISO standard
# ---------------------------
def determine_restraint_area_iso(ax, az):
    """ISO district mapping from user equations (ax,az in g). az positive down."""
    # District 1:
    if ax > 0.2 and az > 0.2:
        return 1
    if 0 < ax < 0.2 and az > 0.7:
        return 1
    if -0.2 < ax < 0 and az > (-1.5 * ax + 0.7):
        return 1

    # District 2:
    if 0 < ax < 0.2 and 0.2 < az < 0.7:
        return 2
    if -0.2 < ax < 0 and 0.2 < az < (-1.5 * ax + 0.7):
        return 2
    if -0.7 < ax < -0.2 and az > 0.2:
        return 2

    # District 3:
    if -1.2 < ax < -0.7 and az > 0.2:
        return 3
    if -0.7 < ax < 0 and az > ((-0.2 / 0.7) * ax):
        return 3
    if ax > 0 and 0 < az < 0.2:
        return 3

    # District 4:
    if -0.7 < ax < 0 and 0 < az < ((-0.2 / 0.7) * ax):
        return 4
    if -1.2 < ax < -0.7 and 0 < az < 0.2:
        return 4
    if -1.8 < ax < -1.2 and az > 0:
        return 4
    if 0 < ax < 0.7 and ((-0.2 / 0.7) * ax) < az < 0:
        return 4
    if ax > 0.7 and -0.2 < az < 0:
        return 4

    # District 5:
    if ax > 0.7 and az < -0.2:
        return 5
    if 0 < ax < 0.7 and az < ((-0.2 / 0.7) * ax):
        return 5
    if ax < 0 and az < 0:
        return 5
    if ax < -1.8:
        return 5

    # default
    return 3

# ---------------------------
# Plotting functions for AS and ISO zones
# ---------------------------
def plot_acceleration_envelope_iso(diameter, angular_velocity, braking_accel, g=9.81):
    # (reuse user's prior iso plotting, slightly adapted to az positive down)
    theta_vals = np.linspace(0, 2*np.pi, 360)
    ax_vals = []
    az_vals = []
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g)
        ax_vals.append(a_x / g)
        az_vals.append(a_z / g)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ax_vals, y=az_vals, mode='markers', marker=dict(color='#2196F3', size=4), name='Accel points'))

    # draw some representative ISO region polygons (approximate, per user equations)
    m = -0.2/0.7

    # District 1 polygon (approx)
    x_d1 = [0.2, 2.0, 2.0, 0.2, 0, -0.2]
    y_d1 = [0.2, 0.2, 2.0, 2.0, 0.7, 0.7]
    fig.add_trace(go.Scatter(x=x_d1, y=y_d1, fill='toself', fillcolor='rgba(128,0,128,0.15)', line=dict(color='purple', width=1), name='ISO 1'))

    # District 2 polygon (approx)
    x_d2 = [-0.7, -0.2] + list(np.linspace(-0.2, 0, 20)) + list(np.linspace(0, 0.2, 20)) + [0.2]
    y_d2 = [0.2, 0.2] + list((-1.5 * np.linspace(-0.2,0,20) + 0.7)) + list(0.2*np.ones(20)) + [0.2]
    fig.add_trace(go.Scatter(x=x_d2, y=y_d2, fill='toself', fillcolor='rgba(255,165,0,0.12)', line=dict(color='orange', width=1), name='ISO 2'))

    # District 3/4/5 shapes are sketched similar to earlier code (omitted details for brevity)
    # (We keep the visual to show comparison; the main classification uses determine_restraint_area_iso)

    fig.update_layout(title="ISO Acceleration Envelope (ax vs az) — az positive down",
                      xaxis_title="ax [g]",
                      yaxis_title="az [g]",
                      height=600,
                      xaxis=dict(range=[-2.2,2.2]),
                      yaxis=dict(range=[-2.2,2.2]),
                      template="plotly_white")
    return fig

def plot_acceleration_envelope_as(diameter, angular_velocity, braking_accel, g=9.81):
    theta_vals = np.linspace(0, 2*np.pi, 360)
    ax_vals = []
    az_vals = []
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g)
        ax_vals.append(a_x / g)
        az_vals.append(a_z / g)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ax_vals, y=az_vals, mode='markers', marker=dict(color='#2196F3', size=4), name='Accel points'))

    m = -0.2/0.7
    # Visual zone sketches per AS definitions (approx)
    # Zone 5: left/up wedge and right-top wedge and wedge under sloped line for 0<ax<0.7
    fig.add_shape(type="rect", x0=-2.2, x1=0.0, y0=-2.2, y1=0.0, fillcolor="rgba(255,0,0,0.10)", line=dict(color='red', width=1))
    fig.add_shape(type="rect", x0=0.7, x1=2.2, y0=-2.2, y1=-0.2, fillcolor="rgba(255,0,0,0.10)", line=dict(color='red', width=1))
    xs = np.linspace(0,0.7,30); ys = m*xs
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='red', dash='dash'), showlegend=False))

    # Zone 4: left-lower wedge
    xs = np.linspace(-0.7,0,40); ys_top = m*xs; ys_bottom = np.zeros_like(xs)
    fig.add_trace(go.Scatter(x=np.concatenate([xs, xs[::-1]]), y=np.concatenate([ys_bottom, ys_top[::-1]]), fill='toself', fillcolor='rgba(0,200,0,0.10)', line=dict(color='green',width=1), name='AS 4'))

    # Zone 3: central band between sloped line and az=0.2
    xs = np.linspace(-0.7,0.7,200)
    ys_lower = m*xs; ys_upper = np.full_like(xs, 0.2)
    fig.add_trace(go.Scatter(x=np.concatenate([xs, xs[::-1]]), y=np.concatenate([ys_lower, ys_upper[::-1]]), fill='toself', fillcolor='rgba(255,255,0,0.10)', line=dict(color='gold',width=1), name='AS 3'))

    # Zone 1 / 2 rectangles on right lower
    fig.add_shape(type="rect", x0=0.2, x1=2.2, y0=0.2, y1=2.2, fillcolor="rgba(255,165,0,0.12)", line=dict(color='orange', width=1))  # Region claimed as 1/2 overlap
    fig.add_shape(type="rect", x0=0.7, x1=2.2, y0=-0.2, y1=0.2, fillcolor="rgba(200,200,200,0.06)", line=dict(color='black', width=1))

    fig.update_layout(title="AS-style Acceleration Envelope (ax vs az) — az positive down",
                      xaxis_title="ax [g]",
                      yaxis_title="az [g]",
                      height=600,
                      xaxis=dict(range=[-2.2,2.2]),
                      yaxis=dict(range=[-2.2,2.2]),
                      template="plotly_white")
    return fig

# ---------------------------
# Navigation & validation
# ---------------------------
def select_generation(gen):
    st.session_state.generation_type = gen
    st.session_state.step = 1

def go_back():
    st.session_state.step = max(0, st.session_state.step - 1)

def reset_design():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

def validate_current_step_and_next():
    s = st.session_state
    errors = []

    # step indexing:
    # 0: generation, 1: cabin geometry, 2: primary params, 3: rotation time
    # 4: provincial characteristics (new), 5: environment conditions
    # 6: soil & importance (auto), 7: orientation, 8: device classification (NS8987)
    # 9: restraint both ISO & AS page, 10: final

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
    elif s.step == 4:
        # require that provincial characteristics were calculated (z0 present)
        if 'terrain_z0' not in s.environment_data:
            errors.append("Please calculate provincial characteristics (Compute z₀) before proceeding.")
    elif s.step == 5:
        env = s.environment_data
        if not env.get('province'):
            errors.append("Select a province (go back to Provincial Characteristics).")
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
    elif s.step == 6:
        if not s.soil_type:
            errors.append("Please select a soil type.")
        # importance is auto computed - no user input required
    elif s.step == 7:
        if not s.orientation_confirmed:
            errors.append("Please confirm the carousel orientation or select a custom direction.")
    # other steps no special validation

    if errors:
        st.session_state.validation_errors = errors
        for e in errors:
            st.error(e)
    else:
        st.session_state.validation_errors = []
        st.session_state.step = min(10, st.session_state.step + 1)

# ---------------------------
# UI
# ---------------------------
st.title("🎡 Ferris Wheel Designer")
total_steps = 11
st.progress(st.session_state.get('step', 0) / (total_steps - 1))
st.markdown(f"**Step {st.session_state.get('step', 0) + 1} of {total_steps}**")
st.markdown("---")

# Step 0: generation
if st.session_state.step == 0:
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
    cols = st.columns(4, gap="small")
    for i, (col, img_path, caption) in enumerate(zip(cols, image_files, captions)):
        with col:
            try:
                st.image(img_path, width=180)
            except Exception:
                st.write(f"Image not found: {img_path}")
            st.caption(caption)
            st.button(f"Select\n{caption}", key=f"gen_btn_{i}", on_click=select_generation, args=(caption,))
    st.markdown("---")
    st.write("Click the button under the image to select a generation and proceed.")

# Step 1: cabin geometry
elif st.session_state.step == 1:
    st.header("Step 2: Cabin Geometry Selection")
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
            if st.button(f"Select\n{label}", key=f"geom_img_btn_{i}"):
                st.session_state.cabin_geometry = label
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

# Step 2: primary params
elif st.session_state.step == 2:
    st.header("Step 3: Primary Parameters, Cabin Capacity & VIP")
    st.subheader(f"Generation: {st.session_state.generation_type}")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        diameter = st.number_input("Ferris Wheel Diameter (m)", min_value=30, max_value=80, value=int(st.session_state.diameter), step=1, key="diameter_input")
        st.session_state.diameter = diameter

    geometry = st.session_state.cabin_geometry
    base = base_for_geometry(diameter, geometry) if geometry else (np.pi * diameter / 4.0)
    min_c, max_c = calc_min_max_from_base(base)

    num_cabins = st.number_input("Number of Cabins", min_value=min_c, max_value=max_c, value=min(max(int(st.session_state.num_cabins), min_c), max_c), step=1, key="num_cabins_input")
    st.session_state.num_cabins = num_cabins

    c1, c2 = st.columns(2)
    with c1:
        cabin_capacity = st.number_input("Cabin Capacity (passengers per cabin)", min_value=4, max_value=8, value=st.session_state.cabin_capacity, step=1, key="cabin_capacity_input")
        st.session_state.cabin_capacity = cabin_capacity
    with c2:
        num_vip = st.number_input("Number of VIP Cabins", min_value=0, max_value=st.session_state.num_cabins, value=min(st.session_state.num_vip_cabins, st.session_state.num_cabins), step=1, key="num_vip_input")
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

# Step 3: rotation time
elif st.session_state.step == 3:
    st.header("Step 4: Rotation Time & Derived Speeds")
    st.markdown("---")

    diameter = st.session_state.diameter
    circumference = np.pi * diameter
    default_rotation_time_min = (circumference / 0.2) / 60.0 if diameter > 0 else 1.0

    rotation_time_min = st.number_input("Rotation time (minutes per full rotation)", min_value=0.01, max_value=60.0, value=st.session_state.rotation_time_min if st.session_state.rotation_time_min else float(default_rotation_time_min), step=0.01, format="%.2f", key="rotation_time_input")
    st.session_state.rotation_time_min = rotation_time_min

    ang, rpm, linear = calc_ang_rpm_linear_from_rotation_time(rotation_time_min, diameter)
    st.text_input("Angular speed (rad/s)", value=f"{ang:.6f}", disabled=True)
    st.text_input("Rotational speed (rpm)", value=f"{rpm:.6f}", disabled=True)
    st.text_input("Linear speed at rim (m/s)", value=f"{linear:.6f}", disabled=True)

    cap_per_hour = calculate_capacity_per_hour_from_time(st.session_state.num_cabins, st.session_state.cabin_capacity, st.session_state.num_vip_cabins, rotation_time_min)
    st.metric("Estimated Capacity per Hour", f"{cap_per_hour:.0f} passengers/hour")

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# Step 4: Provincial Characteristics (NEW page)
elif st.session_state.step == 4:
    st.header("Step 5: Provincial Characteristics")
    st.markdown("Select province and compute terrain parameters (z₀, z_min, category). Click **Compute z₀** to store results.")
    provinces = list(TERRAIN_CATEGORIES.keys())
    province = st.selectbox("Province", options=provinces, index=0, key="prov_select_step4")

    if st.button("🔢 Compute z₀ and Terrain Info"):
        terrain = TERRAIN_CATEGORIES.get(province)
        seismic = SEISMIC_BY_PROVINCE.get(province, "Unknown")
        # save only terrain items now
        st.session_state.environment_data.update({
            'province': province,
            'terrain_category': terrain['category'],
            'terrain_z0': terrain['z0'],
            'terrain_zmin': terrain['zmin'],
            'terrain_desc': terrain['desc'],
            'seismic_hazard': seismic
        })
        st.success(f"Computed z₀ = {terrain['z0']} m, terrain category {terrain['category']}. Seismic: {seismic}")

    st.markdown("---")
    st.write("You can go Next once z₀ has been computed.")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# Step 5: Environment Conditions (uses stored provincial info)
elif st.session_state.step == 5:
    st.header("Step 6: Environment Conditions")
    st.markdown("---")
    env = st.session_state.environment_data or {}
    province = env.get('province', None)
    iran_provinces = list(TERRAIN_CATEGORIES.keys())

    c1, c2 = st.columns(2)
    with c1:
        # if province exists preselect it, else choose default
        province = st.selectbox("Province", options=iran_provinces, index=iran_provinces.index(province) if province in iran_provinces else 0, key="env_province_select")
    with c2:
        region_name = st.text_input("Region / Area name", value=st.session_state.environment_data.get('region_name',''), key="env_region_name")

    # if user changed province here, update terrain info (so it's consistent)
    if province in TERRAIN_CATEGORIES:
        terrain = TERRAIN_CATEGORIES[province]
        seismic = SEISMIC_BY_PROVINCE.get(province, "Unknown")
        st.session_state.environment_data.update({
            'province': province,
            'terrain_category': terrain['category'],
            'terrain_z0': terrain['z0'],
            'terrain_zmin': terrain['zmin'],
            'terrain_desc': terrain['desc'],
            'seismic_hazard': seismic
        })
    st.markdown("---")
    st.subheader("Land Surface Area (meters)")
    l1, l2 = st.columns(2)
    with l1:
        land_length = st.number_input("Land Length (m)", min_value=10.0, max_value=150.0, value=st.session_state.environment_data.get('land_length', 100.0), key="env_land_length")
    with l2:
        land_width = st.number_input("Land Width (m)", min_value=10.0, max_value=150.0, value=st.session_state.environment_data.get('land_width', 100.0), key="env_land_width")
    st.metric("Total Land Area", f"{land_length * land_width:.2f} m²")

    st.markdown("---")
    st.subheader("Altitude and Temperature")
    a1, a2 = st.columns(2)
    with a1:
        altitude = st.number_input("Altitude (m)", value=st.session_state.environment_data.get('altitude', 0.0), key="env_altitude")
    with a2:
        temp_min = st.number_input("Minimum Temperature (°C)", value=st.session_state.environment_data.get('temp_min', -10.0), key="env_temp_min")
    temp_max = st.number_input("Maximum Temperature (°C)", value=st.session_state.environment_data.get('temp_max', 40.0), key="env_temp_max")

    st.markdown("---")
    st.subheader("Wind Information")
    w1, w2 = st.columns(2)
    with w1:
        wind_dir = st.selectbox("Wind Direction", options=["North", "South", "East", "West", "Northeast", "Northwest", "Southeast", "Southwest"], key="env_wind_dir")
    with w2:
        wind_max = st.number_input("Maximum Wind Speed (km/h)", min_value=0.0, value=st.session_state.environment_data.get('wind_max', 108.0), key="env_wind_max")
        wind_avg = st.number_input("Average Wind Speed (km/h)", min_value=0.0, value=st.session_state.environment_data.get('wind_avg', 54.0), key="env_wind_avg")

    st.session_state.environment_data.update({
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
    })

    # show terrain and seismic summary (computed earlier)
    st.markdown("---")
    st.subheader("Provincial Summary (from previous step)")
    env_now = st.session_state.environment_data
    st.write(f"• Province: **{env_now.get('province','N/A')}**")
    st.write(f"• Terrain Category: **{env_now.get('terrain_category','N/A')}**, z₀ = **{env_now.get('terrain_z0','N/A')} m**, zmin = **{env_now.get('terrain_zmin','N/A')} m**")
    st.write(f"• Seismic Hazard: **{env_now.get('seismic_hazard','Unknown')}**")
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# Step 6: Soil Type & Importance (importance auto)
elif st.session_state.step == 6:
    st.header("Step 7: Soil Type & Importance (Importance computed automatically)")
    st.markdown("---")

    soil_types = {
        "Type I": {"group_factor": 1.4, "desc": "Hard rock or very stiff soils"},
        "Type II": {"group_factor": 1.2, "desc": "Moderately stiff soils"},
        "Type III": {"group_factor": 1.0, "desc": "Medium dense soils"},
        "Type IV": {"group_factor": 0.8, "desc": "Soft soils (high moisture)"}
    }

    selected_soil = st.selectbox("Select Soil Type", options=list(soil_types.keys()), key="soil_type_select")
    st.session_state.soil_type = selected_soil

    # compute importance group from seismic hazard automatically
    prov = st.session_state.environment_data.get('province')
    seismic = st.session_state.environment_data.get('seismic_hazard', 'Unknown')
    # map seismic hazard to importance group:
    seismic_to_group = {
        "Very High": ("Group 1", 1.4),
        "High": ("Group 2", 1.2),
        "Moderate": ("Group 3", 1.0),
        "Low": ("Group 4", 0.8),
        "Unknown": ("Group 3", 1.0)
    }
    importance_name, importance_factor = seismic_to_group.get(seismic, ("Group 3", 1.0))
    st.session_state.importance_group = importance_name

    st.markdown("---")
    st.subheader("Selected Soil & Computed Importance")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Soil Type:** {selected_soil}")
        st.write(f"**Soil Factor:** {soil_types[selected_soil]['group_factor']}")
    with col2:
        st.write(f"**Importance Group (auto):** {importance_name}")
        st.write(f"**Importance Factor:** {importance_factor}")

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# Step 7: orientation (same as before)
elif st.session_state.step == 7:
    st.header("Step 8: Carousel Orientation Selection")
    st.markdown("---")
    wind_direction = st.session_state.environment_data.get('wind_direction', 'North')
    st.subheader(f"Suggested Orientation Based on Wind Direction: {wind_direction}")
    st.info(f"Based on the prevailing wind direction ({wind_direction}), we recommend orienting the carousel in the same direction for optimal wind load distribution.")

    # Reuse orientation diagram helper (kept simple)
    directions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
    angles = [90, 45, 0, 315, 270, 225, 180, 135]
    fig = go.Figure()
    theta = np.linspace(0, 2*np.pi, 100)
    fig.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode='lines', line=dict(color='gray'), showlegend=False))
    for d,a in zip(directions,angles):
        ar = np.radians(a)
        fig.add_trace(go.Scatter(x=[0, 1.2*np.cos(ar)], y=[0, 1.2*np.sin(ar)], mode='lines+text', text=[None, d], textposition='top center', showlegend=False))
    fig.update_layout(title=f"Orientation suggestion: {wind_direction}", xaxis=dict(visible=False), yaxis=dict(visible=False), height=400)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm Suggested Orientation"):
            st.session_state.carousel_orientation = wind_direction
            st.session_state.orientation_confirmed = True
            st.success(f"Orientation confirmed: {wind_direction}")
    with col2:
        custom_direction = st.selectbox("Or select custom orientation", options=directions, index=directions.index(wind_direction) if wind_direction in directions else 0)
        if st.button("Set Custom Orientation"):
            st.session_state.carousel_orientation = custom_direction
            st.session_state.orientation_confirmed = True
            st.success(f"Custom orientation set: {custom_direction}")

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# Step 8: Device classification (NS8987) - unchanged
elif st.session_state.step == 8:
    st.header("Step 9: Device Classification (NS 8987)")
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
    braking_accel = st.number_input("Braking Acceleration (m/s²)", min_value=0.01, max_value=2.0, value=st.session_state.braking_acceleration, step=0.01, format="%.2f", key="brake_input_step8")
    st.session_state.braking_acceleration = braking_accel
    st.markdown("---")
    st.subheader("Design Case (1 rpm, 0.7 m/s²)")
    omega_design = 1.0 * (2.0 * np.pi / 60.0)
    p_design, n_design, max_accel_design = calculate_dynamic_product(diameter, height, omega_design, 0.7)
    class_design = classify_device(p_design)
    st.metric("Design Max Accel", f"{max_accel_design:.3f} m/s²")
    st.metric("Design Dynamic Product p", f"{p_design:.2f}")
    st.metric("Design Class", f"Class {class_design}")
    st.markdown("---")
    st.subheader("Actual Operation")
    p_actual, n_actual, max_accel_actual = calculate_dynamic_product(diameter, height, angular_velocity, braking_accel)
    class_actual = classify_device(p_actual)
    st.metric("Actual Max Accel", f"{max_accel_actual:.3f} m/s²")
    st.metric("Actual Dynamic Product p", f"{p_actual:.2f}")
    st.metric("Actual Class", f"Class {class_actual}")
    st.session_state.classification_data.update({
        'p_design': p_design, 'class_design': class_design, 'max_accel_design': max_accel_design, 'n_design': n_design,
        'p_actual': p_actual, 'class_actual': class_actual, 'max_accel_actual': max_accel_actual, 'n_actual': n_actual
    })
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# Step 9: Restraint Type — show BOTH ISO & AS diagrams and compute predominant for each
elif st.session_state.step == 9:
    st.header("Step 10: Restraint Determination — ISO & AS (comparison)")
    st.markdown("This page shows both standards side-by-side and reports predominant district/zone for each.")
    st.markdown("---")

    diameter = st.session_state.diameter
    rotation_time_min = st.session_state.rotation_time_min
    braking_accel = st.session_state.braking_acceleration
    if rotation_time_min and rotation_time_min > 0:
        rotation_time_sec = rotation_time_min * 60.0
        angular_velocity = 2.0 * np.pi / rotation_time_sec
    else:
        angular_velocity = 0.0

    # sample angles and determine zones
    theta_vals = np.linspace(0, 2*np.pi, 360)
    iso_list = []
    as_list = []
    ax_vals = []; az_vals = []
    max_ax = -np.inf; max_az = -np.inf
    min_ax = np.inf; min_az = np.inf

    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel)
        ax_g = a_x / 9.81
        az_g = a_z / 9.81  # az positive down
        ax_vals.append(ax_g); az_vals.append(az_g)
        iso_list.append(determine_restraint_area_iso(ax_g, az_g))
        as_list.append(determine_restraint_area_as(ax_g, az_g))
        max_ax = max(max_ax, ax_g); min_ax = min(min_ax, ax_g)
        max_az = max(max_az, az_g); min_az = min(min_az, az_g)

    iso_counts = Counter(iso_list)
    as_counts = Counter(as_list)
    predominant_iso = iso_counts.most_common(1)[0][0]
    predominant_as = as_counts.most_common(1)[0][0]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ISO Result")
        st.metric("Predominant ISO District", f"District {predominant_iso}")
        st.write("Recommended restraint (ISO):")
        iso_descr = {
            1: "District 1: Maximum restraint (full body harness)",
            2: "District 2: Enhanced restraint (over-shoulder)",
            3: "District 3: Standard restraint (lap bar/seat belt)",
            4: "District 4: Moderate restraint (belt + lap bar)",
            5: "District 5: Special consideration (enhanced harness)"
        }
        st.info(iso_descr.get(predominant_iso, "Standard restraint"))
        fig_iso = plot_acceleration_envelope_iso(diameter, angular_velocity, braking_accel)
        st.plotly_chart(fig_iso, use_container_width=True)

    with col2:
        st.subheader("AS Result")
        st.metric("Predominant AS Zone", f"Zone {predominant_as}")
        st.write("Recommended restraint (AS-style):")
        as_descr = {
            1: "Zone 1: Right-lower region - (per your mapping)",
            2: "Zone 2: Central-down",
            3: "Zone 3: Central/side bands",
            4: "Zone 4: Left-lower bands",
            5: "Zone 5: Upper/left/upward activity"
        }
        st.info(as_descr.get(predominant_as, "Standard restraint"))
        fig_as = plot_acceleration_envelope_as(diameter, angular_velocity, braking_accel)
        st.plotly_chart(fig_as, use_container_width=True)

    st.markdown("---")
    st.write("Max/min accelerations (g):")
    st.write(f"ax max: {max_ax:.3f}g, ax min: {min_ax:.3f}g — az max: {max_az:.3f}g, az min: {min_az:.3f}g")

    # update session classification
    st.session_state.classification_data.update({
        'pred_iso': predominant_iso,
        'pred_as': predominant_as,
        'max_ax_g': max_ax, 'min_ax_g': min_ax, 'max_az_g': max_az, 'min_az_g': min_az
    })

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# Step 10: Final summary
elif st.session_state.step == 10:
    st.header("Step 11: Complete Design Summary")
    st.markdown("---")
    st.subheader("Basic Parameters")
    st.write(f"Generation: {st.session_state.generation_type}")
    st.write(f"Diameter: {st.session_state.diameter} m")
    st.write(f"Cabins: {st.session_state.num_cabins} (VIP: {st.session_state.num_vip_cabins})")
    st.write(f"Cabin capacity: {st.session_state.cabin_capacity}")
    st.write(f"Cabin geometry: {st.session_state.cabin_geometry}")
    st.markdown("---")
    st.subheader("Environment & Site")
    env = st.session_state.environment_data
    if env:
        st.write(f"Province: {env.get('province','N/A')}")
        st.write(f"Terrain category: {env.get('terrain_category','N/A')}, z₀ = {env.get('terrain_z0','N/A')} m")
        st.write(f"Seismic hazard: {env.get('seismic_hazard','N/A')}")
        st.write(f"Wind: {env.get('wind_direction','N/A')} | max {env.get('wind_max',0)} km/h")
    st.markdown("---")
    st.subheader("Soil & Importance")
    st.write(f"Soil type: {st.session_state.soil_type}")
    st.write(f"Importance group (auto): {st.session_state.importance_group}")
    st.markdown("---")
    st.subheader("Classification & Restraints")
    cd = st.session_state.classification_data
    if cd:
        st.write(f"Design class: {cd.get('class_design','N/A')}, Actual class: {cd.get('class_actual','N/A')}")
        st.write(f"Predominant ISO District: {cd.get('pred_iso','N/A')}")
        st.write(f"Predominant AS Zone: {cd.get('pred_as','N/A')}")
    st.markdown("---")
    st.subheader("Visualization")
    height = st.session_state.diameter * 1.1
    vip_cap = max(0, st.session_state.cabin_capacity - 2)
    total_capacity_per_rotation = st.session_state.num_vip_cabins * vip_cap + (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity
    ang = (2.0 * np.pi) / (st.session_state.rotation_time_min * 60.0) if st.session_state.rotation_time_min else 0.0
    total_mass = st.session_state.num_cabins * st.session_state.cabin_capacity * 80.0
    moment_of_inertia = total_mass * (st.session_state.diameter/2.0)**2
    motor_power = moment_of_inertia * ang**2 / 1000.0 if ang else 0.0
    fig = create_component_diagram(st.session_state.diameter, height, total_capacity_per_rotation, motor_power)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    l, m, r = st.columns([1,0.5,1])
    with l:
        st.button("⬅️ Back", on_click=go_back)
    with m:
        st.button("🔄 New Design", on_click=reset_design)
    st.success("✅ Design Complete!")

