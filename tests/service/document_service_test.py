import unittest
from unittest.mock import MagicMock, patch
from fastapi import UploadFile

from service.document_service import DocumentService


class TestDocumentService(unittest.TestCase):
    def setUp(self):
        self.document_service = DocumentService()

    def tearDown(self):
        pass

    @patch('document_service.os')
    @patch('document_service.PdfReader')
    @patch('document_service.TextLoader')
    @patch('document_service.CharacterTextSplitter')
    def test_file_upload(self, mock_text_splitter, mock_text_loader, mock_pdf_reader, mock_os):
        mock_os.path.join.return_value = "mock_file_path"
        mock_text_splitter.return_value.split_documents.return_value = ["mock_document"]
        mock_pdf_reader.return_value.pages.__getitem__.return_value.extract_text.return_value = "mock_text"

        file = MagicMock(spec=UploadFile)
        file.filename = "mock_filename"
        file.file.read.return_value = b"mock_contents"

        doc_id = self.document_service.file_upload(file)

        self.assertIsInstance(doc_id, str)
        self.assertGreater(len(doc_id), 0)

    @patch('document_service.faiss')
    @patch('document_service.TextLoader')
    @patch('document_service.CharacterTextSplitter')
    def test_process_document_for_rag(self, mock_text_splitter, mock_text_loader, mock_faiss):
        mock_text_splitter.return_value.split_documents.return_value = ["mock_document"]

        doc_id = "temp"

        result = self.document_service.process_document_for_rag(doc_id)

        self.assertEqual(result, f'Document processed successfully with docId: {doc_id} and filename: {self.document_service.file_to_doc_map[f"{doc_id}.pdf"]}')


if __name__ == '__main__':
    unittest.main()
