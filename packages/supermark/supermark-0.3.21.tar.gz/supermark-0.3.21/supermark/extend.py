from typing import Any, Dict, Optional, Sequence, Set, Union

from .base import Extension, ExtensionPoint
from .chunks import Chunk, MarkdownChunk, RawChunk, YAMLChunk
from .report import Report
from .write_html import HTMLTable, html_link


class ChunkExtensionPoint(ExtensionPoint):
    """They cast a raw chunk into a specialized chunk that can be transformed
    into different target formats.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)


class ChunkExtension(Extension):
    def __init__(self, chunk_class: type) -> None:
        self.chunk_class = chunk_class

    # access to chunk and raw chunk


class YamlExtension(ChunkExtension):
    """Base class for Yaml extensions."""

    def __init__(
        self, type: Union[str, Sequence[str]], chunk_class: type = YAMLChunk
    ) -> None:
        super().__init__(chunk_class)
        self.type = type

    def get_primary_type(self) -> str:
        return self.type if isinstance(self.type, str) else self.type[0]

    def __repr__(self) -> str:
        return "yaml/" + self.get_primary_type()

    def get_doc_table(
        self, example_chunks: Optional[Sequence["Chunk"]] = None
    ) -> HTMLTable:
        table: HTMLTable = HTMLTable(css_class="table")
        table.flush_row()
        table.add_row("Language", html_link("#", "YAML"))
        table.flush_row()
        table.add_row("Mandatory Attributes", "type, name, link")
        table.flush_row()
        table.add_row("Optional Attributes", "title, text")
        table.flush_row()
        table.add_row("Post-Yaml Section", "optional")
        table.flush_row()
        table.add_row("Groups", "no")
        table.flush_row()
        return table


class YamlExtensionPoint(ChunkExtensionPoint):
    """For extension that are based on Yaml chunks."""

    def __init__(self) -> None:
        super().__init__("yaml")
        self.extensions: Dict[str, YamlExtension] = {}

    def register(self, extension: YamlExtension):
        for ttype in (
            [extension.type] if isinstance(extension.type, str) else extension.type
        ):
            self.extensions[ttype] = extension

    def cast_yaml(
        self,
        raw: RawChunk,
        type: str,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
        used_extensions: Optional[Set[Extension]] = None,
    ) -> Optional[YAMLChunk]:
        if "/" in type:
            type = type.split("/")[0]
        if type in self.extensions:
            extension = self.extensions[type]
            if used_extensions is not None:
                used_extensions.add(extension)
            chunk = extension.chunk_class(raw, dictionary, page_variables)
            chunk.extension = extension
            return chunk
        else:
            print(f"no yaml type: {type}")
        return None


class TableClassExtension(Extension):
    """Base class for table class extensions."""

    def __init__(self, type: str, empty_cell: str = ""):
        self.type = type
        self.empty_cell = empty_cell

    def __repr__(self) -> str:
        return "table/" + self.type

    def get_empty_cell(self) -> str:
        return self.empty_cell

    def get_doc_table(
        self, example_chunks: Optional[Sequence["Chunk"]] = None
    ) -> HTMLTable:
        table: HTMLTable = HTMLTable()
        table.add_row("Name", str(self.type))
        table.flush_row()
        return table


class TableClassExtensionPoint(ExtensionPoint):
    def __init__(self) -> None:
        super().__init__("tableclass")
        self.extensions: Dict[str, TableClassExtension] = {}

    def register(self, extension: TableClassExtension):
        self.extensions[extension.type] = extension

    def get_table_class(
        self, type: str, used_extensions: Optional[Set[Extension]] = None
    ) -> Optional[TableClassExtension]:
        if type in self.extensions:
            extension = self.extensions[type]
            if used_extensions is not None:
                used_extensions.add(extension)
            return extension
        return None


class ParagraphExtension(ChunkExtension):
    def __init__(self, tag: str, extra_tags: Optional[Sequence[str]] = None):
        super().__init__(MarkdownChunk)
        self.tag = tag
        self.extra_tags = extra_tags

    def __repr__(self) -> str:
        return "md/" + str(self.tag)

    def get_doc_table(
        self, example_chunks: Optional[Sequence["Chunk"]] = None
    ) -> HTMLTable:
        table: HTMLTable = HTMLTable()
        table.add_row("Tag", str(self.tag))
        table.flush_row()
        return table


class ParagraphExtensionPoint(ChunkExtensionPoint):
    def __init__(self) -> None:
        super().__init__("paragraph")
        self.extensions: Dict[str, ParagraphExtension] = {}

    def register(self, extension: ParagraphExtension):
        self.extensions[extension.tag] = extension
        if extension.extra_tags is not None:
            for tag in extension.extra_tags:
                self.extensions[tag] = extension

    def cast_paragraph_class(
        self,
        raw: RawChunk,
        tag: str,
        page_variables: Dict[str, Any],
        report: Report,
        used_extensions: Optional[Set[Extension]] = None,
    ) -> Optional[MarkdownChunk]:
        if tag in self.extensions:
            extension = self.extensions[tag]
            if used_extensions is not None:
                used_extensions.add(extension)
            chunk = extension.chunk_class(raw, page_variables)
            chunk.extension = extension
            return chunk
        else:
            raw.tell(
                f"Paragraph tag :{tag}: is unknown.",
                level=YAMLChunk.WARNING,
            )
            return MarkdownChunk(raw, page_variables)
