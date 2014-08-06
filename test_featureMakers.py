from featureMakers import *
import pandas as pd
import datetime

import pymysql as mdb
con = mdb.connect('localhost', 'root', '', 'gitdb');

query = "SELECT * FROM WeeklyContributions"
contrib = pd.io.sql.read_sql(query, con)
contrib.index = contrib['week_start']

query = "SELECT full_name, created_at, downloaded_on, language FROM Repos"
repos = pd.io.sql.read_sql(query, con)