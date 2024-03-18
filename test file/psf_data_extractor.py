import os
import fitz  # PyMuPDF
from docx import Document

# Directory containing PDFs
pdf_directory = "BRSR"
# Directory to save Word files
output_directory = "WordFiles"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Create a function to extract text from a PDF and save it to a Word file
def extract_text_from_pdf(pdf_file, output_docx_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    # Create a Word document and add the extracted text to it
    docx_document = Document()
    docx_document.add_paragraph(text)

    # Save the Word document in the output directory with an appropriate name
    docx_document.save(output_docx_file)

# Iterate through all PDF files in the directory
for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, pdf_file)
        # Construct an appropriate name for the output Word file
        output_docx_file = os.path.splitext(pdf_file)[0] + "_text.docx"
        output_docx_path = os.path.join(output_directory, output_docx_file)
        
        # Extract text from the PDF and save it to a Word file
        extract_text_from_pdf(pdf_path, output_docx_path)

        print(f"Text extracted from {pdf_file} and saved to {output_docx_file} in {output_directory}")
