# -*- coding: utf-8 -*-
"""
dashboard.py
------------
Streamlit Power BI-style Titanic EDA Dashboard.
Run with:  streamlit run dashboard.py
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from generate_data import (
    load_and_clean,
    get_kpis,
    apply_style,
    PALETTE,
    COLORS5,
    hex_to_rgba,
)

# ══════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title = "Titanic EDA Dashboard",
    page_icon  = "🚢",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

# ══════════════════════════════════════════════════════════════════════
# CUSTOM CSS  (Modern Light feel)
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; }

/* ── top banner ── */
.dash-header {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid #BFDBFE;
    border-radius: 14px;
    padding: 18px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.dash-header h1 {
    font-size: 1.6rem; font-weight: 800;
    background: linear-gradient(90deg, #2563EB, #10B981);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0;
}
.dash-header p { color: #475569; font-size: 0.82rem; margin: 4px 0 0; }

/* ── KPI cards ── */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px 18px;
    text-align: center;
    transition: transform .25s, box-shadow .25s;
    position: relative; overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    border-radius: 14px 14px 0 0;
}
.kpi-card.green::after  { background: linear-gradient(90deg,#10B981,#34D399); }
.kpi-card.red::after    { background: linear-gradient(90deg,#F43F5E,#FB7185); }
.kpi-card.purple::after { background: linear-gradient(90deg,#2563EB,#60A5FA); }
.kpi-card.amber::after  { background: linear-gradient(90deg,#F59E0B,#FBBF24); }
.kpi-card.blue::after   { background: linear-gradient(90deg,#0EA5E9,#38BDF8); }
.kpi-card.pink::after   { background: linear-gradient(90deg,#EC4899,#F472B6); }
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 10px 25px rgba(37,99,235,0.08); }

.kpi-icon  { font-size: 2rem; }
.kpi-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: .1em;
             color: #64748B; margin: 6px 0 4px; }
.kpi-value { font-size: 1.9rem; font-weight: 800; letter-spacing: -.03em; color: #0F172A; }
.kpi-sub   { font-size: 0.7rem; color: #64748B; margin-top: 4px; }

/* ── section header ── */
.section-head {
    display: flex; align-items: center; gap: 10px;
    margin: 18px 0 10px;
    font-size: 0.78rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .1em;
    color: #475569;
}
.section-head::before {
    content: '';
    display: inline-block; width: 4px; height: 20px; border-radius: 2px;
    background: linear-gradient(to bottom, #2563EB, #10B981);
}

/* ── insight cards ── */
.insight-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 18px;
}
.insight-card h4 { color: #0F172A; font-size: 0.92rem; margin: 0 0 6px; }
.insight-card p  { color: #475569; font-size: 0.78rem; line-height: 1.55; margin: 0; }

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: #F8FAFC !important;
    border-right: 1px solid #E2E8F0;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Loading Titanic data…")
def get_data():
    return load_and_clean()

raw_df = get_data()

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR – FILTERS
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🚢 Titanic Dashboard")
    st.markdown("---")

    st.markdown("### Filters")

    pclass_options = ["All", "1st Class", "2nd Class", "3rd Class"]
    sel_class = st.selectbox("Passenger Class", pclass_options)

    sel_gender = st.selectbox("Gender", ["All", "Male", "Female"])

    age_min, age_max = int(raw_df["Age"].min()), int(raw_df["Age"].max())
    sel_age = st.slider("Age Range", age_min, age_max, (age_min, age_max))

    fare_min, fare_max = float(raw_df["Fare"].min()), float(raw_df["Fare"].max())
    sel_fare = st.slider(
        "Fare Range (GBP)",
        fare_min, fare_max,
        (fare_min, min(fare_max, 300.0)),
        step=0.5,
    )

    emb_options = ["All", "Southampton", "Cherbourg", "Queenstown"]
    sel_emb = st.selectbox("Embarkation Port", emb_options)

    family_opt = st.multiselect(
        "Family Size",
        options=sorted(raw_df["FamilySize"].unique()),
        default=sorted(raw_df["FamilySize"].unique()),
    )
    if not family_opt:
        family_opt = sorted(raw_df["FamilySize"].unique())

    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
**Dataset:** Titanic (Kaggle/UCI)  
**Records:** 891 passengers  
**Features:** 12 original + engineered  
**Tool:** Python · Pandas · Plotly · Streamlit
""")

# ── Apply filters ──────────────────────────────────────────────────────
df = raw_df.copy()
if sel_class != "All":
    df = df[df["PclassLabel"] == sel_class]
if sel_gender != "All":
    df = df[df["SexLabel"] == sel_gender]
