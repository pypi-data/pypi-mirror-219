import subprocess

NAME: str = 'qrlew-net'

class Network:
    """Create a network"""
    def __init__(self, name=NAME):
        self.name = name
        subprocess.run(['docker', 'network', 'create', self.name])