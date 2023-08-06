from dataclasses import dataclass, field
import abc, typing
from typing import List, Union
from pathlib import Path

from pydlmeta.identifier.model import identify
from onnc.bench.core.model.model import Model


@dataclass
class RuntimeSettings:
    pass


class OptionsRegistry(type):

    REGISTRY = []

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY.append(new_cls)
        return new_cls


class Options(metaclass=OptionsRegistry):
    model_format = None
    def __init__(self, loadable: Union[str, Path, Model]):
        self.settings: RuntimeSettings
        self.devices: List = []

        if isinstance(loadable, str) or isinstance(loadable, Path):
            loadable = Model(loadable)

        self.loadable = loadable
        self.__change_cls(loadable)

    def encapsulate(self, options):
        self._encapsulation.append(options)

    def __change_cls(self, loadable):
        format_ = identify(loadable.src)

        for opt_cls in OptionsRegistry.REGISTRY:
            if opt_cls.is_me(format_):
                """
                 The entire Options class is substituded by the derived class
                 after calling self.__class__ = opt_cls. Thus, the followeing
                 self.__init__ will call derived class's init
                """
                self.__class__ = opt_cls
                self.__init__(loadable)

                return

        raise NotImplementedError(f"Unable to identify {loadable}")

    @classmethod
    def is_me(cls, format) -> bool:
        return format == cls.model_format
