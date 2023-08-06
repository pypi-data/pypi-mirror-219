from __future__ import annotations
from typing import Callable, Dict, List, Type

from pydlmeta.identifier.dataset import identify, DatasetFormat
from .transform import DatasetTransformer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dataset import Dataset


class PreprocessTransformer(DatasetTransformer):

    FORMAT = DatasetFormat.NON_SPECIFIED

    @classmethod
    def is_me(cls, dataset: Dataset) -> bool:
        return identify(dataset) == cls.FORMAT

    def transform(self, dataset: Type[Dataset]):
        pass

    def set_preprocessor(self,
                         func: Callable,
                         args: List = [],
                         kwargs: Dict = {}) -> None:
        """Set the transform func as given callback

        Args:
            func (Callable): preprocessor function, the output of the this
                             function has to be the preprocessed dataset.
            args (List): args for the preprocessor function, use `__DATASET__`
                         to indicate the dataset argument position

            kwargs (Dict): keword args for the preprocessor function

        Example:

            def _preprocess(dataset, min_val, max_val, enhancement=False):
              ....
              ....

            set_preprocessor(_preprocess,
                            ['__DATASET__', 1, 100],
                            {'enhancement': True}
                            )
        """

        self.set_transform(func, args, kwargs)
