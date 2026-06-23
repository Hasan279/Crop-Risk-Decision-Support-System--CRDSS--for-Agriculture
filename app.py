import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

from src.agronomic_rules import AgronomicRulesEngine, CROP_KNOWLEDGE_BASE

# --- Language Dictionary ---
UI_TEXT = {
    "en": {
        "page_title": "Crop Risk DSS",
        "options": "⚗️ Options",
        "select_city": "Select City",
        "select_crop": "Select Crop",
        "planting_date": "Planting Date",
        "check_next": "Check Next (Days)",
        "tip": "💡 **Tip:** Change the options above to see past weather risks for your crop.",
        "main_header": "📈 Past Weather Risks",
        "sub_header": "See the chance of bad weather for your crop over the year.",
        "no_data": "Data not loaded. Please run the data pipelines first.",
        "doy_label": "Day of the Year",
        "prob_label": "Chance of Bad Weather",
        "chart_title": "Weather Risk Chances",
        "frost": "Frost",
        "heat_stress": "Heat Stress",
        "heavy_rain": "Heavy Rain",
        "planting_label": "Planting",
        "advice_header": "🎯 Farming Advice",
        "advice_sub": "See what the weather means for your farm.",
        "analyzing": "Analyzing risk parameters...",
        "risk_medium": "Medium Weather Risk",
        "risk_optimal": "Good Time to Plant",
        "risk_high": "High Weather Risk Detected",
        "kpi_city": "City",
        "kpi_crop": "Crop",
        "kpi_days": "Days Checked",
        "days": "Days",
        "disclaimer": "*Disclaimer: This advice is based purely on historical weather probabilities and should not substitute professional agronomic consultation.*"
    },
    "ur": {
        "page_title": "فصل کے خطرے کا نظام",
        "options": "⚗️ ترتیبات",
        "select_city": "شہر منتخب کریں",
        "select_crop": "فصل منتخب کریں",
        "planting_date": "کاشت کی تاریخ",
        "check_next": "اگلے دن چیک کریں (Days)",
        "tip": "💡 **ٹپ:** اپنی فصل کے لیے پچھلے موسمی خطرات دیکھنے کے لیے اوپر دی گئی ترتیبات تبدیل کریں۔",
        "main_header": "📈 ماضی کے موسمی خطرات",
        "sub_header": "سال بھر اپنی فصل کے لیے خراب موسم کے امکانات دیکھیں۔",
        "no_data": "ڈیٹا لوڈ نہیں ہوا۔ براہ کرم پہلے ڈیٹا پائپ لائنز چلائیں۔",
        "doy_label": "سال کا دن",
        "prob_label": "خراب موسم کا امکان",
        "chart_title": "موسمی خطرے کے امکانات",
        "frost": "کورے",
        "heat_stress": "گرمی کی شدت",
        "heavy_rain": "شدید بارش",
        "planting_label": "کاشت",
        "advice_header": "🎯 زراعت کا مشورہ",
        "advice_sub": "دیکھیں کہ موسم آپ کے کھیت کے لیے کیا معنی رکھتا ہے۔",
        "analyzing": "خطرے کے پیرامیٹرز کا تجزیہ ہو رہا ہے...",
        "risk_medium": "درمیانہ موسمی خطرہ",
        "risk_optimal": "کاشت کا بہترین وقت",
        "risk_high": "شدید موسمی خطرہ",
        "kpi_city": "شہر",
        "kpi_crop": "فصل",
        "kpi_days": "چیک کیے گئے دن",
        "days": "دن",
        "disclaimer": "*دستبرداری: یہ مشورہ مکمل طور پر تاریخی موسمی امکانات پر مبنی ہے اور اسے پیشہ ورانہ زرعی مشاورت کا متبادل نہیں سمجھا جانا چاہیے۔*"
    }
}

VAL_TRANSLATIONS = {
    "en": {},
    "ur": {
        "Dera Ghazi Khan": "ڈیرہ غازی خان",
        "Faisalabad": "فیصل آباد",
        "Hafizabad": "حافظ آباد",
        "Okara": "اوکاڑہ",
        "Sanghar": "سانگھڑ",
        "Wheat": "گندم",
        "Cotton": "کپاس",
        "Rice": "چاول",
        "Sugarcane": "گنا",
        "Maize": "مکئی"
    }
}

