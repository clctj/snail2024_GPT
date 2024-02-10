import re  
  
def format_answer_with_links(answer):
    """
    格式化答案，将其中的URL链接转换为带链接的文本。

    参数：
    answer (str): 需要格式化的答案。

    返回：
    str: 格式化后的答案。

    """

    # 改进的正则表达式，以匹配更广泛的 URL 格式
    url_pattern = r'(https?://[^\s<]+|www\.[^\s<]+\.[^\s<]+)'

    # 使用 re.sub 进行替换
    def make_link(match):
        """
        将匹配到的URL链接转换为带链接的文本。

        参数：
        match (str): 匹配到的URL链接。

        返回：
        str: 带链接的文本。

        """
        url = match.group(0)
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return '<a href="{}" style="color: blue;">{}</a>'.format(url, url)

    formatted_answer = re.sub(url_pattern, make_link, answer)
    return formatted_answer
  
# 示例用法  
answer = "访问我们的网站 www.example.com 或 https://test.org 获取更多信息。"  
formatted_answer = format_answer_with_links(answer)  
print(formatted_answer)
