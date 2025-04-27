"""
调用deepseek
结合检索出来的知识作为上下文构建完整的问答
"""

from openai import OpenAI
from vectorize_search import VectorizeSearch

client = OpenAI(api_key='sk-8f88b0621bf8494e9ccd7eb4cab239ca', base_url='https://api.deepseek.com')

def generate_answer(user_question):
    retrieved_doc = VectorizeSearch().nearly_search(user_question)

    context = "\n".join([doc['content'] for doc in retrieved_doc])

    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[
            {'role': 'system', 'content': '你是一个智能问答助手，请你结合以下知识回答问题。'},
            {'role': 'user', 'content': f'问题:{question}\n\n相关知识:{context}'}
        ],
        stream=False
    )

    return response.choices[0].message.content

if __name__ == '__main__':
    question = input("user:")
    answer = generate_answer(question)
    print(f"DeepSeek-V3: {answer}")