df = df[(df["Age"] >= sel_age[0]) & (df["Age"] <= sel_age[1])]
df = df[(df["Fare"] >= sel_fare[0]) & (df["Fare"] <= sel_fare[1])]
if sel_emb != "All":
    df = df[df["EmbarkedLabel"] == sel_emb]
df = df[df["FamilySize"].isin(family_opt)]

kpi = get_kpis(df)

# ══════════════════════════════════════════════════════════════════════
# HEADER BANNER
# ══════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="dash-header">
  <div style="font-size:2.4rem">🚢</div>
  <div>
    <h1>Titanic EDA — Power BI Dashboard</h1>
    <p>Exploratory Data Analysis &nbsp;|&nbsp; {kpi['total']} passengers in current filter
    &nbsp;|&nbsp; Python · Pandas · NumPy · Plotly · Streamlit</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════
def kpi_card(icon, label, value, sub, color_cls):
    return f"""
    <div class="kpi-card {color_cls}">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>"""

cols = st.columns(6)
cards = [
    ("👥", "Total Passengers", f"{kpi['total']:,}",       "in current filter", "purple"),
    ("✅", "Survived",          f"{kpi['survived']:,}",    f"{kpi['surv_rate']:.1f}% rate", "green"),
    ("💀", "Did Not Survive",   f"{kpi['died']:,}",        f"{100-kpi['surv_rate']:.1f}% rate", "red"),
    ("🎂", "Avg Age",           f"{kpi['avg_age']:.1f}",   "years old", "blue"),
    ("💷", "Avg Fare",          f"£{kpi['avg_fare']:.1f}", "per ticket", "amber"),
    ("🏆", "1st Class Surv.",   f"{kpi['class1_surv']:.1f}%", "highest class", "pink"),
]
for col, (icon, label, value, sub, cls) in zip(cols, cards):
    col.markdown(kpi_card(icon, label, value, sub, cls), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# ROW 1 — Survival overview
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-head">📊 Survival Overview</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

# Donut chart
with c1:
    fig = go.Figure(go.Pie(
        labels=["Survived", "Died"],
        values=[kpi["survived"], kpi["died"]],
        hole=0.65,
        marker=dict(
            colors=[PALETTE["survived"], PALETTE["died"]],
            line=dict(color=PALETTE["bg"], width=3),
        ),
        textinfo="percent",
        textfont=dict(size=13),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
    ))
    fig.update_layout(
        **{**{}, **{"paper_bgcolor":"rgba(0,0,0,0)","plot_bgcolor":"rgba(0,0,0,0)",
                    "font":{"family":"Inter","color":PALETTE["text"],"size":12},
                    "margin":{"l":20,"r":20,"t":45,"b":20},
                    "legend":{"bgcolor":"rgba(19,19,42,0.8)","bordercolor":PALETTE["border"],
                              "borderwidth":1,"font":{"size":11}}}},
        title_text="Overall Survival Rate", title_font_size=14,
        annotations=[dict(
            text=f"<b>{kpi['surv_rate']:.1f}%</b><br>Survival",
            x=0.5, y=0.5, font_size=16, showarrow=False, font_color=PALETTE["text"],
        )],
    )
    st.plotly_chart(fig, use_container_width=True)

# Survival by class
with c2:
    cls_d = df.groupby(["PclassLabel","SurvivedLabel"]).size().reset_index(name="Count")
    fig = px.bar(
        cls_d, x="PclassLabel", y="Count", color="SurvivedLabel", barmode="group",
        color_discrete_map={"Survived": PALETTE["survived"], "Died": PALETTE["died"]},
        labels={"PclassLabel":"Passenger Class","Count":"Passengers"},
        title="Survival by Passenger Class",
    )
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# Survival by gender
with c3:
    sex_d = df.groupby(["SexLabel","SurvivedLabel"]).size().reset_index(name="Count")
    fig = px.bar(
        sex_d, x="SexLabel", y="Count", color="SurvivedLabel", barmode="stack",
        color_discrete_map={"Survived": PALETTE["survived"], "Died": PALETTE["died"]},
        labels={"SexLabel":"Gender","Count":"Passengers"},
        title="Survival by Gender",
    )
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# ROW 2 — Demographics & Fares
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-head">🎯 Demographics & Fares</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure()
    for label, colour in [("Survived", PALETTE["survived"]), ("Died", PALETTE["died"])]:
        sub = df[df["SurvivedLabel"] == label]["Age"]
        fig.add_trace(go.Histogram(
            x=sub, name=label, nbinsx=30,
            marker_color=colour, opacity=0.75,
            hovertemplate=f"<b>{label}</b><br>Age: %{{x}}<br>Count: %{{y}}<extra></extra>",
        ))
    fig.update_layout(
        barmode="overlay", title_text="Age Distribution by Survival", title_font_size=14,
        xaxis_title="Age", yaxis_title="Passengers",
    )
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.scatter(
        df, x="Age", y="Fare", color="SurvivedLabel", size="FamilySize",
        symbol="PclassLabel",
        color_discrete_map={"Survived": PALETTE["survived"], "Died": PALETTE["died"]},
        opacity=0.7,
        labels={"Age":"Age","Fare":"Fare (GBP)"},
        hover_data=["SexLabel","PclassLabel","EmbarkedLabel"],
        title="Age vs Fare  (bubble size = Family Size)",
    )
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# ROW 3 — Segmentation
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-head">🧭 Segmentation Analysis</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    ag = df.groupby(["AgeGroup","SurvivedLabel"], observed=False).size().reset_index(name="Count")
    fig = px.bar(
        ag, x="AgeGroup", y="Count", color="SurvivedLabel", barmode="group",
        color_discrete_map={"Survived": PALETTE["survived"], "Died": PALETTE["died"]},
        category_orders={"AgeGroup":["Child","Teen","Adult","Middle-Age","Senior"]},
        labels={"AgeGroup":"Age Group","Count":"Passengers"},
        title="Survival by Age Group",
    )
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    emb_d = df.groupby(["EmbarkedLabel","SurvivedLabel"]).size().reset_index(name="Count")
    fig = px.bar(
        emb_d, x="EmbarkedLabel", y="Count", color="SurvivedLabel", barmode="stack",
        color_discrete_map={"Survived": PALETTE["survived"], "Died": PALETTE["died"]},
        labels={"EmbarkedLabel":"Port","Count":"Passengers"},
        title="Survival by Embarkation Port",
    )
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

with c3:
    fam = (df.groupby("FamilySize")["Survived"].mean() * 100).reset_index()
    fam.columns = ["FamilySize","SurvivalRate"]
    fig = go.Figure(go.Bar(
        x=fam["FamilySize"], y=fam["SurvivalRate"],
        marker=dict(
            color=fam["SurvivalRate"],
            colorscale=[[0, PALETTE["died"]],[0.5, PALETTE["accent3"]],[1, PALETTE["survived"]]],
            showscale=True,
            colorbar=dict(title="Surv%", tickfont=dict(color=PALETTE["subtext"])),
        ),
        hovertemplate="Family Size: %{x}<br>Survival Rate: %{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title_text="Survival Rate by Family Size", title_font_size=14,
        xaxis_title="Family Size", yaxis_title="Survival Rate (%)",
    )
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# ROW 4 — Distributions & Patterns
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-head">📦 Distributions & Patterns</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure()
    cls_colors = {1: PALETTE["accent1"], 2: PALETTE["accent3"], 3: PALETTE["accent4"]}
    for cls in sorted(df["Pclass"].unique()):
        suffix = {1:"st",2:"nd",3:"rd"}.get(cls,"th")
        sub = df[df["Pclass"] == cls]["Fare"]
        clr = cls_colors[cls]
        fig.add_trace(go.Box(
            y=sub, name=f"{cls}{suffix} Class",
            marker_color=clr, line_color=clr, fillcolor=hex_to_rgba(clr, 0.27),
            boxmean=True,
        ))
    fig.update_layout(title_text="Fare Distribution by Class", title_font_size=14,
                      yaxis_title="Fare (GBP)")
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    hmap_df = df.groupby(["PclassLabel","SexLabel"])["Survived"].mean().unstack() * 100
    z  = hmap_df.values
    xt = hmap_df.columns.tolist()
    yt = hmap_df.index.tolist()
    fig = go.Figure(go.Heatmap(
        z=z, x=xt, y=yt,
        colorscale=[[0, PALETTE["died"]],[0.5,"#CBD5E1"],[1, PALETTE["survived"]]],
        text=np.round(z, 1).astype(str),
        texttemplate="%{text}%",
        hovertemplate="Class: %{y}<br>Gender: %{x}<br>Survival: %{z:.1f}%<extra></extra>",
    ))
    fig.update_layout(title_text="Survival Rate Heatmap  (Class x Gender)", title_font_size=14)
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# ROW 5 — Advanced EDA
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-head">🔬 Advanced EDA</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    t_surv = df.groupby("Title")["Survived"].mean().reset_index()
    t_surv["SurvivalRate"] = t_surv["Survived"] * 100
    t_surv = t_surv.sort_values("SurvivalRate", ascending=True)
    fig = go.Figure(go.Bar(
        x=t_surv["SurvivalRate"], y=t_surv["Title"], orientation="h",
        marker=dict(
            color=t_surv["SurvivalRate"],
            colorscale=[[0,PALETTE["died"]],[0.5,PALETTE["accent3"]],[1,PALETTE["survived"]]],
        ),
        text=[f"{v:.1f}%" for v in t_surv["SurvivalRate"]],
        textposition="outside",
        hovertemplate="Title: %{y}<br>Survival Rate: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(title_text="Survival Rate by Title", title_font_size=14,
                      xaxis_title="Survival Rate (%)", yaxis_title="")
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    num_cols = ["Survived","Pclass","Age","SibSp","Parch","Fare",
                "FamilySize","IsAlone","HasCabin"]
    corr = df[num_cols].corr().round(2)
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
        colorscale="RdBu", zmid=0,
        text=corr.values.round(2).astype(str),
        texttemplate="%{text}",
        hovertemplate="%{x} x %{y}: %{z}<extra></extra>",
    ))
    fig.update_layout(title_text="Feature Correlation Matrix", title_font_size=14,
                      xaxis=dict(tickangle=30))
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# ROW 6 — Fare group pie + Violin
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-head">🎻 Additional Insights</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    fg = df["FareGroup"].value_counts().reset_index()
    fg.columns = ["FareGroup","Count"]
    fig = px.pie(
        fg, names="FareGroup", values="Count",
        color_discrete_sequence=COLORS5,
        hole=0.5, title="Fare Group Distribution",
    )
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = go.Figure()
    for grp, col in [("Survived", PALETTE["survived"]), ("Died", PALETTE["died"])]:
        sub = df[df["SurvivedLabel"] == grp]
        fig.add_trace(go.Violin(
            x=sub["SurvivedLabel"], y=sub["Age"],
            name=grp, box_visible=True, meanline_visible=True,
            fillcolor=hex_to_rgba(col, 0.33), line_color=col, opacity=0.8,
        ))
    fig.update_layout(title_text="Age Distribution Violin (Survived vs Died)",
                      title_font_size=14, yaxis_title="Age", violinmode="group")
    apply_style(fig)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-head">💡 Key Insights</div>', unsafe_allow_html=True)

ic1, ic2, ic3 = st.columns(3)
insights = [
    ("👩", "Women & Children First",
     f"Female survival rate was <b style='color:{PALETTE['survived']}'>{kpi['female_surv']:.1f}%</b> "
     f"vs only <b style='color:{PALETTE['died']}'>{kpi['male_surv']:.1f}%</b> for males — "
     "a direct reflection of the evacuation protocol on the night of the sinking."),
    ("💎", "Class Privilege",
     f"1st Class passengers achieved <b style='color:{PALETTE['survived']}'>{kpi['class1_surv']:.1f}%</b> "
     f"survival vs 3rd Class at <b style='color:{PALETTE['died']}'>{kpi['class3_surv']:.1f}%</b> — "
     "proximity to lifeboats and social status played a critical role."),
    ("👨‍👩‍👧", "Family Size Sweet Spot",
     f"Solo travelers survived at <b style='color:{PALETTE['accent3']}'>{kpi['alone_surv']:.1f}%</b> "
     f"vs <b style='color:{PALETTE['survived']}'>{kpi['family_surv']:.1f}%</b> for those with family — "
     "small family groups benefited from mutual assistance during evacuation."),
]
for col, (icon, title, body) in zip([ic1, ic2, ic3], insights):
    col.markdown(
        f'<div class="insight-card"><h4>{icon} {title}</h4><p>{body}</p></div>',
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════
# RAW DATA TABLE
# ══════════════════════════════════════════════════════════════════════
with st.expander("📋 View Raw Filtered Data"):
    display_cols = [
        "PassengerId","Survived","PclassLabel","SexLabel","Age",
        "Fare","EmbarkedLabel","FamilySize","IsAlone","HasCabin",
        "AgeGroup","FareGroup","Title",
    ]
    st.dataframe(
        df[display_cols].rename(columns={
            "PclassLabel":"Class","SexLabel":"Gender",
            "EmbarkedLabel":"Port","IsAlone":"Solo","HasCabin":"Cabin",
        }).reset_index(drop=True),
        use_container_width=True,
        height=320,
    )
    st.download_button(
        "⬇️ Download filtered CSV",
        data=df[display_cols].to_csv(index=False),
        file_name="titanic_filtered.csv",
        mime="text/csv",
    )

# ══════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#64748B;font-size:0.75rem'>"
    "Built with <b style='color:#2563EB'>Python · Pandas · NumPy · Plotly · Streamlit</b> &nbsp;|&nbsp; "
    "Titanic Dataset (Kaggle / UCI) &nbsp;|&nbsp; Power BI-Style EDA Dashboard</p>",
    unsafe_allow_html=True,
)
