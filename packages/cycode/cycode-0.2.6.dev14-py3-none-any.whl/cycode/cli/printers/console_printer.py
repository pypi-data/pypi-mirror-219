from typing import TYPE_CHECKING, ClassVar, Dict, List

import click

from cycode.cli.exceptions.custom_exceptions import CycodeError
from cycode.cli.models import CliError, CliResult
from cycode.cli.printers.json_printer import JsonPrinter
from cycode.cli.printers.sca_table_printer import SCATablePrinter
from cycode.cli.printers.table_printer import TablePrinter
from cycode.cli.printers.text_printer import TextPrinter

if TYPE_CHECKING:
    from cycode.cli.models import LocalScanResult
    from cycode.cli.printers.base_printer import BasePrinter


class ConsolePrinter:
    _AVAILABLE_PRINTERS: ClassVar[Dict[str, 'BasePrinter']] = {
        'text': TextPrinter,
        'json': JsonPrinter,
        'table': TablePrinter,
        # overrides
        'table_sca': SCATablePrinter,
        'text_sca': SCATablePrinter,
    }

    def __init__(self, context: click.Context) -> None:
        self.context = context
        self.scan_type = self.context.obj.get('scan_type')
        self.output_type = self.context.obj.get('output')

        self._printer_class = self._AVAILABLE_PRINTERS.get(self.output_type)
        if self._printer_class is None:
            raise CycodeError(f'"{self.output_type}" output type is not supported.')

    def print_scan_results(self, local_scan_results: List['LocalScanResult']) -> None:
        printer = self._get_scan_printer()
        printer.print_scan_results(local_scan_results)

    def _get_scan_printer(self) -> 'BasePrinter':
        printer_class = self._printer_class

        composite_printer = self._AVAILABLE_PRINTERS.get(f'{self.output_type}_{self.scan_type}')
        if composite_printer:
            printer_class = composite_printer

        return printer_class(self.context)

    def print_result(self, result: CliResult) -> None:
        self._printer_class(self.context).print_result(result)

    def print_error(self, error: CliError) -> None:
        self._printer_class(self.context).print_error(error)
