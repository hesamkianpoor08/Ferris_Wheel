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
    st.session_state.step = 0
if 'standards_confirmed' not in st.session_state:
    st.session_state.standards_confirmed = False
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
if 'terrain_calculated' not in st.session_state:
    st.session_state.terrain_calculated = False

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
    "Tehran": "Very High", "Alborz": "Very High", "Kermanshah": "Very High",
    "Kohgiluyeh and Boyer-Ahmad": "Very High", "Lorestan": "Very High",
    "West Azerbaijan": "Very High", "East Azerbaijan": "Very High",
    "Fars": "Very High", "Hormozgan": "Very High", "Kurdistan": "High",
    "Ilam": "High", "Chaharmahal and Bakhtiari": "High", "Bushehr": "High",
    "Mazandaran": "High", "Gilan": "High", "Khorasan Razavi": "High",
    "South Khorasan": "High", "Qazvin": "Moderate", "Zanjan": "Moderate",
    "Semnan": "Moderate", "Markazi": "Moderate", "Isfahan": "Moderate",
    "Kerman": "Moderate", "Qom": "Low", "Yazd": "Low", "Khuzestan": "Low",
    "Golestan": "Low", "North Khorasan": "Low", "Sistan and Baluchestan": "Low"
}

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

def _rotate_points(xy_x, xy_y, cx, cy, angle_rad):
    """Rotate arrays of points (xy_x, xy_y) about center (cx,cy) by angle_rad."""
    dx = np.array(xy_x) - cx
    dy = np.array(xy_y) - cy
    cosA = np.cos(angle_rad)
    sinA = np.sin(angle_rad)
    rx = cx + (dx * cosA - dy * sinA)
    ry = cy + (dx * sinA + dy * cosA)
    return rx.tolist(), ry.tolist()

def create_component_diagram(diameter, height, capacity, motor_power, num_cabins=12,
                             cabin_geometry="Square", cabin_orientation="vertical"):
    """Enhanced carousel diagram with properly scaled cabins and placement around the wheel.

    cabin_geometry: "Square", "Spherical", "Vertical Cylinder", "Horizontal Cylinder"
    cabin_orientation: "vertical" (upright) or "outward" (rotate to face radially)
    """
    # Basic geometry
    theta = np.linspace(0, 2*np.pi, 400)
    radius = diameter / 2.0
    x_wheel = radius * np.cos(theta)
    y_wheel = radius * np.sin(theta) + height/2.0

    fig = go.Figure()

    # Draw wheel
    fig.add_trace(go.Scatter(x=x_wheel, y=y_wheel, mode='lines',
                             line=dict(color='#2196F3', width=3),
                             showlegend=False, name='Wheel'))

    # Draw support structure (center column)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, height/2], mode='lines',
                             line=dict(color='#FF5722', width=6),
                             showlegend=False, name='Support'))

    # cabin sizing: base scale, but limited by arc spacing to avoid overlap
    circumference = 2 * np.pi * radius if radius > 0 else 1.0
    arc_spacing = circumference / max(1, num_cabins)
    # base desired cabin width (fraction of diameter) and max by arc spacing
    base_w = diameter * 0.04
    max_w = arc_spacing * 0.75   # keep some gap
    cabin_scale = min(base_w, max_w)

    # small radial offset to place cabin slightly outside the rim (so they are visible)
    radial_offset = cabin_scale * 0.1

    for i in range(num_cabins):
        angle = 2.0 * np.pi * i / num_cabins
        cabin_x = (radius + radial_offset) * np.cos(angle)
        cabin_y = (radius + radial_offset) * np.sin(angle) + height/2.0

        # decide rotation in radians
        if cabin_orientation == "outward":
            rot = angle  # rotate so long axis points radially
        else:
            rot = 0.0  # keep upright (no rotation)

        if cabin_geometry == "Spherical":
            # Draw circle for spherical cabin
            cabin_theta = np.linspace(0, 2*np.pi, 40)
            cx = cabin_x + (cabin_scale * 0.5) * np.cos(cabin_theta)
            cy = cabin_y + (cabin_scale * 0.5) * np.sin(cabin_theta)
            fig.add_trace(go.Scatter(x=cx, y=cy, mode='lines',
                                     fill='toself', fillcolor='rgba(255, 193, 7, 0.7)',
                                     line=dict(color='#FFC107', width=1.5),
                                     showlegend=False, hoverinfo='skip'))

        elif cabin_geometry == "Vertical Cylinder":
            # vertical rectangle (height > width)
            w = cabin_scale * 0.45
            h = cabin_scale * 1.0
            rect_x = [cabin_x - w/2, cabin_x + w/2, cabin_x + w/2, cabin_x - w/2, cabin_x - w/2]
            rect_y = [cabin_y - h/2, cabin_y - h/2, cabin_y + h/2, cabin_y + h/2, cabin_y - h/2]
            if rot != 0.0:
                rx, ry = _rotate_points(rect_x, rect_y, cabin_x, cabin_y, rot)
            else:
                rx, ry = rect_x, rect_y
            fig.add_trace(go.Scatter(x=rx, y=ry, mode='lines',
                                     fill='toself', fillcolor='rgba(76, 175, 80, 0.7)',
                                     line=dict(color='#4CAF50', width=1.5),
                                     showlegend=False, hoverinfo='skip'))

        elif cabin_geometry == "Horizontal Cylinder":
            # horizontal rectangle (width > height)
            w = cabin_scale * 1.0
            h = cabin_scale * 0.45
            rect_x = [cabin_x - w/2, cabin_x + w/2, cabin_x + w/2, cabin_x - w/2, cabin_x - w/2]
            rect_y = [cabin_y - h/2, cabin_y - h/2, cabin_y + h/2, cabin_y + h/2, cabin_y - h/2]
            if rot != 0.0:
                rx, ry = _rotate_points(rect_x, rect_y, cabin_x, cabin_y, rot)
            else:
                rx, ry = rect_x, rect_y
            fig.add_trace(go.Scatter(x=rx, y=ry, mode='lines',
                                     fill='toself', fillcolor='rgba(156, 39, 176, 0.7)',
                                     line=dict(color='#9C27B0', width=1.5),
                                     showlegend=False, hoverinfo='skip'))

        else:  # Square (default)
            s = cabin_scale * 0.8
            square_x = [cabin_x - s/2, cabin_x + s/2, cabin_x + s/2, cabin_x - s/2, cabin_x - s/2]
            square_y = [cabin_y - s/2, cabin_y - s/2, cabin_y + s/2, cabin_y + s/2, cabin_y - s/2]
            if rot != 0.0:
                rx, ry = _rotate_points(square_x, square_y, cabin_x, cabin_y, rot)
            else:
                rx, ry = square_x, square_y
            fig.add_trace(go.Scatter(x=rx, y=ry, mode='lines',
                                     fill='toself', fillcolor='rgba(244, 67, 54, 0.7)',
                                     line=dict(color='#F44336', width=1.5),
                                     showlegend=False, hoverinfo='skip'))

        # Cabin number annotation (slightly further outward than cabin center)
        ann_r = radius + radial_offset + cabin_scale * 0.6
        ann_x = ann_r * np.cos(angle)
        ann_y = ann_r * np.sin(angle) + height/2.0
        fig.add_annotation(x=ann_x, y=ann_y, text=str(i+1),
                           showarrow=False, font=dict(size=10, color='black'))

    # top/bottom annotations (as before)
    annotations = [
        dict(x=0, y=height + diameter*0.05 + 2, text=f"Height: {height:.1f} m",
             showarrow=False, font=dict(color='black', size=12)),
        dict(x=diameter/2 + 2, y=height/2, text=f"Diameter: {diameter} m",
             showarrow=False, font=dict(color='black', size=12)),
        dict(x=0, y=-5, text=f"Motor Power: {motor_power:.1f} kW",
             showarrow=False, font=dict(color='black', size=12)),
        dict(x=0, y=-8, text=f"Capacity: {capacity} passengers",
             showarrow=False, font=dict(color='black', size=12)),
        dict(x=0, y=-11, text=f"Cabins: {num_cabins} ({cabin_geometry}, orientation={cabin_orientation})",
             showarrow=False, font=dict(color='black', size=10))
    ]

    fig.update_layout(
        title=dict(text="Ferris Wheel Design Overview", font=dict(color='black', size=16)),
        height=650,
        template="plotly_white",
        plot_bgcolor='white',
        paper_bgcolor='white',
        annotations=annotations,
        margin=dict(l=80, r=80, t=80, b=80),
        xaxis=dict(scaleanchor="y", scaleratio=1, showgrid=True, gridcolor='lightgray',
                   zeroline=False, visible=True),
        yaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=False, visible=True)
    )

    # center view on wheel
    pad = diameter * 0.15
    fig.update_xaxes(range=[-radius - pad, radius + pad])
    fig.update_yaxes(range=[-radius*0.1, height + radius + pad])

    return fig

def calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g=9.81):
    radius = diameter / 2.0
    a_centripetal = radius * (angular_velocity ** 2)
    
    a_z_gravity = -g
    a_x_gravity = 0
    
    a_x_centripetal = a_centripetal * np.cos(theta)
    a_z_centripetal = a_centripetal * np.sin(theta)
    
    a_x_braking = braking_accel * np.sin(theta)
    a_z_braking = -braking_accel * np.cos(theta)
    
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

def classify_device(dynamic_product):
    """Classification per INSO 8987-1-2023"""
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

def determine_restraint_area_iso(ax, az):
    """Determine restraint area based on ISO 17842-2023 (ax and az in units of g)"""
    # District 1: Upper region
    if ax > 0.2 and az > 0.2:
        return 1
    if 0 < ax <= 0.2 and az > 0.7:
        return 1
    if -0.2 < ax < 0 and az > (-1.5 * ax + 0.7):
        return 1
    
    # District 2: Upper-central region
    if 0 < ax <= 0.2 and 0.2 < az <= 0.7:
        return 2
    if -0.2 < ax < 0 and 0.2 < az <= (-1.5 * ax + 0.7):
        return 2
    if -0.7 < ax <= -0.2 and az > 0.2:
        return 2
    
    # District 3: Central edges
    if -1.2 < ax <= -0.7 and az > 0.2:
        return 3
    if -0.7 < ax < 0 and ((-0.2/0.7) * ax) < az <= 0.2:
        return 3
    if ax > 0 and 0 < az <= 0.2:
        return 3
    
    # District 4: Lower-central region
    if -0.7 < ax < 0 and 0 < az < ((-0.2/0.7) * ax):
        return 4
    if -1.2 < ax <= -0.7 and 0 < az <= 0.2:
        return 4
    if -1.8 < ax <= -1.2 and az > 0:
        return 4
    if 0 < ax <= 0.7 and ((-0.2/0.7) * ax) < az < 0:
        return 4
    if ax > 0.7 and -0.2 < az < 0:
        return 4
    
    # District 5: Lower region
    if ax > 0.7 and az < -0.2:
        return 5
    if 0 < ax <= 0.7 and az < ((-0.2/0.7) * ax):
        return 5
    if ax < 0 and az < 0:
        return 5
    if ax < -1.8:
        return 5
    
    return 2  # Default

def determine_restraint_area_as(ax, az):
    """Determine restraint area based on AS 3533.1-2009+A1-2011 (ax and az in units of g)"""
    # Region 1: Upper region
    if ax > 0.2 and az > 0.2:
        return 1
    
    # Zone 2: Upper-central region
    if -0.7 < ax <= 0.2 and az > 0.2:
        return 2
    
    # Zone 3: Central region
    if -0.7 < ax <= 0.7 and ((-0.2/0.7) * ax) < az <= 0.2:
        return 3
    if ax > 0.7 and -0.2 < az <= 0.2:
        return 3
    if -1.2 < ax <= -0.7 and az > 0.2:
        return 3
    
    # Zone 4: Lower-central region
    if -0.7 < ax < 0 and 0 < az < ((-0.2/0.7) * ax):
        return 4
    if -1.2 < ax <= -0.7 and 0 < az <= 0.2:
        return 4
    if -1.8 < ax <= -1.2 and az > 0:
        return 4
    
    # Zone 5: Lower region
    if ax <= 0 and az <= 0:
        return 5
    if 0.7 <= ax and az < -0.2:
        return 5
    if 0 < ax < 0.7 and az < ((-0.2/0.7) * ax):
        return 5
    if ax < -1.8:
        return 5
    
    return 2  # Default

def plot_acceleration_envelope_iso(diameter, angular_velocity, braking_accel, g=9.81):
    """Plot the ax vs az acceleration envelope with ISO 17842 zones and actual acceleration points"""
    theta_vals = np.linspace(0, 2*np.pi, 360)
    ax_vals = []
    az_vals = []
    
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g)
        ax_vals.append(a_x / g)
        az_vals.append(a_z / g)
    
    ax_vals = np.array(ax_vals)
    az_vals = np.array(az_vals)
    
    fig = go.Figure()
    
    
    # Plot actual acceleration envelope (after zones for visibility)
    fig.add_trace(go.Scatter(x=ax_vals, y=az_vals, mode='lines',
                             line=dict(color='#2196F3', width=3),
                             name='Acceleration Envelope'))

    magnitudes = np.sqrt(ax_vals**2 + az_vals**2)
    max_idx = int(np.argmax(magnitudes))
    max_ax = ax_vals[max_idx]
    max_az = az_vals[max_idx]
    max_mag = magnitudes[max_idx]
    max_theta_deg = float(np.degrees(theta_vals[max_idx]))
    label = f'Max |a|: {max_mag:.3f} g\n(ax={max_ax:.3f}g, az={max_az:.3f}g)\nθ={max_theta_deg:.1f}°'
    
    fig.add_trace(go.Scatter(
        x=[max_ax], y=[max_az],
        mode='markers+text',
        marker=dict(size=16, color='red', symbol='star',
                    line=dict(color='darkred', width=2)),
        text=[label],
        textposition='top center',
        textfont=dict(size=10, color='darkred', family='Arial Black'),
        showlegend=False,
        hoverinfo='text',
        hovertext=label
    ))
    
    fig.update_layout(
        title="ISO 17842 - Acceleration Envelope with Operating Points", 
        xaxis_title="Horizontal Acceleration ax [g]",
        yaxis_title="Vertical Acceleration az [g]", 
        height=700, 
        template="plotly_white",
        xaxis=dict(range=[-2.2, 2.2], zeroline=True, zerolinewidth=2, zerolinecolor='black'),
        yaxis=dict(range=[-2.2, 2.2], zeroline=True, zerolinewidth=2, zerolinecolor='black')
    )
    return fig

