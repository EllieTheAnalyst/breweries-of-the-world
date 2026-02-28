#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import streamlit as st
import plotly.express as px
import pydeck as pdk
from pathlib import Path

# -----------------------------
# Paths (based on where app.py lives)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent  # .../global-breweries-analysis/app
DATA_PATH = BASE_DIR / "cleaned data" / "breweries_cleaned_all.csv"

# Helpful debug check
if not DATA_PATH.exists():
    st.error(f"CSV not found at: {DATA_PATH}")
    st.stop()

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Global Breweries Dashboard",
    page_icon="🍺",
    layout="wide",
)

st.title("🍺 Global Breweries Dashboard")
st.caption("Open Brewery data • Cleaned dataset • Built with Streamlit")

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Defensive casting (CSV can store as strings)
    for col in ["latitude", "longitude"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Normalize text columns a bit
    for col in ["country", "brewery_type", "state_province", "city", "name"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df

df = load_data(DATA_PATH)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

# Country filter
countries = sorted(df["country"].dropna().astype(str).str.strip().unique())
countries = [c for c in countries if c.lower() != "nan"]
selected_countries = st.sidebar.multiselect(
    "Country",
    options=countries,
    default=[],
    help="Leave empty to include all countries.",
    key="filter_countries",
)

# Brewery type filter
types = sorted([t for t in df["brewery_type"].dropna().unique() if t != "nan"])
selected_types = st.sidebar.multiselect(
    "Brewery Type",
    options=types,
    default=[],
    help="Leave empty to include all types.",
    key="filter_types",
)

# Apply filters
df_f = df.copy()
if selected_countries:
    df_f = df_f[df_f["country"].isin(selected_countries)]
if selected_types:
    df_f = df_f[df_f["brewery_type"].isin(selected_types)]

# A geo-valid subset for mapping
geo_mask = (
    df_f["latitude"].notna()
    & df_f["longitude"].notna()
    & df_f["latitude"].between(-90, 90)
    & df_f["longitude"].between(-180, 180)
)
df_geo = df_f.loc[geo_mask].copy()

# -----------------------------
# KPIs
# -----------------------------
k1, k2, k3 = st.columns(3)
k1.metric("Rows (filtered)", f"{len(df_f):,}")
k2.metric("Geo-valid rows", f"{len(df_geo):,}")
k3.metric("Countries (filtered)", f"{df_f['country'].nunique():,}")

st.divider()

# -----------------------------
# Tabs
# -----------------------------
tab_map, tab_country, tab_country_no_us, tab_types = st.tabs(
    ["🗺️ Map", "🌍 By Country", "🌍 By Country (Excl. US)", "🏷️ Types"]
)

# -----------------------------
# 1) MAP
# -----------------------------
with tab_map:
    st.subheader("Brewery Locations (Geo-valid)")

    # Helpful visibility/debug line
    st.caption(f"Showing {len(df_geo):,} geo-valid breweries")

    if df_geo.empty:
        st.warning("No geo-valid records with the current filters.")
    else:
        # Center the map on the data
        center_lat = float(df_geo["latitude"].mean())
        center_lon = float(df_geo["longitude"].mean())

        # Controls (pixel size works better than meters for dashboards)
        radius_px = st.slider("Point size (px)", 2, 30, 8, key="map_radius_px")
        opacity = st.slider("Point opacity", 0.1, 1.0, 0.75, step=0.05, key="map_opacity")
        zoom = st.slider("Map zoom", 1, 10, 3, key="map_zoom")

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_geo,
            get_position="[longitude, latitude]",
            get_radius=radius_px,
            radius_units="pixels",
            # Bright fill + outline so points show on dark basemap
            get_fill_color=[255, 99, 71, 180],      # tomato-ish w/ alpha
            get_line_color=[255, 255, 255, 220],    # white outline
            line_width_min_pixels=1,
            stroked=True,
            filled=True,
            pickable=True,
            auto_highlight=True,
            opacity=opacity,
        )

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom,
            min_zoom=1,
            max_zoom=15,
        )

        tooltip = {
            "html": "<b>{name}</b><br/>Type: {brewery_type}<br/>City: {city}<br/>Country: {country}",
            "style": {"backgroundColor": "white", "color": "black"},
        }

        st.pydeck_chart(
            pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
        )

    st.caption("Tip: Use the sidebar filters to focus on a subset (country/type).")

# -----------------------------
# 2) BY COUNTRY
# -----------------------------
with tab_country:
    st.subheader("Recorded Breweries by Country")

    country_counts = (
        df_f.groupby("country", dropna=False)["id"]
        .count()
        .sort_values(ascending=False)
        .reset_index(name="count")
    )

    top_n = st.slider("Show top N countries", 5, 50, 20, key="top_n_countries")
    plot_df = country_counts.head(top_n)

    fig = px.bar(
        plot_df,
        x="count",
        y="country",
        orientation="h",
        text="count",
        title=None,
        labels={"count": "Recorded breweries", "country": ""},
    )
    fig.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
    fig.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True, key="country_bar")

    st.caption("Note: This reflects dataset coverage, not true national totals.")

# -----------------------------
# 3) BY COUNTRY EXCL US
# -----------------------------
with tab_country_no_us:
    st.subheader("Recorded Breweries by Country (Excluding United States)")

    df_no_us = df_f[df_f["country"] != "United States"].copy()

    if df_no_us.empty:
        st.warning("No rows after excluding United States (check your filters).")
    else:
        country_counts_no_us = (
            df_no_us.groupby("country")["id"]
            .count()
            .sort_values(ascending=False)
            .reset_index(name="count")
        )

        top_n2 = st.slider("Show top N (excl. US)", 5, 50, 20, key="top_n_no_us")
        plot_df2 = country_counts_no_us.head(top_n2)

        fig2 = px.bar(
            plot_df2,
            x="count",
            y="country",
            orientation="h",
            text="count",
            labels={"count": "Recorded breweries", "country": ""},
        )
        fig2.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
        fig2.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig2, use_container_width=True, key="country_bar_no_us")

# -----------------------------
# 4) TYPES
# -----------------------------
with tab_types:
    st.subheader("Brewery Type Composition (Top Countries)")

    exclude_types = st.multiselect(
        "Exclude types",
        options=sorted(types),
        default=["planning", "closed", "location"],
        help="Optional cleanup for visualization clarity.",
        key="exclude_types",
    )

    df_types = df_f.copy()
    if exclude_types:
        df_types = df_types[~df_types["brewery_type"].isin(exclude_types)]

    if df_types.empty:
        st.warning("No rows after type exclusions (check filters).")
    else:
        top_countries_n = st.slider("Top N countries to compare", 3, 15, 5, key="top_n_compare")

        top_countries = (
            df_types.groupby("country")["id"].count().sort_values(ascending=False).head(top_countries_n).index
        )

        comp = (
            df_types[df_types["country"].isin(top_countries)]
            .groupby(["country", "brewery_type"])["id"]
            .count()
            .reset_index(name="count")
        )

        comp["share"] = comp["count"] / comp.groupby("country")["count"].transform("sum")

        fig3 = px.bar(
            comp,
            x="share",
            y="country",
            color="brewery_type",
            orientation="h",
            labels={"share": "Share of breweries", "country": ""},
        )
        fig3.update_layout(height=500)
        fig3.update_xaxes(tickformat=".0%")
        st.plotly_chart(fig3, use_container_width=True, key="types_comp")

        st.caption("This is a composition chart: each country sums to 100%.")

st.divider()
st.caption("Next upgrade: add a downloadable CSV, better theming, and a small narrative section for your portfolio.")

