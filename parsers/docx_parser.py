
import os
import subprocess

import mammoth
from docx import Document

from logger import logger


# process a .doc or .docx file and extract text
def parse_doc_file(file_path):
    def convert_doc_to_docx(path):
        out_dir = os.path.dirname(path)
        try:
            subprocess.run(["libreoffice", "--headless", "--convert-to", "docx", path, "--outdir", out_dir], check=True)
            new_path = path + "x"
            if os.path.exists(new_path):
                return new_path
            alt_path = os.path.join(out_dir, os.path.basename(path).replace(".doc", ".docx"))
            return alt_path if os.path.exists(alt_path) else None
        except Exception as e:
            logger.error(f"Convert failed: {e}")
            return None

    # extract text using python-docx
    def extract_docx_text(path):
        try:
            doc = Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            logger.error(f"Read file .docx failed: {e}")
            return ''

    if file_path.endswith(".doc"):
        file_path = convert_doc_to_docx(file_path)
        if not file_path:
            return ''

    try:
        with open(file_path, "rb") as f:
            result = mammoth.extract_raw_text(f)
        return [result.value.strip()]
    except Exception:
        logger.warning("Mammoth failed, fallback to python-docx...")
        return extract_docx_text(file_path)
