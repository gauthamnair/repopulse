import gitImporter
import gitModels

import logging
logging.basicConfig(level=logging.INFO)

failurelog = open('failures.txt', "w")
successlog = open('success.txt', "w")

importer = gitImporter.importer

qstr = 'language:Python stars:>9'
queryChunker = gitImporter.SearchQueryChunker(
	importer, qstr, daysInterval = 30)

numRepoDownloaded=0

for repo in queryChunker.search():
	if not repo.fork:
		logging.info('getting %s' % repo.full_name)
		try:
			gitModels.makeRepo(repo)
			gitModels.session.commit()
			successlog.write(repo.full_name)
		except Exception as err:
			logging.info(err.message)
			failurelog.write(repo.full_name)
			failurelog.write('error:' + err.message)


