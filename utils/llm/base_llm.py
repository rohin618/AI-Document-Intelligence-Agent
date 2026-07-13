from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    def extract_invoice_json(self, ocr_text: str):
        pass