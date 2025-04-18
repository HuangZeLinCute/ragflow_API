# This is test file
from knowledge_base import KnowledgeBase
from assistant import ChatAssistantManager


if __name__ == "__main__":
    kb = KnowledgeBase(api_key="your-api_key", base_url="http://localhost:9380")
    user_id = "123"
    doc_name = "test.pdf"
    # dataset = kb.upload_file(user_id, "test.pdf")  # 上传后获取 dataset
    # kb.delete_document(user_id, doc_name)
    # kb.parse_document(dataset)  # 传入刚上传后的 dataset 对象
    manager = ChatAssistantManager(
        api_key="ragflow-M3Nzk5NWRjMTRmZjExZjBiMGJmMDI0Mm", base_url="http://localhost:9380"
    )
    manager.list_assistants(user_id)
    # manager.delete_assistants("test")
    # manager.create_session("assistant","test")
    # manager.list_sessions("assistant")
    # manager.delete_sessions("assistant", "test")
    manager.chat("assistant","test")
