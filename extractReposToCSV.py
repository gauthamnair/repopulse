import gitModels
from collections import defaultdict
import pandas as pd

repos = gitModels.session.query(gitModels.Repo).all()

data = defaultdict(list)

for repo in repos:
	for key, value in repo.__dict__.items():
		if not key.startswith('_'):
			data[key] += [value]

for k, v in data.items():
	print k, ":", len(v)

data = pd.DataFrame(data)

data[['full_name', 'owner_login', 'stargazers_count']].to_csv('data/intermediate/infoRepos.csv')