# lm_config.py

"""
定义模型参数配置类
"""

from dataclasses import dataclass
import os

from dotenv import load_dotenv

@dataclass
class LLMConfig:
# 定义minerU服务配置
    llm_model: str
    model_provider: str
    base_url: str
    api_key : str



load_dotenv()

# lm_config = LLMConfig(
#     llm_model="qwen3.7-flash-2026-07-15",
#     model_provider="openai",
#     base_url=os.getenv("DASHSCOPE_BASE_URL"),
#     api_key=os.getenv("DASHSCOPE_API_KEY")
# )

lm_config = LLMConfig(
    llm_model="qwen3.7-flash-2026-07-15",
    model_provider="openai",
    base_url=os.environ["DASHSCOPE_BASE_URL"],
    api_key=os.environ["DASHSCOPE_API_KEY"]
)