def plot_acceleration_envelope_as(diameter, angular_velocity, braking_accel, g=9.81):
    """Plot the ax vs az acceleration envelope with AS 3533.1 zones and actual acceleration points"""
    theta_vals = np.linspace(0, 2*np.pi, 360)
    ax_vals = []
    az_vals = []
    
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, g)
        ax_vals.append(a_x / g)
        az_vals.append(a_z / g)
    
    ax_vals = np.array(ax_vals)
    az_vals = np.array(az_vals)
    
    fig = go.Figure()

    # Plot actual acceleration envelope (after zones for visibility)
    fig.add_trace(go.Scatter(x=ax_vals, y=az_vals, mode='lines',
                             line=dict(color='#2196F3', width=3),
                             name='Acceleration Envelope'))
    
    magnitudes = np.sqrt(ax_vals**2 + az_vals**2)
    max_idx = int(np.argmax(magnitudes))
    max_ax = ax_vals[max_idx]
    max_az = az_vals[max_idx]
    max_mag = magnitudes[max_idx]
    max_theta_deg = float(np.degrees(theta_vals[max_idx]))
    label = f'Max |a|: {max_mag:.3f} g\n(ax={max_ax:.3f}g, az={max_az:.3f}g)\nθ={max_theta_deg:.1f}°'
    
    fig.add_trace(go.Scatter(
        x=[max_ax], y=[max_az],
        mode='markers+text',
        marker=dict(size=16, color='red', symbol='star',
                    line=dict(color='darkred', width=2)),
        text=[label],
        textposition='top center',
        textfont=dict(size=10, color='darkred', family='Arial Black'),
        showlegend=False,
        hoverinfo='text',
        hovertext=label
    ))
    
    fig.update_layout(
        title="AS 3533.1 - Acceleration Envelope with Operating Points", 
        xaxis_title="Horizontal Acceleration ax [g]",
        yaxis_title="Vertical Acceleration az [g]", 
        height=700, 
        template="plotly_white",
        xaxis=dict(range=[-2.2, 2.2], zeroline=True, zerolinewidth=2, zerolinecolor='black'),
        yaxis=dict(range=[-2.2, 2.2], zeroline=True, zerolinewidth=2, zerolinecolor='black')
    )
    return fig

def create_orientation_diagram(selected_direction, land_length=None, land_width=None, diameter=None):
    """Create a visual diagram showing the carousel orientation on land area"""
    directions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
    angles = [90, 45, 0, 315, 270, 225, 180, 135]
    
    fig = go.Figure()
    
    # Draw land area rectangle if dimensions provided
    if land_length and land_width:
        # Normalize to fit in view
        max_dim = max(land_length, land_width)
        scale = 2.0 / max_dim  # Scale to fit in ±1.5 range
        
        rect_width = land_width * scale
        rect_height = land_length * scale
        
        # Draw land area
        land_x = [-rect_width/2, rect_width/2, rect_width/2, -rect_width/2, -rect_width/2]
        land_y = [-rect_height/2, -rect_height/2, rect_height/2, rect_height/2, -rect_height/2]
        
        fig.add_trace(go.Scatter(x=land_x, y=land_y, mode='lines', 
                                fill='toself', fillcolor='rgba(200, 200, 200, 0.3)',
                                line=dict(color='gray', width=2),
                                name='Land Area',
                                showlegend=True))
        
        # Add land dimensions annotation
        fig.add_annotation(x=0, y=rect_height/2 + 0.15, 
                          text=f"Land: {land_length}m × {land_width}m",
                          showarrow=False, font=dict(size=12, color='gray'))
    
    # Draw compass rose
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = 0.8 * np.cos(theta)
    y_circle = 0.8 * np.sin(theta)
    fig.add_trace(go.Scatter(x=x_circle, y=y_circle, mode='lines', 
                            line=dict(color='lightgray', width=1, dash='dash'), 
                            showlegend=False))
    
    # Draw direction indicators
    for direction, angle in zip(directions, angles):
        angle_rad = np.radians(angle)
        x = 1.0 * np.cos(angle_rad)
        y = 1.0 * np.sin(angle_rad)
        
        color = 'red' if direction == selected_direction else 'blue'
        size = 14 if direction == selected_direction else 10
        width = 3 if direction == selected_direction else 1
        
        fig.add_trace(go.Scatter(x=[0, x], y=[0, y], mode='lines+text', 
                                line=dict(color=color, width=width),
                                text=['', direction], textposition='top center',
                                textfont=dict(size=size, color=color, 
                                            family='Arial Black' if direction == selected_direction else 'Arial'),
                                showlegend=False))
    
    # Draw ferris wheel on land area
    if selected_direction in directions and diameter:
        idx = directions.index(selected_direction)
        angle_rad = np.radians(angles[idx])
        
        # Scale wheel to fit
        if land_length and land_width:
            max_dim = max(land_length, land_width)
            scale = 2.0 / max_dim
            wheel_radius = (diameter / 2) * scale * 0.8  # 80% of actual size for visibility
        else:
            wheel_radius = 0.15
        
        # Position wheel at center
        wheel_center_x = 0
        wheel_center_y = 0
        
        # Draw wheel
        wheel_theta = np.linspace(0, 2*np.pi, 50)
        wheel_x = wheel_center_x + wheel_radius * np.cos(wheel_theta)
        wheel_y = wheel_center_y + wheel_radius * np.sin(wheel_theta)
        
        fig.add_trace(go.Scatter(x=wheel_x, y=wheel_y, mode='lines', 
                                fill='toself', fillcolor='rgba(33, 150, 243, 0.3)',
                                line=dict(color='#2196F3', width=3), 
                                name='Ferris Wheel',
                                showlegend=True))
        
        # Draw orientation arrow on wheel
        arrow_length = wheel_radius * 0.7
        arrow_x = wheel_center_x + arrow_length * np.cos(angle_rad)
        arrow_y = wheel_center_y + arrow_length * np.sin(angle_rad)
        
        fig.add_annotation(x=arrow_x, y=arrow_y, ax=wheel_center_x, ay=wheel_center_y,
                          xref='x', yref='y', axref='x', ayref='y',
                          showarrow=True, arrowhead=3, arrowsize=2, arrowwidth=3,
                          arrowcolor='red')
    
    fig.update_layout(title=f"Ferris Wheel Orientation: {selected_direction}",
                      xaxis=dict(range=[-1.5, 1.5], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="y"),
                      yaxis=dict(range=[-1.5, 1.5], showgrid=False, zeroline=False, showticklabels=False, scaleratio=1),
                      height=600, template="plotly_white", paper_bgcolor='white', plot_bgcolor='white',
                      legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)'))
    return fig

# --- Navigation & validation ---
def select_generation(gen):
    st.session_state.generation_type = gen
    st.session_state.step = 2

def go_back():
    st.session_state.step = max(0, st.session_state.step - 1)

def reset_design():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def validate_current_step_and_next():
    s = st.session_state
    errors = []

    if s.step == 0:
        if not s.standards_confirmed:
            errors.append("Please confirm your understanding of the standards.")
    elif s.step == 1:
        if not s.generation_type:
            errors.append("Please select a generation.")
    elif s.step == 2:
        if not s.cabin_geometry:
            errors.append("Please select a cabin geometry.")
    elif s.step == 3:
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
    elif s.step == 4:
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
    elif s.step == 6:
        if not s.terrain_calculated:
            errors.append("Please click 'Calculate Terrain Parameters' before continuing.")
    elif s.step == 7:
        if not s.soil_type:
            errors.append("Please select a soil type.")
    elif s.step == 8:
        if not s.orientation_confirmed:
            errors.append("Please confirm the carousel orientation or select a custom direction.")
    
    if errors:
        st.session_state.validation_errors = errors
        for e in errors:
            st.error(e)
    else:
        st.session_state.validation_errors = []
        st.session_state.step = min(12, st.session_state.step + 1)

# --- UI ---
st.title("🎡 Ferris Wheel Designer")
total_steps = 13
st.progress(st.session_state.get('step', 0) / (total_steps - 1))
st.markdown(f"**Step {st.session_state.get('step', 0) + 1} of {total_steps}**")
st.markdown("---")

