from numpy import datetime_data
import pandas as pd
import utils.check_url as cu
import utils.url_generator as ug
import datetime
import time



if __name__=="__main__":
    print("Sleeping 10 seconds...")
    time.sleep(10)
    print("Starting scraping...")
    urls=ug.get_urls_for_keyword("gyurcsány")[:3]

    results=cu.search_URLs(urls)

    results.to_csv("output.csv")