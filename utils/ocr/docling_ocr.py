"""
Docling OCR Engine

Uses IBM Docling to extract structured text from PDF documents.
"""

from pathlib import Path

from docling.document_converter import DocumentConverter

from .base_ocr import BaseOCR


class DoclingOCR(BaseOCR):
    """OCR implementation using IBM Docling."""

    def __init__(self):
        self.converter: DocumentConverter | None = None

    # -----------------------------------------
    # Load Model
    # -----------------------------------------
    def load_model(self) -> None:
        """Load the Docling converter."""

        if self.converter is None:
            print("Loading Docling...")
            self.converter = DocumentConverter()

    # -----------------------------------------
    # Extract Text
    # -----------------------------------------
    def extract_text(self, file_path: str) -> str:
        """
        Extract structured text from a PDF using Docling.

        Args:
            file_path: Path to the PDF.

        Returns:
            Markdown representation of the document.
        """

        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        self.load_model()

        try:
            result = self.converter.convert(file_path)

            if result is None or result.document is None:
                raise RuntimeError("Docling returned an empty document.")

            text = result.document.export_to_markdown().strip()

            if not text:
                raise RuntimeError("No text extracted from document.")

            return text

        except Exception as e:
            raise RuntimeError(f"Docling OCR failed: {e}") from e

    # -----------------------------------------
    # Unload Model
    # -----------------------------------------
    def unload_model(self) -> None:
        """Unload the Docling converter."""

        if self.converter is not None:
            del self.converter
            self.converter = None
            print("Docling unloaded.")