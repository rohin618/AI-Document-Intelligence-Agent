import gc
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

from ..base_ocr import BaseOCR


class GOTOCR(BaseOCR):

    MODEL_NAME = "stepfun-ai/GOT-OCR-2.0-hf"

    def __init__(self):
        super().__init__()

    # --------------------------------------------------
    # Load Model
    # --------------------------------------------------
    def load_model(self):

        print(f"\nLoading GOT-OCR on {self.device}...")

        self.processor = AutoProcessor.from_pretrained(
            self.MODEL_NAME
        )

        self.model = AutoModelForImageTextToText.from_pretrained(
            self.MODEL_NAME
        )

        self.model.to(self.device)

        print("GOT-OCR Loaded Successfully!")

    # --------------------------------------------------
    # OCR
    # --------------------------------------------------
    def extract_text(self, image_path: str) -> str:

        image = None
        inputs = None
        generated_ids = None

        try:

            # Load model only when needed
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

            inputs = self.processor(
                image,
                return_tensors="pt"
            ).to(self.device)

            print("Running OCR...")

            with torch.inference_mode():

                generated_ids = self.model.generate(
                    **inputs,
                    do_sample=False,
                    tokenizer=self.processor.tokenizer,
                    stop_strings="<|im_end|>",
                    max_new_tokens=1024,
                )

            text = self.processor.decode(
                generated_ids[0, inputs["input_ids"].shape[1]:],
                skip_special_tokens=True,
            )

            return text.strip()

        except Exception as e:
            raise RuntimeError(f"GOT-OCR failed: {e}")

        finally:

            if image is not None:
                del image

            if inputs is not None:
                del inputs

            if generated_ids is not None:
                del generated_ids

            self.unload_model()

    # --------------------------------------------------
    # Release Memory
    # --------------------------------------------------
    def unload_model(self):

        print("\nUnloading GOT-OCR...")

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