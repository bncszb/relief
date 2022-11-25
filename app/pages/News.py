import streamlit as st
import pandas as pd
import sqlite3
import os

import subprocess

db_path="app/cache/news/news.sqlite"

query="""
SELECT * FROM news_table
"""

def scrape_news():

    subprocess.run(["bash","app/scripts/update_news.sh"])



def export_keyword():
    print(os.getcwd())
    os.makedirs("app/cache/news", exist_ok=True)
    with open("app/cache/news/keywords.txt", "w") as f:
        print(st.session_state.keyword, file=f)

def update_table():
    conn=sqlite3.connect(db_path)
    sql_data=pd.read_sql_query(query, conn)

    if len(sql_data)>0:
        merged_results=sql_data.groupby(["title","date"]).aggregate(set).reset_index()

    else:
        merged_results=f"Nem található friss cikk **{st.session_state.keyword}** kulcsszóval."
    results.empty()
    results.write(merged_results)
if __name__ == '__main__':
    st.set_page_config(
        layout="wide"
    )
    st.markdown("""
    # News
    Ez az oldal a magyar hírportálok friss híreinek gyors átnézését segíti.  
    Jelenleg csak a megyei lapokat nézi, de később ez bővíthető más portálokra is. 

    ##### Útmutató:
    1. Írj be egy kulcsszót a lenti szövegdobozba
    2. Nyomd meg a **Keresés** gombot. Ez akár 10-15 másodpercet is igénybe vehet.
    3. Frissítsd a táblázatot a megfelelő gombbal.
    """)

    st.text_input("Kulcsszó", key="keyword", on_change=export_keyword)

    st.button("Keresés", on_click=scrape_news)

    st.button("Táblázat frissítése", on_click=update_table)


    results=st.container()
    results.empty()
