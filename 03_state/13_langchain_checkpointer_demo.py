# 03_state/13_langchain_checkpointer_demo.py

"""
基于LangChain的create_agent实现checkpointer机制
"""

import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from lm_config import lm_config

# 1、定义LLM实例
# uv add langchain
# uv add langchain-openai

print(lm_config)


llm_client = init_chat_model(
    model=lm_config.llm_model,
    model_provider=lm_config.model_provider,
    base_url=lm_config.base_url,
    api_key=lm_config.api_key
)

# 2、定义checkpointer实例
checkpointer = InMemorySaver()

# 3、定义工具
@tool
def weather_tool(city: str, date: str) -> str:
    """查询天气工具"""
    return f'{city}在{date}的天气是晴朗的'

# 4、构建Agent时引入checkpointer
agent = create_agent(
    model=llm_client,
    tools=[weather_tool],
    checkpointer=checkpointer,
)

# 5、用户第一次调用
user_res1 = agent.invoke(
    input={"messages": "北京2026-04-27天气怎么样"},
    config={"configurable": {"thread_id": "user_session1"}}
)
print('第一次调用', user_res1['messages'][-1])

# 6、用户在同一个会话当中，第二次调用
user_res2 = agent.invoke(
    input={"messages": "适合出去玩吗"},
    config={"configurable": {"thread_id": "user_session1"}}
)
print('第二次调用', user_res2['messages'][-1])
