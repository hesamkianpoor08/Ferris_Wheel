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
                'generation_instruction': {
            'en': "Click the button under the image to select a generation and proceed.",
            'fa': "برای انتخاب نسل و ادامه، دکمه زیر تصویر را کلیک کنید."
        },
        'generation_selected': {'en': "Generation", 'fa': "نسل"},
        'select_generation': {'en': "Select Ferris Wheel Generation", 'fa': "انتخاب نسل چرخ و فلک"},
        'gen_1_truss': {'en': "1st Generation (Truss type)", 'fa': "نسل اول (نوع خرپایی)"},
        'gen_2_cable': {'en': "2nd Generation_1st type (Cable type)", 'fa': "نسل دوم - نوع اول (کابلی)"},
        'gen_2_pure_cable': {'en': "2nd Generation_2nd type (Pure cable type)", 'fa': "نسل دوم - نوع دوم (کاملاً کابلی)"},
        'gen_4_hubless': {'en': "4th Generation (Hubless centerless)", 'fa': "نسل چهارم (بدون مرکز)"},
        
        # Step 2 - Cabin Geometry
        'cabin_geometry_header': {'en': "Choose a cabin shape.", 'fa': "یک شکل کابین انتخاب کنید."},
        'select_cabin_geometry': {'en': "Select Cabin Geometry", 'fa': "انتخاب هندسه کابین"},
        'cabin_geometry_instruction': {'en': "Choose a cabin shape.", 'fa': "یک شکل کابین انتخاب کنید."},
        'geom_square': {'en': "Square", 'fa': "مربعی"},
        'geom_vert_cyl': {'en': "Vertical Cylinder", 'fa': "استوانه عمودی"},
        'geom_horiz_cyl': {'en': "Horizontal Cylinder", 'fa': "استوانه افقی"},
        'geom_spherical': {'en': "Spherical", 'fa': "کروی"},
        'geom_spherical_caption': {'en': "This option is more expensive but has a better appearance.", 
                                  'fa': "این گزینه گران‌تر است اما جلوه‌ی ظاهری بهتری دارد"},
        
        # Step 3 - Primary Parameters
        'generation_label': {'en': "Generation", 'fa': "نسل"},
        'calc_capacities_btn': {'en': "🔄 Calculate Capacities", 'fa': "🔄 محاسبه ظرفیت‌ها"},

        # Back/Next buttons (shared)
        'back_btn': {'en': "⬅️ Back", 'fa': "⬅️ بازگشت"},
        'next_btn': {'en': "Next ➡️", 'fa': "➡️ بعدی"},

        # Validation errors
        'err_confirm_standards': {
            'en': "Please confirm your understanding of the standards.",
            'fa': "لطفاً درک خود از استانداردها را تأیید کنید."
        },
        'err_select_generation': {
            'en': "Please select a generation.",
            'fa': "لطفاً یک نسل انتخاب کنید."
        },
        'err_select_geometry': {
            'en': "Please select a cabin geometry.",
            'fa': "لطفاً شکل کابین را انتخاب کنید."
        },
        'err_diameter': {
            'en': "Diameter must be between 30 and 80 meters.",
            'fa': "قطر باید بین ۳۰ تا ۸۰ متر باشد."
        },
        'err_num_cabins': {
            'en': "Set a valid number of cabins.",
            'fa': "تعداد معتبری از کابین‌ها وارد کنید."
        },
        'err_cabin_capacity': {
            'en': "Cabin capacity must be between 4 and 8.",
            'fa': "ظرفیت کابین باید بین ۴ تا ۸ نفر باشد."
        },
        'err_vip_cabins': {
            'en': "Number of VIP cabins must be between 0 and total cabins.",
            'fa': "تعداد کابین‌های VIP باید بین ۰ و کل کابین‌ها باشد."
        },
        'err_calc_capacities': {
            'en': "Please click 'Calculate Capacities' before continuing.",
            'fa': "لطفاً قبل از ادامه روی 'محاسبه ظرفیت‌ها' کلیک کنید."
        },
        'err_rotation_time': {
            'en': "Enter valid rotation time (minutes per rotation).",
            'fa': "زمان چرخش معتبر وارد کنید (دقیقه در هر دور)."
        },
        'err_province': {'en': "Select a province.", 'fa': "یک استان انتخاب کنید."},
        'err_city': {'en': "Select a city.", 'fa': "یک شهر انتخاب کنید."},
        'err_region': {'en': "Enter region name.", 'fa': "نام منطقه را وارد کنید."},
        'err_land_length': {
            'en': "Land length must be between 10 and 150 meters.",
            'fa': "طول زمین باید بین ۱۰ تا ۱۵۰ متر باشد."
        },
        'err_land_width': {
            'en': "Land width must be between 10 and 150 meters.",
            'fa': "عرض زمین باید بین ۱۰ تا ۱۵۰ متر باشد."
        },
        'err_altitude': {'en': "Enter altitude.", 'fa': "ارتفاع را وارد کنید."},
        'err_wind_max': {
            'en': "Enter maximum wind speed (km/h).",
            'fa': "حداکثر سرعت باد (km/h) را وارد کنید."
        },
        'err_terrain': {
            'en': "Please click 'Calculate Terrain Parameters' before continuing.",
            'fa': "لطفاً قبل از ادامه روی 'محاسبه پارامترهای زمین' کلیک کنید."
        },
        'err_soil': {
            'en': "Please select a soil type.",
            'fa': "لطفاً نوع خاک را انتخاب کنید."
        },
        'err_orientation': {
            'en': "Please confirm the carousel orientation or select a custom direction.",
            'fa': "لطفاً جهت‌گیری چرخ و فلک را تأیید یا یک جهت سفارشی انتخاب کنید."
        },
        'cabin_specification': {'en': "Cabin Specification", 'fa': "مشخصات کابین"},
        'diameter_label': {'en': "Ferris Wheel Diameter (m)", 'fa': "قطر چرخ و فلک (متر)"},
        'num_cabins_label': {'en': "Number of Cabins", 'fa': "تعداد کابین‌ها"},
        'cabin_cap_label': {'en': "Cabin Capacity (passengers per cabin)", 'fa': "ظرفیت کابین (مسافر به ازای هر کابین)"},
        'num_vip_label': {'en': "Number of VIP Cabins", 'fa': "تعداد کابین‌های VIP"},
        'calc_capacities': {'en': "🔄 Calculate Capacities", 'fa': "🔄 محاسبه ظرفیت‌ها"},
        'per_rotation_capacity': {'en': "Per-rotation capacity", 'fa': "ظرفیت به ازای هر دور"},
        'vip_capacity': {'en': "VIP capacity (per rotation)", 'fa': "ظرفیت VIP (به ازای هر دور)"},
        'passengers': {'en': "passengers", 'fa': "مسافر"},
        'each_vip': {'en': "each VIP:", 'fa': " VIPهر:"},
        'capacities_calculated': {'en': "Capacities calculated.", 'fa': "ظرفیت‌ها محاسبه شدند."},
        
        # Step 4 - Rotation Time
        'rotation_time': {'en': "Rotation Time & Derived Speeds", 'fa': "زمان چرخش و سرعت‌های مشتق شده"},
        'rotation_time_instruction': {'en': "Enter the rotation time or select target capacity per hour",
                                     'fa': "زمان چرخش را وارد کنید یا ظرفیت هدف در ساعت را انتخاب کنید"},
        'rotation_time_label': {'en': "Rotation Time (minutes)", 'fa': "زمان چرخش (دقیقه)"},
        'capacity_per_hour': {'en': "Capacity per Hour (pax/hr)", 'fa': "ظرفیت در ساعت (ساعت/مسافر)"},
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
                'design_ref_step5': {
            'en': "**Design per AS 1170.4-2007(A1), EN 1991-1-4:2005, ISIRI 2800**",
            'fa': "**طراحی طبق AS 1170.4-2007(A1)، EN 1991-1-4:2005، ISIRI 2800**"
        },
        'land_surface_area': {'en': "Land Surface Area (meters)", 'fa': "مساحت زمین (متر)"},
        'total_land_area': {'en': "Total Land Area", 'fa': "مساحت کل زمین"},
        'altitude_temp': {'en': "Altitude and Temperature", 'fa': "ارتفاع و دما"},
        'wind_information': {'en': "Wind Information", 'fa': "اطلاعات باد"},
        'wind_direction_label': {'en': "Wind Direction", 'fa': "جهت باد"},
        'wind_speed_second': {'en': "Second interval wind speed (km/h)", 'fa': "سرعت باد لحظه‌ای (km/h)"},
        'wind_speed_minute': {'en': "Minute interval wind speed (km/h)", 'fa': "سرعت باد میانگین (km/h)"},
        'speed_label': {'en': "speed", 'fa': "سرعت"},
        'load_wind_rose': {'en': "Load wind rose (upload jpg/pdf)", 'fa': "بارگذاری گلباد (آپلود jpg/pdf)"},
        'wind_rose_file': {'en': "Wind rose file (jpg/pdf)", 'fa': "فایل گلباد (jpg/pdf)"},
        'wind_dir_north': {'en': "North", 'fa': "شمال"},
        'wind_dir_south': {'en': "South", 'fa': "جنوب"},
        'wind_dir_east': {'en': "East", 'fa': "شرق"},
        'wind_dir_west': {'en': "West", 'fa': "غرب"},
        'wind_dir_northeast': {'en': "Northeast", 'fa': "شمال‌شرق"},
        'wind_dir_northwest': {'en': "Northwest", 'fa': "شمال‌غرب"},
        'wind_dir_southeast': {'en': "Southeast", 'fa': "جنوب‌شرق"},
        'wind_dir_southwest': {'en': "Southwest", 'fa': "جنوب‌غرب"},
        
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
    "Gilan":                      {"category": "0",   "z0": 0.003, "zmin": 1,  "desc": "Sea or coastal area exposed to the open sea",                         "desc_fa": "دریا یا منطقه ساحلی در معرض دریای آزاد"},
    "Mazandaran":                 {"category": "0",   "z0": 0.003, "zmin": 1,  "desc": "Sea or coastal area exposed to the open sea",                         "desc_fa": "دریا یا منطقه ساحلی در معرض دریای آزاد"},
    "Golestan":                   {"category": "0",   "z0": 0.003, "zmin": 1,  "desc": "Sea or coastal area exposed to the open sea",                         "desc_fa": "دریا یا منطقه ساحلی در معرض دریای آزاد"},
    "Bushehr":                    {"category": "0",   "z0": 0.003, "zmin": 1,  "desc": "Sea or coastal area exposed to the open sea",                         "desc_fa": "دریا یا منطقه ساحلی در معرض دریای آزاد"},
    "Hormozgan":                  {"category": "0",   "z0": 0.003, "zmin": 1,  "desc": "Sea or coastal area exposed to the open sea",                         "desc_fa": "دریا یا منطقه ساحلی در معرض دریای آزاد"},
    "Khuzestan":                  {"category": "0",   "z0": 0.003, "zmin": 1,  "desc": "Sea or coastal area exposed to the open sea",                         "desc_fa": "دریا یا منطقه ساحلی در معرض دریای آزاد"},
    "Sistan and Baluchestan":     {"category": "0",   "z0": 0.003, "zmin": 1,  "desc": "Sea or coastal area exposed to the open sea (coastal parts)",         "desc_fa": "دریا یا منطقه ساحلی در معرض دریای آزاد (بخش‌های ساحلی)"},
    "Yazd":                       {"category": "I",   "z0": 0.01,  "zmin": 1,  "desc": "Flat or desert area with negligible vegetation",                      "desc_fa": "منطقه مسطح یا بیابانی با پوشش گیاهی ناچیز"},
    "Semnan":                     {"category": "I",   "z0": 0.01,  "zmin": 1,  "desc": "Flat or desert area with negligible vegetation",                      "desc_fa": "منطقه مسطح یا بیابانی با پوشش گیاهی ناچیز"},
    "Qom":                        {"category": "I",   "z0": 0.01,  "zmin": 1,  "desc": "Flat or desert area with negligible vegetation",                      "desc_fa": "منطقه مسطح یا بیابانی با پوشش گیاهی ناچیز"},
    "South Khorasan":             {"category": "I",   "z0": 0.01,  "zmin": 1,  "desc": "Flat or desert area with negligible vegetation",                      "desc_fa": "منطقه مسطح یا بیابانی با پوشش گیاهی ناچیز"},
    "Kerman":                     {"category": "I",   "z0": 0.01,  "zmin": 1,  "desc": "Flat or desert area with negligible vegetation",                      "desc_fa": "منطقه مسطح یا بیابانی با پوشش گیاهی ناچیز"},
    "Qazvin":                     {"category": "II",  "z0": 0.05,  "zmin": 2,  "desc": "Low vegetation, scattered trees or buildings",                        "desc_fa": "پوشش گیاهی کم، درختان یا ساختمان‌های پراکنده"},
    "Zanjan":                     {"category": "II",  "z0": 0.05,  "zmin": 2,  "desc": "Low vegetation, scattered trees or buildings",                        "desc_fa": "پوشش گیاهی کم، درختان یا ساختمان‌های پراکنده"},
    "Hamedan":                    {"category": "II",  "z0": 0.05,  "zmin": 2,  "desc": "Low vegetation, scattered trees or buildings",                        "desc_fa": "پوشش گیاهی کم، درختان یا ساختمان‌های پراکنده"},
    "Markazi":                    {"category": "II",  "z0": 0.05,  "zmin": 2,  "desc": "Low vegetation, scattered trees or buildings",                        "desc_fa": "پوشش گیاهی کم، درختان یا ساختمان‌های پراکنده"},
    "North Khorasan":             {"category": "II",  "z0": 0.05,  "zmin": 2,  "desc": "Low vegetation, scattered trees or buildings",                        "desc_fa": "پوشش گیاهی کم، درختان یا ساختمان‌های پراکنده"},
    "Khorasan Razavi":            {"category": "II",  "z0": 0.05,  "zmin": 2,  "desc": "Semi-arid plains, mixed low vegetation",                             "desc_fa": "دشت‌های نیمه‌خشک، پوشش گیاهی کم و مختلط"},
    "East Azerbaijan":            {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "West Azerbaijan":            {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Ardabil":                    {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Kurdistan":                  {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Kermanshah":                 {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Ilam":                       {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Lorestan":                   {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Chaharmahal and Bakhtiari":  {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Kohgiluyeh and Boyer-Ahmad": {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Fars":                       {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Isfahan":                    {"category": "III", "z0": 0.3,   "zmin": 5,  "desc": "Regular vegetation or rural/forested terrain",                       "desc_fa": "پوشش گیاهی معمولی یا زمین روستایی/جنگلی"},
    "Tehran":                     {"category": "IV",  "z0": 1.0,   "zmin": 10, "desc": "Densely built-up urban area",                                        "desc_fa": "منطقه شهری با تراکم ساختمانی بالا"},
    "Alborz":                     {"category": "IV",  "z0": 1.0,   "zmin": 10, "desc": "Densely built-up urban area",                                        "desc_fa": "منطقه شهری با تراکم ساختمانی بالا"},
}

# City data with seismic hazard levels
CITIES_DATA = {
    "Khuzestan": [
        {"city": "Abadan", "city_fa": "آبادان", "hazard": "Low"},
        {"city": "Aghajari", "city_fa": "آغاجاری", "hazard": "High"},
        {"city": "Omidiyeh", "city_fa": "امیدیه", "hazard": "Moderate"},
        {"city": "Andimeshk", "city_fa": "اندیمشک", "hazard": "High"},
        {"city": "Izeh", "city_fa": "ایذه", "hazard": "High"},
        {"city": "Ahvaz", "city_fa": "اهواز", "hazard": "Moderate"},
        {"city": "Arvankenar", "city_fa": "اروندکنار", "hazard": "Low"},
        {"city": "Baghmalk", "city_fa": "باغملک", "hazard": "High"},
        {"city": "Bandar Imam Khomeini", "city_fa": "بندر امام خمینی", "hazard": "Low"},
        {"city": "Bandar Mahshahr", "city_fa": "بندر ماهشهر", "hazard": "Low"},
        {"city": "Bastan", "city_fa": "بستان", "hazard": "Moderate"},
        {"city": "Behbahan", "city_fa": "بهبهان", "hazard": "High"},
        {"city": "Khorramshahr", "city_fa": "خرمشهر", "hazard": "Low"},
        {"city": "Dezful", "city_fa": "دزفول", "hazard": "High"},
        {"city": "Dehdez", "city_fa": "دهدز", "hazard": "High"},
        {"city": "Ramshir", "city_fa": "رامشیر", "hazard": "Moderate"},
        {"city": "Ramhormoz", "city_fa": "رامهرمز", "hazard": "High"},
        {"city": "Sarbandar", "city_fa": "سربندر", "hazard": "Low"},
        {"city": "Shadegan", "city_fa": "شادگان", "hazard": "Low"},
        {"city": "Shush", "city_fa": "شوش", "hazard": "Moderate"},
        {"city": "Shushtar", "city_fa": "شوشتر", "hazard": "High"},
        {"city": "Sosangerd", "city_fa": "سوسنگرد", "hazard": "Moderate"},
        {"city": "Hamidiyeh", "city_fa": "حمیدیه", "hazard": "Moderate"},
        {"city": "Haftgel", "city_fa": "هفتگل", "hazard": "High"},
        {"city": "Hendijan", "city_fa": "هندیجان", "hazard": "Moderate"},
        {"city": "Hovizeh", "city_fa": "هویزه", "hazard": "Moderate"},
        {"city": "Masjed Soleyman", "city_fa": "مسجد سلیمان", "hazard": "High"},
        {"city": "Mollasani", "city_fa": "ملاثانی", "hazard": "Moderate"},
        {"city": "Lali", "city_fa": "لالی", "hazard": "High"},
    ],
    "Ilam": [
        {"city": "Abdanan", "city_fa": "آبدانان", "hazard": "Moderate"},
        {"city": "Ilam", "city_fa": "ایلام", "hazard": "Moderate"},
        {"city": "Ivan", "city_fa": "ایوان", "hazard": "Moderate"},
        {"city": "Darreh Shahr", "city_fa": "دره شهر", "hazard": "Moderate"},
        {"city": "Dashte Abbas", "city_fa": "دشت عباس", "hazard": "Moderate"},
        {"city": "Dehloran", "city_fa": "دهلران", "hazard": "Moderate"},
        {"city": "Mehran", "city_fa": "مهران", "hazard": "Moderate"},
        {"city": "Musian", "city_fa": "موسیان", "hazard": "Moderate"},
    ],
    "Fars": [
        {"city": "Abadeh", "city_fa": "آباده", "hazard": "High"},
        {"city": "Arsanjan", "city_fa": "ارسنجان", "hazard": "Moderate"},
        {"city": "Eqlid", "city_fa": "اقلید", "hazard": "High"},
        {"city": "Estahban", "city_fa": "استهبان", "hazard": "High"},
        {"city": "Behrestān", "city_fa": "بهرستان", "hazard": "High"},
        {"city": "Khavaran", "city_fa": "خاوران", "hazard": "High"},
        {"city": "Kharameh", "city_fa": "خرامه", "hazard": "High"},
        {"city": "Khonj", "city_fa": "خنج", "hazard": "High"},
        {"city": "Darab", "city_fa": "داراب", "hazard": "High"},
        {"city": "Dehbid", "city_fa": "دهبید", "hazard": "High"},
        {"city": "Zarqan", "city_fa": "زرقان", "hazard": "High"},
        {"city": "Safashahr", "city_fa": "صفاشهر", "hazard": "Moderate"},
        {"city": "Sepidan", "city_fa": "سپیدان", "hazard": "High"},
        {"city": "Surian", "city_fa": "سوریان", "hazard": "High"},
        {"city": "Shiraz", "city_fa": "شیراز", "hazard": "High"},
        {"city": "Farashband", "city_fa": "فراشبند", "hazard": "High"},
        {"city": "Fasa", "city_fa": "فسا", "hazard": "High"},
        {"city": "Firuzabad", "city_fa": "فیروزآباد", "hazard": "High"},
        {"city": "Qaderabad", "city_fa": "قادرآباد", "hazard": "Moderate"},
        {"city": "Qir", "city_fa": "قیر", "hazard": "High"},
        {"city": "Kazerun", "city_fa": "کازرون", "hazard": "High"},
        {"city": "Kavar", "city_fa": "کوار", "hazard": "High"},
        {"city": "Gerash", "city_fa": "گراش", "hazard": "High"},
        {"city": "Lar", "city_fa": "لار", "hazard": "High"},
        {"city": "Lamerd", "city_fa": "لامرد", "hazard": "High"},
        {"city": "Marvdasht", "city_fa": "مرودشت", "hazard": "High"},
        {"city": "Mehr", "city_fa": "مهر", "hazard": "High"},
        {"city": "Neyriz", "city_fa": "نیریز", "hazard": "High"},
        {"city": "Nourabad", "city_fa": "نورآباد", "hazard": "High"},
        {"city": "Jahrom", "city_fa": "جهرم", "hazard": "High"},
    ],
    "Qazvin": [
        {"city": "Ab-e Garm", "city_fa": "آب‌گرم", "hazard": "High"},
        {"city": "Abyek", "city_fa": "آبیک", "hazard": "Very High"},
        {"city": "Avaj", "city_fa": "آوج", "hazard": "High"},
        {"city": "Buin Zahra", "city_fa": "بوئین زهرا", "hazard": "Very High"},
        {"city": "Takestan", "city_fa": "تاکستان", "hazard": "High"},
        {"city": "Qazvin", "city_fa": "قزوین", "hazard": "Very High"},
        {"city": "Moalem Kalayeh", "city_fa": "معلم کلایه", "hazard": "Very High"},
    ],
    "Zanjan": [
        {"city": "Ab Bar", "city_fa": "آب‌بر", "hazard": "Very High"},
        {"city": "Abhar", "city_fa": "ابهر", "hazard": "High"},
        {"city": "Khorramdarreh", "city_fa": "خرمدره", "hazard": "High"},
        {"city": "Zanjan", "city_fa": "زنجان", "hazard": "High"},
        {"city": "Soltaniyeh", "city_fa": "سلطانیه", "hazard": "High"},
        {"city": "Soltanabad", "city_fa": "سلطان‌آباد", "hazard": "High"},
        {"city": "Sayin Qaleh", "city_fa": "صائین قلعه", "hazard": "High"},
        {"city": "Qaydar", "city_fa": "قیدار", "hazard": "High"},
        {"city": "Giluwan", "city_fa": "گیلوان", "hazard": "Very High"},
        {"city": "Mahneshan", "city_fa": "ماهنشان", "hazard": "High"},
    ],
    "Hamedan": [
        {"city": "Asadabad", "city_fa": "اسدآباد", "hazard": "High"},
        {"city": "Bahar", "city_fa": "بهار", "hazard": "Moderate"},
        {"city": "Tuyserkan", "city_fa": "تویسرکان", "hazard": "High"},
        {"city": "Razan", "city_fa": "رزن", "hazard": "High"},
        {"city": "Kabutarāhang", "city_fa": "کبودرآهنگ", "hazard": "Moderate"},
        {"city": "Malayer", "city_fa": "ملایر", "hazard": "High"},
        {"city": "Nahavand", "city_fa": "نهاوند", "hazard": "Very High"},
        {"city": "Hamedan", "city_fa": "همدان", "hazard": "High"},
        {"city": "Famenin", "city_fa": "فامنین", "hazard": "Moderate"},
    ],
    "Markazi": [
        {"city": "Ashtian", "city_fa": "آشتیان", "hazard": "High"},
        {"city": "Arak", "city_fa": "اراک", "hazard": "Moderate"},
        {"city": "Astaneh", "city_fa": "آستانه", "hazard": "Moderate"},
        {"city": "Tafresh", "city_fa": "تفرش", "hazard": "High"},
        {"city": "Khondab", "city_fa": "خنداب", "hazard": "Moderate"},
        {"city": "Khomein", "city_fa": "خمین", "hazard": "Moderate"},
        {"city": "Delijan", "city_fa": "دلیجان", "hazard": "High"},
        {"city": "Zarandieh", "city_fa": "زرندیه", "hazard": "High"},
        {"city": "Sarband", "city_fa": "سربند", "hazard": "High"},
        {"city": "Shazand", "city_fa": "شازند", "hazard": "High"},
        {"city": "Saveh", "city_fa": "ساوه", "hazard": "High"},
        {"city": "Farmahin", "city_fa": "فرمهین", "hazard": "Moderate"},
        {"city": "Komijan", "city_fa": "کمیجان", "hazard": "Moderate"},
        {"city": "Mahallat", "city_fa": "محلات", "hazard": "Moderate"},
        {"city": "Nobaran", "city_fa": "نوبران", "hazard": "High"},
    ],
    "Yazd": [
        {"city": "Abarkuh", "city_fa": "ابرکوه", "hazard": "Moderate"},
        {"city": "Ardakan", "city_fa": "اردکان", "hazard": "Moderate"},
        {"city": "Bafq", "city_fa": "بافق", "hazard": "High"},
        {"city": "Behābād", "city_fa": "بهاباد", "hazard": "High"},
        {"city": "Taft", "city_fa": "تفت", "hazard": "Moderate"},
        {"city": "Khor", "city_fa": "خور", "hazard": "Moderate"},
        {"city": "Dihuk", "city_fa": "دیهوک", "hazard": "Very High"},
        {"city": "Rābat Posht-e Bādām", "city_fa": "رباط پشت‌بادام", "hazard": "High"},
        {"city": "Zarch", "city_fa": "زارچ", "hazard": "Moderate"},
        {"city": "Saqand", "city_fa": "سقند", "hazard": "High"},
        {"city": "Mehriz", "city_fa": "مهریز", "hazard": "Moderate"},
        {"city": "Meybod", "city_fa": "میبد", "hazard": "Moderate"},
        {"city": "Herat", "city_fa": "هرات", "hazard": "High"},
        {"city": "Yazd", "city_fa": "یزد", "hazard": "Moderate"},
        {"city": "Tabas", "city_fa": "طبس", "hazard": "Very High"},
        {"city": "Naybandan", "city_fa": "نایبندان", "hazard": "Very High"},
        {"city": "Dehshir", "city_fa": "دهشیر", "hazard": "High"},
    ],
    "Semnan": [
        {"city": "Aradan", "city_fa": "آرادان", "hazard": "High"},
        {"city": "Astaneh", "city_fa": "آستانه", "hazard": "High"},
        {"city": "Damghan", "city_fa": "دامغان", "hazard": "High"},
        {"city": "Sorkheh", "city_fa": "سرخه", "hazard": "High"},
        {"city": "Semnan", "city_fa": "سمنان", "hazard": "High"},
        {"city": "Shahrud", "city_fa": "شاهرود", "hazard": "High"},
        {"city": "Absarabad", "city_fa": "آبسرآباد", "hazard": "High"},
        {"city": "Garmsar", "city_fa": "گرمسار", "hazard": "High"},
        {"city": "Mehdishahr", "city_fa": "مهدیشهر", "hazard": "Very High"},
        {"city": "Meyamey", "city_fa": "میامی", "hazard": "High"},
        {"city": "Shahmirzad", "city_fa": "شهمیرزاد", "hazard": "Very High"},
        {"city": "Ivānkī", "city_fa": "ایوانکی", "hazard": "High"},
        {"city": "Jām", "city_fa": "جام", "hazard": "High"},
        {"city": "Biarjmand", "city_fa": "بیارجمند", "hazard": "Moderate"},
        {"city": "Bastam", "city_fa": "بسطام", "hazard": "High"},
        {"city": "Tazareh", "city_fa": "تزره", "hazard": "High"},
        {"city": "Torud", "city_fa": "طرود", "hazard": "High"},
        {"city": "Forumad", "city_fa": "فرومد", "hazard": "High"},
        {"city": "Mojen", "city_fa": "مجن", "hazard": "High"},
        {"city": "Moalleman", "city_fa": "معلمان", "hazard": "High"},
        {"city": "Amir Abad", "city_fa": "امیرآباد", "hazard": "High"},
    ],
    "Qom": [
        {"city": "Qom", "city_fa": "قم", "hazard": "High"},
        {"city": "Solfchegan", "city_fa": "سلفچگان", "hazard": "High"},
        {"city": "Gazaran", "city_fa": "گازران", "hazard": "High"},
        {"city": "Kahak", "city_fa": "کهک", "hazard": "High"},
        {"city": "Kooshk Nosrat", "city_fa": "کوشک نصرت", "hazard": "High"},
    ],
    "South Khorasan": [
        {"city": "Birjand", "city_fa": "بیرجند", "hazard": "High"},
        {"city": "Tabas Masina", "city_fa": "طبس مسینا", "hazard": "High"},
        {"city": "Khosvaf", "city_fa": "خوسف", "hazard": "Moderate"},
        {"city": "Khezri", "city_fa": "خضری", "hazard": "Very High"},
        {"city": "Dasht Beyaz", "city_fa": "دشت بیاض", "hazard": "Very High"},
        {"city": "Sarayan", "city_fa": "سرایان", "hazard": "Very High"},
        {"city": "Sarbisheh", "city_fa": "سربیشه", "hazard": "High"},
        {"city": "Sade", "city_fa": "سده", "hazard": "High"},
        {"city": "Shahrukht", "city_fa": "شاهرخت", "hazard": "Very High"},
        {"city": "Qaen", "city_fa": "قاین", "hazard": "Very High"},
        {"city": "Kooli", "city_fa": "کولی", "hazard": "Very High"},
        {"city": "Nehbandan", "city_fa": "نهبندان", "hazard": "High"},
        {"city": "Boshruyeh", "city_fa": "بشرویه", "hazard": "High"},
    ],
    "Kerman": [
        {"city": "Anār", "city_fa": "انار", "hazard": "High"},
        {"city": "Baft", "city_fa": "بافت", "hazard": "High"},
        {"city": "Bārdsar", "city_fa": "بردسیر", "hazard": "High"},
        {"city": "Bam", "city_fa": "بم", "hazard": "High"},
        {"city": "Jiroft", "city_fa": "جیرفت", "hazard": "High"},
        {"city": "Rafsanjan", "city_fa": "رفسنجان", "hazard": "High"},
        {"city": "Ravar", "city_fa": "راور", "hazard": "High"},
        {"city": "Rayen", "city_fa": "راین", "hazard": "High"},
        {"city": "Zarand", "city_fa": "زرند", "hazard": "High"},
        {"city": "Sīrjān", "city_fa": "سیرجان", "hazard": "Moderate"},
        {"city": "Sirch", "city_fa": "سیرچ", "hazard": "Very High"},
        {"city": "Sabz Abad", "city_fa": "سبزآباد", "hazard": "High"},
        {"city": "Sarcheshmeh", "city_fa": "سرچشمه", "hazard": "High"},
        {"city": "Shahdad", "city_fa": "شهداد", "hazard": "Very High"},
        {"city": "Shahrbabak", "city_fa": "شهربابک", "hazard": "High"},
        {"city": "Kerman", "city_fa": "کرمان", "hazard": "High"},
        {"city": "Golbaf", "city_fa": "گلباف", "hazard": "Very High"},
        {"city": "Kahnuj", "city_fa": "کهنوج", "hazard": "High"},
        {"city": "Kohbanān", "city_fa": "کوهبنان", "hazard": "High"},
        {"city": "Kianshahr", "city_fa": "کیانشهر", "hazard": "High"},
        {"city": "Mahan", "city_fa": "ماهان", "hazard": "High"},
        {"city": "Manujan", "city_fa": "منوجان", "hazard": "High"},
    ],
    "East Azerbaijan": [
        {"city": "Ahar", "city_fa": "اهر", "hazard": "High"},
        {"city": "Azhdarshur", "city_fa": "آذرشهر", "hazard": "High"},
        {"city": "Osku", "city_fa": "اسکو", "hazard": "Very High"},
        {"city": "Bonab", "city_fa": "بناب", "hazard": "Moderate"},
        {"city": "Bostanābād", "city_fa": "بستان‌آباد", "hazard": "Very High"},
        {"city": "Tabriz", "city_fa": "تبریز", "hazard": "Very High"},
        {"city": "Tasuj", "city_fa": "تسوج", "hazard": "Very High"},
        {"city": "Jolfa", "city_fa": "جلفا", "hazard": "High"},
        {"city": "Khajeh", "city_fa": "خاجه", "hazard": "High"},
        {"city": "Sarab", "city_fa": "سراب", "hazard": "High"},
        {"city": "Shabestar", "city_fa": "شبستر", "hazard": "Very High"},
        {"city": "Sharafkhaneh", "city_fa": "شرفخانه", "hazard": "Very High"},
        {"city": "Sofian", "city_fa": "صوفیان", "hazard": "Very High"},
        {"city": "Ajab Shir", "city_fa": "عجب‌شیر", "hazard": "Moderate"},
        {"city": "Qareh Aghaj", "city_fa": "قره‌آغاج", "hazard": "High"},
        {"city": "Kaleybar", "city_fa": "کلیبر", "hazard": "High"},
        {"city": "Maragheh", "city_fa": "مراغه", "hazard": "Moderate"},
        {"city": "Marand", "city_fa": "مرند", "hazard": "High"},
        {"city": "Mianeh", "city_fa": "میانه", "hazard": "Very High"},
        {"city": "Haris", "city_fa": "هریس", "hazard": "High"},
        {"city": "Heris", "city_fa": "هریس", "hazard": "High"},
        {"city": "Hashtrud", "city_fa": "هشترود", "hazard": "High"},
        {"city": "Varzaqān", "city_fa": "ورزقان", "hazard": "High"},
        {"city": "Zonūz", "city_fa": "زنوز", "hazard": "High"},
    ],
    "West Azerbaijan": [
        {"city": "Oshnaviyeh", "city_fa": "اشنویه", "hazard": "High"},
        {"city": "Urmia", "city_fa": "ارومیه", "hazard": "Moderate"},
        {"city": "Bukan", "city_fa": "بوکان", "hazard": "Moderate"},
        {"city": "Piranshahr", "city_fa": "پیرانشهر", "hazard": "High"},
        {"city": "Takab", "city_fa": "تکاب", "hazard": "Moderate"},
        {"city": "Chaypareh", "city_fa": "چایپاره", "hazard": "High"},
        {"city": "Khoy", "city_fa": "خوی", "hazard": "High"},
        {"city": "Salmas", "city_fa": "سلماس", "hazard": "Very High"},
        {"city": "Sarv", "city_fa": "سرو", "hazard": "Moderate"},
        {"city": "Sardasht", "city_fa": "سردشت", "hazard": "High"},
        {"city": "Shahin Dezh", "city_fa": "شاهین‌دژ", "hazard": "Moderate"},
        {"city": "Siyah Cheshmeh", "city_fa": "سیه‌چشمه", "hazard": "High"},
        {"city": "Showt", "city_fa": "شوط", "hazard": "High"},
        {"city": "Qarah Zīā od Dīn", "city_fa": "قره‌ضیاءالدین", "hazard": "High"},
        {"city": "Qotur", "city_fa": "قطور", "hazard": "Very High"},
        {"city": "Kelisa Kandi", "city_fa": "کلیساکندی", "hazard": "High"},
        {"city": "Maku", "city_fa": "ماکو", "hazard": "High"},
        {"city": "Mahābād", "city_fa": "مهاباد", "hazard": "Moderate"},
        {"city": "Miandoab", "city_fa": "میاندوآب", "hazard": "Moderate"},
        {"city": "Naqadeh", "city_fa": "نقده", "hazard": "High"},
        {"city": "Poldasht", "city_fa": "پلدشت", "hazard": "High"},
    ],
    "Ardabil": [
        {"city": "Aslanduz", "city_fa": "اصلاندوز", "hazard": "High"},
        {"city": "Ardabil", "city_fa": "اردبیل", "hazard": "High"},
        {"city": "Parsābād", "city_fa": "پارس‌آباد", "hazard": "High"},
        {"city": "Beleh Savar", "city_fa": "بیله‌سوار", "hazard": "High"},
        {"city": "Khalkhal", "city_fa": "خلخال", "hazard": "High"},
        {"city": "Sarein", "city_fa": "سرعین", "hazard": "High"},
        {"city": "Zaviyeh", "city_fa": "زاویه", "hazard": "Very High"},
        {"city": "Germi", "city_fa": "گرمی", "hazard": "High"},
        {"city": "Giveh", "city_fa": "گیوی", "hazard": "High"},
        {"city": "Kolur", "city_fa": "کلور", "hazard": "Very High"},
        {"city": "Meshginshahr", "city_fa": "مشگین‌شهر", "hazard": "High"},
        {"city": "Namin", "city_fa": "نمین", "hazard": "High"},
        {"city": "Nir", "city_fa": "نیر", "hazard": "High"},
        {"city": "Hashtjin", "city_fa": "هشتجین", "hazard": "Very High"},
        {"city": "Lahrood", "city_fa": "لاهرود", "hazard": "High"},
    ],
    "Kurdistan": [
        {"city": "Baneh", "city_fa": "بانه", "hazard": "High"},
        {"city": "Bijar", "city_fa": "بیجار", "hazard": "Moderate"},
        {"city": "Qorveh", "city_fa": "قروه", "hazard": "High"},
        {"city": "Kamyaran", "city_fa": "کامیاران", "hazard": "Very High"},
        {"city": "Marivan", "city_fa": "مریوان", "hazard": "Very High"},
        {"city": "Sanandaj", "city_fa": "سنندج", "hazard": "High"},
        {"city": "Saqez", "city_fa": "سقز", "hazard": "High"},
        {"city": "Divandarreh", "city_fa": "دیواندره", "hazard": "Moderate"},
    ],
    "Kermanshah": [
        {"city": "Eslamābād-e Gharb", "city_fa": "اسلام‌آباد غرب", "hazard": "High"},
        {"city": "Paveh", "city_fa": "پاوه", "hazard": "High"},
        {"city": "Sarab-e Neelofar", "city_fa": "سراب نیلوفر", "hazard": "High"},
        {"city": "Bisetun", "city_fa": "بیستون", "hazard": "High"},
        {"city": "Javanrud", "city_fa": "جوانرود", "hazard": "High"},
        {"city": "Harsin", "city_fa": "هرسین", "hazard": "High"},
        {"city": "Ravansar", "city_fa": "روانسر", "hazard": "High"},
        {"city": "Sar-e Pol-e Zahab", "city_fa": "سرپل ذهاب", "hazard": "High"},
        {"city": "Songhor", "city_fa": "سنقر", "hazard": "High"},
        {"city": "Sahneh", "city_fa": "صحنه", "hazard": "Very High"},
        {"city": "Somar", "city_fa": "سومار", "hazard": "Moderate"},
        {"city": "Qasr-e Shirin", "city_fa": "قصر شیرین", "hazard": "High"},
        {"city": "Kangavar", "city_fa": "کنگاور", "hazard": "Very High"},
        {"city": "Kermanshah", "city_fa": "کرمانشاه", "hazard": "High"},
        {"city": "Kerend", "city_fa": "کرند", "hazard": "High"},
        {"city": "Gilan-e Gharb", "city_fa": "گیلان غرب", "hazard": "High"},
        {"city": "Nosoud", "city_fa": "نوسود", "hazard": "High"},
    ],
    "Lorestan": [
        {"city": "Azna", "city_fa": "ازنا", "hazard": "Very High"},
        {"city": "Aleshtar", "city_fa": "الشتر", "hazard": "High"},
        {"city": "Aligudarz", "city_fa": "الیگودرز", "hazard": "High"},
        {"city": "Borujerd", "city_fa": "بروجرد", "hazard": "Very High"},
        {"city": "Poldokhtar", "city_fa": "پلدختر", "hazard": "Moderate"},
        {"city": "Khorramabad", "city_fa": "خرم‌آباد", "hazard": "High"},
        {"city": "Dorud", "city_fa": "دورود", "hazard": "Very High"},
        {"city": "Kuhdasht", "city_fa": "کوهدشت", "hazard": "High"},
        {"city": "Mamoun", "city_fa": "ممون", "hazard": "High"},
    ],
    "Chaharmahal and Bakhtiari": [
        {"city": "Ardal", "city_fa": "اردل", "hazard": "High"},
        {"city": "Borūjen", "city_fa": "بروجن", "hazard": "High"},
        {"city": "Boldaji", "city_fa": "بلداجی", "hazard": "High"},
        {"city": "Dogoombadan", "city_fa": "دوگنبدان", "hazard": "High"},
        {"city": "Saman", "city_fa": "سامان", "hazard": "High"},
        {"city": "Sarkhoon", "city_fa": "سرخون", "hazard": "High"},
        {"city": "Shalmazar", "city_fa": "شلمزار", "hazard": "High"},
        {"city": "Shahrekord", "city_fa": "شهرکرد", "hazard": "High"},
        {"city": "Farsan", "city_fa": "فارسان", "hazard": "Very High"},
        {"city": "Koohrang", "city_fa": "کوهرنگ", "hazard": "Very High"},
        {"city": "Gandoman", "city_fa": "گندمان", "hazard": "High"},
        {"city": "Lordegan", "city_fa": "لردگان", "hazard": "High"},
        {"city": "Naghan", "city_fa": "ناغان", "hazard": "High"},
    ],
    "Kohgiluyeh and Boyer-Ahmad": [
        {"city": "Dehdasht", "city_fa": "دهدشت", "hazard": "High"},
        {"city": "Dishmuk", "city_fa": "دیشموک", "hazard": "High"},
        {"city": "Yasuj", "city_fa": "یاسوج", "hazard": "High"},
        {"city": "Gachsaran", "city_fa": "گچساران", "hazard": "High"},
        {"city": "Si Sakhti", "city_fa": "سی‌سخت", "hazard": "High"},
    ],
    "Isfahan": [
        {"city": "Abyaneh", "city_fa": "ابیانه", "hazard": "High"},
        {"city": "Ardestan", "city_fa": "اردستان", "hazard": "High"},
        {"city": "Aran", "city_fa": "آران", "hazard": "High"},
        {"city": "Isfahan", "city_fa": "اصفهان", "hazard": "Moderate"},
        {"city": "Anarak", "city_fa": "انارک", "hazard": "Moderate"},
        {"city": "Badrud", "city_fa": "بادرود", "hazard": "Moderate"},
        {"city": "Tiran", "city_fa": "تیران", "hazard": "Moderate"},
        {"city": "Charmhin", "city_fa": "چرمهین", "hazard": "High"},
        {"city": "Chadegan", "city_fa": "چادگان", "hazard": "High"},
        {"city": "Dehaqan", "city_fa": "دهاقان", "hazard": "High"},
        {"city": "Daran", "city_fa": "داران", "hazard": "High"},
        {"city": "Dorche", "city_fa": "درچه", "hazard": "High"},
        {"city": "Jondoq", "city_fa": "جندق", "hazard": "High"},
        {"city": "Khur", "city_fa": "خور", "hazard": "Moderate"},
        {"city": "Khansar", "city_fa": "خوانسار", "hazard": "Moderate"},
        {"city": "Zarrinshahr", "city_fa": "زرین‌شهر", "hazard": "High"},
        {"city": "Zvareh", "city_fa": "زواره", "hazard": "Moderate"},
        {"city": "Zafreh", "city_fa": "زفره", "hazard": "High"},
        {"city": "Semīrom", "city_fa": "سمیرم", "hazard": "High"},
        {"city": "Shahreza", "city_fa": "شهرضا", "hazard": "High"},
        {"city": "Shahin Shahr", "city_fa": "شاهین‌شهر", "hazard": "Moderate"},
        {"city": "Golpayegan", "city_fa": "گلپایگان", "hazard": "Moderate"},
        {"city": "Kashan", "city_fa": "کاشان", "hazard": "High"},
        {"city": "Kuhpayeh", "city_fa": "کوهپایه", "hazard": "High"},
        {"city": "Meimeh", "city_fa": "میمه", "hazard": "Moderate"},
        {"city": "Mobarakeh", "city_fa": "مبارکه", "hazard": "High"},
        {"city": "Natanz", "city_fa": "نطنز", "hazard": "High"},
        {"city": "Najaf Abad", "city_fa": "نجف‌آباد", "hazard": "Moderate"},
        {"city": "Nain", "city_fa": "نائین", "hazard": "High"},
        {"city": "Alvandeh", "city_fa": "الوانده", "hazard": "Moderate"},
        {"city": "Fin", "city_fa": "فین", "hazard": "High"},
        {"city": "Qomsar", "city_fa": "قمصر", "hazard": "High"},
        {"city": "Freydunshahr", "city_fa": "فریدونشهر", "hazard": "High"},
    ],
    "Tehran": [
        {"city": "Eshtahard", "city_fa": "اشتهارد", "hazard": "Very High"},
        {"city": "Bumehen", "city_fa": "بومهن", "hazard": "Very High"},
        {"city": "Pishva", "city_fa": "پیشوا", "hazard": "High"},
        {"city": "Tehran", "city_fa": "تهران", "hazard": "Very High"},
        {"city": "Damavand", "city_fa": "دماوند", "hazard": "Very High"},
        {"city": "Rabat Karim", "city_fa": "رباط کریم", "hazard": "Very High"},
        {"city": "Rey", "city_fa": "ری", "hazard": "Very High"},
        {"city": "Rudehen", "city_fa": "رودهن", "hazard": "Very High"},
        {"city": "Sarbandan", "city_fa": "سربندان", "hazard": "Very High"},
        {"city": "Solegān", "city_fa": "سولقان", "hazard": "Very High"},
        {"city": "Shahriar", "city_fa": "شهریار", "hazard": "Very High"},
        {"city": "Shahr-e Qods", "city_fa": "شهر قدس", "hazard": "High"},
        {"city": "Shahr-e Jadid-e Parand", "city_fa": "شهر جدید پرند", "hazard": "High"},
        {"city": "Taleqān", "city_fa": "طالقان", "hazard": "Very High"},
        {"city": "Fasham", "city_fa": "فشم", "hazard": "Very High"},
        {"city": "Firuzkooh", "city_fa": "فیروزکوه", "hazard": "Very High"},
        {"city": "Gejr", "city_fa": "گجر", "hazard": "Very High"},
        {"city": "Kilan", "city_fa": "کیلان", "hazard": "Very High"},
        {"city": "Lavasan", "city_fa": "لواسان", "hazard": "Very High"},
        {"city": "Masha", "city_fa": "ماشا", "hazard": "Very High"},
        {"city": "Mardabad", "city_fa": "مارداباد", "hazard": "Very High"},
        {"city": "Hasanābād", "city_fa": "حسن‌آباد", "hazard": "High"},
        {"city": "Erjmand", "city_fa": "ارجمند", "hazard": "Very High"},
        {"city": "Dizin", "city_fa": "دیزین", "hazard": "Very High"},
        {"city": "Varamin", "city_fa": "ورامین", "hazard": "High"},
    ],
    "Alborz": [
        {"city": "Karaj", "city_fa": "کرج", "hazard": "Very High"},
        {"city": "Hashtgerd", "city_fa": "هشتگرد", "hazard": "Very High"},
        {"city": "Savojbolagh", "city_fa": "ساوجبلاغ", "hazard": "High"},
        {"city": "Nazarābād", "city_fa": "نظرآباد", "hazard": "High"},
    ],
    "Gilan": [
        {"city": "Astara", "city_fa": "آستارا", "hazard": "High"},
        {"city": "Astaneh", "city_fa": "آستانه", "hazard": "High"},
        {"city": "Bandar Anzali", "city_fa": "بندر انزلی", "hazard": "High"},
        {"city": "Jirandeh", "city_fa": "جیرنده", "hazard": "Very High"},
        {"city": "Chaboksar", "city_fa": "چابکسر", "hazard": "High"},
        {"city": "Rudsar", "city_fa": "رودسر", "hazard": "High"},
        {"city": "Rudbar", "city_fa": "رودبار", "hazard": "Very High"},
        {"city": "Rezvanshahr", "city_fa": "رضوانشهر", "hazard": "High"},
        {"city": "Rasht", "city_fa": "رشت", "hazard": "High"},
        {"city": "Siahkal", "city_fa": "سیاهکل", "hazard": "High"},
        {"city": "Sowme'eh Sara", "city_fa": "صومعه‌سرا", "hazard": "High"},
        {"city": "Shaft", "city_fa": "شفت", "hazard": "High"},
        {"city": "Fuman", "city_fa": "فومن", "hazard": "High"},
        {"city": "Kelachay", "city_fa": "کلاچای", "hazard": "High"},
        {"city": "Langerud", "city_fa": "لنگرود", "hazard": "High"},
        {"city": "Lahijan", "city_fa": "لاهیجان", "hazard": "High"},
        {"city": "Manjil", "city_fa": "منجیل", "hazard": "Very High"},
        {"city": "Masal", "city_fa": "ماسال", "hazard": "Very High"},
        {"city": "Masuleh", "city_fa": "ماسوله", "hazard": "Very High"},
        {"city": "Hashtpar", "city_fa": "هشتپر", "hazard": "High"},
        {"city": "Deylaman", "city_fa": "دیلمان", "hazard": "High"},
        {"city": "Talesh", "city_fa": "تالش", "hazard": "High"},
    ],
    "Mazandaran": [
        {"city": "Alasht", "city_fa": "الاشت", "hazard": "High"},
        {"city": "Amol", "city_fa": "آمل", "hazard": "High"},
        {"city": "Azmaaldaoleh", "city_fa": "آزمالدوله", "hazard": "High"},
        {"city": "Babolsar", "city_fa": "بابلسر", "hazard": "High"},
        {"city": "Babol", "city_fa": "بابل", "hazard": "High"},
        {"city": "Behshahr", "city_fa": "بهشهر", "hazard": "High"},
        {"city": "Beldeh", "city_fa": "بلده", "hazard": "High"},
        {"city": "Tonekabon", "city_fa": "تنکابن", "hazard": "High"},
        {"city": "Chalus", "city_fa": "چالوس", "hazard": "High"},
        {"city": "Hasan Kif", "city_fa": "حسن‌کیف", "hazard": "High"},
        {"city": "Ramsar", "city_fa": "رامسر", "hazard": "High"},
        {"city": "Savadkuh", "city_fa": "سوادکوه", "hazard": "High"},
        {"city": "Sari", "city_fa": "ساری", "hazard": "High"},
        {"city": "Polur", "city_fa": "پلور", "hazard": "Very High"},
        {"city": "Pol-e Sefid", "city_fa": "پل‌سفید", "hazard": "High"},
        {"city": "Qarakhil", "city_fa": "قراخیل", "hazard": "High"},
        {"city": "Qaemshahr", "city_fa": "قائمشهر", "hazard": "High"},
        {"city": "Kelardasht", "city_fa": "کلاردشت", "hazard": "Very High"},
        {"city": "Galugah", "city_fa": "گلوگاه", "hazard": "High"},
        {"city": "Mahmoudabad", "city_fa": "محمودآباد", "hazard": "High"},
        {"city": "Marzanābād", "city_fa": "مرزن‌آباد", "hazard": "High"},
        {"city": "Neka", "city_fa": "نکا", "hazard": "High"},
        {"city": "Nur", "city_fa": "نور", "hazard": "High"},
        {"city": "Noshahr", "city_fa": "نوشهر", "hazard": "High"},
        {"city": "Kiāsar", "city_fa": "کیاسر", "hazard": "High"},
        {"city": "Freydunkenar", "city_fa": "فریدونکنار", "hazard": "High"},
    ],
    "Golestan": [
        {"city": "Aq Qala", "city_fa": "آق‌قلا", "hazard": "High"},
        {"city": "Ali Abad", "city_fa": "علی‌آباد", "hazard": "High"},
        {"city": "Azadshahr", "city_fa": "آزادشهر", "hazard": "High"},
        {"city": "Bandar Gaz", "city_fa": "بندر گز", "hazard": "High"},
        {"city": "Bandar Torkaman", "city_fa": "بندر ترکمن", "hazard": "High"},
        {"city": "Ramian", "city_fa": "رامیان", "hazard": "High"},
        {"city": "Kalaleh", "city_fa": "کلاله", "hazard": "High"},
        {"city": "Kordkuy", "city_fa": "کردکوی", "hazard": "High"},
        {"city": "Gorgan", "city_fa": "گرگان", "hazard": "High"},
        {"city": "Gonbad Kavus", "city_fa": "گنبد کاووس", "hazard": "High"},
        {"city": "Marave Tappeh", "city_fa": "مراوه‌تپه", "hazard": "High"},
        {"city": "Minoodasht", "city_fa": "مینودشت", "hazard": "High"},
    ],
    "North Khorasan": [
        {"city": "Esfarayen", "city_fa": "اسفراین", "hazard": "High"},
        {"city": "Ashkhaneh", "city_fa": "آشخانه", "hazard": "High"},
        {"city": "Bojnurd", "city_fa": "بجنورد", "hazard": "High"},
        {"city": "Jajarm", "city_fa": "جاجرم", "hazard": "High"},
        {"city": "Chaman Bid", "city_fa": "چمن‌بید", "hazard": "High"},
        {"city": "Rābat", "city_fa": "رباط", "hazard": "Very High"},
        {"city": "Garmkhan", "city_fa": "گرمخان", "hazard": "High"},
        {"city": "Gifan", "city_fa": "گیفان", "hazard": "Very High"},
        {"city": "Maneh", "city_fa": "مانه", "hazard": "High"},
        {"city": "Shirvan", "city_fa": "شیروان", "hazard": "Very High"},
        {"city": "Farouj", "city_fa": "فاروج", "hazard": "Very High"},
    ],
    "Khorasan Razavi": [
        {"city": "Bajestan", "city_fa": "بجستان", "hazard": "High"},
        {"city": "Bajgiran", "city_fa": "باجگیران", "hazard": "High"},
        {"city": "Bardaskan", "city_fa": "بردسکن", "hazard": "High"},
        {"city": "Taybad", "city_fa": "تایباد", "hazard": "High"},
        {"city": "Torbat-e Jam", "city_fa": "تربت جام", "hazard": "High"},
        {"city": "Torbat-e Heydarieh", "city_fa": "تربت حیدریه", "hazard": "High"},
        {"city": "Joghatay", "city_fa": "جغتای", "hazard": "High"},
        {"city": "Chenaran", "city_fa": "چناران", "hazard": "High"},
        {"city": "Khaf", "city_fa": "خواف", "hazard": "High"},
        {"city": "Dargaz", "city_fa": "درگز", "hazard": "High"},
        {"city": "Daruneh", "city_fa": "درونه", "hazard": "High"},
        {"city": "Rivand", "city_fa": "ریوند", "hazard": "High"},
        {"city": "Roshtkhar", "city_fa": "رشتخوار", "hazard": "High"},
        {"city": "Sabzevar", "city_fa": "سبزوار", "hazard": "High"},
        {"city": "Sangān", "city_fa": "سنگان", "hazard": "High"},
        {"city": "Sarakhs", "city_fa": "سرخس", "hazard": "High"},
        {"city": "Salehabād", "city_fa": "صالح‌آباد", "hazard": "High"},
        {"city": "Shandiz", "city_fa": "شاندیز", "hazard": "High"},
        {"city": "Fariman", "city_fa": "فریمان", "hazard": "High"},
        {"city": "Ferdows", "city_fa": "فردوس", "hazard": "Very High"},
        {"city": "Qalandarābād", "city_fa": "قلندرآباد", "hazard": "High"},
        {"city": "Quchan", "city_fa": "قوچان", "hazard": "Very High"},
        {"city": "Kalat", "city_fa": "کلات", "hazard": "High"},
        {"city": "Kakhk", "city_fa": "کاخک", "hazard": "Very High"},
        {"city": "Kashmar", "city_fa": "کاشمر", "hazard": "High"},
        {"city": "Gonabad", "city_fa": "گناباد", "hazard": "High"},
        {"city": "Golbahār", "city_fa": "گلبهار", "hazard": "High"},
        {"city": "Marzadaran", "city_fa": "مرزداران", "hazard": "High"},
        {"city": "Mashhad", "city_fa": "مشهد", "hazard": "High"},
        {"city": "Neyshabur", "city_fa": "نیشابور", "hazard": "High"},
        {"city": "Kamberz", "city_fa": "کامبرز", "hazard": "High"},
    ],
    "Sistan and Baluchestan": [
        {"city": "Iranshahr", "city_fa": "ایرانشهر", "hazard": "High"},
        {"city": "Bampur", "city_fa": "بمپور", "hazard": "Moderate"},
        {"city": "Bezman", "city_fa": "بزمان", "hazard": "Moderate"},
        {"city": "Chabahar", "city_fa": "چابهار", "hazard": "High"},
        {"city": "Dehak", "city_fa": "دهاک", "hazard": "High"},
        {"city": "Zabol", "city_fa": "زابل", "hazard": "High"},
        {"city": "Zaboli", "city_fa": "زابلی", "hazard": "High"},
        {"city": "Zahak", "city_fa": "زهک", "hazard": "High"},
        {"city": "Zahedan", "city_fa": "زاهدان", "hazard": "High"},
        {"city": "Saravan", "city_fa": "سراوان", "hazard": "High"},
        {"city": "Sarbaz", "city_fa": "سرباز", "hazard": "High"},
        {"city": "Sib va Suran", "city_fa": "سیب و سوران", "hazard": "High"},
        {"city": "Fanuj", "city_fa": "فنوج", "hazard": "High"},
        {"city": "Qasr-e Qand", "city_fa": "قصرقند", "hazard": "High"},
        {"city": "Koochak", "city_fa": "کوچک", "hazard": "High"},
        {"city": "Konarak", "city_fa": "کنارک", "hazard": "High"},
        {"city": "Gowater", "city_fa": "گواتر", "hazard": "High"},
        {"city": "Khash", "city_fa": "خاش", "hazard": "High"},
        {"city": "Jalq", "city_fa": "جالق", "hazard": "High"},
        {"city": "Mirjaveh", "city_fa": "میرجاوه", "hazard": "High"},
        {"city": "Nasrat Abad", "city_fa": "نصرت‌آباد", "hazard": "High"},
        {"city": "Nikshahr", "city_fa": "نیکشهر", "hazard": "High"},
    ],
    "Bushehr": [
        {"city": "Ahram", "city_fa": "اهرم", "hazard": "Moderate"},
        {"city": "Asaluyeh", "city_fa": "عسلویه", "hazard": "High"},
        {"city": "Bandar Dayyer", "city_fa": "بندر دیر", "hazard": "High"},
        {"city": "Bandar Deylam", "city_fa": "بندر دیلم", "hazard": "Moderate"},
        {"city": "Bandar Taheri", "city_fa": "بندر طاهری", "hazard": "High"},
        {"city": "Bandar Genaveh", "city_fa": "بندر گناوه", "hazard": "Moderate"},
        {"city": "Bandar-e Kangan", "city_fa": "بندر کنگان", "hazard": "High"},
        {"city": "Bandar-e Maqām", "city_fa": "بندر مقام", "hazard": "High"},
        {"city": "Borazjan", "city_fa": "برازجان", "hazard": "High"},
        {"city": "Bushehr", "city_fa": "بوشهر", "hazard": "Moderate"},
        {"city": "Jam", "city_fa": "جم", "hazard": "High"},
        {"city": "Khark", "city_fa": "خارک", "hazard": "Moderate"},
        {"city": "Khormoj", "city_fa": "خورموج", "hazard": "Moderate"},
        {"city": "Dalaki", "city_fa": "دالکی", "hazard": "High"},
        {"city": "Deylvar", "city_fa": "دیلوار", "hazard": "Moderate"},
        {"city": "Riz", "city_fa": "ریز", "hazard": "High"},
        {"city": "Shabānkāreh", "city_fa": "شبانکاره", "hazard": "Moderate"},
        {"city": "Taheri", "city_fa": "طاهری", "hazard": "High"},
        {"city": "Gāvbandi", "city_fa": "گاوبندی", "hazard": "High"},
        {"city": "Genaveh", "city_fa": "گناوه", "hazard": "Moderate"},
    ],
    "Hormozgan": [
        {"city": "Bandar Abbas", "city_fa": "بندرعباس", "hazard": "High"},
        {"city": "Bandar Khamir", "city_fa": "بندر خمیر", "hazard": "High"},
        {"city": "Bandar Lengeh", "city_fa": "بندر لنگه", "hazard": "High"},
        {"city": "Bastak", "city_fa": "بستک", "hazard": "High"},
        {"city": "Jask", "city_fa": "جاسک", "hazard": "High"},
        {"city": "Charak", "city_fa": "چارک", "hazard": "High"},
        {"city": "Hajiabad", "city_fa": "حاجی‌آباد", "hazard": "High"},
        {"city": "Rudān", "city_fa": "رودان", "hazard": "High"},
        {"city": "Qeshm", "city_fa": "قشم", "hazard": "High"},
        {"city": "Kish", "city_fa": "کیش", "hazard": "High"},
        {"city": "Gavbandi", "city_fa": "گاوبندی", "hazard": "High"},
        {"city": "Lavan", "city_fa": "لاوان", "hazard": "High"},
        {"city": "Minab", "city_fa": "میناب", "hazard": "High"},
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
        st.session_state.step = min(13, st.session_state.step + 1)

def map_direction_to_axis_and_vector(dir_str, persian=False):
    d = (dir_str or "").strip().lower()
    s = 1 / math.sqrt(2)

    if d in ('north-south', 'north–south', 'north south'):
        return 'NS', 'شمال–جنوب' if persian else 'North–South', (0, 1)
    if d in ('east-west', 'east–west', 'east west'):
        return 'EW', 'شرق–غرب' if persian else 'East–West', (1, 0)
    if d in ('northeast-southwest', 'northeast–southwest', 'northeast southwest'):
        return 'NE_SW', 'شمال‌شرقی–جنوب‌غربی' if persian else 'Northeast–Southwest', (s, s)
    if d in ('northwest-southeast', 'northwest–southeast', 'northwest southeast'):
        return 'SE_NW', 'شمال‌غربی–جنوب‌شرقی' if persian else 'Northwest–Southeast', (-s, s)

    if d in ('north', 'n'):
        return 'NS', 'شمال' if persian else 'North', (0, 1)
    if d in ('south', 's'):
        return 'NS', 'جنوب' if persian else 'South', (0, -1)
    if d in ('east', 'e'):
        return 'EW', 'شرق' if persian else 'East', (1, 0)
    if d in ('west', 'w'):
        return 'EW', 'غرب' if persian else 'West', (-1, 0)
    if d in ('northeast', 'ne'):
        return 'NE_SW', 'شمال‌شرقی' if persian else 'Northeast', (s, s)
    if d in ('southwest', 'sw'):
        return 'NE_SW', 'جنوب‌غربی' if persian else 'Southwest', (-s, -s)
    if d in ('southeast', 'se'):
        return 'SE_NW', 'جنوب‌شرقی' if persian else 'Southeast', (s, -s)
    if d in ('northwest', 'nw'):
        return 'SE_NW', 'شمال‌غربی' if persian else 'Northwest', (-s, s)

    return 'NS', 'شمال–جنوب' if persian else 'North–South', (0, 1)


def axis_label(axis, persian=False):
    labels = {
        'NS':    ('شمال–جنوب',              'North–South'),
        'EW':    ('شرق–غرب',               'East–West'),
        'NE_SW': ('شمال‌شرقی–جنوب‌غربی',   'Northeast–Southwest'),
        'SE_NW': ('جنوب‌شرقی–شمال‌غربی',   'Southeast–Northwest'),
    }
    fa, en = labels.get(axis, ('شمال–جنوب', 'North–South'))
    return fa if persian else en


def create_orientation_diagram(axis_key, land_length, land_width, arrow_vec):
    """
    Creates a diagram with a fixed rectangle and a double-headed arrow showing wind direction.
    
    Args:
        axis_key: The orientation axis key
        land_length: Length of the land (horizontal dimension)
        land_width: Width of the land (vertical dimension)
        arrow_vec: Vector tuple (x, y) indicating arrow direction
    """
    w = float(land_length)
    h = float(land_width)
    
    # Fixed rectangle corners (no rotation)
    corners = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2), (-w/2, -h/2)]
    xs, ys = zip(*corners)
    
    fig = go.Figure()
    
    # Draw the fixed rectangle
    fig.add_trace(go.Scatter(
        x=xs, y=ys, 
        mode='lines', 
        fill='toself',
        fillcolor='rgba(60,140,220,0.3)', 
        line=dict(color='rgb(30,90,160)', width=2),
        showlegend=False, 
        hoverinfo='skip'
    ))
    
    # Calculate arrow length (70% of the smaller dimension)
    arrow_length = min(w, h) * 0.7
    
    # Calculate arrow endpoints based on direction vector
    dx = arrow_vec[0] * arrow_length / 2
    dy = arrow_vec[1] * arrow_length / 2
    
    # Add double-headed arrow (from -dx,-dy to +dx,+dy)
    # First arrow head (positive direction)
    fig.add_annotation(
        x=dx, y=dy,
        ax=-dx, ay=-dy,
        xref='x', yref='y',
        axref='x', ayref='y',
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor='red',
        showarrow=True
    )
    
    # Second arrow head (negative direction)
    fig.add_annotation(
        x=-dx, y=-dy,
        ax=dx, ay=dy,
        xref='x', yref='y',
        axref='x', ayref='y',
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor='red',
        showarrow=True
    )
    
    # Add dimension labels
    # Length label (bottom)
    fig.add_annotation(
        x=0, y=-h/2 - 10,
        text=f"{land_length} m",
        showarrow=False,
        font=dict(size=12, color='black')
    )
    
    # Width label (left side)
    fig.add_annotation(
        x=-w/2 - 15, y=0,
        text=f"{land_width} m",
        showarrow=False,
        font=dict(size=12, color='black'),
        textangle=-90
    )
    
    # Set layout
    pad = max(w, h) * 0.25
    fig.update_layout(
        xaxis=dict(range=[-w/2-pad, w/2+pad], visible=False),
        yaxis=dict(range=[-h/2-pad, h/2+pad], visible=False),
        width=700, 
        height=500, 
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False,
        plot_bgcolor='white'
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

total_steps = 14
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
    st.write(
        "Click the button under the image to select a generation and proceed." if not persian else
        "برای انتخاب نسل و ادامه، دکمه زیر تصویر را کلیک کنید."
    )
    st.markdown("---")

    left_col = st.container()
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", key="back_btn_step1", on_click=go_back)


# === STEP 2: Cabin Geometry ===
if st.session_state.get("step", 0) == 2:
    st.header(get_text('select_cabin_geometry', persian))
    st.markdown(
        "Choose a cabin shape." if not persian else "یک شکل کابین انتخاب کنید."
    )

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
                st.error(f"Could not load image: {img_path}")
            st.caption(label)
            if label == get_text('geom_spherical', persian):
                st.markdown(
                    f"<p style='font-size:12px; color:gray; text-align:center;'>"
                    f"{get_text('geom_spherical_caption', persian)}</p>",
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
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", key="geom_back_btn", on_click=go_back)


# === STEP 3: Primary parameters ===
elif st.session_state.step == 3:

    if st.session_state.get('scroll_to_top'):
        components.html(
            """<script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>""",
            height=0,
        )
        st.session_state.scroll_to_top = False

    st.header(get_text('cabin_specification', persian))
    st.subheader(
        f"{'نسل' if persian else 'Generation'}: {st.session_state.generation_type}"
    )

    if st.session_state.get('validation_errors'):
        for e in st.session_state.validation_errors:
            st.error(e)
        st.session_state.validation_errors = []

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        diameter = st.number_input(
            get_text('diameter_label', persian),
            min_value=30, max_value=80,
            value=int(st.session_state.diameter),
            step=1, key="diameter_input"
        )
        st.session_state.diameter = diameter

    geometry = st.session_state.cabin_geometry
    base = base_for_geometry(diameter, geometry) if geometry else (np.pi * diameter / 4.0)
    min_c, max_c = calc_min_max_from_base(base)

    num_cabins = st.number_input(
        get_text('num_cabins_label', persian),
        min_value=min_c, max_value=max_c,
        value=min(max(int(st.session_state.num_cabins), min_c), max_c),
        step=1, key="num_cabins_input"
    )
    st.session_state.num_cabins = num_cabins

    c1, c2 = st.columns(2)
    with c1:
        cabin_capacity = st.number_input(
            get_text('cabin_cap_label', persian),
            min_value=4, max_value=8,
            value=st.session_state.cabin_capacity,
            step=1, key="cabin_capacity_input"
        )
        st.session_state.cabin_capacity = cabin_capacity
    with c2:
        num_vip = st.number_input(
            get_text('num_vip_label', persian),
            min_value=0, max_value=st.session_state.num_cabins,
            value=min(st.session_state.num_vip_cabins, st.session_state.num_cabins),
            step=1, key="num_vip_input"
        )
        st.session_state.num_vip_cabins = num_vip

    st.markdown("---")
    if st.button(
        "🔄 Calculate Capacities" if not persian else "🔄 محاسبه ظرفیت‌ها"
    ):
        vip_cap = max(0, st.session_state.cabin_capacity - 2)
        vip_total = st.session_state.num_vip_cabins * vip_cap
        regular_total = (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity
        per_rotation = vip_total + regular_total
        c1, c2 = st.columns(2)
        c1.metric(
            "Per-rotation capacity" if not persian else "ظرفیت به ازای هر دور",
            f"{per_rotation} {'passengers' if not persian else 'مسافر'}"
        )
        c2.metric(
            "VIP capacity (per rotation)" if not persian else "ظرفیت ویژه (به ازای هر دور)",
            f"{vip_total} {'passengers' if not persian else 'مسافر'} "
            f"({'each VIP' if not persian else 'هر ظرفیت ویژه'}: {vip_cap})"
        )
        st.success(
            "Capacities calculated." if not persian else "ظرفیت‌ها محاسبه شدند."
        )
        st.session_state.capacities_calculated = True

    st.markdown("---")
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)

# === STEP 4: Rotation Time ===
elif st.session_state.step == 4:
    st.header(get_text('rotation_time', persian))
    st.markdown("---")

    diameter = st.session_state.diameter
    circumference = np.pi * diameter
    default_rotation_time_min = (circumference / 0.2) / 60.0 if diameter > 0 else 1.0

    rotation_time_min = st.number_input(
        "Rotation time (minutes per full rotation)" if not persian else "زمان چرخش (دقیقه به ازای یک دور کامل)",
        min_value=0.01, max_value=60.0,
        value=st.session_state.rotation_time_min if st.session_state.rotation_time_min else float(default_rotation_time_min),
        step=0.01, format="%.2f", key="rotation_time_input"
    )
    st.session_state.rotation_time_min = rotation_time_min

    ang, rpm, linear = calc_ang_rpm_linear_from_rotation_time(rotation_time_min, diameter)

    st.text_input(
        "Rotational speed (rpm)" if not persian else "سرعت چرخش (دور در دقیقه)",
        value=f"{rpm:.6f}", disabled=True
    )
    st.caption(
        f"Angular speed (rad/s): {ang:.6f}" if not persian else f"سرعت زاویه‌ای (رادیان بر ثانیه): {ang:.6f}"
    )
    st.text_input(
        "Linear speed at rim (m/s)" if not persian else "سرعت خطی در لبه چرخ (متر بر ثانیه)",
        value=f"{linear:.6f}", disabled=True
    )

    cap_per_hour = calculate_capacity_per_hour_from_time(st.session_state.num_cabins, st.session_state.cabin_capacity,
                                                          st.session_state.num_vip_cabins, rotation_time_min)
    st.metric(
        "Estimated Capacity per Hour" if not persian else "ظرفیت تخمینی در ساعت",
        f"{cap_per_hour:.0f} {'passengers/hour' if not persian else 'مسافر/ساعت'}"
    )

    st.markdown("---")
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)



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

    st.markdown(get_text('design_ref_step5', persian))
    st.markdown("---")

    PROVINCE_FA = {
        "Khuzestan": "خوزستان", "Ilam": "ایلام", "Fars": "فارس",
        "Qazvin": "قزوین", "Zanjan": "زنجان", "Hamedan": "همدان",
        "Markazi": "مرکزی", "Yazd": "یزد", "Semnan": "سمنان",
        "Qom": "قم", "South Khorasan": "خراسان جنوبی", "Kerman": "کرمان",
        "East Azerbaijan": "آذربایجان شرقی", "West Azerbaijan": "آذربایجان غربی",
        "Ardabil": "اردبیل", "Kurdistan": "کردستان", "Kermanshah": "کرمانشاه",
        "Lorestan": "لرستان", "Chaharmahal and Bakhtiari": "چهارمحال و بختیاری",
        "Kohgiluyeh and Boyer-Ahmad": "کهگیلویه و بویراحمد", "Isfahan": "اصفهان",
        "Tehran": "تهران", "Alborz": "البرز", "Gilan": "گیلان",
        "Mazandaran": "مازندران", "Golestan": "گلستان",
        "North Khorasan": "خراسان شمالی", "Khorasan Razavi": "خراسان رضوی",
        "Sistan and Baluchestan": "سیستان و بلوچستان", "Bushehr": "بوشهر",
        "Hormozgan": "هرمزگان",
    }

    iran_provinces = list(TERRAIN_CATEGORIES.keys())

    c1, c2 = st.columns(2)
    with c1:
        province = st.selectbox(
            get_text('select_province', persian),
            options=iran_provinces,
            index=0,
            format_func=lambda x: PROVINCE_FA.get(x, x) if persian else x,
            key="province_select"
        )

        city_data = CITIES_DATA.get(province, [])
        if city_data:
            city_fa_map = {c["city"]: c.get("city_fa", c["city"]) for c in city_data}
            city_options = [c["city"] for c in city_data]
            city = st.selectbox(
                get_text('select_city', persian),
                options=city_options,
                format_func=lambda x: city_fa_map.get(x, x) if persian else x,
                key="city_select"
            )
        else:
            city = st.text_input(get_text('select_city', persian), key="city_input")

    with c2:
        region_name = st.text_input(
            get_text('region_name', persian),
            value=st.session_state.environment_data.get('region_name', ''),
            key="region_name_input"
        )

    st.markdown("---")
    st.subheader(get_text('land_surface_area', persian))
    l1, l2 = st.columns(2)
    with l1:
        land_length = st.number_input(
            get_text('land_length', persian),
            min_value=10, max_value=150,
            value=int(st.session_state.environment_data.get('land_length', 100)),
            step=1, key="land_length_input"
        )
    with l2:
        land_width = st.number_input(
            get_text('land_width', persian),
            min_value=10, max_value=150,
            value=int(st.session_state.environment_data.get('land_width', 100)),
            step=1, key="land_width_input"
        )
    st.metric(get_text('total_land_area', persian), f"{land_length * land_width} m²")

    st.markdown("---")
    st.subheader(get_text('altitude_temp', persian))
    a1, a2 = st.columns(2)
    with a1:
        temp_max = st.number_input(
            get_text('max_temp', persian),
            value=int(st.session_state.environment_data.get('temp_max', 40)),
            step=1, key="temp_max_input"
        )
    with a2:
        temp_min = st.number_input(
            get_text('min_temp', persian),
            value=int(st.session_state.environment_data.get('temp_min', -10)),
            step=1, key="temp_min_input"
        )
    altitude = st.number_input(
        get_text('altitude', persian),
        value=int(st.session_state.environment_data.get('altitude', 0)),
        step=1, key="altitude_input"
    )

    st.markdown("---")
    st.subheader(get_text('wind_information', persian))
    w1, w2 = st.columns(2)

    wind_directions_en = ["North", "South", "East", "West", "Northeast", "Northwest", "Southeast", "Southwest"]
    wind_directions_fa = ["شمال", "جنوب", "شرق", "غرب", "شمال‌شرق", "شمال‌غرب", "جنوب‌شرق", "جنوب‌غرب"]

    with w1:
        wind_dir = st.selectbox(
            get_text('wind_direction_label', persian),
            options=wind_directions_en,
            format_func=lambda x: wind_directions_fa[wind_directions_en.index(x)] if persian else x,
            key="wind_dir_input"
        )

    with w2:
        wind_max = st.number_input(
            get_text('wind_speed_second', persian),
            min_value=0,
            value=int(st.session_state.environment_data.get('wind_max', 108)),
            step=1, key="wind_max_input"
        )
        wind_max_ms = float(wind_max) / 3.6
        st.caption(f"{get_text('speed_label', persian)}: {wind_max_ms:.2f} m/s")

        wind_avg = st.number_input(
            get_text('wind_speed_minute', persian),
            min_value=0,
            value=int(st.session_state.environment_data.get('wind_avg', 54)),
            step=1, key="wind_avg_input"
        )
        wind_avg_ms = float(wind_avg) / 3.6
        st.caption(f"{get_text('speed_label', persian)}: {wind_avg_ms:.2f} m/s")

    st.markdown("---")
    load_wind = st.checkbox(
        get_text('load_wind_rose', persian),
        value=st.session_state.get('wind_rose_loaded', False),
        key="load_wind_checkbox"
    )
    st.session_state.wind_rose_loaded = load_wind
    if load_wind:
        wind_file = st.file_uploader(
            get_text('wind_rose_file', persian),
            type=['jpg', 'jpeg', 'pdf'],
            key="wind_rose_uploader"
        )
        st.session_state.wind_rose_file = wind_file

    if province in TERRAIN_CATEGORIES:
        terrain = TERRAIN_CATEGORIES[province]
        seismic = get_seismic_hazard_from_city(province, city)
    else:
        terrain = {"category": "II", "z0": 0.05, "zmin": 2, "desc": ""}
        seismic = "Unknown"

    st.session_state.environment_data = {
        'province': province, 'city': city, 'region_name': region_name,
        'land_length': land_length, 'land_width': land_width,
        'land_area': land_length * land_width, 'altitude': altitude,
        'temp_min': temp_min, 'temp_max': temp_max,
        'wind_direction': wind_dir, 'wind_max': wind_max, 'wind_avg': wind_avg,
        'terrain_category': terrain['category'],
        'terrain_desc': terrain.get('desc', ''), 'seismic_hazard': seismic
    }

    st.markdown("---")
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)


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

    st.markdown(
        "**Terrain classification per AS 1170.4-2007(A1), ISIRI 2800**" if not persian else
        "**طبقه‌بندی زمین طبق AS 1170.4-2007(A1)، ISIRI 2800**"
    )
    st.markdown("---")

    env = st.session_state.environment_data
    province = env.get('province', 'Tehran')
    city = env.get('city', '')

    PROVINCE_FA = {
        "Khuzestan": "خوزستان", "Ilam": "ایلام", "Fars": "فارس",
        "Qazvin": "قزوین", "Zanjan": "زنجان", "Hamedan": "همدان",
        "Markazi": "مرکزی", "Yazd": "یزد", "Semnan": "سمنان",
        "Qom": "قم", "South Khorasan": "خراسان جنوبی", "Kerman": "کرمان",
        "East Azerbaijan": "آذربایجان شرقی", "West Azerbaijan": "آذربایجان غربی",
        "Ardabil": "اردبیل", "Kurdistan": "کردستان", "Kermanshah": "کرمانشاه",
        "Lorestan": "لرستان", "Chaharmahal and Bakhtiari": "چهارمحال و بختیاری",
        "Kohgiluyeh and Boyer-Ahmad": "کهگیلویه و بویراحمد", "Isfahan": "اصفهان",
        "Tehran": "تهران", "Alborz": "البرز", "Gilan": "گیلان",
        "Mazandaran": "مازندران", "Golestan": "گلستان",
        "North Khorasan": "خراسان شمالی", "Khorasan Razavi": "خراسان رضوی",
        "Sistan and Baluchestan": "سیستان و بلوچستان", "Bushehr": "بوشهر",
        "Hormozgan": "هرمزگان",
    }
    city_data = CITIES_DATA.get(province, [])
    city_fa_map = {c["city"]: c.get("city_fa", c["city"]) for c in city_data}
    province_display = PROVINCE_FA.get(province, province) if persian else province
    city_display = city_fa_map.get(city, city) if persian else city

    st.subheader(f"{'استان انتخاب شده' if persian else 'Selected Province'}: {province_display}")
    st.subheader(f"{'شهر انتخاب شده' if persian else 'Selected City'}: {city_display}")
    st.info(f"**{'منطقه' if persian else 'Region'}:** {env.get('region_name', 'N/A')}")

    if province in TERRAIN_CATEGORIES:
        terrain = TERRAIN_CATEGORIES[province]
        seismic = get_seismic_hazard_from_city(province, city)

        st.markdown("---")
        st.subheader("Terrain Information" if not persian else "اطلاعات زمین")
        if st.button(
            "🔄 Calculate Terrain Parameters" if not persian else "🔄 محاسبه پارامترهای زمین",
            type="primary"
        ):
            st.session_state.terrain_calculated = True

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**{'Terrain Category' if not persian else 'دسته‌بندی زمین'}:** {terrain['category']}")
                st.markdown(f"**{'Description' if not persian else 'توضیحات'}:** {terrain.get('desc_fa', terrain.get('desc', 'N/A')) if persian else terrain.get('desc', 'N/A')}")
            with col2:
                seismic_color = {"Very High": "🔴", "High": "🟠", "Moderate": "🟡", "Low": "🟢", "Very Low": "🟢"}
                seismic_label = "Seismic Hazard (ISIRI 2800)" if not persian else "خطر لرزه‌ای (ISIRI 2800)"
                st.markdown(f"{seismic_color.get(seismic, '')} **{seismic_label}:** {seismic}")

            if st.session_state.terrain_calculated:
                st.markdown("---")
                st.success(
                    "✅ Terrain parameters have been calculated. You can proceed to the next step." if not persian else
                    "✅ پارامترهای زمین محاسبه شدند. می‌توانید به مرحله بعد بروید."
                )

    st.markdown("---")
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)


# === STEP 7: Soil Type (auto-calculate Importance Group) ===
elif st.session_state.step == 7:
    st.header(get_text('soil_type', persian))
    st.markdown(
        "**Soil classification per ISIRI 2800 (4th Edition)**" if not persian else
        "**طبقه‌بندی خاک طبق ISIRI 2800 (ویرایش چهارم)**"
    )
    st.markdown("---")

    st.subheader("Soil Type Selection" if not persian else "انتخاب نوع خاک")

    soil_types = {
        "Type I": {
            "desc_en": "a. Coarse- and fine-grained igneous rocks, very hard and strong sedimentary rocks, and other hard conglomerate and silicate sedimentary rocks.\nb. Hard soils (dense sand and very stiff clay) with a total thickness of less than 30 meters above bedrock.",
            "desc_fa": "الف. سنگ‌های آذرین درشت‌دانه و ریزدانه، سنگ‌های رسوبی بسیار سخت و محکم و سایر سنگ‌های رسوبی سخت.\nب. خاک‌های سخت (شن متراکم و رس بسیار سفت) با ضخامت کل کمتر از ۳۰ متر.",
            "group_factor": 1.4,
            "importance_group": "Group 1"
        },
        "Type II": {
            "desc_en": "a. Weak igneous rocks (such as tuff), moderately cemented sedimentary rocks, and rocks that have been partially weathered.\nb. Hard soils (dense sand and very stiff clay) with a total thickness greater than 30 meters.",
            "desc_fa": "الف. سنگ‌های آذرین ضعیف (مانند توف)، سنگ‌های رسوبی با سیمانه‌شدگی متوسط و سنگ‌هایی که تا حدی هوازده شده‌اند.\nب. خاک‌های سخت با ضخامت کل بیشتر از ۳۰ متر.",
            "group_factor": 1.2,
            "importance_group": "Group 2"
        },
        "Type III": {
            "desc_en": "a. Weathered or decomposed metamorphic rocks.\nb. Medium dense soils, layers of sand and clay with moderate cohesion and medium stiffness.",
            "desc_fa": "الف. سنگ‌های دگرگونی هوازده یا تجزیه‌شده.\nب. خاک‌های با تراکم متوسط، لایه‌های شن و رس با چسبندگی و سختی متوسط.",
            "group_factor": 1.0,
            "importance_group": "Group 3"
        },
        "Type IV": {
            "desc_en": "a. Soft soils with high moisture content due to a shallow groundwater level.\nb. Any soil profile that includes at least 7 meters of clayey soil with a plasticity index greater than 20 or a moisture content higher than 40 percent.",
            "desc_fa": "الف. خاک‌های نرم با رطوبت بالا به دلیل سطح آب‌های زیرزمینی کم‌عمق.\nب. هر پروفیل خاکی که حداقل ۷ متر خاک رسی با شاخص خمیرایی بیشتر از ۲۰ یا رطوبت بیشتر از ۴۰ درصد داشته باشد.",
            "group_factor": 0.8,
            "importance_group": "Group 4"
        }
    }

    for soil_type, data in soil_types.items():
        desc = data['desc_fa'] if persian else data['desc_en']
        with st.expander(f"{soil_type} ({'ضریب' if persian else 'Factor'}: {data['group_factor']})"):
            st.write(desc)

    selected_soil = st.selectbox(
        "Select Soil Type" if not persian else "انتخاب نوع خاک",
        options=list(soil_types.keys()),
        key="soil_type_select"
    )
    st.session_state.soil_type = selected_soil

    auto_importance_group = soil_types[selected_soil]['importance_group']
    auto_importance_factor = soil_types[selected_soil]['group_factor']
    st.session_state.importance_group = auto_importance_group

    st.markdown("---")
    st.subheader(
        "Automatically Calculated Importance Group" if not persian else
        "گروه اهمیت محاسبه‌شده به‌صورت خودکار"
    )

    st.success(
        f"**{'Importance Group' if not persian else 'گروه اهمیت'}:** {auto_importance_group} "
        f"({'Factor' if not persian else 'ضریب'}: {auto_importance_factor})"
    )
    st.info(
        "The importance group is automatically determined based on the selected soil type per ISIRI 2800." if not persian else
        "گروه اهمیت به‌صورت خودکار بر اساس نوع خاک انتخاب‌شده طبق ISIRI 2800 تعیین می‌شود."
    )

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Soil Type" if not persian else "نوع خاک", selected_soil)
    with col2:
        st.metric("Soil Factor" if not persian else "ضریب خاک", soil_types[selected_soil]['group_factor'])
    with col3:
        st.metric("Importance Factor" if not persian else "ضریب اهمیت", auto_importance_factor)

    st.markdown("---")
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)


# === STEP 8: Carousel Orientation ===
if st.session_state.step == 8:

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

    st.header(get_text('carousel_orientation', persian))

    if st.session_state.get('validation_errors'):
        for e in st.session_state.validation_errors:
            st.error(e)
        st.session_state.validation_errors = []

    st.markdown(
        "**Wind direction analysis per AS 1170.4-2007(A1), EN 1991-1-4:2005**" if not persian else
        "**تحلیل جهت باد طبق AS 1170.4-2007(A1)، EN 1991-1-4:2005**"
    )
    st.markdown("---")

    env = st.session_state.get('environment_data', {})
    wind_direction = env.get('wind_direction', 'North')
    land_length = env.get('land_length', 100)
    land_width = env.get('land_width', 100)

    axis_key, suggested_label, arrow_vec = map_direction_to_axis_and_vector(wind_direction)

    st.subheader(f"{'جهت پیشنهادی' if persian else 'Suggested Orientation'}: {suggested_label}")
    st.markdown(f"**{'ابعاد زمین' if persian else 'Land dimensions'}:** {land_length} m × {land_width} m")
    st.info(f"{'بر اساس جهت غالب باد' if persian else 'Based on prevailing wind direction'}: {wind_direction}")

    fig = create_orientation_diagram(axis_key, land_length, land_width, arrow_vec)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "✅ Confirm Suggested Orientation" if not persian else "✅ تأیید جهت پیشنهادی"
        ):
            st.session_state.carousel_orientation = axis_key
            st.session_state.orientation_confirmed = True
            st.success(f"{'جهت تأیید شد' if persian else 'Orientation confirmed'}: {suggested_label}")

    with col2:
        st.markdown(
            "**Or select custom orientation:**" if not persian else "**یا یک جهت سفارشی انتخاب کنید:**"
        )

    directions_en = ['North-South', 'East-West', 'Northeast-Southwest', 'Northwest-Southeast']
    directions_fa = ['شمال-جنوب', 'شرق-غرب', 'شمال‌شرقی-جنوب‌غربی', 'جنوب‌شرقی-شمال‌غربی']

    direction_map = {
        'NS': 'North-South', 'EW': 'East-West',
        'NE_SW': 'Northeast-Southwest', 'SE_NW': 'Northwest-Southeast'
    }
    current_orientation = direction_map.get(axis_key, 'North-South')
    init_index = directions_en.index(current_orientation) if current_orientation in directions_en else 0

    custom_direction = st.selectbox(
        get_text('custom_direction', persian),
        options=directions_en,
        index=init_index,
        format_func=lambda x: directions_fa[directions_en.index(x)] if persian else x,
        key="custom_orientation_select"
    )

    if st.button(
        "Set Custom Orientation" if not persian else "تنظیم جهت سفارشی",
        key="set_custom_orientation_btn"
    ):
        axis_key_custom, label_custom, arrow_vec_custom = map_direction_to_axis_and_vector(custom_direction)
        st.session_state.carousel_orientation = axis_key_custom
        st.session_state.orientation_confirmed = True
        st.success(f"{'جهت سفارشی تنظیم شد' if persian else 'Custom orientation set'}: {label_custom}")

        fig_custom = create_orientation_diagram(axis_key_custom, land_length, land_width, arrow_vec_custom)
        st.plotly_chart(fig_custom, use_container_width=True)

    st.markdown("---")
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)


# === STEP 9: Device Classification ===
elif st.session_state.step == 9:
    st.header(get_text('device_classification', persian))

    st.markdown(
        "**Calculation per INSO 8987-1-2023**" if not persian else
        "**محاسبه طبق INSO 8987-1-2023**"
    )
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
    st.info(
        "⚠️ **Note:** Enter your actual braking acceleration for the design analysis" if not persian else
        "⚠️ **توجه:** شتاب ترمز واقعی خود را برای تحلیل طراحی وارد کنید"
    )

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

    st.subheader("⚙️ Device Classification Analysis" if not persian else "⚙️ تحلیل طبقه‌بندی دستگاه")
    st.markdown(
        "**Based on Gravity and Braking Acceleration Only:**" if not persian else
        "**بر اساس گرانش و شتاب ترمز:**"
    )

    param_col1, param_col2, param_col3 = st.columns(3)
    with param_col1:
        st.metric("Rotation Speed" if not persian else "سرعت چرخش", f"{rpm:.4f} rpm")
    with param_col2:
        st.metric("Braking Acceleration" if not persian else "شتاب ترمز", f"{braking_accel:.2f} m/s²")
    with param_col3:
        st.metric("Diameter" if not persian else "قطر", f"{diameter} m")

    def calculate_accelerations_clean(theta, diameter, angular_velocity, braking_accel, g=9.81):
        """
        Calculate accelerations at a given angle (only gravity + braking + centripetal)
        Environmental loads are NOT included in device classification
        """
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

    def calculate_dynamic_product_clean(diameter, height, angular_velocity, braking_accel, g=9.81):
        """
        Calculate dynamic product (only operational accelerations, no environmental loads)
        """
        theta_vals = np.linspace(0, 2*np.pi, 360)
        max_accel = 0
        for theta in theta_vals:
            _, _, a_total = calculate_accelerations_clean(theta, diameter, angular_velocity, braking_accel, g)
            if a_total > max_accel:
                max_accel = a_total
        v = (diameter / 2.0) * angular_velocity
        n = max_accel / g
        p = v * height * n
        return p, n, max_accel

    p_actual, n_actual, max_accel_actual = calculate_dynamic_product_clean(
        diameter, height, angular_velocity, braking_accel
    )

    def classify_intrinsic_secured(p):
        """Intrinsic safety secured per INSO 8987-1-2023"""
        if 0.1 < p <= 25:   return 1
        elif 25 < p <= 100:  return 2
        elif 100 < p <= 200: return 3
        elif p > 200:        return 4
        return None

    def classify_intrinsic_not_secured(p):
        """Intrinsic safety not secured per INSO 8987-1-2023"""
        if 0.1 < p <= 25:   return 2
        elif 25 < p <= 100:  return 3
        elif 100 < p <= 200: return 4
        elif p > 200:        return 5
        return None

    class_secured = classify_intrinsic_secured(p_actual)
    class_not_secured = classify_intrinsic_not_secured(p_actual)

    st.markdown("---")
    st.markdown("**Calculated Values:**" if not persian else "**مقادیر محاسبه شده:**")

    result_col1, result_col2, result_col3 = st.columns(3)
    with result_col1:
        st.metric("Max Acceleration" if not persian else "حداکثر شتاب", f"{max_accel_actual:.3f} m/s²")
        st.caption(f"({n_actual:.3f}g)")
    with result_col2:
        st.metric("Dynamic Product (p)" if not persian else "حاصل‌ضرب دینامیکی", f"{p_actual:.2f}")
    with result_col3:
        st.metric("Linear Velocity" if not persian else "سرعت خطی", f"{(diameter/2.0) * angular_velocity:.3f} m/s")

    st.markdown("---")
    st.subheader(
        "📋 Device Classification per INSO 8987-1-2023" if not persian else
        "📋 طبقه‌بندی دستگاه طبق INSO 8987-1-2023"
    )

    class_col1, class_col2 = st.columns(2)

    with class_col1:
        st.markdown("#### **Intrinsic Safety Secured**" if not persian else "#### **ایمنی ذاتی تأمین شده**")
        st.success(f"**Class {class_secured}**")
        st.markdown("""
| Class | Dynamic Product (P) |
|-------|---------------------|
| 1     | 0.1 < P ≤ 25        |
| 2     | 25 < P ≤ 100        |
| 3     | 100 < P ≤ 200       |
| 4     | 200 < P             |
""")
        if class_secured == 1:
            st.info("✅ Lowest classification - Minimal restraint requirements" if not persian else
                    "✅ پایین‌ترین طبقه - حداقل الزامات مهاربند")
        elif class_secured == 2:
            st.info("✅ Low to moderate classification - Standard restraint" if not persian else
                    "✅ طبقه پایین تا متوسط - مهاربند استاندارد")
        elif class_secured == 3:
            st.warning("⚠️ Moderate to high classification - Enhanced restraint required" if not persian else
                       "⚠️ طبقه متوسط تا بالا - مهاربند تقویت‌شده لازم است")
        elif class_secured == 4:
            st.error("⚠️ Highest classification - Maximum restraint required" if not persian else
                     "⚠️ بالاترین طبقه - حداکثر مهاربند لازم است")

    with class_col2:
        st.markdown("#### **Intrinsic Safety NOT Secured**" if not persian else "#### **ایمنی ذاتی تأمین نشده**")
        st.warning(f"**Class {class_not_secured}**")
        st.markdown("""
| Class | Dynamic Product (P) |
|-------|---------------------|
| 2     | 0.1 < P ≤ 25        |
| 3     | 25 < P ≤ 100        |
| 4     | 100 < P ≤ 200       |
| 5     | 200 < P             |
""")
        if class_not_secured == 2:
            st.info("⚠️ Requires additional safety measures" if not persian else
                    "⚠️ نیازمند اقدامات ایمنی اضافی")
        elif class_not_secured == 3:
            st.warning("⚠️ Enhanced safety measures required" if not persian else
                       "⚠️ اقدامات ایمنی تقویت‌شده لازم است")
        elif class_not_secured == 4:
            st.error("⚠️ Comprehensive safety system required" if not persian else
                     "⚠️ سیستم ایمنی جامع لازم است")
        elif class_not_secured == 5:
            st.error("🚨 Maximum safety classification - Special precautions mandatory" if not persian else
                     "🚨 بالاترین طبقه ایمنی - احتیاط‌های ویژه اجباری است")

    st.session_state.classification_data = {
        'p_actual': p_actual,
        'class_secured': class_secured,
        'class_not_secured': class_not_secured,
        'max_accel_actual': max_accel_actual,
        'n_actual': n_actual,
        'rpm_actual': rpm,
        'angular_velocity': angular_velocity,
        'braking_accel': braking_accel,
    }

    st.info(
        "ℹ️ **Note:** Environmental loads (wind, snow, earthquake) will be calculated separately in the next step and are not included in the device classification." if not persian else
        "ℹ️ **توجه:** بارهای محیطی (باد، برف، زلزله) در مرحله بعد به‌صورت جداگانه محاسبه می‌شوند و در طبقه‌بندی دستگاه لحاظ نشده‌اند."
    )

    st.markdown("---")
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)



