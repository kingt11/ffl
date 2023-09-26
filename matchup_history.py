import requests
import pandas as pd
import os
from dotenv import load_dotenv
import clean

load_dotenv()

# load environment variables
LEAGUE_ID = os.getenv('LEAGUE_ID')
SWID_COOKIES = os.getenv('SWID_COOKIES')
ESPN_S2_COOKIES = os.getenv('ESPN_S2_COOKIES')

# dictionary for cookies
espn_cookies = {'swid': SWID_COOKIES,
                'espn_s2': ESPN_S2_COOKIES}


seasons = [
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
    2022
]

# Creating an dataFrame for matchups for one season
matchups_full = []
for season in seasons:
    df_matchups = clean.create_matchups(LEAGUE_ID, espn_cookies, season)
    matchups_full.append(df_matchups)

df_matchups_season = pd.concat(matchups_full, ignore_index=True)

# Export to csv
df_matchups_season.to_csv('csv_output/matchups_historical.csv')
