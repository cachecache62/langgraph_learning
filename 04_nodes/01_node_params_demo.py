"""
客户服务系统智能体
"""
from http.client import responses
from typing import TypedDict, List

from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime


# 1.模拟大模型客户端
class MockLLM:
    def invoke(self, prompt: str):
        return f"🤖: 你好哈哈哈哈：{prompt}"

# 2. 模拟数据库客户端
class MockDatabase:
    def get_user_info(self, user_id: str):
        return {
            "id": user_id,
            "role": "VIP" if "vip" in user_id else "普通用户"
        }

# 3.定义图状态
class CustomerSupporState(TypedDict):
    query: str #用户问题
    response: str #AI客服的回复
    log: List[str]

# 4.定义节点
def node_customer_service(state: CustomerSupporState, config: RunnableConfig, runtime: Runtime):

    # 测试1.获取state参数的值
    user_query = state["query"]
    print("当前节点的state参数为：", user_query)

    # 测试2.获取config参数的值
    configurable = config.get("configurable")
    user_id = configurable.get("user_id", "guest")
    print("当前节点的config参数为：", user_id)

    # 测试3.获取runtime参数的值
    llm_client = runtime.context['llm_client']

    db_client = runtime.context['db_client']
    # 健壮性校验
    if not llm_client or not db_client:
        # raise Exception("缺少必要客户端")
        return {
            "response": "系统错误：客户端初始化失败",
            "log": ["错误：LLM或DB客户端尚未初始化"]
        }

    # 调用数据库客户端
    user_info = db_client.get_user_info(user_id)
    # 调用大模型客户端
    llm_response = llm_client.invoke(f"{user_info["role"]}提问：今天中午吃什么？")

    return {
        "response": llm_response,
        "log": [user_query]
    }

# 5.构建图
def build_graph():
    workflow = StateGraph(CustomerSupporState)
    workflow.add_node("node_customer_service", node_customer_service)
    # workflow.add_edge(START, "node_customer_service")
    workflow.set_entry_point("node_customer_service")
    workflow.add_edge("node_customer_service", END)
    return workflow.compile()

# 运行
if __name__ == "__main__":

    #创建实例
    app = build_graph()

    # 1.构造状态参数：初始化状态
    init_state = {
        "query": "会员都有那些权益？"
    }

    # 2.构造config参数
    config = {
        "configurable": {
            "thread_id": "user_session1",
            "user_id": "vip_user_888"
        }
    }

    # 3.构造runtime参数
    context = {
        "llm_client": MockLLM(),
        "db_client": MockDatabase()
    }

    result = app.invoke(input=init_state, config=config, context=context)
    print(result)