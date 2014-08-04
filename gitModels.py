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


Base.metadata.create_all(engine)


sessionMaker = sa.orm.sessionmaker(bind=engine)
session = sessionMaker()

def makeRepo(repo):
	theRepo = Repo(
		full_name=repo.full_name,
		name=repo.name,
		owner_login=repo.owner.login,
		fork=repo.fork,
		has_wiki=repo.has_wiki,
		has_issues=repo.has_issues,
		homepage=repo.homepage,
		language=repo.language,
		description=repo.description,
		created_at=repo.created_at,
		pushed_at=repo.pushed_at,
		size=repo.size,
		)
	session.add(theRepo)
	return theRepo


