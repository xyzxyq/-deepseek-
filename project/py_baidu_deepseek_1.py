import requests
from bs4 import BeautifulSoup
from messages import Messages
from more_itertools import peekable

# 存储HTTP请求的头部信息，模拟浏览器的请求，伪装成正常用户访问网页
headers = {
    "User-Agent": Messages.User_Agent,
    "Cookie": Messages.Baidu_Cookie
}
# print("headers.Cookie: ",content,end='')

search_message = "deepseek"
# 计数器，用于计数当前读取到了多少个网页
num = 0
for num in range(0, 100, 20):
    # requests.get()发送get请求，返回值为页面搜索结果（HTML格式）
    response = requests.get(f"https://www.baidu.com/s?wd={search_message}&pn={num}", headers=headers)
    # 获取网页源代码
    html = response.text
    # 生成一个Beautifulsoup对象，使得容易查找信息，"html.parser"是python内置html解析器
    soup = BeautifulSoup(html, "html.parser")

    # 查找标题，具有属性“h3”
    all_titles = soup.find_all("h3")
    # 查找span里面的信息
    all_spans = soup.find_all("span")

    # 递归地查找所有节点并转化为列表的形式
    all_elements = list(soup.find_all(recursive=True))

    # 迭代遍历标题
    iterable = peekable(all_titles)
    for title in iterable:
        num += 1
        # 将标题文本格式化，同时去掉所有空格和换行
        text_title = title.get_text(strip=True)
        # 查找标题对应的链接
        href = title.find("a")
        # 找到链接对应的部分
        link_title = href["href"] if href else "N/A"

        # 寻找摘要信息
        summary = ""
        title_index = all_elements.index(title)

        for span in all_spans:
            span_index = all_elements.index(span)
            if iterable.peek(default="End") == "End":
                break
            if span_index >= all_elements.index(iterable.peek()):
                break
            if span_index > title_index:
                span_text = span.get_text(strip=True)
                if span_text and '广告' not in span_text:
                    summary += span_text + '\n'

        print(f"{num}.{text_title}:")
        print(f"    链接：{link_title}")
        print(f"    摘要：{summary}")
