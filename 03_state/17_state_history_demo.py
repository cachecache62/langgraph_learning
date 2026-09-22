# 03_state/17_state_history_demo.py

import operator
import os
from typing import Annotated

from anyio.lowlevel import checkpoint
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# 1. 定义图状态
class State(TypedDict):
    aggregate: Annotated[list, operator.add]

# 2. 定义节点函数
def a(state: State, config):
    print(f'Adding "A" to {state["aggregate"]}')
    return {"aggregate": ["A"]}

def b(state: State, config):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["B"]}

def c(state: State, config):
    print(f'Adding "C" to {state["aggregate"]}')
    return {"aggregate": ["C"]}

def b_2(state: State, config):
    print(f'Adding "B_2" to {state["aggregate"]}')
    return {"aggregate": ["B_2"]}

def d(state: State, config):
    print(f'Adding "D" to {state["aggregate"]}')
    return {"aggregate": ["D"]}

# 3. 通过状态创建图实例
graph = StateGraph(State)
graph.add_node("a", a)
graph.add_node("b", b)
graph.add_node("b_2", b_2)
graph.add_node("c", c)
graph.add_node("d", d)

# 4. 添加边
graph.add_edge(START, "a")
graph.add_edge("a", "b")
graph.add_edge("a", "c")
graph.add_edge("b", "b_2")
graph.add_edge("b_2", "d")
graph.add_edge("c", "d")
graph.add_edge("d", END)

# 5.编译图
checkpointer = SqliteSaver(sqlite3.connect(database="./sqlite_data/pregel.db", check_same_thread=False))
app = graph.compile(checkpointer=checkpointer)

# 6.执行
final_state = app.invoke({}, config={"configurable": {"thread_id": "4"}})

# 7.获取最终状态
print(final_state)

# 8.查看所有历史状态
all_states = app.get_state_history(config={"configurable": {"thread_id": "4"}})
all_states_list = list(all_states)

for state in all_states_list:
    print(state)

# 9.查看最后一次状态
last_state = app.get_state(config={"configurable": {"thread_id": "4"}})
print(last_state)



