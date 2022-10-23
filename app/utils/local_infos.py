import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
from geopy import distance


base_url="http://xn--tosz-5qa.hu/szolgaltatasaink/onkormanyzati-adatbazis/?telepules="
print("Reading settlement coordinates")
settlement_coords=pd.read_csv("../data/database/settlement_coordinates.csv")


def get_county_urls():
    
    county_page = requests.get(base_url)

    soup= BeautifulSoup(county_page.text) 

    selectors=soup.find_all("select")
    for s in selectors:
        if "megye" in s["onchange"]:
            county_opts = {o.text: o["value"] for o in s.contents if "Válasszon" not in o.text}
            break

    return county_opts

def get_town_urls(county_opts):
    all_towns={}
    for k in county_opts:
        county_URL=base_url+county_opts[k]
        print(k)
        
        county_page = requests.get(county_URL)
        county_soup= BeautifulSoup(county_page.text)

        selectors=county_soup.find_all("select")
        for s in selectors:
            if "telepules" in s["onchange"]:
                opts = {o.text: o["value"] for o in s.contents if "Válasszon" not in o.text}
                break

        all_towns.update(opts)
        time.sleep(1)
    return all_towns

def get_data_for_towns(towns):
    with open("/Users/benceszabo/Side/relief/src/field/toosz_towns.json") as f:
        town_urls=json.load(f)

    df = pd.DataFrame(columns=['Polgármester e-mail', 'Polgármester', 'Cím', 'Önkormányzat telefon',
        'Önkormányzat e-mail'])

    for k in towns:
        town_url=base_url+town_urls[k]
        print(k)
        
        town_page = requests.get(town_url)
        town_soup= BeautifulSoup(town_page.text)
        town_soup.find_all("col_md_6")

        col_md_6s=town_soup.find_all("div", {"class": "col-md-6"})

        town_info={}
        for c in col_md_6s:
            if "önkormányzat" in str(c.contents[0]).lower():
                for line in c.contents[0].contents:
                    if "Cím:" in line:
                        town_info['Cím']=line.replace("Cím: ","")
                    elif "Telefon" in line:
                        town_info['Önkormányzat telefon']=line.replace("Telefon: ","")
                    elif "mailto:" in str(line):
                        town_info['Önkormányzat e-mail']=line.text

            if "polgármester" in str(c.contents[0]).lower():
                for line in c.contents[0].contents:
                    if "Cím:" in line:
                        town_info['Cím']=line.replace("Cím: ","")
                    elif "Telefon" in line:
                        town_info['Polgármester telefon']=line.replace("Telefon: ","")
                    elif "mailto:" in str(line):
                        town_info['Polgármester e-mail']=line.text
                
                town_info['Polgármester']=c.contents[0].contents[3]
        town_series=pd.Series(town_info,name=k)
        df.loc[k]=town_info
        time.sleep(1)
    return df
            

def get_coords(settlement):
    coords= settlement_coords.groupby("Settlement").mean().loc[settlement]
    return coords["longitude"],coords["latitude"]


# def close_towns(town, radius):

#     locations=settlement_coords.groupby("Settlement").mean().reset_index()

#     epicenter = get_coords(town)

#     locations["distance"]=locations.apply(lambda row: distance.distance(epicenter,(row["longitude"], row["latitude"])).km,axis=1)
#     locations=locations[locations["distance"]<radius]
#     return list(locations["Settlement"])


def close_towns(epicenter, radius):
    locations=settlement_coords.groupby("Settlement").mean().reset_index()

    locations["distance"]=locations.apply(lambda row: distance.distance(epicenter,(row["longitude"], row["latitude"])).km,axis=1)
    locations=locations[locations["distance"]<radius]
    return locations