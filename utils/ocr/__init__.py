"""
OCR Package

Supported OCR Engines

- GOT-OCR
- TrOCR

Public API

    from utils.ocr import extract_text
"""

from .ocr import extract_text

__all__ = [
    "extract_text"
]