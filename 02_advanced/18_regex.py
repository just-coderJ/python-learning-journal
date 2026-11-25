"""
=========================================================
📚 模块: 18 正则表达式
💡 核心对比：
1. re.match 从头匹配，re.search 全局搜索，re.findall 提取所有。
2. re.compile 预编译正则表达式，减少重复解析开销（Java 中也建议用 static final Pattern 预编译）。
=========================================================
"""
import re
from shlex import split

print("--- 1. 基础匹配与模式 ---")
# 任务 1：用 re.match 验证 '010-12345678' 座机。
# 任务 2：用 re.split 切分 'a, b;; c  d'，去除所有空串。

phone_str = '010-12345678'
match_obj = re.match(r'^((\d{3})-(\d{8}))$', phone_str)
search_obj = re.search(r'^((\d{3})-(\d{8}))$', phone_str)
find_obj = re.findall(r'^((\d{3})-(\d{8}))$', phone_str)

# search：扫描整个字符串，找到第一个匹配项就停止。 match：从字符串的最开头匹配。 findall：扫描字符串，找到所有满足的匹配项。

if match_obj:
    print(f"任务1 - 验证成功: {match_obj.group(0)}")
else:
    print("任务1 - 验证失败")

if search_obj:
    print(f"任务1 - 全局验证成功: {search_obj.group(0)}")
else:
    print("任务1 - 全局验证失败")

if find_obj:
    print(f"任务1 - 全部验证成功: {find_obj[0]}")
else:
    print("任务1 - 全部验证失败")

text = 'a, b;; c  d'

split_result = [x for x in re.split(r'[\s,;]', text) if x]
print(f"任务2 - 切分结果: {split_result}")

print("\n--- 2. 贪婪与非贪婪模式 ---")
s = '<html><body>Hello</body></html>'
# 任务 3：对比 r'<.*>' 与 r'<.*?>' 匹配到的字符串长度。
# 任务 4：用非贪婪提取上述字符串中的 body 内容 'Hello'。

s = '<html><body>Hello</body></html>'
# 贪婪：.* 会尽可能吃到最后，匹配到最后一个 >
greedy_match = re.match(r'<.*>', s)
# 非贪婪：.*? 尽可能少吃，只要碰到第一个 > 就停下来
non_greedy_match  = re.match(r'<.*?>', s)

print(f"任务3 - 贪婪匹配: {greedy_match.group(0)} (长度: {len(greedy_match.group(0))})")
print(f"任务3 - 非贪婪匹配: {non_greedy_match.group(0)} (长度: {len(non_greedy_match.group(0))})")

extract_body = re.search(r'<body>(.*?)</body>', s)

if extract_body:
    print(f"任务4 - 提取内容: {extract_body.group(1)}")

print("\n--- 3. 编译与分组提取 ---")
# 任务 5：用 re.compile(r'(\d{4})-(\d{2})-(\d{2})') 匹配日期，提取年月日。
# 任务 6：用 re.sub 将多个连续空格替换为单个空格。

date_pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
date_str = '2026-10-31'
date_match = date_pattern.match(date_str)

if date_match:
    # 通过索引访问分组，或者直接用 groups() 获取元组
    year, month, day = date_match.groups()
    print(f"任务5 - 提取日期: 年={year}, 月={month}, 日={day}")

space_text = "Hello     World!   Python    is   great."
# 正则解析：\s+ 匹配一个或多个空白字符（空格、制表符等）
cleaned_text = re.sub(r'\s+', ' ', space_text)
print(f"任务6 - 替换结果: {cleaned_text}")