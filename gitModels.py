from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

import logging

logging.basicConfig(level=logging.INFO)

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
	
	size = Column(sa.Integer)
	forks_count = Column(sa.Integer)
	stargazers_count = Column(sa.Integer)
	subscribers_count = Column(sa.Integer)
	network_count = Column(sa.Integer)

	_specialGetterFromPyGithubObject = {
		'owner_login': lambda x: x.owner.login,
		'subscribers_count' : lambda x: x.raw_data['subscribers_count']
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
	theRepo = Repo(**kvpairs)
	session.add(theRepo)
	return theRepo


