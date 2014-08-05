import gitImporter
import gitModels

import logging
logging.basicConfig(level=logging.INFO)

outlog = open('log.txt', "w")

importer = gitImporter.importer

qstr = 'language:R stars:>1'
queryChunker = gitImporter.SearchQueryChunker(
	importer, qstr, daysInterval = 30)


for repo in queryChunker.search():
	if not repo.fork:
		logging.info('getting %s' % repo.full_name)
		try:
			gitModels.makeRepo(repo)
			gitModels.session.commit()
		except Exception as err:
			logging.info(err.message)
			outlog.write(repo.full_name)


