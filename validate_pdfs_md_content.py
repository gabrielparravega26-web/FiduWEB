from pathlib import Path
from pypdf import PdfReader
import re

base = Path(r"c:\Users\Gabriel\OneDrive\Documentos\FiduWEB\Especificaciones de Negocio")

errors = []
summary = []

for pdf in sorted(base.glob("*.pdf")):
    md = pdf.with_suffix(".md")
    if not md.exists():
        errors.append(f"MD missing for PDF: {pdf.name}")
        continue

    try:
        reader = PdfReader(str(pdf))
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            text = text.replace("\x00", "")
            pages.append(text)
        pdf_text = "\n\n".join(pages)
    except Exception as exc:
        errors.append(f"PDF read failed: {pdf.name}: {exc}")
        continue

    md_text = md.read_text(encoding="utf-8", errors="ignore")

    # A minimal structure/title validation.
    if not md_text.lstrip().startswith("# "):
        errors.append(f"MD header missing: {md.name}")

    # Normalized text overlap check based on word-level similarity.
    def normalize(s: str) -> str:
        s = s.lower()
        s = re.sub(r"[^a-z0-9áéíóúñüàèìòù\s]+", " ", s)
        s = re.sub(r"\s+", " ", s)
        return s.strip()

    pdf_words = set(normalize(pdf_text).split())
    md_words = set(normalize(md_text).split())
    overlap = len(pdf_words & md_words)
    total = max(len(pdf_words | md_words), 1)
    overlap_ratio = overlap / total

    # Mark if there is insufficient overlap after PDF extraction.
    if overlap_ratio < 0.05:
        errors.append(f"Low overlap ratio: {pdf.name} -> {overlap_ratio:.3f}")

    # Check a reasonable text length in both sources.
    if len(pdf_text.strip()) < 80 or len(md_text.strip()) < 80:
        errors.append(f"Low text length: {pdf.name}")

    # Optional: file-level summary.
    summary.append(f"{pdf.name}: pages={len(reader.pages)} pdf_chars={len(pdf_text)} md_chars={len(md_text)} overlap={overlap_ratio:.3f}")

if errors:
    print("VALIDATION_ERRORS")
    for err in errors:
        print(err)
else:
    print("VALIDATION_OK")

print("SUMMARY")
for item in summary:
    print(item)
