from extraction import PDFExtractor
from vector_store import VectorStoreManager
import os
def main():
    # Path to the PDF file
    pdf_path = "/home/saideepak/RAG/AppleDoc.pdf"  # Replace with your PDF file path

    # Extract text from the PDF
    extracted_text = PDFExtractor().get_test_from_pdf(pdf_path)

    # Initialize the vector store manager
    vector_store_manager = VectorStoreManager()

    # Process and store the extracted text in the vector store
    vector_store_manager.process_and_store_text(extracted_text, source_id=os.path.basename(pdf_path))

    # Example query to test the vector store
    results = vector_store_manager.get_collection().query(
        query_texts=["What is the Company name?"],
        n_results=1
    )
    
    print("\nQuery results:")
    for result in results['documents']:
        print(result)

if __name__ == "__main__":
    main()