# Set page config
st.set_page_config(
    page_title="Crop Risk DSS",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS Injection for Light Mode & Custom Components
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Noto Nastaliq Urdu', sans-serif;
    }
    
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.2rem;
        padding-top: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* Fix Sidebar Text Colors */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] label {
        color: #f9fafb !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #e5e7eb !important;
        font-weight: 500;
    }

    /* Custom HTML Component Styling */
    .insight-card-optimal {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-radius: 16px;
        padding: 24px;
        color: #166534;
        display: flex;
        gap: 20px;
        align-items: flex-start;
        box-shadow: 0 4px 15px rgba(22, 101, 52, 0.05);
    }
    .insight-card-risk {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
        border-radius: 16px;
        padding: 24px;
        color: #991b1b;
        display: flex;
        gap: 20px;
        align-items: flex-start;
        box-shadow: 0 4px 15px rgba(153, 27, 27, 0.05);
    }
    .insight-card-warn {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fde68a;
        border-radius: 16px;
        padding: 24px;
        color: #92400e;
        display: flex;
        gap: 20px;
        align-items: flex-start;
        box-shadow: 0 4px 15px rgba(146, 64, 14, 0.05);
    }
    .insight-icon {
        font-size: 2.2rem;
        background: rgba(255,255,255,0.8);
        border-radius: 50%;
        min-width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .insight-content {
        display: flex;
        flex-direction: column;
    }
    .insight-title {
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 6px;
    }
    .insight-text {
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
    }
    .kpi-card {
        background: white;
        border: 1px solid #f3f4f6;
        border-radius: 16px;
        padding: 24px 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05), 0 4px 6px -2px rgba(0,0,0,0.03);
        border-color: #e5e7eb;
    }
    .kpi-label {
        color: #6b7280;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }
    .kpi-value {
        color: #111827;
        font-size: 1.5rem;
        font-weight: 700;
        line-height: 1.2;
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .kpi-grid {
            grid-template-columns: 1fr;
            gap: 12px;
        }
        .insight-card-optimal, .insight-card-risk, .insight-card-warn {
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .main-header {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data_path = current_dir / "data" / "processed" / "risk_probabilities.csv"
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError:
        return pd.DataFrame()

import importlib
from src import agronomic_rules
importlib.reload(agronomic_rules)
from src.agronomic_rules import AgronomicRulesEngine, CROP_KNOWLEDGE_BASE

@st.cache_resource
def load_engine_v3():
    return AgronomicRulesEngine()

df = load_data()
engine = load_engine_v3()

# Sidebar Configuration
with st.sidebar:
    lang_choice = st.radio("🌐 Language / زبان", ["English", "اردو"], horizontal=True)
    lang = "en" if lang_choice == "English" else "ur"
    t = UI_TEXT[lang]
    
    st.markdown(f"## {t['options']}")
    st.markdown("---")
    
    cities = sorted(df['city_name'].unique()) if not df.empty else ["Dera Ghazi Khan", "Faisalabad", "Hafizabad", "Okara", "Sanghar"]
    crops = list(CROP_KNOWLEDGE_BASE.keys())
    windows = [15, 30, 45, 60, 90]
    
    def translate_val(val):
        return VAL_TRANSLATIONS[lang].get(val, val)
    
    selected_city = st.selectbox(t['select_city'], cities, format_func=translate_val)
    selected_crop = st.selectbox(t['select_crop'], crops, format_func=translate_val)
    planting_date = st.date_input(t['planting_date'], datetime.today().date())
    selected_window = st.selectbox(t['check_next'], options=windows, index=1)
    
    st.markdown("---")
    st.info(t['tip'])

# Main content
st.markdown(f'<div class="main-header">{t["main_header"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{t["sub_header"]}</div>', unsafe_allow_html=True)

if df.empty:
    st.warning(t['no_data'])
else:
    plant_date_str = planting_date.strftime("%m-%d")
    plant_doy = planting_date.timetuple().tm_yday
    
    subset = df[(df['city_name'] == selected_city) & (df['window_days'] == selected_window)].copy()
    subset['Risk Type'] = subset['risk_type'].str.replace('_', ' ').str.title()
    
    # Map risk types to translated names for the chart
    risk_mapping = {
        "Frost": t["frost"],
        "Heat Stress": t["heat_stress"],
        "Heavy Rain": t["heavy_rain"]
    }
    subset['Risk Type'] = subset['Risk Type'].map(lambda x: risk_mapping.get(x, x))
    
    # Enhance Plotly Chart to match the UI screenshot
    fig = px.line(
        subset, 
        x="DOY", 
        y="probability", 
        color="Risk Type",
        render_mode="svg",
        markers=False,
        labels={"DOY": t["doy_label"], "probability": t["prob_label"]},
        color_discrete_map={
            t["frost"]: "#3b82f6",       # Blue
            t["heat_stress"]: "#ef4444", # Red
            t["heavy_rain"]: "#10b981"   # Green
        }
    )
    
    # Smooth lines and fill
    fig.update_traces(
        line_shape='spline', 
        line=dict(width=3), 
        fill='tozeroy', 
    )
    
    for trace in fig.data:
        if trace.name == t['frost']:
            trace.fillcolor = 'rgba(59, 130, 246, 0.08)'
        elif trace.name == t['heat_stress']:
            trace.fillcolor = 'rgba(239, 68, 68, 0.08)'
        elif trace.name == t['heavy_rain']:
            trace.fillcolor = 'rgba(16, 185, 129, 0.08)'
    
    # Add Planting Date Line
    fig.add_vline(
        x=plant_doy, 
        line_width=2, 
        line_dash="dash", 
        line_color="#4b5563",
        annotation_text=f"{t['planting_label']} ({plant_date_str})", 
        annotation_position="top right",
        annotation_font_color="#4b5563"
    )
    
    # Premium Light Theme Layout matching the screenshot
    fig.update_layout(
        title=dict(text=t['chart_title'], x=0.5, font=dict(size=18, color="#111827", family="Inter", weight="bold")),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Inter", color="#4b5563", size=13),
        yaxis=dict(
            title="",
            tickformat=".0%", 
            showgrid=True, 
            gridcolor="#f3f4f6",
            zerolinecolor="#e5e7eb"
        ),
        xaxis=dict(
            title="",
            showgrid=False, 
            zerolinecolor="#e5e7eb",
            rangeslider=dict(visible=True, bgcolor="#f9fafb", bordercolor="#e5e7eb", thickness=0.08)
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.35,
            xanchor="center",
            x=0.5,
            title=""
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    # ------------------ BOTTOM SECTION ------------------
    st.markdown(f'<div class="main-header">{t["advice_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{t["advice_sub"]}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.spinner(t["analyzing"]):
        recommendation = engine.generate_recommendation(
            city=selected_city, 
            crop=selected_crop, 
            plant_date_str=plant_date_str, 
            window_days=selected_window,
            lang=lang
        )
        
        # Determine styling based on language-agnostic logic or specific string matching
        # Because recommendation changes language, we check for both English and Urdu substrings
        is_optimal = "Good Weather" in recommendation or "موسم سازگار ہے" in recommendation
        is_warning = "Weather Warning" in recommendation or "موسمیاتی انتباہ" in recommendation
        
        card_class = "insight-card-warn"
        icon = "⚠️"
        title = t["risk_medium"]
        
        if is_optimal:
            card_class = "insight-card-optimal"
            icon = "✅"
            title = t["risk_optimal"]
        elif is_warning:
            card_class = "insight-card-risk"
            icon = "🚨"
            title = t["risk_high"]
            
        st.markdown(f"""
        <div class="{card_class}">
            <div class="insight-icon">{icon}</div>
            <div class="insight-content">
                <div class="insight-title" style="{"font-family: 'Noto Nastaliq Urdu', sans-serif;" if lang=='ur' else ""}">{title}</div>
                <div class="insight-text" style="{"font-family: 'Noto Nastaliq Urdu', sans-serif;" if lang=='ur' else ""}">{recommendation.replace(chr(10), '<br>')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(
        f"""<div style="text-align: right; color: #9ca3af; font-size: 0.8rem; margin-top: 8px; font-style: italic; {"font-family: 'Noto Nastaliq Urdu', sans-serif;" if lang=='ur' else ""}">
        {t["disclaimer"]}
        </div>""", 
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">{t["kpi_city"]}</div>
            <div class="kpi-value" style="{"font-family: 'Noto Nastaliq Urdu', sans-serif;" if lang=='ur' else ""}">{translate_val(selected_city)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">{t["kpi_crop"]}</div>
            <div class="kpi-value" style="{"font-family: 'Noto Nastaliq Urdu', sans-serif;" if lang=='ur' else ""}">{translate_val(selected_crop)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">{t["kpi_days"]}</div>
            <div class="kpi-value" style="{"font-family: 'Noto Nastaliq Urdu', sans-serif;" if lang=='ur' else ""}">{selected_window} {t["days"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
