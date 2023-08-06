from typing import Union

from .tags import BaseTag, ChildlessTagMixin, Tag_str


class Component(ChildlessTagMixin, BaseTag):
    _tag_name = ""

    def __init__(self) -> None:
        super().__init__()

    def add(self, tags: Union[BaseTag, list[BaseTag]]) -> __qualname__:
        raise NotImplementedError("Override add() for adding additional children")

    def content(self) -> Union[BaseTag, list[BaseTag]]:
        raise NotImplementedError("Add the component content")

    def _restructure(self):
        content = self.content()
        if not isinstance(content, list):
            content = [content]
        if len(self.children) == 0:
            self.children.extend(content)

    def html(self) -> Tag_str:
        self._restructure()
        return Tag_str("", "")
