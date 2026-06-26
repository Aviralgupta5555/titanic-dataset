<div align="center">

# 🚢 Titanic EDA Dashboard
### A Power BI–Style Interactive Analytics App Built in Python

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A fully interactive, Power BI–inspired exploratory data analysis dashboard for the Titanic dataset — built entirely in Python with **Streamlit**, **Pandas**, **NumPy**, and **Plotly**. No external BI tool required.

[Features](#-features) • [Quickstart](#-quickstart) • [Project Structure](#-project-structure) • [Tech Stack](#-tech-stack) • [Dataset](#-dataset)

![Dashboard Preview](data/preview.png)

</div>

---

## 📖 Overview

This project recreates the look, feel, and interactivity of a **Power BI report** using only open-source Python tooling. It combines KPI cards, cross-filtering, and a library of 12+ chart types into a single-page analytics dashboard — ideal for portfolio projects, data analysis practice, or as a template for building BI-style apps in Streamlit.

## ✨ Features

### 📊 EDA & Analytics

| Section | Charts Included |
|---|---|
| **Survival Overview** | Donut chart · Grouped bar by class · Stacked bar by gender |
| **Demographics & Fares** | Age distribution histogram · Age vs. Fare bubble scatter |
| **Segmentation** | Age group bar chart · Embarkation port breakdown · Family size survival rate |
| **Distributions & Patterns** | Fare box plot · Survival heatmap (class × gender) |
| **Advanced EDA** | Title-based survival rate · Feature correlation matrix |
| **Additional Insights** | Fare group pie chart · Age distribution violin plot |

### 🎛️ Interactive Sidebar Filters
- Passenger class
- Gender
- Age range (slider)
- Fare range (slider)
- Embarkation port
- Family size (multi-select)

### 🧩 Extras
- 6 animated KPI summary cards
- 3 auto-generated "Key Insight" cards with statistics
- Searchable raw data table with **CSV export**
- Fully responsive, dark-themed layout

---

## 🚀 Quickstart

### Prerequisites
- Python 3.9+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
streamlit run dashboard.py
```

The app will open automatically in your browser at `http://localhost:8501`.

> 💡 The Titanic dataset is auto-downloaded from GitHub on first run and cached locally in `data/`. No manual download required.

---

## 📁 Project Structure

```
da-project/
├── .streamlit/
│   └── config.toml        # Dark theme & server settings
├── data/
│   └── titanic.csv        # Auto-downloaded on first run
├── dashboard.py            # Streamlit app (main entry point)
├── generate_data.py        # Data loading, EDA & feature engineering
├── powerbi_guide.md        # Power BI export guide
├── requirements.txt        # Python dependencies
└── README.md                # This file
```

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| **Pandas** | Data loading, cleaning & aggregation |
| **NumPy** | Numerical operations & feature engineering |
| **Plotly** | Interactive charts (bar, scatter, heatmap, violin, etc.) |
| **Streamlit** | Web app framework & UI components |
| **Scikit-learn** | Reserved for future ML extension |

---

## 🗂️ Dataset

- **Source:** [Kaggle Titanic Competition](https://www.kaggle.com/c/titanic) / UCI Machine Learning Repository
- **Records:** 891 passengers
- **Features:** 12 original columns + 7 engineered features

### Engineered Features

| Feature | Description |
|---|---|
| `FamilySize` | `SibSp + Parch + 1` |
| `IsAlone` | `1` if `FamilySize == 1`, else `0` |
| `HasCabin` | `1` if `Cabin` is not null, else `0` |
| `AgeGroup` | Binned into Child / Teen / Adult / Middle-Age / Senior |
| `FareGroup` | Binned into Low / Medium / High / Premium |
| `Title` | Extracted from `Name` (Mr, Mrs, Miss, Rare, etc.) |
| `SurvivedLabel` | Human-readable label for the `Survived` flag |

---

## 🗺️ Roadmap

- [ ] Add a machine learning tab (survival prediction with Scikit-learn)
- [ ] Add PDF/PNG export for individual charts
- [ ] Deploy a live demo via Streamlit Community Cloud

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](../../issues) or open a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a pull request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

Built as a Power BI–style analytics project using open-source Python tools, inspired by the classic Titanic dataset used across the data science community.

<div align="center">

If you found this project useful, consider giving it a ⭐ on GitHub!

</div>
