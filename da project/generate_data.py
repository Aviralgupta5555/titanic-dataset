# -*- coding: utf-8 -*-
"""
generate_data.py
----------------
Loads the Titanic dataset (from local /data or GitHub fallback),
performs all EDA cleaning & feature engineering, and returns a
clean DataFrame ready for the dashboard.
"""

import os
import numpy as np
import pandas as pd

# ── Paths ──────────────────────────────────────────────────────────────
DATA_DIR      = os.path.join(os.path.dirname(__file__), "data")
LOCAL_CSV     = os.path.join(DATA_DIR, "titanic.csv")
GITHUB_URL    = (
    "https://raw.githubusercontent.com/"
    "datasciencedojo/datasets/master/titanic.csv"
)

# ── Colour palette (shared with dashboard) ─────────────────────────────
PALETTE = {
    "survived" : "#10B981", # Emerald Green
    "died"     : "#F43F5E", # Coral Red
    "accent1"  : "#2563EB", # Royal Blue
    "accent2"  : "#10B981", # Emerald Green
    "accent3"  : "#F59E0B", # Amber
    "accent4"  : "#6366F1", # Indigo
    "accent5"  : "#0EA5E9", # Ice Blue
    "bg"       : "#F8FAFC", # Slate-50
    "card"     : "#FFFFFF", # Pure White
    "border"   : "#E2E8F0", # Slate-200
    "text"     : "#0F172A", # Slate-900
    "subtext"  : "#64748B", # Slate-500
    "grid"     : "rgba(37,99,235,0.06)", # Faint blue grid
}

COLORS5 = [
    PALETTE["accent1"], PALETTE["accent2"],
    PALETTE["accent3"], PALETTE["accent4"],
    PALETTE["accent5"],
]

# ── Plotly layout base (re-used in dashboard.py) ───────────────────────
LAYOUT_BASE = dict(
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor  = "rgba(0,0,0,0)",
    font          = dict(family="Inter, Segoe UI, sans-serif",
                         color=PALETTE["text"], size=12),
    margin        = dict(l=20, r=20, t=45, b=20),
    legend        = dict(
        bgcolor     = "rgba(255,255,255,0.9)",
        bordercolor = PALETTE["border"],
        borderwidth = 1,
        font        = dict(size=11),
    ),
)


# ── Internal helpers ───────────────────────────────────────────────────
def _apply_axis_style(fig):
    """Apply consistent dark-mode axis styling."""
    fig.update_xaxes(
        gridcolor    = PALETTE["grid"],
        zerolinecolor= PALETTE["border"],
        tickfont     = dict(color=PALETTE["subtext"]),
    )
    fig.update_yaxes(
        gridcolor    = PALETTE["grid"],
        zerolinecolor= PALETTE["border"],
        tickfont     = dict(color=PALETTE["subtext"]),
    )
    return fig


def apply_style(fig):
    """Public wrapper – apply base layout + axis style to any figure."""
    fig.update_layout(**LAYOUT_BASE)
    return _apply_axis_style(fig)


def hex_to_rgba(hex_str: str, opacity: float) -> str:
    """Convert hex string (e.g. #6C63FF) to rgba string."""
    h = hex_str.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r}, {g}, {b}, {opacity})"



# ── Data loading ───────────────────────────────────────────────────────
def _load_raw() -> pd.DataFrame:
    """Load raw CSV – local first, GitHub fallback, then synthetic."""
    if os.path.exists(LOCAL_CSV):
        return pd.read_csv(LOCAL_CSV)

    try:
        df = pd.read_csv(GITHUB_URL)
        # Cache locally for future runs
        os.makedirs(DATA_DIR, exist_ok=True)
        df.to_csv(LOCAL_CSV, index=False)
        return df
    except Exception:
        pass

    # Synthetic fallback
    np.random.seed(42)
    n = 891
    ages  = np.random.normal(29, 14, n)
    ages  = np.clip(ages, 0.5, 80).astype(float)
    ages[np.random.rand(n) < 0.20] = np.nan

    cabin = np.array([None] * n, dtype=object)
    cabin[np.random.rand(n) >= 0.77] = "C85"

    return pd.DataFrame({
        "PassengerId": range(1, n + 1),
        "Survived"   : np.random.choice([0, 1], n, p=[0.62, 0.38]),
        "Pclass"     : np.random.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55]),
        "Name"       : [f"Doe, Mr. Person {i}" for i in range(n)],
        "Sex"        : np.random.choice(["male", "female"], n, p=[0.65, 0.35]),
        "Age"        : ages,
        "SibSp"      : np.random.choice([0,1,2,3,4], n, p=[0.68,0.23,0.06,0.02,0.01]),
        "Parch"      : np.random.choice([0,1,2,3,4], n, p=[0.76,0.13,0.09,0.01,0.01]),
        "Ticket"     : [f"TKT{i}" for i in range(n)],
        "Fare"       : np.abs(np.random.exponential(32, n)),
        "Cabin"      : cabin,
        "Embarked"   : np.random.choice(["S","C","Q"], n, p=[0.72,0.19,0.09]),
    })


