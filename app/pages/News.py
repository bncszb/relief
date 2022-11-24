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
    with open("app/cache/news/keywords.txt", "w") as f:
        print(st.session_state.keyword, file=f)

def update_table():
    conn=sqlite3.connect(db_path)
    sql_data=pd.read_sql_query(query, conn)

    merged_results=sql_data.groupby(["title","date"]).aggregate(set).reset_index()


    results.empty()
    results.write(merged_results)
if __name__ == '__main__':
    st.set_page_config(
        layout="wide"
    )
    st.markdown("""
    # News
    Scrape search results for a certain keyword in the news portals of Hungarian counties.
    """)

    st.text_input("Keyword", key="keyword", on_change=export_keyword)

    st.button("Search keyword", on_click=scrape_news)

    st.button("Update table", on_click=update_table)


    results=st.container()
    results.empty()
