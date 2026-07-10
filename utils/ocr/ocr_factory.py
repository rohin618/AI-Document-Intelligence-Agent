"""
OCR Factory

Responsible for creating OCR engine instances.

Supported OCR Engines:
- GOT-OCR
- TrOCR
- PaddleOCR
- Docling
"""

from .docling_ocr import DoclingOCR
from .got_ocr import GOTOCR
from .paddle_ocr import PaddleOCREngine
from .trocr import TrOCR
from .rapid_ocr import RapidOCREngine


class OCRFactory:

    _ENGINES = {
        "got": GOTOCR,
        "trocr": TrOCR,
        "paddle": PaddleOCREngine,
        "docling": DoclingOCR,
        "rapid": RapidOCREngine,
    }

    @classmethod
    def get_engine(cls, engine_name: str):

        engine_name = engine_name.lower().strip()

        if engine_name not in cls._ENGINES:
            supported = ", ".join(cls._ENGINES.keys())

            raise ValueError(
                f"Unsupported OCR Engine: '{engine_name}'. "
                f"Supported engines: {supported}"
            )

        return cls._ENGINES[engine_name]()