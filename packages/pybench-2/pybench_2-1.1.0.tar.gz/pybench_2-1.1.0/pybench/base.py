from abc import ABC, abstractmethod
from typing import Iterator


class BenchSetup(ABC):
    @classmethod
    def iter_configs(cls, default_cfg: dict) -> Iterator["BenchSetup"]:
        """Iterate different configurations for each run"""
        raise NotImplementedError()

    @abstractmethod
    def get_method_name(self) -> str:
        """Get the method name."""
        pass

    @abstractmethod
    def get_bench_name(self) -> str:
        """Get benchmark name"""
        pass

    @abstractmethod
    def get_setup(self) -> str:
        """Get the setup code for pyperf"""
        pass

    @abstractmethod
    def get_statement(self) -> str:
        """Get the benchmark statement for pyperf"""
        pass
