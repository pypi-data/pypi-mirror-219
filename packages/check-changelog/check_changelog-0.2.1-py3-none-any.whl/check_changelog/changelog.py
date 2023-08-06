"""
Parse changelog and ensure it conforms to the required structure.

See https://keepachangelog.com/en/ for details
"""

import inspect
import logging
import re

from markdown_it import MarkdownIt

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


def run(func, narg):
    log.debug("func %s, narg %s", func, narg)
    count = 0
    while True:
        try:
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
    log.debug("%s", func_name())
    msg = "expected 'Changelog'"

    def _validate(msg):
        t = tokens.next()
        log.info("title: %s", t.content)
        if t.content != "Changelog":
            m1 = "bad title"
            raise CLSyntaxError(m1, t, msg)

    do_item("h1", msg, _validate)


def notes():
    log.debug("%s", func_name())
    do_item("p", "", None)


def release_header():
    log.debug("%s", func_name())
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

    do_item("h2", msg, _validate)


def change():
    log.debug("%s", func_name())
    msg = "expecting list item"
    do_item("li", msg, None)


def change_list():
    log.debug("%s", func_name())
    msg = "expecting unordered list"

    def _validate(msg):  # noqa: ARG001
        tokens.next()
        run(change, narg="+")

    do_item("ul", msg, _validate)


def change_type():
    log.debug("%s", func_name())
    msg = "expecting '### <Change Type>'"

    def _validate(msg):
        t = tokens.next()
        log.info("change type: %s", t.content)
        msg += "; got '%s'" % t.content
        cnames = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
        if t.content not in cnames:
            m1 = "bad change type"
            raise CLSyntaxError(m1, t, "expected one of %s" % cnames)

    do_item("h3", msg, _validate)


def change_block():
    log.debug("%s", func_name())
    run(change_type, narg=1)
    try:
        run(change_list, narg="+")
    except CLNotFoundError as exp:
        raise CLSyntaxError(exp.msg, exp.token) from exp


def release():
    log.debug("%s", func_name())
    run(release_header, narg=1)
    run(notes, narg="*")
    run(change_block, narg="*")


def check_changelog(text):
    log.debug("%s", func_name())
    md = MarkdownIt("commonmark", {"breaks": True, "html": True})
    global tokens  # noqa: PLW0603
    tokens = Tokens(md.parse(text))

    run(title, narg=1)
    run(notes, narg="*")
    run(release, narg="+")

    if tokens.is_empty() or tokens.get().tag == "hr":
        return
    msg = "out of context"
    raise CLSyntaxError(msg, tokens.get())