# === STEP 10: environmental loads ===
elif st.session_state.step == 10:
    st.header("🌦️ Environmental Loads Analysis" if not persian else "🌦️ تحلیل بارهای محیطی")
    st.caption("Per ISO 17842-2023, AS 3533.1-2009, ISIRI 2800, ISIRI 519")
    st.markdown("---")
    
    diameter = st.session_state.diameter
    height = diameter * 1.1
    
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
    
    cabin_geometry = st.session_state.get('cabin_geometry', 'Square')
    cabin_capacity = st.session_state.get('cabin_capacity', 6)
    cabin_surface_area = estimate_cabin_surface_area(cabin_geometry, cabin_capacity, diameter)
    
    st.info(
        f"**Estimated Cabin Surface Area:** {cabin_surface_area} m² (based on {cabin_geometry}, {cabin_capacity} passengers)" if not persian else
        f"**مساحت تخمینی سطح کابین:** {cabin_surface_area} m² (بر اساس {cabin_geometry}، {cabin_capacity} مسافر)"
    )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    # SNOW LOAD
    with col1:
        enable_snow = st.checkbox(
            "🌨️ Snow Load" if not persian else "🌨️ بار برف",
            value=st.session_state.enable_snow, key="snow_checkbox"
        )
        st.session_state.enable_snow = enable_snow
        
        if enable_snow:
            st.markdown("**Per ISO 17842-2023 §4.3.3.5**")
            snow_coef = st.number_input(
                "Snow Pressure (kN/m²)" if not persian else "فشار برف (کیلونیوتن بر متر مربع)",
                min_value=0.1, max_value=1.0,
                value=st.session_state.snow_coefficient,
                step=0.05, format="%.2f", key="snow_coef_input",
                help="Standard value: 0.2 kN/m² per ISO 17842-2023" if not persian else "مقدار استاندارد: 0.2 kN/m² طبق ISO 17842-2023"
            )
            st.session_state.snow_coefficient = snow_coef
            snow_load_calc = snow_coef * cabin_surface_area
            st.success(
                f"**Snow Force: {snow_load_calc:.2f} kN**" if not persian else
                f"**نیروی برف: {snow_load_calc:.2f} kN**"
            )
            st.caption(
                f"Calculation: {snow_coef} × {cabin_surface_area} m²" if not persian else
                f"محاسبه: {snow_coef} × {cabin_surface_area} m²"
            )
    
    # WIND LOAD
    with col2:
        enable_wind = st.checkbox(
            "💨 Wind Load" if not persian else "💨 بار باد",
            value=st.session_state.enable_wind, key="wind_checkbox"
        )
        st.session_state.enable_wind = enable_wind
        
        if enable_wind:
            st.markdown("**Per ISO 17842-2023 §4.3.3.4**")
            
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
                "0 < H ≤ 8": 0.20, "8 < H ≤ 20": 0.30,
                "20 < H ≤ 35": 0.35, "35 < H ≤ 50": 0.40
            }
            wind_pressure = wind_pressure_map[height_category]
            st.session_state.wind_pressure = wind_pressure
            st.caption(
                f"Base wind pressure q: {wind_pressure} kN/m²" if not persian else
                f"فشار پایه باد q: {wind_pressure} kN/m²"
            )
            
            st.markdown("**Design Factors:**" if not persian else "**ضرایب طراحی:**")
            terror_factor = st.slider(
                "Terror Factor" if not persian else "فاکتور وحشت",
                min_value=1.0, max_value=5.0,
                value=st.session_state.terror_factor, step=0.5,
                key="terror_factor_slider"
            )
            st.session_state.terror_factor = terror_factor
            
            height_factor = st.slider(
                "Height Factor" if not persian else "فاکتور ارتفاع",
                min_value=1.0, max_value=5.0,
                value=st.session_state.height_factor, step=0.5,
                key="height_factor_slider"
            )
            st.session_state.height_factor = height_factor
            
            wind_load_calc = wind_pressure * cabin_surface_area * terror_factor * height_factor
            st.success(
                f"**Wind Force: {wind_load_calc:.2f} kN**" if not persian else
                f"**نیروی باد: {wind_load_calc:.2f} kN**"
            )
            st.caption(
                f"Calculation: {wind_pressure} × {cabin_surface_area} × {terror_factor} × {height_factor}" if not persian else
                f"محاسبه: {wind_pressure} × {cabin_surface_area} × {terror_factor} × {height_factor}"
            )
    
    # EARTHQUAKE LOAD
    with col3:
        enable_earthquake = st.checkbox(
            "🌍 Earthquake Load" if not persian else "🌍 بار زلزله",
            value=st.session_state.enable_earthquake, key="earthquake_checkbox"
        )
        st.session_state.enable_earthquake = enable_earthquake
        
        if enable_earthquake:
            st.markdown("**Per ISO 17842-2023 §4.3.4 & ISIRI 2800**")
            seismic_coef = st.number_input(
                "Seismic Coefficient" if not persian else "ضریب زلزله",
                min_value=0.0, max_value=0.5,
                value=st.session_state.seismic_coefficient,
                step=0.01, format="%.3f", key="seismic_coef_input",
                help="Typical range per ISIRI 2800: 0.10 - 0.35" if not persian else "محدوده معمول طبق ISIRI 2800: 0.10 تا 0.35"
            )
            st.session_state.seismic_coefficient = seismic_coef
            approx_mass = diameter * 500
            earthquake_load_calc = seismic_coef * (approx_mass * 9.81 / 1000)
            st.success(
                f"**Horizontal Force: {earthquake_load_calc:.2f} kN**" if not persian else
                f"**نیروی افقی: {earthquake_load_calc:.2f} kN**"
            )
            st.success(
                f"**Vertical Force: {earthquake_load_calc * 0.5:.2f} kN**" if not persian else
                f"**نیروی عمودی: {earthquake_load_calc * 0.5:.2f} kN**"
            )
            st.caption(
                f"Approx. cabin mass: {approx_mass:.0f} kg" if not persian else
                f"جرم تقریبی کابین: {approx_mass:.0f} kg"
            )
            st.caption(
                f"Calculation: {seismic_coef} × {approx_mass * 9.81 / 1000:.1f} kN" if not persian else
                f"محاسبه: {seismic_coef} × {approx_mass * 9.81 / 1000:.1f} kN"
            )
    
    st.markdown("---")
    
    snow_force = 0.0
    wind_force = 0.0
    earthquake_force_h = 0.0
    earthquake_force_v = 0.0
    
    if st.session_state.enable_snow:
        snow_force = st.session_state.snow_coefficient * cabin_surface_area
    if st.session_state.enable_wind:
        wind_force = (st.session_state.wind_pressure * cabin_surface_area *
                     st.session_state.terror_factor * st.session_state.height_factor)
    if st.session_state.enable_earthquake:
        approx_mass = diameter * 500
        earthquake_force_h = st.session_state.seismic_coefficient * (approx_mass * 9.81 / 1000)
        earthquake_force_v = earthquake_force_h * 0.5
    
    st.subheader("📊 Total Environmental Forces" if not persian else "📊 مجموع نیروهای محیطی")
    
    force_col1, force_col2, force_col3 = st.columns(3)
    with force_col1:
        st.metric(
            "Vertical Forces (Z-axis)" if not persian else "نیروهای عمودی (محور Z)",
            f"{snow_force + earthquake_force_v:.2f} kN"
        )
        if snow_force > 0:
            st.caption(f"{'Snow' if not persian else 'برف'}: {snow_force:.2f} kN ↓")
        if earthquake_force_v > 0:
            st.caption(f"{'Earthquake (vertical)' if not persian else 'زلزله (عمودی)'}: {earthquake_force_v:.2f} kN")
    
    with force_col2:
        st.metric(
            "Horizontal Forces (X-axis)" if not persian else "نیروهای افقی (محور X)",
            f"{wind_force + earthquake_force_h:.2f} kN"
        )
        if wind_force > 0:
            st.caption(f"{'Wind' if not persian else 'باد'}: {wind_force:.2f} kN →")
        if earthquake_force_h > 0:
            st.caption(f"{'Earthquake (horizontal)' if not persian else 'زلزله (افقی)'}: {earthquake_force_h:.2f} kN")
    
    with force_col3:
        total_force = np.sqrt((wind_force + earthquake_force_h)**2 + (snow_force + earthquake_force_v)**2)
        st.metric(
            "Resultant Force" if not persian else "نیروی محصول",
            f"{total_force:.2f} kN"
        )
        st.caption("Vector sum of all forces" if not persian else "حاصل برداری تمام نیروها")
    
    st.markdown("---")
    st.subheader("🎯 3D Force Visualization" if not persian else "🎯 تصویرسازی سه‌بعدی نیروها")
    
    def create_force_diagram(diameter, height, snow_f, wind_f, eq_h, eq_v):
        import plotly.graph_objects as go
        theta = np.linspace(0, 2*np.pi, 100)
        radius = diameter / 2
        x_circle = radius * np.cos(theta)
        y_circle = np.zeros_like(theta)
        z_circle = radius * np.sin(theta) + height/2
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=x_circle, y=y_circle, z=z_circle, mode='lines',
                                   line=dict(color='gray', width=4), name='Ferris Wheel', showlegend=True))
        fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, height/2], mode='lines',
                                   line=dict(color='gray', width=6), name='Support', showlegend=True))
        scale = diameter / 20.0
        origin = [0, 0, height/2]
        if snow_f > 0:
            arrow_length = snow_f * scale
            fig.add_trace(go.Scatter3d(x=[origin[0], origin[0]], y=[origin[1], origin[1]],
                                       z=[origin[2], origin[2] - arrow_length], mode='lines+text',
                                       line=dict(color='blue', width=8),
                                       text=['', f'Snow<br>{snow_f:.1f} kN'], textposition='bottom center',
                                       name=f'Snow: {snow_f:.1f} kN', showlegend=True))
            fig.add_trace(go.Cone(x=[origin[0]], y=[origin[1]], z=[origin[2] - arrow_length],
                                  u=[0], v=[0], w=[-1], sizemode='absolute', sizeref=diameter/10,
                                  showscale=False, colorscale=[[0, 'blue'], [1, 'blue']], showlegend=False))
        if wind_f > 0:
            arrow_length = wind_f * scale
            fig.add_trace(go.Scatter3d(x=[origin[0], origin[0] + arrow_length],
                                       y=[origin[1], origin[1]], z=[origin[2], origin[2]], mode='lines+text',
                                       line=dict(color='green', width=8),
                                       text=['', f'Wind<br>{wind_f:.1f} kN'], textposition='top center',
                                       name=f'Wind: {wind_f:.1f} kN', showlegend=True))
            fig.add_trace(go.Cone(x=[origin[0] + arrow_length], y=[origin[1]], z=[origin[2]],
                                  u=[1], v=[0], w=[0], sizemode='absolute', sizeref=diameter/10,
                                  showscale=False, colorscale=[[0, 'green'], [1, 'green']], showlegend=False))
        if eq_h > 0:
            arrow_length_h = eq_h * scale
            fig.add_trace(go.Scatter3d(x=[origin[0], origin[0] + arrow_length_h],
                                       y=[origin[1], origin[1]], z=[origin[2], origin[2]], mode='lines+text',
                                       line=dict(color='red', width=8, dash='dash'),
                                       text=['', f'EQ-H<br>{eq_h:.1f} kN'], textposition='top center',
                                       name=f'Earthquake (H): {eq_h:.1f} kN', showlegend=True))
            fig.add_trace(go.Cone(x=[origin[0] + arrow_length_h], y=[origin[1]], z=[origin[2]],
                                  u=[1], v=[0], w=[0], sizemode='absolute', sizeref=diameter/10,
                                  showscale=False, colorscale=[[0, 'red'], [1, 'red']], showlegend=False))
        if eq_v > 0:
            arrow_length_v = eq_v * scale
            fig.add_trace(go.Scatter3d(x=[origin[0]], y=[origin[1]], z=[origin[2], origin[2] + arrow_length_v],
                                       mode='lines+text', line=dict(color='orange', width=8, dash='dash'),
                                       text=['', f'EQ-V<br>{eq_v:.1f} kN'], textposition='top center',
                                       name=f'Earthquake (V): {eq_v:.1f} kN', showlegend=True))
            fig.add_trace(go.Cone(x=[origin[0]], y=[origin[1]], z=[origin[2] + arrow_length_v],
                                  u=[0], v=[0], w=[1], sizemode='absolute', sizeref=diameter/10,
                                  showscale=False, colorscale=[[0, 'orange'], [1, 'orange']], showlegend=False))
        fig.update_layout(
            scene=dict(xaxis=dict(title='X (m)', range=[-diameter, diameter]),
                      yaxis=dict(title='Y (m)', range=[-diameter/2, diameter/2]),
                      zaxis=dict(title='Z (m)', range=[0, height*1.2]), aspectmode='data'),
            title='Environmental Forces on Ferris Wheel Structure' if not persian else 'نیروهای محیطی بر سازه چرخ و فلک',
            showlegend=True, height=700
        )
        return fig
    
    fig_forces = create_force_diagram(diameter, height, snow_force, wind_force, earthquake_force_h, earthquake_force_v)
    st.plotly_chart(fig_forces, use_container_width=True)
    
    st.info(
        "**Legend:** Blue = Snow (downward), Green = Wind (horizontal), Red/Orange = Earthquake (horizontal/vertical)" if not persian else
        "**راهنما:** آبی = برف (رو به پایین)، سبز = باد (افقی)، قرمز/نارنجی = زلزله (افقی/عمودی)"
    )
    
    st.session_state.environmental_loads = {
        'snow_force': snow_force, 'wind_force': wind_force,
        'earthquake_force_h': earthquake_force_h, 'earthquake_force_v': earthquake_force_v,
        'total_force': total_force, 'cabin_surface_area': cabin_surface_area,
        'snow_coefficient': st.session_state.snow_coefficient if enable_snow else 0,
        'wind_pressure': st.session_state.wind_pressure if enable_wind else 0,
        'terror_factor': st.session_state.terror_factor if enable_wind else 1,
        'height_factor': st.session_state.height_factor if enable_wind else 1,
        'seismic_coefficient': st.session_state.seismic_coefficient if enable_earthquake else 0,
    }
    
    st.markdown("---")
    st.success(
        "✅ Environmental loads calculated. These will be used for bearing selection in the next step." if not persian else
        "✅ بارهای محیطی محاسبه شدند. این مقادیر در مرحله بعد برای انتخاب یاتاقان استفاده می‌شوند."
    )
    
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)


