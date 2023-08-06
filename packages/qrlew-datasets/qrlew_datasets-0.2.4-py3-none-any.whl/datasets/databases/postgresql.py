from typing import Optional
from time import sleep
import logging
import subprocess
from sqlalchemy import create_engine, Engine, MetaData, text
from datasets.database import MutableDatabase
from datasets.network import Network

NAME: str = "qrlew-psql"
PORT: int = 5432
USER: str = "postgres"
PASSWORD: str = "qrlew-psql"

class PostgreSQL(MutableDatabase):
    def __init__(self, name=NAME, user=USER, password=PASSWORD, port=PORT) -> None:
        self.name = name
        self.user = user
        self.password = password
        self.port = port
        self.net = Network().name
        self.engine()

    def try_get_existing(self) -> Optional[Engine]:
        """Try to connect to postgresql"""
        if subprocess.run(['docker', 'exec', self.name, 'pg_isready']).returncode == 0:
            try:
                engine = create_engine(f'postgresql+psycopg://{self.user}:{self.password}@localhost:{self.port}/postgres')
                # Try to connect
                with engine.connect() as conn:
                    tables = conn.execute(text('''SELECT * FROM pg_catalog.pg_tables WHERE schemaname='public' '''))
                    for table in tables:
                        print(table)
                return engine
            except:
                return None
        else:
            return None

    def try_get_container(self) -> Optional[Engine]:
        """Try to start or run a postgresql container"""
        # Try to start an existing container
        if subprocess.run(['docker', 'start', self.name]).returncode != 0:
            # Run a new container
            subprocess.run([
                'docker',
                'run',
                '--hostname', self.name,
                '--volume', '/tmp:/tmp',
                '--name', self.name,
                '--detach', '--rm',
                '--env', f'POSTGRES_PASSWORD={self.password}',
                '--net', self.net,
                '--publish', f'{self.port}:5432',
                'postgres'])
        attempts = 0
        while subprocess.run(['docker', 'exec', self.name, 'pg_isready']).returncode != 0 and attempts < 10:
            print("Waiting postgresql to be ready...")
            sleep(1)
            attempts += 1
        return self.try_get_existing()

    # Implements engine
    def engine(self) -> Engine:
        """Create a postgresql engine"""
        engine = self.try_get_existing()
        if engine is None:
            engine = self.try_get_container()
        assert(engine is not None)
        return engine
    
    def url(self) -> str:
        return f'postgresql://{self.user}:{self.password}@{self.name}:{self.port}/postgres'

    # Dump psql files
    def dump(self, path: str) -> None:
        """Dump psql"""
        subprocess.run(['docker', 'exec', self.name, 'pg_dump',
                        '--host=localhost',
                        f'--username={self.user}',
                        '-Fp',
                        '-n', self.schema(),
                        '-f', path])
    
    def load(self, path: str) -> None:
        """Load psql"""
        logging.info(f'Loading {path}')
        subprocess.run(['docker', 'exec', self.name, 'psql',
                        '--host=localhost',
                        f'--username={self.user}',
                        '--dbname=postgres',
                        f'--file={path}'])
