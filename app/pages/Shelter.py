import streamlit as st
import json
import pandas as pd
import utils.local_infos as li
from utils.misc import to_excel


MAPBOX_TOKEN="pk.eyJ1IjoiYm5jc3piIiwiYSI6ImNsOWw3YmJ2MjFmemEzdW8wc2FnNThobXcifQ.vPHkFjv8WSsIgmS6tMlHhA"

if "schools_data" not in st.session_state:
    schools_data_path="/Users/benceszabo/Side/relief/data/database/kir_mukodo_feladatellatasi_helyek_2022_10_22.xlsx"
    print("Reading school data")
    st.session_state.schools_data = pd.read_excel(schools_data_path)
    col_ids=[3,7,8,9,10,12,13,14,25,26,28,64,65,66,67,69,73]
    cols=st.session_state.schools_data.columns[col_ids]
    st.session_state.schools_data=st.session_state.schools_data[cols]

if "town_urls" not in st.session_state:
    print("Reading town data")
    with open("../data/database/toosz_towns.json") as f:
        st.session_state.town_urls=json.load(f)

if "settlement_coords" not in st.session_state:
    print("Reading settlement coordinates")
    st.session_state.settlement_coords=pd.read_csv("../data/database/settlement_coordinates.csv")


def update_data():
    shelter_data.empty()
    st.session_state.close_towns=li.close_towns(epicenter, radius)

    towns_nearby=list(st.session_state.close_towns["Settlement"])
    st.session_state.settlement_contacts=li.get_data_for_towns(towns_nearby)


    st.session_state.close_schools=st.session_state.schools_data[st.session_state.schools_data["A feladatellátási hely települése"].isin(towns_nearby)]


if __name__ == '__main__':

    st.set_page_config(
        layout="wide"
        )

    if "settlement" not in st.session_state:
        st.session_state.settlement = None

    if "close_towns" not in st.session_state:
        st.session_state.close_towns = None
    
    if "settlement_contacts" not in st.session_state:
        st.session_state.settlement_contacts = None
    
    if "close_schools" not in st.session_state:
        st.session_state.close_schools = None

    st.title("Shelter")
    st.markdown("""
    This page is for finding contact infos given the name of the settlement.
    For this you have to:
    - select the name of the settlement
    - set a radius (in km) in which you plan to operate
    
    WARNING
    This is a proof of concept site. The data, and the methods through which we gather them are NOT yet maintained.

    Settlement contacts are scraped from: http://xn--tosz-5qa.hu/szolgaltatasaink/onkormanyzati-adatbazis/?telepules=   
    School contacts are filtered from the dataframe published on 2022/10/22 at: https://dari.oktatas.hu/ -- 'Működő köznevelési feladatellátási helyek listája'  

    TO DO:
    - we need better error messages if the scraping is unsuccessful
    - school database updates need to be added
    """)

    st.session_state.settlement=st.selectbox("Settlement in need", st.session_state.settlement_coords["Settlement"])

    settlement_info=st.container()

    epicenter=li.get_coords(st.session_state.settlement)

    settlement_info.write(f"**{st.session_state.settlement}** coordinates: N {epicenter[0]: 0.6}, E {epicenter[1]: 0.6}")

    radius=st.slider("Radius for shelters", min_value=0, max_value=50, step=5, value=10)

    st.button("Get data", on_click=update_data)
    
    shelter_data=st.container()

    shelter_data.empty()
 
    if st.session_state.close_towns is not None:
 
        shelter_data.map(st.session_state.close_towns)

    if st.session_state.settlement_contacts is not None:

        shelter_data.table(st.session_state.settlement_contacts)
        contacts_xlsx = to_excel(st.session_state.settlement_contacts)
        shelter_data.download_button(label='📥 Download Settlement Contacts',
                                    data=contacts_xlsx ,
                                    file_name= 'settlement_contacts.xlsx')

    if st.session_state.close_schools is not None:

        shelter_data.table(st.session_state.close_schools)

        school_contacts_xlsx = to_excel(st.session_state.close_schools)

        shelter_data.download_button(label='📥 Download School Contacts',
                                    data=school_contacts_xlsx ,
                                    file_name= 'school_contacts.xlsx')