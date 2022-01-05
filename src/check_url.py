from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

def check_URL(URL):
    options = Options()
    options.headless = True

    #options=None
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",options=options)

    driver.get(URL)
    time.sleep(1)

    results_section=driver.find_elements(By.CSS_SELECTOR,"div.results.ng-tns-c101-0")
    assert len(results_section)==1, f"Result section not found at XPATH \nLink:{URL}"
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

        date=date.lower()

        if "órája" in date or "perce" in date or "tegnap" in date:
            print (date)
            print (link)

        else:
            date_obj = datetime. strptime(date, '%Y.%m.%d. %H:%M')
        

            if datetime.now()-timedelta(days=1) < date_obj:
                print (date)
                print (link)

    driver.close()
        
def check_URLs(URLs):
    options = Options()
    options.headless = True

    #options=None
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",options=options)

    for URL in URLs:
        
        driver.get(URL)
        time.sleep(1)

        results_section=driver.find_elements(By.CSS_SELECTOR,"div.results.ng-tns-c101-0")
        assert len(results_section)==1, f"Result section not found at XPATH \nLink:{URL}"
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

            date=date.lower()

            if "órája" in date or "perce" in date or "tegnap" in date:
                print (date)
                print (link)

            else:
                date_obj = datetime. strptime(date, '%Y.%m.%d. %H:%M')
            

                if datetime.now()-timedelta(days=1) < date_obj:
                    print (date)
                    print (link)

    driver.close()
        