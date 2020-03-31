#!/usb/bin/python

import datetime
import pickle


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
