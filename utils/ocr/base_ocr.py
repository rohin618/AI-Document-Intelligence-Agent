"""
Base OCR Interface

All OCR engines must inherit from this class.

Example:
    - GOTOCR
    - TrOCR
    - FlorenceOCR
    - DonutOCR
"""

from abc import ABC, abstractmethod
import torch


class BaseOCR(ABC):
    """
    Abstract Base Class for all OCR engines.
    """

    def __init__(self):
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    @abstractmethod
    def load_model(self):
        """
        Load the OCR model and processor.
        """
        pass

    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        """
        Extract text from an image.

        Parameters
        ----------
        image_path : str
            Path to the image.

        Returns
        -------
        str
            Extracted OCR text.
        """
        pass

    @abstractmethod
    def unload_model(self):
        """
        Release model memory.
        """
        pass