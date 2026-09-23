# 1. 定义状态
from typing import TypedDict, Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command


class TransferState(TypedDict):
    recipient: str
    amount: int
    memo: str
    approved: bool
    final_status: str

# 2.定义节点1:中断确认节点
def review_transfer(state: TransferState) -> dict[str, Any]:
    """
    审核节点
    :param state: 图状态
    :return: 修改的状态值
    """

    # 组织数据
    print("\n[Node] review_transfer：生成待执行的转账请求")

    # 准备待审核的数据
    pending_transfer = {
        "recipient": state["recipient"],
        "amount": state["amount"],
        "memo": state["memo"],
    }

    # 中断并获取确认结果
    user_review = interrupt(
        {
            "pending_transfer": pending_transfer,
            "title": "转账审核",
            "instruction": "请返回是否批转或要修改的字段",
        }
    )

    # 恢复执行并处理返回结果
    approved = False #用户是否同意
    update_transfer = dict (pending_transfer)

    #处理中断决策
    if isinstance(user_review, bool):
        approved = user_review
    elif isinstance(user_review, dict):
        approved = user_review.get("approved", True)
        for k in("recipient", "amount", "memo"):
            if k in user_review:
                update_transfer[k] = user_review[k]

    print(f"[Node] review_transfer：用户决策：{approved}")

    # 返回结果
    return {
        "approved": approved,
        "recipient": update_transfer["recipient"],
        "amount": update_transfer["amount"],
        "memo": update_transfer["memo"],
    }

# 3.定义节点2：模拟支付节点
def execute_transfer(state: TransferState) -> dict[str, str]:
    """
    执行节点：根据审核结果执行转账
    """
    if not state["approved"]:
        print("\n[Node] execute_transfer：用户未批准，取消转账")
        return {"final_status": "已取消：用户未批准"}

    print("\n[Node] execute_transfer：模拟执行转账...")
    return {
        "final_status": f"成功转账 {state['amount']} 元给 {state['recipient']}"
    }

# 3. 构建图
def build_graph():
    # 必须传入 checkpointer 才能支持中断
    graph = StateGraph(TransferState)
    graph.add_node("review_transfer", review_transfer)
    graph.add_node("execute_transfer", execute_transfer)

    #顺序边
    graph.add_edge(START, "review_transfer")
    graph.add_edge("review_transfer", "execute_transfer")
    graph.add_edge("execute_transfer", END)

    return graph.compile(checkpointer=InMemorySaver())

# 5.执行图结构
if __name__ == "__main__":
    app = build_graph()

    config = {"configurable": {"thread_id": "abc"}}

    init_state = {
        "recipient": "张三",
        "amount": 100,
        "memo": "转账测试",
        "approved": False
    }

    # 第一次调用流程
    result = app.invoke(init_state, config)

    # 接受到中断信息
    interrupt_value = result["__interrupt__"][0]
    # 用户基于页面做出选择
    print(f"模拟为用户提供前端页面显示如下信息:{interrupt_value.value}")

    #模拟用户所做的决策
    user_decision = {"approved": False, "recipient": "张三", "amount": 108, "memo": "谢谢"}

    # 恢复流程（第二次调用）：将用户决策送入智能体内部
    final_result = app.invoke(Command(resume=user_decision), config = config)

    # 获取到第二次调用的结果
    print(f"最终结果：{final_result}")