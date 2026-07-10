# AI Document Intelligence Agent

## Overview

The **AI Document Intelligence Agent** is an AI-powered intelligent document processing system designed to automate invoice extraction from PDF and image documents. The system dynamically analyzes document characteristics and selects the most suitable OCR engine using an agent-based architecture. The extracted OCR text is then processed by the **Qwen2.5-0.5B-Instruct Large Language Model** to generate structured invoice JSON.

---

## Features

- Dynamic OCR Engine Selection
- Document Analyzer
- Document Profile Generation
- Rule-Based Engine Selection
- OCR Factory Pattern
- Multi-OCR Engine Support
- FastAPI REST API
- PDF to Image Conversion
- Qwen LLM-based JSON Extraction
- Business Logic Validation & Enrichment
- Invoice Storage
- Dashboard Integration

---

## Technology Stack

### Programming Language
- Python 3.11

### Backend
- FastAPI
- Uvicorn

### OCR Engines
- GOT-OCR
- TrOCR
- PaddleOCR
- RapidOCR
- Docling OCR

### Large Language Model (LLM)
- Qwen2.5-0.5B-Instruct

### AI Framework
- Hugging Face Transformers
- PyTorch
- Accelerate

### PDF Processing
- PyMuPDF

### Image Processing
- OpenCV
- Pillow

### Data Processing
- Pandas
- NumPy

---

# Project Workflow

```
User Upload
     │
     ▼
FastAPI
     │
     ▼
Document Agent
     │
     ▼
Document Analyzer
     │
     ▼
Document Profile
     │
     ▼
Rule Engine
     │
     ▼
Engine Selector
     │
     ▼
OCR Factory
     │
     ▼
Selected OCR Engine
     │
     ▼
Extracted OCR Text
     │
     ▼
Qwen2.5-0.5B-Instruct
     │
     ▼
Structured Invoice JSON
     │
     ▼
Business Logic Enrichment
     │
     ▼
Dashboard / API Response
```

---

# Clone Repository

```bash
git clone https://github.com/rohin618/AI-Document-Intelligence-Agent.git

cd AI-Document-Intelligence-Agent
```

---

# Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

```bash
uvicorn app:app --reload
```

If your entry file is different, replace `app` with the appropriate filename.

Example:

```bash
uvicorn main:app --reload
```

---

# Open the Application

### Home Page

```
http://127.0.0.1:8000
```

### Swagger API Documentation

```
http://127.0.0.1:8000/docs
```

---

# Project Structure

```text
AI-Document-Intelligence-Agent/
│
├── app.py
├── requirements.txt
├── README.md
│
├── prompts/
│
├── templates/
│
├── static/
│
├── utils/
│   ├── agents/
│   ├── analyzer/
│   ├── ocr/
│   │   ├── base_ocr.py
│   │   ├── ocr_factory.py
│   │   ├── got_ocr.py
│   │   ├── trocr.py
│   │   ├── paddle_ocr.py
│   │   ├── rapid_ocr.py
│   │   └── docling_ocr.py
│   │
│   ├── llm.py
│   ├── pdf_converter.py
│   ├── helper.py
│   └── ...
│
├── outputs/
│
└── data/
```

---

# Supported File Formats

- PDF
- PNG
- JPG
- JPEG

---

# OCR Engines

| OCR Engine | Purpose |
|------------|---------|
| GOT-OCR | Transformer-based OCR for general document recognition |
| TrOCR | Lightweight OCR for printed text |
| PaddleOCR | High-accuracy OCR for invoices and structured documents |
| RapidOCR | Lightweight CPU-optimized OCR |
| Docling OCR | Advanced layout-aware OCR for complex documents |

---

# Large Language Model

- Qwen2.5-0.5B-Instruct

The LLM converts OCR text into structured invoice JSON containing:

- Invoice Number
- Invoice Date
- Due Date
- Supplier
- Buyer
- Category
- Currency
- Amount

---

# Future Enhancements

- AI-based OCR Engine Prediction
- Vision Language Model (VLM) Integration
- Confidence-based OCR Routing
- Prompt Optimization
- Backend Analytics using Pandas & NumPy
- Dashboard Prediction using Machine Learning
- Hugging Face Deployment
- Cloud Deployment

---

# Author

**Rohini Kumar D**

Software Developer Intern

AI/ML Developer

---

# License

This project was developed as part of an internship project for educational and research purposes.