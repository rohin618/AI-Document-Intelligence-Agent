import gc

from rapidocr import RapidOCR

from ..base_ocr import BaseOCR


class RapidOCREngine(BaseOCR):

    def __init__(self):
        super().__init__()

    # -----------------------------------------
    # Load Model
    # -----------------------------------------
    def load_model(self):

        print("\nLoading RapidOCR...")

        self.model = RapidOCR()

        print("RapidOCR Loaded Successfully!")

    # -----------------------------------------
    # OCR
    # -----------------------------------------
    def extract_text(self, image_path: str) -> str:

        try:

            self.load_model()

            print("Running OCR...")

            result = self.model(image_path)

            lines = []

            if result:

                # Different RapidOCR versions return
                # slightly different formats.
                if isinstance(result, tuple):
                    result = result[0]

                for item in result:

                    # Object format
                    if hasattr(item, "txt"):
                        lines.append(item.txt)

                    # Tuple/List format
                    elif isinstance(item, (list, tuple)):

                        if len(item) >= 2:

                            text = item[1]

                            if isinstance(text, str):
                                lines.append(text)

                            elif isinstance(text, (list, tuple)):
                                lines.append(text[0])

            return "\n".join(lines)

        except Exception as e:
            raise RuntimeError(f"RapidOCR failed: {e}")

        finally:
            self.unload_model()

    # -----------------------------------------
    # Release Memory
    # -----------------------------------------
    def unload_model(self):

        print("\nUnloading RapidOCR...")

        if self.model is not None:
            del self.model
            self.model = None

        gc.collect()

        print("Memory Released!")