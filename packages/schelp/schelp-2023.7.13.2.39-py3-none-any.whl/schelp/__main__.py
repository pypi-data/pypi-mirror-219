""" schelp.__main__
"""

from fleks import app, cli
from fleks.util import lme

from . import fmt

LOGGER = lme.get_logger(__name__)


@cli.click.argument("filename")
@cli.click.command
def entry(filename: str = "/dev/stdin"):
    """CLI tool for schelp
    :param filename: str:  (Default value = '/dev/stdin')
    """
    if filename == "-":
        filename = "/dev/stdin"
    try:
        with open(filename) as fhandle:
            text = fhandle.read()
    except FileNotFoundError:
        LOGGER.warning("input is not a file; parsing as string")
        text = filename
    formatted = fmt(text, filename=filename)
    print(text)
    print()
    print(formatted)

    lme.CONSOLE.print(
        app.Syntax(
            fmt(text, filename=filename),
            "bash",
            word_wrap=True,
        )
    )


if __name__ == "__main__":
    entry()
