import gitImporter
import gitModels
import logging
import datetime
logging.basicConfig(level=logging.INFO)

outlog = open('log.txt', "w")

session = gitModels.session
importer = gitImporter.importer

started = datetime.datetime.today()

for repo in session.query(gitModels.Repo):
	logging.info('getting activity for ' + repo.full_name)
	logging.info(datetime.datetime.today())
	pyGithubRepo = importer.getRepo(repo.full_name)
	weeklyContributions = importer.getWeeklyContributions(pyGithubRepo)
	gitModels.storeWeeklyContributions(weeklyContributions, repo.full_name)
	session.commit()

logging.info('finished')
logging.info(datetime.datetime.today())
logging.info('started')
logging.info(started)