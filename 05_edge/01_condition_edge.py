# 1.状态
from typing import Literal

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class GraphState:
    value: int
    step: str

# 2.定义节点
def node_a(state: GraphState) -> dict:
    print('执行节点A', state)
    return {
        "value": state["value"],
        "step": "节点A执行完毕"
    }

def node_b(state: GraphState) -> dict:
    print('执行节点B', state)
    return {
        "value": state["value"] * 10,
        "step": "节点B执行完毕"
    }

def node_c(state: GraphState) -> dict:
    print('执行节点C', state)
    return {
        "value": state["value"] + 1,
        "step": "节点C执行完毕"
    }

#3. 定义路由函数
def route_condition(state: GraphState) -> Literal["node_b","node_c"]:
    if state["value"] < 100:
        return "node_b"
    else:
        return "node_c"

#4. 创建图
def build_graph():
    graph = StateGraph(GraphState)
    #注册节点
    graph.add_node("node_a", node_a)
    graph.add_node("node_b", node_b)
    graph.add_node("node_c", node_c)

    #添加普通边（顺序边）
    graph.add_edge(START, "node_a")
    graph.add_conditional_edges(
        "node_a",
        route_condition, #指定路由函数
        # {
        #     "node_b": "node_b",
        #     "node_c": "node_c"
        # }
    )

    graph.add_edge("node_b", END)
    graph.add_edge("node_c", END)

    #编译一下
    return graph.compile()

if __name__ == "__main__":

    app = build_graph()

    result = app.invoke({"value": 500})
    print(result)

    app.get_graph().print_ascii()