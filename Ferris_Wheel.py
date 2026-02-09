import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os
import math
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="Ferris Wheel Designer",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Language Support ---
def get_text(key, persian=False):
    """Get text in selected language"""
    texts = {
        # Navigation
        'welcome_title': {'en': "Welcome to Ferris Wheel Designer", 'fa': "به طراح چرخ و فلک خوش آمدید"},
        'step': {'en': "Step", 'fa': "مرحله"},
        'of': {'en': "of", 'fa': "از"},
        'back': {'en': "Back", 'fa': "بازگشت"},
        'next': {'en': "Next", 'fa': "بعدی"},
        'calculate': {'en': "Calculate", 'fa': "محاسبه"},
        'confirm': {'en': "Confirm", 'fa': "تایید"},
        'select': {'en': "Select", 'fa': "انتخاب"},
        
        # Step 0 - Welcome Page
        'welcome_header': {'en': "Welcome to Ferris Wheel Designer", 'fa': "خوش آمدید به طراح چرخ و فلک"},
        'about_title': {'en': "🎯 About This Application", 'fa': "🎯 درباره این نرم‌افزار"},
        'about_intro': {'en': "This comprehensive Ferris Wheel Design Tool assists engineers and designers in creating safe, efficient, and compliant ferris wheel installations. The application guides you through:", 
                       'fa': "این ابزار جامع طراحی چرخ و فلک به مهندسان و طراحان در ایجاد نصب‌های ایمن، کارآمد و مطابق با استانداردهای چرخ و فلک کمک می‌کند. این برنامه شما را در موارد زیر راهنمایی می‌کند"},
        
        'feature_generation': {'en': "**Generation Selection**: Choose from various ferris wheel generations and structural types",
                              'fa': "**انتخاب نسل**: انتخاب از نسل‌ها و انواع سازه‌ای مختلف چرخ و فلک"},
        'feature_cabin': {'en': "**Cabin Configuration**: Design cabin geometry, capacity, and VIP arrangements",
                         'fa': "**پیکربندی کابین**: طراحی هندسه، ظرفیت و آرایش کابین های وی آی پی"},
        'feature_performance': {'en': "**Performance Analysis**: Calculate rotation times, speeds, and passenger capacity",
                               'fa': "**تحلیل عملکرد**: محاسبه زمان چرخش، سرعت‌ها و ظرفیت مسافری"},
        'feature_environment': {'en': "**Environmental Assessment**: Analyze site conditions, wind loads, and terrain parameters",
                               'fa': "**ارزیابی محیطی**: تحلیل شرایط سایت، بارهای باد و پارامترهای زمین"},
        'feature_safety': {'en': "**Safety Classification**: Determine device class and restraint requirements",
                          'fa': "**طبقه‌بندی ایمنی**: تعیین کلاس دستگاه و الزامات مهاربند"},
        'feature_structural': {'en': "**Structural Design**: Generate comprehensive design specifications",
                              'fa': "**طراحی سازه**: تولید مشخصات کامل طراحی"},
        
        'standards_title': {'en': "📋 Design Standards & References", 'fa': "📋 استانداردها و مراجع طراحی"},
        'standards_intro': {'en': "This application implements calculations and requirements based on the following international and national standards:",
                           'fa': "این نرم‌افزار محاسبات و الزامات را بر اساس استانداردهای بین‌المللی و ملی زیر پیاده‌سازی می‌کند"},
        
        # Standards Headers
        'standards_current': {'en': "#### Current Standards for Amusement Devices:", 'fa': "#### استانداردهای فعلی برای وسایل تفریحی"},
        'standards_legacy': {'en': "#### Legacy Standards (Reference):", 'fa': "#### استانداردهای قدیمی (مرجع)"},
        'standards_loads': {'en': "#### Standards for Load Analysis:", 'fa': "#### استانداردهای تحلیل بار"},
        'standards_applications': {'en': "#### Key Application Areas:", 'fa': "#### حوزه‌های کاربردی کلیدی"},
        
        # Application Areas
        'app_wind': {'en': "**Wind Load Analysis**: AS 1170.4, EN 1991-1-4, ISIRI 2800",
                    'fa': "**تحلیل بار باد**: AS 1170.4، EN 1991-1-4، ISIRI 2800"},
        'app_seismic': {'en': "**Seismic Analysis**: ISIRI 2800",
                       'fa': "**تحلیل لرزه‌ای**: ISIRI 2800"},
        'app_structural': {'en': "**Structural Design**: DIN 18800, EN 1993",
                          'fa': "**طراحی سازه**: DIN 18800، EN 1993"},
        'app_safety': {'en': "**Safety Classification**: INSO 8987, ISO 17842",
                      'fa': "**طبقه‌بندی ایمنی**: INSO 8987، ISO 17842"},
        
        # Warning
        'warning_title': {'en': "⚠️ **Important Notice:**", 'fa': "⚠️ **اطلاعیه مهم:**"},
        'warning_intro': {'en': "By proceeding, you acknowledge that:", 'fa': "با ادامه، شما تأیید می‌کنید که"},
        'warning_1': {'en': "This tool provides preliminary design calculations based on the referenced standards",
                     'fa': "این ابزار محاسبات طراحی اولیه را بر اساس استانداردهای ذکر شده ارائه می‌دهد"},
        'warning_2': {'en': "Final designs must be reviewed and approved by licensed professional engineers",
                     'fa': "طرح‌های نهایی باید توسط مهندسان حرفه‌ای دارای مجوز بررسی و تأیید شوند"},
        'warning_3': {'en': "Local building codes and regulations must be consulted and followed",
                     'fa': "آیین‌نامه‌ها و مقررات ساختمانی محلی باید مشورت و رعایت شوند"},
        'warning_4': {'en': "Site-specific conditions may require additional analysis beyond this tool's scope",
                     'fa': "شرایط خاص سایت ممکن است نیاز به تحلیل اضافی فراتر از محدوده این ابزار داشته باشد"},
        'warning_5': {'en': "The designer assumes responsibility for verifying all calculations and compliance",
                     'fa': "طراح مسئولیت تأیید تمام محاسبات و انطباق را بر عهده دارد"},
        
        # Confirmation
        'confirm_checkbox': {'en': "✅ I understand and accept that all calculations are based on the standards listed above, and I will ensure compliance with local regulations and professional engineering review.",
                            'fa': "✅ من درک می‌کنم و می‌پذیرم که تمام محاسبات بر اساس استانداردهای فهرست شده در بالا هستند و من انطباق با مقررات محلی و بررسی مهندسی حرفه‌ای را تضمین خواهم کرد."},
        'confirm_success': {'en': "✅ Standards confirmed. You may proceed to the design process.",
                           'fa': "✅ استانداردها تأیید شدند. می‌توانید به فرآیند طراحی ادامه دهید."},
        'confirm_info': {'en': "Please confirm your understanding of the standards to continue.",
                        'fa': "لطفاً درک خود از استانداردها را برای ادامه تأیید کنید."},
        'start_button': {'en': "🚀 Start Design Process", 'fa': "🚀 شروع فرآیند طراحی"},
        
        # Step 1 - Generation Selection
        'select_generation': {'en': "Select Ferris Wheel Generation", 'fa': "انتخاب نسل چرخ و فلک"},
        'gen_1_truss': {'en': "1st Generation (Truss type)", 'fa': "نسل اول (نوع خرپایی)"},
        'gen_2_cable': {'en': "2nd Generation_1st type (Cable type)", 'fa': "نسل دوم - نوع اول (کابلی)"},
        'gen_2_pure_cable': {'en': "2nd Generation_2nd type (Pure cable type)", 'fa': "نسل دوم - نوع دوم (کاملاً کابلی)"},
        'gen_4_hubless': {'en': "4th Generation (Hubless centerless)", 'fa': "نسل چهارم (بدون مرکز)"},
        
        # Step 2 - Cabin Geometry
        'select_cabin_geometry': {'en': "Select Cabin Geometry", 'fa': "انتخاب هندسه کابین"},
        'cabin_geometry_instruction': {'en': "Choose a cabin shape.", 'fa': "یک شکل کابین انتخاب کنید."},
        'geom_square': {'en': "Square", 'fa': "مربعی"},
        'geom_vert_cyl': {'en': "Vertical Cylinder", 'fa': "استوانه عمودی"},
        'geom_horiz_cyl': {'en': "Horizontal Cylinder", 'fa': "استوانه افقی"},
        'geom_spherical': {'en': "Spherical", 'fa': "کروی"},
        'geom_spherical_caption': {'en': "This option is more expensive but has a better appearance.", 
                                  'fa': "این گزینه گران‌تر است اما جلوه‌ی ظاهری بهتری دارد"},
        
        # Step 3 - Primary Parameters
        'cabin_specification': {'en': "Cabin Specification", 'fa': "مشخصات کابین"},
        'diameter_label': {'en': "Ferris Wheel Diameter (m)", 'fa': "قطر چرخ و فلک (متر)"},
        'num_cabins_label': {'en': "Number of Cabins", 'fa': "تعداد کابین‌ها"},
        'cabin_cap_label': {'en': "Cabin Capacity (passengers per cabin)", 'fa': "ظرفیت کابین (مسافر به ازای هر کابین)"},
        'num_vip_label': {'en': "Number of VIP Cabins", 'fa': "تعداد کابین‌های VIP"},
        'calc_capacities': {'en': "🔄 Calculate Capacities", 'fa': "🔄 محاسبه ظرفیت‌ها"},
        'per_rotation_capacity': {'en': "Per-rotation capacity", 'fa': "ظرفیت به ازای هر دور"},
        'vip_capacity': {'en': "VIP capacity (per rotation)", 'fa': "ظرفیت VIP (به ازای هر دور)"},
        'passengers': {'en': "passengers", 'fa': "مسافر"},
        'each_vip': {'en': "each VIP:", 'fa': "هر VIP:"},
        'capacities_calculated': {'en': "Capacities calculated.", 'fa': "ظرفیت‌ها محاسبه شدند."},
        
        # Step 4 - Rotation Time
        'rotation_time': {'en': "Rotation Time & Derived Speeds", 'fa': "زمان چرخش و سرعت‌های مشتق شده"},
        'rotation_time_instruction': {'en': "Enter the rotation time or select target capacity per hour",
                                     'fa': "زمان چرخش را وارد کنید یا ظرفیت هدف در ساعت را انتخاب کنید"},
        'rotation_time_label': {'en': "Rotation Time (minutes)", 'fa': "زمان چرخش (دقیقه)"},
        'capacity_per_hour': {'en': "Capacity per Hour (pax/hr)", 'fa': "ظرفیت در ساعت (مسافر/ساعت)"},
        'angular_velocity': {'en': "Angular Velocity", 'fa': "سرعت زاویه‌ای"},
        'linear_velocity': {'en': "Linear Velocity at Rim", 'fa': "سرعت خطی در لبه"},
        'rotation_speed': {'en': "Rotation Speed", 'fa': "سرعت چرخش"},
        
        # Step 5 - Environment
        'environment_conditions': {'en': "Environment Conditions", 'fa': "شرایط محیطی"},
        'select_province': {'en': "Select Province", 'fa': "انتخاب استان"},
        'select_city': {'en': "Select City", 'fa': "انتخاب شهر"},
        'region_name': {'en': "Region / Area name", 'fa': "نام منطقه / ناحیه"},
        'land_dimensions': {'en': "Land Dimensions", 'fa': "ابعاد زمین"},
        'land_length': {'en': "Land Length (m)", 'fa': "طول زمین (متر)"},
        'land_width': {'en': "Land Width (m)", 'fa': "عرض زمین (متر)"},
        'altitude': {'en': "Altitude (m above sea level)", 'fa': "ارتفاع (متر از سطح دریا)"},
        'temp_range': {'en': "Temperature Range", 'fa': "محدوده دما"},
        'min_temp': {'en': "Minimum Temperature (°C)", 'fa': "حداقل دما (°C)"},
        'max_temp': {'en': "Maximum Temperature (°C)", 'fa': "حداکثر دما (°C)"},
        
        # Step 6 - Provincial
        'provincial_characteristics': {'en': "Provincial Characteristics & Terrain Parameters", 'fa': "ویژگی‌های استانی و پارامترهای زمین"},
        'zone': {'en': "Zone", 'fa': "منطقه"},
        'terrain_category': {'en': "Terrain Category", 'fa': "دسته‌بندی زمین"},
        'wind_direction': {'en': "Prevailing Wind Direction", 'fa': "جهت غالب باد"},
        'avg_wind_speed': {'en': "Average Wind Speed (km/h)", 'fa': "سرعت متوسط باد (کیلومتر در ساعت)"},
        'max_wind_speed': {'en': "Maximum Wind Speed (km/h)", 'fa': "حداکثر سرعت باد (کیلومتر در ساعت)"},
        'seismic_hazard': {'en': "Seismic Hazard Level", 'fa': "سطح خطر لرزه‌ای"},
        
        # Step 7 - Soil Type
        'soil_type': {'en': "Soil Type & Importance Classification", 'fa': "نوع خاک و طبقه‌بندی اهمیت"},
        'select_soil': {'en': "Select Soil Type", 'fa': "انتخاب نوع خاک"},
        'select_importance': {'en': "Select Importance Group", 'fa': "انتخاب گروه اهمیت"},
        
        # Step 8 - Orientation
        'carousel_orientation': {'en': "Carousel Orientation Selection", 'fa': "انتخاب جهت‌گیری چرخ و فلک"},
        'suggested_orientation': {'en': "Suggested Orientation (perpendicular to wind)", 'fa': "جهت پیشنهادی (عمود بر باد)"},
        'confirm_orientation': {'en': "Confirm Suggested Orientation", 'fa': "تایید جهت پیشنهادی"},
        'custom_direction': {'en': "Custom Direction", 'fa': "جهت سفارشی"},
        'north_south': {'en': "North-South", 'fa': "شمال-جنوب"},
        'east_west': {'en': "East-West", 'fa': "شرق-غرب"},
        'northeast_southwest': {'en': "Northeast-Southwest", 'fa': "شمال شرقی-جنوب غربی"},
        'southeast_northwest': {'en': "Southeast-Northwest", 'fa': "جنوب شرقی-شمال غربی"},
        
        # Step 9 - Classification
        'device_classification': {'en': "Device Classification", 'fa': "طبقه‌بندی دستگاه"},
        'calc_per_standard': {'en': "**Calculation per INSO 8987-1-2023**", 'fa': "**محاسبه طبق INSO 8987-1-2023**"},
        'braking_accel_param': {'en': "Braking Acceleration Parameter", 'fa': "پارامتر شتاب ترمز"},
        'braking_accel': {'en': "Braking Acceleration (m/s²)", 'fa': "شتاب ترمز (m/s²)"},
        'braking_accel_actual': {'en': "Braking Acceleration (m/s²) - Actual Operation", 'fa': "شتاب ترمز (m/s²) - عملیات واقعی"},
        'additional_loads': {'en': "Additional Load Factors", 'fa': "بارهای اضافی"},
        'snow_load': {'en': "Snow Load", 'fa': "بار برف"},
        'wind_load': {'en': "Wind Load", 'fa': "بار باد"},
        'earthquake_load': {'en': "Earthquake Load", 'fa': "بار زلزله"},
        'design_case': {'en': "Design Case Analysis", 'fa': "تحلیل حالت طراحی"},
        'actual_operation': {'en': "Actual Operation Analysis", 'fa': "تحلیل عملیات واقعی"},
        'max_acceleration': {'en': "Max Acceleration", 'fa': "حداکثر شتاب"},
        'dynamic_product': {'en': "Dynamic Product (p)", 'fa': "حاصل‌ضرب دینامیکی (p)"},
        'device_class': {'en': "Device Class", 'fa': "کلاس دستگاه"},
        'load_contributions': {'en': "Additional Load Contributions", 'fa': "مشارکت بارهای اضافی"},
        
        # Step 10 - Restraint
        'restraint_type': {'en': "Restraint Type Determination", 'fa': "تعیین نوع مهاربند"},
        
        # Step 11 - Summary
        'design_summary': {'en': "Complete Design Summary", 'fa': "خلاصه کامل طراحی"},
        'basic_params': {'en': "🎡 Basic Design Parameters", 'fa': "🎡 پارامترهای پایه طراحی"},
        'generation': {'en': "Generation", 'fa': "نسل"},
        'diameter': {'en': "Diameter", 'fa': "قطر"},
        'height': {'en': "Height", 'fa': "ارتفاع"},
        'total_cabins': {'en': "Total Cabins", 'fa': "کل کابین‌ها"},
        'vip_cabins': {'en': "VIP Cabins", 'fa': "کابین‌های VIP"},
        'cabin_capacity': {'en': "Cabin Capacity", 'fa': "ظرفیت کابین"},
        'cabin_geometry': {'en': "Cabin Geometry", 'fa': "هندسه کابین"},
        'rotation_time_min': {'en': "Rotation Time", 'fa': "زمان چرخش"},
        'capacity_hour': {'en': "Capacity/Hour", 'fa': "ظرفیت/ساعت"},
        'env_site_conditions': {'en': "🌍 Environment & Site Conditions", 'fa': "🌍 شرایط محیطی و سایت"},
        'province': {'en': "Province", 'fa': "استان"},
        'city': {'en': "City", 'fa': "شهر"},
        'region': {'en': "Region", 'fa': "منطقه"},
        'land_area': {'en': "Land Area", 'fa': "مساحت زمین"},
        'temp_range_display': {'en': "Temperature Range", 'fa': "محدوده دما"},
        'soil_importance': {'en': "🏗️ Soil & Structural Importance", 'fa': "🏗️ خاک و اهمیت سازه"},
        'orientation_title': {'en': "🧭 Carousel Orientation", 'fa': "🧭 جهت‌گیری چرخ و فلک"},
        'selected_orientation': {'en': "Selected Orientation", 'fa': "جهت‌گیری انتخاب شده"},
        'safety_classification': {'en': "⚠️ Safety Classification", 'fa': "⚠️ طبقه‌بندی ایمنی"},
        'design_class': {'en': "Design Class", 'fa': "کلاس طراحی"},
        'actual_class': {'en': "Actual Class", 'fa': "کلاس واقعی"},
        'restraint_requirements': {'en': "🔒 Restraint System Requirements", 'fa': "🔒 الزامات سیستم مهاربند"},
        'motor_drive': {'en': "⚙️ Motor & Drive System", 'fa': "⚙️ سیستم موتور و درایو"},
        'rated_power': {'en': "Rated Power", 'fa': "توان نامی"},
        'peak_power': {'en': "Peak Power", 'fa': "توان پیک"},
        'operational_power': {'en': "Operational", 'fa': "توان عملیاتی"},
        'total_mass': {'en': "Total Mass", 'fa': "جرم کل"},
        'design_viz': {'en': "📊 Design Visualization", 'fa': "📊 تصویرسازی طراحی"},
        'design_report': {'en': "📄 Design Summary Report", 'fa': "📄 گزارش خلاصه طراحی"},
        'view_report': {'en': "📋 View Complete Design Report", 'fa': "📋 مشاهده گزارش کامل طراحی"},
        'new_design': {'en': "🔄 New Design", 'fa': "🔄 طراحی جدید"},
        'export_report': {'en': "📥 Export Report", 'fa': "📥 خروجی گزارش"},
        'design_complete': {'en': "✅ Design Complete! All parameters have been configured.", 
                           'fa': "✅ طراحی کامل شد! تمام پارامترها تنظیم شده‌اند."},
        'export_coming_soon': {'en': "Report export functionality - Coming soon!", 
                              'fa': "قابلیت خروجی گزارش - به زودی!"},
        'professional_note': {'en': "🚧 **Note:** Detailed structural, electrical, and safety analyses require professional engineering consultation.",
                             'fa': "🚧 **توجه:** تحلیل‌های دقیق سازه‌ای، الکتریکی و ایمنی نیازمند مشاوره مهندسی حرفه‌ای هستند."},
    }
    return texts.get(key, {}).get('fa' if persian else 'en', key)

