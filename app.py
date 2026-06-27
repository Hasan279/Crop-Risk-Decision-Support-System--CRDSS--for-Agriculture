import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import plotly.graph_objects as go
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
        "disclaimer": "*Disclaimer: This advice is based purely on historical weather probabilities and should not substitute professional agronomic consultation.*",
        "risk_exposure": "Risk Exposure (Next {days} Days)",
        "crop_stages": "Crop Growth Timeline",
        "avg_risk": "Avg Risk",
        "tab_yearly": "📅 Yearly Trend",
        "tab_distribution": "🎯 Risk Distribution",
        "tab_lifecycle": "🌱 Crop Lifecycle"
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
        "disclaimer": "*دستبرداری: یہ مشورہ مکمل طور پر تاریخی موسمی امکانات پر مبنی ہے اور اسے پیشہ ورانہ زرعی مشاورت کا متبادل نہیں سمجھا جانا چاہیے۔*",
        "risk_exposure": "خطرے کی نمائش (اگلے {days} دن)",
        "crop_stages": "فصل کی نشوونما کا ٹائم لائن",
        "avg_risk": "اوسط خطرہ",
        "tab_yearly": "📅 سالانہ رجحان",
        "tab_distribution": "🎯 خطرے کی تقسیم",
        "tab_lifecycle": "🌱 فصل کی زندگی کا دور"
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

