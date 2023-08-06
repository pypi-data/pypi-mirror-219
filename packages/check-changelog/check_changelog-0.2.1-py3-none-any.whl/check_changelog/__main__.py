"""
Check that changelog conforms to 'Keep A Changelog' style.

See https://keepachangelog.com/en/ for details

EPILOG:
Example:
```
check-changelog --file CHANGELOG.md
```
"""


import logging
import sys

import pydevkit.log.config  # noqa: F401
from pydevkit.argparse import ArgumentParser

from . import __version__
from .changelog import CLNotFoundError, CLSyntaxError, check_changelog

log = logging.getLogger(__name__)


def get_args():
    p = ArgumentParser(help=__doc__, version=__version__)
    p.add_argument(
        "--file", help="changelog file to check", default="CHANGELOG.md"
    )

    return p.parse_known_args()


def main():
    args, unknown_args = get_args()
    if unknown_args:
        log.warning("Unknown arguments: %s", unknown_args)
        sys.exit(1)
    try:
        text = open(args.file, "r").read()
        check_changelog(text)
        sys.exit(0)
    except (CLSyntaxError, CLNotFoundError) as exp:
        log.error(
            "%s:%d: %s; got '%s'%s",
            args.file,
            exp.lineno,
            exp.msg,
            exp.content,
            "; " + exp.msg_extra if exp.msg_extra else "",
        )
    except Exception as exp:
        log.error("%s", exp)
    sys.exit(1)


if __name__ == "__main__":
    main()