# ── EDA & Feature Engineering ─────────────────────────────────────────
def load_and_clean() -> pd.DataFrame:
    """
    Full EDA pipeline:
      1. Load raw data
      2. Impute missing values
      3. Engineer new features
      4. Add display-friendly label columns
    Returns a clean DataFrame.
    """
    df = _load_raw()

    # ── Missing value imputation
    df["Age"]      = df["Age"].fillna(df["Age"].median())
    df["Fare"]     = df["Fare"].fillna(df["Fare"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

    # ── Derived features
    df["HasCabin"]   = df["Cabin"].notna().astype(int)
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"]    = (df["FamilySize"] == 1).astype(int)

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins   = [0, 12, 17, 35, 60, 100],
        labels = ["Child", "Teen", "Adult", "Middle-Age", "Senior"],
    )
    df["FareGroup"] = pd.cut(
        df["Fare"],
        bins   = [0, 10, 30, 100, 600],
        labels = ["Low", "Medium", "High", "Premium"],
    )

    # ── Title extraction
    df["Title"] = df["Name"].str.extract(r",\s*([^.]+)\.")
    rare_titles = df["Title"].value_counts()
    rare_titles = rare_titles[rare_titles < 10].index
    df["Title"] = df["Title"].replace({t: "Rare" for t in rare_titles})

    # ── Label columns for charts
    df["SurvivedLabel"] = df["Survived"].map({0: "Died", 1: "Survived"})
    df["PclassLabel"]   = df["Pclass"].map(
        {1: "1st Class", 2: "2nd Class", 3: "3rd Class"}
    )
    df["EmbarkedLabel"] = df["Embarked"].map(
        {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}
    )
    df["SexLabel"] = df["Sex"].str.title()

    return df


# ── Summary statistics (used in sidebar / tooltips) ───────────────────
def get_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    surv  = int(df["Survived"].sum())
    return {
        "total"      : total,
        "survived"   : surv,
        "died"       : total - surv,
        "surv_rate"  : surv / total * 100,
        "avg_age"    : df["Age"].mean(),
        "avg_fare"   : df["Fare"].mean(),
        "female_surv": df[df["Sex"]=="female"]["Survived"].mean() * 100,
        "male_surv"  : df[df["Sex"]=="male"]["Survived"].mean()   * 100,
        "class1_surv": df[df["Pclass"]==1]["Survived"].mean()     * 100,
        "class2_surv": df[df["Pclass"]==2]["Survived"].mean()     * 100,
        "class3_surv": df[df["Pclass"]==3]["Survived"].mean()     * 100,
        "alone_surv" : df[df["IsAlone"]==1]["Survived"].mean()    * 100,
        "family_surv": df[df["IsAlone"]==0]["Survived"].mean()    * 100,
    }


if __name__ == "__main__":
    df  = load_and_clean()
    kpi = get_kpis(df)
    print("=== Titanic EDA Summary ===")
    print(f"  Total passengers : {kpi['total']}")
    print(f"  Survived         : {kpi['survived']}  ({kpi['surv_rate']:.1f}%)")
    print(f"  Died             : {kpi['died']}")
    print(f"  Avg age          : {kpi['avg_age']:.1f} yrs")
    print(f"  Avg fare         : GBP {kpi['avg_fare']:.2f}")
    print(f"  Female surv rate : {kpi['female_surv']:.1f}%")
    print(f"  Male surv rate   : {kpi['male_surv']:.1f}%")
    print(f"  1st class surv   : {kpi['class1_surv']:.1f}%")
    print(df.head())
    print(df.dtypes)