# === STEP 11: bearing selection ===
elif st.session_state.step == 11:
    st.header("⚙️ Bearing Selection" if not persian else "⚙️ انتخاب یاتاقان")
    st.caption("Based on SKF Spherical Roller Bearings Catalog" if not persian else "بر اساس کاتالوگ یاتاقان‌های غلتکی کروی SKF")
    st.markdown("---")
    
    diameter = st.session_state.diameter
    class_data = st.session_state.get('classification_data', {})
    env_loads = st.session_state.get('environmental_loads', {})
    num_cabins = st.session_state.num_cabins
    cabin_capacity = st.session_state.cabin_capacity
    cabin_mass = cabin_capacity * 75
    
    snow_force = env_loads.get('snow_force', 0) * 1000
    wind_force = env_loads.get('wind_force', 0) * 1000
    eq_force_h = env_loads.get('earthquake_force_h', 0) * 1000
    eq_force_v = env_loads.get('earthquake_force_v', 0) * 1000
    
    st.subheader("📊 Load Summary" if not persian else "📊 خلاصه بارها")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Wheel Diameter" if not persian else "قطر چرخ", f"{diameter} m")
        st.metric("Number of Cabins" if not persian else "تعداد کابین‌ها", num_cabins)
    with col2:
        st.metric("Cabin Mass" if not persian else "جرم کابین", f"{cabin_mass} kg")
        st.metric("Total Cabin Mass" if not persian else "جرم کل کابین‌ها", f"{cabin_mass * num_cabins / 1000:.1f} tons")
    with col3:
        total_env_force = np.sqrt((wind_force + eq_force_h)**2 + (snow_force + eq_force_v)**2)
        st.metric("Total Env. Force" if not persian else "نیروی محیطی کل", f"{total_env_force/1000:.2f} kN")
    
    st.markdown("---")
    
    st.subheader("🔄 Cabin Swing Axle Bearings" if not persian else "🔄 یاتاقان محور چرخش کابین")
    st.caption("Spherical Plain Bearings (Maintenance-Free) - Angular Contact Type")
    
    st.markdown("""
    **Application:** Cabin pivot points allowing free rotation
    - **Type:** Maintenance-free spherical plain bearings (GAC..F series)
    - **Material:** Steel/PTFE composite sliding surface
    - **Lubrication:** Maintenance-free (lifetime lubrication)
    - **Function:** Allows cabin to remain upright during wheel rotation
    """ if not persian else """
    **کاربرد:** نقاط محوری کابین برای چرخش آزاد
    - **نوع:** یاتاقان‌های ساده کروی بدون نیاز به نگهداری (سری GAC..F)
    - **جنس:** سطح لغزنده مرکب فولاد/PTFE
    - **روغنکاری:** بدون نیاز به نگهداری (روغنکاری مادام‌العمر)
    - **عملکرد:** اجازه می‌دهد کابین در حین چرخش چرخ عمودی بماند
    """)
    
    cabin_bearing_load = cabin_mass * 9.81 * 1.5
    st.info(
        f"**Required Load Capacity per Cabin Bearing:** {cabin_bearing_load/1000:.2f} kN" if not persian else
        f"**ظرفیت بار لازم برای هر یاتاقان کابین:** {cabin_bearing_load/1000:.2f} kN"
    )
    
    cabin_bearing_options = [
        {"designation": "GAC 25 F", "d": 25, "D": 47, "C": 21.6, "C0": 34.5},
        {"designation": "GAC 30 F", "d": 30, "D": 55, "C": 27, "C0": 43},
        {"designation": "GAC 35 F", "d": 35, "D": 62, "C": 32.5, "C0": 52},
        {"designation": "GAC 40 F", "d": 40, "D": 68, "C": 39, "C0": 62},
        {"designation": "GAC 45 F", "d": 45, "D": 75, "C": 45.5, "C0": 73.5},
        {"designation": "GAC 50 F", "d": 50, "D": 80, "C": 53, "C0": 85},
        {"designation": "GAC 55 F", "d": 55, "D": 90, "C": 53, "C0": 85},
        {"designation": "GAC 60 F", "d": 60, "D": 95, "C": 63, "C0": 100},
    ]
    
    required_C0 = cabin_bearing_load / 1000
    suitable_cabin_bearings = [b for b in cabin_bearing_options if b['C0'] > required_C0 * 1.2]
    
    if suitable_cabin_bearings:
        selected_cabin_bearing = suitable_cabin_bearings[0]
        st.success(f"""
        **{'Selected Cabin Bearing' if not persian else 'یاتاقان کابین انتخاب‌شده'}:** {selected_cabin_bearing['designation']}
        - {'Bore diameter (d)' if not persian else 'قطر داخلی (d)'}: {selected_cabin_bearing['d']} mm
        - {'Outer diameter (D)' if not persian else 'قطر خارجی (D)'}: {selected_cabin_bearing['D']} mm
        - {'Static load rating (C₀)' if not persian else 'ظرفیت بار استاتیکی (C₀)'}: {selected_cabin_bearing['C0']} kN
        - {'Safety factor' if not persian else 'ضریب اطمینان'}: {selected_cabin_bearing['C0'] / required_C0:.2f}
        """)
        st.session_state.cabin_bearing = selected_cabin_bearing
    else:
        st.error("No suitable bearing found in standard range. Custom bearing required." if not persian else
                 "یاتاقان مناسبی در محدوده استاندارد یافت نشد. یاتاقان سفارشی لازم است.")
        st.session_state.cabin_bearing = None
    
    st.markdown("---")
    
    st.subheader("🎯 Main Spindle Bearings" if not persian else "🎯 یاتاقان محور اصلی")
    st.caption("Spherical Roller Bearings (Tapered Bore) - Heavy Duty")
    
    st.markdown("""
    **Application:** Main wheel rotation axis
    - **Type:** Spherical roller bearings with tapered bore (for easy mounting)
    - **Series:** 222xx, 223xx, 230xx, 231xx (depending on load)
    - **Features:** Self-aligning, high load capacity, suitable for heavy radial and axial loads
    - **Mounting:** On tapered shaft/adapter sleeve
    """ if not persian else """
    **کاربرد:** محور چرخش اصلی چرخ
    - **نوع:** یاتاقان‌های غلتکی کروی با سوراخ مخروطی (برای نصب آسان)
    - **سری:** 222xx، 223xx، 230xx، 231xx (بسته به بار)
    - **ویژگی‌ها:** خودتنظیم، ظرفیت بار بالا، مناسب برای بارهای شعاعی و محوری سنگین
    - **نصب:** روی شفت مخروطی یا آستین آداپتور
    """)
    
    total_wheel_mass = (diameter * 1000 + cabin_mass * num_cabins + diameter * 500)
    radial_load = total_wheel_mass * 9.81
    total_radial_load = np.sqrt(radial_load**2 + (wind_force + eq_force_h)**2)
    axial_load = snow_force + eq_force_v + radial_load * 0.1
    equivalent_load = total_radial_load + 1.5 * axial_load
    
    st.info(f"""
    **{'Main Bearing Load Analysis' if not persian else 'تحلیل بار یاتاقان اصلی'}:**
    - {'Total Wheel Mass' if not persian else 'جرم کل چرخ'}: {total_wheel_mass/1000:.1f} tons
    - {'Radial Load' if not persian else 'بار شعاعی'}: {total_radial_load/1000:.2f} kN
    - {'Axial Load' if not persian else 'بار محوری'}: {axial_load/1000:.2f} kN
    - {'Equivalent Dynamic Load' if not persian else 'بار دینامیکی معادل'}: {equivalent_load/1000:.2f} kN
    """)
    
    spindle_bearing_options = [
        {"designation": "23030 CCK/W33", "d": 150, "D": 225, "C": 531, "C0": 750},
        {"designation": "23032 CCK/W33", "d": 160, "D": 240, "C": 614, "C0": 880},
        {"designation": "23034 CCK/W33", "d": 170, "D": 260, "C": 745, "C0": 1060},
        {"designation": "23036 CCK/W33", "d": 180, "D": 280, "C": 883, "C0": 1250},
        {"designation": "23038 CC/W33", "d": 190, "D": 290, "C": 916, "C0": 1340},
        {"designation": "23040 CC/W33", "d": 200, "D": 310, "C": 1058, "C0": 1530},
        {"designation": "23044 CC/W33", "d": 220, "D": 340, "C": 1261, "C0": 1860},
        {"designation": "23048 CC/W33", "d": 240, "D": 360, "C": 1340, "C0": 2080},
        {"designation": "23052 CC/W33", "d": 260, "D": 400, "C": 1675, "C0": 2550},
        {"designation": "23056 CC/W33", "d": 280, "D": 420, "C": 1797, "C0": 2850},
        {"designation": "23060 CC/W33", "d": 300, "D": 460, "C": 2219, "C0": 3450},
    ]
    
    required_C = (equivalent_load / 1000) * 1.5
    suitable_spindle_bearings = [b for b in spindle_bearing_options if b['C'] > required_C]
    
    if suitable_spindle_bearings:
        selected_spindle_bearing = suitable_spindle_bearings[0]
        st.success(f"""
        **{'Selected Main Spindle Bearing' if not persian else 'یاتاقان محور اصلی انتخاب‌شده'}:** {selected_spindle_bearing['designation']}
        - {'Bore diameter (d)' if not persian else 'قطر داخلی (d)'}: {selected_spindle_bearing['d']} mm
        - {'Outer diameter (D)' if not persian else 'قطر خارجی (D)'}: {selected_spindle_bearing['D']} mm
        - {'Dynamic load rating (C)' if not persian else 'ظرفیت بار دینامیکی (C)'}: {selected_spindle_bearing['C']} kN
        - {'Static load rating (C₀)' if not persian else 'ظرفیت بار استاتیکی (C₀)'}: {selected_spindle_bearing['C0']} kN
        - {'Safety factor' if not persian else 'ضریب اطمینان'}: {selected_spindle_bearing['C'] / (equivalent_load/1000):.2f}
        - **{'Recommended Quantity' if not persian else 'تعداد پیشنهادی'}:** {'2 bearings (one on each side of spindle)' if not persian else '۲ یاتاقان (یکی در هر طرف محور)'}
        """)
        st.info("""
        **Mounting Recommendations:**
        - Use tapered adapter sleeve for easy mounting/dismounting
        - Apply proper preload to prevent bearing slip
        - Use shaft tolerance h6 or h7
        - Housing tolerance H7 or H8
        - Ensure proper alignment during installation
        """ if not persian else """
        **توصیه‌های نصب:**
        - از آستین آداپتور مخروطی برای نصب/جداسازی آسان استفاده کنید
        - پیش‌بار مناسب برای جلوگیری از لغزش یاتاقان اعمال کنید
        - تلرانس شفت h6 یا h7
        - تلرانس مجاری H7 یا H8
        - از تراز بودن صحیح در هنگام نصب اطمینان حاصل کنید
        """)
        st.session_state.spindle_bearing = selected_spindle_bearing
    else:
        st.error("No suitable bearing found in standard range. Consult SKF for custom solution." if not persian else
                 "یاتاقان مناسبی در محدوده استاندارد یافت نشد. برای راه‌حل سفارشی با SKF مشورت کنید.")
        st.session_state.spindle_bearing = None
    
    st.markdown("---")
    st.subheader("📐 Bearing Arrangement Diagram" if not persian else "📐 نمودار چیدمان یاتاقان")
    
    def create_bearing_diagram(diameter):
        import plotly.graph_objects as go
        fig = go.Figure()
        theta = np.linspace(0, 2*np.pi, 100)
        radius = diameter / 2
        x_wheel = radius * np.cos(theta)
        y_wheel = radius * np.sin(theta)
        fig.add_trace(go.Scatter(x=x_wheel, y=y_wheel, mode='lines',
                                 line=dict(color='gray', width=3), name='Wheel Rim', fill='none'))
        fig.add_trace(go.Scatter(x=[-0.5, 0.5], y=[0, 0], mode='lines',
                                 line=dict(color='black', width=8), name='Main Spindle'))
        for side, x_pos in [('Left', -0.3), ('Right', 0.3)]:
            fig.add_trace(go.Scatter(x=[x_pos], y=[0], mode='markers+text',
                                     marker=dict(size=20, color='red', symbol='square'),
                                     text=[f'Main Bearing\n({side})'],
                                     textposition='top center',
                                     name=f'Main Bearing {side}'))
        num_cabins_show = min(8, st.session_state.num_cabins)
        cabin_angles = np.linspace(0, 2*np.pi, num_cabins_show, endpoint=False)
        for i, angle in enumerate(cabin_angles):
            cabin_x = radius * np.cos(angle)
            cabin_y = radius * np.sin(angle)
            fig.add_trace(go.Scatter(x=[cabin_x], y=[cabin_y], mode='markers',
                                     marker=dict(size=12, color='blue', symbol='circle'),
                                     name='Cabin Bearing' if i == 0 else '',
                                     showlegend=(i == 0)))
            cabin_size = diameter * 0.05
            fig.add_shape(type='rect',
                         x0=cabin_x - cabin_size, y0=cabin_y - cabin_size,
                         x1=cabin_x + cabin_size, y1=cabin_y + cabin_size,
                         line=dict(color='lightblue', width=2),
                         fillcolor='rgba(173, 216, 230, 0.3)')
        fig.update_layout(
            title='Bearing Locations on Ferris Wheel' if not persian else 'محل یاتاقان‌ها روی چرخ و فلک',
            xaxis=dict(scaleanchor='y', scaleratio=1, range=[-diameter*0.6, diameter*0.6], title='X (m)'),
            yaxis=dict(range=[-diameter*0.6, diameter*0.6], title='Y (m)'),
            height=600, showlegend=True
        )
        return fig
    
    fig_bearings = create_bearing_diagram(diameter)
    st.plotly_chart(fig_bearings, use_container_width=True)
    
    st.caption("""
    **Legend:**
    - Red squares: Main spindle bearings (Spherical Roller, Tapered Bore)
    - Blue circles: Cabin swing bearings (Spherical Plain, Maintenance-Free)
    - Light blue boxes: Passenger cabins
    """ if not persian else """
    **راهنما:**
    - مربع‌های قرمز: یاتاقان‌های محور اصلی (غلتکی کروی، سوراخ مخروطی)
    - دایره‌های آبی: یاتاقان‌های چرخش کابین (ساده کروی، بدون نگهداری)
    - جعبه‌های آبی روشن: کابین‌های مسافری
    """)
    
    st.markdown("---")
    st.subheader("🔧 Maintenance Recommendations" if not persian else "🔧 توصیه‌های نگهداری")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Cabin Bearings (Maintenance-Free):**
        - ✅ No relubrication required
        - ✅ Sealed design protects against contamination
        - 🔍 Visual inspection: Every 6 months
        - 🔍 Check for wear/play: Annually
        - 🔄 Typical service life: 10-15 years
        """ if not persian else """
        **یاتاقان‌های کابین (بدون نگهداری):**
        - ✅ نیازی به روغنکاری مجدد نیست
        - ✅ طراحی مهر و موم‌شده در برابر آلودگی محافظت می‌کند
        - 🔍 بازرسی بصری: هر ۶ ماه یک‌بار
        - 🔍 بررسی سایش/لقی: سالانه
        - 🔄 عمر سرویس معمول: ۱۰ تا ۱۵ سال
        """)
    
    with col2:
        st.markdown("""
        **Main Spindle Bearings:**
        - 🔧 Relubrication: Every 500-1000 operating hours
        - 🔧 Use lithium-based grease (NLGI Grade 2)
        - 🔍 Vibration monitoring: Monthly
        - 🔍 Temperature monitoring: Continuous
        - 🔍 Detailed inspection: Annually
        - 🔄 Typical service life: 30,000-50,000 hours
        """ if not persian else """
        **یاتاقان‌های محور اصلی:**
        - 🔧 روغنکاری مجدد: هر ۵۰۰ تا ۱۰۰۰ ساعت کارکرد
        - 🔧 از گریس پایه لیتیوم (درجه NLGI 2) استفاده کنید
        - 🔍 پایش ارتعاش: ماهانه
        - 🔍 پایش دما: مداوم
        - 🔍 بازرسی دقیق: سالانه
        - 🔄 عمر سرویس معمول: ۳۰٬۰۰۰ تا ۵۰٬۰۰۰ ساعت
        """)
    
    st.info("""
    **Critical Safety Note:**
    - All bearing replacements must be performed by qualified personnel
    - Follow SKF installation procedures exactly
    - Verify proper alignment and preload after installation
    - Document all maintenance activities
    - Replace bearings showing any signs of wear, damage, or excessive play
    """ if not persian else """
    **نکته ایمنی مهم:**
    - تمام تعویض‌های یاتاقان باید توسط پرسنل واجد شرایط انجام شود
    - دستورالعمل‌های نصب SKF را دقیقاً رعایت کنید
    - پس از نصب، تراز بودن و پیش‌بار صحیح را تأیید کنید
    - تمام فعالیت‌های نگهداری را مستند کنید
    - یاتاقان‌هایی که هرگونه علائم سایش، آسیب یا لقی بیش از حد دارند را تعویض کنید
    """)
    
    st.markdown("---")
    st.success(
        "✅ Bearing selection complete. Proceed to restraint system requirements." if not persian else
        "✅ انتخاب یاتاقان کامل شد. به مرحله الزامات سیستم مهاربند بروید."
    )
    
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)


# === STEP 12: Restraint Type ===
elif st.session_state.step == 12:
    st.header(get_text('restraint_type', persian))
    st.image("assets/Axis_Guide.jpg",
            caption="Axis Guide" if not persian else "راهنمای محورها",
            width=500)
    st.markdown("**ISO 17842-2023 & AS 3533.1-2009+A1-2011**")
    st.markdown("---")
    
    diameter = st.session_state.diameter
    classification_data = st.session_state.get('classification_data', {})
    angular_velocity = classification_data.get('angular_velocity', 0.0)
    braking_accel = classification_data.get('braking_accel', st.session_state.braking_acceleration)
    rpm_actual = classification_data.get('rpm_actual', 0.0)
    snow_load = classification_data.get('snow_load', 0.0)
    wind_load = classification_data.get('wind_load', 0.0)
    earthquake_load = classification_data.get('earthquake_load', 0.0)
    
    st.subheader("Passenger Acceleration Analysis" if not persian else "تحلیل شتاب مسافران")
    
    st.info(f"""**Design Parameters:**
