# Secondary Development of RAGflow API

## Main Business Logic Implemented in This Project

User ID → Knowledge Base Block → Data → Assistant → Session

The knowledge base module is created directly using the user ID, and it manages data files. Assistants and sessions are then created through each knowledge base module.

# RAGflow Knowledge Base API User Guide

You need to install `ragflow` before using this project.

## Starting the Service

```bash
# Create a new uv environment
uv venv .venv

# Activate the environment
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Start the service
python api.py
```

The service will start at http://localhost:8000. You can visit http://localhost:8000/docs to see the interactive API documentation.

## API Usage Examples

### 1. Knowledge Base Management

#### Upload File  

POST /knowledge-base/{user_id}/upload  

```json
// Use multipart/form-data
{
  "file": "@/path/to/your/document.pdf"
}
```

#### Delete Document  

DELETE /knowledge-base/{user_id}/documents/{doc_name}

### 2. Assistant Management

#### Create Assistant  

POST /assistants  

```json
{
  "user_id": "user123",
  "assistant_name": "my_assistant",
  "prompt": "You are a professional document assistant."
}
```

#### Get All Assistants of a User  

GET /assistants/{user_id}

#### Delete Assistant  

DELETE /assistants/{assistant_name}

### 3. Session Management

#### Create Session  

POST /sessions  

```json
{
  "assistant_name": "my_assistant",
  "session_name": "my_session"
}
```

#### Get All Sessions of an Assistant  

GET /sessions/{assistant_name}

#### Delete Session  

DELETE /sessions/{assistant_name}/{session_name}

### 4. Chat Interaction

#### Send Message  

POST /chat  

```json
{
  "assistant_name": "my_assistant",
  "session_name": "my_session",
  "message": "Please help me summarize the main content of this document."
}
```

## Request Examples

### Using curl

```bash
# Upload File
curl -X POST "http://localhost:8000/knowledge-base/user123/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"

# Create Assistant
curl -X POST "http://localhost:8000/assistants" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "assistant_name": "my_assistant",
    "prompt": "You are a professional document assistant."
  }'

# Create Session
curl -X POST "http://localhost:8000/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_name": "my_assistant",
    "session_name": "my_session"
  }'

# Send Chat Message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_name": "my_assistant",
    "session_name": "my_session",
    "message": "Please help me summarize the main content of this document."
  }'
```

### Using Python requests

```python
import requests
import json

# Upload File
files = {'file': open('document.pdf', 'rb')}
response = requests.post('http://localhost:8000/knowledge-base/user123/upload', files=files)

# Create Assistant
data = {
    "user_id": "user123",
    "assistant_name": "my_assistant",
    "prompt": "You are a professional document assistant."
}
response = requests.post('http://localhost:8000/assistants', json=data)

# Create Session
data = {
    "assistant_name": "my_assistant",
    "session_name": "my_session"
}
response = requests.post('http://localhost:8000/sessions', json=data)

# Send Chat Message
data = {
    "assistant_name": "my_assistant",
    "session_name": "my_session",
    "message": "Please help me summarize the main content of this document."
}
response = requests.post('http://localhost:8000/chat', json=data)
```

## Notes

1. All APIs include error handling and will return appropriate error messages when errors occur.
2. File uploads support PDF, TXT, DOC, and DOCX formats.
3. Chat messages support streaming responses, returning the complete reply content.
4. Make sure the RAGFlow service is running (default address: http://localhost:9380)

# China Documentation

For detailed English documentation, please refer to [README_CN.md](README_CN.md).

# Future Updates

**agent module**
