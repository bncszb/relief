from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

def search_URLs_df(URL_df):
    # turn off a few things to make scapring faster
    #     options.experimental_options["prefs"] = { 
    #     "profile.managed_default_content_settings.images": 2, 
    #     "profile.managed_default_content_settings.stylesheets": 2, 
    #     "profile.managed_default_content_settings.javascript": 2, 
    #     "profile.managed_default_content_settings.cookies": 2, 
    #     "profile.managed_default_content_settings.geolocation": 2, 
    #     "profile.default_content_setting_values.notifications": 2, 
    # }

    print("Creating driver...")

    opts = Options()
    prefs = {
        'profile.managed_default_content_settings.images':2,
        'disk-cache-size': 4096,
        
    }
    # opts.add_argument("--user-data-dir=/home/chrome_cache")
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--headless")
    # driver = webdriver.Remote(command_executor='http://localhost:4444', options=opts)
    driver = webdriver.Remote(command_executor='http://chrome:4444', options=opts)

    res=[]

    for i in URL_df.index:

        URL = URL_df["url"].iloc[i]
        region = URL_df["region"].iloc[i]

        print(f"Getting url: {URL}...")
        driver.get(URL)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,"/html/body/app-root/app-base/app-search/section/div/div/div[3]/app-article-card[1]/article/div/div[2]/a/h2"))
            )
            results_df=check_URL(driver)
            results_df["region"]=region

            res.append(results_df)
        except:
            Exception(f"{URL} not loaded!")


    all_results_df=pd.concat(res)

    driver.close()
    driver.quit()
    return all_results_df


def search_URL(URL):

    print("Creating driver...")
    driver = webdriver.Remote(command_executor='http://chrome:4444')
    
    print("Getting url...")
    driver.get(URL)
    time.sleep(1)

    results_df=check_URL(driver)


    driver.close()
    driver.quit()
    return results_df

def search_URLs(URLs):

    print("Creating driver...")
    driver = webdriver.Remote(command_executor='http://chrome:4444')

    res=[]

    for URL in URLs:

        print("Getting url...")
        driver.get(URL)
        time.sleep(1)

        results_df=check_URL(driver)

        res.append(results_df)

    all_results_df=pd.concat(res)

    driver.close()
    driver.quit()
    return all_results_df


def check_URL(driver):

    columns=[
        "link",
        "date",
        "title"
        ]
    results_df=pd.DataFrame(columns=columns)

    results_section=driver.find_elements(By.CSS_SELECTOR,"div.results.ng-tns-c102-0")
    assert len(results_section)==1, "Result section not found at XPATH \nLink:{URL}"

    results_section=results_section[0]

    results=results_section.find_elements(By.CSS_SELECTOR,"div.article-block.ng-star-inserted")

    print(f"Results: {len(results)}")
    if len(results)==0:
        print("No results")
        return

    for result in results:
        title=result.find_element(By.CSS_SELECTOR,"h2.article-title").accessible_name
        link=result.find_element(By.CSS_SELECTOR,"a.article-link.ng-star-inserted").get_attribute("href")
        date=result.find_element(By.CSS_SELECTOR,"span.article-date").get_attribute("innerHTML")

        result_dict={
            "title": title,
            "link": link,
            "date": date
            }

        date=date.lower()

        if "órája" in date or "perce" in date or "tegnap" in date:
            print (date)
            print (link)


            results_df=results_df.append(result_dict,ignore_index=True)

        else:
            date_obj = datetime. strptime(date, '%Y.%m.%d. %H:%M')
        

            if datetime.now()-timedelta(days=1) < date_obj:
                print (date)
                print (link)
                results_df=results_df.append(result_dict,ignore_index=True)

    return results_df