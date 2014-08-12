import gitImporter
import gitModels
import logging
import datetime
logging.basicConfig(level=logging.INFO)


session = gitModels.session
importer = gitImporter.importer

started = datetime.datetime.today()

repoString = 'hadley/plyr'
pyGithubRepo = importer.getRepo(repoString)
weeklyContributions = importer.getWeeklyContributions(pyGithubRepo)
gitModels.storeWeeklyContributions(weeklyContributions, 
	repo_full_name = repoString)
session.commit()
