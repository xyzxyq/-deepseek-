"""
本地部署deepseek（1.5B）
"""
import requests
from vectorize_search import VectorizeSearch  # 保持原来的向量检索

class LocalDeepSeekChat:
    def __init__(self, model='deepseek-r1:1.5b', base_url='http://localhost:11434'):
        self.model = model
        self.base_url = base_url

    def generate_answer(self, user_question):
        # 检索相关知识
        retrieved_doc = VectorizeSearch().nearly_search(user_question)
        context = "\n".join([doc['content'] for doc in retrieved_doc])

        # 构建消息格式（Chat 模式）
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个智能问答助手，请结合以下知识回答问题。"},
                {"role": "user", "content": f"问题：{user_question}\n\n相关知识：{context}"}
            ],
            "stream": False
        }

        response = requests.post(f"{self.base_url}/api/chat", json=payload)
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            raise Exception(f"请求失败：{response.status_code} - {response.text}")


# 测试入口
if __name__ == '__main__':
    question = input("User: ")
    bot = LocalDeepSeekChat()
    answer = bot.generate_answer(question)
    print(f"🤖 DeepSeek (本地): {answer}")
