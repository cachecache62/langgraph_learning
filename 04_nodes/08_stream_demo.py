import operator
import time
from typing import Annotated, TypedDict, List

from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.runtime import Runtime

from lm_config import lm_config

# 初始化 LLM
llm_client = init_chat_model(
    model=lm_config.llm_model,
    model_provider=lm_config.model_provider,
    base_url=lm_config.base_url,
    api_key=lm_config.api_key,
)

# 1.定义图状态
class State(TypedDict):
    input: str #用户输入
    messages: Annotated[List[BaseMessage], add_messages] #存储聊天记录
    current_step: str #当前步骤

# 2. 定义节点
def node_input(state: State):
    """接收用户输入"""
    input = state["input"]
    time.sleep(3)  # 模拟耗时操作
    return {
        "messages": [HumanMessage(content=input)],
        "current_step": "接收用户输入"
    }

# 3. 定义处理过程节点
def node_processing(state: State, runtime: Runtime):
    """
    模拟中间处理过程
    并使用 writer 输出自定义流式数据, 这对应 stream_mode="custom"
    """

    steps = ["正在分析用户意图", "正在检索知识库", "正在构建最终的提示词"]
    writer = runtime.stream_writer

    for i, step in enumerate(steps, start=1):
        time.sleep(1) #模拟耗时操作
        # print(f"{i = }, {step = }")
        writer({
            "step_index": i,
            "description": step,
            "timestamp": time.time()
        })

    return {
        "current_step": "处理完成"
    }

# 4. 定义大模型生成答案节点
def node_generation(state: State):
    """
    大模型生成答案
    """
    response = llm_client.invoke(state["messages"])

    return{
        "messages": [response],
        "current_step": "答案生成完成"
    }

# 5. 构建图
def build_graph():

    graph = StateGraph(State)
    graph.add_node("input", node_input)
    graph.add_node("process", node_processing)
    graph.add_node("generate", node_generation)

    graph.add_edge(START, "input")
    graph.add_edge("input", "process")
    graph.add_edge("process", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


# 编译并执行
def demo_langgraph():

    app = build_graph()
    init_state = {"input": "我是谁"}

    # 测试1
    # for event in app.stream(init_state, stream_mode="values"):
    #     print(f"state: {event}")

    # 测试2
    # for event in app.stream(init_state, stream_mode="updates"):
    #     print(f"state: {event}")

    # 测试3
    # for event in app.stream(init_state, stream_mode="custom"):
    #     print(f"state: {event}")

    # 测试4
    # for event in app.stream(init_state, stream_mode="messages"):
    #     print(f"state: {event}")

    # 打字机效果
    # for message, metadata in app.stream(init_state, stream_mode="messages"):
    #     print(message.content, end="", flush=True)

    # for chunk, metadata in app.stream(init_state, stream_mode="messages"):
    #     node_name = metadata.get('langgraph_node', 'unknown')
    #     # 打印 Token 内容，模拟打字机效果
    #     print(f"[{node_name}] Token: {chunk.content!r}")
    #     time.sleep(0.1)  # 仅用于演示视觉效果

    # for message, metadata in app.stream(init_state, stream_mode="messages"):
    #     if message.content:
    #         for char in message.content:
    #             print(char, end="", flush=True)
    #             time.sleep(0.03)



    # 测试5
    # count = 0
    # for event in app.stream(init_state, stream_mode="debug"):
    #     if count < 3:  # 仅演示前几条
    #         print(f"Debug Event: {event['type']} - {event.get('payload', {}).get('name')}")
    #     count += 1
    # print("... (省略后续 debug 信息)")

    # 测试6. Mixed Mode (混合模式)
    print("描述: 同时获取 updates 和 custom 数据")
    for mode, data in app.stream(init_state, stream_mode=["updates", "custom"]):
        if mode == "updates":
            print(f"[Updates] 来自节点 {list(data.keys())[0]}")
        elif mode == "custom":
            print(f"[Custom] {data['description']}")

if __name__ == "__main__":
    demo_langgraph()