# === STEP 0: Welcome and Standards ===
if st.session_state.get('step', 0) == 0:
    st.header("Welcome to Ferris Wheel Designer")
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 About This Application
    
    This comprehensive Ferris Wheel Design Tool assists engineers and designers in creating safe, efficient, 
    and compliant ferris wheel installations. The application guides you through:
    
    - **Generation Selection**: Choose from various ferris wheel generations and structural types
    - **Cabin Configuration**: Design cabin geometry, capacity, and VIP arrangements
    - **Performance Analysis**: Calculate rotation times, speeds, and passenger capacity
    - **Environmental Assessment**: Analyze site conditions, wind loads, and terrain parameters
    - **Safety Classification**: Determine device class and restraint requirements
    - **Structural Design**: Generate comprehensive design specifications
    
    ### 📋 Design Standards & References
    
    This application implements calculations and requirements based on the following international and national standards:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Current Standards for Amusement Devices:
        - **AS 3533.1-2009+A1-2011** - Amusement rides and devices - Design and construction
        - **INSO 8987-1-2023** - Safety of amusement rides and amusement devices - Part 1: General requirements
        - **INSO 8987-2-2022** - Safety of amusement rides and amusement devices - Part 2: Operation and maintenance
        - **INSO 8987-3-2022** - Safety of amusement rides and amusement devices - Part 3: Requirements for inspection
        - **ISO 17842-2-2022** - Safety of amusement rides and amusement devices - Part 2: Operation and maintenance
        - **ISO 17842-3-2022** - Safety of amusement rides and amusement devices - Part 3: Requirements for inspection
        - **ISO 17842-2023** - Safety of amusement rides and amusement devices
        
        #### Legacy Standards (Reference):
        - **AS 3533.2-2009+A1-2011** - Amusement rides and devices - Operation and maintenance
        - **AS 3533.3-2003 R2013** - Amusement rides and devices - Qualification of inspection personnel
        - **INSO 8987-2-2009** - Safety of amusement rides (Previous edition)
        - **INSO 8987-3-2003** - Safety of amusement rides (Previous edition)
        - **INSO 8987-2009** - Safety of amusement rides (Previous edition)
        """)
    
    with col2:
        st.markdown("""
        #### Standards for Load Analysis:
        - **ISIRI 519** - Iranian National Standard - Design loads for buildings
        - **AS 1170.4-2007(A1)** - Structural design actions - Wind actions
        - **BS EN 1991-1-4:2005+A1-2010** - Eurocode 1: Actions on structures - Wind actions
        - **DIN 18800-1-1990** - Structural steelwork - Design and construction
        - **DIN 18800-2-1990** - Structural steelwork - Stability, buckling of shells
        - **EN 1991-1-3:2003** - Eurocode 1: Actions on structures - Snow loads
        - **EN 1993-1-9:2005** - Eurocode 3: Design of steel structures - Fatigue
        - **EN1993-1-9-AC 2009** - Eurocode 3: Design of steel structures - Fatigue (Amendment)
        - **ISIRI 2800** - Iranian Code of Practice for Seismic Resistant Design of Buildings (4th Edition)
        
        #### Key Application Areas:
        - **Wind Load Analysis**: AS 1170.4, EN 1991-1-4, ISIRI 2800
        - **Seismic Analysis**: ISIRI 2800
        - **Structural Design**: DIN 18800, EN 1993
        - **Safety Classification**: INSO 8987, ISO 17842
        """)
    
    st.markdown("---")
    st.warning("""
    ⚠️ **Important Notice:**
    
    By proceeding, you acknowledge that:
    - This tool provides preliminary design calculations based on the referenced standards
    - Final designs must be reviewed and approved by licensed professional engineers
    - Local building codes and regulations must be consulted and followed
    - Site-specific conditions may require additional analysis beyond this tool's scope
    - The designer assumes responsibility for verifying all calculations and compliance
    """)
    
    st.markdown("---")
    
    # Confirmation checkbox
    standards_accepted = st.checkbox(
        "✅ I understand and accept that all calculations are based on the standards listed above, "
        "and I will ensure compliance with local regulations and professional engineering review.",
        key="standards_confirmation"
    )
    
    st.session_state.standards_confirmed = standards_accepted
    
    if standards_accepted:
        st.success("✅ Standards confirmed. You may proceed to the design process.")
        if st.button("🚀 Start Design Process", type="primary"):
            st.session_state.step = 1
            st.rerun()
    else:
        st.info("Please confirm your understanding of the standards to continue.")

# === STEP 1: Generation selection ===
elif st.session_state.get('step', 0) == 1:
    st.header("Step 1: Select Ferris Wheel Generation")
    st.markdown("---")
    
    image_files = ["./git/assets/1st.jpg", "./git/assets/2nd_1.jpg", "./git/assets/2nd_2.jpg", "./git/assets/4th.jpg"]
    captions = ["1st Generation (Truss type)", "2nd Generation_1st type (Cable type)", "2nd Generation_2nd type (Pure cable type)", "4th Generation (Hubless centerless)"]
    
    cols = st.columns(4, gap="small")
    for i, (col, img_path, caption) in enumerate(zip(cols, image_files, captions)):
        with col:
            try:
                st.image(img_path, width=240)
            except:
                st.write(f"Image not found: {img_path}")
            st.caption(caption)
            st.button("Select", key=f"gen_btn_{i}", on_click=select_generation, args=(caption,))
    
    st.markdown("---")
    st.write("Click the button under the image to select a generation and proceed.")

# === STEP 2: Cabin Geometry ===
if st.session_state.get("step", 0) == 2:
    st.header("Step 2: Select Cabin Geometry")
    st.markdown("Choose a cabin shape.")
    
    geom_images = [
        ("Square", "./git/assets/square.jpg"),
        ("Vertical Cylinder", "./git/assets/vertical.jpg"),
        ("Horizontal Cylinder", "./git/assets/horizontal.jpg"),
        ("Spherical", "./git/assets/sphere.jpg"),
    ]

    cols = st.columns(4, gap="small")

    def select_geometry_callback(selected_label):
        st.session_state.cabin_geometry = selected_label

        if "diameter" not in st.session_state:
            st.session_state.diameter = 0.0
        if "num_cabins" not in st.session_state:
            st.session_state.num_cabins = 1

        base = base_for_geometry(st.session_state.diameter, selected_label)
        min_c, max_c = calc_min_max_from_base(base)
        st.session_state.num_cabins = min(max(st.session_state.num_cabins, min_c), max_c)

        st.session_state.capacities_calculated = False
        st.session_state.step = 3   
        st.experimental_rerun()

    for i, (label, img_path) in enumerate(geom_images):
        with cols[i]:
            try:

                st.image(img_path, use_column_width=True)
            except Exception as e:
                import os
                st.write(f"Could not load image: {img_path}")
                st.write("Exists:", os.path.exists(img_path))
                st.write("Abs path:", os.path.abspath(img_path))
                st.write("Error:", e)
            st.caption(label)
            st.button("Select", key=f"geom_img_btn_{i}", on_click=select_geometry_callback, args=(label,))


# === STEP 3: Primary parameters ===
elif st.session_state.step == 3:
    st.header("Step 3: Cabin Capacity & VIP")
    st.subheader(f"Generation: {st.session_state.generation_type}")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        diameter = st.number_input("Ferris Wheel Diameter (m)", min_value=30, max_value=80, value=int(st.session_state.diameter), step=1, key="diameter_input")
        st.session_state.diameter = diameter

    geometry = st.session_state.cabin_geometry
    base = base_for_geometry(diameter, geometry) if geometry else (np.pi * diameter / 4.0)
    min_c, max_c = calc_min_max_from_base(base)

    num_cabins = st.number_input("Number of Cabins", min_value=min_c, max_value=max_c, 
                                  value=min(max(int(st.session_state.num_cabins), min_c), max_c), step=1, key="num_cabins_input")
    st.session_state.num_cabins = num_cabins

    c1, c2 = st.columns(2)
    with c1:
        cabin_capacity = st.number_input("Cabin Capacity (passengers per cabin)", min_value=4, max_value=8, 
                                         value=st.session_state.cabin_capacity, step=1, key="cabin_capacity_input")
        st.session_state.cabin_capacity = cabin_capacity
    with c2:
        num_vip = st.number_input("Number of VIP Cabins", min_value=0, max_value=st.session_state.num_cabins, 
                                   value=min(st.session_state.num_vip_cabins, st.session_state.num_cabins), step=1, key="num_vip_input")
        st.session_state.num_vip_cabins = num_vip

    st.markdown("---")
    if st.button("🔄 Calculate Capacities"):
        vip_cap = max(0, st.session_state.cabin_capacity - 2)
        vip_total = st.session_state.num_vip_cabins * vip_cap
        regular_total = (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity
        per_rotation = vip_total + regular_total
        c1, c2 = st.columns(2)
        c1.metric("Per-rotation capacity", f"{per_rotation} passengers")
        c2.metric("VIP capacity (per rotation)", f"{vip_total} passengers (each VIP: {vip_cap})")
        st.success("Capacities calculated.")
        st.session_state.capacities_calculated = True

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 4: Rotation Time ===
elif st.session_state.step == 4:
    st.header("Step 4: Rotation Time & Derived Speeds")
    st.markdown("---")

    diameter = st.session_state.diameter
    circumference = np.pi * diameter
    default_rotation_time_min = (circumference / 0.2) / 60.0 if diameter > 0 else 1.0

    rotation_time_min = st.number_input("Rotation time (minutes per full rotation)", min_value=0.01, max_value=60.0, 
                                         value=st.session_state.rotation_time_min if st.session_state.rotation_time_min else float(default_rotation_time_min), 
                                         step=0.01, format="%.2f", key="rotation_time_input")
    st.session_state.rotation_time_min = rotation_time_min

    ang, rpm, linear = calc_ang_rpm_linear_from_rotation_time(rotation_time_min, diameter)

    st.text_input("Rotational speed (rpm)", value=f"{rpm:.6f}", disabled=True)
    st.caption(f"Angular speed (rad/s): {ang:.6f}")
    st.text_input("Linear speed at rim (m/s)", value=f"{linear:.6f}", disabled=True)

    cap_per_hour = calculate_capacity_per_hour_from_time(st.session_state.num_cabins, st.session_state.cabin_capacity, 
                                                          st.session_state.num_vip_cabins, rotation_time_min)
    st.metric("Estimated Capacity per Hour", f"{cap_per_hour:.0f} passengers/hour")

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 5: Environment Conditions ===
elif st.session_state.step == 5:
    st.header("Step 5: Environment Conditions")
    st.markdown("**Design per AS 1170.4-2007(A1), EN 1991-1-4:2005, ISIRI 2800**")
    st.markdown("---")

    iran_provinces = list(TERRAIN_CATEGORIES.keys())

    c1, c2 = st.columns(2)
    with c1:
        province = st.selectbox("Province", options=iran_provinces, index=0, key="province_select")
    with c2:
        region_name = st.text_input(
            "Region / Area name",
            value=st.session_state.environment_data.get('region_name', ''),
            key="region_name_input"
        )

    st.markdown("---")
    st.subheader("Land Surface Area (meters)")
    l1, l2 = st.columns(2)
    with l1:
        land_length = st.number_input(
            "Land Length (m)",
            min_value=10,
            max_value=150,
            value=int(st.session_state.environment_data.get('land_length', 100)),
            step=1,
            key="land_length_input"
        )
    with l2:
        land_width = st.number_input(
            "Land Width (m)",
            min_value=10,
            max_value=150,
            value=int(st.session_state.environment_data.get('land_width', 100)),
            step=1,
            key="land_width_input"
        )
    st.metric("Total Land Area", f"{land_length * land_width} m²")

    st.markdown("---")
    st.subheader("Altitude and Temperature")
    a1, a2 = st.columns(2)
    with a1:
        temp_max = st.number_input(
            "Maximum Temperature (°C)",
            value=int(st.session_state.environment_data.get('temp_max', 40)),
            step=1,
            key="temp_max_input"
        )
    with a2:
        temp_min = st.number_input(
            "Minimum Temperature (°C)",
            value=int(st.session_state.environment_data.get('temp_min', -10)),
            step=1,
            key="temp_min_input"
        )
    altitude = st.number_input(
        "Altitude (m)",
        value=int(st.session_state.environment_data.get('altitude', 0)),
        step=1,
        key="altitude_input"
    )

    st.markdown("---")
    st.subheader("Wind Information")
    w1, w2 = st.columns(2)
    with w1:
        wind_dir = st.selectbox(
            "Wind Direction",
            options=["North", "South", "East", "West", "Northeast", "Northwest", "Southeast", "Southwest"],
            key="wind_dir_input"
        )
    with w2:
        wind_max = st.number_input(
            "Maximum Wind Speed (km/h)",
            min_value=0,
            value=int(st.session_state.environment_data.get('wind_max', 108)),
            step=1,
            key="wind_max_input"
        )
        wind_avg = st.number_input(
            "Average Wind Speed (km/h)",
            min_value=0,
            value=int(st.session_state.environment_data.get('wind_avg', 54)),
            step=1,
            key="wind_avg_input"
        )

    st.markdown("---")
    load_wind = st.checkbox("Load wind rose (upload jpg/pdf)", value=st.session_state.get('wind_rose_loaded', False), key="load_wind_checkbox")
    st.session_state.wind_rose_loaded = load_wind
    if load_wind:
        wind_file = st.file_uploader("Wind rose file (jpg/pdf)", type=['jpg', 'jpeg', 'pdf'], key="wind_rose_uploader")
        st.session_state.wind_rose_file = wind_file

    if province in TERRAIN_CATEGORIES:
        terrain = TERRAIN_CATEGORIES[province]
        seismic = SEISMIC_HAZARD.get(province, "Unknown")
    else:
        terrain = {"category": "II", "z0": 0.05, "zmin": 2, "desc": ""}
        seismic = "Unknown"

    st.session_state.environment_data = {
        'province': province, 'region_name': region_name, 'land_length': land_length, 'land_width': land_width,
        'land_area': land_length * land_width, 'altitude': altitude, 'temp_min': temp_min, 'temp_max': temp_max,
        'wind_direction': wind_dir, 'wind_max': wind_max, 'wind_avg': wind_avg,
        'terrain_category': terrain['category'], 'terrain_z0': terrain['z0'], 'terrain_zmin': terrain['zmin'],
        'terrain_desc': terrain.get('desc', ''), 'seismic_hazard': seismic
    }

    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 6: Provincial Characteristics (Terrain Calculation) ===
elif st.session_state.step == 6:
    st.header("Step 6: Provincial Characteristics & Terrain Parameters")
    st.markdown("**Terrain classification per AS 1170.4-2007(A1), ISIRI 2800**")
    st.markdown("---")
    
    env = st.session_state.environment_data
    province = env.get('province', 'Tehran')
    
    st.subheader(f"Selected Province: {province}")
    st.info(f"**Region:** {env.get('region_name', 'N/A')}")
    
    if province in TERRAIN_CATEGORIES:
        terrain = TERRAIN_CATEGORIES[province]
        seismic = SEISMIC_HAZARD.get(province, "Unknown")
        
        st.markdown("---")
        st.subheader("Terrain Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Terrain Category:** {terrain['category']}")
            st.markdown(f"**Description:** {terrain.get('desc', 'N/A')}")
        with col2:
            seismic_color = {"Very High": "🔴", "High": "🟠", "Moderate": "🟡", "Low": "🟢"}
            st.markdown(f"{seismic_color.get(seismic, '')} **Seismic Hazard (ISIRI 2800):** {seismic}")
        
        st.markdown("---")
        
        if st.button("🔄 Calculate Terrain Parameters", type="primary"):
            st.session_state.terrain_calculated = True
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Terrain Category", terrain['category'])
            with col2:
                st.metric("Roughness Length (z₀)", f"{terrain['z0']} m")
            with col3:
                st.metric("Minimum Height (z_min)", f"{terrain['zmin']} m")
            
            st.success("✅ Terrain parameters calculated successfully!")
            st.info(f"**z₀ = {terrain['z0']} m** - This value will be used for wind load calculations per AS 1170.4.")
        
        if st.session_state.terrain_calculated:
            st.markdown("---")
            st.success("✅ Terrain parameters have been calculated. You can proceed to the next step.")
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 7: Soil Type (auto-calculate Importance Group) ===
elif st.session_state.step == 7:
    st.header("Step 7: Soil Type & Importance Classification")
    st.markdown("**Soil classification per ISIRI 2800 (4th Edition)**")
    st.markdown("---")
    
    st.subheader("Soil Type Selection")
    
    soil_types = {
        "Type I": {
            "desc": "a. Coarse- and fine-grained igneous rocks, very hard and strong sedimentary rocks, and other hard conglomerate and silicate sedimentary rocks.\nb. Hard soils (dense sand and very stiff clay) with a total thickness of less than 30 meters above bedrock.",
            "group_factor": 1.4,
            "importance_group": "Group 1"
        },
        "Type II": {
            "desc": "a. Weak igneous rocks (such as tuff), moderately cemented sedimentary rocks, and rocks that have been partially weathered.\nb. Hard soils (dense sand and very stiff clay) with a total thickness greater than 30 meters.",
            "group_factor": 1.2,
            "importance_group": "Group 2"
        },
        "Type III": {
            "desc": "a. Weathered or decomposed metamorphic rocks.\nb. Medium dense soils, layers of sand and clay with moderate cohesion and medium stiffness.",
            "group_factor": 1.0,
            "importance_group": "Group 3"
        },
        "Type IV": {
            "desc": "a. Soft soils with high moisture content due to a shallow groundwater level.\nb. Any soil profile that includes at least 7 meters of clayey soil with a plasticity index greater than 20 or a moisture content higher than 40 percent.",
            "group_factor": 0.8,
            "importance_group": "Group 4"
        }
    }
    
    for soil_type, data in soil_types.items():
        with st.expander(f"{soil_type} (Factor: {data['group_factor']})"):
            st.write(data['desc'])
    
    selected_soil = st.selectbox("Select Soil Type", options=list(soil_types.keys()), key="soil_type_select")
    st.session_state.soil_type = selected_soil
    
    # Auto-calculate importance group based on soil type
    auto_importance_group = soil_types[selected_soil]['importance_group']
    auto_importance_factor = soil_types[selected_soil]['group_factor']
    st.session_state.importance_group = auto_importance_group
    
    st.markdown("---")
    st.subheader("Automatically Calculated Importance Group")
    
    st.success(f"**Importance Group:** {auto_importance_group} (Factor: {auto_importance_factor})")
    st.info("The importance group is automatically determined based on the selected soil type per ISIRI 2800.")
    
    # Display selected factors
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Soil Type", selected_soil)
    with col2:
        st.metric("Soil Factor", soil_types[selected_soil]['group_factor'])
    with col3:
        st.metric("Importance Factor", auto_importance_factor)
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 8: Carousel Orientation ===
elif st.session_state.step == 8:
    st.header("Step 8: Carousel Orientation Selection")
    st.markdown("**Wind direction analysis per AS 1170.4-2007(A1), EN 1991-1-4:2005**")
    st.markdown("---")
    
    wind_direction = st.session_state.environment_data.get('wind_direction', 'North')
    land_length = st.session_state.environment_data.get('land_length', 100)
    land_width = st.session_state.environment_data.get('land_width', 100)
    diameter = st.session_state.diameter
    
    st.subheader(f"Suggested Orientation Based on Wind Direction: {wind_direction}")
    st.info(f"Based on the prevailing wind direction ({wind_direction}), we recommend orienting the carousel in the same direction for optimal wind load distribution.")
    
    fig_orientation = create_orientation_diagram(wind_direction, land_length, land_width, diameter)
    st.plotly_chart(fig_orientation, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm Suggested Orientation", type="primary"):
            st.session_state.carousel_orientation = wind_direction
            st.session_state.orientation_confirmed = True
            st.success(f"Orientation confirmed: {wind_direction}")
    
    with col2:
        st.markdown("**Or select custom orientation:**")
    
    directions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
    custom_direction = st.selectbox("Custom Direction", options=directions, 
                                    index=directions.index(wind_direction) if wind_direction in directions else 0, 
                                    key="custom_orientation_select")
    
    if st.button("Set Custom Orientation"):
        st.session_state.carousel_orientation = custom_direction
        st.session_state.orientation_confirmed = True
        st.success(f"Custom orientation set: {custom_direction}")
        fig_custom = create_orientation_diagram(custom_direction, land_length, land_width, diameter)
        st.plotly_chart(fig_custom, use_container_width=True)
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 9: Device Classification ===
elif st.session_state.step == 9:
    st.header("Step 9: Device Classification")
    st.markdown("**Calculation per INSO 8987-1-2023**")
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
    
    st.subheader("Braking Acceleration Parameter")
    braking_accel = st.number_input("Braking Acceleration (m/s²)", min_value=0.01, max_value=2.0, 
                                    value=st.session_state.braking_acceleration, step=0.01, format="%.2f", 
                                    key="braking_accel_input")
    st.session_state.braking_acceleration = braking_accel
    
    st.markdown("---")
    st.subheader("Design Case Analysis")
    st.markdown("**Design parameters:** Speed = 1 rpm, Braking acceleration = 0.7 m/s²")
    
    omega_design = 1.0 * (2.0 * np.pi / 60.0)
    a_brake_design = 0.7
    
    p_design, n_design, max_accel_design = calculate_dynamic_product(diameter, height, omega_design, a_brake_design)
    class_design = classify_device(p_design)
    
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
    
    p_actual, n_actual, max_accel_actual = calculate_dynamic_product(diameter, height, angular_velocity, braking_accel)
    class_actual = classify_device(p_actual)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Max Acceleration", f"{max_accel_actual:.3f} m/s²")
        st.caption(f"({n_actual:.3f}g)")
    with col2:
        st.metric("Dynamic Product (p)", f"{p_actual:.2f}")
    with col3:
        st.metric("Device Class (Actual)", f"Class {class_actual}")
    
    st.session_state.classification_data = {
        'p_design': p_design, 'class_design': class_design, 'max_accel_design': max_accel_design, 'n_design': n_design,
        'p_actual': p_actual, 'class_actual': class_actual, 'max_accel_actual': max_accel_actual, 'n_actual': n_actual
    }
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 10: Restraint Type (Both ISO and AS Standards) ===
elif st.session_state.step == 10:
    st.header("Step 10: Restraint Type Determination")
    st.markdown("**ISO 17842-2023 & AS 3533.1-2009+A1-2011**")
    st.markdown("---")

    diameter = st.session_state.diameter
    rotation_time_min = st.session_state.rotation_time_min
    braking_accel = st.session_state.braking_acceleration
    
    if rotation_time_min and rotation_time_min > 0:
        rotation_time_sec = rotation_time_min * 60.0
        angular_velocity = 2.0 * np.pi / rotation_time_sec
    else:
        angular_velocity = 0.0
    
    st.subheader("Passenger Acceleration Analysis")
    
    theta_vals = np.linspace(0, 2*np.pi, 360)
    max_ax = -float('inf')
    max_az = -float('inf')
    min_ax = float('inf')
    min_az = float('inf')
    restraint_districts_iso = []
    restraint_zones_as = []
    
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel)
        a_x_g = a_x / 9.81
        a_z_g = a_z / 9.81
        
        if a_x_g > max_ax:
            max_ax = a_x_g
        if a_z_g > max_az:
            max_az = a_z_g
        if a_x_g < min_ax:
            min_ax = a_x_g
        if a_z_g < min_az:
            min_az = a_z_g
        
        district_iso = determine_restraint_area_iso(a_x_g, a_z_g)
        restraint_districts_iso.append(district_iso)
        
        zone_as = determine_restraint_area_as(a_x_g, a_z_g)
        restraint_zones_as.append(zone_as)
    
    from collections import Counter
    district_counts_iso = Counter(restraint_districts_iso)
    predominant_district_iso = district_counts_iso.most_common(1)[0][0]
    
    zone_counts_as = Counter(restraint_zones_as)
    predominant_zone_as = zone_counts_as.most_common(1)[0][0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Max ax", f"{max_ax:.3f}g")
    with col2:
        st.metric("Min ax", f"{min_ax:.3f}g")
    with col3:
        st.metric("Max az", f"{max_az:.3f}g")
    with col4:
        st.metric("Min az", f"{min_az:.3f}g")
    
    st.markdown("---")
    
    # ISO Standard Results
    st.subheader("📋 ISO 17842-2023 Analysis")
    
    restraint_descriptions_iso = {
        1: "District 1 - Upper region: Maximum restraint required (full body harness)",
        2: "District 2 - Upper-central: Enhanced restraint (over-shoulder restraint)",
        3: "District 3 - Central edges: Standard restraint (lap bar or seat belt)",
        4: "District 4 - Lower-central: Moderate restraint (seat belt with lap bar)",
        5: "District 5 - Lower region: Special consideration required (enhanced harness system)"
    }
    
    st.success(f"**Predominant District (ISO):** {predominant_district_iso}")
    st.info(f"**Recommended Restraint (ISO):** {restraint_descriptions_iso.get(predominant_district_iso, 'Standard restraint')}")
    
    # AS Standard Results
    st.markdown("---")
    st.subheader("📋 AS 3533.1-2009+A1-2011 Analysis")
    
    restraint_descriptions_as = {
        1: "Region 1 - Upper region: Maximum restraint required (full body harness)",
        2: "Zone 2 - Upper-central: Enhanced restraint (over-shoulder restraint)",
        3: "Zone 3 - Central region: Standard restraint (lap bar or seat belt)",
        4: "Zone 4 - Lower-central: Moderate restraint (seat belt with lap bar)",
        5: "Zone 5 - Lower region: Special consideration required (enhanced harness system)"
    }
    
    st.success(f"**Predominant Zone (AS):** {predominant_zone_as}")
    st.info(f"**Recommended Restraint (AS):** {restraint_descriptions_as.get(predominant_zone_as, 'Standard restraint')}")
    
    st.markdown("---")
    
    # Display both diagrams side by side
    col_iso, col_as = st.columns(2)
    
    with col_iso:
        st.subheader("ISO 17842 Acceleration Envelope")
        fig_accel_iso = plot_acceleration_envelope_iso(diameter, angular_velocity, braking_accel)
        st.plotly_chart(fig_accel_iso, use_container_width=True)
        
        st.markdown("""
        **ISO District Classifications:**
        - **District 1** (Purple): Maximum restraint
        - **District 2** (Orange): Enhanced restraint
        - **District 3** (Yellow): Standard restraint
        - **District 4** (Green): Moderate restraint
        - **District 5** (Red): Special consideration
        """)
    
    with col_as:
        st.subheader("AS 3533.1 Acceleration Envelope")
        fig_accel_as = plot_acceleration_envelope_as(diameter, angular_velocity, braking_accel)
        st.plotly_chart(fig_accel_as, use_container_width=True)
        
        st.markdown("""
        **AS Zone Classifications:**
        - **Region 1** (Purple): Maximum restraint
        - **Zone 2** (Orange): Enhanced restraint
        - **Zone 3** (Yellow): Standard restraint
        - **Zone 4** (Green): Moderate restraint
        - **Zone 5** (Red): Special consideration
        """)
    
    st.session_state.classification_data.update({
        'restraint_district_iso': predominant_district_iso,
        'restraint_zone_as': predominant_zone_as,
        'max_ax_g': max_ax,
        'max_az_g': max_az,
        'min_ax_g': min_ax,
        'min_az_g': min_az,
        'restraint_description_iso': restraint_descriptions_iso.get(predominant_district_iso, 'Standard restraint'),
        'restraint_description_as': restraint_descriptions_as.get(predominant_zone_as, 'Standard restraint')
    })
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 11: Final Design Overview ===
elif st.session_state.step == 11:
    st.header("Step 11: Complete Design Summary")
    st.markdown("---")

    # Basic Parameters
    st.subheader("🎡 Basic Design Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Generation:** {st.session_state.generation_type}")
        st.write(f"**Diameter:** {st.session_state.diameter} m")
        st.write(f"**Height:** {st.session_state.diameter * 1.1:.1f} m")
    with col2:
        st.write(f"**Total Cabins:** {st.session_state.num_cabins}")
        st.write(f"**VIP Cabins:** {st.session_state.num_vip_cabins}")
        st.write(f"**Cabin Capacity:** {st.session_state.cabin_capacity} passengers")
    with col3:
        if st.session_state.cabin_geometry:
            st.write(f"**Cabin Geometry:** {st.session_state.cabin_geometry}")
        st.write(f"**Rotation Time:** {st.session_state.rotation_time_min:.2f} min")
        cap_hour = calculate_capacity_per_hour_from_time(st.session_state.num_cabins, st.session_state.cabin_capacity,
                                                          st.session_state.num_vip_cabins, st.session_state.rotation_time_min)
        st.write(f"**Capacity/Hour:** {cap_hour:.0f} pax/hr")

    st.markdown("---")
    
    # Environment & Site Conditions
    st.subheader("🌍 Environment & Site Conditions")
    st.caption("Per AS 1170.4-2007(A1), EN 1991-1-4:2005, ISIRI 2800")
    env = st.session_state.environment_data
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Province:** {env.get('province','N/A')}")
        st.write(f"**Region:** {env.get('region_name','N/A')}")
        st.write(f"**Land Area:** {env.get('land_area',0):.2f} m²")
        st.write(f"**Altitude:** {env.get('altitude',0)} m")
        st.write(f"**Temperature Range:** {env.get('temp_min',0)}°C to {env.get('temp_max',0)}°C")
    with col2:
        st.write(f"**Terrain Category:** {env.get('terrain_category','N/A')}")
        st.write(f"**z₀:** {env.get('terrain_z0','N/A')} m")
        st.write(f"**z_min:** {env.get('terrain_zmin','N/A')} m")
        st.write(f"**Seismic Hazard (ISIRI 2800):** {env.get('seismic_hazard','N/A')}")
        st.write(f"**Wind Direction:** {env.get('wind_direction','N/A')}")
        st.write(f"**Max Wind Speed:** {env.get('wind_max',0)} km/h")

    st.markdown("---")
    
    # Soil & Importance
    st.subheader("🏗️ Soil & Structural Importance")
    st.caption("Per ISIRI 2800 (4th Edition)")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Soil Type:** {st.session_state.soil_type}")
    with col2:
        st.write(f"**Importance Group:** {st.session_state.importance_group}")

    st.markdown("---")
    
    # Orientation
    st.subheader("🧭 Carousel Orientation")
    st.caption("Per AS 1170.4-2007(A1), EN 1991-1-4:2005")
    st.write(f"**Selected Orientation:** {st.session_state.carousel_orientation}")
    fig_final_orientation = create_orientation_diagram(
        st.session_state.carousel_orientation,
        env.get('land_length'),
        env.get('land_width'),
        st.session_state.diameter
    )
    st.plotly_chart(fig_final_orientation, use_container_width=True)

    st.markdown("---")
    
    # Safety Classification
    st.subheader("⚠️ Safety Classification")
    st.caption("Per INSO 8987-1-2023")
    if st.session_state.classification_data:
        class_data = st.session_state.classification_data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Design Class", f"Class {class_data.get('class_design','N/A')}")
            st.caption(f"Dynamic Product: {class_data.get('p_design',0):.2f}")
        with col2:
            st.metric("Actual Class", f"Class {class_data.get('class_actual','N/A')}")
            st.caption(f"Dynamic Product: {class_data.get('p_actual',0):.2f}")
        with col3:
            st.metric("Max Acceleration", f"{class_data.get('n_actual',0):.3f}g")
            st.caption("Actual operation")
        
        st.markdown("---")
        st.subheader("🔒 Restraint System Requirements")
        col_iso, col_as = st.columns(2)
        with col_iso:
            st.info(f"**ISO 17842-2023**\n\nDistrict {class_data.get('restraint_district_iso','N/A')}\n\n{class_data.get('restraint_description_iso', 'N/A')}")
        with col_as:
            st.info(f"**AS 3533.1-2009+A1-2011**\n\nZone {class_data.get('restraint_zone_as','N/A')}\n\n{class_data.get('restraint_description_as', 'N/A')}")

    st.markdown("---")
    
    # Visualization
    st.subheader("📊 Design Visualization")
    height = st.session_state.diameter * 1.1
    vip_cap = max(0, st.session_state.cabin_capacity - 2)
    total_capacity_per_rotation = (st.session_state.num_vip_cabins * vip_cap + 
                                   (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity)

    ang = (2.0 * np.pi) / (st.session_state.rotation_time_min * 60.0) if st.session_state.rotation_time_min else 0.0
    total_mass = st.session_state.num_cabins * st.session_state.cabin_capacity * 80.0
    moment_of_inertia = total_mass * (st.session_state.diameter/2.0)**2
    motor_power = moment_of_inertia * ang**2 / 1000.0 if ang else 0.0

    fig = create_component_diagram(st.session_state.diameter, height, total_capacity_per_rotation, motor_power)
    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})

    st.markdown("---")
    
    # Design Summary Report
    st.subheader("📄 Design Summary Report")
    
    with st.expander("📋 View Complete Design Report"):
        st.markdown(f"""
        ## Ferris Wheel Design Report
        
        ### Project Information
        - **Project Name:** {env.get('region_name', 'N/A')} Ferris Wheel
        - **Location:** {env.get('province', 'N/A')}, Iran
        - **Generation Type:** {st.session_state.generation_type}
        
        ### Structural Parameters
        - **Wheel Diameter:** {st.session_state.diameter} m
        - **Total Height:** {height:.1f} m
        - **Number of Cabins:** {st.session_state.num_cabins}
        - **Cabin Geometry:** {st.session_state.cabin_geometry}
        - **Passenger Capacity per Cabin:** {st.session_state.cabin_capacity}
        - **VIP Cabins:** {st.session_state.num_vip_cabins}
        - **Total Capacity per Hour:** {cap_hour:.0f} passengers
        
        ### Operating Parameters
        - **Rotation Time:** {st.session_state.rotation_time_min:.2f} minutes
        - **Rotational Speed:** {ang * 60.0 / (2.0 * np.pi):.4f} rpm
        - **Linear Speed at Rim:** {ang * (st.session_state.diameter / 2.0):.3f} m/s
        - **Estimated Motor Power:** {motor_power:.1f} kW
        
        ### Site Conditions
        - **Province:** {env.get('province', 'N/A')}
        - **Region:** {env.get('region_name', 'N/A')}
        - **Land Dimensions:** {env.get('land_length', 0)} m × {env.get('land_width', 0)} m
        - **Total Land Area:** {env.get('land_area', 0)} m²
        - **Altitude:** {env.get('altitude', 0)} m above sea level
        - **Temperature Range:** {env.get('temp_min', 0)}°C to {env.get('temp_max', 0)}°C
        
        ### Wind & Environmental Data (AS 1170.4, EN 1991-1-4, ISIRI 2800)
        - **Prevailing Wind Direction:** {env.get('wind_direction', 'N/A')}
        - **Maximum Wind Speed:** {env.get('wind_max', 0)} km/h
        - **Average Wind Speed:** {env.get('wind_avg', 0)} km/h
        - **Terrain Category:** {env.get('terrain_category', 'N/A')}
        - **Roughness Length (z₀):** {env.get('terrain_z0', 'N/A')} m
        - **Minimum Height (z_min):** {env.get('terrain_zmin', 'N/A')} m
        - **Carousel Orientation:** {st.session_state.carousel_orientation}
        
        ### Geotechnical Data (ISIRI 2800)
        - **Soil Type:** {st.session_state.soil_type}
        - **Importance Group:** {st.session_state.importance_group}
        - **Seismic Hazard Level:** {env.get('seismic_hazard', 'N/A')}
        
        ### Safety Classification (INSO 8987-1-2023)
        - **Design Class:** Class {class_data.get('class_design', 'N/A')}
        - **Design Dynamic Product:** {class_data.get('p_design', 0):.2f}
        - **Actual Operating Class:** Class {class_data.get('class_actual', 'N/A')}
        - **Actual Dynamic Product:** {class_data.get('p_actual', 0):.2f}
        - **Maximum Acceleration:** {class_data.get('n_actual', 0):.3f}g
        - **Braking Acceleration:** {st.session_state.braking_acceleration} m/s²
        
        ### Restraint System Requirements
        
        #### ISO 17842-2023 Classification
        - **District:** {class_data.get('restraint_district_iso', 'N/A')}
        - **Requirement:** {class_data.get('restraint_description_iso', 'N/A')}
        - **Acceleration Range:** ax = [{class_data.get('min_ax_g', 0):.3f}g to {class_data.get('max_ax_g', 0):.3f}g], az = [{class_data.get('min_az_g', 0):.3f}g to {class_data.get('max_az_g', 0):.3f}g]
        
        #### AS 3533.1-2009+A1-2011 Classification
        - **Zone:** {class_data.get('restraint_zone_as', 'N/A')}
        - **Requirement:** {class_data.get('restraint_description_as', 'N/A')}
        
        ### Applicable Standards
        - INSO 8987-1-2023 (Safety of amusement rides - General requirements)
        - ISO 17842-2023 (Safety of amusement rides and devices)
        - AS 3533.1-2009+A1-2011 (Design and construction)
        - AS 1170.4-2007(A1) (Wind actions)
        - EN 1991-1-4:2005+A1-2010 (Eurocode - Wind actions)
        - ISIRI 2800 (Seismic resistant design)
        - ISIRI 519 (Design loads for buildings)
        - DIN 18800 (Structural steelwork)
        - EN 1993 (Design of steel structures)
        
        ---
        
        **Note:** This is a preliminary design report. Final engineering calculations, detailed 
        structural analysis, and professional review by licensed engineers are required before 
        construction. All designs must comply with local building codes and regulations.
        """)
    
    st.info("🚧 **Note:** Detailed structural, electrical, and safety analyses require professional engineering consultation.")
    
    st.markdown("---")
    l, m, r = st.columns([1,0.5,1])
    with l:
        st.button("⬅️ Back", on_click=go_back)
    with m:
        st.button("🔄 New Design", on_click=reset_design)
    with r:
        if st.button("📥 Export Report"):
            st.info("Report export functionality - Coming soon!")
    
    st.success("✅ Design Complete! All parameters have been configured.")

# === STEP 12: Additional Analysis (Optional Future Step) ===
elif st.session_state.step == 12:
    st.header("Step 12: Additional Analysis")
    st.markdown("---")
    
    st.info("This step is reserved for future enhancements such as:")
    st.markdown("""
    - Detailed structural load calculations
    - Finite element analysis integration
    - Cost estimation
    - Construction timeline
    - Maintenance schedule
    - Safety inspection checklist
    """)
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back", on_click=go_back)
    with right_col:
        st.button("🔄 New Design", on_click=reset_design)