from typing import List, Dict, Union
from pathlib import Path
import shutil
import json
import os
from os.path import abspath

from onnc.bench.core.model.model import Model


class Deployment:
    """
    Deployment describes the output directory of a compilation results.
        ├── base_path
        │   └── model_0
        │       ├── build
        │       │   └── model
        │       ├── report.json
        │       └── working_dir
    """
    META_FNAME = Path('.deployment.json')

    def __init__(self, base_path: Path):

        if not os.path.isdir(base_path):
            raise FileNotFoundError(f'"{base_path}" is not an exist dir')
        self.base_path = Path(base_path)
        self.report_paths = list(self.base_path.rglob("**/report.json"))
        if len(self.report_paths) == 0:
            raise FileNotFoundError(
                'A deployment dir should contain at least one model_N/report.json'
                'but not found in {}'.format(self.base_path)
            )

    @property
    def reports(self):
        res = []
        for report_path in self.report_paths:
            with open(report_path, 'r') as f:
                report = json.load(f)
                # res.append(json.dumps(report, sort_keys=True, indent=2))
                res.append(report)
        return res

    @property
    def loadable(self):
        if len(self.loadables) > 1:
            raise ValueError("Error: Compilation result contains multiple "
                             "models, use loadables instead.")
        elif len(self.loadables) == 0:
            raise ValueError("Error: No loadable found "
                             "(Maybe compilation fail?)")
        return self.loadables[0]

    @property
    def loadables(self) -> List[Model]:

        if not os.path.exists(self.base_path):
            raise Exception(f'Deployment base_path is not a directory: '
                            f'{self.base_path}.')
        res = []
        for sub_model_root in os.listdir(self.base_path):
            """
            └── self.base_path
                └── model_0    <------ sub_model_root
                │    ├── build
                │    │   ├── by_product
                │    │   └── model.xxx
                │    ├── report.json
                │    └── working_dir
                │        └── asdf.txt

            """
            root = self.base_path / sub_model_root
            if not os.path.isdir(root / "build"):
                raise Exception(f'Invalid deployment subdir {root}: '
                                f'Missing model directory')
            model_to_add = None
            if os.path.isdir(root / "build/model"):
                """
                Case 1: submodel is a directory named model contains
                        multiple files. Ex: Openvino .xml, .bin
                """
                model_to_add = Model(abspath(root / "build/model"))
            else:
                """
                Case 2: submodel is a single file name starts with model
                """
                for file in os.listdir(root / "build"):
                    if file.startswith("model"):
                        model_to_add = Model(abspath(root / f"build/{file}"))
                        break
            if not model_to_add:
                raise Exception(
                    f"Unrecognized deployment subdir "
                    f"abspath{root}, plz contacts developers to fix it.")
            else:
                res.append(model_to_add)
        return res

    def deploy(self, target: Path):
        """Copy the deployment folder to target

        Copy the deployment folder to target and reconstruct the meta

        """
        shutil.copytree(self.base_path, target)
        if os.path.exists(target / self.META_FNAME):
            os.remove(target / self.META_FNAME)
        return Deployment(target)
