from nhl_scraper import nhl
import pandas as pd


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

scraper = nhl.Scraper()
box = scraper.box_score([2019020002])
