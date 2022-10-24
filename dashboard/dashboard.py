from datetime import date
from typing import Optional

import pandas as pd
import pydeck as pdk
import requests
import streamlit as st

from config.runtime_config import RuntimeConfig


def get_data(crime_type: Optional[str] = None, crime_date: Optional[date] = None):
    """Get data from crime app endpoint and convert it to pandas dataframe and return it"""
    url = f"http://{RuntimeConfig.crime_app_host}:{RuntimeConfig.crime_app_port}/crimes"
    params = {'crime_type': crime_type, 'crime_date': crime_date}
    response = requests.get(url=url, params=params)
    response_dataframe = pd.DataFrame.from_records(response.json()).dropna()
    return response_dataframe


def main():
    st.title(RuntimeConfig.dashboard_name)
    crime_type_value = st.sidebar.multiselect(label='Select crime type:',
                                              options=get_data().primary_type.unique())

    crime_date_value = st.sidebar.date_input(label='Pick a Date')
    crime_date_checkbox = st.sidebar.checkbox(label='Filter by date')
    if crime_date_checkbox:
        crime_date_filter = crime_date_value
    else:
        crime_date_filter = None

    st.write(get_data(crime_type=crime_type_value, crime_date=crime_date_filter))
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=get_data(crime_type=crime_type_value, crime_date=crime_date_filter),
        get_position=["longitude", "latitude"],
        get_color=[200, 30, 0, 160],
        get_radius=1500,
        radius_scale=0.05,
    )
    view_state = pdk.ViewState(latitude=41.87, longitude=-87.62, zoom=11, bearing=0, pitch=45)

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
    )
    st.pydeck_chart(r)


if __name__ == "__main__":
    main()
