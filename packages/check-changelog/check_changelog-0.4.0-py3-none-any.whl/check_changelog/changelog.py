"""
Parse changelog and ensure it conforms to the required structure.

See https://keepachangelog.com/en/ for details
"""

import inspect
import logging
import re

from markdown_it import MarkdownIt
from pydevkit.log import prettify

log = logging.getLogger(__name__)
logging.getLogger("markdown_it").setLevel(logging.INFO)


class Tokens(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.idx = 0
        self.lineno = 0
        self.content = ""

    def get(self):
        if self.is_empty():
            return None
        t = self[self.idx]
        if log.getEffectiveLevel() == logging.DEBUG:
            self.prn_token(t)
        if t.map:
            self.lineno = t.map[0]
            self.content = t.content
        return self[self.idx]

    def next(self):  # noqa: A003
        if self.is_empty():
            return None
        self.idx += 1
        return self.get()

    def is_empty(self):
        return self.idx >= len(self)

    def consume_until(self, func):
        log.debug("consume_until")
        while True:
            t = self.get()
            self.next()
            if func(t):
                return

    def prn_token(self, t, lvl=0):
        attrs = ["type", "tag", "map", "content"]
        rc = {}
        for a in attrs:
            rc[a] = getattr(t, a, None)
        log.debug("token[%d]: %s%s", self.idx, " " * lvl, rc)
        if not t.children:
            return
        lvl += 2
        for c in t.children:
            self.prn_token(c, lvl)


tokens = None


class CLError(Exception):
    def __init__(self, msg, token=None, msg_extra=""):
        self.token = token
        self.lineno = tokens.lineno
        self.content = tokens.content
        self.msg = msg
        self.msg_extra = msg_extra
        log.debug("%s: %d: %s", self.__class__.__name__, self.lineno, self.msg)

    def __str__(self):
        return self.msg


class CLSyntaxError(CLError):
    pass


class CLNotFoundError(CLError):
    pass


class CLPartiallyFoundError(CLError):
    pass


xdata = []


def run(func, narg):
    data_len = len(xdata)
    xdata.append({})
    try:
        run_real(func, narg)
        rc = xdata[data_len]
        log.debug("func %s, narg %s: exit %s", func, narg, rc)
        return rc
    except Exception:
        raise
    finally:
        log.debug("func %s, narg %s: cleanup", func, narg)
        del xdata[data_len:]


def run_real(func, narg):
    count = 0
    while True:
        try:
            log.debug("func %s, narg %s: enter", func, narg)
            func()
        except CLSyntaxError:
            raise
        except CLNotFoundError as exp:
            if narg == "?" or narg == "*":
                return
            if narg == "+" and count > 0:
                return
            if count == 0:
                raise
            raise CLPartiallyFoundError(exp.msg, exp.token) from exp
        count += 1
        if narg == "?":
            return
        if isinstance(narg, int) and count == narg:
            return
        if (narg == "+" or narg == "*") and count > len(tokens):
            return


def func_name():
    return inspect.currentframe().f_back.f_code.co_name


tag2type = {
    "h1": "heading",
    "h2": "heading",
    "h3": "heading",
    "ul": "bullet_list",
    "li": "list_item",
    "p": "paragraph",
}


def do_item(tag, msg, validate):
    t = tokens.get()
    if not (t and t.type == tag2type[tag] + "_open" and t.tag == tag):
        raise CLNotFoundError(msg, t)
    if validate:
        validate(msg)
    tokens.consume_until(
        lambda x: x.tag == tag
        and x.type == tag2type[tag] + "_close"
        and x.level == t.level
    )


def title():
    msg = "expected 'Changelog'"

    def _validate(msg):
        t = tokens.next()
        log.info("title: %s", t.content)
        if t.content != "Changelog":
            m1 = "bad title"
            raise CLSyntaxError(m1, t, msg)
        xdata[-1]["title"] = t.content

    do_item("h1", msg, _validate)


def notes():
    def _validate(msg):  # noqa: ARG001
        t = tokens.next()
        t.content.replace("\n", " ")
        obj = xdata[-1]
        size = obj.get("notes", 0)
        size += len(t.content)
        obj["notes"] = size

    do_item("p", "", _validate)


def release_header():
    msg = "expected '[Unreleased]' or '[ver] - YYYY-MM-DD'"
    msgr = "expected '[ver] - YYYY-MM-DD'"

    def _validate(msg):
        t = tokens.next()
        log.info("release: %s", t.content)
        kids_num_unreleased = 3
        kids_num_released = 4
        if not (
            len(t.children) >= kids_num_unreleased
            and t.children[0].type == "link_open"
            and t.children[0].attrs.get("href")
        ):
            m1 = "no link for release"
            raise CLSyntaxError(m1, t)
        rname = t.children[1].content
        log.debug("rname '%s'", rname)
        if rname is None:
            m1 = "bad release title"
            raise CLSyntaxError(m1, t, msg)
        xdata[-1]["name"] = rname

        if rname == "Unreleased":
            if len(t.children) != kids_num_unreleased:
                m1 = "bad release title"
                raise CLSyntaxError(m1, t, msg)
            return
        if len(t.children) != kids_num_released:
            m1 = "bad release title"
            raise CLSyntaxError(m1, t, msg)
        rdate = t.children[3].content
        log.debug("rdate '%s'", rdate)
        if not re.search("^ - \\d\\d\\d\\d-\\d\\d-\\d\\d$", rdate):
            m1 = "bad release date"
            raise CLSyntaxError(m1, t, msgr)
        xdata[-1]["date"] = rdate.split()[-1]

    do_item("h2", msg, _validate)


def change():
    msg = "expecting list item"
    do_item("li", msg, None)
    count = xdata[-1].get("num", 0)
    xdata[-1]["num"] = count + 1


def change_list():
    msg = "expecting unordered list"

    def _validate(msg):  # noqa: ARG001
        tokens.next()
        rc = run(change, narg="+")
        xdata[-1].update(rc)

    do_item("ul", msg, _validate)


change_type_names = [
    "Added",
    "Changed",
    "Deprecated",
    "Removed",
    "Fixed",
    "Security",
]
change_type_len = max([len(k) for k in change_type_names])


def change_type():
    msg = "expecting '### <Change Type>'"

    def _validate(msg):
        t = tokens.next()
        log.debug("change type: %s", t.content)
        msg += "; got '%s'" % t.content
        if t.content not in change_type_names:
            m1 = "bad change type"
            raise CLSyntaxError(m1, t, "expected one of %s" % change_type_names)
        xdata[-1]["type"] = t.content.lower()

    do_item("h3", msg, _validate)


def change_block():
    rc = run(change_type, narg=1)
    try:
        rc.update(run(change_list, narg="+"))
    except CLNotFoundError as exp:
        raise CLSyntaxError(exp.msg, exp.token) from exp
    log.debug("change_block rc: %s", rc)
    num = xdata[-1].get(rc["type"], 0)
    xdata[-1][rc["type"]] = rc["num"] + num


def release():
    rel = {}
    rc = run(release_header, narg=1)
    rel.update(rc)

    rc = run(notes, narg="*")
    rel.update(rc)

    rc = run(change_block, narg="*")
    rel["changes"] = rc
    log.debug("release: %s", rel)
    arr = xdata[-1].get("rels", [])
    arr.append(rel)
    xdata[-1]["rels"] = arr


def check_changelog(text):
    md = MarkdownIt("commonmark", {"breaks": True, "html": True})
    global tokens  # noqa: PLW0603
    tokens = Tokens(md.parse(text))

    xdata.append({"releases": []})
    rc = run(title, narg=1)
    xdata[-1].update(rc)
    rc = run(notes, narg="*")
    xdata[-1].update(rc)
    rc = run(release, narg="+")
    xdata[-1]["releases"] += rc["rels"]
    log.debug("xdata: %s", xdata)
    rc = xdata.pop()
    log.debug("final rc: %s", prettify(rc))

    if tokens.is_empty() or tokens.get().tag == "hr":
        return rc
    msg = "out of context"
    raise CLSyntaxError(msg, tokens.get())


def check_changelog_main(fname, text):
    try:
        return check_changelog(text)
    except (CLSyntaxError, CLNotFoundError) as exp:
        log.error(
            "%s:%d: %s; got '%s'%s",
            fname,
            exp.lineno,
            exp.msg,
            exp.content,
            "; " + exp.msg_extra if exp.msg_extra else "",
        )
        return False
    except Exception as exp:
        log.error("%s", exp)
        raise
