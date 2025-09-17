import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import torch

# Specify the embedding model for efficiency
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Custom embedding function to use the specified model
class CustomEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    
    def __call__(self, input_texts):
        return self.model.encode(input_texts, convert_to_numpy=True).tolist()

class VectorStoreManager:
    """
    Manages chunking, embedding, and storing text in a local ChromaDB.
    """
    def __init__(self, persist_directory="./chroma_db"):
        self.model = SentenceTransformer(model_name, device="cuda:0") 
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_function = CustomEmbeddingFunction(model_name)
        self.collection = self.client.get_or_create_collection(
            name="document_chunks",
            embedding_function=self.embedding_function
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " "]
        )

    def process_and_store_text(self, document_text, source_id):
        chunks = self.text_splitter.split_text(document_text)
        chunk_ids = [f"{source_id}_chunk_{i}" for i in range(len(chunks))]

        # Process in batches to avoid memory issues
        batch_size =8 # Adjust as needed based on your RAM
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            batch_ids = chunk_ids[i:i + batch_size]
            
            self.collection.upsert(
                documents=batch_chunks,
                metadatas=[{"source": source_id}] * len(batch_chunks),
                ids=batch_ids
            )
            print(f"Stored batch {i // batch_size + 1}/{len(chunks) // batch_size + 1}")

        print(f"Successfully chunked and stored {len(chunks)} total chunks for {source_id}.")

    def get_collection(self):
        return self.collection

if __name__ == "__main__":
    # Example usage for testing the vector store
    sample_text = """PART I — FINANCIAL INFORMATION
 Item 1.    Financial Statements
 Apple Inc.
 CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS (Unaudited)
 (In millions, except number of shares, which are reflected in thousands, and per-share amounts)
 Three Months Ended Six Months Ended
 March 29,
 2025
 March 30,
 2024
 March 29,
 2025
 March 30,
 2024
 Net sales:
   Products $ 68,714 $ 66,886 $ 166,674 $ 163,344 
   Services 26,645 23,867 52,985 46,984 
Total net sales 95,359 90,753 219,659 210,328 
Cost of sales:
   Products 44,030 42,424 103,477 100,864 
   Services 6,462 6,058 13,040 12,338 
Total cost of sales 50,492 48,482 116,517 113,202 
Gross margin 44,867 42,271 103,142 97,126 
Operating expenses:
 Research and development 8,550 7,903 16,818 15,599 
Selling, general and administrative 6,728 6,468 13,903 13,254 
Total operating expenses 15,278 14,371 30,721 28,853 
Operating income 29,589 27,900 72,421 68,273 
Other income/(expense), net (279) 158 (527) 108 
Income before provision for income taxes 29,310 28,058 71,894 68,381 
Provision for income taxes 4,530 4,422 10,784 10,829 
Net income $ 24,780 $ 23,636 $ 61,110 $ 57,552 
Earnings per share:
 Basic $ 1.65 $ 1.53 $ 4.06 $ 3.72 
Diluted $ 1.65 $ 1.53 $ 4.05 $ 3.71 
Shares used in computing earnings per share:
 Basic 14,994,082 15,405,856 15,037,903 15,457,810 
Diluted 15,056,133 15,464,709 15,103,499 15,520,675 
See accompanying Notes to Condensed Consolidated Financial Statements.
 Apple Inc. | Q2 2025 Form 10-Q | 1
"""
    
    db_manager = VectorStoreManager()
    db_manager.process_and_store_text(sample_text, "sample_document")

    results = db_manager.get_collection().query(
        query_texts=["What is Total operating Expenses?"],
        n_results=1
    )
    print("\nQuery results:")
    print(results)