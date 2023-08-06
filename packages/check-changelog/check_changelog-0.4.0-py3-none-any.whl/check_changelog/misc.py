"""Task code."""

import logging

log = logging.getLogger(__name__)


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
        raise
    if rc:
        log.info("%s", task_status(ttype, tname, "ok"))
    else:
        log.error("%s", task_status(ttype, tname, "fail"))
    return rc