- Rotation Speed: {rpm_actual:.4f} rpm
- Braking Acceleration: {braking_accel:.2f} m/s²
- Diameter: {diameter} m""" if not persian else
f"""**پارامترهای طراحی:**
- سرعت چرخش: {rpm_actual:.4f} دور در دقیقه
- شتاب ترمز: {braking_accel:.2f} m/s²
- قطر: {diameter} متر""")
    
    if any([snow_load > 0, wind_load > 0, earthquake_load > 0]):
        st.info("**Active Additional Loads:**" if not persian else "**بارهای اضافی فعال:**")
        load_info = []
        if snow_load > 0:
            load_info.append(f"🌨️ {'Snow' if not persian else 'برف'}: {snow_load:.2f} kN")
        if wind_load > 0:
            load_info.append(f"💨 {'Wind' if not persian else 'باد'}: {wind_load:.2f} kN")
        if earthquake_load > 0:
            load_info.append(f"🌍 {'Earthquake' if not persian else 'زلزله'}: {earthquake_load:.2f} kN")
        st.write(" | ".join(load_info))
        st.markdown("---")
    
    theta_vals = np.linspace(0, 2*np.pi, 360)
    max_ax = -float('inf')
    max_az = -float('inf')
    min_ax = float('inf')
    min_az = float('inf')
    restraint_zones_iso = []
    restraint_zones_as = []
    
    for theta in theta_vals:
        a_x, a_z, _ = calculate_accelerations_at_angle(
            theta, diameter, angular_velocity, braking_accel, snow_load, wind_load, earthquake_load
        )
        a_x_g = a_x / 9.81
        a_z_g = a_z / 9.81
        a_z_g_mirrored = -a_z_g
        if a_x_g > max_ax: max_ax = a_x_g
        if a_z_g_mirrored > max_az: max_az = a_z_g_mirrored
        if a_x_g < min_ax: min_ax = a_x_g
        if a_z_g_mirrored < min_az: min_az = a_z_g_mirrored
        restraint_zones_iso.append(determine_restraint_area_iso(a_x_g, a_z_g_mirrored))
        restraint_zones_as.append(determine_restraint_area_as(a_x_g, a_z_g_mirrored))
    
    from collections import Counter
    zone_counts_iso = Counter(restraint_zones_iso)
    predominant_zone_iso = zone_counts_iso.most_common(1)[0][0]
    zone_counts_as = Counter(restraint_zones_as)
    predominant_zone_as = zone_counts_as.most_common(1)[0][0]
    
    st.markdown("**Acceleration Ranges:**" if not persian else "**محدوده شتاب‌ها:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Max ax", f"{max_ax:.3f}g")
    with col2: st.metric("Min ax", f"{min_ax:.3f}g")
    with col3: st.metric("Max az", f"{max_az:.3f}g")
    with col4: st.metric("Min az", f"{min_az:.3f}g")
    
    st.markdown("---")
    
    st.subheader("📋 ISO 17842-2023 Analysis")
    restraint_descriptions_iso = {
        1: "Zone 1 - Upper region: Maximum restraint required (full body harness)",
        2: "Zone 2 - Upper-central: Enhanced restraint (over-shoulder restraint)",
        3: "Zone 3 - Central edges: Standard restraint (lap bar or seat belt)",
        4: "Zone 4 - Lower-central: Moderate restraint (seat belt with lap bar)",
        5: "Zone 5 - Lower region: Special consideration required (enhanced harness system)"
    } if not persian else {
        1: "ناحیه ۱ - بالا: حداکثر مهاربند لازم است (بند کمربند تمام‌بدن)",
        2: "ناحیه ۲ - بالا-مرکز: مهاربند تقویت‌شده (مهاربند روی شانه)",
        3: "ناحیه ۳ - لبه‌های مرکزی: مهاربند استاندارد (میله جلوی پا یا کمربند ایمنی)",
        4: "ناحیه ۴ - پایین-مرکز: مهاربند متوسط (کمربند ایمنی با میله جلوی پا)",
        5: "ناحیه ۵ - پایین: نیاز به بررسی ویژه (سیستم بند تقویت‌شده)"
    }
    
    st.success(f"**{'Predominant Zone (ISO)' if not persian else 'ناحیه غالب (ISO)'}:** {predominant_zone_iso}")
    st.info(f"**{'Recommended Restraint (ISO)' if not persian else 'مهاربند پیشنهادی (ISO)'}:** {restraint_descriptions_iso.get(predominant_zone_iso, 'Standard restraint')}")
    
    st.markdown("---")
    st.subheader("📋 AS 3533.1-2009+A1-2011 Analysis")
    restraint_descriptions_as = {
        1: "Zone 1 - Upper region: Maximum restraint required (full body harness)",
        2: "Zone 2 - Upper-central: Enhanced restraint (over-shoulder restraint)",
        3: "Zone 3 - Central region: Standard restraint (lap bar or seat belt)",
        4: "Zone 4 - Lower-central: Moderate restraint (seat belt with lap bar)",
        5: "Zone 5 - Lower region: Special consideration required (enhanced harness system)"
    } if not persian else {
        1: "ناحیه ۱ - بالا: حداکثر مهاربند لازم است (بند کمربند تمام‌بدن)",
        2: "ناحیه ۲ - بالا-مرکز: مهاربند تقویت‌شده (مهاربند روی شانه)",
        3: "ناحیه ۳ - مرکز: مهاربند استاندارد (میله جلوی پا یا کمربند ایمنی)",
        4: "ناحیه ۴ - پایین-مرکز: مهاربند متوسط (کمربند ایمنی با میله جلوی پا)",
        5: "ناحیه ۵ - پایین: نیاز به بررسی ویژه (سیستم بند تقویت‌شده)"
    }
    
    st.success(f"**{'Predominant Zone (AS)' if not persian else 'ناحیه غالب (AS)'}:** {predominant_zone_as}")
    st.info(f"**{'Recommended Restraint (AS)' if not persian else 'مهاربند پیشنهادی (AS)'}:** {restraint_descriptions_as.get(predominant_zone_as, 'Standard restraint')}")
    
    st.markdown("---")
    col_iso, col_as = st.columns(2)
    
    with col_iso:
        st.subheader("ISO 17842 Acceleration Envelope")
        fig_accel_iso = plot_acceleration_envelope_iso(diameter, angular_velocity, braking_accel, snow_load, wind_load, earthquake_load)
        st.plotly_chart(fig_accel_iso, use_container_width=True)
        st.markdown("""
        **ISO Zone Classifications:**
        - **Zone 1** (Purple): Maximum restraint
        - **Zone 2** (Orange): Enhanced restraint
        - **Zone 3** (Yellow): Standard restraint
        - **Zone 4** (Green): Moderate restraint
        - **Zone 5** (Red): Special consideration
        """ if not persian else """
        **طبقه‌بندی نواحی ISO:**
        - **ناحیه ۱** (بنفش): حداکثر مهاربند
        - **ناحیه ۲** (نارنجی): مهاربند تقویت‌شده
        - **ناحیه ۳** (زرد): مهاربند استاندارد
        - **ناحیه ۴** (سبز): مهاربند متوسط
        - **ناحیه ۵** (قرمز): بررسی ویژه
        """)
        st.markdown("**📊 Points Distribution in Zones (ISO):**" if not persian else "**📊 توزیع نقاط در نواحی (ISO):**")
        total_points = len(restraint_zones_iso)
        for zone in sorted(zone_counts_iso.keys()):
            count = zone_counts_iso[zone]
            percentage = (count / total_points) * 100
            st.write(f"- {'Zone' if not persian else 'ناحیه'} {zone}: {count} {'points' if not persian else 'نقطه'} ({percentage:.1f}%)")
    
    with col_as:
        st.subheader("AS 3533.1 Acceleration Envelope")
        fig_accel_as = plot_acceleration_envelope_as(diameter, angular_velocity, braking_accel, snow_load, wind_load, earthquake_load)
        st.plotly_chart(fig_accel_as, use_container_width=True)
        st.markdown("""
        **AS Zone Classifications:**
        - **Zone 1** (Purple): Maximum restraint
        - **Zone 2** (Orange): Enhanced restraint
        - **Zone 3** (Yellow): Standard restraint
        - **Zone 4** (Green): Moderate restraint
        - **Zone 5** (Red): Special consideration
        """ if not persian else """
        **طبقه‌بندی نواحی AS:**
        - **ناحیه ۱** (بنفش): حداکثر مهاربند
        - **ناحیه ۲** (نارنجی): مهاربند تقویت‌شده
        - **ناحیه ۳** (زرد): مهاربند استاندارد
        - **ناحیه ۴** (سبز): مهاربند متوسط
        - **ناحیه ۵** (قرمز): بررسی ویژه
        """)
        st.markdown("**📊 Points Distribution in Zones (AS):**" if not persian else "**📊 توزیع نقاط در نواحی (AS):**")
        total_points = len(restraint_zones_as)
        for zone in sorted(zone_counts_as.keys()):
            count = zone_counts_as[zone]
            percentage = (count / total_points) * 100
            st.write(f"- {'Zone' if not persian else 'ناحیه'} {zone}: {count} {'points' if not persian else 'نقطه'} ({percentage:.1f}%)")
    
    st.session_state.classification_data.update({
        'restraint_zone_iso': predominant_zone_iso, 'restraint_zone_as': predominant_zone_as,
        'max_ax_g': max_ax, 'max_az_g': max_az, 'min_ax_g': min_ax, 'min_az_g': min_az,
        'restraint_description_iso': restraint_descriptions_iso.get(predominant_zone_iso, 'Standard restraint'),
        'restraint_description_as': restraint_descriptions_as.get(predominant_zone_as, 'Standard restraint'),
        'zone_distribution_iso': dict(zone_counts_iso), 'zone_distribution_as': dict(zone_counts_as)
    })
    
    st.markdown("---")
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with right_col:
        st.button("Next ➡️" if not persian else "بعدی ➡️", on_click=validate_current_step_and_next)


# === STEP 13: Final Design Overview ===
elif st.session_state.step == 13:
    st.header(get_text('design_summary', persian))
    st.markdown("---")
    
    st.subheader("🎡 Basic Design Parameters" if not persian else "🎡 پارامترهای پایه طراحی")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**{'Generation' if not persian else 'نسل'}:** {st.session_state.generation_type}")
        st.write(f"**{'Diameter' if not persian else 'قطر'}:** {st.session_state.diameter} m")
        st.write(f"**{'Height' if not persian else 'ارتفاع'}:** {st.session_state.diameter * 1.1:.1f} m")
    with col2:
        st.write(f"**{'Total Cabins' if not persian else 'کل کابین‌ها'}:** {st.session_state.num_cabins}")
        st.write(f"**{'VIP Cabins' if not persian else 'کابین‌های VIP'}:** {st.session_state.num_vip_cabins}")
        st.write(f"**{'Cabin Capacity' if not persian else 'ظرفیت کابین'}:** {st.session_state.cabin_capacity} {'passengers' if not persian else 'مسافر'}")
    with col3:
        if st.session_state.cabin_geometry:
            st.write(f"**{'Cabin Geometry' if not persian else 'هندسه کابین'}:** {st.session_state.cabin_geometry}")
        st.write(f"**{'Rotation Time' if not persian else 'زمان چرخش'}:** {st.session_state.rotation_time_min:.2f} min")
        cap_hour = calculate_capacity_per_hour_from_time(
            st.session_state.num_cabins, st.session_state.cabin_capacity,
            st.session_state.num_vip_cabins, st.session_state.rotation_time_min
        )
        st.write(f"**{'Capacity/Hour' if not persian else 'ظرفیت/ساعت'}:** {cap_hour:.0f} pax/hr")
    
    st.markdown("---")
    st.subheader("🌍 Environment & Site Conditions" if not persian else "🌍 شرایط محیطی و سایت")
    st.caption("Per AS 1170.4-2007(A1), EN 1991-1-4:2005, ISIRI 2800")
    env = st.session_state.environment_data

    PROVINCE_FA = {
        "Khuzestan": "خوزستان", "Ilam": "ایلام", "Fars": "فارس",
        "Qazvin": "قزوین", "Zanjan": "زنجان", "Hamedan": "همدان",
        "Markazi": "مرکزی", "Yazd": "یزد", "Semnan": "سمنان",
        "Qom": "قم", "South Khorasan": "خراسان جنوبی", "Kerman": "کرمان",
        "East Azerbaijan": "آذربایجان شرقی", "West Azerbaijan": "آذربایجان غربی",
        "Ardabil": "اردبیل", "Kurdistan": "کردستان", "Kermanshah": "کرمانشاه",
        "Lorestan": "لرستان", "Chaharmahal and Bakhtiari": "چهارمحال و بختیاری",
        "Kohgiluyeh and Boyer-Ahmad": "کهگیلویه و بویراحمد", "Isfahan": "اصفهان",
        "Tehran": "تهران", "Alborz": "البرز", "Gilan": "گیلان",
        "Mazandaran": "مازندران", "Golestan": "گلستان",
        "North Khorasan": "خراسان شمالی", "Khorasan Razavi": "خراسان رضوی",
        "Sistan and Baluchestan": "سیستان و بلوچستان", "Bushehr": "بوشهر",
        "Hormozgan": "هرمزگان",
    }
    province_val = env.get('province', 'N/A')
    city_val = env.get('city', 'N/A')
    city_data = CITIES_DATA.get(province_val, [])
    city_fa_map = {c["city"]: c.get("city_fa", c["city"]) for c in city_data}
    province_display = PROVINCE_FA.get(province_val, province_val) if persian else province_val
    city_display = city_fa_map.get(city_val, city_val) if persian else city_val

    wind_directions_fa_map = {
        "North": "شمال", "South": "جنوب", "East": "شرق", "West": "غرب",
        "Northeast": "شمال‌شرق", "Northwest": "شمال‌غرب",
        "Southeast": "جنوب‌شرق", "Southwest": "جنوب‌غرب"
    }
    wind_dir_display = wind_directions_fa_map.get(env.get('wind_direction', 'N/A'), env.get('wind_direction', 'N/A')) if persian else env.get('wind_direction', 'N/A')

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{'Province' if not persian else 'استان'}:** {province_display}")
        st.write(f"**{'City' if not persian else 'شهر'}:** {city_display}")
        st.write(f"**{'Region' if not persian else 'منطقه'}:** {env.get('region_name', 'N/A')}")
        st.write(f"**{'Land Area' if not persian else 'مساحت زمین'}:** {env.get('land_area', 0):.2f} m²")
        st.write(f"**{'Altitude' if not persian else 'ارتفاع'}:** {env.get('altitude', 0)} m")
        st.write(f"**{'Temperature Range' if not persian else 'محدوده دما'}:** {env.get('temp_min', 0)}°C {'to' if not persian else 'تا'} {env.get('temp_max', 0)}°C")
    with col2:
        st.write(f"**{'Terrain Category' if not persian else 'دسته‌بندی زمین'}:** {env.get('terrain_category', 'N/A')}")
        st.write(f"**{'Seismic Hazard (ISIRI 2800)' if not persian else 'خطر لرزه‌ای (ISIRI 2800)'}:** {env.get('seismic_hazard', 'N/A')}")
        st.write(f"**{'Wind Direction' if not persian else 'جهت باد'}:** {wind_dir_display}")
        st.write(f"**{'Max Wind Speed' if not persian else 'حداکثر سرعت باد'}:** {env.get('wind_max', 0)} km/h")
    
    st.markdown("---")
    st.subheader("🏗️ Soil & Structural Importance" if not persian else "🏗️ خاک و اهمیت سازه")
    st.caption("Per ISIRI 2800 (4th Edition)")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{'Soil Type' if not persian else 'نوع خاک'}:** {st.session_state.soil_type}")
    with col2:
        st.write(f"**{'Importance Group' if not persian else 'گروه اهمیت'}:** {st.session_state.importance_group}")
    
    st.markdown("---")
    st.subheader("🧭 Carousel Orientation" if not persian else "🧭 جهت‌گیری چرخ و فلک")
    st.caption("Per AS 1170.4-2007(A1), EN 1991-1-4:2005")
    axis_key = st.session_state.get('carousel_orientation', None)
    if axis_key:
        st.write(f"**{'Selected Orientation' if not persian else 'جهت‌گیری انتخاب‌شده'}:** {axis_label(axis_key)}")
        arrow_map = {
            'NS': (0, 1), 'EW': (1, 0),
            'NE_SW': (1/math.sqrt(2), 1/math.sqrt(2)),
            'SE_NW': (-1/math.sqrt(2), 1/math.sqrt(2))
        }
        arrow_vec = arrow_map.get(axis_key, (0, 1))
        fig_final_orientation = create_orientation_diagram(axis_key, env.get('land_length', 100), env.get('land_width', 100), arrow_vec)
        st.plotly_chart(fig_final_orientation, use_container_width=True)
    else:
        st.write(f"**{'Selected Orientation' if not persian else 'جهت‌گیری انتخاب‌شده'}:** N/A")
    
    st.markdown("---")
    st.subheader("⚠️ Safety Classification" if not persian else "⚠️ طبقه‌بندی ایمنی")
    st.caption("Per INSO 8987-1-2023")
    
    if st.session_state.classification_data:
        class_data = st.session_state.classification_data
        st.markdown("**Operational Parameters:**" if not persian else "**پارامترهای عملیاتی:**")
        param_col1, param_col2, param_col3 = st.columns(3)
        with param_col1:
            rpm_actual = class_data.get('rpm_actual', 0)
            st.metric("Rotation Speed" if not persian else "سرعت چرخش", f"{rpm_actual:.4f} rpm")
        with param_col2:
            braking_accel = class_data.get('braking_accel', st.session_state.braking_acceleration)
            st.metric("Braking Acceleration" if not persian else "شتاب ترمز", f"{braking_accel:.2f} m/s²")
        with param_col3:
            st.metric("Max Acceleration" if not persian else "حداکثر شتاب", f"{class_data.get('n_actual', 0):.3f}g")
        
        st.markdown("---")
        st.markdown("**Device Classification (INSO 8987-1-2023):**" if not persian else "**طبقه‌بندی دستگاه (INSO 8987-1-2023):**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Intrinsic Safety **SECURED**" if not persian else "#### ایمنی ذاتی **تأمین شده**")
            class_secured = class_data.get('class_secured', 'N/A')
            p_actual = class_data.get('p_actual', 0)
            if class_secured != 'N/A':
                st.success(f"**Class {class_secured}**")
                st.caption(f"Dynamic Product (p): {p_actual:.2f}")
                secured_desc = {
                    1: "Lowest classification - Minimal restraint requirements" if not persian else "پایین‌ترین طبقه - حداقل الزامات مهاربند",
                    2: "Low to moderate classification - Standard restraint" if not persian else "طبقه پایین تا متوسط - مهاربند استاندارد",
                    3: "Moderate to high classification - Enhanced restraint required" if not persian else "طبقه متوسط تا بالا - مهاربند تقویت‌شده لازم است",
                    4: "Highest classification - Maximum restraint required" if not persian else "بالاترین طبقه - حداکثر مهاربند لازم است"
                }
                st.info(secured_desc.get(class_secured, "Standard restraint"))
                st.markdown("""
