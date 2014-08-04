from gitImporter import importer
import gitModels

import logging
logging.basicConfig(level=logging.INFO)

qstr = 'language:R stars:>1'

outlog = open('log.txt', "w")

for repo in importer.searchRepositories(qstr):
	if not repo.fork:
		logging.info('getting %s' % repo.full_name)
		try:
			gitModels.makeRepo(repo)
			gitModels.session.commit()
		except Exception as err:
			logging.info(err.message)
			outlog.write(repo.full_name)

