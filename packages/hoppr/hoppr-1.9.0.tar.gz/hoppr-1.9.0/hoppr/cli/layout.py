"""
Hoppr stage output Rich layout
"""
from __future__ import annotations

from rich.console import Console
from rich.containers import Lines
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.text import Text

from hoppr import __version__

BORDER_LINES = 2
HEADER_SIZE = 3
REMOVE_LINES = BORDER_LINES + HEADER_SIZE

console = Console()


class HopprJobsPanel(Panel):
    """
    Customized Rich Progress bar Panel
    """

    progress_bar = Progress(
        "{task.description}",
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )

    def __init__(self) -> None:
        super().__init__(
            renderable=self.progress_bar,
            title="[bold blue]Jobs",
            title_align="left",
            border_style="purple",
        )

    def add_task(self, description: str, **fields) -> int:
        """
        Add a task to be tracked in the `jobs` side panel

        Args:
            description (str): A description of the task

        Returns:
            int: ID of the added task
        """
        return self.progress_bar.add_task(description, start=False, **fields)


class HopprOutputPanel(Panel):
    """
    Customized Rich Text box to simulate a console
    """

    lines = Lines()

    def __init__(self) -> None:
        super().__init__(
            renderable=self.lines,
            border_style="purple",
            expand=False,
            title_align="left",
        )

    def print(self, line: str, style: str = "") -> None:
        """
        Write a message to the console output panel

        Args:
            line (str): Message to write
            style (str): Style to apply to message string
        """
        self.lines.append(Text(line, style))

        # Subtract static lines of Panel boxes to get displayed height of text
        if len(self.lines) > console.height - REMOVE_LINES:
            self.lines.pop(index=0)


class HopprProgressPanel(Panel):  # pylint: disable=too-few-public-methods
    """
    Customized Rich Progress bar Panel
    """

    progress_bar = Progress()

    def __init__(self) -> None:
        super().__init__(
            renderable=self.progress_bar,
            title="[bold blue]Progress",
            title_align="left",
            border_style="purple",
        )

        self.progress_bar.add_task(description="All Jobs")


class HopprLayout(Layout):
    """
    Layout of the Hoppr console application
    """

    name: str = "root"
    jobs_panel = HopprJobsPanel()
    output_panel = HopprOutputPanel()
    overall_progress = HopprProgressPanel()

    def __init__(self, title: str = f"Hoppr v{__version__}") -> None:
        super().__init__()

        self.split(Layout(name="header", size=HEADER_SIZE), Layout(name="main"))
        self["main"].split_row(Layout(name="side"), Layout(name="console", ratio=2))
        self["side"].split(Layout(name="jobs"), Layout(name="progress", size=3))

        # Initialize header
        header = Text(text=title, style="bold blue", justify="center")
        self["header"].update(renderable=Panel(renderable=header, border_style="purple"))

        # Initialize jobs side bar panel
        self["jobs"].update(renderable=self.jobs_panel)

        # Initialize overall progress side bar
        self["progress"].update(renderable=self.overall_progress)

        # Initialize main body panel
        self["console"].update(renderable=self.output_panel)

    def add_job(self, description: str, **fields) -> int:
        """
        Add a job to the `jobs` side panel

        Args:
            description (str): Description of the job to add
        """
        return self.jobs_panel.add_task(description, **fields)

    def print(self, line: str, style: str = "") -> None:
        """
        Write a message to the console output panel

        Args:
            line (str): Message to write
        """
        self.output_panel.print(line, style)
