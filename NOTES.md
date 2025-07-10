in conversation.py, I am making the method signature to just return the output of the LLM. We are never going to use the dictionary response of the API for now, so for better visibility just the string output is given

Implementing a basic user service with in memory db. 

API usage guidelines

1. hit register endpoint and a user registered
2. For the registered user, make a call to login and save the response token
3. now you can use all the functional apis with the header Authorization:Bearer <token>
4. Added a postman collection for reference in the main directory for testing the endpoints

Assumptions:
1. We are not deleting the document context, as the RAG application use is to give output from a knowledge base. This knowledge base is getting updated in process document. These documents become the knowledge base. So even for new chats, we should return answer with context of all documents.