**Classification Ranges:**
- Class 1: 0.1 < P ≤ 25
- Class 2: 25 < P ≤ 100
- Class 3: 100 < P ≤ 200
- Class 4: 200 < P
""" if not persian else """
**محدوده طبقه‌بندی:**
- کلاس ۱: 0.1 < P ≤ 25
- کلاس ۲: 25 < P ≤ 100
- کلاس ۳: 100 < P ≤ 200
- کلاس ۴: 200 < P
""")
        with col2:
            st.markdown("#### Intrinsic Safety **NOT Secured**" if not persian else "#### ایمنی ذاتی **تأمین نشده**")
            class_not_secured = class_data.get('class_not_secured', 'N/A')
            if class_not_secured != 'N/A':
                st.warning(f"**Class {class_not_secured}**")
                st.caption(f"Dynamic Product (p): {p_actual:.2f}")
                not_secured_desc = {
                    2: "Requires additional safety measures" if not persian else "نیازمند اقدامات ایمنی اضافی",
                    3: "Enhanced safety measures required" if not persian else "اقدامات ایمنی تقویت‌شده لازم است",
                    4: "Comprehensive safety system required" if not persian else "سیستم ایمنی جامع لازم است",
                    5: "Maximum safety classification - Special precautions mandatory" if not persian else "بالاترین طبقه ایمنی - احتیاط‌های ویژه اجباری است"
                }
                st.info(not_secured_desc.get(class_not_secured, "Additional safety measures required"))
                st.markdown("""
