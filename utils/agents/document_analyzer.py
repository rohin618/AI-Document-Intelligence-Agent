from pathlib import Path

import cv2
import fitz
import numpy as np

from .document_profile import DocumentProfile


class DocumentAnalyzer:

    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}

    TEXT_THRESHOLD = 50

    # -----------------------------------------------------

    def analyze(self, file_path: str) -> DocumentProfile:

        path = Path(file_path)

        extension = path.suffix.lower()

        if extension == ".pdf":
            return self._analyze_pdf(path)

        if extension in self.IMAGE_EXTENSIONS:
            return self._analyze_image(path)

        raise ValueError(f"Unsupported file type: {extension}")

    # -----------------------------------------------------

    def _analyze_pdf(self, path: Path):

        profile = DocumentProfile(document_type="pdf")

        document = fitz.open(path)

        page = document[0]

        text = page.get_text()

        profile.text_density = len(text)

        profile.digital_pdf = len(text.strip()) > self.TEXT_THRESHOLD

        profile.scanned_pdf = not profile.digital_pdf

        # Detect tables (PyMuPDF >= 1.23)
        try:

            tables = page.find_tables()

            profile.has_tables = len(tables.tables) > 0

        except:

            profile.has_tables = False

        blocks = page.get_text("blocks")

        if len(blocks) > 20:

            profile.layout_complexity = "complex"

        else:

            profile.layout_complexity = "simple"

        document.close()

        return profile

    # -----------------------------------------------------

    def _analyze_image(self, path: Path):

        profile = DocumentProfile(document_type="image")

        profile.image = True

        image = cv2.imread(str(path))

        if image is None:

            raise RuntimeError("Cannot load image")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        h, w = gray.shape

        profile.resolution = (w, h)

        profile.blur_score = cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()

        profile.brightness = float(np.mean(gray))

        profile.contrast = float(np.std(gray))

        # Quality

        if (

            w < 1000

            or h < 1000

            or profile.blur_score < 100

        ):

            profile.quality = "low"

        else:

            profile.quality = "high"

        # Layout estimation

        edges = cv2.Canny(gray, 80, 150)

        complexity = np.sum(edges > 0)

        if complexity > 15000:

            profile.layout_complexity = "complex"

        else:

            profile.layout_complexity = "simple"

        return profile