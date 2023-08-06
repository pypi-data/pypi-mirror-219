from datasets.sources.relational_dataset_repository import RelationalDatasetRepository

class IMDB(RelationalDatasetRepository):
    def __init__(self) -> None:
        super().__init__('imdb_ijs')
