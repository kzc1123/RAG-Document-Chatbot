import os
from pathlib import Path

from fastapi import APIRouter, UploadFile, HTTPException, Depends

from config import UPLOAD_DIR
from config import user_service
from service.document_service import DocumentService
from utils.get_current_user import JWTBearer

document_router = APIRouter()
document_service = DocumentService()


@document_router.post("/process-document", dependencies=[Depends(JWTBearer(user_service))])
async def process_document(file: UploadFile):
    """
    Process the uploaded document and store it in the local storage
    Args:
        file (UploadFile): The uploaded file object.

    Returns:
        str: Processed document content.
    """
    doc_id = await document_service.file_upload(file)
    return await document_service.process_document_for_rag(doc_id)


@document_router.get("/get-documents", dependencies=[Depends(JWTBearer(user_service))])
async def get_documents(offset: int = 0, limit: int = 10):
    """
    Get all PDF documents (not their chunks) for this chat-session from the local storage.
    Optionally add offset & limit to paginate the results.

    Args:
        offset (int): Offset value for pagination (default is 0).
        limit (int): Limit value for pagination (default is 10).

    Returns:
        List: List of documents.
    """
    # List all files in the upload directory
    directory = Path(UPLOAD_DIR)
    files = os.listdir(directory)
    file_map = document_service.file_to_doc_map

    processed_files = [file_map[file] for file in files if file in file_map]

    # Paginate the results
    documents = processed_files[offset: offset + limit]

    return documents


@document_router.get("/get-document/{doc_id}", dependencies=[Depends(JWTBearer(user_service))])
async def get_document(doc_id: str):
    """
    Get a specific document by its ID.

    Args:
        doc_id (str): Document ID.

    Returns:
        str: File content if the document exists, else raises HTTPException.
    """
    # Check if the document exists
    directory = Path(UPLOAD_DIR)
    if not os.path.exists(os.path.join(directory, f"{doc_id}.pdf")):
        raise HTTPException(status_code=404, detail="Document not found")

    # Read the file content
    with open(os.path.join(UPLOAD_DIR, f"{doc_id}.pdf"), "r") as file:
        file_content = file.read()

    return file_content
