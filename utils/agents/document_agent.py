import logging

from .engine_selector import EngineSelector

logger = logging.getLogger(__name__)


class DocumentAgent:

    def __init__(self):

        self.selector = EngineSelector()

    def choose_engine(self, file_path: str):

        decision = self.selector.select(file_path)

        profile = decision["profile"]

        logger.info("=" * 60)
        logger.info("AGENT DOCUMENT ANALYSIS")
        logger.info("=" * 60)

        logger.info(f"Document Type      : {profile.document_type}")
        logger.info(f"Digital PDF       : {profile.digital_pdf}")
        logger.info(f"Scanned PDF       : {profile.scanned_pdf}")
        logger.info(f"Has Tables        : {profile.has_tables}")
        logger.info(f"Layout Complexity : {profile.layout_complexity}")
        logger.info(f"Quality           : {profile.quality}")

        if profile.image:
            logger.info(f"Resolution        : {profile.resolution}")
            logger.info(f"Blur Score        : {profile.blur_score:.2f}")
            logger.info(f"Brightness        : {profile.brightness:.2f}")
            logger.info(f"Contrast          : {profile.contrast:.2f}")

        logger.info("-" * 60)

        logger.info(f"Selected OCR      : {decision['engine']}")
        logger.info(f"Confidence        : {decision['confidence'] * 100:.0f}%")
        logger.info(f"Reason            : {decision['reason']}")

        logger.info("=" * 60)

        return decision["engine"]