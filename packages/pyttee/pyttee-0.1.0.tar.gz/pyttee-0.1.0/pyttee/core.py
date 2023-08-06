
# core.py

from pyttee.parser import parse_tag
from pyttee.compiler import compile_tag


def run_template(template: list, printer):
    if not template:
        return

    tag = parse_tag(template)
    compile_tag(tag, printer)
