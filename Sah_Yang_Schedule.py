import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe

def Sah_filtered_dataframe():
    SERVICE_ACCOUNT_FILE = "flowerbot-13-5d93422fd7b6.json"
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    sah_spreadsheet = client.open_by_key("1mrlJEDjfNPkJnnQwFdpmli4SySIva2rOzyhvqqD2n6o")
    sah_worksheet = sah_spreadsheet.worksheet("25/08")
    sah_data = sah_worksheet.get("A1:E50")
    sah_df = pd.DataFrame(sah_data)
    sah_df.replace("", pd.NA, inplace=True)
    sah_df.dropna(how='all', inplace=True)
    sah_df.dropna(axis=1, how='all', inplace=True)
    sah_df.columns = sah_df.iloc[0]
    sah_df = sah_df[1:].reset_index(drop=True)
    sah_df = sah_df[~sah_df["컨텐츠"].str.contains("미정|휴방", na=False)].copy()
    sah_df.fillna("시간 미정", inplace=True)

    return sah_df
