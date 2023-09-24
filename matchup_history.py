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
df_matchups_season = clean.create_matchups(LEAGUE_ID, espn_cookies, 2018)

# Creating an dataFrame for roster for one season
roster_season = []
for i in range(1, 17):
    df = clean.create_roster(LEAGUE_ID, espn_cookies, i, 2018)
    roster_season.append(df)

df_roster_season = pd.concat(roster_season, ignore_index=True)

# Export to csv
df_matchups_season.to_csv('csv_output/matchups_2018.csv')
df_roster_season.to_csv('csv_output/rosters_2018.csv')


# Initialize empty lists to store the dataframes for matchups and rosters across all seasons
# all_matchups = []
# all_rosters = []

# for season in seasons:
# Creating a DataFrame for matchups for the current season
#    df_matchups = clean.create_matchups(LEAGUE_ID, espn_cookies, season)
#    all_matchups.append(df_matchups)

# Creating a DataFrame for roster for the current season
#   roster_season = []
#    for i in range(1, 17):
#        df = clean.create_roster(LEAGUE_ID, espn_cookies, i, season)
#        roster_season.append(df)
#    df_roster_season = pd.concat(roster_season, ignore_index=True)
#    all_rosters.append(df_roster_season)

# Concatenate all the dataframes across seasons for matchups and rosters
# df_all_matchups = pd.concat(all_matchups, ignore_index=True)
# df_all_rosters = pd.concat(all_rosters, ignore_index=True)

# df_all_matchups.to_csv('csv_output/matchups_full_history.csv')
# df_all_rosters.to_csv('csv_output/rosters_full_history.csv')
