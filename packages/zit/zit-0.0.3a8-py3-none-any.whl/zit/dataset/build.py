import json
from hashlib import blake2s


class DatasetBuilder:
    def __init__(self):
        self._datasets = {}

    def __call__(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def _hash_params(params, digest_size=4):
        hasher = blake2s(digest_size=digest_size)
        hasher.update(json.dumps(params, sort_keys=True).encode("utf-8"))
        return hasher.hexdigest()
