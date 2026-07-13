import gc

from paddleocr import PaddleOCR

from ..base_ocr import BaseOCR


class PaddleOCREngine(BaseOCR):

    def __init__(self):
        super().__init__()

    # -----------------------------------------
    # Load Model
    # -----------------------------------------
    def load_model(self):

        print("\nLoading PaddleOCR...")

        self.model = PaddleOCR(
            use_angle_cls=True,
            lang="en",
            use_gpu=False
        )

        print("PaddleOCR Loaded Successfully!")

    # -----------------------------------------
    # OCR
    # -----------------------------------------
    def extract_text(self, image_path: str) -> str:

        try:

            self.load_model()

            print("Running OCR...")

            result = self.model.ocr(
                image_path,
                cls=True
            )

            lines = []

            if result:

                for page in result:

                    if page is None:
                        continue

                    for line in page:

                        text = line[1][0]
                        lines.append(text)

            return "\n".join(lines)

        except Exception as e:
            raise RuntimeError(f"PaddleOCR failed: {e}")

        finally:
            self.unload_model()

    # -----------------------------------------
    # Release Memory
    # -----------------------------------------
    def unload_model(self):

        print("\nUnloading PaddleOCR...")

        if self.model is not None:
            del self.model
            self.model = None

        gc.collect()

        print("Memory Released!")