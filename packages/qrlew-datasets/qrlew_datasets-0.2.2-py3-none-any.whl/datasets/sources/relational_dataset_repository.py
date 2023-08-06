from sqlalchemy import Engine, create_engine
from datasets.database import Database

class RelationalDatasetRepository(Database):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._schema = name

    def engine(self) -> Engine:
        return create_engine(f'mysql+pymysql://guest:relational@relational.fit.cvut.cz:3306/{self.schema()}')
    
    def url(self) -> str:
        return f'mysql://guest:relational@relational.fit.cvut.cz:3306/{self.schema()}'
    
    def schema(self) -> str:
        return self._schema
