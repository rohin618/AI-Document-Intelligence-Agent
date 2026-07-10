from pathlib import Path
import shutil
import tempfile
import json
import os

from fastapi import APIRouter, File, HTTPException, UploadFile

from utils.agents.document_agent import DocumentAgent
from utils.ocr import extract_text
from utils.pdf_converter import pdf_to_images
from utils.llm import extract_invoice_json
import traceback

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from utils.business_logic import enrich_invoice

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request}
    )
    
import json

@router.get("/dashboard-data")
def dashboard_data():

    with open("data/invoices.json", "r") as f:
        invoices = json.load(f)

    return invoices


@router.post("/extract")
async def extract(file: UploadFile = File(...)):

    with tempfile.TemporaryDirectory() as temp_dir:

        # -----------------------------------------
        # Save Uploaded File
        # -----------------------------------------
        file_path = Path(temp_dir) / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -----------------------------------------
        # Select OCR Engine
        # -----------------------------------------
        agent = DocumentAgent()

        selected_engine = agent.choose_engine(str(file_path))

        file_extension = file_path.suffix.lower()

        try:

            ocr_text = ""

            # -----------------------------------------
            # Image Files
            # -----------------------------------------
            if file_extension in [".png", ".jpg", ".jpeg"]:

                ocr_text = extract_text(
                    image_path=str(file_path),
                    engine=selected_engine
                )

            # -----------------------------------------
            # PDF Files
            # -----------------------------------------
            elif file_extension == ".pdf":

                # -------------------------------------
                # Docling works directly on PDF
                # -------------------------------------
                if selected_engine == "docling":

                    ocr_text = extract_text(
                        image_path=str(file_path),
                        engine="docling"
                    )

                # -------------------------------------
                # Other OCR engines use images
                # -------------------------------------
                else:

                    image_paths = pdf_to_images(str(file_path))

                    page_texts = []

                    for image_path in image_paths:

                        text = extract_text(
                            image_path=image_path,
                            engine=selected_engine
                        )

                        page_texts.append(text)

                    ocr_text = "\n\n".join(page_texts)

            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file_extension}"
                )

            # -----------------------------------------
            # LLM Extraction
            # -----------------------------------------
            print("\nRunning Qwen LLM...\n")

            invoice_json = extract_invoice_json(ocr_text)

            # Enrich invoice
            invoice_json = enrich_invoice(invoice_json)

            json_file = "data/invoices.json"

            # Create data folder if needed
            os.makedirs("data", exist_ok=True)

            # Create file if it doesn't exist
            if not os.path.exists(json_file):
                with open(json_file, "w") as f:
                    json.dump([], f, indent=4)

            # Read existing invoices safely
            try:
                with open(json_file, "r") as f:
                    invoices = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                invoices = []

            # Append new invoice
            invoices.append(invoice_json)

            # Save updated invoices
            with open(json_file, "w") as f:
                json.dump(invoices, f, indent=4)

            print("Invoice Extraction Completed!")

            # -----------------------------------------
            # Response
            # -----------------------------------------
            return {
                "status": "success",
                "filename": file.filename,
                "ocr_engine": selected_engine,
                "ocr_text": ocr_text,
                "invoice": invoice_json
            }

        except Exception as e:
            print("\n" + "=" * 80)
            print("FULL ERROR")
            traceback.print_exc()
            print("=" * 80 + "\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )