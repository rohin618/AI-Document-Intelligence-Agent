from pathlib import Path
import tempfile
import fitz


def pdf_to_images(pdf_path: str, zoom: float = 2.0):
    """
    Convert a PDF into high-resolution PNG images.

    Args:
        pdf_path (str): Path to PDF.
        zoom (float): Rendering zoom. Default = 2.0

    Returns:
        list[str]: List of image paths.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = fitz.open(str(pdf_path))

    image_paths = []

    # Create temporary folder
    output_dir = Path(tempfile.mkdtemp(prefix="pdf_pages_"))

    matrix = fitz.Matrix(zoom, zoom)

    for page_number, page in enumerate(document):

        pix = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        image_path = output_dir / f"page_{page_number + 1}.png"

        pix.save(str(image_path))

        image_paths.append(str(image_path))

    document.close()

    return image_paths