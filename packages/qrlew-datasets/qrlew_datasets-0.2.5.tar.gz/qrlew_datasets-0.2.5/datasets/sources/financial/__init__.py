from datasets.sources.relational_dataset_repository import RelationalDatasetRepository

class Financial(RelationalDatasetRepository):
    def __init__(self) -> None:
        super().__init__('financial')
