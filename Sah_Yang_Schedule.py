import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe

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
sah_worksheet = sah_spreadsheet.worksheet("25/05")
sah_data = sah_worksheet.get("A1:E32")
sah_df = pd.DataFrame(sah_data)
sah_df.replace("", pd.NA, inplace=True)
sah_df.dropna(how='all', inplace=True)
sah_df.dropna(axis=1, how='all', inplace=True)
sah_df_ = sah_df[~(sah_df[2].isna() & sah_df[3].isna())]
sah_df_.fillna("시간 미정", inplace=True)
print(sah_df_)
