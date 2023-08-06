from typing import Optional
from time import sleep
import subprocess
from sqlalchemy import create_engine, Engine, MetaData, text
from datasets.database import MutableDatabase

NAME: str = "qrlew-mariadb"
PORT: int = 3306
USER: str = "qrlew"
PASSWORD: str = "qrlew-mariadb"

class MariaDB(MutableDatabase):
    def __init__(self, name=NAME, user=USER, password=PASSWORD, port=PORT) -> None:
        self.name = name
        self.user = user
        self.password = password
        self.port = port
        self.engine()

    def try_get_existing(self) -> Optional[Engine]:
        """Try to connect to mariadb"""
        if subprocess.run(['docker', 'exec', self.name, 'mariadb-admin',
                              f'--password={self.password}',
                              'status']).returncode == 0:
            try:
                engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@localhost:{self.port}')
                # Try to connect
                conn = engine.connect()
                conn.close()
                return engine
            except:
                return None
        else:
            return None

    def try_get_container(self) -> Optional[Engine]:
        """Try to start or run a mariadb container"""
        # Try to start an existing container
        if subprocess.run(['docker', 'start', self.name]).returncode != 0:
            # Run a new container
            subprocess.run([
                'docker',
                'run',
                '--volume', '/tmp:/tmp',
                '--name', self.name,
                '--detach', '--rm',
                '--env', f'MARIADB_USER={self.user}',
                '--env', f'MARIADB_PASSWORD={self.password}',
                '--env', f'MARIADB_ROOT_PASSWORD={self.password}',
                '--publish', f'{self.port}:3306',
                'mariadb:latest'])
        attempts = 0
        while subprocess.run(['docker', 'exec', self.name, 'mariadb-admin',
                              f'--password={self.password}',
                              'status']).returncode != 0 and attempts < 10:
            print("Waiting mariadb to be ready...")
            sleep(1)
            attempts += 1
        return self.try_get_existing()

    # Implements engine
    def engine(self) -> Engine:
        """Create a mariadb engine"""
        engine = self.try_get_existing()
        if engine is None:
            engine = self.try_get_container()
        assert(engine is not None)
        return engine
    
    # Dump psql files
    def dump(self, path: str) -> None:
        """Dump psql"""
        self._dump('localhost', self.user, self.password, self.schema(), path)
    
    # Dump psql files
    def _dump(self, host: str, user: str, password: str, db: str, path: str) -> None:
        """Dump psql"""
        subprocess.run(['docker', 'exec', self.name, 'mariadb-dump',
                        f'--host={host}',
                        f'--user={user}',
                        f'--password={password}',
                        db,
                        '--compatible=postgresql',
                        f'--result-file={path}'])
