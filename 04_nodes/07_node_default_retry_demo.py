from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy


# 1. 定义状态
class State(TypedDict):
    result: str

# 2.模拟一个不稳定的API调用
def mock_unstable_node(state: State) -> State[str, str]:

    # 定义重试次数
    global attempt_counter
    attempt_counter += 1
    print(f"正在尝试第{attempt_counter}次调用")

    if attempt_counter < 3:
        raise ConnectionError(f"模拟API调用失败,第{attempt_counter}次调用")
    else:
        print("模拟API调用成功")
        return{
            "result": f"API调用成功，经过了{attempt_counter}次重试"
        }

# 3.构建图
def build_graph():

    graph = StateGraph(State)
    graph.add_node(
        "mock_unstable_node",
        mock_unstable_node,
        retry_policy=RetryPolicy(max_attempts=5, retry_on=(ConnectionError, TimeoutError))
    )
    graph.add_edge(START, "mock_unstable_node")
    graph.add_edge("mock_unstable_node", END)

    return graph.compile()


if __name__ == "__main__":

    #重置全局计数器
    global attempt_counter
    attempt_counter = 0

    app = build_graph()
    result = app.invoke({})
    print(result)
