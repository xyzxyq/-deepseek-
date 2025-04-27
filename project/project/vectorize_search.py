"""
创建一个 FAISS 向量索引并存储，用于后续的文本相似性检索。
使用cpu计算方法--->计算时间较长，后续可以优化为使用GPU进行计算

然后基于 FAISS 向量索引进行 最近邻搜索
返回在知识库中的搜索结果
"""

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorizeSearch:
    def __init__(self):
        print("📂 读取 processed_message.json ...")
        with open('processed_message.json', 'r', encoding='utf-8') as file:
            self.documents = json.load(file)

        print("🧠 加载 Sentence-BERT 模型 ...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def create_vector_retrieval_bs(self):
        print(f"✅ 成功加载 {len(self.documents)} 条文本数据")

        print("🔄 计算文本向量 ...")
        text_embeddings = [self.model.encode(doc['content']) for doc in self.documents]
        text_embeddings = np.array(text_embeddings, dtype=np.float32)

        print("📏 计算向量维度 ...")
        dimension = text_embeddings.shape[1]
        print(f"✅ 向量维度: {dimension}")

        print("🛠️  创建 FAISS 索引 ...")
        index = faiss.IndexFlatL2(dimension)
        index.add(text_embeddings)

        print("💾 存储索引到 'Knowledge_index.faiss' ...")
        faiss.write_index(index, 'Knowledge_index.faiss')
        print("🎉 索引创建完成！")

        return index

    def nearly_search(self, query, top_k=3):
        print(f'查询：{query}')

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding, dtype=np.float32)

        index = self.create_vector_retrieval_bs()
        _, indices = index.search(query_embedding, top_k)

        indices = indices[0]
        if max(indices) >= len(self.documents):
            print("❌ 错误: 索引超出范围，可能索引损坏")
            return []

        results = [self.documents[i] for i in indices]
        print(f"✅ 检索到 {len(results)} 条相关内容")
        return results


if __name__ == '__main__':
    result=VectorizeSearch().nearly_search("deepseek如何使用",top_k=3)
    print(result)
