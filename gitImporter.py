from github import Github
import os
import logging
import time
import datetime


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


class SearchQueryChunker:
	'''
		Used to turn repository search queries that return too many
		(>) results
		into smaller queries by chunking by repository date creation
	'''
	MAX_RESULTS = 999
	MIN_DATE = datetime.date(2000, 1, 1)

	def __init__(self, importer, query, daysInterval=30):
		self.query = query
		self.upper_date_limit = datetime.date.today()
		self.lower_date_limit = self.upper_date_limit - datetime.timedelta(days=daysInterval)
		self.daysInterval = float(daysInterval)
		self.importer = importer

	def getNumResultsInCurrentInterval(self):
		full_query = '%s created:%s..%s' % (self.query, self.lower_date_limit, self.upper_date_limit)
		logging.info('counting results for search ' + full_query)

		self.importer.waitForSearchLimitRefresh()
		searchPaginator = self.importer.g.search_repositories(query=full_query)
		return searchPaginator.totalCount

	def searchCurrentInterval(self):
		full_query = '%s created:%s..%s' % (self.query, self.lower_date_limit, self.upper_date_limit)
		logging.info('github search for ' + full_query)

		for repo in self.importer.searchRepositories(full_query):
			yield repo

	def search(self):
		while True:
			if self.getNumResultsInCurrentInterval() < self.MAX_RESULTS:
				for repo in self.searchCurrentInterval():
					yield repo
				if self.lower_date_limit < self.MIN_DATE:
					break
				self.daysInterval *= 2
				self.upper_date_limit = self.lower_date_limit - datetime.timedelta(days=1)
				self.lower_date_limit = self.upper_date_limit - datetime.timedelta(self.daysInterval)
			else:
				if self.daysInterval < 0.5:
					raise Exception("interval is just one day but still too many results")

				self.daysInterval *= 0.5
				self.lower_date_limit = self.upper_date_limit - datetime.timedelta(self.daysInterval)






mypw = os.environ['GITPASSWD']

importer = GitDataImporter(Github('gauthamnair', mypw))

importerNoAuth = GitDataImporter(Github())
