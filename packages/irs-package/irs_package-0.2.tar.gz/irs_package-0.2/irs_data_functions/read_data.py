import pandas as pd
import numpy as np
import io
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Path to the downloaded credentials JSON file
credentials_path = '/Users/vedantrathi/Desktop/irs_api_credentials.json'
# Google Drive file ID of the CSV file
file_id_2020 = '1Gvfs55UqIqm_U_27wHes9Rp_WBO0pQfV'
file_id_2019 = '13oymfGzHOBRR9NasFmrz7i4ZW5XOPPRg'


# Authenticate using credentials
credentials = service_account.Credentials.from_service_account_file(
    credentials_path,
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)

# Build the Google Drive API service
drive_service = build('drive', 'v3', credentials=credentials)
# Download the CSV file data
request = drive_service.files().get_media(fileId=file_id_2020)
content = request.execute()

# Convert the content to a pandas DataFrame
df_2020 = pd.read_csv(io.StringIO(content.decode('utf-8')))
df_2020['Year'] = 2020
# print(df_2020.iloc[0])

request = drive_service.files().get_media(fileId=file_id_2019)
content = request.execute()

# Convert the content to a pandas DataFrame
df_2019 = pd.read_csv(io.StringIO(content.decode('utf-8')))
df_2019['Year'] = 2019
print(df_2019.iloc[0])

combined = [df_2019, df_2020]
df_irs_data = pd.concat(combined)
df_irs_data = df_irs_data.reset_index(drop=True)


def number_of_returns_by_state_and_year(state_code, year):
    """
    This function will output the number of returs given a state code and the year.
    """
    df_filtered = df_irs_data[(df_irs_data['STATE']==state_code) & (df_irs_data['Year']==year) & (df_irs_data['zipcode']==0)]
    return df_filtered['N1'].iloc[0]



"""final_df = pd.DataFrame()

for i in range(2020, 2021):
    file_id = f'file_id_{i}'
    request = drive_service.files().get_media(fileId=file_id)
    content = request.execute()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    df['Year'] = i
    final_df = final_df.append(df, ignore_index=True)
# Convert the content to a pandas DataFrame

print(final_df)"""
