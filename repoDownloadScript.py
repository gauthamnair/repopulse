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
	numRepoDownloaded += 1
	if not repo.fork:
		logging.info('%d storing %s' % (numRepoDownloaded, repo.full_name))
		try:
			gitModels.makeRepo(repo)
			gitModels.session.commit()
			successlog.write(repo.full_name + "\n")
		except Exception as err:
			logging.info(err.message)
			logging.exception("failure storing " + repo.full_name + "\n")
			failurelog.write(repo.full_name + "\n")


