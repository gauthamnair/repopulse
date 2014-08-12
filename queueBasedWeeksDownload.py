import gitImporter
import gitModels
import logging
import datetime
import time
logging.basicConfig(level=logging.ERROR)

outlog = open('log.txt', "w")

session = gitModels.session
importer = gitImporter.importer

started = datetime.datetime.today()


def weeklyDataIsAlreadyDownloaded(repo_full_name):
	rows = session.query(
		gitModels.WeeklyContribution
		).filter(
		gitModels.WeeklyContribution.repo_full_name == repo_full_name
		).count()
	return rows > 0


repologfile = open('repologfile.txt', "w")


class getWeeklyContributionsTask:
	maxFailures = 10

	def __init__(self, repo_full_name, taskid):
		self.repo_full_name = repo_full_name
		self.gotRepo = False
		self.gotWeeks = False
		self.done = False
		self.repo = None
		self.failures = 0
		self.id = taskid

	def do(self):
		if not self.gotRepo:
			try:
				self.getRepo()
				self.gotRepo = True
			except Exception:
				logging.exception('failed to get repo for ' + self.repo_full_name)
				self.failures += 1

		elif not self.gotWeeks:
			try:
				self.getWeeks()
				self.gotWeeks = True
				self.done = True
				repologfile.write('%d Success: %s\n' % (self.id, self.repo_full_name))
			except Exception:
				logging.exception('failed to get weeks for ' + self.repo_full_name)
				self.failures += 1

		if self.failures > self.maxFailures:
			repologfile.write('%d Failed: %s\n' % (self.id, self.repo_full_name))
			self.done = True


	def getRepo(self):
		self.repo = importer.getRepo(self.repo_full_name)

	def getWeeks(self):
		weeklyContributions = importer.getWeeklyContributions(self.repo)
		if weeklyContributions == None:
			raise Exception
		else:
			gitModels.storeWeeklyContributions(weeklyContributions, self.repo_full_name)
			session.commit()


class TaskQueue:
	def __init__(self, maxSize=5):
		self.maxSize = maxSize
		self.queue = list()

	def addTask(self, task):
		self.queue.append(task)

	def work(self):
		task = self.queue.pop(0)
		task.do()
		if task.done:
			return
		else:
			self.addTask(task)

	def isEmpty(self):
		return len(self.queue) == 0

	def isFull(self):
		return len(self.queue) == self.maxSize



taskQueue = TaskQueue()
taskid = 0

for repo in session.query(gitModels.Repo):
	while taskQueue.isFull():
		taskQueue.work()
		time.sleep(0.5)

	taskid += 1
	if not weeklyDataIsAlreadyDownloaded(repo.full_name):
		newTask = getWeeklyContributionsTask(repo.full_name, taskid=taskid)
		taskQueue.addTask(newTask)
	else:
		repologfile.write('%d Ignored: %s\n' % (taskid, repo.full_name))

while not taskQueue.isEmpty():
	taskQueue.work()
	time.sleep(1)

repologfile.close()

# logging.info('finished')
# logging.info(datetime.datetime.today())
# logging.info('started')
# logging.info(started)