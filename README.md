# relief

A Streamlit application created and maintained by the volunteers, who work for the Disaster Relief Department of the Hungarian Charity Service of the Order of Malta.  

This project is an ever-evolving collection of features to help the department during both in peacetime and in events like the Russo-Ukrainian War or Covid19. 

## Features:
### News
A Scrapy solution to get search results for a certain keyword in the news portals of Hungarian counties. Results are saved in a sqlite database and visualized in the application. The search itself is executed by the search engine of the site, so there is no unneccessary traffic.
### Rain

### Shelter
This page is for finding contact infos in a certain range around a settlement.
- Contacts for the local councils and mayors are scraped from [this](http://xn--tosz-5qa.hu/szolgaltatasaink/onkormanyzati-adatbazis/?telepules=) governmental site. 
- School contacts are filtered from the regularly updated dataframe published [here](https://dari.oktatas.hu/), under 'Működő köznevelési feladatellátási helyek listája'.
