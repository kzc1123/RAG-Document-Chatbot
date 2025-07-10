import os
from pathlib import Path

from faiss import IndexFlatL2
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
# from sqlalchemy import create_engine, MetaData, Table
# from sqlalchemy.orm import sessionmaker
# import sqlalchemy

from service.user_service import UserService

API_KEY = "YOUR_API_KEY_HERE"
UPLOAD_DIR = os.path.join(Path(__file__).parent, "document_library")

from openai import OpenAI
openai_client = OpenAI(api_key=API_KEY)
embeddings = OpenAIEmbeddings(client=openai_client)
user_service = UserService()

faiss = FAISS(
        embedding_function=embeddings,
        index=IndexFlatL2(1536),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )


def initialize_faiss():
    global faiss
    faiss = None
    faiss = FAISS(
        embedding_function=embeddings,
        index=IndexFlatL2(1536),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# DATABASE_URL = 'mysql://root:secret@localhost:3306/homestead'
# MYSQL_HOST = "mysql"
# MYSQL_PORT = 3306
# MYSQL_USER = "my_user"
# MYSQL_PASSWORD = "my_password"
# MYSQL_DATABASE = "my_database"
# DB_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
#
#
# engine = create_engine(DB_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = get_db()
# metadata = MetaData()
#
# users = Table('users', metadata, autoload_with=engine)
