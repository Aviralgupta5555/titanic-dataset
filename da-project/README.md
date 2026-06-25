# Titanic Power BI-Style EDA Dashboard

A fully interactive **Power BI-inspired EDA dashboard** built entirely in Python using Streamlit, Pandas, NumPy and Plotly.

![Dashboard Screenshot](data/preview.png)

---

## Project Structure

```
da project/
├── .streamlit/
│   └── config.toml        # Dark theme & server settings
├── data/
│   └── titanic.csv        # Auto-downloaded on first run
├── dashboard.py           # Streamlit app (main entry point)
├── generate_data.py       # Data loading, EDA & feature engineering
├── powerbi_guide.md       # Power BI export guide
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## Features

### EDA & Analytics
| Section | Charts |
|---|---|
| Survival Overview | Donut chart · Grouped bar (class) · Stacked bar (gender) |
| Demographics & Fares | Age histogram · Age vs Fare scatter (bubble) |
| Segmentation | Age group bar · Embarkation port · Family size survival rate |
| Distributions & Patterns | Fare box-plot · Survival heatmap (class × gender) |
| Advanced EDA | Title survival rate · Feature correlation matrix |
| Additional Insights | Fare group pie · Age violin plot |

### Interactive Filters (Sidebar)
- Passenger class  
- Gender  
- Age range slider  
- Fare range slider  
- Embarkation port  
- Family size multi-select  

### Extras
- 6 animated KPI cards  
- 3 Key Insight cards with statistics  
- Raw data table with **CSV download**  
- Fully responsive layout  

---

## Quickstart

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the dashboard
```bash
streamlit run dashboard.py
```

The app opens at **http://localhost:8501** automatically.  
The Titanic CSV is downloaded from GitHub and cached in `data/` on first run.

---

## Tech Stack

| Library | Purpose |
|---|---|
| **Pandas** | Data loading, cleaning & aggregation |
| **NumPy** | Numerical operations & feature engineering |
| **Plotly** | Interactive charts (bar, scatter, heatmap, violin …) |
| **Streamlit** | Web app framework & UI components |
| **Scikit-learn** | (available for ML extension) |

---

## Dataset

- **Source:** [Kaggle Titanic Competition](https://www.kaggle.com/c/titanic) / UCI ML Repository  
- **Records:** 891 passengers  
- **Features:** 12 original + 7 engineered (`AgeGroup`, `FareGroup`, `FamilySize`, `IsAlone`, `HasCabin`, `Title`, `SurvivedLabel`)

---

## Engineered Features

| Feature | Description |
|---|---|
| `FamilySize` | SibSp + Parch + 1 |
| `IsAlone` | 1 if FamilySize == 1 |
| `HasCabin` | 1 if Cabin is not null |
| `AgeGroup` | Binned: Child / Teen / Adult / Middle-Age / Senior |
| `FareGroup` | Binned: Low / Medium / High / Premium |
| `Title` | Extracted from Name (Mr, Mrs, Miss, Rare …) |

---

## Author

Built as a Power BI-style analytics project using Python open-source tools.
