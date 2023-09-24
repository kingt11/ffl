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


# Creating an dataFrame for matchups for one season
df_matchups = clean.create_matchups(LEAGUE_ID, espn_cookies, 2015)

# Creating an dataFrame for roster for one season
roster_season = []
for i in range(1, 17):
    df = clean.create_roster(LEAGUE_ID, espn_cookies, i, 2015)
    roster_season.append(df)

df_roster_season = pd.concat(roster_season, ignore_index=True)
