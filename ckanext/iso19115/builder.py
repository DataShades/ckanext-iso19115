from __future__ import annotations

import contextlib
import contextvars
import enum
import json
import logging
import operator
import re
from typing import Any, Iterable, Optional

import exrex
import xmlschema
from faker import Faker
from xmlschema.validators import (
    XsdAnyElement,
    XsdAtomic,
    XsdElement,
    XsdGroup,
    XsdList,
    XsdType,
    XsdUnion,
)
from xmlschema.validators.complex_types import XsdComplexType

from . import utils

log = logging.getLogger(__name__)


class Validation(enum.Enum):
    strict = "strict"
    lax = "lax"
    skip = "skip"


visited = contextvars.ContextVar("visited")
recursive = contextvars.ContextVar("recursive", default=False)
depth = contextvars.ContextVar("depth", default=0)
inside_union = contextvars.ContextVar("inside_union", default=False)

faker = Faker()


@contextlib.contextmanager
def set_context(data: dict[contextvars.ContextVar[Any], Any]):
    tokens: dict[contextvars.ContextVar, contextvars.Token] = {}
    for cv, value in data.items():
        tokens[cv] = cv.set(value)
    yield
    for cv, token in tokens.items():
        cv.reset(token)


class Builder:
    root: xmlschema.XsdElement

    def __init__(self, schema: xmlschema.XMLSchema, root: str):
        el = utils.lookup(root, schema)

        assert isinstance(
            el, XsdElement
        ), "Builder root at {str} must be available"

        self.root = el

    def build(self, data):
        data["@xmlns"] = utils.ns
        el = self.root.encode(data, converter=xmlschema.BadgerFishConverter)
        return el

    def example(self, fmt: str, seed: Optional[str] = None):
        if not seed:
            seed = Faker().pystr()
        log.info("Using seed: %s", seed)
        Faker.seed(seed)

        tree = BfsTree(self.root, False, False)
        example = tree.dictize()
        if fmt == "xml":
            el = self.build(example)
            return xmlschema.etree_tostring(
                el, namespaces=utils.ns, xml_declaration=True
            )
        else:
            return json.dumps(example, indent=2)

    def print_tree(
        self, fmt, skip_optional, qualified: bool = True, max_depth: int = 0
    ):
        tree = DfsTree(self.root, skip_optional, qualified, max_depth)
        if fmt == "overview":
            print(tree)


class Tree:
    def __init__(
        self, node, skip_optional: bool, qualified: bool, max_depth: int = 0
    ):
        self.skip_optional = skip_optional
        self.qualified = qualified
        self.max_depth = max_depth
        self.node = make_node(node)

    def _yield_from_node(self, node: BaseNode):
        yield node

    def __iter__(self):
        ctx = contextvars.copy_context()
        with set_context({visited: set()}):
            yield from ctx.run(self._yield_from_node, self.node)


class BfsTree(Tree):
    def dictize(self):
        root = next(iter(self))
        return root.example()


class DfsTree(Tree):
    def _yield_from_node(self, node: BaseNode):

        if self.skip_optional and node.is_composed() and node.is_optional():
            return

        if self.max_depth and self.max_depth - 1 < depth.get():
            yield TooDeepNode(node.node)
            return

        if node.visited() and node.is_composed():
            yield RecursionNode(node.node)
            return
        yield node

        with node.visit() as children:

            for child in children:
                yield from self._yield_from_node(child)

    def __str__(self):
        return "\n".join(n.into_indent(self.qualified) for n in self)


def make_node(node: XsdType) -> BaseNode:
    if isinstance(node, XsdElement):
        return ElementNode(node)
    if isinstance(node, XsdAtomic):
        return AtomicNode(node)
    if isinstance(node, XsdUnion):
        return UnionNode(node)

    if isinstance(node, XsdList):
        return ListNode(node)
    else:
        # breakpoint()
        raise TypeError(f"Unsupported node type {node}")


class BaseNode:
    children: Iterable["BaseNode"]

    def __init__(self, node: XsdType, children=()):
        self.node = node
        self.children = map(make_node, children)

    @property
    def id(self):
        return self.node.qualified_name

    @contextlib.contextmanager
    def visit(self):
        with set_context(
            {
                recursive: self.visited(),
                depth: depth.get() + 1,
                inside_union: self.is_abstract() or self.is_union(),
            }
        ):
            visited.get().add(self.id)
            yield self.children

    def visited(self):
        return bool(self.id and self.id in visited.get())

    def name(self, qualified: bool):
        if qualified:
            return self.node.qualified_name
        return self.node.prefixed_name

    def is_optional(self):
        return self.node.is_emptiable()

    # def is_optional(self):
    #     return False

    def is_union(self):
        return False

    def is_abstract(self):
        return self.node.abstract

    def is_multiple(self):
        return False

    def is_composed(self):
        return True

    def _unwrap(self):
        root = self

        if root.is_abstract():
            with root.visit() as options:

                root = faker.random_element(
                    sorted(options, key=operator.attrgetter("id"))
                )
        return root

    def example(self) -> Any:
        assert False, "Base example is not defined"

    def into_indent(self, qualified):
        spec = ""

        if self.is_optional():
            spec = "?"

        if self.is_multiple():
            spec = "*" if spec == "?" else "+"

        name = self.name(qualified)
        if name and self.node.abstract:
            name = name.join("<>")

        indent = depth.get() * "    "

        prefix = "|" if inside_union.get() else " "

        attributes = []
        if isinstance(self.node, XsdElement):
            attributes = [
                a.prefixed_name
                for a in self.node.attributes.values()
                if a.prefixed_name and not a.prefixed_name.startswith("xlink:")
            ]
        attr_text = ", ".join(attributes)
        if attr_text:
            attr_text = f" [{attr_text}]"
        return f"{indent}{prefix}{spec}{name}{attr_text}"

    def _resolve_substitutions(self, node):
        options = set()
        subst = node.maps.substitution_groups.get(node.name, [])
        for s in subst:
            if s.abstract:
                options.update(self._resolve_substitutions(s))
            else:
                options.add(s)
        return options


