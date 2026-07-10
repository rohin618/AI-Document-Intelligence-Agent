"""
Invoice Prompt

Optimized for Qwen2.5-0.5B-Instruct
"""

# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are an expert Accounts Payable invoice extraction assistant.

Your task is to extract invoice information from OCR text.

Rules:

1. Return ONLY valid JSON.
2. Do NOT return markdown.
3. Do NOT explain anything.
4. Do NOT guess missing values.
5. If a field is missing, return "".
6. Amount must be numeric.
7. Dates should remain exactly as written in the invoice.
8. Currency should be the currency code if available (INR, USD, EUR, etc.).
9. Ignore unrelated text, logos, headers and footers.
10. Output must exactly match the JSON schema.
"""

# ==========================================================
# JSON SCHEMA
# ==========================================================

JSON_SCHEMA = """
{
    "invoice_number": "",
    "invoice_date": "",
    "due_date": "",
    "supplier": "",
    "buyer": "",
    "category": "",
    "currency": "",
    "amount": 0
}
"""

# ==========================================================
# BUILD PROMPT
# ==========================================================

def build_invoice_prompt(ocr_text: str):

    return [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": f"""
Extract the invoice information from the OCR text.

Return ONLY valid JSON.

Instructions:

- Follow the schema exactly.
- Do not add extra fields.
- Do not remove fields.
- Missing string values -> ""
- Missing numeric values -> 0
- Do not guess values.
- Preserve invoice number, dates and names exactly.
- Amount should be numeric only.
- Category should be one of the following if identifiable:

    IT
    Office Supplies
    Logistics
    Utilities
    Travel
    Marketing
    Maintenance
    Other

If the category cannot be identified, return:

"Other"

JSON SCHEMA

{JSON_SCHEMA}

OCR TEXT

{ocr_text}
"""
        }

    ]