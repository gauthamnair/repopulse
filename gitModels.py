from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
import datetime

import logging

# logging.basicConfig(level=logging.INFO)

engine = create_engine("mysql+pymysql://root:@localhost/gitdb", echo=True)
Base = declarative_base()

connection = engine.connect()
logging.info("Show tables:")
result = connection.execute("SHOW TABLES")
for row in result:
	logging.info("Found Table:")
	logging.info(row)


from sqlalchemy import Column

class Repo(Base):
	__tablename__ = 'Repos'
	id = Column(sa.Integer, primary_key=True)
	
	full_name = Column(sa.Unicode(1024))
	name = Column(sa.Unicode(1024))
	owner_login = Column(sa.Unicode(1024))

	fork = Column(sa.Boolean)
	has_wiki = Column(sa.Boolean)
	has_issues = Column(sa.Boolean)
	homepage = Column(sa.Unicode(1024))

	language = Column(sa.Unicode(1024))
	description = Column(sa.UnicodeText)
	created_at = Column(sa.DateTime)
	pushed_at = Column(sa.DateTime)

	downloaded_on = Column(sa.DateTime)
	
	size = Column(sa.Integer)
	forks_count = Column(sa.Integer)
	stargazers_count = Column(sa.Integer)
	subscribers_count = Column(sa.Integer)
	network_count = Column(sa.Integer)

	# turns out network_count and the true subscribers
	# count require github requests if starting from a repo
	# obtained from the search API. Making them null.
	# could fill them in later.
	_specialGetterFromPyGithubObject = {
		'owner_login': lambda x: x.owner.login,
		'subscribers_count' : lambda x: None,
		'network_count' : lambda x: None,
		'downloaded_on' : lambda x: datetime.datetime.today()
	}
	_doNotGetFromPyGithubObject = ['id']


class WeeklyContribution(Base):
	__tablename__ = 'WeeklyContributions'
	id = Column(sa.Integer, primary_key=True)
	author_login = Column(sa.Unicode(1024))
	repo_full_name = Column(sa.Unicode(1024))
	week_start = Column(sa.DateTime)
	commits_num = Column(sa.Integer)
	additions_num = Column(sa.Integer)
	deletions_num = Column(sa.Integer)

class CachedWeeklyContribution(Base):
	__tablename__ = 'CachedWeeklyContributions'

	id = Column(sa.Integer, primary_key=True)
	author_login = Column(sa.Unicode(1024))
	repo_full_name = Column(sa.Unicode(1024))
	week_start = Column(sa.DateTime)
	commits_num = Column(sa.Integer)
	additions_num = Column(sa.Integer)
	deletions_num = Column(sa.Integer)

	downloaded_on = Column(sa.DateTime)


Base.metadata.create_all(engine)


sessionMaker = sa.orm.sessionmaker(bind=engine)
session = sessionMaker()


def extractKVPairsForModel(Model, pyGithubObject):
	columnNames = Model.__table__.columns.keys()
	kvpairs = dict()
	for colName in columnNames:
		if colName in Model._doNotGetFromPyGithubObject:
			continue;
		else:
			if colName in Model._specialGetterFromPyGithubObject:
				getter = Model._specialGetterFromPyGithubObject[colName]
				value = getter(pyGithubObject)
			else:
				value = getattr(pyGithubObject, colName)
			kvpairs[colName] = value
	return kvpairs


def makeRepo(pyGithubRepo):
	kvpairs = extractKVPairsForModel(Repo, pyGithubRepo)
	
	full_name = pyGithubRepo.full_name
	
	existingRepo = session.query(Repo).filter_by(full_name=full_name).first()
	if existingRepo:
		logging.info("A repo %s already exists. ignoring insert and returning existing", full_name)
		return existingRepo
	else:
		theRepo = Repo(**kvpairs)
		session.add(theRepo)
		return theRepo


def storeWeeklyContributions(weeklyContributions, repo_full_name):
	for contributor in weeklyContributions:
		author_login = contributor.author.login
		weeks = [week for week in contributor.raw_data['weeks'] if week['c'] > 0]

		for week in weeks:
			wm = WeeklyContribution(
				author_login=author_login,
				repo_full_name=repo_full_name,
				week_start=datetime.datetime.fromtimestamp(week['w']),
				commits_num = week['c'],
				additions_num = week['a'],
				deletions_num = week['d']
			)
			session.add(wm)

def cacheWeeklyContributions(weeklyContributions, repo_full_name):
	downloaded_on = datetime.datetime.today()

	for contributor in weeklyContributions:
		author_login = contributor.author.login
		weeks = [week for week in contributor.raw_data['weeks'] if week['c'] > 0]

		for week in weeks:
			wm = CachedWeeklyContribution(
				author_login=author_login,
				repo_full_name=repo_full_name,
				week_start=datetime.datetime.fromtimestamp(week['w']),
				commits_num = week['c'],
				additions_num = week['a'],
				deletions_num = week['d'],
				downloaded_on = downloaded_on
			)
			session.add(wm)

def getOrClearCachedWeeklyData(repo_full_name):
	baseQuery = session.query(CachedWeeklyContribution)
	query = baseQuery.filter(
		CachedWeeklyContribution.repo_full_name == repo_full_name)
	weeks = query.all()

	if len(weeks) == 0:
		return weeks

	oldestAllowed = datetime.datetime.now() - datetime.timedelta(2)

	if any(week.downloaded_on < oldestAllowed for week in weeks):
		session.delete(weeks)
		session.commit()
		return []
	else:
		return weeks
