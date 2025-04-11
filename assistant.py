from ragflow_sdk import RAGFlow
from knowledge_base import KnowledgeBase


class ChatAssistantManager:
    def __init__(self, api_key, base_url):
        self.rag = RAGFlow(api_key=api_key, base_url=base_url)

    def create_chat_assistant(self, user_id, assistant_name, prompt=None):
        # 根据用户 ID 构造知识库名
        dataset_name = f"user_{user_id}_dataset"
        datasets = self.rag.list_datasets(name=dataset_name)
        if not datasets:
            print(f"[ERROR] 未找到用户 {user_id} 的知识库（{dataset_name}）")
            return None

        dataset_ids = [ds.id for ds in datasets]

        assistant = self.rag.create_chat(
            name=assistant_name,
            dataset_ids=dataset_ids,
            prompt=prompt
        )
        print(f"[INFO] 聊天助手 {assistant_name} 创建成功，绑定知识库 {dataset_name}，使用提示词：{prompt}")
        return assistant

    def list_assistants(self, user_id=None):
        """
        可选参数 user_id：如果提供，则只列出与该用户关联的聊天助手。
        """
        all_assistants = self.rag.list_chats()  # 获取所有聊天助手
        if user_id is None:
            return all_assistants  # 如果没有提供 user_id，则返回所有助手

        # 根据用户ID构建相关的知识库名称
        user_dataset_name = f"user_{user_id}_dataset"
        filtered = []

        for assistant in all_assistants:
            print(assistant.name)
            filtered.append(assistant)

        return filtered

    def delete_assistants(self, assistant_name=None):
        """
        删除聊天助手，通过名字获取ID，然后删除该助手。
        """
        assistants = self.rag.list_chats()

        # 如果提供了 assistant_name，则根据名字查找助手
        if assistant_name:
            to_delete = [a for a in assistants if assistant_name in a.name]  # 通过名字匹配
        else:
            to_delete = assistants  # 如果没有提供名字，则删除所有助手

        if not to_delete:
            print("[WARN] 未找到需要删除的聊天助手")
            return

        # 获取助手ID
        assistant_ids = [a.id for a in to_delete]
        names = [a.name for a in to_delete]

        # 删除助手
        self.rag.delete_chats(ids=assistant_ids)
        print(f"[INFO] 已删除聊天助手: {names}（ID: {assistant_ids}）")

    def create_session(self, assistant_name, session_name):
        """
        创建一个会话，绑定指定名称的聊天助手，并可以指定会话名称
        """
        assistants = self.rag.list_chats(name=assistant_name)
        if not assistants:
            print(f"[ERROR] 未找到名为 '{assistant_name}' 的助手")
            return None

        assistant = assistants[0]
        # 创建会话时，如果提供了会话名字，则使用该名字，否则使用默认名字
        session = assistant.create_session(name=session_name) if session_name else assistant.create_session()
        print(f"[INFO] 会话创建成功，绑定助手：{assistant.name}（ID: {assistant.id}）")
        if session_name:
            print(f"[INFO] 会话名称为：{session_name}")
        return session

    def list_sessions(self, assistant_name):
        """
        列出指定聊天助手的所有会话，并打印会话名称
        """
        assistants = self.rag.list_chats(name=assistant_name)
        if not assistants:
            print(f"[ERROR] 未找到名为 '{assistant_name}' 的助手")
            return []

        assistant = assistants[0]
        sessions = assistant.list_sessions()

        if not sessions:
            print(f"[INFO] 助手 '{assistant_name}' 当前没有会话")
        else:
            print(f"[INFO] 助手 '{assistant_name}' 当前有 {len(sessions)} 个会话：")
            for session in sessions:
                print(f"- 会话名称: {session.name} (ID: {session.id})")

        return sessions

    def delete_sessions(self, assistant_name, session_names):
        """
        删除指定聊天助手的部分会话，基于会话名称进行删除
        """
        # 获取聊天助手
        assistants = self.rag.list_chats(name=assistant_name)
        if not assistants:
            print(f"[ERROR] 未找到名为 '{assistant_name}' 的助手")
            return

        assistant = assistants[0]

        # 获取会话列表
        sessions = assistant.list_sessions()

        # 找到匹配的会话名称，并获取它们的 ID
        session_ids_to_delete = []
        for session in sessions:
            if session.name in session_names:  # 如果会话名称匹配
                session_ids_to_delete.append(session.id)

        if not session_ids_to_delete:
            print(f"[INFO] 未找到与给定名称匹配的会话")
            return

        # 删除找到的会话
        assistant.delete_sessions(ids=session_ids_to_delete)
        print(f"[INFO] 成功删除助手 '{assistant.name}' 的会话: {session_ids_to_delete}")

    def chat(self, assistant_name, session_name):
        """
        与指定名称的助手和会话进行聊天，聊天开始时提供第一句欢迎回应
        """
        # 获取指定名称的聊天助手
        assistants = self.rag.list_chats(name=assistant_name)
        if not assistants:
            print(f"[ERROR] 未找到名为 {assistant_name} 的助手")
            return

        assistant = assistants[0]

        # 获取该助手的所有会话
        sessions = assistant.list_sessions()

        # 查找指定会话名称的会话
        session = None
        for s in sessions:
            if s.name == session_name:
                session = s
                break

        if not session:
            print(f"[ERROR] 未找到名为 '{session_name}' 的会话")
            return

        # 提供初始的问候语并显示会话信息
        print("我是您的助理，需要我帮助您什么？")

        # 开始聊天
        while True:
            question = input("\n==================== User =====================\n> ")
            if question.lower() in ['exit', '退出']:
                print("\n==================== Chat End =====================\n")
                break

            print("\n==================== Miss R =====================\n")
            cont = ""
            for ans in session.ask(question, stream=True):
                print(ans.content[len(cont):], end='', flush=True)
                cont = ans.content