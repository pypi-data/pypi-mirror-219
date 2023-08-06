"""
Check that git tags are documented in CHANGELOG.md.

See https://keepachangelog.com/en/ for details
"""

import logging
import re
import subprocess as sp
import sys

log = logging.getLogger(__name__)


def get_tags_stdin():
    refs = sys.stdin.readlines()
    log.debug("refs %s", refs)
    pfx = "refs/tags/"
    pfx_len = len(pfx)
    return [r[pfx_len:].split()[0] for r in refs if r.startswith(pfx)]


def get_tags_git(latest=1000):
    cmd = "git tag --list --merged | tac"
    if latest >= 0:
        cmd += " | head -n %d" % latest
    tags = sp.check_output(cmd, shell=True)
    tags = tags.decode(encoding="utf-8", errors="ignore")
    return tags.split()


def get_tags(atags):
    log.debug("tag source: %s", atags)
    tags = None
    if atags == "hook":
        tags = get_tags_stdin()
    elif atags == "history":
        tags = get_tags_git(-1)
    elif atags.startswith("history:"):
        latest = atags.split(":")[1]
        try:
            latest = int(latest)
        except Exception:
            log.error("can't get latest from '%s'", latest)
            latest = -1
        tags = get_tags_git(latest)
    return tags


def git_check_tags(txt, atags):
    tags = get_tags(atags)
    if not tags:
        return True
    log.info("scan %d tags from '%s' source", len(tags), atags)
    rc = True
    for tag in tags:
        m = changelog_has_tag(txt, tag)
        log.debug("tag %s, found %s", tag, m)
        if m["status"] == "ok":
            log.info("tag '%s' found at line %s", tag, m["line"])
        else:
            log.error("tag '%s' %s", tag, m["status"])
            rc = False
    return rc


def changelog_has_tag(txt, tag):
    tag_header_re = "(?m)^## \\[(TAGRE)\\].*(\\d{4}-\\d{2}-\\d{2})$"
    tag_re = re.escape(tag)
    tag_re = tag_header_re.replace("TAGRE", tag_re)
    m = re.search(tag_re, txt)
    if m:
        rc = {"status": "ok", "line": txt[: m.start()].count("\n") + 1}
    else:
        rc = {"status": "not found", "regex": tag_re}
    return rc
