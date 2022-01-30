import pandas as pd
from utils.check_url import check_URL

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

url="https://www.baon.hu/kereses?global_filter=gyurcs%C3%A1ny"


check_URL(url)