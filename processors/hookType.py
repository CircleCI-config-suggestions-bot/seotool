# Standard Library
from typing import Awaitable, Callable

# Third Party
from bs4 import BeautifulSoup
from click.decorators import FC
from pluggy.hooks import _HookRelay

# First Party
from engines.dataModels import response
from processors.dataModels import ResultSet


class HookType(_HookRelay):
    def process_html(self, html: BeautifulSoup, url: str, status_code: int, response: response) -> None:
        ...

    def process(self, html: BeautifulSoup, url: str, status_code: int, response: response) -> None:
        ...

    def process_output(self, resultsSets: list[ResultSet]) -> list[Awaitable[None]]:
        ...

    def get_results_set(self) -> list[ResultSet]:
        ...

    def get_options(self) -> list[Callable[[FC], FC]]:
        ...

    def should_process(self, url: str, response: response) -> list[bool]:
        ...

    def log(self, line: str, style: str) -> None:
        ...

    def log_error(self, line: str) -> None:
        ...
