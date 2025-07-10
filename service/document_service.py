import os
import uuid
from pathlib import Path

from PyPDF2 import PdfReader
from fastapi import UploadFile
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from client.openai_client import OpenAIClient
from config import API_KEY, faiss, UPLOAD_DIR


class DocumentService:
    def __init__(self):
        """
        Initializes the DocumentService.

        Initializes vector database (vdb), OpenAI client, and file-to-document mapping.
        """
        self.vdb = faiss
        self.open_ai_client = OpenAIClient(API_KEY)
        self.file_to_doc_map = {}

    async def file_upload(self, file: UploadFile):
        """
        Uploads a file and processes its contents.

        Uploads the provided file, extracts text content from the PDF, and saves it to disk.

        Args:
            file (UploadFile): The file to upload.

        Returns:
            str: The unique identifier (UUID) of the uploaded document.

        Raises:
            Exception: If there's an error during file processing.
        """
        doc_id = str(uuid.uuid4())
        contents = file.file.read()
        filename = file.filename
        with open("temp.pdf", "wb") as f:
            f.write(contents)

        pdf_reader = PdfReader("temp.pdf")
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()

        directory = Path(UPLOAD_DIR)
        directory.mkdir(parents=True, exist_ok=True)

        with open(directory / f"{doc_id}.pdf", 'w') as f:
            f.write(text)
            self.file_to_doc_map[f"{doc_id}.pdf"] = filename
        return doc_id

    async def process_document_for_rag(self, doc_id):
        """
        Processes a document for RAG (Retrieval-Augmented Generation) model.

        Processes the document identified by the provided document ID for RAG model.
        Loads the document, splits it into chunks, and adds them to the vector database.

        Args:
            doc_id (str): The unique identifier (UUID) of the document.

        Returns:
            str: A success message indicating the processing status of the document.

        Raises:
            Exception: If there's an error during document processing.
        """
        filename = self.file_to_doc_map[f"{doc_id}.pdf"]
        loader = TextLoader(file_path=(os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")))
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        self.vdb.add_documents(docs)

        return f'Document processed successfully with docId: {doc_id} and filename: {filename}'