# --- Session State Initialization ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'persian' not in st.session_state:
    st.session_state.persian = False
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
if 'language_set' not in st.session_state:
    st.session_state.language_set = False
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True

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

# City data with seismic hazard levels
CITIES_DATA = {
    "Khuzestan": [
        {"city": "Abadan", "hazard": "Low"},
        {"city": "Aghajari", "hazard": "High"},
        {"city": "Omidiyeh", "hazard": "High"},
        {"city": "Andimeshk", "hazard": "High"},
        {"city": "Izeh", "hazard": "High"},
        {"city": "Ahvaz", "hazard": "High"},
        {"city": "Baghmalk", "hazard": "High"},
        {"city": "Bandar Imam Khomeini", "hazard": "High"},
        {"city": "Bandar Mahshahr", "hazard": "High"},
        {"city": "Bastan", "hazard": "High"},
        {"city": "Behbahan", "hazard": "High"},
        {"city": "Khorramshahr", "hazard": "Low"},
        {"city": "Dezful", "hazard": "High"},
        {"city": "Dehdez", "hazard": "High"},
        {"city": "Ramshir", "hazard": "High"},
        {"city": "Ramhormoz", "hazard": "High"},
        {"city": "Sarbandar", "hazard": "Low"},
        {"city": "Shadegan", "hazard": "Low"},
        {"city": "Shahr-e Stan", "hazard": "Moderate"},
        {"city": "Shush", "hazard": "High"},
        {"city": "Shushtar", "hazard": "High"},
        {"city": "Sosangerd", "hazard": "High"},
        {"city": "Hamidiyeh", "hazard": "High"},
        {"city": "Haftgel", "hazard": "High"},
        {"city": "Hendijan", "hazard": "High"},
        {"city": "Hovizeh", "hazard": "High"},
        {"city": "Masjed Soleyman", "hazard": "Very High"},
        {"city": "Mollasani", "hazard": "High"},
        {"city": "Lali", "hazard": "High"},
    ],
    "Ilam": [
        {"city": "Abdanan", "hazard": "High"},
        {"city": "Ilam", "hazard": "High"},
        {"city": "Ivan", "hazard": "High"},
        {"city": "Darreh Shahr", "hazard": "High"},
        {"city": "Dashte Abbas", "hazard": "High"},
        {"city": "Dehloran", "hazard": "High"},
        {"city": "Mehran", "hazard": "High"},
        {"city": "Malekshahi", "hazard": "High"},
        {"city": "Musian", "hazard": "High"},
    ],
    "Fars": [
        {"city": "Abadeh", "hazard": "High"},
        {"city": "Arsanjan", "hazard": "Moderate"},
        {"city": "Eqlid", "hazard": "High"},
        {"city": "Estahban", "hazard": "High"},
        {"city": "Behrestān", "hazard": "High"},
        {"city": "Khavaran", "hazard": "High"},
        {"city": "Kharameh", "hazard": "High"},
        {"city": "Khonj", "hazard": "High"},
        {"city": "Darab", "hazard": "High"},
        {"city": "Dehbid", "hazard": "High"},
        {"city": "Zarqan", "hazard": "High"},
        {"city": "Safashahr", "hazard": "High"},
        {"city": "Sepidan", "hazard": "High"},
        {"city": "Surian", "hazard": "High"},
        {"city": "Shiraz", "hazard": "High"},
        {"city": "Farashband", "hazard": "High"},
        {"city": "Fasa", "hazard": "High"},
        {"city": "Firuzabad", "hazard": "High"},
        {"city": "Qaderabad", "hazard": "High"},
        {"city": "Qir", "hazard": "High"},
        {"city": "Kazerun", "hazard": "High"},
        {"city": "Kavar", "hazard": "High"},
        {"city": "Gerash", "hazard": "High"},
        {"city": "Lar", "hazard": "High"},
        {"city": "Lamerd", "hazard": "High"},
        {"city": "Marvdasht", "hazard": "High"},
        {"city": "Mehr", "hazard": "High"},
        {"city": "Neyriz", "hazard": "High"},
        {"city": "Nourabad", "hazard": "High"},
        {"city": "Jahrom", "hazard": "High"},
    ],
    "Qazvin": [
        {"city": "Ab-e Garm", "hazard": "High"},
        {"city": "Abyek", "hazard": "Very High"},
        {"city": "Avaj", "hazard": "High"},
        {"city": "Buin Zahra", "hazard": "Very High"},
        {"city": "Takestan", "hazard": "High"},
        {"city": "Qazvin", "hazard": "Very High"},
        {"city": "Moalem Kalayeh", "hazard": "Very High"},
    ],
    "Zanjan": [
        {"city": "Ab Bar", "hazard": "Very High"},
        {"city": "Abhar", "hazard": "High"},
        {"city": "Khorramdarreh", "hazard": "High"},
        {"city": "Zanjan", "hazard": "High"},
        {"city": "Soltaniyeh", "hazard": "High"},
        {"city": "Soltanabad", "hazard": "High"},
        {"city": "Sayin Qaleh", "hazard": "High"},
        {"city": "Qaydar", "hazard": "High"},
        {"city": "Giluwan", "hazard": "Very High"},
        {"city": "Mahneshan", "hazard": "High"},
    ],
    "Hamedan": [
        {"city": "Asadabad", "hazard": "High"},
        {"city": "Bahar", "hazard": "High"},
        {"city": "Tuyserkan", "hazard": "High"},
        {"city": "Razan", "hazard": "High"},
        {"city": "Kabutarāhang", "hazard": "High"},
        {"city": "Malayer", "hazard": "High"},
        {"city": "Nahavand", "hazard": "Very High"},
        {"city": "Hamedan", "hazard": "Very High"},
        {"city": "Famenin", "hazard": "High"},
    ],
    "Markazi": [
        {"city": "Ashtian", "hazard": "High"},
        {"city": "Arak", "hazard": "High"},
        {"city": "Astaneh", "hazard": "High"},
        {"city": "Tafresh", "hazard": "High"},
        {"city": "Khondab", "hazard": "High"},
        {"city": "Khomein", "hazard": "High"},
        {"city": "Delijan", "hazard": "High"},
        {"city": "Zarandieh", "hazard": "High"},
        {"city": "Sarband", "hazard": "High"},
        {"city": "Shazand", "hazard": "High"},
        {"city": "Saveh", "hazard": "High"},
        {"city": "Farmahin", "hazard": "High"},
        {"city": "Komijan", "hazard": "High"},
        {"city": "Mahallat", "hazard": "High"},
        {"city": "Nobaran", "hazard": "High"},
    ],
    "Yazd": [
        {"city": "Abarkuh", "hazard": "High"},
        {"city": "Ardakan", "hazard": "High"},
        {"city": "Bafq", "hazard": "High"},
        {"city": "Behābād", "hazard": "High"},
        {"city": "Taft", "hazard": "High"},
        {"city": "Khor", "hazard": "High"},
        {"city": "Dihuk", "hazard": "Very High"},
        {"city": "Rābat Posht-e Bādām", "hazard": "High"},
        {"city": "Zarch", "hazard": "High"},
        {"city": "Saqand", "hazard": "High"},
        {"city": "Mehriz", "hazard": "High"},
        {"city": "Meybod", "hazard": "High"},
        {"city": "Herat", "hazard": "High"},
        {"city": "Yazd", "hazard": "High"},
        {"city": "Tabas", "hazard": "High"},
        {"city": "Naybandan", "hazard": "Very High"},
    ],
    "Semnan": [
        {"city": "Aradan", "hazard": "High"},
        {"city": "Astaneh", "hazard": "High"},
        {"city": "Damghan", "hazard": "High"},
        {"city": "Sorkheh", "hazard": "High"},
        {"city": "Semnan", "hazard": "High"},
        {"city": "Shahrud", "hazard": "High"},
        {"city": "Absarabad", "hazard": "High"},
        {"city": "Garmsar", "hazard": "High"},
        {"city": "Mehdishahr", "hazard": "High"},
        {"city": "Meyamey", "hazard": "High"},
        {"city": "Shahmirzad", "hazard": "High"},
        {"city": "Ivānkī", "hazard": "High"},
        {"city": "Jām", "hazard": "High"},
        {"city": "Biarjmand", "hazard": "High"},
        {"city": "Bastam", "hazard": "High"},
        {"city": "Tazareh", "hazard": "High"},
        {"city": "Torud", "hazard": "High"},
        {"city": "Forumad", "hazard": "High"},
        {"city": "Mojen", "hazard": "High"},
        {"city": "Moalleman", "hazard": "High"},
    ],
    "Qom": [
        {"city": "Qom", "hazard": "High"},
        {"city": "Solfchegan", "hazard": "High"},
        {"city": "Gazaran", "hazard": "High"},
        {"city": "Kahak", "hazard": "High"},
        {"city": "Kooshk Nosrat", "hazard": "High"},
    ],
    "South Khorasan": [
        {"city": "Birjand", "hazard": "High"},
        {"city": "Tabas Masina", "hazard": "Very High"},
        {"city": "Khosvaf", "hazard": "High"},
        {"city": "Khezri", "hazard": "Very High"},
        {"city": "Dasht Beyaz", "hazard": "Very High"},
        {"city": "Sarayan", "hazard": "Very High"},
        {"city": "Sarbisheh", "hazard": "High"},
        {"city": "Sade", "hazard": "High"},
        {"city": "Shahrukht", "hazard": "Very High"},
        {"city": "Qaen", "hazard": "High"},
        {"city": "Kooli", "hazard": "Very High"},
        {"city": "Nehbandan", "hazard": "High"},
        {"city": "Boshruyeh", "hazard": "High"},
    ],
    "Kerman": [
        {"city": "Anār", "hazard": "High"},
        {"city": "Baft", "hazard": "High"},
        {"city": "Bārdsar", "hazard": "High"},
        {"city": "Bam", "hazard": "High"},
        {"city": "Jiroft", "hazard": "High"},
        {"city": "Rafsanjan", "hazard": "High"},
        {"city": "Ravar", "hazard": "High"},
        {"city": "Rayen", "hazard": "High"},
        {"city": "Zarand", "hazard": "High"},
        {"city": "Sīrjān", "hazard": "High"},
        {"city": "Sirch", "hazard": "Very High"},
        {"city": "Sabz Abad", "hazard": "High"},
        {"city": "Shahdad", "hazard": "High"},
        {"city": "Shahrbabak", "hazard": "High"},
        {"city": "Kerman", "hazard": "High"},
        {"city": "Golbaf", "hazard": "Very High"},
        {"city": "Kahnuj", "hazard": "High"},
        {"city": "Kohbanān", "hazard": "High"},
        {"city": "Kianshahr", "hazard": "High"},
        {"city": "Mahan", "hazard": "High"},
        {"city": "Manujan", "hazard": "High"},
    ],
    "East Azerbaijan": [
        {"city": "Ahar", "hazard": "High"},
        {"city": "Azhdarshur", "hazard": "High"},
        {"city": "Osku", "hazard": "High"},
        {"city": "Bonab", "hazard": "High"},
        {"city": "Bostanābād", "hazard": "Very High"},
        {"city": "Tabriz", "hazard": "Very High"},
        {"city": "Tasuj", "hazard": "Very High"},
        {"city": "Jolfa", "hazard": "High"},
        {"city": "Khajeh", "hazard": "High"},
        {"city": "Sarab", "hazard": "High"},
        {"city": "Shabestar", "hazard": "Very High"},
        {"city": "Sharafkhaneh", "hazard": "Very High"},
        {"city": "Sofian", "hazard": "High"},
        {"city": "Ajab Shir", "hazard": "High"},
        {"city": "Qareh Aghaj", "hazard": "High"},
        {"city": "Kaleybar", "hazard": "Very High"},
        {"city": "Maragheh", "hazard": "High"},
        {"city": "Marand", "hazard": "High"},
        {"city": "Mianeh", "hazard": "Very High"},
        {"city": "Haris", "hazard": "Very High"},
        {"city": "Heris", "hazard": "Very High"},
        {"city": "Hashtrud", "hazard": "Very High"},
        {"city": "Varzaqān", "hazard": "Very High"},
        {"city": "Zonūz", "hazard": "High"},
    ],
    "West Azerbaijan": [
        {"city": "Oshnaviyeh", "hazard": "High"},
        {"city": "Urmia", "hazard": "High"},
        {"city": "Bukan", "hazard": "High"},
        {"city": "Piranshahr", "hazard": "High"},
        {"city": "Takab", "hazard": "High"},
        {"city": "Chaypareh", "hazard": "High"},
        {"city": "Khoy", "hazard": "High"},
        {"city": "Salmas", "hazard": "Very High"},
        {"city": "Sarv", "hazard": "High"},
        {"city": "Sardasht", "hazard": "High"},
        {"city": "Shahin Dezh", "hazard": "High"},
        {"city": "Siyah Cheshmeh", "hazard": "High"},
        {"city": "Showt", "hazard": "High"},
        {"city": "Qarah Zīā od Dīn", "hazard": "High"},
        {"city": "Qotur", "hazard": "Very High"},
        {"city": "Kelisa Kandi", "hazard": "High"},
        {"city": "Maku", "hazard": "Very High"},
        {"city": "Mahābād", "hazard": "Very High"},
        {"city": "Miandoab", "hazard": "Very High"},
        {"city": "Naqadeh", "hazard": "Very High"},
        {"city": "Poldasht", "hazard": "High"},
    ],
    "Ardabil": [
        {"city": "Aslanduz", "hazard": "High"},
        {"city": "Ardabil", "hazard": "High"},
        {"city": "Parsābād", "hazard": "High"},
        {"city": "Beleh Savar", "hazard": "High"},
        {"city": "Khalkhal", "hazard": "High"},
        {"city": "Sarein", "hazard": "High"},
        {"city": "Zaviyeh", "hazard": "High"},
        {"city": "Germi", "hazard": "High"},
        {"city": "Giveh", "hazard": "High"},
        {"city": "Kolur", "hazard": "Very High"},
        {"city": "Meshginshahr", "hazard": "Very High"},
        {"city": "Namin", "hazard": "High"},
        {"city": "Nir", "hazard": "High"},
        {"city": "Hashtjin", "hazard": "Very High"},
        {"city": "Lahrood", "hazard": "High"},
    ],
    "Kurdistan": [
        {"city": "Baneh", "hazard": "High"},
        {"city": "Bijar", "hazard": "High"},
        {"city": "Qorveh", "hazard": "Very High"},
        {"city": "Kamyaran", "hazard": "Very High"},
        {"city": "Marivan", "hazard": "Very High"},
        {"city": "Sanandaj", "hazard": "High"},
        {"city": "Saqez", "hazard": "High"},
        {"city": "Divandarreh", "hazard": "High"},
    ],
    "Kermanshah": [
        {"city": "Eslamābād-e Gharb", "hazard": "High"},
        {"city": "Paveh", "hazard": "High"},
        {"city": "Sarab-e Neelofar", "hazard": "High"},
        {"city": "Bisetun", "hazard": "High"},
        {"city": "Javanrud", "hazard": "High"},
        {"city": "Harsin", "hazard": "Very High"},
        {"city": "Ravansar", "hazard": "High"},
        {"city": "Sar-e Pol-e Zahab", "hazard": "High"},
        {"city": "Songhor", "hazard": "High"},
        {"city": "Sahneh", "hazard": "Very High"},
        {"city": "Somar", "hazard": "High"},
        {"city": "Qasr-e Shirin", "hazard": "Very High"},
        {"city": "Kangavar", "hazard": "Very High"},
        {"city": "Kermanshah", "hazard": "Very High"},
        {"city": "Kerend", "hazard": "Very High"},
        {"city": "Gilan-e Gharb", "hazard": "High"},
        {"city": "Nosoud", "hazard": "High"},
    ],
    "Lorestan": [
        {"city": "Azna", "hazard": "Very High"},
        {"city": "Aleshtar", "hazard": "High"},
        {"city": "Aligudarz", "hazard": "High"},
        {"city": "Borujerd", "hazard": "Very High"},
        {"city": "Poldokhtar", "hazard": "High"},
        {"city": "Khorramabad", "hazard": "High"},
        {"city": "Dorud", "hazard": "Very High"},
        {"city": "Kuhdasht", "hazard": "Very High"},
        {"city": "Mamoun", "hazard": "High"},
        {"city": "Nurābād", "hazard": "High"},
    ],
    "Chaharmahal and Bakhtiari": [
        {"city": "Ardal", "hazard": "High"},
        {"city": "Borūjen", "hazard": "High"},
        {"city": "Boldaji", "hazard": "High"},
        {"city": "Dogoombadan", "hazard": "High"},
        {"city": "Saman", "hazard": "High"},
        {"city": "Sarkhoon", "hazard": "High"},
        {"city": "Shalmazar", "hazard": "High"},
        {"city": "Shahrekord", "hazard": "High"},
        {"city": "Farsan", "hazard": "Very High"},
        {"city": "Koohrang", "hazard": "Very High"},
        {"city": "Gandoman", "hazard": "High"},
        {"city": "Lordegan", "hazard": "High"},
        {"city": "Naghan", "hazard": "High"},
    ],
    "Kohgiluyeh and Boyer-Ahmad": [
        {"city": "Dehdasht", "hazard": "High"},
        {"city": "Dishmuk", "hazard": "High"},
        {"city": "Yasuj", "hazard": "High"},
        {"city": "Gachsaran", "hazard": "High"},
        {"city": "Si Sakhti", "hazard": "High"},
    ],
    "Isfahan": [
        {"city": "Abyaneh", "hazard": "High"},
        {"city": "Ardestan", "hazard": "High"},
        {"city": "Aran", "hazard": "High"},
        {"city": "Isfahan", "hazard": "High"},
        {"city": "Anarak", "hazard": "High"},
        {"city": "Badrud", "hazard": "High"},
        {"city": "Tiran", "hazard": "High"},
        {"city": "Charmhin", "hazard": "High"},
        {"city": "Chadegan", "hazard": "High"},
        {"city": "Dehaqan", "hazard": "High"},
        {"city": "Daran", "hazard": "High"},
        {"city": "Dorche", "hazard": "High"},
        {"city": "Jondoq", "hazard": "High"},
        {"city": "Khur", "hazard": "High"},
        {"city": "Khansar", "hazard": "High"},
        {"city": "Zarrinshahr", "hazard": "High"},
        {"city": "Zvareh", "hazard": "High"},
        {"city": "Zafreh", "hazard": "High"},
        {"city": "Semīrom", "hazard": "High"},
        {"city": "Shahreza", "hazard": "High"},
        {"city": "Shahin Shahr", "hazard": "High"},
        {"city": "Golpayegan", "hazard": "High"},
        {"city": "Kashan", "hazard": "High"},
        {"city": "Kuhpayeh", "hazard": "High"},
        {"city": "Meimeh", "hazard": "High"},
        {"city": "Mobarakeh", "hazard": "High"},
        {"city": "Natanz", "hazard": "High"},
        {"city": "Najaf Abad", "hazard": "High"},
        {"city": "Nain", "hazard": "High"},
        {"city": "Alvandeh", "hazard": "High"},
        {"city": "Fin", "hazard": "High"},
        {"city": "Qomsar", "hazard": "High"},
        {"city": "Freydunshahr", "hazard": "High"},
    ],
    "Tehran": [
        {"city": "Eshtahard", "hazard": "Very High"},
        {"city": "Bumehen", "hazard": "Very High"},
        {"city": "Pishva", "hazard": "High"},
        {"city": "Tehran", "hazard": "Very High"},
        {"city": "Damavand", "hazard": "Very High"},
        {"city": "Rabat Karim", "hazard": "Very High"},
        {"city": "Rey", "hazard": "Very High"},
        {"city": "Rudehen", "hazard": "Very High"},
        {"city": "Sarbandan", "hazard": "Very High"},
        {"city": "Solegān", "hazard": "Very High"},
        {"city": "Shahriar", "hazard": "Very High"},
        {"city": "Shahr-e Qods", "hazard": "High"},
        {"city": "Shahr-e Jadid-e Parand", "hazard": "High"},
        {"city": "Taleqān", "hazard": "Very High"},
        {"city": "Fasham", "hazard": "High"},
        {"city": "Firuzkooh", "hazard": "Very High"},
        {"city": "Gejr", "hazard": "High"},
        {"city": "Kilan", "hazard": "Very High"},
        {"city": "Lavasan", "hazard": "Very High"},
        {"city": "Masha", "hazard": "Very High"},
        {"city": "Mardabad", "hazard": "Very High"},
        {"city": "Hasanābād", "hazard": "High"},
        {"city": "Erjmand", "hazard": "Very High"},
        {"city": "Dizin", "hazard": "Very High"},
        {"city": "Varamin", "hazard": "High"},
    ],
    "Alborz": [
        {"city": "Karaj", "hazard": "Very High"},
        {"city": "Hashtgerd", "hazard": "Very High"},
        {"city": "Savojbolagh", "hazard": "High"},
        {"city": "Nazarābād", "hazard": "High"},
    ],
    "Gilan": [
        {"city": "Astara", "hazard": "High"},
        {"city": "Astaneh", "hazard": "High"},
        {"city": "Bandar Anzali", "hazard": "High"},
        {"city": "Jirandeh", "hazard": "Very High"},
        {"city": "Chaboksar", "hazard": "High"},
        {"city": "Rudsar", "hazard": "High"},
        {"city": "Rudbar", "hazard": "Very High"},
        {"city": "Rezvanshahr", "hazard": "High"},
        {"city": "Rasht", "hazard": "High"},
        {"city": "Siahkal", "hazard": "High"},
        {"city": "Sowme'eh Sara", "hazard": "High"},
        {"city": "Shaft", "hazard": "High"},
        {"city": "Fuman", "hazard": "High"},
        {"city": "Kelachay", "hazard": "High"},
        {"city": "Langerud", "hazard": "High"},
        {"city": "Lahijan", "hazard": "High"},
        {"city": "Manjil", "hazard": "Very High"},
        {"city": "Masal", "hazard": "High"},
        {"city": "Masuleh", "hazard": "Very High"},
        {"city": "Hashtpar", "hazard": "High"},
        {"city": "Deylaman", "hazard": "High"},
        {"city": "Talesh", "hazard": "High"},
    ],
    "Mazandaran": [
        {"city": "Alasht", "hazard": "High"},
        {"city": "Amol", "hazard": "High"},
        {"city": "Azmaaldaoleh", "hazard": "High"},
        {"city": "Babolsar", "hazard": "High"},
        {"city": "Babol", "hazard": "High"},
        {"city": "Behshahr", "hazard": "High"},
        {"city": "Beldeh", "hazard": "High"},
        {"city": "Tonekabon", "hazard": "High"},
        {"city": "Chalus", "hazard": "High"},
        {"city": "Hasan Kif", "hazard": "High"},
        {"city": "Ramsar", "hazard": "High"},
        {"city": "Savadkuh", "hazard": "High"},
        {"city": "Sari", "hazard": "High"},
        {"city": "Polur", "hazard": "Very High"},
        {"city": "Pol-e Sefid", "hazard": "High"},
        {"city": "Qarakhil", "hazard": "High"},
        {"city": "Qaemshahr", "hazard": "High"},
        {"city": "Kelardasht", "hazard": "Very High"},
        {"city": "Galugah", "hazard": "High"},
        {"city": "Mahmoudabad", "hazard": "High"},
        {"city": "Marzanābād", "hazard": "High"},
        {"city": "Neka", "hazard": "High"},
        {"city": "Nur", "hazard": "High"},
        {"city": "Noshahr", "hazard": "High"},
        {"city": "Kiāsar", "hazard": "High"},
        {"city": "Freydunkenar", "hazard": "High"},
    ],
    "Golestan": [
        {"city": "Aq Qala", "hazard": "High"},
        {"city": "Ali Abad", "hazard": "High"},
        {"city": "Azadshahr", "hazard": "High"},
        {"city": "Bandar Gaz", "hazard": "High"},
        {"city": "Bandar Torkaman", "hazard": "High"},
        {"city": "Ramian", "hazard": "High"},
        {"city": "Kalaleh", "hazard": "High"},
        {"city": "Kordkuy", "hazard": "High"},
        {"city": "Gorgan", "hazard": "High"},
        {"city": "Gonbad Kavus", "hazard": "High"},
        {"city": "Marave Tappeh", "hazard": "High"},
        {"city": "Minoodasht", "hazard": "High"},
    ],
    "North Khorasan": [
        {"city": "Esfarayen", "hazard": "High"},
        {"city": "Ashkhaneh", "hazard": "High"},
        {"city": "Bojnurd", "hazard": "High"},
        {"city": "Jajarm", "hazard": "High"},
        {"city": "Chaman Bid", "hazard": "High"},
        {"city": "Rābat", "hazard": "Very High"},
        {"city": "Garmkhan", "hazard": "High"},
        {"city": "Gifan", "hazard": "Very High"},
        {"city": "Maneh", "hazard": "High"},
        {"city": "Shirvan", "hazard": "High"},
        {"city": "Farouj", "hazard": "Very High"},
    ],
    "Khorasan Razavi": [
        {"city": "Bajestan", "hazard": "High"},
        {"city": "Bajgiran", "hazard": "High"},
        {"city": "Bardaskan", "hazard": "High"},
        {"city": "Taybad", "hazard": "High"},
        {"city": "Torbat-e Jam", "hazard": "High"},
        {"city": "Torbat-e Heydarieh", "hazard": "High"},
        {"city": "Joghatay", "hazard": "High"},
        {"city": "Chenaran", "hazard": "High"},
        {"city": "Khaf", "hazard": "High"},
        {"city": "Dargaz", "hazard": "High"},
        {"city": "Daruneh", "hazard": "High"},
        {"city": "Rivand", "hazard": "High"},
        {"city": "Roshtkhar", "hazard": "High"},
        {"city": "Sabzevar", "hazard": "High"},
        {"city": "Sangān", "hazard": "High"},
        {"city": "Sarakhs", "hazard": "High"},
        {"city": "Salehabād", "hazard": "High"},
        {"city": "Shandiz", "hazard": "High"},
        {"city": "Fariman", "hazard": "High"},
        {"city": "Ferdows", "hazard": "High"},
        {"city": "Qalandarābād", "hazard": "High"},
        {"city": "Quchan", "hazard": "High"},
        {"city": "Kalat", "hazard": "High"},
        {"city": "Kakhk", "hazard": "High"},
        {"city": "Kashmar", "hazard": "High"},
        {"city": "Gonabad", "hazard": "High"},
        {"city": "Golbahār", "hazard": "High"},
        {"city": "Marzadaran", "hazard": "High"},
        {"city": "Mashhad", "hazard": "Very High"},
        {"city": "Neyshabur", "hazard": "High"},
        {"city": "Kamberz", "hazard": "High"},
    ],
    "Sistan and Baluchestan": [
        {"city": "Iranshahr", "hazard": "High"},
        {"city": "Bampur", "hazard": "High"},
        {"city": "Bezman", "hazard": "High"},
        {"city": "Chabahar", "hazard": "High"},
        {"city": "Dehak", "hazard": "High"},
        {"city": "Zabol", "hazard": "High"},
        {"city": "Zaboli", "hazard": "High"},
        {"city": "Zahak", "hazard": "High"},
        {"city": "Zahedan", "hazard": "High"},
        {"city": "Saravan", "hazard": "High"},
        {"city": "Sarbaz", "hazard": "High"},
        {"city": "Sib va Suran", "hazard": "High"},
        {"city": "Fanuj", "hazard": "High"},
        {"city": "Qasr-e Qand", "hazard": "High"},
        {"city": "Koochak", "hazard": "High"},
        {"city": "Konarak", "hazard": "High"},
        {"city": "Gowater", "hazard": "High"},
        {"city": "Khash", "hazard": "High"},
        {"city": "Jalq", "hazard": "High"},
        {"city": "Mirjaveh", "hazard": "High"},
        {"city": "Nasrat Abad", "hazard": "High"},
        {"city": "Nikshahr", "hazard": "High"},
    ],
    "Bushehr": [
        {"city": "Ahram", "hazard": "High"},
        {"city": "Asaluyeh", "hazard": "High"},
        {"city": "Bandar Dayyer", "hazard": "High"},
        {"city": "Bandar Deylam", "hazard": "High"},
        {"city": "Bandar Taheri", "hazard": "High"},
        {"city": "Bandar Genaveh", "hazard": "High"},
        {"city": "Bandar-e Kangan", "hazard": "High"},
        {"city": "Bandar-e Maqām", "hazard": "High"},
        {"city": "Borazjan", "hazard": "High"},
        {"city": "Bushehr", "hazard": "High"},
        {"city": "Jam", "hazard": "High"},
        {"city": "Khark", "hazard": "High"},
        {"city": "Khormoj", "hazard": "High"},
        {"city": "Dalaki", "hazard": "High"},
        {"city": "Deylvar", "hazard": "High"},
        {"city": "Riz", "hazard": "High"},
        {"city": "Shabānkāreh", "hazard": "High"},
        {"city": "Taheri", "hazard": "High"},
        {"city": "Gāvbandi", "hazard": "High"},
        {"city": "Genaveh", "hazard": "High"},
    ],
    "Hormozgan": [
        {"city": "Bandar Abbas", "hazard": "High"},
        {"city": "Bandar Khamir", "hazard": "High"},
        {"city": "Bandar Lengeh", "hazard": "High"},
        {"city": "Bastak", "hazard": "High"},
        {"city": "Jask", "hazard": "High"},
        {"city": "Charak", "hazard": "High"},
        {"city": "Hajiabad", "hazard": "High"},
        {"city": "Rudān", "hazard": "High"},
        {"city": "Qeshm", "hazard": "High"},
        {"city": "Kish", "hazard": "High"},
        {"city": "Gavbandi", "hazard": "High"},
        {"city": "Lavan", "hazard": "High"},
        {"city": "Minab", "hazard": "High"},
    ],
}


