#!/usr/bin/python

import pytest
from nhl_scraper import nhl
import mock_nhl
import datetime
    

@pytest.fixture
def nhl_scraper():
    s = nhl.Scraper()

    # Put the mock adapter in so we don't make calls out
    mock = mock_nhl.EndpointAdapter()

    cached_dates = [datetime.datetime(2018, 1, 14),
                    datetime.datetime(2018, 1, 15),
                    datetime.datetime(2018, 1, 16)]
    for cached_date in cached_dates:
        mock.add_date(cached_date)

    s.set_endpoint_adapter(mock)
    yield s