class TooDeepNode(BaseNode):
    def into_indent(self, *args, **kwargs):
        value = super().into_indent(*args, **kwargs)

        return f"{value} (too deep...)"


class RecursionNode(BaseNode):
    def into_indent(self, *args, **kwargs):
        value = super().into_indent(*args, **kwargs)
        indent = (depth.get() + 1) * "    "

        return f"{value} (seen before)\n{indent}..."


class AtomicNode(BaseNode):
    def example(self):
        node = self.node.primitive_type
        ln = node.local_name

        if node.is_datetime():
            if ln == "duration":
                return faker.pystr_format("P#YT#H")

            dt = faker.date_time()
            fmt = {
                "date": "%Y-%m-%d",
                "dateTime": "%Y-%m-%dT%H:%M:%S",
                "time": "%H:%M:%S",
                "gYearMonth": "%Y-%m",
                "gYear": "%Y",
            }
            assert ln in fmt, f"Unsupported date type {ln}"

            return dt.strftime(fmt[ln])

        if node.local_name == "string":
            if self.node.patterns:
                pat = self.node.patterns.regexps[0]
                try:
                    return exrex.getone(pat)
                except re.error as e:
                    log.error(e)
                    return faker.pystr()

            return faker.sentence()
        if node.local_name == "boolean":
            return faker.pybool()
        if node.local_name in ("decimal", "double"):
            return faker.pyfloat()
        if node.local_name == "anyURI":
            return faker.uri()

        raise TypeError(f"Unsupported atomic example {node}")

    def is_composed(self):
        return False


class ElementNode(BaseNode):
    def __init__(self, node: XsdElement):

        if node.abstract:
            children = self._resolve_substitutions(node)
        else:
            children = node.type
            if isinstance(children, XsdComplexType):
                children = children.content
            if isinstance(children, XsdGroup):
                model = children.model
                children = [
                    child
                    for child in children.iter_elements()
                    if not isinstance(child, XsdAnyElement)
                ]

                # TODO: handle this
                # if model == "choice":
                # children = children[:1]

            elif isinstance(children, (XsdUnion)):
                children = children.member_types
                # children = [children.member_types[0]]
            elif isinstance(children, (XsdList, XsdAtomic, XsdUnion)):

                children = [children]
            else:
                raise TypeError(f"Node type {node} is not supported")

        super().__init__(node, children)

    def is_multiple(self):
        return not self.node.is_single()

    def is_composed(self):
        return self.node.type.is_complex()

    def example(self):
        root = self._unwrap()
        if self is not root:
            return root.example()

        if root.is_composed() and root.is_optional():
            return {}

        if self.visited() and self.is_composed():
            return {}

        data = {}

        with root.visit() as children:
            if (
                root.is_composed()
                and isinstance(root.node.type.content, XsdGroup)
                and root.node.type.content.model == "choice"
            ):
                children = [faker.random_element(children)]

            for child in children:
                child = child._unwrap()
                value = child.example()
                if value == {} and child.is_optional():
                    continue

                key = (
                    child.name(False)
                    if not isinstance(child, AtomicNode)
                    else "$"
                )
                data[key] = value

        for attr in root.node.attributes.values():
            if attr.use == "required":
                value = make_node(attr.type).example()
                if isinstance(value, dict):
                    value = value["$"]

                data["@" + attr.name] = value

            # if attr.local_name == "nilReason":
            # data["@" + attr.name] = "missing"

        local_name = root.node.local_name
        if local_name in utils.codelist_names():
            options = utils.codelist_options(local_name)
            valid_code = faker.random_element(options)
            data["@codeListValue"] = valid_code.name
            # XXX: debug
            if local_name == "CI_DateTypeCode":
                data["@codeListValue"] = "creation"
            data["@codeList"] = valid_code.location

        return data


class UnionNode(BaseNode):
    def __init__(self, node: XsdUnion, children=None):
        if not children:
            children = node.member_types
        super().__init__(node, children)

    def is_union(self):
        return True

    def example(self):
        with self.visit() as options:
            choice = faker.random_element(options)
            example = choice.example()
            return example if choice.is_composed() else {"$": example}


class ListNode(BaseNode):
    def __init__(self, node: XsdList):
        children = [node.base_type]
        super().__init__(node, children)

    def is_multiple(self):
        return True

    def example(self):
        component = AtomicNode(self.node.base_type)
        return [component.example() for _ in range(faker.random_digit())]
