from dataclasses import dataclass


@dataclass
class DocumentProfile:

    document_type: str

    digital_pdf: bool = False

    scanned_pdf: bool = False

    image: bool = False

    has_tables: bool = False

    layout_complexity: str = "simple"

    quality: str = "high"

    resolution: tuple = (0, 0)

    blur_score: float = 0

    text_density: int = 0

    brightness: float = 0

    contrast: float = 0

    recommended_engine: str = ""

    confidence: float = 0

    reason: str = ""