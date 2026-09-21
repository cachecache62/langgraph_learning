# 03_state/15_state_recovery_demo.py

"""
LangGraph 状态存储示例：从checkpointer中恢复状态
"""
import os
import sqlite3
from typing import TypedDict

from anyio.lowlevel import checkpoint
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import END
from langgraph.graph import START
from langgraph.graph import StateGraph


# 1. 构建图状态
class MyState(TypedDict):
    key_1: str
    key_2: str
    key_3: str


# 2. 定义节点函数
def node_1(state: MyState) -> MyState:
    print('node_1状态为', state)
    return {"key_1": "value_1"}


def node_2(state: MyState) -> MyState:
    print('node_2状态为', state)
    # raise Exception("模拟node_2节点报错")
    return {"key_2": "value_2"}



def node_3(state: MyState) -> MyState:
    print('node_3状态为', state)
    return {"key_3": "value_3"}


# 3. 构建图
def build_graph():
    workflow = StateGraph(MyState)
    workflow.add_node(node_1)
    workflow.add_node(node_2)
    workflow.add_node(node_3)
    workflow.add_edge(START, "node_1")
    workflow.add_edge("node_1", "node_2")
    workflow.add_edge("node_1", "node_3")
    workflow.add_edge("node_2", END)
    workflow.add_edge("node_3", END)
    return workflow

# 4. 主函数
def demo_langgraph():

    #1. 创建sqlite的connection对象
    os.makedirs("./sqlite_data", exist_ok=True)
    sqlite3_conn = sqlite3.connect(database="./sqlite_data/sqlite.db", check_same_thread= False)
    checkpointer = SqliteSaver(sqlite3_conn)

    # 2.构建图
    graph = build_graph()

    # 3. 编译图
    app = graph.compile(checkpointer=checkpointer)

    # 4. 执行智能体
    # 非None是从头开始执行
    result = app.invoke({},  config={"configurable": {"thread_id": "user_session5"}})

    # None从checkpointer中恢复状态
    # result = app.invoke(None,  config={"configurable": {"thread_id": "user_session4"}})

    print("执行结果为：", result)

if __name__ == "__main__":
    demo_langgraph()