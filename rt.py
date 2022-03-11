"""
Rₜ Choropleth Map
"""

# %%
__author__ = "Daniel Cárdenas"
__maintainer__ = "Daniel Cárdenas"
__email__ = "jcard151@fiu.edu"

# %%
import functools
import json
from urllib.request import urlopen

import numpy as np
import pandas as pd
import plotly.express as px
from IPython import get_ipython

# %%
df = pd.read_csv(
    "https://raw.githubusercontent.com/epiforecasts/covid-rt-estimates/master/subnational/united-states/cases/summary/rt.csv",
    usecols=["date", "state", "mean", "lower_90", "upper_90"],
    parse_dates=["date"],
    infer_datetime_format=True,
)

# %%
df

# %%
df = df.rename(columns={"mean": "rt"})

# %%
df["rt"] = round(df.rt, 2)
df["lower_90"] = round(df["lower_90"], 2)
df["upper_90"] = round(df["upper_90"], 2)

# %%
case_data = pd.read_csv(
    "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
    parse_dates=["date"],
    infer_datetime_format=True,
    usecols=["date", "state", "cases", "deaths"],
)

# %%
live_case_data = pd.read_csv(
    "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv",
    parse_dates=["date"],
    infer_datetime_format=True,
    usecols=["date", "state", "cases", "deaths"],
)

# %%
case_data = pd.concat([case_data, live_case_data])

# %%
# abbre = {
#     "AL": "Alabama",
#     "AK": "Alaska",
#     "AZ": "Arizona",
#     "AR": "Arkansas",
#     "CA": "California",
#     "CO": "Colorado",
#     "CT": "Connecticut",
#     "DE": "Delaware",
#     "FL": "Florida",
#     "GA": "Georgia",
#     "HI": "Hawaii",
#     "ID": "Idaho",
#     "IL": "Illinois",
#     "IN": "Indiana",
#     "IA": "Iowa",
#     "KS": "Kansas",
#     "KY": "Kentucky",
#     "LA": "Louisiana",
#     "ME": "Maine",
#     "MD": "Maryland",
#     "MA": "Massachusetts",
#     "MI": "Michigan",
#     "MN": "Minnesota",
#     "MS": "Mississippi",
#     "MO": "Missouri",
#     "MT": "Montana",
#     "NE": "Nebraska",
#     "NV": "Nevada",
#     "NH": "New Hampshire",
#     "NJ": "New Jersey",
#     "NM": "New Mexico",
#     "NY": "New York",
#     "NC": "North Carolina",
#     "ND": "North Dakota",
#     "OH": "Ohio",
#     "OK": "Oklahoma",
#     "OR": "Oregon",
#     "PA": "Pennsylvania",
#     "RI": "Rhode Island",
#     "SC": "South Carolina",
#     "SD": "South Dakota",
#     "TN": "Tennessee",
#     "TX": "Texas",
#     "UT": "Utah",
#     "VT": "Vermont",
#     "VA": "Virginia",
#     "WA": "Washington",
#     "WV": "West Virginia",
#     "WI": "Wisconsin",
#     "WY": "Wyoming",
# }

# %%
state_codes = {
    "Alabama": "01",
    "Alaska": "02",
    "Arizona": "04",
    "Arkansas": "05",
    "California": "06",
    "Colorado": "08",
    "Connecticut": "09",
    "Delaware": "10",
    "District of Columbia": "11",
    "Florida": "12",
    "Georgia": "13",
    "Hawaii": "15",
    "Idaho": "16",
    "Illinois": "17",
    "Indiana": "18",
    "Iowa": "19",
    "Kansas": "20",
    "Kentucky": "21",
    "Louisiana": "22",
    "Maine": "23",
    "Maryland": "24",
    "Massachusetts": "25",
    "Michigan": "26",
    "Minnesota": "27",
    "Mississippi": "28",
    "Missouri": "29",
    "Montana": "30",
    "Nebraska": "31",
    "Nevada": "32",
    "New Hampshire": "33",
    "New Jersey": "34",
    "New Mexico": "35",
    "New York": "36",
    "North Carolina": "37",
    "North Dakota": "38",
    "Ohio": "39",
    "Oklahoma": "40",
    "Oregon": "41",
    "Pennsylvania": "42",
    "Rhode Island": "44",
    "South Carolina": "45",
    "South Dakota": "46",
    "Tennessee": "47",
    "Texas": "48",
    "Utah": "49",
    "Vermont": "50",
    "Virginia": "51",
    "Washington": "53",
    "West Virginia": "54",
    "Wisconsin": "55",
    "Wyoming": "56",
}

# %%
# df["state"] = df["state"].map(abbre)

# %%
df["fips"] = df["state"].map(state_codes)


# %%
def date_ranges(dataframe):
    """
    Slices DataFrame to specific dates.
    """

    latest = sorted(dataframe["date"].unique())[-1]
    today = pd.Timestamp.today().normalize()
    two_w_ago = today - np.timedelta64(14, "D")
    one_m_ago = (today - pd.DateOffset(months=1)).to_numpy()
    two_m_ago = (today - pd.DateOffset(months=2)).to_numpy()
    three_m_ago = (today - pd.DateOffset(months=3)).to_numpy()

    dates = [latest, today, two_w_ago, one_m_ago, two_m_ago, three_m_ago]

    df_dates = [dataframe["date"] == date for date in dates]

    filtered = functools.reduce(lambda x, y: x | y, df_dates)

    return dataframe[filtered]


# %%
plotly = date_ranges(df).merge(date_ranges(case_data), how="left")

# %%
plotly.query("state == 'New York'")

# %%
plotly.sort_values(by=["date", "state"], inplace=True, ascending=True)

# %%
plotly

# %%
plotly.to_csv("data/rt.csv", index=False)

# %%
plotly = pd.read_csv("data/rt.csv", dtype={"fips": str})


# %%
URL = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"

with urlopen(URL) as response:
    us = json.load(response)

# %%
fig = px.choropleth(
    plotly,
    geojson=us,
    locations="fips",
    featureidkey="id",
    animation_frame="date",
    animation_group="rt",
    color="rt",
    color_continuous_scale=[
        (0, "green"),
        (0.5, "rgb(135, 226, 135)"),
        (0.5, "rgb(226, 136, 136)"),
        (1, "red"),
    ],
    hover_name="state",
    hover_data=["date", "rt", "lower_90", "upper_90", "cases", "deaths"],
    range_color=(0, 2),
    center={"lon": -94.99141861526407, "lat": 38.1354813882185},
    scope="usa",
    labels={
        "date": "Date",
        "state": "State",
        "rt": "Rₜ",
        "lower_90": "Lower Range",
        "upper_90": "Upper Range",
        "cases": "Cases",
        "deaths": "Deaths",
        "fips": "FIPS",
    },
)


fig.layout.font.family = "Arial"

fig.update_layout(
    title="Rₜ: COVID-19 | United States",
    annotations=[
        dict(
            xanchor="right",
            x=1,
            yanchor="top",
            y=-0.05,
            showarrow=False,
            text="Sources: https://epiforecasts.io/covid/, The New York Times",
        )
    ],
    autosize=True,
)

fig.show()

# %%
with open("../danielcs88.github.io/html/rt.html", "w", encoding="utf_8") as f:
    f.write(fig.to_html(include_plotlyjs="cdn"))


# %%
get_ipython().system(" cd ../danielcs88.github.io/ && git pull")


# %%
get_ipython().system(
    ' cd ../danielcs88.github.io/ && git add --all && git commit -m "Update" && git push'
)
