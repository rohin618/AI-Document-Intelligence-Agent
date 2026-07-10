from .document_profile import DocumentProfile


class OCRDecisionRules:

    def select_engine(self, profile: DocumentProfile):

        scores = {
            "docling": 0,
            "paddle": 0,
            "rapid": 0,
            "got": 0
        }

        reasons = []

        # ----------------------------------------
        # PDF Rules
        # ----------------------------------------

        if profile.document_type == "pdf":

            if profile.digital_pdf:
                scores["docling"] += 60
                reasons.append("Digital PDF detected")

            if profile.scanned_pdf:
                scores["paddle"] += 40
                scores["rapid"] += 30
                reasons.append("Scanned PDF detected")

            if profile.has_tables:
                scores["docling"] += 40
                reasons.append("Tables detected")

            if profile.layout_complexity == "complex":
                scores["docling"] += 20
                scores["got"] += 10
                reasons.append("Complex layout")

        # ----------------------------------------
        # Image Rules
        # ----------------------------------------

        if profile.document_type == "image":

            if profile.quality == "low":

                scores["paddle"] += 60

                reasons.append("Low quality image")

            else:

                scores["rapid"] += 50

                reasons.append("High quality image")

            if profile.layout_complexity == "complex":

                scores["got"] += 40

                reasons.append("Complex layout")

            else:

                scores["rapid"] += 20

            if profile.blur_score < 80:

                scores["paddle"] += 20

                reasons.append("Blur detected")

        # ----------------------------------------
        # Brightness
        # ----------------------------------------

        if profile.brightness < 70:

            scores["paddle"] += 15

            reasons.append("Dark document")

        # ----------------------------------------
        # Contrast
        # ----------------------------------------

        if profile.contrast < 35:

            scores["paddle"] += 10

            reasons.append("Low contrast")

        # ----------------------------------------
        # Winner
        # ----------------------------------------

        best_engine = max(scores, key=scores.get)

        confidence = scores[best_engine] / 100

        profile.recommended_engine = best_engine

        profile.confidence = round(min(confidence, 1), 2)

        profile.reason = ", ".join(reasons)

        return profile