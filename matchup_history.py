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

# testing with one week in one year - will loop through once complete
scoring_period_id = 1
season_id = 2015

# pull in raw data
espn_raw_data = clean.get_raw_data(
    LEAGUE_ID, espn_cookies, scoring_period_id, season_id)

# create dataframes
# Creating an updated DataFrame for matchups and roster data
df_matchups = clean.create_matchups(espn_raw_data)
df_roster = clean.create_roster(espn_raw_data)

df_roster.to_csv('csv_output/roster.csv')
