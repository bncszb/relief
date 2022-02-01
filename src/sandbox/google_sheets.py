import pygsheets
import pandas as pd

# Use customized credentials 
creds_path="/Users/benceszabo/Side/relief/client_secret.json"
gc = pygsheets.authorize(client_secret=creds_path)

sh=gc.open("test")

counties=pd.read_excel("/Users/benceszabo/Side/relief/data/local/counties.xlsx")
wk1 = sh.sheet1

wk1.set_dataframe(counties, 'A50')