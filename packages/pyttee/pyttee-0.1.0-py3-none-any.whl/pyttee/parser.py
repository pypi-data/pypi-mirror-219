
from pyttee.models import Tag


def parse_rule_with_props(this_tag: Tag, rule: list):
    rule_len = len(rule)
    second_elem = rule[1]
    this_tag.props = second_elem

    if rule_len > 3:
        for r in rule[2:]:
            t = parse_tag(r)
            this_tag.children.append(t)
    else:
        this_tag.children = [parse_tag(rule[2])]


def parse_tag(rule: list | str) -> Tag | str:
    if type(rule) == str:
        return rule

    rule_len = len(rule)
    this_tag: Tag = Tag.default_factory()

    if rule_len <= 1:
        raise NotImplemented(
            "Parsing of rule represented by a list of one or less element"
        )

    this_tag.name = rule[0]

    if rule_len > 2:
        second_elem = rule[1]
        is_rule_has_props = type(second_elem) == dict

        if is_rule_has_props:
            parse_rule_with_props(this_tag, rule)
        else:
            for child in rule[1:]:
                t = parse_tag(child)
                this_tag.children.append(t)

        return this_tag

    this_tag.children.append(parse_tag(rule[1]))
    return this_tag


if __name__ == "__main__":
    template_1 = ["h1", "meow"]
    template_2 = ["body", ["meow", "owo"], ["h1", ["h2", "owo"]]]
    template_3 = ["body", {"color": "red", "align": "center"}, template_2]
    print(parse_tag(template_3))
