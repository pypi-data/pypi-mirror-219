from datasets.sources.relational_dataset_repository import RelationalDatasetRepository

class Hepatitis(RelationalDatasetRepository):
    def __init__(self) -> None:
        super().__init__('Hepatitis_std')
