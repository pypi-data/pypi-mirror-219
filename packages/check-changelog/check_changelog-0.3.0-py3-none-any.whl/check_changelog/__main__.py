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
import os
import sys

import pydevkit.log.config  # noqa: F401
from pydevkit.argparse import ArgumentParser

from . import __version__
from .changelog import check_changelog_main
from .git import git_check_tags

log = logging.getLogger(__name__)

bool_yes_no = ["yes", "no"]


def get_args():
    p = ArgumentParser(help=__doc__, version=__version__)
    p.add_argument(
        "--check",
        help=("if value is 'yes', check changelog structure"),
        choices=bool_yes_no,
        default="yes",
    )
    p.add_argument(
        "--install",
        help=("if value is 'yes', installs git 'pre-push' hook"),
        choices=bool_yes_no,
        default="no",
    )
    p.add_argument(
        "--tags",
        help=(
            "check that specified git tags are documented. "
            "Value can be 'hook' to read tag "
            "refs from stdin as pre-push hook would do. Or it can be "
            "'history:N' for N latest tags, or 'history' to all tags."
        ),
        default="",
    )
    p.add_argument("-C", help="top project dir", dest="topdir", default=".")
    p.add_argument(
        "--file", help="changelog file to check", default="CHANGELOG.md"
    )

    return p.parse_known_args()


def task_status(ttype, tname, status):
    clrs = {
        "norm": "\033[0m",
        "ok": "\033[32;1m",
        "fail": "\033[31;1m",
        "starting": "\033[32;1m",
    }
    msg = ""
    rc = {
        "clr-off": clrs["norm"],
        "clr-on": clrs[status],
        "type": ttype,
        "name": tname,
        "status": status,
    }
    fmt = "%(clr-on)s%(type)s%(clr-off)s %(name)s: %(clr-on)s%(status)s%(clr-off)s"
    msg += fmt % rc
    return msg


def run_task(ttype, tname, func, *args):
    _norm = "\033[0m"
    _ok = "\033[32;1m"
    _fail = "\033[31;1m"
    log.info("%s", task_status(ttype, tname, "starting"))
    try:
        rc = func(*args)
    except Exception as exc:
        rc = False
        log.error("%s", exc)
    if rc:
        log.info("%s", task_status(ttype, tname, "ok"))
    else:
        log.error("%s", task_status(ttype, tname, "fail"))
    return rc


def run_all_tasks(args):
    text = open(args.file, "r").read()
    rcs = []
    if args.check == "yes":
        rc = run_task(
            "task",
            "check changelog structure",
            check_changelog_main,
            args.file,
            text,
        )
        rcs.append(rc)

    if args.tags:
        rc = run_task(
            "task", "check tags documentation", git_check_tags, text, args.tags
        )
        rcs.append(rc)

    return all(rcs)


def install_git_hook():
    path = ".git/hooks/pre-push"
    if os.path.exists(path):
        log.warning("remove current '%s'", path)
        os.unlink(path)
    sh = "#!/bin/bash\n\n" + sys.argv[0] + " --tags=hook --check=no\n"
    open(path, "w").write(sh)
    os.chmod(path, 0o755)
    return True


def main():
    args, unknown_args = get_args()
    if unknown_args:
        log.warning("Unknown arguments: %s", unknown_args)
        sys.exit(1)
    if args.topdir != ".":
        try:
            log.info("working dir '%s'", args.topdir)
            os.chdir(args.topdir)
        except Exception as exp:
            log.error("%s", exp)
            sys.exit(1)

    if args.install == "yes":
        rc = run_task("hook", "install pre-push", install_git_hook)
    else:
        rc = run_task("file", args.file, run_all_tasks, args)
    sys.exit(0 if rc else 1)


if __name__ == "__main__":
    main()
