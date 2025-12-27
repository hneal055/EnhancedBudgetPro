# ============================================================
# UNIVERSAL FORMAT ROUTER (FINAL | RELIABLE | EXT-SAFE)
# ============================================================

from .fdx_loader import load_fdx
from .fountain_loader import load_fountain
from .celtx_loader import load_celtx
from .pdf_loader import load_pdf
from .plaintext_loader import load_text

# ------------------------------
# 🔥 Never fails on multi-part extensions
# ------------------------------


def detect_format(path):
    p = path.lower()

    if p.endswith(".fdx"):
        return "fdx"
    if p.endswith(".fountain"):
        return "fountain"
    if p.endswith(".celtx"):
        return "celtx"
    if p.endswith(".celtx.json"):
        return "celtx"
    if p.endswith(".json"):
        return "celtx"   # Celtx JSON support
    if p.endswith(".pdf"):
        return "pdf"
    if p.endswith(".txt"):
        return "txt"

    return None   # 👉 only if file type is truly unsupported


# ------------------------------
# File Router -> sends script to correct loader
# ------------------------------
def route_file(path):
    fmt = detect_format(path)

    if fmt == "fdx":
        return load_fdx(path)
    if fmt == "fountain":
        return load_fountain(path)
    if fmt == "celtx":
        return load_celtx(path)
    if fmt == "pdf":
        return load_pdf(path)
    if fmt == "txt":
        return load_text(path)

    raise ValueError(f"❌ Unsupported format '{fmt}' for {path}")

