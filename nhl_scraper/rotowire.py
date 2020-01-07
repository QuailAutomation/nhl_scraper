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
    goalies_cache = None
    def __init__(self):
        self.ea = EndpointAdapter()


    def starting_goalies(self):
        """Returns the full list of all players in the NHL.

        Each player is returned with their teamID and playerID.

        :return: All players
        :rtype: pandas.DataFrame
        """
        if Scraper.goalies_cache is None:
            Scraper.goalies_cache = self.ea.starting_goalies_endpoint()
        today = date.today()
        soup = BeautifulSoup(Scraper.goalies_cache, 'html.parser')
        starter_data = soup.findAll("div", {'class': 'starters-matrix'})
        tds = starter_data[0].findAll("div", {'class': 'flex-row'})
        searchable_data = []

        for i in range(1, len(tds)):
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
                            searchable_data.append([today + timedelta(days=day_index),goalie_name,opponent,status])

        return_value = pd.DataFrame(searchable_data,columns=['date', 'goalie_name', 'opponent_team', 'starting_status'])
        return_value.set_index('goalie_name', inplace=True)
        return_value.sort_index(inplace=True)
        return return_value

if __name__ == "__main__":
    scraper = Scraper()
    goalies = scraper.starting_goalies()
    pass