**Classification Ranges:**
- Class 2: 0.1 < P ≤ 25
- Class 3: 25 < P ≤ 100
- Class 4: 100 < P ≤ 200
- Class 5: 200 < P
""" if not persian else """
**محدوده طبقه‌بندی:**
- کلاس ۲: 0.1 < P ≤ 25
- کلاس ۳: 25 < P ≤ 100
- کلاس ۴: 100 < P ≤ 200
- کلاس ۵: 200 < P
""")
        
        snow_load = class_data.get('snow_load', 0.0)
        wind_load = class_data.get('wind_load', 0.0)
        earthquake_load = class_data.get('earthquake_load', 0.0)
        
        if any([snow_load > 0, wind_load > 0, earthquake_load > 0]):
            st.markdown("---")
            st.subheader("🌦️ Additional Load Factors" if not persian else "🌦️ عوامل بار اضافی")
            st.caption("Environmental and seismic loads included in analysis" if not persian else "بارهای محیطی و لرزه‌ای در تحلیل لحاظ شده‌اند")
            load_col1, load_col2, load_col3 = st.columns(3)
            with load_col1:
                if snow_load > 0:
                    cabin_area = class_data.get('cabin_surface_area', 0)
                    snow_coef = class_data.get('snow_coefficient', 0.2)
                    st.metric("🌨️ Snow Load" if not persian else "🌨️ بار برف", f"{snow_load:.2f} kN")
                    st.caption(f"{'Pressure' if not persian else 'فشار'}: {snow_coef:.2f} kN/m²")
                    st.caption(f"{'Area' if not persian else 'مساحت'}: {cabin_area:.2f} m²")
                else:
                    st.write("🌨️ Snow Load: Not applied" if not persian else "🌨️ بار برف: اعمال نشده")
            with load_col2:
                if wind_load > 0:
                    st.metric("💨 Wind Load" if not persian else "💨 بار باد", f"{wind_load:.2f} kN")
                    if st.session_state.get('enable_wind', False):
                        st.caption(f"Terror Factor: {st.session_state.get('terror_factor', 1.0):.1f}")
                        st.caption(f"Height Factor: {st.session_state.get('height_factor', 1.0):.1f}")
                else:
                    st.write("💨 Wind Load: Not applied" if not persian else "💨 بار باد: اعمال نشده")
            with load_col3:
                if earthquake_load > 0:
                    st.metric("🌍 Earthquake Load" if not persian else "🌍 بار زلزله", f"{earthquake_load:.2f} kN")
                    if st.session_state.get('enable_earthquake', False):
                        st.caption(f"Seismic Coef: {st.session_state.get('seismic_coefficient', 0.15):.3f}")
                else:
                    st.write("🌍 Earthquake Load: Not applied" if not persian else "🌍 بار زلزله: اعمال نشده")
        
        cabin_bearing = st.session_state.get('cabin_bearing')
        spindle_bearing = st.session_state.get('spindle_bearing')
        
        if cabin_bearing or spindle_bearing:
            st.markdown("---")
            st.subheader("⚙️ Bearing Selection" if not persian else "⚙️ انتخاب یاتاقان")
            st.caption("Selected from SKF Catalog (Step 11)" if not persian else "انتخاب‌شده از کاتالوگ SKF (مرحله ۱۱)")
            col_bear1, col_bear2 = st.columns(2)
            with col_bear1:
                if cabin_bearing:
                    st.markdown(f"""
