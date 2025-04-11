from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from knowledge_base import KnowledgeBase
from assistant import ChatAssistantManager

app = FastAPI(
    title="Knowledge Base API",
    description="API for managing knowledge base and chat assistants",
    version="1.0.0"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置
RAGFLOW_API_KEY = "ragflow-M3Nzk5NWRjMTRmZjExZjBiMGJmMDI0Mm"
RAGFLOW_BASE_URL = "http://localhost:9380"

# 依赖注入
def get_kb():
    return KnowledgeBase(api_key=RAGFLOW_API_KEY, base_url=RAGFLOW_BASE_URL)

def get_assistant_manager():
    return ChatAssistantManager(api_key=RAGFLOW_API_KEY, base_url=RAGFLOW_BASE_URL)

# 模型定义
class AssistantCreate(BaseModel):
    assistant_name: str
    prompt: Optional[str] = None

class SessionCreate(BaseModel):
    assistant_name: str
    session_name: str

class ChatMessage(BaseModel):
    assistant_name: str
    session_name: str
    message: str

# 1. 知识库相关API
@app.post("/knowledge-base/{user_id}/upload")
async def upload_file(
    user_id: str,
    file: UploadFile = File(...),
    kb: KnowledgeBase = Depends(get_kb)
):
    """上传文件到知识库"""
    try:
        # 保存上传的文件
        with open(file.filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 上传到知识库
        dataset = kb.upload_file(user_id, file.filename)
        # 解析文档
        kb.parse_document(dataset)
        
        return {"message": "File uploaded and parsed successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/knowledge-base/{user_id}/documents/{doc_name}")
async def delete_document(
    user_id: str,
    doc_name: str,
    kb: KnowledgeBase = Depends(get_kb)
):
    """删除知识库中的文档"""
    try:
        kb.delete_document(user_id, doc_name)
        return {"message": f"Document {doc_name} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 2. 聊天助手相关API
@app.post("/assistants")
async def create_assistant(
    user_id: str,
    assistant_data: AssistantCreate,
    manager: ChatAssistantManager = Depends(get_assistant_manager)
):
    """创建聊天助手"""
    try:
        assistant = manager.create_chat_assistant(
            user_id,
            assistant_data.assistant_name,
            assistant_data.prompt
        )
        return {"message": "Assistant created successfully", "assistant": assistant}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/assistants/{user_id}")
async def list_assistants(
    user_id: str,
    manager: ChatAssistantManager = Depends(get_assistant_manager)
):
    """列出用户的所有聊天助手"""
    try:
        assistants = manager.list_assistants(user_id)
        return {"assistants": assistants}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/assistants/{assistant_name}")
async def delete_assistant(
    assistant_name: str,
    manager: ChatAssistantManager = Depends(get_assistant_manager)
):
    """删除聊天助手"""
    try:
        manager.delete_assistants(assistant_name)
        return {"message": f"Assistant {assistant_name} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 3. 会话相关API
@app.post("/sessions")
async def create_session(
    session_data: SessionCreate,
    manager: ChatAssistantManager = Depends(get_assistant_manager)
):
    """创建聊天会话"""
    try:
        manager.create_session(session_data.assistant_name, session_data.session_name)
        return {"message": "Session created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sessions/{assistant_name}")
async def list_sessions(
    assistant_name: str,
    manager: ChatAssistantManager = Depends(get_assistant_manager)
):
    """列出助手的所有会话"""
    try:
        sessions = manager.list_sessions(assistant_name)
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/sessions/{assistant_name}/{session_name}")
async def delete_session(
    assistant_name: str,
    session_name: str,
    manager: ChatAssistantManager = Depends(get_assistant_manager)
):
    """删除聊天会话"""
    try:
        manager.delete_sessions(assistant_name, session_name)
        return {"message": f"Session {session_name} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 4. 聊天API
@app.post("/chat")
async def chat(
    chat_data: ChatMessage,
    manager: ChatAssistantManager = Depends(get_assistant_manager)
):
    """发送聊天消息"""
    try:
        response = []
        for ans in manager.chat(chat_data.assistant_name, chat_data.session_name):
            response.append(ans.content)
        return {"response": "".join(response)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 