# Map seismic hazard from city data
def get_seismic_hazard_from_city(province, city_name):
    """Get seismic hazard level for a specific city"""
    if province in CITIES_DATA:
        for city in CITIES_DATA[province]:
            if city["city"] == city_name:
                return city["hazard"]
    # Fallback to province-level hazard
    hazard_map = {
        "Tehran": "High", "Alborz": "High", "Kermanshah": "High",
        "Kohgiluyeh and Boyer-Ahmad": "High", "Lorestan": "High",
        "West Azerbaijan": "High", "East Azerbaijan": "High",
        "Fars": "High", "Hormozgan": "High", "Kurdistan": "Moderate",
        "Ilam": "Moderate", "Chaharmahal and Bakhtiari": "Moderate", 
        "Bushehr": "Moderate", "Mazandaran": "Moderate", "Gilan": "Moderate", 
        "Khorasan Razavi": "Moderate", "South Khorasan": "Moderate", 
        "Qazvin": "Moderate", "Zanjan": "Moderate", "Semnan": "Moderate", 
        "Markazi": "Moderate", "Isfahan": "Moderate", "Kerman": "Moderate", 
        "Qom": "Low", "Yazd": "Low", "Khuzestan": "Low",
        "Golestan": "Low", "North Khorasan": "Low", "Sistan and Baluchestan": "Low"
    }
    return hazard_map.get(province, "Moderate")

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

