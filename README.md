# Fantasy Football League History - WORK IN PROGRESS
Export your matchup history to .csv for your ESPN fantasy football league using the API with python.
This project is currently working on previous seasons but please see disclaimer below for more information.

## Disclaimer
This project serves as a learning experience for me as an introduction to git.
Below is an list of repos from which I drew inspo and can better serve your purposes of accessing the ESPN API:
- [cwendt94/espn-api](https://github.com/cwendt94/espn-api)
- [rbarton65/espnff](https://github.com/rbarton65/espnff)
- [Jman4190/espn-ff-api](https://github.com/Jman4190/espn-ff-api)
- [dtcarls/fantasy_football_chat_bot](https://github.com/dtcarls/fantasy_football_chat_bot)

## Usage
See this post by [Jman4190](https://jman4190.medium.com/how-to-use-python-with-the-espn-fantasy-draft-api-ecde38621b1b) to understand how to access your `LEAGUE_ID`, `SWID_COOKIES`, and `ESPN_S2_COOKIES` from ESPN.

Create a `.env` file and add the following:
*(don't forget to add `.env` to your `.gitignore` file)*
```
LEAGUE_ID=YOU_LEAGUE_ID_HERE
SWID_COOKIES=YOUR_SWID_COOKIE_HERE
ESPN_S2_COOKIES=YOUR_ESPN_S2_COOKIE_HERE
```

Update `matchup_history.py` with the seasons that you would like exported to .csv.

*Note: I will continute to play with this script for practice but would highly recommend using one of the repos mentioned above for ESPN Fantasy API.*