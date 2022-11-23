import pandas as pd
import requests
import zipfile
import pathlib as p

import matplotlib.pyplot as plt
import scipy.interpolate as interp
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import os

def get_weather_report ():
    date=days[st.session_state.new_date].strftime("%Y%m%d")
    
    rain_data_url=f"https://odp.met.hu/weather/weather_reports/synoptic/hungary/daily_rain/csv/HABP_1RD_{date}.csv.zip"
    dir_path=f"cache/rain_data/{date}"

    os.makedirs(dir_path, exist_ok=True)
    
    file_path=f"cache/rain_data/{date}/HABP_1RD_{date}.csv.zip"

    p.Path(dir_path).mkdir(exist_ok=True)

    rain_data = requests.get(rain_data_url)
    with open(file_path, "wb")as file:
        file.write(rain_data.content)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(dir_path)

    rain_df = pd.read_csv(file_path,delimiter=";")

    stripped_cols={c: c.strip() for c in rain_df.columns}

    rain_df=rain_df.rename(columns=stripped_cols)
    rain_df=rain_df.sort_values("r", ascending=False)

    st.session_state.rain_df=rain_df


if __name__ == '__main__':

    st.set_page_config(
    layout="wide"
    )

    if "rain_df" not in st.session_state:
        st.session_state.rain_df=None

    st.title("Rain")
    # .strftime("%Y%m%d")
    day=datetime.now()
    days={}
    for i in range(7):
        day=day - timedelta(days=1)
        days[day.strftime("%Y-%m-%d")]=day

    selected_day=st.selectbox("Get daily OMSZ report", days.keys(), on_change=get_weather_report, key="new_date")

    if st.session_state.rain_df is not None:
        st.table(st.session_state.rain_df.head())

        col1, col2= st.columns([1,1])
        with col1:
            fig, ax = plt.subplots()
            measurements=st.session_state.rain_df[st.session_state.rain_df["r"]!=-999]
            im=ax.scatter(measurements["Longitude"],measurements["Latitude"],c=measurements["r"])
            fig.colorbar(im)
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            measurements=st.session_state.rain_df[st.session_state.rain_df["r"]!=-999]
            
            # MS_data=[]
            # for row in measurements.iterrows():
            #     try:
            #         next_point = meteostat.Point(row[1]["Latitude"], row[1]["Longitude"])
            #         daily_data = meteostat.Daily(next_point, days[selected_day], days[selected_day]+ timedelta(days=1))
            #         next_pont={
            #             "Longitude": row[1]["Longitude"],
            #             "Latitude": row[1]["Latitude"],
            #             "r": daily_data.fetch()["prcp"].iloc[0]
            #         }
            #         MS_data.append(next_pont)
            #     except:
            #         pass

            # meteo_df=pd.DataFrame(MS_data)
            # im=ax.scatter(meteo_df["Longitude"],meteo_df["Latitude"],c=meteo_df["r"])


            x=measurements["Longitude"]
            y=measurements["Latitude"]
            z=measurements["r"]

            X = np.linspace(min(x), max(x), 500)
            Y = np.linspace(min(y), max(y), 500)

            X, Y = np.meshgrid(X, Y)


            interpolator_RBF = interp.RBFInterpolator(list(zip(x, y)), z)


            Z_RBF=interpolator_RBF(np.array([X,Y]).reshape(2, -1).T)
            im=ax.pcolormesh(X, Y, Z_RBF.reshape(500, 500), shading='auto',vmin=np.min(Z_RBF), vmax=np.max(Z_RBF))
            eps=0.0001 # Helps with the scatter colormap, it probably uses the lower end of the map if only one value is given
            ax.scatter(x,y,c=z,vmin=np.min(Z_RBF)-eps, vmax=np.max(Z_RBF)+eps)
            fig.colorbar(im)
            
            st.pyplot(fig)




