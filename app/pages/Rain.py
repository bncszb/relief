import requests
import zipfile

import matplotlib.pyplot as plt
from scipy.io import netcdf
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import os
import shutil
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from colorcet import fire
import datashader.transfer_functions as tf
import plotly.express as px
import pandas as pd

MAPBOX_TOKEN="pk.eyJ1IjoiYm5jc3piIiwiYSI6ImNsOWw3YmJ2MjFmemEzdW8wc2FnNThobXcifQ.vPHkFjv8WSsIgmS6tMlHhA"

def round_dt(dt, delta):
    return datetime.min + round((dt - datetime.min) / delta) * delta

def get_radar_data(number_of_reports):
    
    dir_path=f"app/cache/rain_data"
    shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)

    p="https://odp.met.hu/weather/radar/composite/nc/refl2D_pscappi/radar_composite-refl2D_pscappi-{}.nc.zip"
    zip_path="app/cache/rain_data/radar_composite-refl2D_pscappi-{}.nc.zip"
    

    now=datetime.utcnow()
    delta = timedelta(minutes=5)
    now=round_dt(now, delta)

    radar_paths=[]

    while len(radar_paths)<number_of_reports:

        timestamp=datetime.strftime(now, "%Y%m%d_%H%M")
        url=p.format(timestamp)

        print(now)
        print(url)

        response=requests.get(url)
        statuscode=response.status_code
        print(statuscode)

        if statuscode==200:
            data_path=zip_path.format(timestamp)
            with open(data_path, "wb")as file:
                file.write(response.content)

            with zipfile.ZipFile(data_path, 'r') as zip_ref:
                zip_ref.extractall(dir_path)

            

            radar_paths.append(data_path.replace(".zip",""))

        now=now-delta

    return radar_paths

def read_radar_data(radar_path):
    file2read = netcdf.NetCDFFile(radar_path,'r')
    rain = file2read.variables["refl2D_pscappi"][:]
    rain = (rain>0)*rain
    rain = 0.01*rain
    return rain

def create_rain_fig(path):

    LON_MIN=13.5
    LON_MAX=25.5
    LAT_MIN=44.004
    LAT_MAX=50.5

    LAT_STEPS=813
    LON_STEPS=961

    lat=np.linspace(LAT_MIN, LAT_MAX, LAT_STEPS)
    lon=np.linspace(LON_MIN, LON_MAX, LON_STEPS)

    coordinates = [[LON_MIN, LAT_MIN],
                [LON_MAX, LAT_MIN],
                [LON_MAX, LAT_MAX],
                [LON_MIN, LAT_MAX]]

    center=pd.DataFrame([[(LAT_MIN+LAT_MAX)/2,(LON_MIN+LON_MAX)/2]], columns=["Lat", "Lon"])
    
    radar_data=rasterio.open(path)
    rain=radar_data.read(1)
    rain=np.where(rain>0, 0.01*rain, np.NaN)
    rain=xr.DataArray(rain,coords=[ ("Lat",lat),("Lon", lon),])

    img = tf.shade(rain, cmap=fire)[::-1].to_pil()

    fig = px.scatter_mapbox(center, lat='Lat', lon='Lon', zoom=5)
    fig.update_layout(mapbox_style="carto-darkmatter",
                    mapbox_layers = [
                    {
                        "sourcetype": "image",
                        "source": img,
                        "coordinates": coordinates
                    }]
    )
    return fig

def get_rain_data():
    radar_path=get_radar_data(1)[0]
    fig=create_rain_fig(radar_path)
    return fig


if __name__ == '__main__':

    st.set_page_config(
    layout="wide"
    )

    st.plotly_chart(get_rain_data())

    


