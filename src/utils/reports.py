import pygsheets
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import json

def authorize():
    creds_path="/home/credentials/client_secret.json"
    # creds_path="/home/credentials/sheets.googleapis.com-python.json"

    gc = pygsheets.authorize(client_secret=creds_path)
    with open("/home/credentials/credentials.json") as f:
        creds_dict=json.load(f)

    creds=Credentials.from_authorized_user_info(creds_dict)
    
    return gc, creds

def upload_sheet(df, title):
    gc, creds = authorize()

    sh=gc.create(title)
    file_id=sh.id

    wk1 = sh.sheet1
    wk1.set_dataframe(df, 'A1')

    drive = build('drive', 'v3', credentials=creds)
    folderId = '1EGDyuebNJp7Vuq5p44cXijuk_X9rzoAw'
    drive.files().update(fileId=file_id, addParents=folderId, removeParents='root').execute()