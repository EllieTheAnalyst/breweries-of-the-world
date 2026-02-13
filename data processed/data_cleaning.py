#!/usr/bin/env python
# coding: utf-8

# **First Inspection**

"""
Global Breweries Analysis
Data Cleaning Script

Author: Ellie
Description: Cleans and prepares Open Brewery data for visualization.
"""


import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 50)


# In[292]:


breweries = pd.read_csv("../raw data/breweries.csv")


# In[293]:


breweries.head()


# In[294]:


breweries.info()


# **Create a working copy (never work on the actual raw dataset)**

# In[295]:


df = breweries.copy()


# **Standardise column names**

# In[296]:


df.columns = (
    df.columns
    .str.lower()
    .str.strip()
)


# **Drop columns you don’t need**

# In[297]:


df = df[
    [
        "id",
        "name",
        "brewery_type",
        "city",
        "state_province",
        "country",
        "latitude",
        "longitude",
    ]
]


# **Quick check**

# In[298]:


df.info()


# **Sanity check the country column**
# 
# #How US-heavy is the dataset? 

# In[299]:


df["country"].value_counts().head(15)


# ## Data Coverage Observation
# 
# The dataset is heavily skewed toward the United States, which accounts for the vast majority
# of recorded breweries. This reflects the underlying data collection process of Open Brewery DB,
# which relies on open and community-sourced contributions. As a result, brewery counts should
# be interpreted as indicators of dataset coverage rather than true national totals.
# 
# ## Analytical Scope: Excluding the United States
# 
# Due to the overwhelming dominance of U.S. entries in the dataset, the United States is excluded
# from subsequent analyses. This allows for a more interpretable comparison between other countries
# represented in Open Brewery DB.
# 
# All results should be interpreted as reflecting dataset coverage rather than true national brewery counts.

# In[300]:


df_non_us = df[df["country"] != "United States"].copy()


# **Quick Check**

# In[301]:


df_non_us.shape


# In[302]:


df_non_us["country"].value_counts()


# ## First analysis
# 
# # Top tier (within this dataset)
# 
# - Australia (514) → very strong coverage, active craft scene, English-language bias
# 
# - South Africa (104) → surprisingly high → interesting insight! 
# 
# - Ireland (70) → culturally expected, validates the dataset a bit
# 
# # UK fragmentation
# 
# - England (62)
# 
# - Scotland (10)
# 
# - Isle of Man (2)
# 
# UK ≈ 74 breweries -> That would put the UK ahead of Ireland in this dataset.

# ## Country Definitions and Cultural Context
# 
# The dataset distinguishes between England, Scotland, and other constituent countries
# of the United Kingdom. These categories are preserved in the analysis.
# 
# This decision is intentional: brewing traditions, alcohol culture, and identity
# differ significantly across these regions, and aggregating them into a single
# "United Kingdom" category would obscure culturally meaningful differences.

# In[303]:


# cleaned dataset including the US
df.to_csv(
    "../cleaned data/breweries_cleaned_all.csv",
    index=False
)


# ## Cleaning Complete
# 
# The cleaned dataset was saved to disk and will be used for all subsequent analyses
# and visualisations. This notebook focuses solely on inspection and data preparation.

# ## Debugging Insight: Invalid Geographic Coordinates
# 
# During Tableau-based spatial visualisation, several brewery records appeared in
# geographically impossible locations (e.g., latitude values exceeding the valid
# range of -90 to 90 degrees).
# 
# Inspection of tooltips revealed invalid or inconsistent coordinate values,
# including swapped latitude/longitude pairs and implausible magnitudes
# (e.g., latitude values in the millions).
# 
# A validation step was therefore introduced to retain only records with:
# - Latitude between -90 and 90
# - Longitude between -180 and 180
# 
# As a result, 2,380 records (~26% of the dataset) were excluded from spatial analysis.
# 
# This highlights the iterative nature of exploratory data analysis:
# visualisation can reveal structural data issues not evident in tabular inspection.
# 

# In[304]:


len_before = len(df)


# In[305]:


df = df[
    (df["latitude"].between(-90, 90)) &
    (df["longitude"].between(-180, 180))
]


# In[306]:


len_after = len(df)

print("Rows removed:", len_before - len_after)


# In[307]:


df.shape


# In[308]:


df.to_csv("../cleaned data/breweries_cleaned_all.csv", index=False)


# In[309]:


df = pd.read_csv("../cleaned data/breweries_cleaned_all.csv")

print("Max latitude:", df["latitude"].max())
print("Min latitude:", df["latitude"].min())
print("Max longitude:", df["longitude"].max())
print("Min longitude:", df["longitude"].min())


# ### Final Dataset Export (Post-Validation)
# 
# After identifying and correcting invalid geographic coordinates during 
# Tableau-based spatial debugging, the validated dataset is re-exported.
# 
# This file now represents the definitive cleaned version used for 
# all subsequent spatial analysis and dashboard development.
