import time
from typing import TypedDict

from langgraph.cache.memory import InMemoryCache
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy


# 1.定义图状态
class State(TypedDict):
    x: int
    result: int

# 2.定义节点，模拟耗时节点
def expensive_node(state: State)->State[str,int]:
    print(f"正在执行耗时节点")
    time.sleep(5)
    print(f"耗时节点执行完毕")

    return {"result": state["x"] * 2}

# 3.构建图
def build_graph():
    graph = StateGraph(State)
    # 添加节点时，为节点配置缓存策略，这里设置为10秒缓存
    graph.add_node("expensive_node", expensive_node, cache_policy=CachePolicy(ttl=10))
    graph.add_edge(START, "expensive_node")
    graph.add_edge("expensive_node", END)
    return graph

# 4.编译并执行
def demo_langgraph():
    graph = build_graph()

    app = graph.compile(cache=InMemoryCache())

    # 第一次调用
    result1 = app.invoke({"x": 5})
    print(result1)
    time.sleep(3)

    # 第二次调用
    result2 = app.invoke({"x": 5})
    print(result2)

if __name__ == "__main__":
    demo_langgraph()