#!/usb/bin/python

import datetime
import pickle

import json
import os
from nhl_scraper import nhl
import tests.mock_nhl as mock_nhl
import datetime
import pytest

def test_teams(nhl_scraper):
    df = nhl_scraper.teams()
    print(df)
    assert(len(df.index) == 31)
    assert(df[df.abbrev == 'TOR'].iloc(0)[0]['name'] == 'Maple Leafs')
    assert(df[df.city == 'San Jose'].iloc(0)[0]['name'] == 'Sharks')
    assert(df[df.city == 'Vegas'].iloc(0)[0]['id'] == 54)


def test_schedule_one_day(nhl_scraper):
    dc = nhl_scraper.games_count(datetime.datetime(2018, 1, 14),
                                 datetime.datetime(2018, 1, 14))
    print(dc)
    assert(len(dc) == 8)
    assert(dc[17] == 1)
    assert(dc[15] == 0)


def test_schedule_multi_day(nhl_scraper):
    dc = nhl_scraper.games_count(datetime.datetime(2018, 1, 14),
                                 datetime.datetime(2018, 1, 16))
    print(dc)
    assert(len(dc) == 18)
    assert(dc[17] == 2)
    assert(dc[3] == 2)
    assert(dc[11] == 0)


def test_players(nhl_scraper):
    df = nhl_scraper.players()
    print(df)
    assert(df[df["name"] == "Jason Spezza"].iloc(0)[0]["teamId"] == 10)


def test_pickle(nhl_scraper):
    dc = nhl_scraper.games_count(datetime.datetime(2018, 1, 14),
                                 datetime.datetime(2018, 1, 16))
    tmp = pickle.dumps(dc)
    new_dc = pickle.loads(tmp)
    assert(new_dc[17] == 2)
    assert(new_dc[11] == 0)

@pytest.fixture
def nhl_scraper():
    s = nhl.Scraper()

    # Put the mock adapter in so we don't make calls out
    mock = mock_nhl.MockNhlEndpointAdapter()

    cached_dates = [datetime.datetime(2018, 1, 14),
                    datetime.datetime(2018, 1, 15),
                    datetime.datetime(2018, 1, 16)]
    for cached_date in cached_dates:
        mock.add_date(cached_date)

    s.set_endpoint_adapter(mock)
    return s



class MockNhlEndpointAdapter:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.schedule_cache = {}
        self.players_cache = None

    def teams_endpoint(self):
        fn = "sample.nhl.teams.json"
        with open(self.dir_path + "/" + fn, "r") as f:
            return json.load(f)

    def schedule_endpoint(self, date):
        if date in self.schedule_cache:
            return self.schedule_cache[date]
        else:
            raise RuntimeError("{} is not in the schedule cache".format(date))

    def add_date(self, date):
        ds = date.strftime("%Y%m%d")
        fn = "sample.nhl.schedule.{}.json".format(ds)
        with open(self.dir_path + "/" + fn, "r") as f:
            self.schedule_cache[date] = json.load(f)

    def players_endpoint(self, team_ids):
        if self.players_cache is None:
            fn = "sample.nhl.players.json"
            with open(self.dir_path + "/" + fn, "r") as f:
                self.players_cache = json.load(f)
        return self.players_cache


