import logging
from datasets.sources import Loader, Financial, IMDB, Hepatitis
from datasets.databases import PostgreSQL

logging.basicConfig(level=logging.DEBUG)

database = PostgreSQL()
loader = Loader(database)

# Build all dumps
for source in [Financial(), IMDB(), Hepatitis()]:
    print(source)
    loader.load(source)
    database.set_schema(source.schema())
    database.dump(f'/tmp/{source.schema()}.sql')
    print(database.declaration())
