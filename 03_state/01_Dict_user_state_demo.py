# 使用纯字典做状态定义的风险
# 1. 拼写错误，运行时才能发现
# 2. 数据类型模糊
from typing import Dict, Any

user_state = Dict[str, Any]
user_state = {
    "name": "Peter",
    "age": 20
}

print(user_state["name"])
print(user_state["age"])

user_state["score"] = 99.0
print(user_state["score"])

print(user_state)