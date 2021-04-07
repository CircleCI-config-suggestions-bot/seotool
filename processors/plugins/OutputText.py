# Standard Library
from contextlib import nullcontext
from typing import List

# Third Party
import click
from rich.console import Console
from rich.table import Table

# First Party
from processors import ResultSet, hookimpl_processor
from seotool.crawl import Crawler


class OutputText:
    show_no_issue = False

    def __init__(self, crawler: Crawler, text_show_no_issue=False, text_save_output=True, text_width=None) -> None:
        self.crawler = crawler
        self.show_no_issue = text_show_no_issue
        self.file = None

        if text_save_output and text_width is None:
            self.width = 120
        else:
            self.width = int(text_width) if text_width is not None else None

        if text_save_output:
            try:
                self.file = self.crawler.get_output_name("text-report", "txt")
            except AttributeError:
                pass

    @hookimpl_processor(trylast=True)
    def process_output(self, resultsSets: List[ResultSet]):
        with open(self.file, "w") if self.file is not None else nullcontext() as f:
            console = Console(file=f, width=self.width)

            console.print(f"[underline]SEO Report for {self.crawler.url}[/underline]", justify="center")
            console.print("\n")
            for result_set in resultsSets:
                table = Table(title=result_set.title, expand=True)
                if not result_set.has_data:
                    if not self.show_no_issue:
                        continue
                    table.add_row("No issues")
                else:
                    for key in result_set.data_headers:
                        table.add_column(key)

                    for row in result_set.data_flat_dict:
                        table.add_row(*list(row.values()))

                console.print(table)
                console.print("\n")

    @hookimpl_processor
    def get_options(self):
        help_no_issue = "Text output shows reports with no issues"
        help_save_output = "Text output is saved to file"
        help_width = "Text output width, defaults to screen size"
        return [
            click.option("--text-show-no-issue", default=False, is_flag=True, help=help_no_issue),
            click.option("--text-save-output/--text-show-output", default=True, is_flag=True, help=help_save_output),
            click.option("--text-width", default=None, help=help_width),
        ]