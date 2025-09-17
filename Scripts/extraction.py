from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
import os


class PDFExtractor:
    def __init__(self):
        pass
    def convert_pdf_to_images(self, pdf_path):
        """
        Convert PDF to a list of images.
        """
        images = convert_from_path(pdf_path)
        return images
    def convert_images_to_text(self, images):
        """
        Convert a list of images to text.
        """
        text = []
        for image in images:
            text.append(image_to_string(image))
        return text
    
    def get_test_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file.
        """
        images = self.convert_pdf_to_images(pdf_path)
        text = self.convert_images_to_text(images)
        return text
if __name__ == "__main__":
    pdf_path = "/home/saideepak/RAG/AppleDoc.pdf"  # Replace with your PDF file path
    extractor = PDFExtractor()
    text = extractor.get_test_from_pdf(pdf_path)
    for page_num, page_text in enumerate(text):
        print(f"Page {page_num + 1}:\n{page_text}\n")