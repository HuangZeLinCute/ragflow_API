import os
from ragflow_sdk import RAGFlow


class KnowledgeBase:
    def __init__(self, api_key, base_url):
        self.ragflow = RAGFlow(api_key=api_key, base_url=base_url)

    def create_or_get_dataset(self, user_id):
        dataset_name = f"user_{user_id}_dataset"
        all_datasets = self.ragflow.list_datasets()
        print("[INFO] 当前用户所有数据集：", [dataset.name for dataset in all_datasets])
        existing = [ds for ds in all_datasets if ds.name == dataset_name]
        if existing:
            print(f"[INFO] 知识库 '{dataset_name}' 已经存在，返回现有数据集。")
            return existing[0]
        else:
            print(f"[INFO] 知识库 '{dataset_name}' 不存在，正在创建新的知识库。")
            return self.ragflow.create_dataset(
                name=dataset_name,
                description=f"Knowledge base for user {user_id}",
                permission="me"
            )

    def upload_file(self, user_id, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        ext = os.path.splitext(file_path)[-1].lower()
        if ext not in [".pdf", ".txt", ".doc", ".docx"]:
            raise ValueError(f"不支持的文件格式: {ext}")

        dataset = self.create_or_get_dataset(user_id)
        with open(file_path, "rb") as f:
            content = f.read()

        dataset.upload_documents([{
            "display_name": os.path.basename(file_path),
            "blob": content
        }])
        print(f"[SUCCESS] 上传成功: {file_path} → {dataset.name}")
        return dataset  # 关键：返回上传后的 dataset，供解析用

    def delete_document(self, user_id, doc_name):
        """
        根据文档名称删除用户知识库中的文档（支持模糊名称匹配）
        """
        dataset = self.create_or_get_dataset(user_id)
        docs = dataset.list_documents()

        matched_ids = []

        for doc in docs:
            # 尝试从文档对象中获取名称（通常是 display_name 或 name 字段）
            name = getattr(doc, "display_name", None) or getattr(doc, "name", None)
            if name == doc_name:
                matched_ids.append(doc.id)

        if matched_ids:
            # 使用官方推荐的批量删除方式
            dataset.delete_documents(ids=matched_ids)
            print(f"[INFO] 已删除文档：{doc_name}（共 {len(matched_ids)} 个）")
        else:
            print(f"[WARN] 未找到文档：{doc_name}")

    def parse_document(self, user_dataset):
        import time
        """
        解析上传的文件，提取文本内容
        """
        documents = user_dataset.list_documents()
        ids = []
        for document in documents:
            ids.append(document.id)
        if not ids:
            print("[ERROR] 没有找到任何文档，请先上传。")
            return
        try:
            user_dataset.async_parse_documents(document_ids=ids)
            print("[INFO] 正在异步解析文档...")

            # 循环检查解析状态，直到解析完成
            while True:
                documents = user_dataset.list_documents()
                all_done = True  # 用来判断是否所有文档都解析完成
                for doc in documents:
                    doc_info = doc.__dict__ if hasattr(doc, '__dict__') else doc
                    run_status = doc_info.get('run', '')
                    progress = round(float(doc_info.get('progress', 0.0)) * 100, 2)
                    print(f"[INFO] 文档: {doc_info.get('name')}")
                    print(f"       ID: {doc_info.get('id')}")
                    print(f"       当前状态: {run_status}")
                    print(f"       进度: {progress}%")

                    if run_status != 'DONE':  # 如果有一个文档还没完成，就继续轮询
                        all_done = False

                if all_done:  # 所有文档解析完成
                    print("[INFO] 文档解析完成！")
                    break
                time.sleep(1)  # 每5秒检查一次状态
        except Exception as e:
            print(f"[ERROR] 解析文件时发生错误: {e}")

