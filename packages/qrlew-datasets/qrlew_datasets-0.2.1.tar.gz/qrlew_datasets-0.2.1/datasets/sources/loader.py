import subprocess
from datasets.database import Database
from datasets.network import Network

NAME: str = "qrlew-pgloader"

class Loader:
    def __init__(self, destination: Database) -> None:
        self.destination = destination
        self.net = Network().name

    def load(self, source: Database) -> bool:
        """Try to run pgloader to load a DB into the target DB"""
        # Try to start an existing container
        subprocess.run([
                'docker',
                'run',
                '--rm',
                '-it',
                '--net', self.net,
                'dimitri/pgloader:latest',
                'pgloader',
                 source.url(),
                 self.destination.url()])
        return True