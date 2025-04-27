import json

from bs4 import BeautifulSoup
import requests
from more_itertools.more import peekable
import time
import random

from messages import Messages

headers = {
    "User-Agent": '',
    "Cookie": Messages.Baidu_Cookie,
}


def crawl_message(to_crawl_url, to_crawl_key, to_crawl_pages):
    count = 0
    results=[]
    for num in range(to_crawl_pages):
        print(f'第{num + 1}页内容：')

        headers['User-Agent'] = random.choice(Messages.user_agents)
        response = requests.get(f'{to_crawl_url}s?wd={to_crawl_key}&pn={num*10}',
                                headers=headers)

        if response.status_code != 200:
            print(f"⚠️ 请求失败，状态码：{response.status_code}")
            continue

        html = response.text
        if "百度安全验证" in html or "请输入验证码" in html:
            print("⚠️ 遇到百度反爬验证，可能需要更换 IP 或降低访问频率")
            break

        soup = BeautifulSoup(html, 'html.parser')

        all_titles = soup.find_all('h3')
        all_spans = soup.find_all('span', recursive=True)
        all_elements = list(soup.find_all(recursive=True))
        # recursive=True表示递归地查找所有的子元素
        end_part = soup.find('style', attrs={'data-vue-ssr-id': 'a459854e:0'})

        iterable = peekable(all_titles)
        for title in iterable:
            text_title = title.get_text(strip=True)

            if to_crawl_key.lower() not in text_title.lower():
                continue

            count += 1
            print(f'{count}.{text_title}:')

            href = title.find('a')
            link_title = href['href'] if href else 'N\A'

            summary = ''
            title_index = all_elements.index(title)
            for span in all_spans:
                span_index = all_elements.index(span)
                if iterable.peek(default='End') == 'End':
                    pass
                elif span_index >= all_elements.index(iterable.peek()):
                    break

                if span_index > title_index:
                    span_text = span.get_text(strip=True)
                    if end_part:
                        if span_index >= all_elements.index(end_part):
                            break
                    if span_text and '广告' not in span_text and span_text not in summary:
                        summary += span_text + '\n'

            print(f'    链接：{link_title}')
            if summary:
                print(f'    摘要：{summary}')
            # with open('Crawled_Data.txt', 'a', encoding='utf-8') as file:
            #     file.write(f'{count}.{text_title}:\n')
            #     if link_title:
            #         file.write(f'    链接：{link_title}\n')
            #     if summary:
            #         file.write(f'    网页摘要：{summary}\n')


            result={
                'title':text_title,
                'link':'',
                'summary':'',
            }
            if link_title:
                result['link']=link_title
            if summary:
                result['summary']=summary

            results.append(result)

        time.sleep(5)

    with open('crawl_search_message.json', 'a', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    crawl_message('https://baidu.com/', 'deepseek', 10)
