"""
Add release to CHANGELOG.md.

See https://keepachangelog.com/en/ for details
"""

import logging
import os
import re
import subprocess as sp
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import toml

from .changelog import check_changelog_main
from .misc import run_task

log = logging.getLogger(__name__)

host = "https://github.com/user/project"
tag_path = "releases/tag"


def get_host():
    data = toml.load("pyproject.toml")
    try:
        data = data["project"]["urls"]
    except Exception:
        return host
    key = "Repository"
    if key in data:
        url = data[key]
        if url.endswith(".git"):
            url = url[:-4]
        log.debug("project url: from %s key: %s", key, url)
        return url
    key = "Homepage"
    if key in data:
        url = data[key]
        log.debug("project url: from %s key: %s", key, url)
        return url
    return None


footer = """

------

The format is based on [Keep a Changelog][kacl] and [Common Changelog][ccl] styles
and this project adheres to [Semantic Versioning][semver]

[semver]: https://semver.org/spec/v2.0.0.html "Semantic Versioning"
[kacl]: https://keepachangelog.com/en/ "Keep a Changelog"
[ccl]: https://common-changelog.org/ "Common Changelog"
"""


class ChangeLog:
    def __init__(self):
        self.rels = []
        self.host = get_host()

    def add_rel(self, name, date=None):
        log.info("add release '%s' %s", name, date if date else "")
        self.rels.append([name, date])

    def __str__(self):
        rels = []
        links = []
        for rel in self.rels:
            txt = "## [%s]%s\n\n" % (rel[0], " - " + rel[1] if rel[1] else "")
            rels.append(txt)
            links.append(self.add_link(rel[0]))
        rc = "".join(rels) + "\n" + "\n".join(links)
        return "# Changelog\n\n" + rc + footer

    def add_link(self, name):
        if name == "Unreleased":
            return f"[{name}]: {self.host}"
        return f"[{name}]: {self.host}/{tag_path}/{name}"


def find_rel(rels, name):
    for i, v in enumerate(rels):
        if v["name"] == name:
            return (i, v)
    return None


def cl_add_released(args, cl):
    m = cl["match"]
    txt = cl["text"]
    rc = cl["parsed-cl"]
    uname = "Unreleased"
    unrel = find_rel(rc["releases"], uname)
    log.debug("unrel %s", unrel)
    rel = find_rel(rc["releases"], args.release)
    log.debug("rel %s", rel)
    if rel:
        if rel[0] == (1 if unrel else 0):
            log.info("release '%s' is a first named release already", args.release)
            return True
        log.error("release '%s' already exists", args.release)
        return False
    if not unrel:
        log.info("No %s section to convert to release", uname)
        return False
    dt = datetime.now(tz=ZoneInfo("UTC")).strftime("%Y-%m-%d")
    rc = "\n\n## [%s] - %s" % (args.release, dt)
    txt = txt[0 : m.end(0)] + rc + "\n" + txt[m.end(0) + 1 :]

    unlink_reg = "(?m)^\\[Unreleased\\]:.*"
    m = re.search(unlink_reg, txt)
    if not m:
        log.error("missing %s link. Pattern not found '%s'", uname, unlink_reg)
        return False
    cl = ChangeLog()
    link = cl.add_link(args.release)
    rc = "\n%s\n" % link
    txt = txt[: m.end(0)] + rc + txt[m.end(0) + 1 :]
    log.debug("new changelog: %s", txt)
    path = args.file
    open(path, "w").write(txt)
    return True


def cl_add_unreleased(args, cl):
    m = cl["match"]
    txt = cl["text"]
    path = args.file
    uname = "Unreleased"
    rel = cl["parsed-cl"]["releases"][0]
    if rel["name"] == uname:
        log.info("file %s already has %s section", path, uname)
        return True
    txt = txt[0 : m.start(0)] + "\n## [" + uname + "]\n\n" + txt[m.start(0) + 1 :]
    log.debug("new changelog: %s", txt)
    open(path, "w").write(txt)
    return True


def cl_create(args):
    log.debug("cl_create: %s", args)
    fmt = "%(refname:strip=2) %(taggerdate:short)"
    cmd = "git tag --format='" + fmt + "' -l --merged | tac"
    tags = sp.check_output(cmd, shell=True)
    tags = tags.decode(encoding="utf-8", errors="ignore")
    tags = tags.splitlines()
    cl = ChangeLog()
    cl.add_rel("Unreleased")
    for tag in tags:
        log.debug("found tag %s", tag)
        tmp = tag.split()
        cl.add_rel(*tmp)

    open(args.file, "w").write(str(cl))
    return True


def do_release(args):
    log.debug("do_release: %s", args)
    rc = True
    if not os.path.isfile(args.file):
        rc = run_task("task", "create " + args.file, cl_create, args)
    if not rc:
        return False
    log.info("read %s", args.file)
    txt = open(args.file, "r").read()
    pcl = run_task(
        "task",
        "check changelog structure",
        check_changelog_main,
        args.file,
        txt,
    )
    log.debug("parsed changelog %s", pcl)
    if not pcl:
        log.error("can't parse %s", args.file)
        return False

    sec_reg = "(?m)\\n^## (?P<rel>.*)"
    m = re.search(sec_reg, txt)
    if not m:
        log.error("%s: no releases found", args.file)
        log.warning("To create new changelog, remove '%s' file", args.file)
        log.warning("and run `check-changelog --release=new`")
        sys.exit(1)
    cl = {"text": txt, "parsed-cl": pcl, "match": m}
    if args.release == "new":
        rc = run_task("task", "new release", cl_add_unreleased, args, cl)
    elif args.release:
        msg = "convert [Unreleased] to [%s]" % args.release
        rc = run_task("task", msg, cl_add_released, args, cl)
    if not rc:
        return False
    return True
