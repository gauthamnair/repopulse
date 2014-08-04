from github import Github
import os
import logging
import time


class GitDataImporter:
	def __init__(self, githubObject):
		self.g = githubObject

	def getLimitRemaining(self):
		ratelimit = self.g.get_rate_limit()
		corelimit = ratelimit.raw_data['resources']['core']
		return corelimit['remaining']

	def getSearchLimitRemaining(self):
		ratelimit = self.g.get_rate_limit()
		searchimit = ratelimit.raw_data['resources']['search']
		return searchimit['remaining']

	def waitForAPILimitRefresh(self):
		while self.getLimitRemaining() == 0:
			logging.info('waiting a minute')
			time.sleep(60)

	def waitForSearchLimitRefresh(self):
		while self.getSearchLimitRemaining() == 0:
			logging.info('waiting for search api limit')
			time.sleep(10)

	def getRepo(self, argsToGetRepo):
		self.waitForAPILimitRefresh()
		return self.g.get_repo(argsToGetRepo)

	def getCommitsForRepo(self, repo):
		logging.info('grabbing commits for repo %s' % repo.name)
		commitPaginator = repo.get_commits()
		currentPageNumber = 0
		while True:
			self.waitForAPILimitRefresh()
			logging.info('requesting page %d of commits' % currentPageNumber)
			pageContents = commitPaginator.get_page(currentPageNumber)
			if len(pageContents) == 0:
				break
			else:
				for item in pageContents:
					yield item
			currentPageNumber += 1

	def searchRepositories(self, query):
		self.waitForSearchLimitRefresh()
		searchPaginator = self.g.search_repositories(query=query)
		currentPageNumber = 0
		while True:
			self.waitForSearchLimitRefresh()
			logging.info('requesting page %d of searchResults' % currentPageNumber)
			pageContents = searchPaginator.get_page(currentPageNumber)
			if len(pageContents) == 0:
				break
			else:
				for item in pageContents:
					yield item
			currentPageNumber += 1


mypw = os.environ['GITPASSWD']

importer = GitDataImporter(Github('gauthamnair', mypw))

importerNoAuth = GitDataImporter(Github())