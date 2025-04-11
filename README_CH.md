# RAGflow的API二次开发



## 本项目主要实现的业务逻辑

用户ID → 知识库块 → 数据 → 助手 → 会话

通过用户ID直接创建知识库模块，然后知识库模块来管理数据文件，通过每个知识库模块创建助手和会话。

# RAGflow Knowledge Base API 使用指南

​	本项目要先安装ragflow

## 启动服务

```bash
# 创建uv新环境
uv venv .venv

# 激活环境
.venv\Scripts\activate

# 下载依赖
uv pip install -r requirements.txt

# 启动服务
python api.py
```

服务将在 http://localhost:8000 启动，可以访问 http://localhost:8000/docs 查看交互式API文档。

## API 使用示例

### 1. 知识库管理

#### 上传文件

POST /knowledge-base/{user_id}/upload

```json
// 使用 multipart/form-data
{
  "file": "@/path/to/your/document.pdf"
}
```

#### 删除文档

DELETE /knowledge-base/{user_id}/documents/{doc_name}

### 2. 聊天助手管理

#### 创建助手

POST /assistants

```json
{
  "user_id": "user123",
  "assistant_name": "my_assistant",
  "prompt": "你是一个专业的文档助手"
}
```

#### 获取用户的所有助手

GET /assistants/{user_id}

#### 删除助手

DELETE /assistants/{assistant_name}

### 3. 会话管理

#### 创建会话

POST /sessions

```json
{
  "assistant_name": "my_assistant",
  "session_name": "my_session"
}
```

#### 获取助手的所有会话

GET /sessions/{assistant_name}

#### 删除会话

DELETE /sessions/{assistant_name}/{session_name}

### 4. 聊天交互

#### 发送消息

POST /chat

```json
{
  "assistant_name": "my_assistant",
  "session_name": "my_session",
  "message": "请帮我总结这份文档的主要内容"
}
```

## 请求示例

### 使用curl

```bash
# 上传文件
curl -X POST "http://localhost:8000/knowledge-base/user123/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"

# 创建助手
curl -X POST "http://localhost:8000/assistants" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "assistant_name": "my_assistant",
    "prompt": "你是一个专业的文档助手"
  }'

# 创建会话
curl -X POST "http://localhost:8000/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_name": "my_assistant",
    "session_name": "my_session"
  }'

# 发送聊天消息
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_name": "my_assistant",
    "session_name": "my_session",
    "message": "请帮我总结这份文档的主要内容"
  }'
```

### 使用Python requests

```python
import requests
import json

# 上传文件
files = {'file': open('document.pdf', 'rb')}
response = requests.post('http://localhost:8000/knowledge-base/user123/upload', files=files)

# 创建助手
data = {
    "user_id": "user123",
    "assistant_name": "my_assistant",
    "prompt": "你是一个专业的文档助手"
}
response = requests.post('http://localhost:8000/assistants', json=data)

# 创建会话
data = {
    "assistant_name": "my_assistant",
    "session_name": "my_session"
}
response = requests.post('http://localhost:8000/sessions', json=data)

# 发送聊天消息
data = {
    "assistant_name": "my_assistant",
    "session_name": "my_session",
    "message": "请帮我总结这份文档的主要内容"
}
response = requests.post('http://localhost:8000/chat', json=data)
```

## 注意事项

1. 所有API都有错误处理，当发生错误时会返回相应的错误信息
2. 文件上传支持PDF、TXT、DOC、DOCX格式
3. 聊天消息支持流式响应，返回的是完整的回答内容
4. 所有API都需要确保RAGFlow服务正在运行（默认地址：http://localhost:9380） 

# 未来更新

 **agent模块**
