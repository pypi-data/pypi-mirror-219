from collections import namedtuple
from dataclasses import dataclass

Tag_str = namedtuple("Tag_str", ["start", "close"])


class MetaName:
    VIEWPORT = "viewport"
    AUTHOR = "author"
    DESCRIPTION = "description"
    GOOGLE_SITE_VERIFICATION = "google-site-verification"


class Rel:
    STYLESHEET = "stylesheet"


class Attr:
    def __init__(self) -> None:
        ...

    def __str__(self) -> str:
        return " ".join(
            [f'{key}="{val}"' for key, val in vars(self).items() if val is not None]
        )


class RawAttr(Attr):
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)


@dataclass
class HTMLAttr(Attr):
    lang: str = "en"


@dataclass
class MetaAttr(Attr):
    name: str = None
    content: str = None
    charset: str = None

    @classmethod
    def setCharset(cls, charset: str = "UTF-8") -> None:
        return cls(None, None, charset)


@dataclass
class VisibleAttr(Attr):
    id: str = None
    name: str = None


@dataclass
class TextAttr(Attr):
    id: str = None
    name: str = None


@dataclass
class LinkAttr(Attr):
    href: str = None
    rel: str = None


@dataclass
class ScriptAttr(Attr):
    src: str = None
    integrity: str = None
    crossorigin: str = None
    referrerpolicy: str = None


@dataclass
class AAttr(Attr):
    href: str = None
    target: str = None


@dataclass
class ImgAttr(Attr):
    src: str = None


@dataclass
class CanvasAttr(Attr):
    id: str = None
    name: str = None
    width: str = None
    height: str = None


@dataclass
class DefaultAttr(Attr):
    """
    Default HTML Attribute class, some attributes are renamed as they are keywords in python.
    async -> async_
    class -> class
    for -> for_
    """

    accept: str = None
    accesskey: str = None
    action: str = None
    alt: str = None
    async_: str = None
    autocomplete: str = None
    autofocus: str = None
    autoplay: str = None
    charset: str = None
    checked: str = None
    cite: str = None
    class_: str = None
    cols: str = None
    colspan: str = None
    content: str = None
    contenteditable: str = None
    controls: str = None
    coords: str = None
    data: str = None
    data: str = None
    datetime: str = None
    default: str = None
    defer: str = None
    dir: str = None
    dirname: str = None
    disabled: str = None
    download: str = None
    draggable: str = None
    enctype: str = None
    for_: str = None
    form: str = None
    formaction: str = None
    headers: str = None
    height: str = None
    hidden: str = None
    high: str = None
    href: str = None
    hreflang: str = None
    http: str = None
    id: str = None
    ismap: str = None
    kind: str = None
    label: str = None
    lang: str = None
    list: str = None
    loop: str = None
    low: str = None
    max: str = None
    maxlength: str = None
    media: str = None
    method: str = None
    min: str = None
    multiple: str = None
    muted: str = None
    name: str = None
    novalidate: str = None
    onabort: str = None
    onafterprint: str = None
    onbeforeprint: str = None
    onbeforeunload: str = None
    onblur: str = None
    oncanplay: str = None
    oncanplaythrough: str = None
    onchange: str = None
    onclick: str = None
    oncontextmenu: str = None
    oncopy: str = None
    oncuechange: str = None
    oncut: str = None
    ondblclick: str = None
    ondrag: str = None
    ondragend: str = None
    ondragenter: str = None
    ondragleave: str = None
    ondragover: str = None
    ondragstart: str = None
    ondrop: str = None
    ondurationchange: str = None
    onemptied: str = None
    onended: str = None
    onerror: str = None
    onfocus: str = None
    onhashchange: str = None
    oninput: str = None
    oninvalid: str = None
    onkeydown: str = None
    onkeypress: str = None
    onkeyup: str = None
    onload: str = None
    onloadeddata: str = None
    onloadedmetadata: str = None
    onloadstart: str = None
    onmousedown: str = None
    onmousemove: str = None
    onmouseout: str = None
    onmouseover: str = None
    onmouseup: str = None
    onmousewheel: str = None
    onoffline: str = None
    ononline: str = None
    onpagehide: str = None
    onpageshow: str = None
    onpaste: str = None
    onpause: str = None
    onplay: str = None
    onplaying: str = None
    onpopstate: str = None
    onprogress: str = None
    onratechange: str = None
    onreset: str = None
    onresize: str = None
    onscroll: str = None
    onsearch: str = None
    onseeked: str = None
    onseeking: str = None
    onselect: str = None
    onstalled: str = None
    onstorage: str = None
    onsubmit: str = None
    onsuspend: str = None
    ontimeupdate: str = None
    ontoggle: str = None
    onunload: str = None
    onvolumechange: str = None
    onwaiting: str = None
    onwheel: str = None
    open: str = None
    optimum: str = None
    pattern: str = None
    placeholder: str = None
    poster: str = None
    preload: str = None
    readonly: str = None
    rel: str = None
    required: str = None
    reversed: str = None
    rows: str = None
    rowspan: str = None
    sandbox: str = None
    scope: str = None
    selected: str = None
    shape: str = None
    size: str = None
    sizes: str = None
    span: str = None
    spellcheck: str = None
    src: str = None
    srcdoc: str = None
    srclang: str = None
    srcset: str = None
    start: str = None
    step: str = None
    style: str = None
    tabindex: str = None
    target: str = None
    title: str = None
    translate: str = None
    type: str = None
    usemap: str = None
    value: str = None
    width: str = None
    wra: str = None
