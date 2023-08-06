from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

import click

from cycode.cli.models import CliError, CliResult

if TYPE_CHECKING:
    from cycode.cli.models import LocalScanResult


class BasePrinter(ABC):
    RED_COLOR_NAME = 'red'
    WHITE_COLOR_NAME = 'white'
    GREEN_COLOR_NAME = 'green'

    def __init__(self, context: click.Context) -> None:
        self.context = context

    @abstractmethod
    def print_scan_results(self, local_scan_results: List['LocalScanResult']) -> None:
        pass

    @abstractmethod
    def print_result(self, result: CliResult) -> None:
        pass

    @abstractmethod
    def print_error(self, error: CliError) -> None:
        pass
