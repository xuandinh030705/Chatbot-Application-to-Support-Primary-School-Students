try:
    from langchain.agents import AgentExecutor, create_openai_functions_agent
except ImportError:
    from langchain_classic.agents import AgentExecutor, create_openai_functions_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
try:
    from langchain.callbacks.base import BaseCallbackHandler
except ImportError:
    from langchain_core.callbacks.base import BaseCallbackHandler
from app.utils.chat_utils import convert_history
from app.models.agent import AgentInput
from app.core.agents.tools import math_tool
from app.utils import logger

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY or "dummy" in GROQ_API_KEY.lower():
    from app.utils import logger as _logger
    _logger.warning("GROQ_API_KEY missing or dummy - using mock mode for math_agent_ver3")
    if not GROQ_API_KEY:
        GROQ_API_KEY = "gsk_dummy"

def _is_dummy(key):
    return not key or "dummy" in key.lower()

def _mock_text_v3(query, grade):
    return f"🧪 [MOCK Solver→Checker] Thầy/cô chào con! Con hỏi: \"{query[:150]}\" (lớp {grade}). Đây là lời giải mẫu (mock do chưa có key thật):\n\nHiệu số ban đầu: 45 - 35 = 10\nTử số mới: 10 × 2 = 20\nSố a cần tìm: 35 - 20 = 15\n> Mock này minh họa format Solver→Checker. Điền GROQ_API_KEY thật để chạy LLM thật."


class CustomHandler(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        if hasattr(response, "llm_output") and response.llm_output:
            usage = response.llm_output.get("usage", {})
            logger.info(f"LLM usage: {usage}")
        else:
            logger.info("No usage info available")

    def on_tool_end(self, output, **kwargs):
        logger.info(f"Tool output: {output}")


def create_solver_agent():
    """Agent A: giải toán lớp 1-5"""
    system_message_solver = """
Bạn là giáo viên Toán lớp tiểu học. Giải tất cả bài toán lớp 1-5 bằng lời và phép tính cơ bản.
Tuyệt đối không dùng ẩn số, chữ cái đại diện, hoặc phương trình/hệ phương trình.
Nếu nhận hướng sửa từ Checker, hãy chỉnh lại cho đúng.
Dừng lại trước khi đưa kết quả cuối cùng.
Luôn xưng hô: thầy/cô - con.
"""
    chat = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        streaming=False,
        api_key=GROQ_API_KEY,
        callbacks=[CustomHandler()]
    )

    tools = [math_tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message_solver),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(
        llm=chat,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        return_intermediate_steps=True
    )


def create_checker_agent():
    """Agent B: kiểm tra câu trả lời, trả về lý do + hướng sửa"""
    system_message_checker = """
Bạn là kiểm duyệt viên Toán lớp tiểu học.
Nhiệm vụ: kiểm tra câu trả lời của Agent A và đánh giá:
1. Có dùng ẩn số, phương trình, hệ phương trình không?
2. Có vượt phạm vi kiến thức lớp 1-5 không?

Trả về:
- Nếu đúng: "VALID"
- Nếu sai: "INVALID: Lý do vi phạm; Hướng sửa cho Agent A"
Ví dụ: "INVALID: Dùng ẩn số x; Hướng sửa: viết bằng lời và phép tính cơ bản"
"""
    chat = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        streaming=False,
        api_key=GROQ_API_KEY,
        callbacks=[CustomHandler()]
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message_checker),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),  # bắt buộc cho agent
    ])

    agent = create_openai_functions_agent(
        llm=chat,
        tools=[],
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=[],
        verbose=False,
        return_intermediate_steps=False
    )


def math_agent_with_check(agent_input: AgentInput, max_retries: int = 3):
    """Vòng lặp tự động: Solver -> Checker -> sửa lại nếu invalid"""
    if _is_dummy(GROQ_API_KEY):
        logger.info("Returning mock for math_agent_ver3 due to dummy key")
        mock = _mock_text_v3(agent_input.query, agent_input.grade)
        if agent_input.stream:
            def gen():
                for w in mock.split(" "):
                    yield w + " "
            return gen()
        return mock
    solver = create_solver_agent()
    checker = create_checker_agent()
    chat_history = convert_history(agent_input.history)

    answer = None
    for attempt in range(max_retries):
        # Step 1: Solver Agent tạo câu trả lời
        result = solver.invoke({
            "input": agent_input.query,
            "chat_history": chat_history
        })
        answer_text = result["output"]
        logger.info(f"Agent A output (attempt {attempt + 1}): {answer_text}")

        # Step 2: Checker Agent kiểm tra
        check_result = checker.invoke({"input": answer_text})
        check_output = check_result["output"]
        logger.info(f"Agent B check: {check_output}")

        if "VALID" in check_output:
            answer = answer_text
            break
        else:
            # Nếu INVALID -> thêm hướng sửa vào lịch sử chat
            chat_history.append({
                "role": "assistant",
                "content": f"Hướng sửa từ Checker: {check_output}"
            })

    if not answer:
        answer = "Agent không thể tạo câu trả lời hợp lệ sau 3 lần thử."

    return answer


if __name__ == "__main__":
    from app.models.agent import AgentInput
    from app.schemas.chat import Message, Model
    from app.models.user import UserRole

    # Ví dụ câu hỏi test
    test_query = "Cho phân số 35/45 .Tìm số tự nhiên a sao cho khi ta bớt cả tử số và mẫu số đi a đơn vị thì ta đ¬ược phân số 2/3."

    # Khởi tạo AgentInput đầy đủ
    agent_input = AgentInput(
        model=Model.gptoss120b,  # hoặc model bạn muốn dùng
        stream=False,
        query=test_query,
        role=UserRole.USER,    # hoặc role phù hợp
        user_name="Học sinh A",
        grade=5,
        history=[]                # bắt đầu không có lịch sử
    )

    # Chạy vòng Solver -> Checker
    result = math_agent_with_check(agent_input)

    print("===== Kết quả cuối cùng =====")
    print(result)
