from pathlib import Path
from pypdf import PdfReader
import re

base = Path(r"c:\Users\Gabriel\OneDrive\Documentos\FiduWEB\Especificaciones de Negocio")
pdfs = sorted(base.glob("*.pdf"))

for pdf in pdfs:
    md_path = pdf.with_suffix(".md")
    if md_path.exists():
        print(f"Skipped existing: {pdf.name} -> {md_path.name}")
        continue

    try:
        reader = PdfReader(str(pdf))
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            text = text.replace("\x00", "")
            pages.append(text)

        full_text = "\n\n".join(pages)
        full_text = re.sub(r"\n{3,}", "\n\n", full_text)
        full_text = re.sub(r"[ \t]+\n", "\n", full_text)

        title = pdf.stem.replace("_", " ").replace("-", " ").title()
        content = f"# {title}\n\n" + full_text.strip() + "\n"
        md_path.write_text(content, encoding="utf-8")
        print(f"Created: {md_path.name}")
    except Exception as exc:
        print(f"Failed: {pdf.name}: {exc}")
