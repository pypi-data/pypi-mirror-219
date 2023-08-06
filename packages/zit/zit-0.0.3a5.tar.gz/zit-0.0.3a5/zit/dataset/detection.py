import os
from pathlib import Path

from ..routes import build_default_router
from ..utils import find_zit_root
from .build import DatasetBuilder
from .factory import DatasetFactory
from .manager import Manager


class DetectionDatasetBuilder(DatasetBuilder):
    def __call__(self, **kwargs):
        zit_root = find_zit_root(Path.cwd())

        image_source = str(zit_root / kwargs.get("image_source", "images"))
        annotation_source = str(zit_root / kwargs.get("annotation_source", "annotations.csv"))

        params = {
            "task": "detection",
            "image_source": image_source,
            "annotation_source": annotation_source,
        }

        hash_ = self._hash_params(params)

        if hash_ in self._datasets:
            dataset = self._datasets[hash_]

        else:
            manage_root = str(zit_root / ".zit" / "manager" / hash_)
            os.makedirs(manage_root, exist_ok=True)
            manager = Manager(manage_root, "detection", dataframe_serving=True)
            manager.add_metas(image_source, for_init=True)
            manager.add_annotations(annotation_source, for_init=True)

            meta_serving = kwargs.get("meta_serving", False)
            router, df, meta_df = build_default_router(
                params,
                manager,
                meta_serving=meta_serving,
            )

            dataset = {
                "params": params,
                "manager": manager,
                "router": router,
                "df": df,
                "meta_df": meta_df,
            }

            self._datasets[hash_] = dataset

        return dataset


DatasetFactory.register("detection", DetectionDatasetBuilder())
