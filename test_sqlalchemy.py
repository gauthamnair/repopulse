import gitModels
from gitImporter import importer
import datetime

import logging
logging.basicConfig(level=logging.INFO)

plyr = importer.getRepo('hadley/plyr')


# stored = gitModels.makeRepo(plyr)

# fromdb = gitModels.session.query(gitModels.Repo).first()

# assert(fromdb.full_name == stored.full_name)
# gitModels.session.commit()


weeklyContributions = plyr.get_stats_contributors()

contributor = weeklyContributions[-1]
author_login = contributor.author.login
repo_full_name = plyr.full_name
weeks = [week for week in contributor.raw_data['weeks'] if week['c'] > 0]

for week in weeks:
	wm = gitModels.WeeklyContribution(
		author_login=author_login,
		repo_full_name=repo_full_name,
		week_start=datetime.datetime.fromtimestamp(week['w']),
		commits_num = week['c'],
		additions_num = week['a'],
		deletions_num = week['d']
	)
	gitModels.session.add(wm)

gitModels.session.commit()