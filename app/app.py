# streamlit application

import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# ── Auto Database Initialization ───────────────────────────────────────────────
# Adds app/ folder to path so startup.py can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from startup import initialize_database
initialize_database()

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Food Wastage Pattern Analysis",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH    = os.path.join(BASE_DIR, "database", "food_wastage.db")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ── DB Connection ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_connection()

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-right: 1px solid #2ecc71;
}
[data-testid="stSidebar"] * { color: #ecf0f1 !important; }
[data-testid="stSidebar"] .stRadio label {
    background: rgba(46,204,113,0.1);
    border: 1px solid rgba(46,204,113,0.3);
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0;
    display: block;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(46,204,113,0.25);
    border-color: #2ecc71;
}

.main { background: #0d1117; }
.block-container { padding: 2rem 2rem 2rem 2rem; }

.hero-banner {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 40%, #1a1a2e 100%);
    border: 1px solid #2ecc71;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(46,204,113,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem; font-weight: 700;
    color: #2ecc71; margin: 0 0 0.5rem 0; line-height: 1.2;
}
.hero-subtitle { font-size: 1.1rem; color: #95a5a6; margin: 0; }
.hero-tag {
    display: inline-block;
    background: rgba(46,204,113,0.15);
    border: 1px solid #2ecc71; color: #2ecc71;
    padding: 4px 12px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 600;
    margin-top: 1rem; letter-spacing: 0.05em;
}

.metric-card {
    background: #161b22; border: 1px solid #21262d;
    border-radius: 12px; padding: 1.2rem 1.5rem;
    position: relative; overflow: hidden; transition: border-color 0.2s;
}
.metric-card:hover { border-color: #2ecc71; }
.metric-card::after {
    content: ''; position: absolute;
    bottom: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #2ecc71, #27ae60);
}
.metric-label {
    font-size: 0.75rem; color: #8b949e;
    text-transform: uppercase; letter-spacing: 0.08em;
    font-weight: 600; margin-bottom: 0.4rem;
}
.metric-value { font-size: 2rem; font-weight: 700; color: #e6edf3; line-height: 1; }
.metric-icon  { font-size: 1.5rem; margin-bottom: 0.5rem; }

.section-header {
    font-size: 1.4rem; font-weight: 700; color: #e6edf3;
    border-left: 4px solid #2ecc71; padding-left: 1rem;
    margin: 2rem 0 1rem 0;
}

.insight-box {
    background: linear-gradient(135deg, rgba(46,204,113,0.08), rgba(39,174,96,0.04));
    border: 1px solid rgba(46,204,113,0.3);
    border-left: 4px solid #2ecc71; border-radius: 8px;
    padding: 1rem 1.2rem; margin-top: 0.8rem;
    font-size: 0.9rem; color: #c9d1d9; line-height: 1.6;
}

.chart-container {
    background: #161b22; border: 1px solid #21262d;
    border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;
}
.chart-title { font-size: 1rem; font-weight: 600; color: #e6edf3; margin-bottom: 0.8rem; }

.info-card {
    background: #161b22; border: 1px solid #21262d;
    border-radius: 10px; padding: 1.2rem; height: 100%;
}
.info-card-title {
    font-size: 0.85rem; font-weight: 700; color: #2ecc71;
    text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.6rem;
}
.info-card-body { font-size: 0.9rem; color: #8b949e; line-height: 1.7; }

.green-divider { border: none; border-top: 1px solid #2ecc71; opacity: 0.3; margin: 1.5rem 0; }

.page-title    { font-size: 1.8rem; font-weight: 700; color: #e6edf3; margin-bottom: 0.3rem; }
.page-subtitle { font-size: 0.95rem; color: #8b949e; margin-bottom: 1.5rem; }

.form-section {
    background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.2rem 0 0.8rem 0;'>
        <div style='font-size:3rem;'>🍱</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2ecc71; opacity:0.3; margin:0.5rem 0 1rem 0;'>",
                unsafe_allow_html=True)

    page = st.radio(
        "Analytics Hub",
        ["🏠  Home & Overview",
         "📊  Insights & Trends",
         "📈  Analysis",
         "🔎  Filter & Search",
         "⚙️  Manage Listings"],
        label_visibility="collapsed"
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Home & Overview":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🍱 Food Wastage Pattern Analysis</div>
        <div class="hero-subtitle">Analyzing food surplus patterns to reduce wastage across cities </div>
        <div class="hero-tag">📍 Food Management · Waste Reduction · Social Good</div>
    </div>
    """, unsafe_allow_html=True)

    total_providers = pd.read_sql("SELECT COUNT(*) AS c FROM providers",     conn).iloc[0,0]
    total_receivers = pd.read_sql("SELECT COUNT(*) AS c FROM receivers",     conn).iloc[0,0]
    total_listings  = pd.read_sql("SELECT COUNT(*) AS c FROM food_listings", conn).iloc[0,0]
    total_claims    = pd.read_sql("SELECT COUNT(*) AS c FROM claims",        conn).iloc[0,0]
    total_qty       = pd.read_sql("SELECT SUM(Quantity) AS c FROM food_listings", conn).iloc[0,0]
    completed       = pd.read_sql("SELECT COUNT(*) AS c FROM claims WHERE Status='Completed'", conn).iloc[0,0]

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    for col, icon, label, val in zip(
        [c1,c2,c3,c4,c5,c6],
        ["🏪","🤝","🍲","📋","📦","✅"],
        ["Providers","Receivers","Listings","Claims","Total Units","Completed"],
        [total_providers, total_receivers, total_listings,
         total_claims, f"{total_qty:,}", completed]
    ):
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='green-divider'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Why This Dashboard?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
            <div class="info-card-body">
            Food wastage is a growing concern — tonnes of edible food are discarded daily while millions go without. Understanding where, when and why 
            this happens is the first step toward fixing it..<br><br>
            To address this,
            <b style='color:#2ecc71;'>This dashboard analyses</b>
            food donation and claim data across multiple cities to uncover wastage patterns, identify the most active providers and 
            receivers, and highlight areas where food distribution can be improved.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Key Features</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
            <div class="info-card-body">
            <b style='color:#e6edf3;'>Analyse Donation Patterns</b>
            — Explore which cities, food types and providers contribute the most<br><br>
            <b style='color:#e6edf3;'>Understand Claim Behaviour</b>
            — See how claims are distributed across completed, cancelled and pending status<br><br>
            <b style='color:#e6edf3;'>Explore Food Trends</b>
            — Identify which meal types and food categories generate the most surplus<br><br>
            <b style='color:#e6edf3;'>Search and Filter Data</b>
            — Find food listings by city, food type, meal type and provider type<br><br>
            <b style='color:#e6edf3;'>Manage Food Listings</b>
            — Add, update and remove food listings directly through the dashboard
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='green-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Data at a Glance</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="info-card">
            <div style='font-size:1.8rem; margin-bottom:0.4rem;'>🏪</div>
            <div class="info-card-title">Providers</div>
            <div style='font-size:0.8rem; color:#2ecc71; margin-bottom:0.6rem; font-weight:600;'>1,000 Providers</div>
            <div style='font-size:0.78rem; color:#8b949e; line-height:1.8;'>
                • Restaurants<br>• Supermarkets<br>• Grocery Stores<br>• Catering Services
            </div>
            <div style='margin-top:0.8rem; font-size:0.78rem; color:#6e7681;
                        border-top:1px solid #21262d; padding-top:0.6rem;'>
                Spread across multiple cities
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <div style='font-size:1.8rem; margin-bottom:0.4rem;'>🤝</div>
            <div class="info-card-title">Receivers</div>
            <div style='font-size:0.8rem; color:#2ecc71; margin-bottom:0.6rem; font-weight:600;'>1,000 Receivers</div>
            <div style='font-size:0.78rem; color:#8b949e; line-height:1.8;'>
                • NGOs<br>• Charities<br>• Shelters<br>• Individuals
            </div>
            <div style='margin-top:0.8rem; font-size:0.78rem; color:#6e7681;
                        border-top:1px solid #21262d; padding-top:0.6rem;'>
                NGOs are the most active receivers
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="info-card">
            <div style='font-size:1.8rem; margin-bottom:0.4rem;'>🍲</div>
            <div class="info-card-title">Food Listings</div>
            <div style='font-size:0.8rem; color:#2ecc71; margin-bottom:0.6rem; font-weight:600;'>1,000 Food Items</div>
            <div style='font-size:0.78rem; color:#8b949e; line-height:1.8;'>
                • Vegetarian<br>• Vegan<br>• Non-Vegetarian<br>• All meal types
            </div>
            <div style='margin-top:0.8rem; font-size:0.78rem; color:#6e7681;
                        border-top:1px solid #21262d; padding-top:0.6rem;'>
                25,794 total units available
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="info-card">
            <div style='font-size:1.8rem; margin-bottom:0.4rem;'>📋</div>
            <div class="info-card-title">Claims</div>
            <div style='font-size:0.8rem; color:#2ecc71; margin-bottom:0.6rem; font-weight:600;'>1,000 Claims</div>
            <div style='font-size:0.78rem; color:#8b949e; line-height:1.8;'>
                • ✅ Completed — 33.9%<br>
                • ❌ Cancelled — 33.6%<br>
                • ⏳ Pending — 32.5%
            </div>
            <div style='margin-top:0.8rem; font-size:0.78rem; color:#6e7681;
                        border-top:1px solid #21262d; padding-top:0.6rem;'>
                339 successfully completed
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='green-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Key Findings</div>', unsafe_allow_html=True)

    findings = [
        ("","Top Provider","Barry Group leads with 5 successful completed claims and highest total quantity donated (179 units)"),
        ("","Top Cities","South Kathryn & New Carol have the most food listings (6 each), driven by Restaurants and Supermarkets"),
        ("","Most Claimed Food","Rice is the most claimed food item (45 claims), followed by Dairy (43 claims)"),
        ("","Cancellation Alert","33.6% of claims are cancelled — nearly equal to completions, signaling need for better follow-through"),
        ("","Food Type Leader","Vegan food has the highest total donated quantity (8,798 units) despite similar listing count"),
        ("","Meal Pattern","Breakfast is both the most listed AND most claimed meal type — highest surplus and demand"),
    ]
    col1, col2 = st.columns(2)
    for i,(icon,title,desc) in enumerate(findings):
        with (col1 if i%2==0 else col2):
            st.markdown(f"""
            <div style='background:#161b22; border:1px solid #21262d; border-radius:10px;
                        padding:1rem 1.2rem; margin-bottom:0.8rem;
                        display:flex; gap:1rem; align-items:flex-start;'>
                <div style='font-size:1.5rem;'>{icon}</div>
                <div>
                    <div style='font-weight:700; color:#e6edf3; font-size:0.95rem;'>{title}</div>
                    <div style='color:#8b949e; font-size:0.85rem; margin-top:0.2rem; line-height:1.5;'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — INSIGHTS & TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊  Insights & Trends":

    st.markdown('<div class="page-title">📊 Insights & Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">15 charts revealing patterns in food donations, claims, and city-level distribution</div>', unsafe_allow_html=True)

    charts = [
        ("chart1_provider_type.png",             "Univariate",   "Provider Type Distribution",
         "Supermarkets lead with 263 providers, but all 4 types contribute almost equally — a well-balanced provider network."),
        ("chart2_receiver_type.png",              "Univariate",   "Receiver Type Distribution",
         "NGOs receive the most (27.4%) followed by Charities (26.3%). Individuals receive least — more outreach needed."),
        ("chart3_food_type.png",                  "Univariate",   "Food Type Distribution",
         "All 3 food types are listed almost equally (330–336), showing no bias in what providers donate."),
        ("chart4_meal_type.png",                  "Univariate",   "Meal Type Distribution",
         "Breakfast is listed most frequently (255), suggesting breakfast food generates the highest daily surplus."),
        ("chart5_city_listings.png",              "Bivariate",    "Top 10 Cities by Food Listings",
         "New Carol and South Kathryn lead with 6 listings each — the most active food donation cities."),
        ("chart6_provider_quantity.png",          "Bivariate",    "Provider Type vs Total Quantity",
         "Restaurants donate the most quantity (6,923 units) despite not being most numerous — each listing contributes more."),
        ("chart7_foodtype_quantity.png",          "Bivariate",    "Food Type vs Total Quantity",
         "Vegan food has the highest donated quantity (8,798 units) — vegan items are donated in larger batch sizes."),
        ("chart8_mealtype_quantity.png",          "Bivariate",    "Meal Type vs Total Quantity",
         "Snacks lead total donated quantity despite fewer listings — each snack donation is larger in volume."),
        ("chart9_city_provider_quantity.png",     "Multivariate", "City + Provider Type + Quantity",
         "South Kathryn leads with ~180 units driven by Restaurants. Each city relies on a single dominant provider type."),
        ("chart10_foodtype_mealtype_quantity.png","Multivariate", "Food Type + Meal Type + Quantity",
         "Snacks dominate in Non-Vegetarian and Vegan. Vegetarian food breaks pattern with Dinner leading — interesting anomaly."),
        ("chart11_provider_claims.png",           "Multivariate", "Top 10 Providers by Claims",
         "Butler-Richardson leads with 12 total claims — nearly double others. High demand but needs investigation on completion rate."),
        ("chart12_receiver_claims.png",           "Multivariate", "Top 10 Receivers by Claims",
         "Top receivers claim 4–5 times each with no single dominant user — healthy, distributed platform usage."),
        ("chart13_claim_status.png",              "Claims",       "Claim Status Distribution",
         "Only 33.9% complete successfully while 33.6% are cancelled — nearly equal! Automated reminders could improve this."),
        ("chart14_top_receivers.png",             "Claims",       "Top Receivers by Completed Claims",
         "Timothy Garrett, James Miller, Derek Potter and Alexandra Owens are the most reliable receivers (3 completions each)."),
        ("chart15_top_providers.png",             "Claims",       "Top Providers by Successful Claims",
         "Barry Group leads with 5 successful claims. Butler-Richardson drops from #1 total — revealing low completion rate."),
    ]

    categories = ["All","Univariate","Bivariate","Multivariate","Claims"]
    selected_cat = st.radio("Filter by Category", categories, horizontal=True)
    filtered = [(f,c,t,i) for f,c,t,i in charts if selected_cat=="All" or c==selected_cat]

    st.markdown(f"<div style='color:#8b949e; font-size:0.85rem; margin-bottom:1rem;'>Showing {len(filtered)} charts</div>",
                unsafe_allow_html=True)

    badge = {
        "Univariate":   ("#1a3a2a","#2ecc71"),
        "Bivariate":    ("#1a2a3a","#3498db"),
        "Multivariate": ("#2a1a3a","#9b59b6"),
        "Claims":       ("#3a2a1a","#e67e22"),
    }

    for i in range(0, len(filtered), 2):
        cols = st.columns(2)
        for col,(filename,category,title,insight) in zip(cols, filtered[i:i+2]):
            chart_path = os.path.join(ASSETS_DIR, filename)
            bg, fg = badge.get(category, ("#1a1a1a","#aaaaaa"))
            with col:
                st.markdown(f"""
                <div class="chart-container">
                    <div style='display:flex; justify-content:space-between;
                                align-items:center; margin-bottom:0.5rem;'>
                        <div class="chart-title">{title}</div>
                        <div style='background:{bg}; color:{fg}; padding:3px 10px;
                                    border-radius:12px; font-size:0.72rem; font-weight:700;
                                    border:1px solid {fg}; white-space:nowrap;'>{category}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if os.path.exists(chart_path):
                    st.image(chart_path, width=520)
                else:
                    st.warning(f"Run eda.py first — chart not found: {filename}")
                st.markdown(f"""
                <div class="insight-box">💡 <b>Insight:</b> {insight}</div>
                <br>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈  Analysis":

    st.markdown('<div class="page-title">📈 Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">18 queries uncovering business insights — including CTEs and Window Functions</div>', unsafe_allow_html=True)

    queries = {
        "Q1 · Providers per City": {
            "sql": "SELECT City, COUNT(*) AS Total_Providers FROM providers GROUP BY City ORDER BY Total_Providers DESC LIMIT 10",
            "insight": "Shows which cities have the most food providers — useful for identifying high-supply areas.",
            "tag": "SQL"
        },
        "Q2 · Provider Type Contributions": {
            "sql": "SELECT Provider_Type, COUNT(*) AS Total_Listings, SUM(Quantity) AS Total_Quantity FROM food_listings GROUP BY Provider_Type ORDER BY Total_Quantity DESC",
            "insight": "Restaurants lead in total donated quantity despite not being the most numerous provider type.",
            "tag": "SQL"
        },
        "Q3 · Provider Contacts by City": {
            "sql": "SELECT Name, Type, Address, Contact FROM providers WHERE City = 'New Carol' ORDER BY Name",
            "insight": "Retrieves direct contact info of providers in a specific city for coordination.",
            "tag": "SQL"
        },
        "Q4 · Receivers with Most Claims": {
            "sql": "SELECT r.Name, r.Type, COUNT(c.Claim_ID) AS Total_Claims FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Name, r.Type ORDER BY Total_Claims DESC LIMIT 10",
            "insight": "Identifies most active receivers — useful for recognizing reliable platform users.",
            "tag": "SQL"
        },
        "Q5 · Total Food Available": {
            "sql": "SELECT SUM(Quantity) AS Total_Food_Available, COUNT(*) AS Total_Listings, ROUND(AVG(Quantity),2) AS Avg_Quantity_Per_Listing FROM food_listings",
            "insight": "25,794 total food units available with an average of 25.79 units per listing.",
            "tag": "SQL"
        },
        "Q6 · Cities with Most Listings": {
            "sql": "SELECT Location AS City, COUNT(*) AS Total_Listings, SUM(Quantity) AS Total_Quantity FROM food_listings GROUP BY Location ORDER BY Total_Listings DESC LIMIT 10",
            "insight": "South Kathryn and New Carol are the most active food donation cities on the platform.",
            "tag": "SQL"
        },
        "Q7 · Food Type Analysis": {
            "sql": "SELECT Food_Type, COUNT(*) AS Total_Listings, SUM(Quantity) AS Total_Quantity, ROUND(AVG(Quantity),2) AS Avg_Quantity FROM food_listings GROUP BY Food_Type ORDER BY Total_Listings DESC",
            "insight": "Vegetarian leads in listing count but Vegan leads in total quantity — larger batch sizes.",
            "tag": "SQL"
        },
        "Q8 · Claims per Food Item": {
            "sql": "SELECT fl.Food_Name, fl.Food_Type, COUNT(c.Claim_ID) AS Total_Claims FROM food_listings fl LEFT JOIN claims c ON fl.Food_ID = c.Food_ID GROUP BY fl.Food_Name, fl.Food_Type ORDER BY Total_Claims DESC LIMIT 10",
            "insight": "Rice (Vegan) is the most claimed food item with 45 claims, followed by Rice (Vegetarian) at 44.",
            "tag": "SQL"
        },
        "Q9 · Most Successful Providers": {
            "sql": "SELECT p.Name, p.Type, p.City, COUNT(c.Claim_ID) AS Successful_Claims FROM providers p JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID JOIN claims c ON fl.Food_ID = c.Food_ID WHERE c.Status = 'Completed' GROUP BY p.Name, p.Type, p.City ORDER BY Successful_Claims DESC LIMIT 10",
            "insight": "Barry Group leads successful completions — the most reliable provider on the platform.",
            "tag": "SQL"
        },
        "Q10 · Claim Status Breakdown": {
            "sql": "SELECT Status, COUNT(*) AS Total_Claims, ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM claims),2) AS Percentage FROM claims GROUP BY Status ORDER BY Percentage DESC",
            "insight": "Completed (33.9%) vs Cancelled (33.6%) — nearly equal, highlighting a critical platform issue.",
            "tag": "SQL"
        },
        "Q11 · Avg Quantity per Receiver": {
            "sql": "SELECT r.Name, r.Type, COUNT(c.Claim_ID) AS Total_Claims, ROUND(AVG(fl.Quantity),2) AS Avg_Quantity FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID JOIN food_listings fl ON c.Food_ID = fl.Food_ID GROUP BY r.Name, r.Type ORDER BY Total_Claims DESC LIMIT 10",
            "insight": "Shows average food quantity received per claim — useful for planning distribution logistics.",
            "tag": "SQL"
        },
        "Q12 · Most Claimed Meal Type": {
            "sql": "SELECT fl.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims, SUM(fl.Quantity) AS Total_Quantity FROM food_listings fl JOIN claims c ON fl.Food_ID = c.Food_ID GROUP BY fl.Meal_Type ORDER BY Total_Claims DESC",
            "insight": "Breakfast is claimed most (278 times) — highest demand matches highest donation frequency.",
            "tag": "SQL"
        },
        "Q13 · Top Donors by Quantity": {
            "sql": "SELECT p.Name, p.Type, p.City, SUM(fl.Quantity) AS Total_Quantity_Donated FROM providers p JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID GROUP BY p.Name, p.Type, p.City ORDER BY Total_Quantity_Donated DESC LIMIT 10",
            "insight": "Barry Group donates the most (179 units) — a key partner for the platform's food supply.",
            "tag": "SQL"
        },
        "Q14 · Food Expiring Soon": {
            "sql": "SELECT fl.Food_Name, fl.Quantity, fl.Expiry_Date, fl.Location, p.Name AS Provider_Name, p.Contact FROM food_listings fl JOIN providers p ON fl.Provider_ID = p.Provider_ID ORDER BY fl.Expiry_Date ASC LIMIT 10",
            "insight": "Critical alert — these items need immediate distribution to prevent waste.",
            "tag": "SQL"
        },
        "Q15 · City-wise Claim Success Rate": {
            "sql": "SELECT p.City, COUNT(c.Claim_ID) AS Total_Claims, SUM(CASE WHEN c.Status='Completed' THEN 1 ELSE 0 END) AS Completed, SUM(CASE WHEN c.Status='Cancelled' THEN 1 ELSE 0 END) AS Cancelled, ROUND(SUM(CASE WHEN c.Status='Completed' THEN 1 ELSE 0 END)*100.0/COUNT(c.Claim_ID),2) AS Success_Rate FROM providers p JOIN food_listings fl ON p.Provider_ID=fl.Provider_ID JOIN claims c ON fl.Food_ID=c.Food_ID GROUP BY p.City ORDER BY Total_Claims DESC LIMIT 10",
            "insight": "City-level success rates reveal where the platform is working well vs where intervention is needed.",
            "tag": "SQL"
        },
        "Q16 · CTE — Provider Performance": {
            "sql": """WITH provider_stats AS (
    SELECT fl.Provider_ID,
           COUNT(DISTINCT fl.Food_ID) AS Total_Listings,
           SUM(fl.Quantity) AS Total_Quantity,
           COUNT(c.Claim_ID) AS Total_Claims
    FROM food_listings fl
    LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
    GROUP BY fl.Provider_ID
),
completed_stats AS (
    SELECT fl.Provider_ID,
           COUNT(c.Claim_ID) AS Completed_Claims
    FROM food_listings fl
    LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
    WHERE c.Status = 'Completed'
    GROUP BY fl.Provider_ID
)
SELECT p.Name, p.Type, p.City,
       ps.Total_Listings, ps.Total_Quantity,
       ps.Total_Claims,
       COALESCE(cs.Completed_Claims,0) AS Completed_Claims,
       ROUND(COALESCE(cs.Completed_Claims,0)*100.0/ps.Total_Claims,2) AS Success_Rate
FROM providers p
JOIN provider_stats ps ON p.Provider_ID = ps.Provider_ID
LEFT JOIN completed_stats cs ON p.Provider_ID = cs.Provider_ID
WHERE ps.Total_Claims > 0
ORDER BY ps.Total_Claims DESC LIMIT 10""",
            "insight": "Uses chained CTEs to compute a combined provider performance score across listings, quantity, and claim success rate.",
            "tag": "CTE"
        },
        "Q17 · Window — Quantity Rank by City": {
            "sql": "SELECT Food_Name, Location AS City, Food_Type, Quantity, RANK() OVER (PARTITION BY Location ORDER BY Quantity DESC) AS Rank_In_City, SUM(Quantity) OVER (PARTITION BY Location) AS City_Total FROM food_listings ORDER BY City, Rank_In_City LIMIT 15",
            "insight": "Uses RANK() window function to rank food items within each city without losing row-level detail.",
            "tag": "Window"
        },
        "Q18 · Window — Running Total of Claims": {
            "sql": "SELECT DATE(Timestamp) AS Claim_Date, COUNT(*) AS Daily_Claims, SUM(COUNT(*)) OVER (ORDER BY DATE(Timestamp)) AS Running_Total, ROUND(AVG(COUNT(*)) OVER (ORDER BY DATE(Timestamp) ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) AS Moving_Avg_3Day FROM claims GROUP BY DATE(Timestamp) ORDER BY Claim_Date LIMIT 15",
            "insight": "Uses SUM() OVER and AVG() OVER window functions to track cumulative claims and 3-day moving average.",
            "tag": "Window"
        },
    }

    tag_style = {
        "SQL":    ("#1a3a2a","#2ecc71"),
        "CTE":    ("#2a1a3a","#9b59b6"),
        "Window": ("#1a2a3a","#3498db"),
    }

    for title, data in queries.items():
        bg, fg = tag_style.get(data["tag"], ("#1a1a1a","#aaa"))
        icon = "🔷" if data["tag"] != "SQL" else "📊"
        with st.expander(f"{icon}  {title}"):
            st.markdown(f"""
            <span style='background:{bg}; color:{fg}; padding:3px 10px;
                         border-radius:12px; font-size:0.75rem; font-weight:700;
                         border:1px solid {fg};'>{data['tag']}</span>
            <br><br>
            """, unsafe_allow_html=True)
            try:
                df = pd.read_sql(data["sql"], conn)
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Query error: {e}")
            st.markdown(f"""
            <div class="insight-box">💡 <b>Insight:</b> {data['insight']}</div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — FILTER & SEARCH
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔎  Filter & Search":

    st.markdown('<div class="page-title">🔎 Filter & Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Find available food listings and provider contacts by applying filters</div>', unsafe_allow_html=True)

    cities     = ["All"] + pd.read_sql("SELECT DISTINCT Location FROM food_listings ORDER BY Location", conn)['Location'].tolist()
    food_types = ["All"] + pd.read_sql("SELECT DISTINCT Food_Type FROM food_listings ORDER BY Food_Type", conn)['Food_Type'].tolist()
    meal_types = ["All"] + pd.read_sql("SELECT DISTINCT Meal_Type FROM food_listings ORDER BY Meal_Type", conn)['Meal_Type'].tolist()
    prov_types = ["All"] + pd.read_sql("SELECT DISTINCT Provider_Type FROM food_listings ORDER BY Provider_Type", conn)['Provider_Type'].tolist()

    st.markdown('<div class="section-header">🎛️ Apply Filters</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: selected_city = st.selectbox("🏙️ City",          cities)
    with c2: selected_food = st.selectbox("🥗 Food Type",     food_types)
    with c3: selected_meal = st.selectbox("🍽️ Meal Type",     meal_types)
    with c4: selected_prov = st.selectbox("🏪 Provider Type", prov_types)

    q = """
        SELECT fl.Food_Name, fl.Quantity, fl.Expiry_Date,
               fl.Food_Type, fl.Meal_Type, fl.Location AS City,
               p.Name AS Provider, p.Type AS Provider_Type,
               p.Contact, p.Address
        FROM food_listings fl
        JOIN providers p ON fl.Provider_ID = p.Provider_ID
        WHERE 1=1
    """
    if selected_city != "All": q += f" AND fl.Location = '{selected_city}'"
    if selected_food != "All": q += f" AND fl.Food_Type = '{selected_food}'"
    if selected_meal != "All": q += f" AND fl.Meal_Type = '{selected_meal}'"
    if selected_prov != "All": q += f" AND fl.Provider_Type = '{selected_prov}'"
    q += " ORDER BY fl.Expiry_Date ASC"

    df = pd.read_sql(q, conn)

    st.markdown("<hr class='green-divider'>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("📋 Listings Found",   len(df))
    c2.metric("📦 Total Quantity",   f"{df['Quantity'].sum():,}" if not df.empty else 0)
    c3.metric("🏪 Unique Providers", df['Provider'].nunique() if not df.empty else 0)

    st.markdown('<div class="section-header">📋 Food Listings</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No listings found. Try a different filter combination.")
    else:
        st.dataframe(df, use_container_width=True, height=350)

    st.markdown('<div class="section-header">📞 Provider Contacts</div>', unsafe_allow_html=True)
    cq = "SELECT Name, Type, City, Contact, Address FROM providers WHERE 1=1"
    if selected_city != "All": cq += f" AND City = '{selected_city}'"
    if selected_prov != "All": cq += f" AND Type = '{selected_prov}'"
    contacts_df = pd.read_sql(cq, conn)
    if contacts_df.empty:
        st.info("No providers found for selected filters.")
    else:
        st.dataframe(contacts_df, use_container_width=True, height=280)

    st.markdown('<div class="section-header">🤝 Receiver Contacts</div>', unsafe_allow_html=True)
    rq = "SELECT Name, Type, City, Contact FROM receivers WHERE 1=1"
    if selected_city != "All": rq += f" AND City = '{selected_city}'"
    receivers_df = pd.read_sql(rq, conn)
    if receivers_df.empty:
        st.info("No receivers found for selected city.")
    else:
        st.dataframe(receivers_df, use_container_width=True, height=280)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — MANAGE LISTINGS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚙️  Manage Listings":

    st.markdown('<div class="page-title">⚙️ Manage Listings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Add new food listings, update existing ones, or remove outdated records</div>', unsafe_allow_html=True)

    op = st.radio(
        "Select Operation",
        ["📋 View All","➕ Add Listing","✏️ Update Listing","🗑️ Delete Listing"],
        horizontal=True
    )
    st.markdown("<hr class='green-divider'>", unsafe_allow_html=True)

    # VIEW
    if op == "📋 View All":
        st.markdown('<div class="section-header">📋 All Food Listings</div>', unsafe_allow_html=True)
        df = pd.read_sql("SELECT * FROM food_listings ORDER BY Food_ID DESC", conn)
        st.dataframe(df, use_container_width=True, height=500)
        c1,c2,c3 = st.columns(3)
        c1.metric("Total Listings",    len(df))
        c2.metric("Total Quantity",    f"{df['Quantity'].sum():,}")
        c3.metric("Unique Food Items", df['Food_Name'].nunique())

    # ADD
    elif op == "➕ Add Listing":
        st.markdown('<div class="section-header">➕ Add New Food Listing</div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            food_name   = st.text_input("🍲 Food Name",       placeholder="e.g. Rice, Bread, Soup")
            quantity    = st.number_input("📦 Quantity",       min_value=1, value=10)
            expiry_date = st.date_input("📅 Expiry Date")
            provider_id = st.number_input("🔑 Provider ID",   min_value=1, value=1)
        with c2:
            provider_type = st.selectbox("🏪 Provider Type",  ["Restaurant","Supermarket","Grocery Store","Catering Service"])
            location      = st.text_input("📍 City/Location", placeholder="e.g. New Carol")
            food_type     = st.selectbox("🥗 Food Type",      ["Vegetarian","Vegan","Non-Vegetarian"])
            meal_type     = st.selectbox("🍽️ Meal Type",      ["Breakfast","Lunch","Dinner","Snacks"])

        if st.button("➕ Add Food Listing", type="primary", use_container_width=True):
            if food_name.strip() and location.strip():
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO food_listings
                        (Food_Name, Quantity, Expiry_Date, Provider_ID,
                         Provider_Type, Location, Food_Type, Meal_Type)
                        VALUES (?,?,?,?,?,?,?,?)
                    """, (food_name, quantity, str(expiry_date),
                          provider_id, provider_type, location, food_type, meal_type))
                    conn.commit()
                    st.success(f"✅ '{food_name}' added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("⚠️ Food Name and Location are required!")

    # UPDATE
    elif op == "✏️ Update Listing":
        st.markdown('<div class="section-header">✏️ Update Food Listing</div>', unsafe_allow_html=True)
        food_id  = st.number_input("Enter Food ID to Update", min_value=1, value=1)
        existing = pd.read_sql(f"SELECT * FROM food_listings WHERE Food_ID = {food_id}", conn)

        if not existing.empty:
            st.markdown("**Current record:**")
            st.dataframe(existing, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            c1,c2 = st.columns(2)
            with c1:
                new_qty  = st.number_input("New Quantity", min_value=1,
                           value=int(existing['Quantity'].iloc[0]))
                new_food = st.selectbox("New Food Type",
                           ["Vegetarian","Vegan","Non-Vegetarian"],
                           index=["Vegetarian","Vegan","Non-Vegetarian"].index(
                               existing['Food_Type'].iloc[0]))
            with c2:
                new_meal = st.selectbox("New Meal Type",
                           ["Breakfast","Lunch","Dinner","Snacks"],
                           index=["Breakfast","Lunch","Dinner","Snacks"].index(
                               existing['Meal_Type'].iloc[0]))
                new_loc  = st.text_input("New Location", value=existing['Location'].iloc[0])

            if st.button("✏️ Save Changes", type="primary", use_container_width=True):
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE food_listings
                        SET Quantity=?, Food_Type=?, Meal_Type=?, Location=?
                        WHERE Food_ID=?
                    """, (new_qty, new_food, new_meal, new_loc, food_id))
                    conn.commit()
                    st.success(f"✅ Food ID {food_id} updated successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning(f"⚠️ No listing found with Food ID {food_id}")

    # DELETE
    elif op == "🗑️ Delete Listing":
        st.markdown('<div class="section-header">🗑️ Delete Food Listing</div>', unsafe_allow_html=True)
        food_id  = st.number_input("Enter Food ID to Delete", min_value=1, value=1)
        existing = pd.read_sql(f"SELECT * FROM food_listings WHERE Food_ID = {food_id}", conn)

        if not existing.empty:
            st.markdown("**Record to be deleted:**")
            st.dataframe(existing, use_container_width=True)
            st.error("⚠️ This action is permanent and cannot be undone!")
            confirm = st.checkbox("I understand this action is permanent")
            if confirm:
                if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True):
                    try:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM food_listings WHERE Food_ID=?", (food_id,))
                        conn.commit()
                        st.success(f"✅ Food ID {food_id} deleted successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.warning(f"⚠️ No listing found with Food ID {food_id}")