#!/usr/bin/env python3
"""Fail a figure script that puts prose inside the artwork.

    python3 figlint.py make_fig11_1.py [more...]

Section 6 of the rules is absolute from Chapter 7 onwards: a figure carries no
sentences. What it may say about itself is axis and tick labels, row, column and
panel headings of a few words, series names labelled on the series, data labels
and readout values, and the word "illustrative". Everything else belongs in the
caption.

The rule lived only in prose, and three chapters of figures were drawn against
it with a commentary line along the bottom of each. So it is a check now. Every
string literal handed to note() or title_in() is counted, and anything longer
than the limit fails unless the script declares it as an axis label.

A script may declare legitimate long strings, which in practice means axis
labels and nothing else:

    LONG_LABELS_ALLOWED = ["word error rate on Saudi broadcast speech, percent"]

Declaring one is a decision to be defended in the review report, not a way to
silence the check.
"""
import ast
import sys

LIMIT = 6          # words


def literals(node):
    """Every string a call argument can evaluate to, including concatenation."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield node.value
    elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = list(literals(node.left))
        right = list(literals(node.right))
        if len(left) == 1 and len(right) == 1:
            yield left[0] + right[0]
    elif isinstance(node, ast.JoinedStr):
        yield ''.join(v.value for v in node.values
                      if isinstance(v, ast.Constant))


def docstrings(tree):
    """Every string node that is a docstring, so it is not artwork."""
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, 'body', [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                out.add(id(body[0].value))
    return out


DIAGNOSTIC = {'SystemExit', 'exit', 'print', 'open', 'sys'}


def diagnostics(tree):
    """Strings inside an error or a print are messages, not artwork."""
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, 'id', getattr(node.func, 'attr', ''))
        if name not in DIAGNOSTIC:
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                out.add(id(sub))
    return out


def check(path):
    tree = ast.parse(open(path, encoding='utf-8').read())
    skip = docstrings(tree) | diagnostics(tree)
    allowed = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign)
                and any(getattr(t, 'id', '') == 'LONG_LABELS_ALLOWED'
                        for t in node.targets)
                and isinstance(node.value, (ast.List, ast.Tuple))):
            for el in node.value.elts:
                allowed.update(literals(el))
    # Every string in the file is a candidate, because artwork text is as
    # often assigned to a name as passed inline. Docstrings and error
    # messages are excluded; nothing else is.
    seen, bad = set(), []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue
        if not isinstance(node.value, str) or id(node) in skip:
            continue
        text = node.value.replace('\n', ' ').strip()
        words = len(text.split())
        if words <= LIMIT or text in allowed or text in seen:
            continue
        if text.startswith('http') or text.endswith('.png'):
            continue
        seen.add(text)
        bad.append((words, text))
    return bad


if __name__ == '__main__':
    failed = 0
    for path in sys.argv[1:]:
        bad = check(path)
        if bad:
            failed += 1
            print(f'{path}: {len(bad)} string(s) of more than {LIMIT} words')
            for words, s in bad:
                print(f'    {words:2d}  {s[:96]}')
    if failed:
        sys.exit(f'{failed} script(s) put prose inside the artwork')
    print('no prose inside the artwork')
