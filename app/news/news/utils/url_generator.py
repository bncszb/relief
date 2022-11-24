import pandas as pd
import sys
sys.path.append("..")

def get_keywords(keywords_path="../cache/news/keywords.txt"):

    with open(keywords_path) as keywords_file:
        keywords = keywords_file.read().splitlines()
    keywords=[kw for kw in keywords if kw !=""]

    return keywords


def get_urls_for_keyword (keyword):
    sites_path="../data/counties_NER.xlsx"
    site_df=pd.read_excel(sites_path)

    search="kereses?text="

    urls=[]
    for i in site_df.index:
        URL=site_df["site"].iloc[i]+search+keyword
        site_name=site_df["site_name"].iloc[i]
        urls.append(URL)
    return urls

def get_search_df_for_keyword (keyword):
    sites_path="../data/counties_NER.xlsx"

    site_df=pd.read_excel(sites_path)
    search="kereses?text="

    site_df["url"]=site_df["site"]+search+keyword
    site_df["region"]=site_df["Megye neve"]
    search_df=site_df[["region", "url"]]
    return search_df