# Design System — Crop Risk DSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');

    /* ── Tokens ── */
    :root {
        --forest:   #1a4731;
        --fern:     #2d6a4f;
        --sage:     #52b788;
        --mist:     #f0f7f4;
        --soil:     #3d2b1f;
        --sand:     #f5f0eb;
        --ink:      #111827;
        --slate:    #4b5563;
        --smoke:    #9ca3af;
        --surface:  #ffffff;
        --page:     #f4f7f5;
        --border:   #e4ede8;
        --red:      #c0392b;
        --amber:    #b45309;
        --radius:   14px;
        --shadow-sm: 0 1px 3px rgba(17,24,39,0.06), 0 1px 2px rgba(17,24,39,0.04);
        --shadow-md: 0 4px 16px rgba(17,24,39,0.08), 0 2px 6px rgba(17,24,39,0.04);
        --shadow-lg: 0 12px 32px rgba(17,24,39,0.10), 0 4px 12px rgba(17,24,39,0.06);
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', 'Noto Nastaliq Urdu', sans-serif;
        color: var(--ink);
    }

    /* ── Page background ── */
    [data-testid="stAppViewContainer"] {
        background-color: var(--page);
    }
    [data-testid="stAppViewContainer"] > .main > .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1160px;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: var(--forest);
        border-right: none;
    }
    [data-testid="stSidebar"] * {
        color: #d1e8dc !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #e8f5ee !important;
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stDateInput > div > div > input {
        background-color: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: #e8f5ee !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.12) !important;
    }
    [data-testid="stSidebar"] .stInfo {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #c5ddd0 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #c5ddd0 !important;
    }
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
        background: transparent !important;
    }

    /* ── Page header ── */
    .page-header {
        padding: 0 0 1.5rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--ink);
        letter-spacing: -0.035em;
        line-height: 1.15;
        margin: 0 0 0.35rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .header-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--fern);
        color: #fff;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 99px;
        vertical-align: middle;
        margin-left: 4px;
        position: relative;
        top: -3px;
    }
    .sub-header {
        font-size: 1rem;
        color: var(--slate);
        font-weight: 400;
        letter-spacing: -0.005em;
        margin: 0;
    }

    /* ── KPI cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
    }
    .kpi-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 22px 22px 22px 28px;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 4px;
        background: var(--sage);
        border-radius: 4px 0 0 4px;
    }
    .kpi-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    .kpi-label {
        color: var(--smoke);
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: var(--ink);
        font-size: 1.65rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        line-height: 1.15;
    }

    /* ── Insight / advice cards ── */
    .insight-card-optimal {
        background: linear-gradient(120deg, #f0fdf5 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-left: 5px solid #22c55e;
        border-radius: var(--radius);
        padding: 24px 28px;
        color: #14532d;
        display: flex;
        gap: 20px;
        align-items: flex-start;
        box-shadow: var(--shadow-sm);
    }
    .insight-card-risk {
        background: linear-gradient(120deg, #fff5f5 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
        border-left: 5px solid #ef4444;
        border-radius: var(--radius);
        padding: 24px 28px;
        color: #7f1d1d;
        display: flex;
        gap: 20px;
        align-items: flex-start;
        box-shadow: var(--shadow-sm);
    }
    .insight-card-warn {
        background: linear-gradient(120deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fde68a;
        border-left: 5px solid #f59e0b;
        border-radius: var(--radius);
        padding: 24px 28px;
        color: #78350f;
        display: flex;
        gap: 20px;
        align-items: flex-start;
        box-shadow: var(--shadow-sm);
    }
    .insight-icon {
        font-size: 2rem;
        background: rgba(255,255,255,0.85);
        border-radius: 50%;
        min-width: 58px;
        height: 58px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        flex-shrink: 0;
    }
    .insight-content {
        display: flex;
        flex-direction: column;
        flex: 1;
    }
    .insight-title {
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 6px;
        letter-spacing: -0.02em;
    }
    .insight-text {
        line-height: 1.75;
        font-size: 0.97rem;
        opacity: 0.88;
    }

    /* ── Section label ── */
    .section-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--fern);
        margin: 2rem 0 0.6rem 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    /* ── Disclaimer ── */
    .disclaimer {
        font-size: 0.78rem;
        color: var(--smoke);
        font-style: italic;
        text-align: right;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid var(--border);
    }

    /* ── Tab strip ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--mist);
        border-radius: 10px;
        padding: 4px;
        border: 1px solid var(--border);
        width: fit-content;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 7px;
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--slate) !important;
        background: transparent;
        padding: 6px 18px;
        transition: background 0.18s ease;
    }
    .stTabs [aria-selected="true"] {
        background: var(--surface) !important;
        color: var(--ink) !important;
        box-shadow: var(--shadow-sm);
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ── Mobile ── */
    @media (max-width: 768px) {
        .kpi-grid { grid-template-columns: 1fr; gap: 12px; }
        .insight-card-optimal, .insight-card-risk, .insight-card-warn {
            flex-direction: column;
            align-items: flex-start;
            padding: 18px;
        }
        .main-header { font-size: 1.6rem; }
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
st.markdown(f"""
<div class="page-header">
    <div class="main-header">
        🌾 {t["main_header"]}
        <span class="header-pill">DSS</span>
    </div>
    <p class="sub-header">{t["sub_header"]}</p>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning(t['no_data'])
else:
    plant_date_str = planting_date.strftime("%m-%d")
    plant_doy = planting_date.timetuple().tm_yday
    
    # 1. KPIs at the top for immediate context
    st.markdown('<div class="section-label">Current Selection</div>', unsafe_allow_html=True)
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Agronomic Advice Card immediately after KPIs
    st.markdown('<div class="section-label">Farming Advice</div>', unsafe_allow_html=True)
    with st.spinner(t["analyzing"]):
        recommendation = engine.generate_recommendation(
            city=selected_city, 
            crop=selected_crop, 
            plant_date_str=plant_date_str, 
            window_days=selected_window,
            lang=lang
        )
        
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
        f"""<div class="disclaimer" style="{"font-family: 'Noto Nastaliq Urdu', sans-serif;" if lang=='ur' else ""}">
        {t["disclaimer"]}
        </div>""", 
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="section-label">Detailed Analysis</div>', unsafe_allow_html=True)
    
    # 3. Use Tabs for the detailed visualizations so it doesn't overwhelm the user
    tab1, tab2, tab3 = st.tabs([t["tab_distribution"], t["tab_yearly"], t["tab_lifecycle"]])
    
    subset = df[(df['city_name'] == selected_city) & (df['window_days'] == selected_window)].copy()
    subset['Risk Type'] = subset['risk_type'].str.replace('_', ' ').str.title()
    
    risk_mapping = {
        "Frost": t["frost"],
        "Heat Stress": t["heat_stress"],
        "Heavy Rain": t["heavy_rain"]
    }
    subset['Risk Type'] = subset['Risk Type'].map(lambda x: risk_mapping.get(x, x))
    
    with tab1:
        # Radar Chart for Average Risk in Window
        target_doys = [(plant_doy + i - 1) % 365 + 1 for i in range(selected_window)]
        exposure_subset = subset[subset['DOY'].isin(target_doys)]
        if not exposure_subset.empty:
            avg_risks = exposure_subset.groupby('Risk Type')['probability'].mean().reset_index()
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=avg_risks['probability'],
                theta=avg_risks['Risk Type'],
                fill='toself',
                line_color='#2d6a4f',
                fillcolor='rgba(45, 106, 79, 0.15)'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, max(0.1, avg_risks['probability'].max() + 0.1)], tickformat=".0%", gridcolor="#e4ede8", tickfont=dict(color="#9ca3af", size=11)),
                    angularaxis=dict(gridcolor="#e4ede8"),
                    bgcolor="rgba(0,0,0,0)"
                ),
                showlegend=False,
                title=dict(text=t['risk_exposure'].format(days=selected_window), font=dict(family="DM Sans", size=17, color="#111827", weight="bold")),
                margin=dict(l=40, r=40, t=54, b=20),
                height=420,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
    with tab2:
        # Yearly Trend Plotly Chart
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
        
        fig.update_layout(
            title=dict(text=t['chart_title'], x=0.5, font=dict(size=18, color="#111827", family="DM Sans", weight="bold")),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#4b5563", size=13),
            yaxis=dict(
                title="",
                tickformat=".0%", 
                showgrid=True, 
                gridcolor="#eef2ef",
                zerolinecolor="#e4ede8"
            ),
            xaxis=dict(
                title="",
                showgrid=False, 
                zerolinecolor="#e4ede8",
                rangeslider=dict(visible=True, bgcolor="#f4f7f5", bordercolor="#e4ede8", thickness=0.06)
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
            height=420
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Gantt Chart for Crop Stages
        crop_rules = CROP_KNOWLEDGE_BASE.get(selected_crop, {})
        if crop_rules:
            stage_data = []
            
            ur_stages = {
                "Vegetative": "نشوونما",
                "Flowering & Grain Filling": "پھول اور دانے بننے کا عمل",
                "Maturity & Harvest": "پکنا اور کٹائی",
                "Flowering & Boll Formation": "پھول اور ٹینڈے بننے کا عمل",
                "Flowering & Heading": "پھول اور خوشے بننے کا عمل",
                "Germination & Tillering": "اگاؤ اور شگوفے نکلنا",
                "Grand Growth": "تیز نشوونما",
                "Silking & Tasseling": "سِلکنگ اور ٹیسلنگ",
                "Maturity": "پکائی"
            }
            
            for stage_name, rules in crop_rules.items():
                stage_start = datetime.combine(planting_date, datetime.min.time()) + timedelta(days=rules['start_day'])
                stage_end = datetime.combine(planting_date, datetime.min.time()) + timedelta(days=rules['end_day'])
                
                display_stage_name = ur_stages.get(stage_name, stage_name) if lang == "ur" else stage_name
                risk_trigger = rules['risk'].replace('_', ' ').title()
                display_risk = risk_mapping.get(risk_trigger, risk_trigger)
                
                stage_data.append({
                    "Stage": display_stage_name,
                    "Start": stage_start,
                    "Finish": stage_end,
                    "Risk Trigger": display_risk
                })
            
            df_stages = pd.DataFrame(stage_data)
            
            fig_stages = px.timeline(
                df_stages, 
                x_start="Start", 
                x_end="Finish", 
                y="Stage", 
                color="Risk Trigger",
                color_discrete_map={
                    t["frost"]: "#3b82f6",
                    t["heat_stress"]: "#ef4444",
                    t["heavy_rain"]: "#10b981"
                }
            )
            fig_stages.update_yaxes(autorange="reversed")
            fig_stages.update_layout(
                title=dict(text=t['crop_stages'], font=dict(family="DM Sans", size=17, color="#111827", weight="bold")),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#4b5563", size=13),
                xaxis=dict(showgrid=True, gridcolor="#eef2ef", title=""),
                yaxis=dict(title="", tickfont=dict(family="Noto Nastaliq Urdu" if lang=="ur" else "DM Sans")),
                margin=dict(l=20, r=20, t=50, b=20),
                height=420,
                showlegend=False
            )
            st.plotly_chart(fig_stages, use_container_width=True)