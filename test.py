# from pathlib import Path

# from utils.agent.document_agent import DocumentAgent
# from utils.llm import extract_invoice_json
# from utils.ocr import extract_text
# from utils.pdf_converter import pdf_to_images


# # --------------------------------------------------
# # Configuration
# # --------------------------------------------------

# FILE_PATH = "invoices/invoice6.pdf"
# # FILE_PATH = "invoices/sampleInv.png"


# def main():

#     try:

#         print("\n========== AI Invoice Extraction ==========\n")

#         # ---------------------------------------------
#         # Document Agent
#         # ---------------------------------------------
#         agent = DocumentAgent()

#         selected_engine = agent.choose_engine(FILE_PATH)

#         print(f"Selected OCR Engine : {selected_engine.upper()}")

#         file_extension = Path(FILE_PATH).suffix.lower()

#         ocr_text = ""

#         # --------------------------------------------------
#         # Image
#         # --------------------------------------------------
#         if file_extension in [".png", ".jpg", ".jpeg"]:

#             print("\nInput Type : Image")

#             ocr_text = extract_text(
#                 image_path=FILE_PATH,
#                 engine=selected_engine
#             )

#         # --------------------------------------------------
#         # PDF
#         # --------------------------------------------------
#         elif file_extension == ".pdf":

#             print("\nInput Type : PDF")

#             image_paths = pdf_to_images(FILE_PATH)

#             print(f"Total Pages : {len(image_paths)}")

#             page_texts = []

#             for page_no, image_path in enumerate(image_paths, start=1):

#                 print(f"\n{'=' * 15} Page {page_no} {'=' * 15}")

#                 text = extract_text(
#                     image_path=image_path,
#                     engine=selected_engine
#                 )

#                 page_texts.append(text)

#             ocr_text = "\n\n".join(page_texts)

#         else:
#             raise ValueError(
#                 f"Unsupported file type: {file_extension}"
#             )

#         # --------------------------------------------------
#         # OCR Output
#         # --------------------------------------------------
#         print("\n========== OCR OUTPUT ==========\n")

#         print(ocr_text)

#         # --------------------------------------------------
#         # LLM
#         # --------------------------------------------------
#         print("\nRunning LLM...\n")

#         json_result = extract_invoice_json(ocr_text)

#         # --------------------------------------------------
#         # JSON Output
#         # --------------------------------------------------
#         print("\n========== JSON OUTPUT ==========\n")

#         print(json_result)

#     except Exception as e:
#         print(f"\nError: {e}")


# if __name__ == "__main__":
#     main()