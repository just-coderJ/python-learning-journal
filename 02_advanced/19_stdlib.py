"""
=========================================================
📚 模块: 19 内建与第三方模块
💡 核心对比：
1. pip 包管理：类似 Maven/Gradle，但依赖隔离依赖于虚拟环境。
2. namedtuple/deque/Counter：Python 集合模块中的高效工具，比基础 list/dict 更省内存。
=========================================================
"""
from collections import namedtuple, Counter, deque
from datetime import datetime, timedelta
import requests

print("--- 1. 内建 collections / datetime ---")
# 任务 1：使用 namedtuple 创建 Point 坐标类。
# 任务 2：使用 Counter 统计字符串词频并打印最常见的元素。
# 任务 3：计算当前时间往后 7 天后的日期格式化输出。

point = namedtuple("Point", ["x","y", "z"])
p = point(10, 20, 30)
print(f"point是一个特殊类, {p.x}, {p.y}, {p.z}")

string = "what a terrible choice!"
counter = Counter(string)
print(f"Counter类可以统计字符串中的字符个数 {counter}")

current_time = datetime.now()
print(current_time)
after_7_days = current_time + timedelta(days=7)
print(after_7_days.strftime('%Y-%m-%d'))

print("\n--- 2. 第三方模块 requests 基础 ---")
# （需在终端执行 pip install requests）
# 任务 4：用 requests.get 访问 https://api.github.com，获取 status_code 和 JSON 中的 current_user_url。

response = requests.get("https://api.github.com", verify=False)

print(f"任务4 - 状态码 (status_code): {response.status_code}")

data = response.json()

print(f"任务4 - current_user_url: {data.get('current_user_url')}")