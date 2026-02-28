# Breweries of the World 🍺

## 🌍 Live Dashboard

https://global-breweries-dashboard.streamlit.app/

---

This repository explores a global dataset of breweries from around the world, with a focus on geographic distribution, country-level patterns, and data preparation for analysis and visualisation.

The project documents the data cleaning process and provides a cleaned, analysis-ready dataset that can be used for further exploration or visual storytelling.

---

## Project Overview

- Global coverage of breweries across multiple countries  
- Emphasis on data cleaning, standardisation, and validation  
- Designed as a foundation for exploratory data analysis and visualisation  
- Includes an interactive Streamlit dashboard for exploration  

This project is structured to evolve over time, documenting both technical progress and analytical insights.

---

## Data Cleaning

The cleaning process includes:

- Removing duplicates and incomplete entries  
- Standardising country and location information  
- Ensuring consistent formatting across variables  
- Converting latitude and longitude to numeric types  
- Basic geographic validation (range checks)

The final cleaned dataset is provided for reuse and further analysis.

---

## Interactive Dashboard

A Streamlit dashboard is included in:

```
app/app.py
```

The dashboard allows users to:

- Filter by country and brewery type  
- Explore geographic distributions on an interactive map  
- Compare brewery counts across countries  
- Analyse brewery type composition  

See the `app/app-README.md` for instructions on running the app locally.

---

## Current Learnings & Observations

During development and visual exploration, several important insights emerged:

- Data quality varies significantly by country.
- Geographic coordinates are not always reliable.
- Some entries appear misclassified (e.g., location inconsistencies).
- Dataset coverage does not reflect true global brewery counts, but rather API/database coverage.

These findings highlight the importance of critical validation when working with real-world open datasets.

---

## Known Issues (Work in Progress)

The following issues are currently being investigated:

- Some brewery locations appear incorrectly placed on the map (e.g., in the sea).
- Occasional country/location mismatches (e.g., a venue appearing in the wrong country).
- Missing or inconsistent coverage for certain countries (e.g., unexpectedly low counts).

These issues likely stem from:
- Incomplete or incorrect latitude/longitude data  
- API inconsistencies  
- Country standardisation challenges  
- Merge or transformation errors during cleaning  

Data validation improvements are planned in the next iteration.

---

## 🚀 Next Steps

Planned improvements include:

- Enhanced geographic validation (cross-checking coordinates against country boundaries)
- Improved country standardisation and mapping logic
- Investigation of unexpected country-level anomalies (e.g., where is Germany coverage?)
- Additional summary statistics for quality checks
- Deployment of the Streamlit dashboard (Streamlit Cloud)
- Expanded documentation of methodology
- add a downloadable CSV, better theming, and a small narrative section

The goal is to move from exploratory analysis toward a more robust, reproducible data pipeline.

---

## Status

Project in active development.  
Data validation and dashboard refinement ongoing.





