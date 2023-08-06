
from pyttee.models import Tag
from typing import Callable


def compile_tag(tag: Tag, printer: Callable[[str], None]):

    first_tag = f"<{tag.name}"

    if tag.props:
        for tag_property in tag.props:
            first_tag += f" {tag_property}='{tag.props[tag_property]}'"

    first_tag += ">"
    printer(first_tag)

    for child in tag.children:
        if type(child) == str:
            printer(child)
            continue

        compile_tag(child, printer)

    printer(f"</{tag.name}>")

