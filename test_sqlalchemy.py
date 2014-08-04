
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
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