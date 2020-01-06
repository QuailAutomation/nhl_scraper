#https://www.rotowire.com/hockey/starting-goalies.php?view=teams

import objectpath
import requests
import json
from datetime import date,timedelta
import pandas as pd


from bs4 import BeautifulSoup


class EndpointAdapter:
    ROTOWIRE_URL = "https://www.rotowire.com/hockey"

    def get(self, api):
        """Send an API request to the URI and return the response as JSON

        :param api: API to call
        :type uri: str
        :return: JSON document of the reponse
        :raises: RuntimeError if any response comes back with an error
        """
        response = requests.get("{}/{}".format(self.ROTOWIRE_URL, api))
        return response.text

    def starting_goalies_endpoint(self):
        return self.get("starting-goalies.php?view=teams")


class Scraper:
    def __init__(self):
        self.ea = EndpointAdapter()
        self.goalies_cache = None

    def starting_goalies(self):
        """Returns the full list of all players in the NHL.

        Each player is returned with their teamID and playerID.

        :return: All players
        :rtype: pandas.DataFrame
        """
        if self.goalies_cache is None:
            # team_df = self.starting_goalies()
            self.goalies_cache = self.ea.starting_goalies_endpoint()
        today = date.today()
        soup = BeautifulSoup(self.goalies_cache, 'html.parser')
        starter_data = soup.findAll("div", {'class': 'starters-matrix'})
        tds = starter_data[0].findAll("div", {'class': 'flex-row'})
        searchable_data = {}
        for i in range(1, len(tds)):
            team = tds[i].find('div', {'class': 'proj-team'}).text.strip()
            team_info = {}
            searchable_data[team] = team_info
            days = tds[i].findAll('div', {'class': 'goalies-row'})
            for week_index in range(0,len(days)):
                each_day = days[week_index].findAll('div', {'class': 'goalie-item'})
                for day_index in range(0,len(each_day)):
                    day = each_day[day_index]

                    for day_num, child in enumerate(day.children):
                        if not isinstance(child,str) :
                            # we have a game
                            goalie_name = child.find('a').text
                            game_info = child.findAll('div', {'class': 'sm-text'})
                            opponent = game_info[0].text[-3:]
                            status = game_info[1].text
                            team_info[today + timedelta(days=day_index)] = {'goalie_name': goalie_name, 'opponent': opponent, 'status': status}

            # row = tds[i].find tds[i].get('class') == ['attrLabels']:
            #     key = tds[i].text.strip().strip(":")
            #     value = tds[i + 1].span.text
            #     searchable_data[key] = value
        columns = ["opponent", "date", "goalie_name", "status"]
        # return_value = pd.DataFrame(searchable_data.items(),columns=columns)
        return_value = pd.concat({k: pd.DataFrame(v).T for k, v in searchable_data.items()}, axis=0)
        # all_players = []
        # for team in self.players_cache["teams"]:
        #     team_id = team["id"]
        #     for plyr in team["roster"]["roster"]:
        #         player_id = plyr["person"]["id"]
        #         player_name = plyr["person"]["fullName"]
        #         position = plyr["position"]["abbreviation"]
        #         all_players.append({columns[0]: team_id,
        #                             columns[1]: player_id,
        #                             columns[2]: player_name,
        #                             columns[3]: position})
        # return pd.DataFrame(data=all_players, columns=columns)
        return return_value

if __name__ == "__main__":
    scraper = Scraper()
    goalies = scraper.starting_goalies()
    pass