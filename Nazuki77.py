import re
from bs4 import BeautifulSoup
text = "hello word:abc world"          # 要搜索的文本
match = re.search(r'word:.......', text)  # 在 text 中搜索
if match:
    print('找到了:', match.group())     # 输出: 找到了: word:abc
    
match = re.search(r'iii', 'piiig')  # 找到 'iii'
if match:
    print('找到了:', match.group())     # 输出: 找到了: iii
match = re.search(r'igs', 'piiig')  # 没找到，返回 None
if match:
    print('找到了:', match.group())
match = re.search(r'..g', 'piiig')  # 找到 'iig'（..匹配任意两字符）
if match:
    print('找到了:', match.group())
match = re.search(r'\d\d\d', 'p123g')  # 找到 '123'
if match:
    print('找到了:', match.group())
match = re.search(r'\w\w\w', '@@abcd!!')  # 找到 'abc'
if match:
    print('找到了:', match.group())     # 输出: 找到了: abc
    
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
</body>
</html>
"""
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())
print(soup.title)
print(soup.title.string)
print(soup.title.name)
for link in soup.find_all('a'):
    print(link.get('href'))
    
print(soup.get_text())

soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
tag = soup.b
print(tag.name)           # 'b'
print(tag['class'])       # ['boldest']（注意class返回列表）
print(tag.attrs)              # {'class': ['boldest']}

# 修改属性
tag['id'] = 'verybold'
print(tag.attrs)
tag['another-attribute'] = 1
print(tag.attrs)
print(tag['another-attribute'])  # 1
print(tag.string)
# 删除属性
del tag['id']
print(tag.attrs)
# 安全获取属性（不存在返回 None 而非报错）
tag.get('id')  # None
print(tag.get('id'))  # None