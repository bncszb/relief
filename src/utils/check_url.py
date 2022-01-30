from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

def search_URLs_df(URL_df):

    print("Creating driver...")
    driver = webdriver.Remote(command_executor='http://chrome:4444')

    res=[]

    for i in URL_df.index:

        URL = URL_df["url"].iloc[i]
        area = URL_df["area"].iloc[i]

        print("Getting url...")
        driver.get(URL)
        time.sleep(1)

        results_df=check_URL(driver)
        results_df["area"]=area

        res.append(results_df)

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
        driver.close()
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