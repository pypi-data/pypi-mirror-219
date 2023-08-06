from typing import List

import pypdfium2


def pdf_to_image(filepath: str, resolution: int = 72, **kwargs) -> List:
    """
    Convert a PDF to a list PIL Image objects.

    Args:
        filepath (str): The PDF file path.
        resolution (int, optional): The resolution to use when converting the PDF to image.
            Defaults to 72.

    Returns:
        List: List of Image objects being one for each page of the PDF.
    """
    pages = []

    pdf = pypdfium2.PdfDocument(filepath)

    for page_num in range(len(pdf)):
        page = pdf.get_page(page_num)
        pil_image = page.render(scale=resolution / 72, **kwargs).to_pil()
        pages.append(pil_image)
    return pages
