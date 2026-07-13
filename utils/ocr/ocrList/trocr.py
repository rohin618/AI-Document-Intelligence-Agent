import gc
import time
import torch
from PIL import Image
from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel,
)

from ..base_ocr import BaseOCR


class TrOCR(BaseOCR):

    MODEL_NAME = "microsoft/trocr-base-printed"

    def __init__(self):
        super().__init__()

    # --------------------------------------------------
    # Load Model
    # --------------------------------------------------
    def load_model(self):

        print(f"\nLoading TrOCR on {self.device}...")

        self.processor = TrOCRProcessor.from_pretrained(
            self.MODEL_NAME
        )

        self.model = VisionEncoderDecoderModel.from_pretrained(
            self.MODEL_NAME
        )

        self.model.to(self.device)
        self.model.eval()

        print("TrOCR Loaded Successfully!")

    # --------------------------------------------------
    # OCR
    # --------------------------------------------------
    def extract_text(self, image_path: str) -> str:

        image = None
        pixel_values = None
        generated_ids = None

        try:

            self.load_model()

            # -----------------------------
            # Load Image
            # -----------------------------
            image = Image.open(image_path).convert("RGB")

            print(f"Original Image Size : {image.size}")

            # Resize very large images
            if image.width > 1600 or image.height > 1600:
                image.thumbnail((1600, 1600))
                print(f"Resized Image Size : {image.size}")

            print("Preparing image for OCR...")

            pixel_values = self.processor(
                images=image,
                return_tensors="pt"
            ).pixel_values.to(self.device)

            print("Running OCR...")

            start = time.time()

            with torch.inference_mode():

                generated_ids = self.model.generate(
                    pixel_values,
                    max_new_tokens=512
                )

            end = time.time()

            print(f"OCR completed in {end-start:.2f} seconds")

            text = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=True
            )[0]

            return text.strip()

        except Exception as e:
            raise RuntimeError(f"TrOCR failed: {e}")

        finally:

            if image is not None:
                del image

            if pixel_values is not None:
                del pixel_values

            if generated_ids is not None:
                del generated_ids

            self.unload_model()

    # --------------------------------------------------
    # Release Memory
    # --------------------------------------------------
    def unload_model(self):

        print("\nUnloading TrOCR...")

        if self.model is not None:
            del self.model
            self.model = None

        if self.processor is not None:
            del self.processor
            self.processor = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        gc.collect()

        print("Memory Released!")