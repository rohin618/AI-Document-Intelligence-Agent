"""
OCR Module

This module exposes a single function:

    extract_text()

Internally it uses the OCR Factory to select
the appropriate OCR engine.

The rest of the application should only import
this file.
"""

from .ocrFactory.ocr_factory import OCRFactory


def extract_text(
    image_path: str,
    engine: str = "got"
) -> str:
    """
    Extract text from an image using the selected OCR engine.

    Parameters
    ----------
    image_path : str
        Path to the image.

    engine : str
        OCR engine to use.

        Supported:
            - got
            - trocr

    Returns
    -------
    str
        Extracted OCR text.
    """

    ocr = OCRFactory.get_engine(engine)

    return ocr.extract_text(image_path)