def create_component_diagram(diameter, height, capacity, motor_power, num_cabins=32 , cabin_geometry="Square"):
    """Enhanced carousel diagram with properly scaled cabins"""
    # Draw wheel as a perfect circle
    theta = np.linspace(0, 2*np.pi, 200)
    radius = diameter / 2
    x_wheel = radius * np.cos(theta)
    y_wheel = radius * np.sin(theta) + height/2

    fig = go.Figure()
    
    # Draw wheel
    fig.add_trace(go.Scatter(x=x_wheel, y=y_wheel, mode='lines', 
                            line=dict(color='#2196F3', width=3), 
                            showlegend=False, name='Wheel'))
    
    # Draw support structure
    fig.add_trace(go.Scatter(x=[0,0], y=[0,height/2], mode='lines', 
                            line=dict(color='#FF5722', width=6), 
                            showlegend=False, name='Support'))
    
    # Draw cabins based on geometry
    cabin_scale = diameter * 0.04  # Scale cabins relative to wheel size
    
    for i in range(num_cabins):
        angle = 2 * np.pi * i / num_cabins
        cabin_x = radius * np.cos(angle)
        cabin_y = radius * np.sin(angle) + height/2
        
        if cabin_geometry == "Spherical":
            # Draw circle for spherical cabin
            cabin_theta = np.linspace(0, 2*np.pi, 30)
            cx = cabin_x + cabin_scale * 0.5 * np.cos(cabin_theta)
            cy = cabin_y + cabin_scale * 0.5 * np.sin(cabin_theta)
            fig.add_trace(go.Scatter(x=cx, y=cy, mode='lines', 
                                    fill='toself', fillcolor='rgba(255, 193, 7, 0.6)',
                                    line=dict(color='#FFC107', width=1.5),
                                    showlegend=False, hoverinfo='skip'))
        
        elif cabin_geometry == "Vertical Cylinder":
            # Draw vertical rectangle
            w = cabin_scale * 0.4
            h = cabin_scale * 0.8
            rect_x = [cabin_x - w/2, cabin_x + w/2, cabin_x + w/2, cabin_x - w/2, cabin_x - w/2]
            rect_y = [cabin_y - h/2, cabin_y - h/2, cabin_y + h/2, cabin_y + h/2, cabin_y - h/2]
            fig.add_trace(go.Scatter(x=rect_x, y=rect_y, mode='lines', 
                                    fill='toself', fillcolor='rgba(76, 175, 80, 0.6)',
                                    line=dict(color='#4CAF50', width=1.5),
                                    showlegend=False, hoverinfo='skip'))
        
        elif cabin_geometry == "Horizontal Cylinder":
            # Draw horizontal rectangle
            w = cabin_scale * 0.8
            h = cabin_scale * 0.4
            rect_x = [cabin_x - w/2, cabin_x + w/2, cabin_x + w/2, cabin_x - w/2, cabin_x - w/2]
            rect_y = [cabin_y - h/2, cabin_y - h/2, cabin_y + h/2, cabin_y + h/2, cabin_y - h/2]
            fig.add_trace(go.Scatter(x=rect_x, y=rect_y, mode='lines', 
                                    fill='toself', fillcolor='rgba(156, 39, 176, 0.6)',
                                    line=dict(color='#9C27B0', width=1.5),
                                    showlegend=False, hoverinfo='skip'))
        
        else:  # Square
            # Draw square
            s = cabin_scale * 0.6
            square_x = [cabin_x - s/2, cabin_x + s/2, cabin_x + s/2, cabin_x - s/2, cabin_x - s/2]
            square_y = [cabin_y - s/2, cabin_y - s/2, cabin_y + s/2, cabin_y + s/2, cabin_y - s/2]
            fig.add_trace(go.Scatter(x=square_x, y=square_y, mode='lines', 
                                    fill='toself', fillcolor='rgba(244, 67, 54, 0.6)',
                                    line=dict(color='#F44336', width=1.5),
                                    showlegend=False, hoverinfo='skip'))

    annotations = [
        dict(x=0, y=height + diameter*0.05 + 2, text=f"Height: {height:.1f} m", 
             showarrow=False, font=dict(color='black', size=12)),
        dict(x=diameter/2 + 2, y=height/2, text=f"Diameter: {diameter} m", 
             showarrow=False, font=dict(color='black', size=12)),
        dict(x=0, y=-5, text=f"Motor Power: {motor_power:.1f} kW", 
             showarrow=False, font=dict(color='black', size=12)),
        dict(x=0, y=-8, text=f"Capacity: {capacity} passengers", 
             showarrow=False, font=dict(color='black', size=12)),
        dict(x=0, y=-11, text=f"Cabins: {num_cabins} ({cabin_geometry})", 
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
        xaxis=dict(scaleanchor="y", scaleratio=1, showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )
    return fig

def calculate_motor_power(diameter, num_cabins, cabin_capacity, num_vip_cabins, 
                         rotation_time_min, cabin_geometry):
    """
    محاسبه واقع‌بینانه توان موتور برای چرخ و فلک
    
    Parameters:
    -----------
    diameter : float
        قطر چرخ (متر)
    num_cabins : int
        تعداد کابین‌ها
    cabin_capacity : int
        ظرفیت هر کابین
    num_vip_cabins : int
        تعداد کابین‌های VIP
    rotation_time_min : float
        زمان یک دور چرخش (دقیقه)
    cabin_geometry : str
        شکل کابین
    
    Returns:
    --------
    dict : {
        'rated_power': توان نامی موتور (kW),
        'peak_power': توان پیک (startup) (kW),
        'operational_power': توان عملیاتی (kW),
        'breakdown': توضیحات محاسبات
    }
    """
    
    # محاسبه جرم‌ها
    # 1. جرم مسافران (80 kg هر نفر)
    vip_capacity = max(0, cabin_capacity - 2)
    total_passengers = (num_vip_cabins * vip_capacity + 
                       (num_cabins - num_vip_cabins) * cabin_capacity)
    mass_passengers = total_passengers * 80.0  # kg
    
    # 2. جرم کابین‌ها (بر اساس شکل و ظرفیت)
    cabin_mass_per_unit = {
        'Square': 450,      # kg per cabin
        'Vertical': 400,    # Cylinder vertical
        'Horizontal': 500,  # Cylinder horizontal
        'Spherical': 350    # Sphere (lighter)
    }
    
    # تشخیص شکل کابین
    cabin_type = 'Square'  # default
    for key in cabin_mass_per_unit.keys():
        if key in cabin_geometry or key.lower() in cabin_geometry.lower():
            cabin_type = key
            break
    
    mass_per_cabin = cabin_mass_per_unit[cabin_type] + (cabin_capacity * 20)  # 20 kg per seat
    mass_cabins = num_cabins * mass_per_cabin  # kg
    
    # 3. جرم سازه فلزی (تخمین بر اساس قطر)
    # فرمول تجربی: mass_structure = diameter^1.5 × factor
    structure_factor = 800  # kg/m^1.5
    mass_structure = diameter ** 1.5 * structure_factor  # kg
    
    # 4. جرم محور و تجهیزات
    mass_axis = diameter * 150  # kg
    
    # جرم کل
    total_mass = mass_passengers + mass_cabins + mass_structure + mass_axis  # kg
    
    # محاسبه پارامترهای حرکتی
    radius = diameter / 2.0  # m
    rotation_time_sec = rotation_time_min * 60.0  # s
    angular_velocity = 2.0 * np.pi / rotation_time_sec  # rad/s
    linear_velocity = angular_velocity * radius  # m/s at rim
    
    # محاسبه گشتاور لازم برای غلبه بر اصطکاک
    # اصطکاک در یاتاقان‌ها و مقاومت هوا
    friction_coefficient = 0.03  # ضریب اصطکاک معادل
    torque_friction = friction_coefficient * total_mass * 9.81 * radius  # N⋅m
    
    # توان عملیاتی (steady state)
    power_operational = torque_friction * angular_velocity / 1000.0  # kW
    
    # توان برای شتاب (startup)
    # فرض: رسیدن به سرعت کامل در 60 ثانیه
    startup_time = 60.0  # seconds
    angular_acceleration = angular_velocity / startup_time  # rad/s²
    
    # moment of inertia
    # ساده‌سازی: تمام جرم در فاصله r
    moment_of_inertia = total_mass * radius ** 2  # kg⋅m²
    
    # گشتاور برای شتاب
    torque_acceleration = moment_of_inertia * angular_acceleration  # N⋅m
    
    # توان پیک (شامل شتاب + اصطکاک)
    power_peak = (torque_acceleration + torque_friction) * angular_velocity / 1000.0  # kW
    
    # توان نامی موتور (با ضریب اطمینان)
    safety_factor = 1.5  # ضریب اطمینان
    power_rated = power_peak * safety_factor  # kW
    
    # حداقل توان موتور (معمولاً چرخ‌های فلک بزرگ از موتورهای قوی‌تر استفاده می‌کنند)
    # فرمول تجربی: حداقل 0.5 kW به ازای هر متر قطر
    power_minimum = diameter * 0.5  # kW
    power_rated = max(power_rated, power_minimum)
    
    # محدود کردن به محدوده واقعی
    # چرخ‌های فلک کوچک: 15-50 kW
    # چرخ‌های فلک متوسط: 50-150 kW
    # چرخ‌های فلک بزرگ: 150-500+ kW
    if diameter < 40:
        power_rated = max(15, min(power_rated, 50))
    elif diameter < 60:
        power_rated = max(50, min(power_rated, 150))
    else:
        power_rated = max(150, min(power_rated, 500))
    
    breakdown = {
        'total_mass': total_mass,
        'mass_passengers': mass_passengers,
        'mass_cabins': mass_cabins,
        'mass_structure': mass_structure,
        'mass_axis': mass_axis,
        'angular_velocity': angular_velocity,
        'linear_velocity': linear_velocity,
        'moment_of_inertia': moment_of_inertia,
        'torque_friction': torque_friction,
        'torque_acceleration': torque_acceleration,
        'startup_time': startup_time
    }
    
    return {
        'rated_power': round(power_rated, 1),
        'peak_power': round(power_peak, 1),
        'operational_power': round(power_operational, 1),
        'breakdown': breakdown
    }


def format_power_breakdown(power_data):
    """
    فرمت کردن جزئیات محاسبه توان برای نمایش
    """
    breakdown = power_data['breakdown']
    
    text = f"""
**Power Calculation Details:**

**Masses:**
- Passengers: {breakdown['mass_passengers']:.0f} kg
- Cabins: {breakdown['mass_cabins']:.0f} kg
- Structure: {breakdown['mass_structure']:.0f} kg
- Axis & Equipment: {breakdown['mass_axis']:.0f} kg
- **Total Mass: {breakdown['total_mass']:.0f} kg**

**Kinematics:**
- Angular Velocity: {breakdown['angular_velocity']:.6f} rad/s
- Linear Velocity (rim): {breakdown['linear_velocity']:.3f} m/s
- Moment of Inertia: {breakdown['moment_of_inertia']:.0f} kg⋅m²

**Torques:**
- Friction Torque: {breakdown['torque_friction']:.0f} N⋅m
- Acceleration Torque: {breakdown['torque_acceleration']:.0f} N⋅m
- Startup Time: {breakdown['startup_time']:.0f} seconds

**Power Requirements:**
- Operational Power: {power_data['operational_power']:.1f} kW (steady state)
- Peak Power: {power_data['peak_power']:.1f} kW (startup)
- **Rated Motor Power: {power_data['rated_power']:.1f} kW** (with safety factor 1.5)
"""
    return text

def calculate_accelerations_at_angle(theta, diameter, angular_velocity, braking_accel, 
                                    snow_load=0.0, wind_load=0.0, earthquake_load=0.0, g=9.81):
    """
    Calculate accelerations at a given angle with additional loads
    
    Parameters:
    -----------
    theta : float
        Angle in radians
    diameter : float
        Wheel diameter in meters
    angular_velocity : float
        Angular velocity in rad/s
    braking_accel : float
        Braking acceleration in m/s²
    snow_load : float
        Snow load in kN (default 0.0)
    wind_load : float
        Wind load in kN (default 0.0)
    earthquake_load : float
        Earthquake load in kN (default 0.0)
    g : float
        Gravitational acceleration (default 9.81 m/s²)
    
    Returns:
    --------
    a_x_total : float
        Total horizontal acceleration in m/s²
    a_z_total : float
        Total vertical acceleration in m/s²
    a_total : float
        Total magnitude of acceleration in m/s²
    """
    radius = diameter / 2.0
    a_centripetal = radius * (angular_velocity ** 2)
    
    # Gravity components
    a_z_gravity = -g
    a_x_gravity = 0
    
    # Centripetal acceleration components
    a_x_centripetal = a_centripetal * np.cos(theta)
    a_z_centripetal = a_centripetal * np.sin(theta)
    
    # Braking acceleration components
    a_x_braking = braking_accel * np.sin(theta)
    a_z_braking = -braking_accel * np.cos(theta)
    
    # Additional loads converted to accelerations
    # Assuming approximate cabin mass of 500 kg per meter of diameter
    approx_mass = diameter * 500  # kg
    
    # Snow load effect (vertical, downward)
    a_snow = 0.0
    if snow_load > 0:
        # Convert kN to N and divide by mass to get acceleration
        a_snow = (snow_load * 1000) / approx_mass  # m/s²
    
    # Wind load effect (horizontal, varies with position)
    a_wind_x = 0.0
    a_wind_z = 0.0
    if wind_load > 0:
        # Wind acts horizontally, but its effect varies with cabin position
        # Maximum effect when cabin is at the side (theta = π/2 or 3π/2)
        wind_accel = (wind_load * 1000) / approx_mass  # m/s²
        # Horizontal component (more effect when cabin is on the side)
        a_wind_x = wind_accel * np.abs(np.sin(theta))
        # Small vertical component due to drag
        a_wind_z = wind_accel * 0.1 * np.cos(theta)
    
    # Earthquake load effect (horizontal and vertical)
    a_eq_x = 0.0
    a_eq_z = 0.0
    if earthquake_load > 0:
        eq_accel = (earthquake_load * 1000) / approx_mass  # m/s²
        # Horizontal component (primary)
        a_eq_x = eq_accel
        # Vertical component (typically 50% of horizontal)
        a_eq_z = eq_accel * 0.5
    
    # Total accelerations
    a_x_total = a_x_gravity + a_x_centripetal + a_x_braking + a_wind_x + a_eq_x
    a_z_total = a_z_gravity + a_z_centripetal + a_z_braking - a_snow + a_wind_z + a_eq_z
    
    a_total = np.sqrt(a_x_total**2 + a_z_total**2)
    
    return a_x_total, a_z_total, a_total

def calculate_dynamic_product(diameter, height, angular_velocity, braking_accel, 
                              snow_load=0.0, wind_load=0.0, earthquake_load=0.0, g=9.81):
    """
    Calculate dynamic product with additional loads
    
    Parameters:
    -----------
    diameter : float
        Wheel diameter in meters
    height : float
        Height in meters
    angular_velocity : float
        Angular velocity in rad/s
    braking_accel : float
        Braking acceleration in m/s²
    snow_load : float
        Snow load in kN (default 0.0)
    wind_load : float
        Wind load in kN (default 0.0)
    earthquake_load : float
        Earthquake load in kN (default 0.0)
    g : float
        Gravitational acceleration (default 9.81 m/s²)
    
    Returns:
    --------
    p : float
        Dynamic product
    n : float
        Maximum acceleration in g units
    max_accel : float
        Maximum acceleration in m/s²
    """
    theta_vals = np.linspace(0, 2*np.pi, 360)
    max_accel = 0
    
    for theta in theta_vals:
        _, _, a_total = calculate_accelerations_at_angle(
            theta, diameter, angular_velocity, braking_accel, 
            snow_load, wind_load, earthquake_load, g
        )
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
    # Zone 1: Upper region
    if ax > 0.2 and az > 0.2:
        return 1
    if 0 < ax <= 0.2 and az > 0.7:
        return 1
    if -0.2 < ax < 0 and az > (-1.5 * ax + 0.7):
        return 1
    
    # Zone 2: Upper-central region
    if 0 < ax <= 0.2 and 0.2 < az <= 0.7:
        return 2
    if -0.2 < ax < 0 and 0.2 < az <= (-1.5 * ax + 0.7):
        return 2
    if -0.7 < ax <= -0.2 and az > 0.2:
        return 2
    
    # Zone 3: Central edges
    if -1.2 < ax <= -0.7 and az > 0.2:
        return 3
    if -0.7 < ax < 0 and ((-0.2/0.7) * ax) < az <= 0.2:
        return 3
    if ax > 0 and 0 < az <= 0.2:
        return 3
    
    # Zone 4: Lower-central region
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
    
    # Zone 5: Lower region
    if ax > 0.7 and az < -0.2:
        return 5
    if 0 < ax <= 0.7 and az < ((-0.2/0.7) * ax):
        return 5
    if ax < 0 and az < 0:
        return 5
    if ax < -1.8:
        return 5
    
    return 2  # Default

def estimate_cabin_surface_area(cabin_geometry, cabin_capacity, diameter):
    """
    تخمین مساحت سطح کابین بر اساس شکل، ظرفیت و قطر چرخ
    
    Parameters:
    -----------
    cabin_geometry : str
        شکل کابین (Square, Vertical Cylinder, Horizontal Cylinder, Spherical)
    cabin_capacity : int
        ظرفیت مسافری کابین
    diameter : float
        قطر چرخ (متر)
    
    Returns:
    --------
    float
        مساحت سطح تقریبی کابین (متر مربع)
    """
    
    # تخمین ابعاد کابین بر اساس ظرفیت
    # فرض: هر مسافر نیاز به ~0.6 m² فضای کف دارد
    floor_area_per_person = 0.6  # m²
    floor_area = cabin_capacity * floor_area_per_person
    
    # ارتفاع استاندارد کابین
    cabin_height = 2.2  # meters
    
    # محدودیت اندازه کابین بر اساس قطر چرخ
    # کابین نباید بیشتر از 1/8 قطر چرخ باشد
    max_cabin_dimension = diameter / 8.0
    
    if "Square" in cabin_geometry or "مربع" in cabin_geometry or "مکعب" in cabin_geometry:
        # کابین مربعی/مکعبی
        side_length = min(np.sqrt(floor_area), max_cabin_dimension)
        # مساحت سطح = 2×(طول×عرض) + 4×(طول×ارتفاع)
        surface_area = 2 * (side_length ** 2) + 4 * (side_length * cabin_height)
        
    elif "Vertical" in cabin_geometry or "عمودی" in cabin_geometry:
        # استوانه عمودی (ایستاده)
        radius = min(np.sqrt(floor_area / np.pi), max_cabin_dimension / 2.0)
        # مساحت سطح = 2×π×r² + 2×π×r×h
        surface_area = 2 * np.pi * (radius ** 2) + 2 * np.pi * radius * cabin_height
        
    elif "Horizontal" in cabin_geometry or "افقی" in cabin_geometry:
        # استوانه افقی (خوابیده)
        # طول استوانه بر اساس فضای کف
        length = min(floor_area / 2.0, max_cabin_dimension)
        radius = min(1.0, max_cabin_dimension / 4.0)  # شعاع ثابت ~1m
        # مساحت سطح = 2×π×r² + 2×π×r×L
        surface_area = 2 * np.pi * (radius ** 2) + 2 * np.pi * radius * length
        
    elif "Spherical" in cabin_geometry or "کروی" in cabin_geometry or "sphere" in cabin_geometry.lower():
        # کابین کروی
        # حجم مورد نیاز بر اساس ظرفیت
        volume_per_person = 1.5  # m³ per person
        required_volume = cabin_capacity * volume_per_person
        # شعاع کره: V = (4/3)πr³
        radius = min((3 * required_volume / (4 * np.pi)) ** (1/3), max_cabin_dimension / 2.0)
        # مساحت سطح کره = 4πr²
        surface_area = 4 * np.pi * (radius ** 2)
        
    else:
        # پیش‌فرض: مربع
        side_length = min(np.sqrt(floor_area), max_cabin_dimension)
        surface_area = 2 * (side_length ** 2) + 4 * (side_length * cabin_height)
    
    # محدود کردن مساحت به محدوده منطقی
    # حداقل: 8 m² (کابین خیلی کوچک)
    # حداکثر: 25 m² (کابین بزرگ)
    surface_area = max(8.0, min(surface_area, 25.0))
    
    return round(surface_area, 2)

def determine_restraint_area_as(ax, az):
    """Determine restraint area based on AS 3533.1-2009+A1-2011 (ax and az in units of g)"""
    # Zone 1: Upper region
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

def plot_acceleration_envelope_iso(diameter, angular_velocity, braking_accel, 
                                  snow_load=0.0, wind_load=0.0, earthquake_load=0.0, g=9.81):
    """Plot the ax vs az acceleration envelope with ISO 17842 zones and actual acceleration points"""
    theta_vals = np.linspace(0, 2*np.pi, 360)
    ax_vals = []
    az_vals = []
    
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(
            theta, diameter, angular_velocity, braking_accel,
            snow_load, wind_load, earthquake_load, g
        )
        ax_vals.append(a_x / g)
        az_vals.append(-a_z / g)
    
    fig = go.Figure()
    
    # Zone 1 (Purple)
    x_z1 = [0.2, 2.0, 2.0, -0.2, -0.2, 0, 0.2]
    y_z1 = [0.2, 0.2, 2.0, 2.0, 1, 0.7, 0.7]
    fig.add_trace(go.Scatter(x=x_z1, y=y_z1, fill='toself', fillcolor='rgba(128,0,128,0.15)', 
                             line=dict(color='purple', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=0.5, y=1.2, text="Zone 1", showarrow=False, 
                      font=dict(size=11, color="purple", family="Arial Black"))
    
    # Zone 2 (Orange)
    x_z2 = [-0.7, 0.2, 0.2, 0, -0.2, -0.2, -0.7]
    y_z2 = [0.2, 0.2, 0.7, 0.7, 1, 2, 2]
    fig.add_trace(go.Scatter(x=x_z2, y=y_z2, fill='toself', fillcolor='rgba(255,165,0,0.15)',
                             line=dict(color='orange', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=-0.2, y=0.45, text="Zone 2", showarrow=False,
                      font=dict(size=11, color="orange", family="Arial Black"))
    
    # Zone 3 (Yellow)
    x_z3 = [-1.2, -0.7, 0, 2, 2.0, 2.0, -0.7, -0.7, -1.2]
    y_z3 = [0.2, 0.2, 0, 0, 0.2, 0.2, 0.2, 2, 2]
    fig.add_trace(go.Scatter(x=x_z3, y=y_z3, fill='toself', fillcolor='rgba(255,255,0,0.15)',
                             line=dict(color='gold', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=0.5, y=0.1, text="Zone 3", showarrow=False,
                      font=dict(size=11, color="gold", family="Arial Black"))
    
    # Zone 4 (Green)
    x_z4 = [-1.8, 0, 0.7, 2, 2, 0, -0.7, -1.2, -1.2, -1.8]
    y_z4 = [0, 0, -0.2, -0.2, 0, 0, 0.2, 0.2, 2, 2]
    fig.add_trace(go.Scatter(x=x_z4, y=y_z4, fill='toself', fillcolor='rgba(0,255,0,0.15)',
                             line=dict(color='green', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=-0.4, y=-0.05, text="Zone 4", showarrow=False,
                      font=dict(size=11, color="green", family="Arial Black"))
    
    # Zone 5 (Red)
    x_z5 = [0.7, 2.0, 2.0, -2, -2.0, -2.0, -1.8, -1.8, 0]
    y_z5 = [-0.2, -0.2, -2.0, -2.0, 0, 2, 2, 0, 0]
    fig.add_trace(go.Scatter(x=x_z5, y=y_z5, fill='toself', fillcolor='rgba(255,0,0,0.15)',
                             line=dict(color='red', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=1.0, y=-0.8, text="Zone 5", showarrow=False,
                      font=dict(size=11, color="red", family="Arial Black"))
    
    # Plot actual acceleration points (after zones for visibility)
    fig.add_trace(go.Scatter(x=ax_vals, y=az_vals, mode='markers+lines',
                             marker=dict(color='#2196F3', size=6, symbol='circle',
                                       line=dict(color='darkblue', width=1)),
                             line=dict(color='#2196F3', width=2),
                             name='Acceleration Envelope'))
    
    # Highlight extreme points
    max_ax_idx = np.argmax(ax_vals)
    min_ax_idx = np.argmin(ax_vals)
    max_az_idx = np.argmax(az_vals)
    min_az_idx = np.argmin(az_vals)
    
    extreme_points = [
        (ax_vals[max_ax_idx], az_vals[max_ax_idx], 'Max ax'),
        (ax_vals[min_ax_idx], az_vals[min_ax_idx], 'Min ax'),
        (ax_vals[max_az_idx], az_vals[max_az_idx], 'Max az'),
        (ax_vals[min_az_idx], az_vals[min_az_idx], 'Min az')
    ]
    
    for ax, az, label in extreme_points:
        fig.add_trace(go.Scatter(x=[ax], y=[az], mode='markers+text',
                                marker=dict(size=12, color='red', symbol='star'),
                                text=[label], textposition='top center',
                                textfont=dict(size=9, color='red', family='Arial Black'),
                                showlegend=False))
    
    fig.update_layout(title="ISO 17842 - Acceleration Envelope with Actual Operating Points", 
                      xaxis_title="Horizontal Acceleration ax [g]",
                      yaxis_title="Vertical Acceleration az [g]", height=700, template="plotly_white",
                      xaxis=dict(range=[-2.2, 2.2], zeroline=True, zerolinewidth=2, zerolinecolor='black'),
                      yaxis=dict(range=[-2.2, 2.2], zeroline=True, zerolinewidth=2, zerolinecolor='black'))
    return fig

def plot_acceleration_envelope_as(diameter, angular_velocity, braking_accel, 
                                 snow_load=0.0, wind_load=0.0, earthquake_load=0.0, g=9.81):
    """Plot the ax vs az acceleration envelope with AS 3533.1 zones and actual acceleration points"""
    theta_vals = np.linspace(0, 2*np.pi, 360)
    ax_vals = []
    az_vals = []
    
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(
            theta, diameter, angular_velocity, braking_accel,
            snow_load, wind_load, earthquake_load, g
        )
        ax_vals.append(a_x / g)
        az_vals.append(-a_z / g)
    
    fig = go.Figure()
    
    # Zone 1 (Purple)
    x_z1 = [0.2, 2.0, 2.0, 0.2]
    y_z1 = [0.2, 0.2, 2.0, 2.0]
    fig.add_trace(go.Scatter(x=x_z1, y=y_z1, fill='toself', fillcolor='rgba(128,0,128,0.15)', 
                             line=dict(color='purple', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=0.8, y=1.0, text="Zone 1", showarrow=False,
                      font=dict(size=11, color="purple", family="Arial Black"))
    
    # Zone 2 (Orange)
    x_z2 = [0.2, -0.7, -0.7, 0.2]
    y_z2 = [0.2, 0.2, 2.0, 2.0]
    fig.add_trace(go.Scatter(x=x_z2, y=y_z2, fill='toself', fillcolor='rgba(255,165,0,0.15)',
                             line=dict(color='orange', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=-0.2, y=0.8, text="Zone 2", showarrow=False,
                      font=dict(size=11, color="orange", family="Arial Black"))
    
    # Zone 3 (Yellow)
    x_z3 = [-1.2, -1.2, -0.7, -0.7, 2, 2.0, 0.7, 0, -0.7, -1.2]
    y_z3 = [0.2, 2, 2, 0.2, 0.2, -0.2, -0.2, 0, 0.2, 0.2]
    fig.add_trace(go.Scatter(x=x_z3, y=y_z3, fill='toself', fillcolor='rgba(255,255,0,0.15)',
                             line=dict(color='gold', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=0.5, y=0.05, text="Zone 3", showarrow=False,
                      font=dict(size=11, color="gold", family="Arial Black"))
    
    # Zone 4 (Green)
    x_z4 = [-1.8, -1.8, -1.2, -1.2, -0.7, 0]
    y_z4 = [0, 2, 2, 0.2, 0.2, 0]
    fig.add_trace(go.Scatter(x=x_z4, y=y_z4, fill='toself', fillcolor='rgba(0,255,0,0.15)',
                             line=dict(color='green', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=-0.5, y=0.05, text="Zone 4", showarrow=False,
                      font=dict(size=11, color="green", family="Arial Black"))
    
    # Zone 5 (Red)
    x_z5 = [0, -1.8, -1.8, -2.0, -2, -2, 2, 2, 0.7]
    y_z5 = [0, 0, 2, 2.0, 0, -2, -2, -0.2, -0.2]
    fig.add_trace(go.Scatter(x=x_z5, y=y_z5, fill='toself', fillcolor='rgba(255,0,0,0.15)',
                             line=dict(color='red', width=2, dash='dash'), showlegend=False))
    fig.add_annotation(x=1.0, y=-0.8, text="Zone 5", showarrow=False,
                      font=dict(size=11, color="red", family="Arial Black"))
    
    # Plot actual acceleration points (after zones for visibility)
    fig.add_trace(go.Scatter(x=ax_vals, y=az_vals, mode='markers+lines',
                             marker=dict(color='#2196F3', size=6, symbol='circle',
                                       line=dict(color='darkblue', width=1)),
                             line=dict(color='#2196F3', width=2),
                             name='Acceleration Envelope'))
    
    # Highlight extreme points
    max_ax_idx = np.argmax(ax_vals)
    min_ax_idx = np.argmin(ax_vals)
    max_az_idx = np.argmax(az_vals)
    min_az_idx = np.argmin(az_vals)
    
    extreme_points = [
        (ax_vals[max_ax_idx], az_vals[max_ax_idx], 'Max ax'),
        (ax_vals[min_ax_idx], az_vals[min_ax_idx], 'Min ax'),
        (ax_vals[max_az_idx], az_vals[max_az_idx], 'Max az'),
        (ax_vals[min_az_idx], az_vals[min_az_idx], 'Min az')
    ]
    
    for ax, az, label in extreme_points:
        fig.add_trace(go.Scatter(x=[ax], y=[az], mode='markers+text',
                                marker=dict(size=12, color='red', symbol='star'),
                                text=[label], textposition='top center',
                                textfont=dict(size=9, color='red', family='Arial Black'),
                                showlegend=False))
    
    fig.update_layout(title="AS 3533.1 - Acceleration Envelope with Actual Operating Points", 
                      xaxis_title="Horizontal Acceleration ax [g]",
                      yaxis_title="Vertical Acceleration az [g]", height=700, template="plotly_white",
                      xaxis=dict(range=[-2.2, 2.2], zeroline=True, zerolinewidth=2, zerolinecolor='black'),
                      yaxis=dict(range=[-2.2, 2.2], zeroline=True, zerolinewidth=2, zerolinecolor='black'))
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
        if not env.get('city'):
            errors.append("Select a city.")
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
        st.session_state.scroll_to_top = True
    else:
        st.session_state.validation_errors = []
        st.session_state.step = min(12, st.session_state.step + 1)


def axis_label(axis):
    return {
        'NS': 'North–South',
        'EW': 'East–West',
        'NE_SW': 'Northeast–Southwest',
        'SE_NW': 'Southeast–Northwest'
    }[axis]

def map_direction_to_axis_and_vector(dir_str):
    d = (dir_str or "").strip().lower()
    s = 1 / math.sqrt(2)
    if d in ('north-south', 'north–south', 'north south'):
        return 'NS', 'North–South', (0, 1)
    if d in ('east-west', 'east–west', 'east west'):
        return 'EW', 'East–West', (1, 0)
    if d in ('northeast-southwest', 'northeast–southwest', 'northeast southwest'):
        return 'NE_SW', 'Northeast–Southwest', (s, s)
    if d in ('northwest-southeast', 'northwest–southeast', 'northwest southeast'):
        return 'SE_NW', 'Northwest–Southeast', (-s, s)

    if d in ('north', 'n'): return 'NS', 'North', (0, 1)
    if d in ('south', 's'): return 'NS', 'South', (0, -1)
    if d in ('east', 'e'): return 'EW', 'East', (1, 0)
    if d in ('west', 'w'): return 'EW', 'West', (-1, 0)
    if d in ('northeast', 'ne'): return 'NE_SW', 'Northeast', (s, s)
    if d in ('southwest', 'sw'): return 'NE_SW', 'Southwest', (-s, -s)
    if d in ('southeast', 'se'): return 'SE_NW', 'Southeast', (s, -s)
    if d in ('northwest', 'nw'): return 'SE_NW', 'Northwest', (-s, s)

    return 'NS', 'North–South', (0, 1)

def create_orientation_diagram(axis_key, land_length, land_width, arrow_vec, arrow_text):
    w, h = float(land_length), float(land_width)
    
    # مستطیل ثابت بدون چرخش
    xs = [-w/2, w/2, w/2, -w/2, -w/2]
    ys = [-h/2, -h/2, h/2, h/2, -h/2]
    
    fig = go.Figure()

    # رسم بدنه مستطیل
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode='lines', 
        line=dict(color='rgb(30,90,160)', width=3),
        showlegend=False, hoverinfo='skip'
    ))

    # تنظیم طول فلش (۴۰٪ کوچکترین ضلع)
    L = min(w, h) * 0.4
    dx, dy = arrow_vec[0] * L, arrow_vec[1] * L

    # رسم فلش دوطرفه قرمز در مرکز
    fig.add_annotation(
        x=dx, y=dy, ax=-dx, ay=-dy,
        xref="x", yref="y", axref="x", ayref="y",
        arrowhead=3, arrowsize=1.5, arrowwidth=4, arrowcolor='red',
        text="", showarrow=True, arrowside='end+start'
    )

    pad = max(w, h) * 0.2
    fig.update_layout(
        xaxis=dict(range=[-w/2-pad, w/2+pad], visible=False),
        yaxis=dict(range=[-h/2-pad, h/2+pad], visible=False),
        width=600, height=450, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig





# --- UI ---
# Language toggle in sidebar
with st.sidebar:
    st.title("🎡 Ferris Wheel Designer")
    persian = st.toggle("🇮🇷 فارسی", value=st.session_state.persian, key="persian_toggle")
    st.session_state.persian = persian
    
    if st.button("🔄 Reset Design"):
        reset_design()
        st.rerun()

total_steps = 13
st.progress(st.session_state.get('step', 0) / (total_steps - 1))
st.markdown(f"**{get_text('step', persian)} {st.session_state.get('step', 0) + 1} {get_text('of', persian)} {total_steps}**")
st.markdown("---")


# === STEP 0: Welcome and Standards ===
if st.session_state.get('step', 0) == 0:
    col_lang1, col_lang2 = st.columns([3,1])
    with col_lang1:
        st.header(get_text('welcome_title', persian))
    with col_lang2:
        # Language selector on main page
        lang_choice = st.radio(
            "Language / زبان",
            options=["English", "فارسی"],
            index=1 if st.session_state.persian else 0,
            horizontal=True,
            key="main_page_language"
        )
        if (lang_choice == "فارسی") != st.session_state.persian:
            st.session_state.persian = (lang_choice == "فارسی")
            st.rerun()
    
    st.markdown("---")
    
    # About Section (بدون عنوان تکراری)
    st.markdown(f"### {get_text('about_title', persian)}")
    st.markdown(get_text('about_intro', persian))
    
    # Features list
    st.markdown(f"""
- {get_text('feature_generation', persian)}
- {get_text('feature_cabin', persian)}
- {get_text('feature_performance', persian)}
- {get_text('feature_environment', persian)}
- {get_text('feature_safety', persian)}
- {get_text('feature_structural', persian)}
""")
    
    # Standards Section
    st.markdown(f"### {get_text('standards_title', persian)}")
    st.markdown(get_text('standards_intro', persian))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(get_text('standards_current', persian))
        st.markdown("""
- **AS 3533.1-2009+A1-2011** - Amusement rides and devices - Design and construction
- **INSO 8987-1-2023** - Safety of amusement rides and amusement devices - Part 1: General requirements
- **INSO 8987-2-2022** - Safety of amusement rides and amusement devices - Part 2: Operation and maintenance
- **INSO 8987-3-2022** - Safety of amusement rides and amusement devices - Part 3: Requirements for inspection
- **ISO 17842-2-2022** - Safety of amusement rides and amusement devices - Part 2: Operation and maintenance
- **ISO 17842-3-2022** - Safety of amusement rides and amusement devices - Part 3: Requirements for inspection
- **ISO 17842-2023** - Safety of amusement rides and amusement devices
""")
        
        st.markdown(get_text('standards_legacy', persian))
        st.markdown("""
- **AS 3533.2-2009+A1-2011** - Amusement rides and devices - Operation and maintenance
- **AS 3533.3-2003 R2013** - Amusement rides and devices - Qualification of inspection personnel
- **INSO 8987-2-2009** - Safety of amusement rides (Previous edition)
- **INSO 8987-3-2003** - Safety of amusement rides (Previous edition)
- **INSO 8987-2009** - Safety of amusement rides (Previous edition)
""")
    
    with col2:
        st.markdown(get_text('standards_loads', persian))
        st.markdown("""
- **ISIRI 519** - Iranian National Standard - Design loads for buildings
- **AS 1170.4-2007(A1)** - Structural design actions - Wind actions
- **BS EN 1991-1-4:2005+A1-2010** - Eurocode 1: Actions on structures - Wind actions
- **DIN 18800-1-1990** - Structural steelwork - Design and construction
- **DIN 18800-2-1990** - Structural steelwork - Stability, buckling of shells
- **EN 1991-1-3:2003** - Eurocode 1: Actions on structures - Snow loads
- **EN 1993-1-9:2005** - Eurocode 3: Design of steel structures - Fatigue
- **EN1993-1-9-AC 2009** - Eurocode 3: Design of steel structures - Fatigue (Amendment)
- **ISIRI 2800** - Iranian Code of Practice for Seismic Resistant Design of Buildings (4th Edition)
""")
        
        st.markdown(get_text('standards_applications', persian))
        st.markdown(f"""
- {get_text('app_wind', persian)}
- {get_text('app_seismic', persian)}
- {get_text('app_structural', persian)}
- {get_text('app_safety', persian)}
""")
    
    st.markdown("---")
    
    # Warning Section
    st.warning(f"""
{get_text('warning_title', persian)}

{get_text('warning_intro', persian)}
- {get_text('warning_1', persian)}
- {get_text('warning_2', persian)}
- {get_text('warning_3', persian)}
- {get_text('warning_4', persian)}
- {get_text('warning_5', persian)}
""")
    
    st.markdown("---")
    
    # Confirmation checkbox
    standards_accepted = st.checkbox(
        get_text('confirm_checkbox', persian),
        key="standards_confirmation"
    )
    
    st.session_state.standards_confirmed = standards_accepted
    
    if standards_accepted:
        st.success(get_text('confirm_success', persian))
        if st.button(get_text('start_button', persian), type="primary"):
            st.session_state.step = 1
            st.rerun()
    else:
        st.info(get_text('confirm_info', persian))

# === STEP 1: Generation selection ===
if st.session_state.get('step', 0) == 1:
    st.header(get_text('select_generation', persian))
    st.markdown("---")

    image_files = [
        "./git/assets/1st.jpg",
        "./git/assets/2nd_1.jpg",
        "./git/assets/2nd_2.jpg",
        "./git/assets/4th.jpg",
    ]
    captions = [
        get_text('gen_1_truss', persian),
        get_text('gen_2_cable', persian),
        get_text('gen_2_pure_cable', persian),
        get_text('gen_4_hubless', persian)
    ]

    cols = st.columns(4, gap="small")
    for i, (col, img_path, caption) in enumerate(zip(cols, image_files, captions)):
        with col:
            if os.path.exists(img_path):
                st.image(img_path, width=240)
            else:
                st.error(f"Image not found: {img_path}")
            st.caption(caption)
            st.button(
                get_text("select", persian),
                key=f"gen_btn_{i}",
                on_click=select_generation,
                args=(caption,)
            )

    st.markdown("---")
    st.write(get_text("select the Ferris Wheel generation ", persian) or "Click the button under the image to select a generation and proceed.")
    st.markdown("---")

    left_col = st.container()
    with left_col:
        st.button("⬅️ Back", key="back_btn", on_click=go_back)



# === STEP 2: Cabin Geometry ===
if st.session_state.get("step", 0) == 2:
    st.header(get_text('select_cabin_geometry', persian))
    st.markdown("Choose a cabin shape.")
    
    geom_images = [
        (get_text('geom_square', persian), "./git/assets/square.jpg"),
        (get_text('geom_vert_cyl', persian), "./git/assets/vertical.jpg"),
        (get_text('geom_horiz_cyl', persian), "./git/assets/horizontal.jpg"),
        (get_text('geom_spherical', persian), "./git/assets/sphere.jpg"),
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
        

    for i, (label, img_path) in enumerate(geom_images):
        with cols[i]:
            try:
                st.image(img_path, use_column_width=True)
            except Exception as e:
                import os
                st.error(f"Could not load image: {img_path}")
                st.write("Exists:", os.path.exists(img_path))
                st.write("Abs path:", os.path.abspath(img_path))
                st.write("Error:", e)
            st.caption(label)
            if label == get_text('geom_spherical', persian):
                st.markdown(
                    f"<p style='font-size:12px; color:gray; text-align:center;'>{get_text('geom_spherical_caption', persian)}</p>",
                    unsafe_allow_html=True
                )
            st.button(
                get_text("select", persian),
                key=f"geom_img_btn_{i}",
                on_click=select_geometry_callback,
                args=(label,)
            )

    left_col = st.container()
    with left_col:
        st.button("⬅️ Back", key="geom_back_btn", on_click=go_back)


# === STEP 3: Primary parameters ===
elif st.session_state.step == 3:
    
    if st.session_state.get('scroll_to_top'):
        components.html(
            """
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>
            """,
            height=0,
        )
        st.session_state.scroll_to_top = False
    
    st.header(get_text('cabin specification', persian))
    st.subheader(f"Generation: {st.session_state.generation_type}")
    
    if st.session_state.get('validation_errors'):
        for e in st.session_state.validation_errors:
            st.error(e)
        st.session_state.validation_errors = []
    
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        diameter = st.number_input(get_text('diameter_label', persian), min_value=30, max_value=80, value=int(st.session_state.diameter), step=1, key="diameter_input")
        st.session_state.diameter = diameter

    geometry = st.session_state.cabin_geometry
    base = base_for_geometry(diameter, geometry) if geometry else (np.pi * diameter / 4.0)
    min_c, max_c = calc_min_max_from_base(base)

    num_cabins = st.number_input(get_text('num_cabins_label', persian), min_value=min_c, max_value=max_c, 
                                  value=min(max(int(st.session_state.num_cabins), min_c), max_c), step=1, key="num_cabins_input")
    st.session_state.num_cabins = num_cabins

    c1, c2 = st.columns(2)
    with c1:
        cabin_capacity = st.number_input(get_text('cabin_cap_label', persian), min_value=4, max_value=8, 
                                         value=st.session_state.cabin_capacity, step=1, key="cabin_capacity_input")
        st.session_state.cabin_capacity = cabin_capacity
    with c2:
        num_vip = st.number_input(get_text('num_vip_label', persian), min_value=0, max_value=st.session_state.num_cabins, 
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
    st.header(get_text('rotation_time', persian))
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
    
    if st.session_state.get('scroll_to_top'):
        components.html(
            """
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>
            """,
            height=0,
        )
        st.session_state.scroll_to_top = False
    
    st.header(get_text('environment_conditions', persian))
    
    
    if st.session_state.get('validation_errors'):
        for e in st.session_state.validation_errors:
            st.error(e)
        st.session_state.validation_errors = []
    
    st.markdown("**Design per AS 1170.4-2007(A1), EN 1991-1-4:2005, ISIRI 2800**")
    st.markdown("---")

    iran_provinces = list(TERRAIN_CATEGORIES.keys())

    c1, c2 = st.columns(2)
    with c1:
        province = st.selectbox(get_text('select_province', persian), options=iran_provinces, index=0, key="province_select")
        
        # City selection based on province
        cities = [city["city"] for city in CITIES_DATA.get(province, [])]
        if cities:
            city = st.selectbox(get_text('select_city', persian), options=cities, key="city_select")
        else:
            city = st.text_input(get_text('select_city', persian), key="city_input")
    
    with c2:
        region_name = st.text_input(
            get_text('region_name', persian),
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
            "second internal wind speed (km/h)",
            min_value=0,
            value=int(st.session_state.environment_data.get('wind_max', 108)),
            step=1,
            key="wind_max_input"
        )
        wind_max_ms = float(wind_max) / 3.6
        st.caption(f"speed: {wind_max_ms:.2f} m/s")

        wind_avg = st.number_input(
            "minutes internal wind speed (km/h)",
            min_value=0,
            value=int(st.session_state.environment_data.get('wind_avg', 54)),
            step=1,
            key="wind_avg_input"
        )
        wind_avg_ms = float(wind_avg) / 3.6
        st.caption(f"speed: {wind_avg_ms:.2f} m/s")

    st.markdown("---")
    load_wind = st.checkbox("Load wind rose (upload jpg/pdf)", value=st.session_state.get('wind_rose_loaded', False), key="load_wind_checkbox")
    st.session_state.wind_rose_loaded = load_wind
    if load_wind:
        wind_file = st.file_uploader("Wind rose file (jpg/pdf)", type=['jpg', 'jpeg', 'pdf'], key="wind_rose_uploader")
        st.session_state.wind_rose_file = wind_file

    if province in TERRAIN_CATEGORIES:
        terrain = TERRAIN_CATEGORIES[province]
        seismic = get_seismic_hazard_from_city(province, city)
    else:
        terrain = {"category": "II", "z0": 0.05, "zmin": 2, "desc": ""}
        seismic = "Unknown"

    st.session_state.environment_data = {
        'province': province, 'city': city, 'region_name': region_name, 'land_length': land_length, 'land_width': land_width,
        'land_area': land_length * land_width, 'altitude': altitude, 'temp_min': temp_min, 'temp_max': temp_max,
        'wind_direction': wind_dir, 'wind_max': wind_max, 'wind_avg': wind_avg,
        'terrain_category': terrain['category'],
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
    
    if st.session_state.get('scroll_to_top'):
        components.html(
            """
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>
            """,
            height=0,
        )
        st.session_state.scroll_to_top = False
    
    st.header(get_text('provincial_characteristics', persian))
    
    if st.session_state.get('validation_errors'):
        for e in st.session_state.validation_errors:
            st.error(e)
        st.session_state.validation_errors = []
    
    st.markdown("**Terrain classification per AS 1170.4-2007(A1), ISIRI 2800**")
    st.markdown("---")
    
    env = st.session_state.environment_data
    province = env.get('province', 'Tehran')
    city = env.get('city', '')
    
    st.subheader(f"Selected Province: {province}")
    st.subheader(f"Selected City: {city}")
    st.info(f"**Region:** {env.get('region_name', 'N/A')}")
    
    if province in TERRAIN_CATEGORIES:
        terrain = TERRAIN_CATEGORIES[province]
        seismic = get_seismic_hazard_from_city(province, city)
        
        st.markdown("---")
        st.subheader("Terrain Information")
        if st.button("🔄 Calculate Terrain Parameters", type="primary"):
            st.session_state.terrain_calculated = True
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Terrain Category:** {terrain['category']}")
                st.markdown(f"**Description:** {terrain.get('desc', 'N/A')}")
            with col2:
                seismic_color = {"Very High": "🔴", "High": "🟠", "Moderate": "🟡", "Low": "🟢", "Very Low": "🟢"}
                st.markdown(f"{seismic_color.get(seismic, '')} **Seismic Hazard (ISIRI 2800):** {seismic}")

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
    st.header(get_text('soil_type', persian))
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
if st.session_state.step == 8:
    if st.session_state.get('scroll_to_top'):
        components.html("<script>window.parent.document.querySelector('section.main').scrollTo(0, 0);</script>", height=0)
        st.session_state.scroll_to_top = False
    
    st.header(get_text('carousel_orientation', persian))
    st.markdown("---")

    env = st.session_state.get('environment_data', {})
    land_length = env.get('land_length', 100)
    land_width = env.get('land_width', 100)
    
    directions = ['North-South', 'Northeast-Southwest', 'East-West', 'Northwest-Southeast']
    
    col_ctrl, col_graph = st.columns([1, 2])
    
    with col_ctrl:
        # منوی انتخاب جهت (تغییر این، بلافاصله نمودار سمت راست را آپدیت می‌کند)
        selected_dir = st.selectbox(get_text('custom_direction', persian), options=directions, key="dir_selector")
        axis_key, arrow_text, arrow_vec = map_direction_to_axis_and_vector(selected_dir)
        
        if st.button("✅ Confirm Orientation", use_container_width=True):
            st.session_state.carousel_orientation = axis_key
            st.session_state.orientation_confirmed = True
            st.success("Confirmed!")

    with col_graph:
        st.write(f"**Land: {land_length}m × {land_width}m**")
        # فراخوانی نمودار فقط و فقط در اینجا
        fig = create_orientation_diagram(axis_key, land_length, land_width, arrow_vec, arrow_text)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.button("⬅️ Back", on_click=go_back)
    with c2: st.button("Next ➡️", on_click=validate_current_step_and_next)

# === STEP 9: Device Classification ===
elif st.session_state.step == 9:
    st.header(get_text('device_classification', persian))
    
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
    
    st.subheader("Braking Acceleration Parameter" if not persian else "پارامتر شتاب ترمز")
    st.info("⚠️ **Note:** Enter your actual braking acceleration for the design analysis" if not persian else 
            "⚠️ **توجه:** شتاب ترمز واقعی خود را برای تحلیل طراحی وارد کنید")
    
    braking_accel = st.number_input(
        "Braking Acceleration (m/s²)" if not persian else "شتاب ترمز (متر بر مجذور ثانیه)", 
        min_value=0.01, max_value=2.0, 
        value=st.session_state.braking_acceleration, 
        step=0.01, format="%.2f", 
        key="braking_accel_input",
        help="Actual braking acceleration for your design" if not persian else "شتاب ترمز واقعی برای طراحی شما"
    )
    st.session_state.braking_acceleration = braking_accel
    
    st.markdown("---")
    st.subheader("Additional Load Factors" if not persian else "بارهای اضافی")
    
    # Initialize session state variables if not present
    if 'enable_snow' not in st.session_state:
        st.session_state.enable_snow = False
    if 'enable_wind' not in st.session_state:
        st.session_state.enable_wind = False
    if 'enable_earthquake' not in st.session_state:
        st.session_state.enable_earthquake = False
    if 'snow_coefficient' not in st.session_state:
        st.session_state.snow_coefficient = 0.2
    if 'terror_factor' not in st.session_state:
        st.session_state.terror_factor = 1.0
    if 'height_factor' not in st.session_state:
        st.session_state.height_factor = 1.0
    if 'seismic_coefficient' not in st.session_state:
        st.session_state.seismic_coefficient = 0.15
    
    # محاسبه خودکار مساحت سطح کابین
    cabin_geometry = st.session_state.get('cabin_geometry', 'Square')
    cabin_capacity = st.session_state.get('cabin_capacity', 6)
    cabin_surface_area = estimate_cabin_surface_area(cabin_geometry, cabin_capacity, diameter)
    
    col1, col2, col3 = st.columns(3)
    
    # Snow Load
    with col1:
        enable_snow = st.checkbox("🌨️ Snow Load" if not persian else "🌨️ بار برف", 
                                  value=st.session_state.enable_snow,
                                  key="snow_checkbox")
        st.session_state.enable_snow = enable_snow
        
        if enable_snow:
            st.info(f"**Cabin Surface Area (estimated):**\n{cabin_surface_area} m²\n\n"
                   f"Based on: {cabin_geometry}, {cabin_capacity} passengers" if not persian else
                   f"**مساحت سطح کابین (تخمین):**\n{cabin_surface_area} متر مربع\n\n"
                   f"بر اساس: {cabin_geometry}، {cabin_capacity} مسافر")
            
            snow_coef = st.number_input(
                "Snow Pressure (kN/m²)" if not persian else "فشار برف (کیلونیوتن بر متر مربع)", 
                min_value=0.1, max_value=1.0, 
                value=st.session_state.snow_coefficient, 
                step=0.05, 
                format="%.2f",
                key="snow_coef_input",
                help="Standard value: 0.2 kN/m² (modifiable)" if not persian else "مقدار استاندارد: 0.2 (قابل تغییر)"
            )
            st.session_state.snow_coefficient = snow_coef
            
            snow_load_calc = snow_coef * cabin_surface_area
            st.caption(f"Snow Load = {snow_coef} × {cabin_surface_area} = **{snow_load_calc:.2f} kN**")
    
    # Wind Load
    with col2:
        enable_wind = st.checkbox("💨 Wind Load" if not persian else "💨 بار باد", 
                                  value=st.session_state.enable_wind,
                                  key="wind_checkbox")
        st.session_state.enable_wind = enable_wind
        
        if enable_wind:
            st.info(f"**Cabin Surface Area (estimated):**\n{cabin_surface_area} m²" if not persian else
                   f"**مساحت سطح کابین (تخمین):**\n{cabin_surface_area} متر مربع")
            
            if 'height_category_index' not in st.session_state:
                st.session_state.height_category_index = 0
            
            height_category = st.selectbox(
                "Height Category (m)" if not persian else "دسته‌بندی ارتفاع (متر)",
                options=["0 < H ≤ 8", "8 < H ≤ 20", "20 < H ≤ 35", "35 < H ≤ 50"],
                index=st.session_state.height_category_index,
                key="height_category"
            )
            
            if 'height_category_value' not in st.session_state or st.session_state.height_category_value != height_category:
                st.session_state.height_category_value = height_category
            
            wind_pressure_map = {
                "0 < H ≤ 8": 0.20,
                "8 < H ≤ 20": 0.30,
                "20 < H ≤ 35": 0.35,
                "35 < H ≤ 50": 0.40
            }
            wind_pressure = wind_pressure_map[height_category]
            st.session_state.wind_pressure = wind_pressure
            st.caption(f"Wind pressure q: {wind_pressure} kN/m²")
            
            st.markdown("**Design Factors:**" if not persian else "**ضرایب طراحی:**")
            terror_factor = st.slider("Terror Factor" if not persian else "فاکتور وحشت", 
                                     min_value=1.0, max_value=5.0, value=st.session_state.terror_factor, step=0.5,
                                     key="terror_factor_slider")
            st.session_state.terror_factor = terror_factor
            
            height_factor = st.slider("Height Factor" if not persian else "فاکتور ارتفاع", 
                                     min_value=1.0, max_value=5.0, value=st.session_state.height_factor, step=0.5,
                                     key="height_factor_slider")
            st.session_state.height_factor = height_factor
            
            wind_load_calc = wind_pressure * cabin_surface_area * terror_factor * height_factor
            st.caption(f"Wind Load = {wind_pressure} × {cabin_surface_area} × {terror_factor} × {height_factor} = **{wind_load_calc:.2f} kN**")
    
    # Earthquake Load
    with col3:
        enable_earthquake = st.checkbox("🌍 Earthquake Load" if not persian else "🌍 بار زلزله", 
                                       value=st.session_state.enable_earthquake,
                                       key="earthquake_checkbox")
        st.session_state.enable_earthquake = enable_earthquake
        
        if enable_earthquake:
            st.caption("Seismic loads" if not persian else "بارهای لرزه‌ای")
            
            seismic_coef = st.number_input("Seismic Coefficient" if not persian else "ضریب زلزله", 
                                          min_value=0.0, max_value=0.5, 
                                          value=st.session_state.seismic_coefficient, step=0.01, format="%.3f",
                                          key="seismic_coef_input",
                                          help="Typical range: 0.10 - 0.35")
            st.session_state.seismic_coefficient = seismic_coef
            
            approx_mass = diameter * 500
            earthquake_load_calc = seismic_coef * (approx_mass * 9.81 / 1000)
            
            st.caption(f"Approx. cabin mass: {approx_mass:.0f} kg")
            st.caption(f"Horizontal force: {seismic_coef} × {approx_mass * 9.81 / 1000:.1f} = **{earthquake_load_calc:.2f} kN**")
            st.caption(f"Vertical force: **{earthquake_load_calc * 0.5:.2f} kN** (50% of horizontal)")
    
    st.markdown("---")
    
    # Calculate additional loads
    snow_load = 0.0
    wind_load = 0.0
    earthquake_load = 0.0
    
    if st.session_state.enable_snow:
        snow_load = st.session_state.snow_coefficient * cabin_surface_area
    
    if st.session_state.enable_wind:
        wind_load = (st.session_state.wind_pressure * cabin_surface_area * 
                    st.session_state.terror_factor * st.session_state.height_factor)
    
    if st.session_state.enable_earthquake:
        approx_mass = diameter * 500
        earthquake_load = st.session_state.seismic_coefficient * (approx_mass * 9.81 / 1000)
    
    # === ACTUAL OPERATION ANALYSIS (تحلیل طراحی واقعی) ===
    st.subheader("⚙️ Device Classification Analysis" if not persian else "⚙️ تحلیل طبقه‌بندی دستگاه")
    st.markdown("**Based on Your Design Parameters:**" if not persian else "**بر اساس پارامترهای طراحی شما:**")
    
    # نمایش پارامترهای ورودی
    param_col1, param_col2, param_col3 = st.columns(3)
    with param_col1:
        st.metric("Rotation Speed" if not persian else "سرعت چرخش", f"{rpm:.4f} rpm")
    with param_col2:
        st.metric("Braking Acceleration" if not persian else "شتاب ترمز", f"{braking_accel:.2f} m/s²")
    with param_col3:
        st.metric("Diameter" if not persian else "قطر", f"{diameter} m")
    
    # محاسبه Dynamic Product
    p_actual, n_actual, max_accel_actual = calculate_dynamic_product(
        diameter, height, angular_velocity, braking_accel,
        snow_load, wind_load, earthquake_load
    )
    
    # طبقه‌بندی بر اساس دو جدول
    def classify_intrinsic_secured(p):
        """Intrinsic safety secured"""
        if 0.1 < p <= 25:
            return 1
        elif 25 < p <= 100:
            return 2
        elif 100 < p <= 200:
            return 3
        elif p > 200:
            return 4
        else:
            return None
    
    def classify_intrinsic_not_secured(p):
        """Intrinsic safety not secured"""
        if 0.1 < p <= 25:
            return 2
        elif 25 < p <= 100:
            return 3
        elif 100 < p <= 200:
            return 4
        elif p > 200:
            return 5
        else:
            return None
    
    class_secured = classify_intrinsic_secured(p_actual)
    class_not_secured = classify_intrinsic_not_secured(p_actual)
    
    st.markdown("---")
    st.markdown("**Calculated Values:**" if not persian else "**مقادیر محاسبه شده:**")
    
    result_col1, result_col2, result_col3 = st.columns(3)
    with result_col1:
        st.metric("Max Acceleration" if not persian else "حداکثر شتاب", 
                 f"{max_accel_actual:.3f} m/s²")
        st.caption(f"({n_actual:.3f}g)")
    with result_col2:
        st.metric("Dynamic Product (p)" if not persian else "حاصل‌ضرب دینامیکی", 
                 f"{p_actual:.2f}")
    with result_col3:
        st.metric("Linear Velocity" if not persian else "سرعت خطی", 
                 f"{(diameter/2.0) * angular_velocity:.3f} m/s")
    
    # نمایش دو نوع طبقه‌بندی
    st.markdown("---")
    st.subheader("📋 Device Classification per INSO 8987-1-2023" if not persian else 
                "📋 طبقه‌بندی دستگاه طبق INSO 8987-1-2023")
    
    class_col1, class_col2 = st.columns(2)
    
    with class_col1:
        st.markdown("#### **Intrinsic Safety Secured**" if not persian else "#### **ایمنی ذاتی تأمین شده**")
        st.success(f"**Class {class_secured}**")
        
        # جدول محدوده‌ها
        st.markdown("""
| Class | Dynamic Product (P) |
|-------|---------------------|
| 1     | 0.1 < P ≤ 25        |
| 2     | 25 < P ≤ 100        |
| 3     | 100 < P ≤ 200       |
| 4     | 200 < P             |
""")
        
        if class_secured == 1:
            st.info("✅ Lowest classification - Minimal restraint requirements")
        elif class_secured == 2:
            st.info("✅ Low to moderate classification - Standard restraint")
        elif class_secured == 3:
            st.warning("⚠️ Moderate to high classification - Enhanced restraint required")
        elif class_secured == 4:
            st.error("⚠️ Highest classification - Maximum restraint required")
    
    with class_col2:
        st.markdown("#### **Intrinsic Safety NOT Secured**" if not persian else "#### **ایمنی ذاتی تأمین نشده**")
        st.warning(f"**Class {class_not_secured}**")
        
        # جدول محدوده‌ها
        st.markdown("""
| Class | Dynamic Product (P) |
|-------|---------------------|
| 2     | 0.1 < P ≤ 25        |
| 3     | 25 < P ≤ 100        |
| 4     | 100 < P ≤ 200       |
| 5     | 200 < P             |
""")
        
        if class_not_secured == 2:
            st.info("⚠️ Requires additional safety measures")
        elif class_not_secured == 3:
            st.warning("⚠️ Enhanced safety measures required")
        elif class_not_secured == 4:
            st.error("⚠️ Comprehensive safety system required")
        elif class_not_secured == 5:
            st.error("🚨 Maximum safety classification - Special precautions mandatory")
    
    # Display load contributions if any are enabled 
    if any([st.session_state.enable_snow, st.session_state.enable_wind, st.session_state.enable_earthquake]):
        st.markdown("---")
        st.markdown("**🌦️ Additional Load Contributions:**" if not persian else "**🌦️ مشارکت بارهای اضافی:**")
        st.caption("These loads are included in the analysis above" if not persian else 
                  "این بارها در تحلیل بالا لحاظ شده‌اند")
        
        load_col1, load_col2, load_col3 = st.columns(3)
        
        with load_col1:
            if st.session_state.enable_snow:
                st.metric("Snow Load" if not persian else "بار برف", f"{snow_load:.3f} kN")
                st.caption(f"{st.session_state.snow_coefficient} kN/m² × {cabin_surface_area} m²")
        
        with load_col2:
            if st.session_state.enable_wind:
                st.metric("Wind Load" if not persian else "بار باد", f"{wind_load:.3f} kN")
                st.caption(f"With terror={st.session_state.terror_factor}, height={st.session_state.height_factor}")
        
        with load_col3:
            if st.session_state.enable_earthquake:
                st.metric("Earthquake Load" if not persian else "بار زلزله", f"{earthquake_load:.3f} kN")
                st.caption(f"Coef={st.session_state.seismic_coefficient:.3f}")
    
    # ذخیره اطلاعات کامل برای Step 10 و 11
    st.session_state.classification_data = {
        'p_actual': p_actual, 
        'class_secured': class_secured, 
        'class_not_secured': class_not_secured,
        'max_accel_actual': max_accel_actual, 
        'n_actual': n_actual,
        'rpm_actual': rpm,
        'angular_velocity': angular_velocity,
        'braking_accel': braking_accel,
        'snow_load': snow_load, 
        'wind_load': wind_load, 
        'earthquake_load': earthquake_load,
        'cabin_surface_area': cabin_surface_area,
        'snow_coefficient': st.session_state.snow_coefficient,
    }
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)


# === STEP 10: Restraint Type (Both ISO and AS Standards) ===
elif st.session_state.step == 10:
    st.header(get_text('restraint_type', persian))
    st.image("assets/Axis_Guide.jpg", 
            caption="Axis Guide" if not persian else "راهنمای محورها",
            use_column_width=True)
    st.markdown("**ISO 17842-2023 & AS 3533.1-2009+A1-2011**")
    st.markdown("---")

    # دریافت داده‌های واقعی از Step 9
    diameter = st.session_state.diameter
    classification_data = st.session_state.get('classification_data', {})
    
    angular_velocity = classification_data.get('angular_velocity', 0.0)
    braking_accel = classification_data.get('braking_accel', st.session_state.braking_acceleration)
    rpm_actual = classification_data.get('rpm_actual', 0.0)
    
    # Get additional loads from classification data
    snow_load = classification_data.get('snow_load', 0.0)
    wind_load = classification_data.get('wind_load', 0.0)
    earthquake_load = classification_data.get('earthquake_load', 0.0)
    
    st.subheader("Passenger Acceleration Analysis" if not persian else "تحلیل شتاب مسافران")
    
    # Display design parameters
    st.info(f"""**Design Parameters:**
- Rotation Speed: {rpm_actual:.4f} rpm
- Braking Acceleration: {braking_accel:.2f} m/s²
- Diameter: {diameter} m""" if not persian else
f"""**پارامترهای طراحی:**
- سرعت چرخش: {rpm_actual:.4f} دور در دقیقه
- شتاب ترمز: {braking_accel:.2f} متر بر مجذور ثانیه
- قطر: {diameter} متر""")
    
    # Display active loads
    if any([snow_load > 0, wind_load > 0, earthquake_load > 0]):
        st.info("**Active Additional Loads:**" if not persian else "**بارهای اضافی فعال:**")
        load_info = []
        if snow_load > 0:
            load_info.append(f"🌨️ Snow: {snow_load:.2f} kN")
        if wind_load > 0:
            load_info.append(f"💨 Wind: {wind_load:.2f} kN")
        if earthquake_load > 0:
            load_info.append(f"🌍 Earthquake: {earthquake_load:.2f} kN")
        st.write(" | ".join(load_info))
        st.markdown("---")
    
    # محاسبه شتاب‌ها در تمام زوایا
    theta_vals = np.linspace(0, 2*np.pi, 360)
    max_ax = -float('inf')
    max_az = -float('inf')
    min_ax = float('inf')
    min_az = float('inf')
    restraint_zones_iso = []
    restraint_zones_as = []
    
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(
            theta, diameter, angular_velocity, braking_accel,
            snow_load, wind_load, earthquake_load
        )
        a_x_g = a_x / 9.81
        a_z_g = a_z / 9.81
        
        # ✅ برای نمایش: az را قرینه می‌کنیم
        a_z_g_mirrored = -a_z_g
        
        if a_x_g > max_ax:
            max_ax = a_x_g
        if a_z_g_mirrored > max_az:  # ✅ استفاده از مقدار قرینه شده
            max_az = a_z_g_mirrored
        if a_x_g < min_ax:
            min_ax = a_x_g
        if a_z_g_mirrored < min_az:  # ✅ استفاده از مقدار قرینه شده
            min_az = a_z_g_mirrored
        
        # ✅ Zone را بر اساس موقعیت قرینه شده تشخیص می‌دهیم
        zone_iso = determine_restraint_area_iso(a_x_g, a_z_g_mirrored)
        restraint_zones_iso.append(zone_iso)
        
        zone_as = determine_restraint_area_as(a_x_g, a_z_g_mirrored)
        restraint_zones_as.append(zone_as)
    
    from collections import Counter
    zone_counts_iso = Counter(restraint_zones_iso)
    predominant_zone_iso = zone_counts_iso.most_common(1)[0][0]
    
    zone_counts_as = Counter(restraint_zones_as)
    predominant_zone_as = zone_counts_as.most_common(1)[0][0]
    
    # نمایش محدوده شتاب‌ها
    st.markdown("**Acceleration Ranges:**" if not persian else "**محدوده شتاب‌ها:**")
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
        1: "Zone 1 - Upper region: Maximum restraint required (full body harness)",
        2: "Zone 2 - Upper-central: Enhanced restraint (over-shoulder restraint)",
        3: "Zone 3 - Central edges: Standard restraint (lap bar or seat belt)",
        4: "Zone 4 - Lower-central: Moderate restraint (seat belt with lap bar)",
        5: "Zone 5 - Lower region: Special consideration required (enhanced harness system)"
    }
    
    st.success(f"**Predominant Zone (ISO):** {predominant_zone_iso}")
    st.info(f"**Recommended Restraint (ISO):** {restraint_descriptions_iso.get(predominant_zone_iso, 'Standard restraint')}")
    
    # AS Standard Results
    st.markdown("---")
    st.subheader("📋 AS 3533.1-2009+A1-2011 Analysis")
    
    restraint_descriptions_as = {
        1: "Zone 1 - Upper region: Maximum restraint required (full body harness)",
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
        fig_accel_iso = plot_acceleration_envelope_iso(
            diameter, angular_velocity, braking_accel,
            snow_load, wind_load, earthquake_load
        )
        st.plotly_chart(fig_accel_iso, use_container_width=True)
        
        st.markdown("""
        **ISO Zone Classifications:**
        - **Zone 1** (Purple): Maximum restraint
        - **Zone 2** (Orange): Enhanced restraint
        - **Zone 3** (Yellow): Standard restraint
        - **Zone 4** (Green): Moderate restraint
        - **Zone 5** (Red): Special consideration
        """)
        
        st.markdown("**📊 Points Distribution in Zones (ISO):**")
        total_points = len(restraint_zones_iso)
        for zone in sorted(zone_counts_iso.keys()):
            count = zone_counts_iso[zone]
            percentage = (count / total_points) * 100
            st.write(f"- Zone {zone}: {count} points ({percentage:.1f}%)")
    
    with col_as:
        st.subheader("AS 3533.1 Acceleration Envelope")
        fig_accel_as = plot_acceleration_envelope_as(
            diameter, angular_velocity, braking_accel,
            snow_load, wind_load, earthquake_load
        )
        st.plotly_chart(fig_accel_as, use_container_width=True)
        
        st.markdown("""
        **AS Zone Classifications:**
        - **Zone 1** (Purple): Maximum restraint
        - **Zone 2** (Orange): Enhanced restraint
        - **Zone 3** (Yellow): Standard restraint
        - **Zone 4** (Green): Moderate restraint
        - **Zone 5** (Red): Special consideration
        """)
        
        st.markdown("**📊 Points Distribution in Zones (AS):**")
        total_points = len(restraint_zones_as)
        for zone in sorted(zone_counts_as.keys()):
            count = zone_counts_as[zone]
            percentage = (count / total_points) * 100
            st.write(f"- Zone {zone}: {count} points ({percentage:.1f}%)")
    
    # به‌روزرسانی classification_data با اطلاعات مهاربند
    st.session_state.classification_data.update({
        'restraint_zone_iso': predominant_zone_iso,
        'restraint_zone_as': predominant_zone_as,
        'max_ax_g': max_ax,
        'max_az_g': max_az,
        'min_ax_g': min_ax,
        'min_az_g': min_az,
        'restraint_description_iso': restraint_descriptions_iso.get(predominant_zone_iso, 'Standard restraint'),
        'restraint_description_as': restraint_descriptions_as.get(predominant_zone_as, 'Standard restraint'),
        'zone_distribution_iso': dict(zone_counts_iso),
        'zone_distribution_as': dict(zone_counts_as)
    })
    
    st.markdown("---")
    left_col, right_col = st.columns([1,1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)

# === STEP 11: Final Design Overview ===
elif st.session_state.step == 11:
    st.header(get_text('design_summary', persian))
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
        st.write(f"**City:** {env.get('city','N/A')}")
        st.write(f"**Region:** {env.get('region_name','N/A')}")
        st.write(f"**Land Area:** {env.get('land_area',0):.2f} m²")
        st.write(f"**Altitude:** {env.get('altitude',0)} m")
        st.write(f"**Temperature Range:** {env.get('temp_min',0)}°C to {env.get('temp_max',0)}°C")
    with col2:
        st.write(f"**Terrain Category:** {env.get('terrain_category','N/A')}")
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

    axis_key = st.session_state.get('carousel_orientation', None)

    if axis_key:
        st.write(f"**Selected Orientation:** {axis_label(axis_key)}")
        arrow_map = {
            'NS': (0, 1, axis_label('NS')),
            'EW': (1, 0, axis_label('EW')),
            'NE_SW': (1/math.sqrt(2), 1/math.sqrt(2), axis_label('NE_SW')),
            'SE_NW': (-1/math.sqrt(2), 1/math.sqrt(2), axis_label('SE_NW'))
        }
        arrow_vec_x, arrow_vec_y, arrow_text = arrow_map.get(axis_key, (0,1,axis_label('NS')))
        arrow_vec = (arrow_vec_x, arrow_vec_y)
        fig_final_orientation = create_orientation_diagram(
            axis_key,
            env.get('land_length'),
            env.get('land_width'),
            arrow_vec,
            arrow_text
        )
        st.plotly_chart(fig_final_orientation, use_container_width=True)
    else:
        st.write("**Selected Orientation:** N/A")

    st.markdown("---")
    
    # Safety Classification - اصلاح شده با دو نوع Classification
    st.subheader("⚠️ Safety Classification")
    st.caption("Per INSO 8987-1-2023")
    if st.session_state.classification_data:
        class_data = st.session_state.classification_data
        
        # نمایش پارامترهای عملیاتی
        st.markdown("**Operational Parameters:**")
        param_col1, param_col2, param_col3 = st.columns(3)
        with param_col1:
            rpm_actual = class_data.get('rpm_actual', 0)
            st.metric("Rotation Speed", f"{rpm_actual:.4f} rpm")
        with param_col2:
            braking_accel = class_data.get('braking_accel', st.session_state.braking_acceleration)
            st.metric("Braking Acceleration", f"{braking_accel:.2f} m/s²")
        with param_col3:
            st.metric("Max Acceleration", f"{class_data.get('n_actual',0):.3f}g")
        
        st.markdown("---")
        
        # دو نوع Classification
        st.markdown("**Device Classification (INSO 8987-1-2023):**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Intrinsic Safety **SECURED**")
            class_secured = class_data.get('class_secured', 'N/A')
            p_actual = class_data.get('p_actual', 0)
            
            if class_secured != 'N/A':
                st.success(f"**Class {class_secured}**")
                st.caption(f"Dynamic Product (p): {p_actual:.2f}")
                
                # توضیحات
                secured_desc = {
                    1: "Lowest classification - Minimal restraint requirements",
                    2: "Low to moderate classification - Standard restraint",
                    3: "Moderate to high classification - Enhanced restraint required",
                    4: "Highest classification - Maximum restraint required"
                }
                st.info(secured_desc.get(class_secured, "Standard restraint"))
                
                # جدول محدوده‌ها
                st.markdown("""
**Classification Ranges:**
- Class 1: 0.1 < P ≤ 25
- Class 2: 25 < P ≤ 100
- Class 3: 100 < P ≤ 200
- Class 4: 200 < P
""")
        
        with col2:
            st.markdown("#### Intrinsic Safety **NOT Secured**")
            class_not_secured = class_data.get('class_not_secured', 'N/A')
            
            if class_not_secured != 'N/A':
                st.warning(f"**Class {class_not_secured}**")
                st.caption(f"Dynamic Product (p): {p_actual:.2f}")
                
                # توضیحات
                not_secured_desc = {
                    2: "Requires additional safety measures",
                    3: "Enhanced safety measures required",
                    4: "Comprehensive safety system required",
                    5: "Maximum safety classification - Special precautions mandatory"
                }
                st.info(not_secured_desc.get(class_not_secured, "Additional safety measures required"))
                
                # جدول محدوده‌ها
                st.markdown("""
**Classification Ranges:**
- Class 2: 0.1 < P ≤ 25
- Class 3: 25 < P ≤ 100
- Class 4: 100 < P ≤ 200
- Class 5: 200 < P
""")
        
        # Display additional loads if any are active
        snow_load = class_data.get('snow_load', 0.0)
        wind_load = class_data.get('wind_load', 0.0)
        earthquake_load = class_data.get('earthquake_load', 0.0)
        
        if any([snow_load > 0, wind_load > 0, earthquake_load > 0]):
            st.markdown("---")
            st.subheader("🌦️ Additional Load Factors")
            st.caption("Environmental and seismic loads included in analysis")
            
            load_col1, load_col2, load_col3 = st.columns(3)
            
            with load_col1:
                if snow_load > 0:
                    cabin_area = class_data.get('cabin_surface_area', 0)
                    snow_coef = class_data.get('snow_coefficient', 0.2)
                    st.metric("🌨️ Snow Load", f"{snow_load:.2f} kN")
                    st.caption(f"Pressure: {snow_coef:.2f} kN/m²")
                    st.caption(f"Area: {cabin_area:.2f} m²")
                else:
                    st.write("🌨️ Snow Load: Not applied")
            
            with load_col2:
                if wind_load > 0:
                    st.metric("💨 Wind Load", f"{wind_load:.2f} kN")
                    if st.session_state.get('enable_wind', False):
                        st.caption(f"Terror Factor: {st.session_state.get('terror_factor', 1.0):.1f}")
                        st.caption(f"Height Factor: {st.session_state.get('height_factor', 1.0):.1f}")
                else:
                    st.write("💨 Wind Load: Not applied")
            
            with load_col3:
                if earthquake_load > 0:
                    st.metric("🌍 Earthquake Load", f"{earthquake_load:.2f} kN")
                    if st.session_state.get('enable_earthquake', False):
                        st.caption(f"Seismic Coef: {st.session_state.get('seismic_coefficient', 0.15):.3f}")
                else:
                    st.write("🌍 Earthquake Load: Not applied")
        
        st.markdown("---")
        st.subheader("🔒 Restraint System Requirements")
        col_iso, col_as = st.columns(2)
        with col_iso:
            st.info(f"**ISO 17842-2023**\n\nZone {class_data.get('restraint_zone_iso','N/A')}\n\n{class_data.get('restraint_description_iso', 'N/A')}")
        with col_as:
            st.info(f"**AS 3533.1-2009+A1-2011**\n\nZone {class_data.get('restraint_zone_as','N/A')}\n\n{class_data.get('restraint_description_as', 'N/A')}")

    st.markdown("---")
    
    # محاسبه صحیح توان موتور
    power_data = calculate_motor_power(
        st.session_state.diameter,
        st.session_state.num_cabins,
        st.session_state.cabin_capacity,
        st.session_state.num_vip_cabins,
        st.session_state.rotation_time_min,
        st.session_state.cabin_geometry
    )
    
    # Motor & Drive System
    st.subheader("⚙️ Motor & Drive System")
    st.caption("Calculated based on total system mass and operational requirements")
    
    motor_col1, motor_col2, motor_col3, motor_col4 = st.columns(4)
    with motor_col1:
        st.metric("Rated Power", f"{power_data['rated_power']:.1f} kW", 
                 help="Rated motor power with safety factor 1.5")
    with motor_col2:
        st.metric("Peak Power", f"{power_data['peak_power']:.1f} kW",
                 help="Peak power required during startup")
    with motor_col3:
        st.metric("Operational", f"{power_data['operational_power']:.1f} kW",
                 help="Steady-state operational power")
    with motor_col4:
        breakdown = power_data['breakdown']
        st.metric("Total Mass", f"{breakdown['total_mass']/1000:.1f} ton",
                 help="Total system mass including structure")
    
    # نمایش جزئیات محاسبات
    with st.expander("🔍 View Motor Power Calculation Details"):
        st.markdown(format_power_breakdown(power_data))
    
    st.markdown("---")
    
    # Visualization
    st.subheader("📊 Design Visualization")
    height = st.session_state.diameter * 1.1
    vip_cap = max(0, st.session_state.cabin_capacity - 2)
    total_capacity_per_rotation = (st.session_state.num_vip_cabins * vip_cap + 
                                   (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity)

    ang = (2.0 * np.pi) / (st.session_state.rotation_time_min * 60.0) if st.session_state.rotation_time_min else 0.0
    num_cabins = st.session_state.num_cabins
    cabin_geometry = st.session_state.cabin_geometry
    
    fig = create_component_diagram(st.session_state.diameter, height, 
                                   total_capacity_per_rotation, 
                                   power_data['rated_power'],
                                   num_cabins, cabin_geometry)
    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})

    st.markdown("---")
    
    # Design Summary Report
    st.subheader("📄 Design Summary Report")
    
    # Get additional load information for report
    snow_load = class_data.get('snow_load', 0.0) if st.session_state.classification_data else 0.0
    wind_load = class_data.get('wind_load', 0.0) if st.session_state.classification_data else 0.0
    earthquake_load = class_data.get('earthquake_load', 0.0) if st.session_state.classification_data else 0.0
    
    # Build additional loads section for report
    additional_loads_report = ""
    if any([snow_load > 0, wind_load > 0, earthquake_load > 0]):
        additional_loads_report = "\n### Additional Load Factors\n"
        
        if snow_load > 0:
            cabin_area = class_data.get('cabin_surface_area', 0)
            snow_coef = class_data.get('snow_coefficient', 0.2)
            additional_loads_report += f"""
#### Snow Load
- **Applied Load:** {snow_load:.2f} kN
- **Snow Pressure:** {snow_coef:.2f} kN/m²
- **Cabin Surface Area (estimated):** {cabin_area:.2f} m²
- **Cabin Geometry:** {st.session_state.get('cabin_geometry', 'N/A')}
- **Calculation:** {snow_coef} × {cabin_area} = {snow_load:.2f} kN
"""
        
        if wind_load > 0:
            wind_pressure = st.session_state.get('wind_pressure', 0)
            height_category = st.session_state.get('height_category_value', 'N/A')
            terror_factor = st.session_state.get('terror_factor', 1.0)
            height_factor = st.session_state.get('height_factor', 1.0)
            cabin_area = class_data.get('cabin_surface_area', 0)
            additional_loads_report += f"""
#### Wind Load
- **Applied Load:** {wind_load:.2f} kN
- **Wind Pressure:** {wind_pressure:.2f} kN/m²
- **Height Category:** {height_category}
- **Terror Factor:** {terror_factor:.1f}
- **Height Factor:** {height_factor:.1f}
- **Cabin Surface Area:** {cabin_area:.2f} m²
- **Calculation:** {wind_pressure} × {cabin_area} × {terror_factor} × {height_factor} = {wind_load:.2f} kN
"""
        
        if earthquake_load > 0:
            seismic_coef = st.session_state.get('seismic_coefficient', 0.15)
            approx_mass = st.session_state.diameter * 500
            additional_loads_report += f"""
#### Earthquake Load
- **Applied Horizontal Load:** {earthquake_load:.2f} kN
- **Seismic Coefficient:** {seismic_coef:.3f}
- **Approximate Cabin Mass:** {approx_mass:.0f} kg
- **Vertical Component:** {earthquake_load * 0.5:.2f} kN (50% of horizontal)
- **Calculation:** {seismic_coef} × ({approx_mass} × 9.81 / 1000) = {earthquake_load:.2f} kN
"""
    
    # دریافت مقادیر برای گزارش
    rpm_actual = class_data.get('rpm_actual', 0) if st.session_state.classification_data else 0
    braking_accel = class_data.get('braking_accel', st.session_state.braking_acceleration) if st.session_state.classification_data else 0
    class_secured = class_data.get('class_secured', 'N/A') if st.session_state.classification_data else 'N/A'
    class_not_secured = class_data.get('class_not_secured', 'N/A') if st.session_state.classification_data else 'N/A'
    p_actual = class_data.get('p_actual', 0) if st.session_state.classification_data else 0
    
    with st.expander("📋 View Complete Design Report"):
        st.markdown(f"""
        ## Ferris Wheel Design Report
        
        ### Project Information
        - **Project Name:** {env.get('region_name', 'N/A')} Ferris Wheel
        - **Location:** {env.get('province', 'N/A')}, {env.get('city', 'N/A')}, Iran
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
        - **Rotational Speed:** {rpm_actual:.4f} rpm
        - **Linear Speed at Rim:** {ang * (st.session_state.diameter / 2.0):.3f} m/s
        - **Braking Acceleration:** {braking_accel:.2f} m/s²
        
        ### Motor & Drive System
        - **Rated Motor Power:** {power_data['rated_power']:.1f} kW (with safety factor 1.5)
        - **Peak Power (Startup):** {power_data['peak_power']:.1f} kW
        - **Operational Power (Steady-State):** {power_data['operational_power']:.1f} kW
        - **Total System Mass:** {breakdown['total_mass']/1000:.1f} tons
          - Passengers: {breakdown['mass_passengers']/1000:.1f} tons
          - Cabins: {breakdown['mass_cabins']/1000:.1f} tons
          - Structure: {breakdown['mass_structure']/1000:.1f} tons
          - Axis & Equipment: {breakdown['mass_axis']/1000:.1f} tons
        - **Moment of Inertia:** {breakdown['moment_of_inertia']:.0f} kg⋅m²
        - **Angular Velocity:** {breakdown['angular_velocity']:.6f} rad/s
        - **Startup Time:** {breakdown['startup_time']:.0f} seconds
        
        ### Site Conditions
        - **Province:** {env.get('province', 'N/A')}
        - **City:** {env.get('city', 'N/A')}
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
        
        #### Intrinsic Safety SECURED
        - **Classification:** Class {class_secured}
        - **Dynamic Product (p):** {p_actual:.2f}
        - **Range:** 
          - Class 1: 0.1 < P ≤ 25
          - Class 2: 25 < P ≤ 100
          - Class 3: 100 < P ≤ 200
          - Class 4: 200 < P
        
        #### Intrinsic Safety NOT Secured
        - **Classification:** Class {class_not_secured}
        - **Dynamic Product (p):** {p_actual:.2f}
        - **Range:**
          - Class 2: 0.1 < P ≤ 25
          - Class 3: 25 < P ≤ 100
          - Class 4: 100 < P ≤ 200
          - Class 5: 200 < P
        
        #### Operational Parameters
        - **Rotation Speed:** {rpm_actual:.4f} rpm
        - **Braking Acceleration:** {braking_accel:.2f} m/s²
        - **Maximum Acceleration:** {class_data.get('n_actual', 0):.3f}g
        {additional_loads_report}
        ### Restraint System Requirements
        
        #### ISO 17842-2023 Classification
        - **Zone:** {class_data.get('restraint_zone_iso', 'N/A')}
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
    st.header(get_text('additional_analysis', persian))
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