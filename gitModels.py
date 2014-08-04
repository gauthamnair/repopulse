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
	
	full_name = Column(sa.String(1024))
	name = Column(sa.String(1024))
	owner_login = Column(sa.String(1024))

	fork = Column(sa.Boolean)
	has_wiki = Column(sa.Boolean)
	has_issues = Column(sa.Boolean)
	homepage = Column(sa.String(1024))

	language = Column(sa.String(1024))
	description = Column(sa.Text)
	created_at = Column(sa.DateTime)
	pushed_at = Column(sa.DateTime)
	
	size = Column(sa.Integer)
	forks_count = Column(sa.Integer)
	stargazers_count = Column(sa.Integer)

	_specialGetterFromPyGithubObject = {
		'owner_login': lambda x: x.owner.login
	}
	_doNotGetFromPyGithubObject = ['id']


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