**{'Cabin Swing Bearings' if not persian else 'یاتاقان‌های چرخش کابین'}:**
- **{'Type' if not persian else 'نوع'}:** {'Spherical Plain (Maintenance-Free)' if not persian else 'ساده کروی (بدون نگهداری)'}
- **{'Series' if not persian else 'سری'}:** GAC..F
- **{'Designation' if not persian else 'نام‌گذاری'}:** {cabin_bearing['designation']}
- **{'Bore' if not persian else 'قطر داخلی'}:** {cabin_bearing['d']} mm
- **{'Outer Diameter' if not persian else 'قطر خارجی'}:** {cabin_bearing['D']} mm
- **{'Static Load Rating (C₀)' if not persian else 'ظرفیت بار استاتیکی (C₀)'}:** {cabin_bearing['C0']} kN
- **{'Quantity' if not persian else 'تعداد'}:** {st.session_state.num_cabins} ({'one per cabin' if not persian else 'یکی برای هر کابین'})
- **{'Maintenance' if not persian else 'نگهداری'}:** {'Maintenance-free, lifetime lubrication' if not persian else 'بدون نگهداری، روغنکاری مادام‌العمر'}
                    """)
            with col_bear2:
                if spindle_bearing:
                    st.markdown(f"""
**{'Main Spindle Bearings' if not persian else 'یاتاقان‌های محور اصلی'}:**
- **{'Type' if not persian else 'نوع'}:** {'Spherical Roller (Tapered Bore)' if not persian else 'غلتکی کروی (سوراخ مخروطی)'}
- **{'Series' if not persian else 'سری'}:** 230xx
- **{'Designation' if not persian else 'نام‌گذاری'}:** {spindle_bearing['designation']}
- **{'Bore' if not persian else 'قطر داخلی'}:** {spindle_bearing['d']} mm
- **{'Outer Diameter' if not persian else 'قطر خارجی'}:** {spindle_bearing['D']} mm
- **{'Dynamic Load Rating (C)' if not persian else 'ظرفیت بار دینامیکی (C)'}:** {spindle_bearing['C']} kN
- **{'Static Load Rating (C₀)' if not persian else 'ظرفیت بار استاتیکی (C₀)'}:** {spindle_bearing['C0']} kN
- **{'Quantity' if not persian else 'تعداد'}:** {'2 (one each side of spindle)' if not persian else '۲ (یکی در هر طرف محور)'}
- **{'Maintenance' if not persian else 'نگهداری'}:** {'Relubrication every 500-1000 hours' if not persian else 'روغنکاری مجدد هر ۵۰۰ تا ۱۰۰۰ ساعت'}
                    """)
        
        st.markdown("---")
        st.subheader("🔒 Restraint System Requirements" if not persian else "🔒 الزامات سیستم مهاربند")
        col_iso, col_as = st.columns(2)
        with col_iso:
            st.info(f"**ISO 17842-2023**\n\n{'Zone' if not persian else 'ناحیه'} {class_data.get('restraint_zone_iso', 'N/A')}\n\n{class_data.get('restraint_description_iso', 'N/A')}")
        with col_as:
            st.info(f"**AS 3533.1-2009+A1-2011**\n\n{'Zone' if not persian else 'ناحیه'} {class_data.get('restraint_zone_as', 'N/A')}\n\n{class_data.get('restraint_description_as', 'N/A')}")
    
    st.markdown("---")
    
    power_data = calculate_motor_power(
        st.session_state.diameter, st.session_state.num_cabins,
        st.session_state.cabin_capacity, st.session_state.num_vip_cabins,
        st.session_state.rotation_time_min, st.session_state.cabin_geometry
    )
    
    st.subheader("⚙️ Motor & Drive System" if not persian else "⚙️ سیستم موتور و درایو")
    st.caption("Calculated based on total system mass and operational requirements" if not persian else "محاسبه‌شده بر اساس جرم کل سیستم و الزامات عملیاتی")
    
    motor_col1, motor_col2, motor_col3, motor_col4 = st.columns(4)
    with motor_col1:
        st.metric("Rated Power" if not persian else "توان نامی", f"{power_data['rated_power']:.1f} kW",
                 help="Rated motor power with safety factor 1.5" if not persian else "توان نامی موتور با ضریب اطمینان ۱.۵")
    with motor_col2:
        st.metric("Peak Power" if not persian else "توان پیک", f"{power_data['peak_power']:.1f} kW",
                 help="Peak power required during startup" if not persian else "توان پیک مورد نیاز در هنگام راه‌اندازی")
    with motor_col3:
        st.metric("Operational" if not persian else "توان عملیاتی", f"{power_data['operational_power']:.1f} kW",
                 help="Steady-state operational power" if not persian else "توان عملیاتی حالت پایدار")
    with motor_col4:
        breakdown = power_data['breakdown']
        st.metric("Total Mass" if not persian else "جرم کل", f"{breakdown['total_mass']/1000:.1f} ton",
                 help="Total system mass including structure" if not persian else "جرم کل سیستم شامل سازه")
    
    with st.expander("🔍 View Motor Power Calculation Details" if not persian else "🔍 مشاهده جزئیات محاسبه توان موتور"):
        st.markdown(format_power_breakdown(power_data))
    
    st.markdown("---")
    st.subheader("📊 Design Visualization" if not persian else "📊 تصویرسازی طراحی")
    height = st.session_state.diameter * 1.1
    vip_cap = max(0, st.session_state.cabin_capacity - 2)
    total_capacity_per_rotation = (
        st.session_state.num_vip_cabins * vip_cap +
        (st.session_state.num_cabins - st.session_state.num_vip_cabins) * st.session_state.cabin_capacity
    )
    ang = (2.0 * np.pi) / (st.session_state.rotation_time_min * 60.0) if st.session_state.rotation_time_min else 0.0
    fig = create_component_diagram(
        st.session_state.diameter, height, total_capacity_per_rotation,
        power_data['rated_power'], st.session_state.num_cabins, st.session_state.cabin_geometry
    )
    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
    
    st.markdown("---")
    st.subheader("📄 Design Summary Report" if not persian else "📄 گزارش خلاصه طراحی")
    
    class_data = st.session_state.classification_data if st.session_state.classification_data else {}
    snow_load = class_data.get('snow_load', 0.0)
    wind_load = class_data.get('wind_load', 0.0)
    earthquake_load = class_data.get('earthquake_load', 0.0)
    rpm_actual = class_data.get('rpm_actual', 0)
    braking_accel = class_data.get('braking_accel', st.session_state.braking_acceleration)
    class_secured = class_data.get('class_secured', 'N/A')
    class_not_secured = class_data.get('class_not_secured', 'N/A')
    p_actual = class_data.get('p_actual', 0)
    cabin_bearing = st.session_state.get('cabin_bearing')
    spindle_bearing = st.session_state.get('spindle_bearing')

    # (report content remains in English as it's a technical export document)
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
    
    bearing_report = ""
    if cabin_bearing or spindle_bearing:
        bearing_report = "\n### Bearing Selection (Step 11)\n"
        if cabin_bearing:
            bearing_report += f"""
