class DatasetFactory:
    _REGISTERED = {}

    @staticmethod
    def register(dataset_type, builder):
        DatasetFactory._REGISTERED[dataset_type] = builder

    @staticmethod
    def get(dataset_type, **kwargs):
        builder = DatasetFactory._REGISTERED.get(dataset_type)
        if not builder:
            raise KeyError(f"dataset type {dataset_type} not supported or registered!")

        return builder(**kwargs)
