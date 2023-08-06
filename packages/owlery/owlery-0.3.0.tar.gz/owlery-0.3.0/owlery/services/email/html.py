import typing as t


class HTMLElement:
    """HTML element."""

    def __init__(
        self,
        tag: str,
        text: t.Optional[str] = None,
        parent: t.Optional["HTMLElement"] = None,
        **attrs,
    ):
        self.tag = tag
        self.text = text
        self.parent = parent
        self.attrs = attrs
        self.children: t.List[HTMLElement] = []

    def append(self, el: "HTMLElement"):
        self.children.append(el)
        return el

    def div(self, text: t.Optional[str] = None, **attrs):
        return self.append(
            HTMLElement("div", text=text, parent=self.parent, **attrs)
        )

    def p(self, text: t.Optional[str] = None, **attrs):
        return self.append(
            HTMLElement("p", text=text, parent=self.parent, **attrs)
        )

    def span(self, text: t.Optional[str] = None, **attrs):
        return self.append(
            HTMLElement("span", text=text, parent=self.parent, **attrs)
        )

    def table(self, **attrs):
        return self.append(Table(parent=self.parent, **attrs))


class Table(HTMLElement):
    """Table."""

    def __init__(
        self,
        data: t.Optional[
            t.Union[
                t.Iterable[t.Iterable[str]],
                t.Iterable[t.Mapping[str, str]],
            ]
        ] = None,
        parent: t.Optional["HTMLElement"] = None,
        **attrs,
    ):
        if data:
            columns = set()
            for item in data:
                pass

        super().__init__("table", parent=parent, **attrs)

    def tbody(self, **attrs) -> "Tbody":
        return self.append(Tbody(parent=self.parent, **attrs))

    def tfoot(self, **attrs) -> "Tfoot":
        return self.append(Tfoot(parent=self.parent, **attrs))

    def thead(self, **attrs) -> "Thead":
        return self.append(Thead(parent=self.parent, **attrs))

    def tr(self, **attrs) -> "Tr":
        return self.append(Tr(**attrs))


class Tbody(HTMLElement):
    """Table body."""

    def __init__(
        self,
        data: t.Optional[t.Iterable[t.Any]] = None,
        parent: t.Optional["HTMLElement"] = None,
        **attrs,
    ):
        if data:
            self.tr(data)

        super().__init__("tbody", parent=parent, **attrs)

    def tr(self, data: t.Optional[t.Iterable[t.Any]] = None, **attrs) -> "Tr":
        return self.append(Tr(data=data, parent=self.parent, **attrs))


class Tfoot(HTMLElement):
    """Table footer."""

    def __init__(
        self,
        data: t.Optional[t.Iterable[t.Any]] = None,
        parent: t.Optional["HTMLElement"] = None,
        **attrs,
    ):
        if data:
            self.tr(data)

        super().__init__("tfoot", parent=parent, **attrs)

    def tr(self, data: t.Optional[t.Iterable[t.Any]] = None, **attrs) -> "Tr":
        return self.append(
            Tr(data=data, head=True, parent=self.parent, **attrs)
        )


class Thead(HTMLElement):
    """Table header."""

    def __init__(
        self,
        data: t.Optional[t.Iterable[t.Any]] = None,
        parent: t.Optional["HTMLElement"] = None,
        **attrs,
    ):
        if data:
            self.tr(data)

        super().__init__("thead", parent=parent, **attrs)

    def tr(self, data: t.Optional[t.Iterable[t.Any]] = None, **attrs) -> "Tr":
        return self.append(
            Tr(data=data, head=True, parent=self.parent, **attrs)
        )


class Tr(HTMLElement):
    """Table row."""

    def __init__(
        self,
        data: t.Optional[t.Iterable[t.Any]] = None,
        parent: t.Optional["HTMLElement"] = None,
        head: bool = False,
        **attrs,
    ):
        if data:
            for item in data:
                if head:
                    self.th(item)
                else:
                    self.td(item)

        self.head = head

        super().__init__("tr", parent=parent, **attrs)

    def td(self, text: t.Optional[str] = None, **attrs):
        return self.append(
            HTMLElement("td", text=text, parent=self.parent, **attrs)
        )

    def th(self, text: t.Optional[str] = None, **attrs):
        return self.append(
            HTMLElement("th", text=text, parent=self.parent, **attrs)
        )
