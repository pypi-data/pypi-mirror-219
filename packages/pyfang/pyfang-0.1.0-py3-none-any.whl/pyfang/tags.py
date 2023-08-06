from __future__ import annotations
from typing import Union

from .attributes import (
    Tag_str,
    Attr,
    DefaultAttr,
    RawAttr,
    HTMLAttr,
    LinkAttr,
    MetaAttr,
    VisibleAttr,
    AAttr,
    ImgAttr,
    ScriptAttr,
    CanvasAttr,
)


class UndefinedStyleWarning(RuntimeWarning):
    ...


class BaseTag:
    def __init__(
        self, style: Union[str, list[str]] = [], attr: Attr = DefaultAttr()
    ) -> None:
        self.attr = attr
        if isinstance(style, str):
            style = style.split(" ")
        self.style = style
        self.children = []

    def add(self, tags: Union[BaseTag, list[BaseTag]]) -> __qualname__:
        assert tags is not None and tags != [], f"Invalid Tags {tags}"
        if not isinstance(tags, list):
            tags = [tags]
        self.children.extend(tags)
        return self

    def html(self) -> Tag_str:
        class_name = ""
        # for style in self.style:
        #     if style not in BaseStyle.global_style_list:
        #         warnings.warn(f'"{style}" is not defined', UndefinedStyleWarning)
        if hasattr(self, "style") and len(self.style) > 0:
            class_name = f"class=\"{' '.join(self.style)}\" "
        return Tag_str(
            f"<{self._tag_name} {class_name}{self.attr}>", f"</{self._tag_name}>"
        )

    def compile(self) -> str:
        tagstack = []
        html = ""
        tagstack.append([self, False])
        while len(tagstack) > 0:
            node, visited = tagstack[-1]
            if not visited:
                # print(node._tag_name, node.html().start)
                html = "".join((html, node.html().start))
                tagstack[-1][1] = True

                for child in node.children[::-1]:
                    tagstack.append([child, 0])
            else:
                html = "".join((html, node.html().close))
                tagstack.pop()

        return html

    def save(self, html_name) -> None:
        html = self.compile()
        with open(html_name + ".html", "w") as f:
            f.write(html)

    def __str__(self) -> str:
        return f"<{self._tag_name}>"


class RawTag(BaseTag):
    def __init__(self, tag_name: str, style: str = [], attr: Attr = RawAttr()) -> None:
        super().__init__(style, attr)
        self._tag_name = tag_name


class ChildlessTagMixin:
    def add(self, tags: Union[BaseTag, list[BaseTag]]) -> __qualname__:
        raise NotImplementedError(f"{self} does not provide an add method")


class TextMixin:
    def html(self) -> Tag_str:
        class_name = ""
        if hasattr(self, "style") and len(self.style) > 0:
            class_name = f"class=\"{', '.join(self.style)}\" "
        return Tag_str(
            f"<{self._tag_name} {class_name}{self.attr}>{self.text}",
            f"</{self._tag_name}>",
        )


class Null(BaseTag):
    _tag_name = ""

    def __init__(self) -> None:
        super().__init__()

    def html(self) -> Tag_str:
        return Tag_str("", "")


# root
class HTML(BaseTag):
    _tag_name = "html"

    def __init__(self, attr: Attr = HTMLAttr()) -> None:
        super().__init__(attr=attr)

    def add(self, head: Head = None, body: Body = None) -> __qualname__:
        tags = []
        if head:
            tags.append(head)
        if body:
            tags.append(body)
        return super().add(tags)


# Document Metadata
class Head(BaseTag):
    _tag_name = "head"

    def __init__(self, attr: Attr = DefaultAttr()) -> None:
        super().__init__(attr=attr)


class Link(ChildlessTagMixin, BaseTag):
    _tag_name = "link"

    def __init__(self, attr: Attr = LinkAttr()) -> None:
        super().__init__(attr=attr)


class Meta(ChildlessTagMixin, BaseTag):
    _tag_name = "meta"

    def __init__(self, attr=MetaAttr.setCharset()) -> None:
        super().__init__(attr=attr)


class Title(ChildlessTagMixin, TextMixin, BaseTag):
    _tag_name = "title"

    def __init__(self, title: str) -> None:
        super().__init__()
        self.text = title


# Sectioning root
class Body(BaseTag):
    _tag_name = "body"

    def __init__(self, attr: Attr = DefaultAttr()) -> None:
        super().__init__(attr=attr)


# Content sectioning
class Nav(BaseTag):
    _tag_name = "nav"

    def __init__(
        self, style: Union[str, list[str]] = [], attr: Attr = DefaultAttr()
    ) -> None:
        super().__init__(style, attr)


# Text Content
class Div(BaseTag):
    _tag_name = "div"

    def __init__(
        self, style: Union[str, list[str]] = [], attr: Attr = VisibleAttr()
    ) -> None:
        super().__init__(style, attr)


class TextTag(TextMixin, BaseTag):
    def __init__(
        self,
        text: str,
        tag_name: str,
        style: Union[str, list[str]] = [],
        attr: Attr = DefaultAttr(),
    ) -> None:
        super().__init__(style, attr)
        self.text = text
        self._tag_name = tag_name

    @classmethod
    def P(
        cls, text: str, style: Union[str, list[str]] = [], attr: Attr = DefaultAttr()
    ):
        return cls(text, "p", style, attr)

    @classmethod
    def Span(
        cls, text: str, style: Union[str, list[str]] = [], attr: Attr = DefaultAttr()
    ):
        return cls(text, "span", style, attr)

    @classmethod
    def H1(
        cls, text: str, style: Union[str, list[str]] = [], attr: Attr = DefaultAttr()
    ):
        return cls(text, "h1", style, attr)

    @classmethod
    def H2(
        cls, text: str, style: Union[str, list[str]] = [], attr: Attr = DefaultAttr()
    ):
        return cls(text, "h2", style, attr)


# Inline text semantics
class A(TextMixin, BaseTag):
    _tag_name = "a"

    def __init__(
        self, text: str = "", style: Union[str, list[str]] = [], attr: Attr = AAttr()
    ) -> None:
        super().__init__(style, attr)
        self.text = text


# Image and multimedia
class Img(ChildlessTagMixin, BaseTag):
    _tag_name = "img"

    def __init__(
        self, style: Union[str, list[str]] = [], attr: Attr = ImgAttr()
    ) -> None:
        super().__init__(style, attr)

    def html(self) -> Tag_str:
        tag = super().html().start[:-1]
        return Tag_str(f"{tag}/>", "")


# Scripting
class Script(ChildlessTagMixin, BaseTag):
    _tag_name = "script"

    def __init__(self, attr: Attr = ScriptAttr()) -> None:
        super().__init__(attr=attr)


class Canvas(BaseTag):
    _tag_name = "canvas"

    def __init__(
        self, style: Union[str, list[str]] = [], attr: Attr = CanvasAttr()
    ) -> None:
        super().__init__(style, attr)
