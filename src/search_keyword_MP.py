from requests_html import AsyncHTMLSession
import pandas as pd
import multiprocessing as mp



async def get_html_for_URL(url):

    r = await asession.get(url)
    print (len(r.html))

def get_keywords(path):
    with open(path) as keywords_file:
        keywords = keywords_file.read().splitlines()

    return keywords

def download_html(URL, file_name):
    print(URL)
    html=get_html_for_URL(URL)
    with open(file_name,"w") as html_file:
        html_file.write(str(html.html))


site_df=pd.read_excel("/Users/benceszabo/Side/relief/data/local/counties.xlsx")


keywords_path="/Users/benceszabo/Side/relief/src/keywords.txt"
keywords=get_keywords(keywords_path)

search="kereses?global_filter="
asession = AsyncHTMLSession()

inputs=[]
for keyword in keywords:
    for i in site_df.index:
        URL=site_df["site"].iloc[i]+search+keyword
        site_name=site_df["site_name"].iloc[i]
        file_name=f"/Users/benceszabo/Side/relief/data/local/search_results/{site_name}_{keyword}.html"
        
        inputs.append((URL,file_name))
        #print (URL)

        #html=get_html_for_URL(URL)
        #with open(file_name,"w") as html_file:
        #    html_file.write(str(html.html))

for (URL, file_name) in inputs:
    asession.run(get_html_for_URL(URL))


