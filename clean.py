import requests
import pandas as pd

# create matchups dataframe for the entire season


def create_matchups(league_id, espn_cookies, season):
    json_data = get_raw_data(league_id, espn_cookies, 1,  season)
    matchups_list = []

    for record in json_data:
        if 'schedule' in record:
            for matchup_number, matchups in enumerate(record['schedule'], start=1):
                # Extracting matchup data (winner, loser, points for home and away teams, and other fields)
                winner = matchups.get('winner', None)
                home_teamId = matchups.get('home', {}).get('teamId', None)
                away_teamId = matchups.get('away', {}).get('teamId', None)
                winner_teamId = home_teamId if winner == 'HOME' else away_teamId if winner == 'AWAY' else None

                matchup_data = {
                    'matchup': matchup_number,
                    'playoffTierType': matchups.get('playoffTierType', None),
                    'winner': winner_teamId,
                    'home_teamId': home_teamId,
                    'home_points': matchups.get('home', {}).get('totalPoints', None),
                    'home_tiebreak': matchups.get('home', {}).get('tiebreak', None),
                    'away_teamId': away_teamId,
                    'away_points': matchups.get('away', {}).get('totalPoints', None),
                    'away_tiebreak': matchups.get('away', {}).get('tiebreak', None),
                    'week_number': matchups.get('matchupPeriodId', None),
                    'year': record.get('seasonId', None)
                }
                matchups_list.append(matchup_data)

    df_matchups_updated = pd.DataFrame(matchups_list)

    # Extracting the 'teams' key and converting it into a pandas DataFrame
    teams_df = None
    for record in json_data:
        if 'teams' in record:
            teams_df = pd.json_normalize(record['teams'])

    # Selecting the desired columns from the teams DataFrame
    selected_columns_teams = [
        'abbrev', 'id', 'location', 'logo', 'name', 'nickname', 'owners', 'primaryOwner', 'rankCalculatedFinal', 'waiverRank'
    ]
    winner_columns_teams = [
        'abbrev', 'id', 'name', 'primaryOwner'
    ]
    # home column names
    home_column_names = {item: 'home_' +
                         item for item in selected_columns_teams}
    # away column names
    away_column_names = {item: 'away_' +
                         item for item in selected_columns_teams}
    # winner column names
    winner_column_names = {item: 'winner_' +
                           item for item in winner_columns_teams}

    teams_df_refined = teams_df[selected_columns_teams]

    # merge winner and rename columns
    df_roster_final = df_matchups_updated.merge(
        teams_df_refined, how='left', left_on='winner', right_on='id')
    df_roster_final = df_roster_final.rename(columns=winner_column_names)

    # merge home team and rename columns
    df_roster_final = df_roster_final.merge(
        teams_df_refined, how='left', left_on='home_teamId', right_on='id')

    df_roster_final = df_roster_final.rename(columns=home_column_names)

    # merge away team and rename columns
    df_roster_final = df_roster_final.merge(
        teams_df_refined, how='left', left_on='away_teamId', right_on='id')

    df_roster_final = df_roster_final.rename(columns=away_column_names)

    return df_roster_final

# create roster dataframe for one week


def create_roster(league_id, espn_cookies, period, season):
    json_data = get_raw_data(league_id, espn_cookies, period, season)
    roster_list = []

    for record in json_data:
        if 'schedule' in record:
            for matchup_number, matchups in enumerate(record['schedule'], start=1):
                # Extracting roster data for both home and away teams
                for loc in ['home', 'away']:
                    if loc in matchups and 'rosterForMatchupPeriod' in matchups[loc]:
                        roster_data = matchups[loc]['rosterForMatchupPeriod']['entries']
                        df_roster = pd.json_normalize(roster_data, sep='_')
                        df_roster['matchup'] = matchup_number
                        df_roster['location'] = loc
                        df_roster['teamId'] = matchups[loc].get('teamId', None)
                        df_roster['week_number'] = matchups.get(
                            'matchupPeriodId', None)
                        df_roster['year'] = record.get('seasonId', None)
                        roster_list.append(df_roster)

    df_roster = pd.concat(roster_list, ignore_index=True)

    # Re-selecting and renaming columns in the roster DataFrame based on user's requirements
    selected_columns = {
        'injuryStatus': 'injuryStatus',
        'status': 'status',
        'playerPoolEntry_player_active': 'active',
        'playerPoolEntry_player_defaultPositionId': 'positionId',
        'playerPoolEntry_player_firstName': 'playerFirstName',
        'playerPoolEntry_player_fullName': 'playerFullName',
        'playerPoolEntry_player_injured': 'injured',
        'playerPoolEntry_player_lastName': 'playerLastName',
        'location': 'location',
        'teamId': 'teamId',
        'week_number': 'week_number',
        'year': 'year'
    }

    # Create a refined roster DataFrame based on the selected columns
    df_roster_refined = df_roster[list(selected_columns.keys())].rename(
        columns=selected_columns)

    # Manually creating the position key DataFrame
    position_key_data = {
        'positionId': [1, 2, 3, 4, 5, 16],
        'position': ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST'],
        'position_long': ['quarterback', 'running back', 'wide receiver', 'tight end', 'kicker', 'defense']}

    position_key_df = pd.DataFrame(position_key_data)

    # Merging the roster DataFrame with the manually created position key DataFrame based on positionID
    df_roster_refined = df_roster_refined.merge(
        position_key_df, on='positionId', how='left')

    # Extracting the 'teams' key and converting it into a pandas DataFrame
    teams_df = None
    for record in json_data:
        if 'teams' in record:
            teams_df = pd.json_normalize(record['teams'])

    # Selecting the desired columns from the teams DataFrame
    selected_columns_teams = [
        'abbrev', 'id', 'location', 'logo', 'name', 'nickname', 'owners', 'primaryOwner', 'rankCalculatedFinal', 'waiverRank'
    ]
    teams_df_refined = teams_df[selected_columns_teams]
    df_roster_final = df_roster_refined.merge(
        teams_df_refined, how='left', left_on='teamId', right_on='id')

    return df_roster_final

# calls api and returns the raw data in JSON format


def get_raw_data(league_id, espn_cookies, period, season):
    # headers
    headers = headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }
    # API pulled from the ispection of the histrical page
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/leagueHistory/{}?scoringPeriodId={}&view=modular&view=mNav&view=mMatchupScore&view=mScoreboard&view=mSettings&view=mTopPerformers&view=mTeam&seasonId={}".format(
        league_id, period, season)

    # Get function to pull in the API, passing headers and cookies
    r = requests.get(url, headers=headers, cookies=espn_cookies)
    espn_raw_data = r.json()

    return espn_raw_data
