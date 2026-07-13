"""
OCR Factory

Responsible for creating OCR engine instances.

Supported OCR Engines:
- GOT-OCR
- TrOCR
- PaddleOCR
- Docling
"""

from importlib import import_module


class OCRFactory:

    _ENGINES = {
        "got": ("utils.ocr.ocrList.got_ocr", "GOTOCR"),
        "trocr": ("utils.ocr.ocrList.trocr", "TrOCR"),
        "paddle": ("utils.ocr.ocrList.paddle_ocr", "PaddleOCREngine"),
        "docling": ("utils.ocr.ocrList.docling_ocr", "DoclingOCR"),
        "rapid": ("utils.ocr.ocrList.rapid_ocr", "RapidOCREngine"),
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

        module_name, class_name = cls._ENGINES[engine_name]

        try:
            module = import_module(module_name)
            engine_class = getattr(module, class_name)
        except ImportError as exc:
            raise ImportError(
                f"Unable to load OCR engine '{engine_name}'. "
                f"Install the required dependencies: {exc}"
            ) from exc

        return engine_class()