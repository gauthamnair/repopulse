from gitImporter import importer

import logging
logging.basicConfig(level=logging.INFO)

def testPlyrCommits():
	plyr = importer.getRepo('hadley/plyr')
	commitsImporter = importer.getCommitsForRepo(plyr)
	commits = list(commitsImporter)
	print len(commits)
	return (plyr, commits)
	# should be at least 715


def testSearchForR2011():
	qstr = 'language:R created:"<= 2011-01-01"'
	repos = list(importer.searchRepositories(qstr))
	return repos