# 🍺 Global Breweries Dashboard (Streamlit)

Interactive dashboard exploring brewery locations and composition patterns worldwide.

Built using:
- Streamlit
- Plotly
- PyDeck
- Pandas

---

## 🚀 Run Locally

1. Clone the repository:

```bash
git clone https://github.com/<YOUR_USERNAME>/breweries-of-the-world.git
cd breweries-of-the-world/streamlit_app
```

2. (Optional but recommended) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app/app.py
```

The app will open in your browser at:
```
http://localhost:8501
```

---

## Features

- Country + brewery type filters
- Interactive geographic map
- Country-level brewery counts
- Composition charts (100% stacked bar)

---

## Known Data Issues (In Progress)

- Some brewery locations may appear in incorrect positions (data validation ongoing).
- Country coverage varies depending on dataset completeness.

Data cleaning improvements are ongoing.

---

## 📁 Data

The dashboard uses a cleaned dataset located in:

```
app/cleaned data/breweries_cleaned_all.csv
```

If running this project without the dataset:
- Ensure the cleaned CSV is present in that directory
- Or update the `DATA_PATH` in `app.py`
