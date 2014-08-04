import gitImporter
import gitdb

import logging
logging.basicConfig(level=logging.INFO)

qstr = 'language:R stars:>1'

outlog = open('log.txt', "a")

for repo in gitImporter.importer.searchRepositories(qstr):
	if not repo.fork:
		logging.info('getting %s' % repo.full_name)
		try:
			gitdb.storeRepo(repo)
		except Exception as err:
			logging.info(err.message)
			outlog.write(repo.full_name)

# failed with:
# 'Only the first 1000 search results are available'