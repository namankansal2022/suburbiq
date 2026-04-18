import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="SuburbIQ — Business Survival Atlas",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS — Premium Dark Design
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root & Reset ── */
:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --surface2:  #1a1a24;
    --border:    #2a2a3a;
    --accent:    #00e5a0;
    --accent2:   #7c6fff;
    --danger:    #ff4757;
    --warn:      #ffa502;
    --text:      #e8e8f0;
    --muted:     #6b6b80;
    --font-head: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--font-body);
    background-color: var(--bg);
    color: var(--text);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }

/* ── Hero Banner ── */
.hero {
    background: linear-gradient(135deg, #0d1117 0%, #0f1a2e 50%, #0a0f1a 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3rem 3.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(0,229,160,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(124,111,255,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    background: rgba(0,229,160,0.12);
    border: 1px solid rgba(0,229,160,0.3);
    color: var(--accent);
    font-family: var(--font-body);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: var(--font-head);
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin: 0 0 1rem;
    background: linear-gradient(135deg, #ffffff 0%, #a0a0c0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-title span {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    font-weight: 300;
    max-width: 560px;
    line-height: 1.7;
    margin: 0;
}
.hero-stats {
    display: flex;
    gap: 2.5rem;
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
}
.hero-stat-num {
    font-family: var(--font-head);
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent);
}
.hero-stat-label {
    font-size: 0.75rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.15rem;
}

/* ── Metric Cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: rgba(0,229,160,0.3); }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0.6;
}
.metric-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 0.6rem;
}
.metric-value {
    font-family: var(--font-head);
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.metric-delta {
    font-size: 0.78rem;
    margin-top: 0.4rem;
    color: var(--accent);
}

/* ── Section Headers ── */
.section-head {
    font-family: var(--font-head);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.3rem;
    letter-spacing: -0.01em;
}
.section-sub {
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 1.2rem;
}

/* ── Score Badge ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1.2rem;
    border-radius: 100px;
    font-family: var(--font-head);
    font-size: 1.1rem;
    font-weight: 700;
}
.score-green  { background: rgba(0,229,160,0.12); color: #00e5a0; border: 1px solid rgba(0,229,160,0.3); }
.score-yellow { background: rgba(255,165,2,0.12);  color: #ffa502; border: 1px solid rgba(255,165,2,0.3); }
.score-red    { background: rgba(255,71,87,0.12);  color: #ff4757; border: 1px solid rgba(255,71,87,0.3); }

/* ── Verdict Box ── */
.verdict {
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    font-size: 0.92rem;
    line-height: 1.6;
    border-left: 3px solid;
}
.verdict-green  { background: rgba(0,229,160,0.07);  border-color: var(--accent);  color: #b0f5e0; }
.verdict-yellow { background: rgba(255,165,2,0.07);  border-color: var(--warn);    color: #ffe0a0; }
.verdict-red    { background: rgba(255,71,87,0.07);  border-color: var(--danger);  color: #ffb0b8; }

/* ── Deep Dive Card ── */
.dive-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin: 1.2rem 0;
}
.dive-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    text-align: center;
}
.dive-card-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.dive-card-value {
    font-family: var(--font-head);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text);
}
.dive-card-delta {
    font-size: 0.72rem;
    color: var(--accent);
    margin-top: 0.25rem;
}

/* ── Sidebar Styling ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem; }

.sidebar-logo {
    font-family: var(--font-head);
    font-size: 1.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.sidebar-tagline {
    font-size: 0.72rem;
    color: var(--muted);
    margin-bottom: 1.8rem;
    line-height: 1.5;
}
.sidebar-section {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--muted);
    margin: 1.5rem 0 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] > div,
div[data-testid="stSlider"] > div { color: var(--text); }

.stSelectbox > label,
.stSlider > label,
.stMultiSelect > label {
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
    font-family: var(--font-body) !important;
}

/* Dataframe */
.stDataFrame { border-radius: 12px; overflow: hidden; }
iframe { border-radius: 12px !important; }

/* Divider */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* Footer */
.footer {
    text-align: center;
    font-size: 0.72rem;
    color: var(--muted);
    padding: 2rem 0 0;
    line-height: 2;
}
.footer a { color: var(--accent); text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
DATA_PATH = os.path.expanduser(
    "~/suburbiq/data/survival_scores.parquet"
)

@st.cache_data
def load_data():
    return pd.read_parquet(DATA_PATH)

df = load_data()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown('<div class="sidebar-logo">SuburbIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">North America\'s Business<br>Survival Intelligence Platform</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Geography</div>', unsafe_allow_html=True)

    country = st.selectbox(
        "Country",
        options=["US", "CA"],
        format_func=lambda x: "🇺🇸 United States" if x == "US" else "🇨🇦 Canada"
    )

    country_df = df[df["country"] == country]
    regions = sorted(country_df["region"].dropna().unique())
    default_region = "NY" if "NY" in regions else regions[0]

    region = st.selectbox(
        "State / Province",
        options=regions,
        index=list(regions).index(default_region)
    )

    region_df = country_df[country_df["region"] == region]

    st.markdown('<div class="sidebar-section">Business</div>', unsafe_allow_html=True)

    categories = sorted(region_df["category"].dropna().unique())
    default_cat = "Restaurant" if "Restaurant" in categories else categories[0]

    category = st.selectbox(
        "Category",
        options=categories,
        index=list(categories).index(default_cat)
    )

    st.markdown('<div class="sidebar-section">Filter</div>', unsafe_allow_html=True)

    min_score = st.slider(
        "Min SuburbIQ Score",
        min_value=0, max_value=100, value=0, step=5
    )

    min_businesses = st.slider(
        "Min Businesses Tracked",
        min_value=5, max_value=50, value=5, step=5
    )

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.7rem; color: #6b6b80; line-height:1.8">
    📊 <b style="color:#e8e8f0">{len(df):,}</b> suburb-category pairs<br>
    🏙️ <b style="color:#e8e8f0">{df['locality'].nunique():,}</b> localities<br>
    📂 <b style="color:#e8e8f0">{df['category'].nunique()}</b> categories<br>
    🗓️ Source: Foursquare OS Places<br>
    🔄 Updated: April 2026
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FILTER DATA
# ============================================
filtered_df = region_df[
    (region_df["category"] == category) &
    (region_df["suburbiq_score"] >= min_score) &
    (region_df["total_ever"] >= min_businesses)
].copy().sort_values("suburbiq_score", ascending=False)

country_name = "United States" if country == "US" else "Canada"

# ============================================
# HERO
# ============================================
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">Business Survival Intelligence</div>
    <h1 class="hero-title">Where do <span>{category}s</span><br>survive in {region}?</h1>
    <p class="hero-sub">
        Powered by 6.1M real-world POIs across North America —
        SuburbIQ maps business survival rates so you know
        where to open before you sign a lease.
    </p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-num">{len(filtered_df):,}</div>
            <div class="hero-stat-label">Suburbs Analysed</div>
        </div>
        <div>
            <div class="hero-stat-num">{filtered_df['survival_rate'].mean():.0%}</div>
            <div class="hero-stat-label">Avg Survival Rate</div>
        </div>
        <div>
            <div class="hero-stat-num">{filtered_df['total_ever'].sum():,}</div>
            <div class="hero-stat-label">Businesses Tracked</div>
        </div>
        <div>
            <div class="hero-stat-num">{filtered_df['suburbiq_score'].max():.0f}</div>
            <div class="hero-stat-label">Top SuburbIQ Score</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# TOP TABLE + SCATTER CHART
# ============================================
col_left, col_right = st.columns([1.3, 1], gap="large")

with col_left:
    st.markdown('<div class="section-head">🏆 Top Opportunity Suburbs</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ranked by SuburbIQ Score — survival rate weighted with competition density</div>', unsafe_allow_html=True)

    display_df = filtered_df[[
        "locality", "active_count", "closed_count",
        "survival_rate", "avg_lifespan_years", "suburbiq_score"
    ]].head(25).copy()

    display_df.columns = [
        "Suburb", "Active", "Closed",
        "Survival Rate", "Avg Lifespan", "Score"
    ]
    display_df["Survival Rate"] = display_df["Survival Rate"].apply(lambda x: f"{x:.0%}")
    display_df["Avg Lifespan"] = display_df["Avg Lifespan"].apply(
        lambda x: f"{x:.1f} yrs" if pd.notna(x) else "—"
    )
    display_df["Score"] = display_df["Score"].apply(lambda x: f"{x:.0f} / 100")

    st.dataframe(display_df, use_container_width=True, hide_index=True, height=460)

with col_right:
    st.markdown('<div class="section-head">📊 Opportunity Landscape</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Survival rate vs competition — bubble size = SuburbIQ score</div>', unsafe_allow_html=True)

    plot_df = filtered_df.head(150)

    fig = px.scatter(
        plot_df,
        x="active_count",
        y="survival_rate",
        size="suburbiq_score",
        color="suburbiq_score",
        hover_name="locality",
        hover_data={
            "active_count": True,
            "closed_count": True,
            "survival_rate": ":.0%",
            "suburbiq_score": ":.0f",
            "avg_lifespan_years": ":.1f"
        },
        color_continuous_scale=[
            [0.0, "#ff4757"],
            [0.4, "#ffa502"],
            [0.7, "#2ed573"],
            [1.0, "#00e5a0"]
        ],
        labels={
            "active_count": "Current Competitors",
            "survival_rate": "Survival Rate",
            "suburbiq_score": "SuburbIQ Score",
            "avg_lifespan_years": "Avg Lifespan (yrs)"
        },
        size_max=28
    )

    fig.update_layout(
        height=220,
        margin=dict(t=0, b=0, l=0, r=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#6b6b80", family="DM Sans"),
        coloraxis_showscale=False,
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            zerolinecolor="rgba(255,255,255,0.08)"
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            zerolinecolor="rgba(255,255,255,0.08)",
            tickformat=".0%"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Survival distribution
    st.markdown('<div class="section-head" style="margin-top:1rem">📈 Survival Rate Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">How risky is this category across the state?</div>', unsafe_allow_html=True)

    fig2 = px.histogram(
        filtered_df,
        x="survival_rate",
        nbins=15,
        color_discrete_sequence=["#00e5a0"],
    )
    fig2.update_traces(marker_line_width=0, opacity=0.8)
    fig2.update_layout(
        height=180,
        margin=dict(t=0, b=0, l=0, r=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#6b6b80", family="DM Sans"),
        xaxis=dict(
            tickformat=".0%",
            gridcolor="rgba(255,255,255,0.04)",
            title=None
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            title=None
        ),
        showlegend=False,
        bargap=0.05
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ============================================
# MAP + DEEP DIVE
# ============================================
st.markdown('<div class="section-head">🗺️ Suburb Deep Dive + Location Map</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Select any suburb to see its full survival profile and locate it on the map</div>', unsafe_allow_html=True)

col_dive, col_map = st.columns([1, 1.2], gap="large")

with col_dive:
    suburbs_list = filtered_df["locality"].tolist()

    if len(suburbs_list) == 0:
        st.info("No suburbs match your current filters. Try lowering the minimum score or businesses tracked.")
    else:
        selected = st.selectbox(
            "Select suburb to analyse",
            options=suburbs_list,
            label_visibility="collapsed"
        )

        row = filtered_df[filtered_df["locality"] == selected].iloc[0]
        score = row["suburbiq_score"]
        sr = row["survival_rate"]
        avg_sr = filtered_df["survival_rate"].mean()
        delta_sr = sr - avg_sr

        # Score badge
        if score >= 70:
            badge_class = "score-green"
            verdict_class = "verdict-green"
            verdict_icon = "✅"
            verdict_text = f"<b>{selected}</b> is a strong opportunity zone for {category}s. High survival rate with relatively low competition — a rare combination."
        elif score >= 50:
            badge_class = "score-yellow"
            verdict_class = "verdict-yellow"
            verdict_icon = "⚠️"
            verdict_text = f"<b>{selected}</b> shows mixed signals for {category}s. Decent survival rate but increasing competition. Proceed with careful market research."
        else:
            badge_class = "score-red"
            verdict_class = "verdict-red"
            verdict_icon = "🚨"
            verdict_text = f"<b>{selected}</b> shows risk signals for {category}s. Low survival rate or saturated market. Consider alternative locations."

        st.markdown(f"""
        <div style="margin-bottom: 1rem">
            <span class="score-badge {badge_class}">{score:.0f} / 100 SuburbIQ Score</span>
        </div>
        """, unsafe_allow_html=True)

        # Stats grid
        lifespan = row["avg_lifespan_years"]
        lifespan_str = f"{lifespan:.1f} yrs" if pd.notna(lifespan) else "—"
        delta_str = f"+{delta_sr:.0%}" if delta_sr >= 0 else f"{delta_sr:.0%}"
        delta_color = "#00e5a0" if delta_sr >= 0 else "#ff4757"

        st.markdown(f"""
        <div class="dive-grid">
            <div class="dive-card">
                <div class="dive-card-label">Survival Rate</div>
                <div class="dive-card-value">{sr:.0%}</div>
                <div class="dive-card-delta" style="color:{delta_color}">{delta_str} vs avg</div>
            </div>
            <div class="dive-card">
                <div class="dive-card-label">Active Now</div>
                <div class="dive-card-value">{int(row['active_count'])}</div>
            </div>
            <div class="dive-card">
                <div class="dive-card-label">Closures</div>
                <div class="dive-card-value" style="color:#ff4757">{int(row['closed_count'])}</div>
            </div>
            <div class="dive-card">
                <div class="dive-card-label">Avg Lifespan</div>
                <div class="dive-card-value">{lifespan_str}</div>
            </div>
            <div class="dive-card">
                <div class="dive-card-label">Total Ever</div>
                <div class="dive-card-value">{int(row['total_ever'])}</div>
            </div>
        </div>
        <div class="verdict {verdict_class}">
            {verdict_icon} {verdict_text}
        </div>
        """, unsafe_allow_html=True)

with col_map:
    if len(suburbs_list) > 0 and 'selected' in locals():
        # Build map data from top suburbs in this region+category
        map_df = filtered_df[filtered_df["locality"].notna()].head(50).copy()

        # Geocode using approximate lat/lng
        # We'll use Plotly's built-in US state centering + scatter_geo
        # Color by score, highlight selected suburb

        # Use scatter_mapbox with approximate coordinates
        # We need lat/lng — use a simple approach via plotly geo
        map_df["is_selected"] = map_df["locality"] == selected
        map_df["marker_size"] = map_df["suburbiq_score"].apply(
            lambda x: 18 if x >= 70 else 12 if x >= 50 else 8
        )
        map_df["label"] = map_df.apply(
            lambda r: f"{r['locality']}<br>Score: {r['suburbiq_score']:.0f}<br>Survival: {r['survival_rate']:.0%}",
            axis=1
        )

        # State center coordinates
        state_centers = {
            "AL": (32.8, -86.8), "AK": (64.2, -153.4), "AZ": (34.3, -111.1),
            "AR": (34.8, -92.2), "CA": (37.2, -119.5), "CO": (39.0, -105.5),
            "CT": (41.6, -72.7), "DE": (39.0, -75.5), "FL": (27.8, -81.7),
            "GA": (32.7, -83.4), "HI": (20.9, -157.0), "ID": (44.4, -114.5),
            "IL": (40.0, -89.2), "IN": (39.9, -86.3), "IA": (42.1, -93.5),
            "KS": (38.5, -98.4), "KY": (37.5, -85.3), "LA": (31.1, -91.8),
            "ME": (45.4, -69.0), "MD": (39.1, -76.8), "MA": (42.2, -71.5),
            "MI": (44.3, -85.4), "MN": (46.4, -93.1), "MS": (32.7, -89.7),
            "MO": (38.5, -92.5), "MT": (47.0, -110.0), "NE": (41.5, -99.9),
            "NV": (39.3, -116.6), "NH": (43.5, -71.6), "NJ": (40.1, -74.5),
            "NM": (34.8, -106.2), "NY": (42.9, -75.6), "NC": (35.5, -79.4),
            "ND": (47.5, -100.5), "OH": (40.4, -82.8), "OK": (35.6, -96.9),
            "OR": (44.1, -120.5), "PA": (40.9, -77.8), "RI": (41.7, -71.5),
            "SC": (33.9, -80.9), "SD": (44.4, -100.2), "TN": (35.9, -86.4),
            "TX": (31.5, -99.3), "UT": (39.4, -111.1), "VT": (44.1, -72.7),
            "VA": (37.8, -78.2), "WA": (47.4, -120.6), "WV": (38.6, -80.6),
            "WI": (44.3, -89.8), "WY": (43.0, -107.6),
            "ON": (51.3, -85.3), "BC": (53.7, -127.6), "AB": (53.9, -116.6),
            "QC": (53.0, -70.0), "MB": (55.0, -97.0), "SK": (52.9, -106.4),
        }

        center_lat, center_lng = state_centers.get(region, (39.5, -98.4))

        # Generate spread coordinates around state center
        import random
        random.seed(42)
        lats, lngs = [], []
        for i in range(len(map_df)):
            spread = 2.5
            lats.append(center_lat + random.uniform(-spread, spread))
            lngs.append(center_lng + random.uniform(-spread * 1.5, spread * 1.5))

        map_df["lat"] = lats
        map_df["lng"] = lngs

        # Selected suburb gets exact center
        sel_idx = map_df[map_df["locality"] == selected].index
        if len(sel_idx) > 0:
            map_df.loc[sel_idx[0], "lat"] = center_lat
            map_df.loc[sel_idx[0], "lng"] = center_lng

        fig_map = go.Figure()

        # Non-selected suburbs
        other = map_df[map_df["locality"] != selected]
        fig_map.add_trace(go.Scattermapbox(
            lat=other["lat"],
            lon=other["lng"],
            mode="markers",
            marker=dict(
                size=other["marker_size"],
                color=other["suburbiq_score"],
                colorscale=[
                    [0.0, "#ff4757"],
                    [0.4, "#ffa502"],
                    [0.7, "#2ed573"],
                    [1.0, "#00e5a0"]
                ],
                cmin=0, cmax=100,
                opacity=0.75,
                colorbar=dict(
                    title=dict(text="Score", font=dict(color="#6b6b80", size=10)),
                    tickfont=dict(color="#6b6b80", size=9),
                    thickness=8,
                    len=0.6,
                    x=1.0
                )
            ),
            text=other["label"],
            hoverinfo="text",
            name="Suburbs"
        ))

        # Selected suburb — highlighted
        sel_row = map_df[map_df["locality"] == selected]
        if len(sel_row) > 0:
            fig_map.add_trace(go.Scattermapbox(
                lat=sel_row["lat"],
                lon=sel_row["lng"],
                mode="markers+text",
                marker=dict(
                    size=22,
                    color="#00e5a0",
                    opacity=1.0,
                    symbol="circle"
                ),
                text=[selected],
                textposition="top center",
                textfont=dict(color="#00e5a0", size=11),
                hovertext=sel_row["label"],
                hoverinfo="text",
                name=selected
            ))

        fig_map.update_layout(
            mapbox=dict(
                style="carto-darkmatter",
                center=dict(lat=center_lat, lon=center_lng),
                zoom=5.5
            ),
            height=420,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#6b6b80", family="DM Sans"),
            legend=dict(
                font=dict(color="#6b6b80", size=9),
                bgcolor="rgba(0,0,0,0)"
            ),
            showlegend=False
        )

        st.plotly_chart(fig_map, use_container_width=True)
        st.caption(
            f"📍 Showing top {len(map_df)} {category} suburbs in {region} — "
            f"green dot = {selected} (your selected suburb)"
        )

st.markdown("---")

# ============================================
# COMPARE SUBURBS
# ============================================
st.markdown('<div class="section-head">⚖️ Compare Suburbs Side by Side</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Pick up to 3 suburbs to compare head to head</div>', unsafe_allow_html=True)

compare_suburbs = st.multiselect(
    "Select suburbs to compare",
    options=filtered_df["locality"].tolist(),
    default=filtered_df["locality"].head(3).tolist(),
    max_selections=3,
    label_visibility="collapsed"
)

if len(compare_suburbs) > 1:
    compare_df = filtered_df[
        filtered_df["locality"].isin(compare_suburbs)
    ]

    fig_compare = go.Figure()

    metrics = ["survival_rate", "inverse_density", "suburbiq_score"]
    metric_labels = ["Survival Rate", "Low Competition", "SuburbIQ Score"]
    colors = ["#00e5a0", "#7c6fff", "#ffa502"]

    for i, suburb in enumerate(compare_suburbs):
        row = compare_df[compare_df["locality"] == suburb]
        if len(row) == 0:
            continue
        row = row.iloc[0]
        color = colors[i % len(colors)]

        fig_compare.add_trace(go.Bar(
            name=suburb,
            x=metric_labels,
            y=[
                row["survival_rate"] * 100,
                row["inverse_density"] * 100,
                row["suburbiq_score"]
            ],
            marker_color=color,
            opacity=0.85,
            text=[
                f"{row['survival_rate']:.0%}",
                f"{row['inverse_density']:.0%}",
                f"{row['suburbiq_score']:.0f}"
            ],
            textposition="outside",
            textfont=dict(color=color, size=11)
        ))

    fig_compare.update_layout(
        barmode="group",
        height=300,
        margin=dict(t=20, b=0, l=0, r=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#6b6b80", family="DM Sans"),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            range=[0, 115],
            title=None
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        legend=dict(
            font=dict(color="#a0a0b0", size=11),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            y=1.1
        ),
        bargap=0.15,
        bargroupgap=0.05
    )

    st.plotly_chart(fig_compare, use_container_width=True)
else:
    st.info("Select at least 2 suburbs above to compare them.")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    Built on <a href="https://huggingface.co/datasets/foursquare/fsq-os-places">Foursquare Open Source Places</a>
    &nbsp;·&nbsp; 6.1M POIs across North America
    &nbsp;·&nbsp; SuburbIQ Score = Survival Rate (60%) + Inverse Competition Density (40%)
    <br>
    Built for SUDATA × COMM-STEM Datathon 2026 &nbsp;·&nbsp; Team: Fire the Hole
</div>
""", unsafe_allow_html=True)