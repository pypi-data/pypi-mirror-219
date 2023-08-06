""" shil
"""
import json
from pathlib import Path

import tatsu
from fleks.util import lme

from .grammar import bashParser

from .format import shfmt  # noqa
from .models import Invocation  # noqa
from .util import invoke  # noqa

DEBUG = True  # False
LOGGER = lme.get_logger(__name__)


class Semantics:
    def strict_word(self, ast):
        LOGGER.warning(f"strict_word: {ast}")
        return ast

    def dquote(self, ast):
        LOGGER.warning(f"dquote: {ast}")
        if len(ast) > 10:
            ast = ast.lstrip()
            return f'"\\n{ast}\\n"'
        return ast

    def squote(self, ast):
        from json import loads

        LOGGER.warning(f"squote: {ast}")
        ast = ast.strip().lstrip()
        is_json = ast.startswith("{") and ast.strip().endswith("}")
        if is_json:
            try:
                # tmp = loads.json5(ast)
                tmp = loads(ast)
            except:
                is_json = False
            else:
                LOGGER.critical(f"found json: {tmp}")
                ast = json.dumps(tmp, indent=2)
            out = [x + " \\" for x in ast.split("\n")]
            out = "\n".join(out)
            return f"'{out}'"
        return ast

    def word(self, ast):
        LOGGER.warning(f"word: {ast}")
        return ast

    def simple_command(self, ast):
        LOGGER.warning(f"simple_command: {ast}")
        tail = ast
        biggest = ""
        for i, l in enumerate(tail):
            if len(l) > len(biggest):
                biggest = l
        result = []
        skip_next = False
        for i, l in enumerate(tail):
            if skip_next:
                skip_next = False
                continue
            try:
                n = tail[i + 1]
            except:
                n = ""
                # LOGGER.warning(f'looking at {[i,l,n]}')
            comb = f"{l} {n}"
            if len(comb) < len(biggest):
                result.append(comb)
                skip_next = True
            else:
                result.append(l)
        # import IPython; IPython.embed()
        newp = []
        while result:
            item = result.pop(0)
            if isinstance(item, (tuple,)):
                item = " ".join(item)
            newp.append(item)
        result = newp
        return "\n  ".join(map(str, result))

    def shell_command(self, ast):
        LOGGER.warning(f"shell_command: {ast}")
        return ast

    def path(self, ast):
        LOGGER.warning(f"path: {ast}")
        try:
            tmp = Path(ast).relative_to(Path(".").absolute())
        except ValueError:
            return ast
        else:
            return f"'{tmp}'"

    def pipeline_command(self, ast):
        LOGGER.warning(f"pipeline_command: {ast}")
        return ast

    def simple_list(self, ast):
        LOGGER.warning(f"simple_list: {ast}")
        return ast

    def word_list(self, ast):
        LOGGER.warning(f"word_list: {ast}")
        return ast

    def opt(self, ast):
        LOGGER.warning(f"opt: {ast}")
        return ast if isinstance(ast, (str,)) else " ".join(ast)

    def opt_val(self, ast):
        LOGGER.warning(f"opt_val: {ast}")
        return ast

    def subcommands(self, ast):
        LOGGER.warning(f"subcommands: {ast}")
        return " ".join(ast)

    def drilldown(self, ast):
        LOGGER.warning(f"drilldown: {ast}")
        return ast

    def entry(self, ast):
        LOGGER.warning(f"entry: {ast}")
        return str(ast)


def fmt(text, filename="?"):
    """"""
    semantics = Semantics()
    parser = bashParser()
    try:
        parsed = parser.parse(
            text,
            parseinfo=True,
            filename=filename,
            semantics=semantics,
        )
    except (tatsu.exceptions.FailedParse,) as exc:
        LOGGER.critical(exc)
        return text
    else:
        out = []
        for item in parsed:
            if isinstance(item, (list, tuple)):
                item = " ".join([str(x) for x in item])
            out.append(item)
        head = out.pop(0)
        # tail=out.copy()
        tail = "\n  ".join(out)
        return f"{head} {tail}"


bash_fmt = fmt
