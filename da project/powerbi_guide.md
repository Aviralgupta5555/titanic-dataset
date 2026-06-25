# Power BI Export Guide

This guide explains how to take the Python EDA outputs from this project
and recreate or complement them in Microsoft Power BI Desktop.

---

## Option 1 — Connect Power BI to the CSV

1. Open **Power BI Desktop** → *Get Data* → **Text/CSV**
2. Navigate to `data/titanic.csv`
3. Click **Transform Data** (Power Query opens)

### Recommended Power Query steps (mirrors `generate_data.py`)

```powerquery
// 1. Fill missing Age with median
let
    MedianAge = List.Median(Table.Column(Source, "Age")),
    #"Filled Age" = Table.ReplaceValue(Source, null, MedianAge,
                      Replacer.ReplaceValue, {"Age"})
in
    #"Filled Age"
```

```powerquery
// 2. Add FamilySize column
= Table.AddColumn(#"Filled Age", "FamilySize",
    each [SibSp] + [Parch] + 1, Int64.Type)

// 3. Add IsAlone column
= Table.AddColumn(#"FamilySize", "IsAlone",
    each if [FamilySize] = 1 then 1 else 0, Int64.Type)

// 4. Add AgeGroup column
= Table.AddColumn(#"IsAlone", "AgeGroup",
    each if [Age] <= 12 then "Child"
         else if [Age] <= 17 then "Teen"
         else if [Age] <= 35 then "Adult"
         else if [Age] <= 60 then "Middle-Age"
         else "Senior")
```

---

## Option 2 — Use Python script inside Power BI

Power BI Desktop supports running Python scripts directly:

1. *Get Data* → **Python script**
2. Paste this snippet:

```python
import pandas as pd
import sys, os

sys.path.insert(0, r"d:\da project")
from generate_data import load_and_clean

dataset = load_and_clean()
```

3. Select the `dataset` table → **Load**

Power BI will now have all engineered features available as columns.

---

## Recommended Visuals in Power BI

| Python Chart | Power BI Visual |
|---|---|
| Survival donut | Donut chart — Survived (Legend), Count (Values) |
| Class bar | Clustered bar — Pclass (Axis), Count (Value), Survived (Legend) |
| Age histogram | Histogram (from AppSource) or Column chart with Age bins |
| Heatmap | Matrix visual — Pclass (Rows), Sex (Columns), Avg Survived (Values) |
| Scatter | Scatter chart — Age (X), Fare (Y), Survived (Legend), FamilySize (Size) |
| Correlation | Custom visual: *Correlation plot* from AppSource |

---

## DAX Measures (copy into Power BI)

```dax
Survival Rate = DIVIDE(SUM(titanic[Survived]), COUNT(titanic[PassengerId]))

Female Survival Rate =
    CALCULATE(
        DIVIDE(SUM(titanic[Survived]), COUNT(titanic[PassengerId])),
        titanic[Sex] = "female"
    )

Avg Fare = AVERAGE(titanic[Fare])

Class 1 Survival Rate =
    CALCULATE(
        DIVIDE(SUM(titanic[Survived]), COUNT(titanic[PassengerId])),
        titanic[Pclass] = 1
    )
```

---

## Theme

To match the clean light theme used in the Streamlit dashboard,
import this JSON theme in Power BI (*View → Themes → Browse for themes*):

```json
{
  "name": "Titanic Light",
  "dataColors": ["#2563EB","#10B981","#F59E0B","#6366F1","#0EA5E9","#F43F5E"],
  "background": "#F8FAFC",
  "foreground": "#0F172A",
  "tableAccent": "#2563EB"
}
```
