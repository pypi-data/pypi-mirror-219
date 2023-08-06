from abc import ABC, abstractmethod
from onnc.forest.core.options import Options

from typing import Union, List


class Runtime:
    """
    This class works like a wrapper which is used for:
    - hidding runtime factory from user
    - narrow down runtime lifecycle (not init until load)
    """

    def __init__(self, options=None):
        self._options = options
        self.loaded_runtimes = []

        self.__init__state: List[bool] = [False, False, False, False, False]
        # indicate whether `launch`, `load`, `bind_input`, `bind_output`,
        #  `materialize` are trigger.

    def launch(self, options):
        self.__init__state[0] = True

    def load(self, options):
        self.__init__state[1] = True
        self.loaded_runtimes.append(make_runtime(options))
        idx = len(self.loaded_runtimes) - 1

        self.loaded_runtimes[idx].launch(options)
        self.loaded_runtimes[idx].load(options)

    def bind_input(self, input: Union[int, str], object: object):
        self.__init__state[2] = True
        return self.loaded_runtimes[0].bind_input(input, object)

    def bind_output(self, output: Union[int, str], object: object):
        self.__init__state[3] = True
        return self.loaded_runtimes[0].bind_output(output, object)

    def bind_all_inputs(self):
        self.__init__state[2] = True
        return self.loaded_runtimes[0].bind_all_inputs()

    def bind_all_outputs(self):
        self.__init__state[3] = True
        return self.loaded_runtimes[0].bind_all_outputs()

    def materialize(self):
        self.__init__state[4] = True
        res = []

        for rt in self.loaded_runtimes:
            res.append(rt.materialize())

        return res

    def read(self, *args):
        return self.loaded_runtimes[0].read(*args)

    def run(self):
        return self.loaded_runtimes[0].run()

    def write(self, *args):
        return self.loaded_runtimes[0].write(*args)

    def __call__(self, inputs: List):
        if not all(self.__init__state):
            self.launch(self._options) if self.__init__state[0] == 0 else None
            self.load(self._options) if self.__init__state[1] == 0 else None
            self.bind_all_inputs() if self.__init__state[2] == 0 else None
            self.bind_all_outputs() if self.__init__state[3] == 0 else None
            self.materialize() if self.__init__state[4] == 0 else None

        self.write(inputs)
        self.run()
        return self.read()


class AbstractAsyncRuntimeImplementation(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def launch(self, options):
        pass

    @abstractmethod
    def load(self, options):
        pass

    @abstractmethod
    def bind_input(self):
        pass

    @abstractmethod
    def bind_output(self):
        pass

    @abstractmethod
    def materialize(self):
        pass

    @abstractmethod
    def submit(self, data):
        pass

    @abstractmethod
    def wait(self):
        pass

    @abstractmethod
    def outcome(self):
        pass


class RuntimeRegistry(type):

    REGISTRY = []

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY.append(new_cls)
        return new_cls


class AbstractRuntimeImplementation(metaclass=RuntimeRegistry):

    @staticmethod
    def is_me(format) -> bool:
        return False

    def __init__(self):
        pass

    @abstractmethod
    def launch(self, options):
        pass

    @abstractmethod
    def load(self, options):
        pass

    @abstractmethod
    def bind_input(self):
        pass

    @abstractmethod
    def bind_output(self):
        pass

    @abstractmethod
    def materialize(self):
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def read(self, data):
        pass


def make_runtime(options: Options) -> AbstractRuntimeImplementation:

    for runtime in RuntimeRegistry.REGISTRY:
        if runtime.is_me(options):
            return runtime()
    raise NotImplementedError(f"Unable to identify {options}")
