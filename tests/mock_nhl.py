#!/usr/bin/python

import json
import os


class EndpointAdapter:
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
