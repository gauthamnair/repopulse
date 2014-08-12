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


gitModels.cacheWeeklyContributions(weeklyContributions, 
	repo_full_name = repoString)
session.commit()



cached = gitModels.getOrClearCachedWeeklyData(repo_full_name=repoString)

baseQuery = session.query(gitModels.CachedWeeklyContribution)
query = baseQuery.filter(
	gitModels.CachedWeeklyContribution.repo_full_name == repoString)
weeks = query.all()