"""
进行数据预处理
将爬取到的文本信息进行处理，让爬取的数据更清晰、可用，
让向量检索更加高效，
处理缺失值，增强鲁棒性
提高大模型生成答案的质量
"""

import json

class Process:
    def process(self):
        with open('crawl_search_message.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        documents=[
            {
            'title':item['title'],
            'content': "{} {}".format(item['title'], item['summary'].replace('\n', ',')),
            'link':item['link'],
            }
            for item in data
        ]

        with open('processed_message.json', 'w', encoding='utf-8') as file:
            json.dump(documents,file,ensure_ascii=False,indent=4)

if __name__ == '__main__':
    Process().process()