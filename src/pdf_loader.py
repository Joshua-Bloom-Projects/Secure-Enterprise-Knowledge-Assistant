"""PDF loading and page-level text extraction."""

from __future__ import annotations

from pathlib import Path

from src.utils import clean_text


def _import_fitz():
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF is not installed. Run `pip install -r requirements.txt` first."
        ) from exc
    return fitz


def load_pdf_pages(pdf_path: Path) -> list[dict]:
    """Extract text from one PDF, preserving page-level metadata."""

    fitz = _import_fitz()
    pages: list[dict] = []

    try:
        document = fitz.open(pdf_path)
    except Exception as exc:
        print(f"[error] Could not open {pdf_path.name}: {exc}")
        return pages

    with document:
        print(f"[load] {pdf_path.name}: {document.page_count} pages")
        for page_index in range(document.page_count):
            page_number = page_index + 1
            try:
                raw_text = document.load_page(page_index).get_text("text")
            except Exception as exc:
                print(f"[warn] {pdf_path.name} page {page_number}: {exc}")
                raw_text = ""

            text = clean_text(raw_text)
            if not text:
                print(f"[skip] {pdf_path.name} page {page_number}: empty page")

            pages.append(
                {
                    "text": text,
                    "metadata": {
                        "document_name": pdf_path.name,
                        "page_number": page_number,
                        "source_path": str(pdf_path),
                    },
                }
            )

    return pages


def load_all_pdfs(source_dir: Path) -> tuple[list[dict], dict]:
    """Load all PDFs from a directory and return pages plus summary stats."""

    source_dir.mkdir(parents=True, exist_ok=True)
    pdf_paths = sorted(source_dir.glob("*.pdf"))
    stats = {
        "pdfs_found": len(pdf_paths),
        "pdfs_processed": 0,
        "pages_extracted": 0,
    }

    if not pdf_paths:
        print(f"[info] No PDF files found in {source_dir}")
        return [], stats

    all_pages: list[dict] = []
    for pdf_path in pdf_paths:
        pages = load_pdf_pages(pdf_path)
        if pages:
            stats["pdfs_processed"] += 1
            stats["pages_extracted"] += len(pages)
            all_pages.extend(pages)

    return all_pages, stats
