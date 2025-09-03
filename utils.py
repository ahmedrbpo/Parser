import pdfplumber

def load_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = " ".join(page.extract_text() or "" for page in pdf.pages)
    return text