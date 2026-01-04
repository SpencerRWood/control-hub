from __future__ import annotations

from dataclasses import dataclass

from docling.document_converter import DocumentConverter


@dataclass(frozen=True)
class ParsedDoc:
    markdown: str
    title: str | None


class DoclingPdfParser:
    def __init__(self) -> None:
        self._converter = DocumentConverter()

    def parse(self, source_uri: str) -> ParsedDoc:
        result = self._converter.convert(source_uri)
        doc = result.document
        md = doc.export_to_markdown()
        title = getattr(getattr(doc, "metadata", None), "title", None)
        return ParsedDoc(markdown=md, title=title)
