from .document_analyzer import DocumentAnalyzer
from .rules import OCRDecisionRules


class EngineSelector:

    def __init__(self):

        self.analyzer = DocumentAnalyzer()
        self.rules = OCRDecisionRules()

    def select(self, file_path: str):

        # Step 1: Analyze document
        profile = self.analyzer.analyze(file_path)

        # Step 2: Apply business rules
        profile = self.rules.select_engine(profile)

        # Step 3: Return decision
        return {

            "engine": profile.recommended_engine,

            "confidence": profile.confidence,

            "reason": profile.reason,

            "profile": profile

        }