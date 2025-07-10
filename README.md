# RAG Assessment
Your task is to create a RAG application using LLM and vector store, which can be used to chat over uploaded documents.

You are given a template to start, but you can modify it.

## GenAI Backend APIs:
1. `POST /process-document` which takes in a file and processes it as chunks and stores in vector databases for later query
2. `POST /chat` which takes query string from user and fetches matching vector chunks and then calls LLM to get an answer.
## Non-GenAI Backend APIs:
3. `GET /get-documents` which returns a list of `doc_id` and/or `doc_name` whichever is able to retrieve pdf from local storage.
4. `GET /get-document/{doc_id}` which returns a document with the given doc_id.
5. `POST /new-chat` which creates a new chat session for user (previous documents and chunks are discarded for this new chat session)
6. `POST /login` endpoint for user to login
7. `POST /logout` endpoint for user to logout
8. `POST /register` endpoint for user to register
9. `GET /user` endpoint for user to get user details
9. `POST /user` endpoint for user to save user details

## Scoring params
- Code working as stated in the instructions (GenAI APIs 60% weightage, Non-GenAI APIs 40% weightage)
- Time taken to complete the task
- Code Quality
- Dockerization
- Scalability of the service
- Resiliency of the service
- Unit Tests
- API Documentation
- Any additional features in RAG

## Instructions: 
* Search for `# TODO` for instructions.
* You are NOT expected to create a UI for this. 
* You can preview & test your backend of app at `https://yourdomain:8000/docs`
* This test will be evaluated for plagiarism (from internet and GPTs).
* Please install the required packages before starting the task.
* You can use any library you want to use for this task.
* You can use any pre-trained model for this task instead of GPT-4.
* You can use any vector store you want to use for this task.
* You can use any local storage, S3, Azure Blob Storage, etc. you want to use for this task.
* You can add/remove arguments from the APIs as you see fit.
* You cannot add/remove/change paths of APIs.
* Some parts are intentionally broken for you to figure out and fix.
* You are free to be creative and assume things where needed, just state that in `NOTES.md`.
* It will be tested with at-least 5 pdfs more than 20 pages each which must be able to correctly answer the questions.
* All documents uploaded in current session should be queryable via chat.