#### Cabin Swing Bearings
- **Designation:** {cabin_bearing['designation']}
- **Bore:** {cabin_bearing['d']} mm, Outer Diameter: {cabin_bearing['D']} mm
- **Static Load Rating:** {cabin_bearing['C0']} kN
- **Quantity:** {st.session_state.num_cabins} (one per cabin)
"""
        if spindle_bearing:
            bearing_report += f"""
#### Main Spindle Bearings
- **Designation:** {spindle_bearing['designation']}
- **Bore:** {spindle_bearing['d']} mm, Outer Diameter: {spindle_bearing['D']} mm
- **Dynamic Load Rating:** {spindle_bearing['C']} kN
- **Static Load Rating:** {spindle_bearing['C0']} kN
- **Quantity:** 2 (one each side of spindle)
"""
    
    with st.expander("📋 View Complete Design Report" if not persian else "📋 مشاهده گزارش کامل طراحی"):
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

### Site Conditions
- **Province:** {env.get('province', 'N/A')}
- **City:** {env.get('city', 'N/A')}
- **Region:** {env.get('region_name', 'N/A')}
- **Land Dimensions:** {env.get('land_length', 0)} m × {env.get('land_width', 0)} m
- **Altitude:** {env.get('altitude', 0)} m above sea level
- **Temperature Range:** {env.get('temp_min', 0)}°C to {env.get('temp_max', 0)}°C

### Wind & Environmental Data
- **Prevailing Wind Direction:** {env.get('wind_direction', 'N/A')}
- **Maximum Wind Speed:** {env.get('wind_max', 0)} km/h
- **Terrain Category:** {env.get('terrain_category', 'N/A')}
- **Carousel Orientation:** {axis_label(st.session_state.carousel_orientation) if st.session_state.get('carousel_orientation') else 'N/A'}

### Geotechnical Data
- **Soil Type:** {st.session_state.soil_type}
- **Importance Group:** {st.session_state.importance_group}
- **Seismic Hazard Level:** {env.get('seismic_hazard', 'N/A')}

### Safety Classification (INSO 8987-1-2023)
- **Intrinsic Safety SECURED:** Class {class_secured}
- **Intrinsic Safety NOT Secured:** Class {class_not_secured}
- **Dynamic Product (p):** {p_actual:.2f}
- **Maximum Acceleration:** {class_data.get('n_actual', 0):.3f}g
{additional_loads_report}
{bearing_report}
### Restraint System Requirements
- **ISO 17842-2023:** Zone {class_data.get('restraint_zone_iso', 'N/A')} - {class_data.get('restraint_description_iso', 'N/A')}
- **AS 3533.1-2009+A1-2011:** Zone {class_data.get('restraint_zone_as', 'N/A')} - {class_data.get('restraint_description_as', 'N/A')}

### Applicable Standards
- INSO 8987-1-2023, ISO 17842-2023, AS 3533.1-2009+A1-2011
- AS 1170.4-2007(A1), EN 1991-1-4:2005+A1-2010
- ISIRI 2800, ISIRI 519, DIN 18800, EN 1993
- SKF Bearing Catalog

---
**Note:** This is a preliminary design report. Final engineering calculations and professional review are required before construction.
        """)
    
    st.info(
        "🚧 **Note:** Detailed structural, electrical, and safety analyses require professional engineering consultation." if not persian else
        "🚧 **توجه:** تحلیل‌های دقیق سازه‌ای، الکتریکی و ایمنی نیازمند مشاوره مهندسی حرفه‌ای هستند."
    )
    
    st.markdown("---")
    l, m, r = st.columns([1, 0.5, 1])
    with l:
        st.button("⬅️ Back" if not persian else "⬅️ بازگشت", on_click=go_back)
    with m:
        st.button("🔄 New Design" if not persian else "🔄 طراحی جدید", on_click=reset_design)
    with r:
        if st.button("📥 Export Report" if not persian else "📥 خروجی گزارش"):
            st.info("Report export functionality - Coming soon!" if not persian else "قابلیت خروجی گزارش - به زودی!")
    
    st.success(
        "✅ Design Complete! All parameters have been configured." if not persian else
        "✅ طراحی کامل شد! تمام پارامترها تنظیم شده‌اند."
    )




