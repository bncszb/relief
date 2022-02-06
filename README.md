# relief

TODO
Docker:
- Selenium:
    - chromedriver

Schedule:
- crontab: 
    - https://stackoverflow.com/questions/34753831/execute-a-shell-script-everyday-at-specific-time
    - https://www.baeldung.com/linux/schedule-script-execution
        
Report:
- sending files with python:
    - https://stackoverflow.com/questions/3362600/how-to-send-email-attachments
    - https://www.tutorialspoint.com/send-mail-with-attachment-from-your-gmail-account-using-python
- drive:
    - https://medium.com/@ammar.nomany.tanvir/read-write-update-drive-excel-file-with-pydrive-f63134120ff9
    - https://stackoverflow.com/questions/58107431/how-to-create-a-sheet-under-a-specific-folder-with-google-api-for-python 
- format:
    - pandas merge rows to list https://www.geeksforgeeks.org/how-to-group-dataframe-rows-into-list-in-pandas-groupby/


Selenium: 
- webdriver service: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
- make things faster: https://seleniumjava.com/2015/12/12/how-to-make-selenium-webdriver-scripts-faster/
    - waits https://selenium-python.readthedocs.io/waits.html
- parallel:
    - https://vigneshgig.medium.com/parallel-scraping-of-dynamic-website-using-selenium-9a7abed0af45
    - https://testdriven.io/blog/concurrent-web-scraping-with-selenium-grid-and-docker-swarm/
- cache (and a bit of parallel):
    - https://stackoverflow.com/questions/57591594/load-cache-on-all-application-servers-using-selenium
    - https://sqa.stackexchange.com/questions/45933/how-do-i-enable-chromedriver-to-use-browser-cache-or-local-storage-with-selenium
- questions:
    - are these drivers automatically headless?

Solved problems:
- docker-compose up not working on remote
    - docker build --no-cache --network host -t bence_seach docker
    - --network host was needed 

- cron:
    - have to change directory or give full path
    - had to find out WHICH docker-compose I am using and use full name in sh file
    - * 9,14 * * * cd /horanszky/bigdb/bence/relief && ./uok.sh
