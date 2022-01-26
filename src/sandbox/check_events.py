import pandas as pd
import bs4
from datetime import datetime, timedelta

def get_keywords(path):
    with open(path) as keywords_file:
        keywords = keywords_file.read().splitlines()

    return keywords


site_df=pd.read_excel("/Users/benceszabo/Side/relief/data/local/counties.xlsx")

keywords_path="/Users/benceszabo/Side/relief/src/keywords.txt"
keywords=get_keywords(keywords_path)



for keyword in keywords:
    for i in site_df.index:

        site_name=site_df["site_name"].iloc[i]
        file_name=f"/Users/benceszabo/Side/relief/data/local/search_results/{site_name}_{keyword}.html"

        print (f"{site_name}: {keyword}")

        with open(file_name,"r") as html_file:
            html_text=html_file.read()

        soup=bs4.BeautifulSoup(html_text)
        subsoup=soup.find(class_="left-column ng-tns-c101-0")
        try:
            results=subsoup.find_all(class_="article-block ng-star-inserted")
            print(len(results))

        except:
            print("No results")
            continue

        for result in results:
            date=result.find(class_="article-date").text
            date=date.lower()

            if "órája" in date or "perce" in date or "tegnap" in date:
                print (date)
                url=site_df["site"].iloc[i]+result.find(class_="article-link ng-star-inserted")["href"][1:]
                print (url)

            else:
                date_obj = datetime. strptime(date, '%Y.%m.%d. %H:%M')
            

                if datetime.now()-timedelta(days=1) < date_obj:
                    print (date)
                    print (results.find(class_="article-link ng-star-inserted")["href"])   

    