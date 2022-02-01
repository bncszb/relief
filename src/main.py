from ast import keyword
import pandas as pd
import utils.check_url as cu
import utils.url_generator as ug
import utils.reports as rep
import datetime
import time



if __name__=="__main__":

    print("Sleeping 10 seconds...")
    time.sleep(10)

    print("Starting scraping...")
    keywords=ug.get_keywords()

    all_results=[]
    for key in keywords:
        print(f"Keyword: {key}")
        urls=ug.get_search_df_for_keyword(key)[:1]

        results=cu.search_URLs_df(urls)
        results["key"]=key
        results.to_csv(f"/home/data/local/search_results/{key}.csv")

        all_results.append(results)

    all_results_df=pd.concat(all_results)
    all_results_df.to_excel("/home/data/local/search_results/all_keys.xlsx")

    timestr = time.strftime("%y-%m-%d_%H-%M")
    title =f"report_{timestr}"
    rep.upload_sheet(all_results_df, title)