# 03_state/14_langgraph_checkpointer_demo.py

"""
LangGraph 状态存储示例：使用 Checkpointer 保持会话上下文
"""
import operator
from typing import TypedDict, List, Annotated

from anyio.lowlevel import checkpoint
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph


# 1. 定义图状态
class AgentState(TypedDict):
    query: str  # 用户问题
    current_context: Annotated[List[str], operator.add]  # 当前上下文摘要（用于演示）


# 2. 定义节点函数
def echo_node(state: AgentState):
    # 获取用户问题
    query = state["query"]

    # 更新上下文摘要（简化模拟）
    new_context = f"最近一次交流: {query}"

    return {
        "current_context": [new_context]
    }


# 3. 构建图
def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("echo", echo_node)
    workflow.add_edge(START, "echo")
    workflow.add_edge("echo", END)  # 直接结束
    return workflow


# 4. 主函数
def demo_langgraph():

    # 1. 创建checkpointer实例
    checkpointer = MemorySaver() #基于内存的短期记忆

    # 2. 构建图
    graph = build_graph()

    # 3. 编译图
    compiled_graph = graph.compile(checkpointer=checkpointer)

    # 4. 第一次运行智能体
    result1 = compiled_graph.invoke(
        input = {"query": "你好， LangGraph"},
        config={"configurable": {"thread_id": "user_session1"}}
    )
    print("第一次执行：", result1["current_context"])

    # 5. 第二次运行智能体
    result2 = compiled_graph.invoke(
        input={"query": "再见， LangGraph"},
        config={"configurable": {"thread_id": "user_session1"}}
    )
    print("第二次执行：", result2["current_context"])

if __name__ == "__main__":
    demo_langgraph()