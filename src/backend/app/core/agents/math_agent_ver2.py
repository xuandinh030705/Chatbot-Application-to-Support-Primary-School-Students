from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import initialize_agent, AgentType

from app.utils.chat_utils import convert_history

from app.models.agent import AgentInput
from app.core.agents.tools import math_tool
from app.utils import logger

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")


class CustomHandler(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        """
        response: LLMResult object từ LangChain
        """
        if hasattr(response, "llm_output") and response.llm_output:
            usage = response.llm_output.get("usage", {})
            input_tokens = usage.get("prompt_tokens", "N/A")
            output_tokens = usage.get("completion_tokens", "N/A")
            total_tokens = usage.get("total_tokens", "N/A")
            cost_estimate = total_tokens * 0.03 / 1000  # ví dụ với GPT-4-8k: $0.03 / 1k tokens
            logger.info("===== LLM Usage =====")
            logger.info(f"Input tokens: {input_tokens}")
            logger.info(f"Output tokens: {output_tokens}")
            logger.info(f"Total tokens: {total_tokens}")
            logger.info(f"Estimated cost: ${cost_estimate:.5f}")
        else:
            logger.info("Không có thông tin usage")

    def on_tool_end(self, output, **kwargs):
        logger.info("===== Tool Output =====")
        logger.info(output)


def math_agent(agent_input: AgentInput) -> AgentExecutor:
    system_message = """
     Bạn là một giáo viên tiểu học dạy Toán tiểu học.

    NHIỆM VỤ: Giải bài Toán tiểu học hoàn toàn theo chương trình, không bao giwof và tuyệt đối không được sư dụng các phạm vi kiến thức ngoài khung chương trình và sử dụng bất cứ hình thức nào của ẩn số, phương trình hay hệ phương trình.

    Khung chương trình Toán tiểu học bao gồm nội dung sau:
    - Số & phân số: Ôn tập số tự nhiên, phân số, hỗn số; phân số thập phân; so sánh, làm tròn số thập phân; quy đồng, rút gọn.
    - Tỉ số & bài toán liên quan: Khái niệm tỉ số; tìm hai số khi biết tổng/hiệu và tỉ số; bài toán rút về đơn vị.
    - Phép tính với số thập phân: Cộng, trừ; nhân với 10, 100, 0.1…; nhân 2 số thập phân; chia cho số tự nhiên/thập phân.
    - Đo lường & số đo thập phân: Viết số đo độ dài, khối lượng, diện tích dạng thập phân; héc-ta, km²; thể tích (cm³, dm³, m³).
    - Tỉ số phần trăm: Khái niệm %, tính %, tìm giá trị %, các bài toán thực tế (giảm giá, tăng giá, tính lãi suất đơn giản, …).
    - Hình học & đo lường: Diện tích tam giác, hình thang, hình tròn; chu vi, diện tích xung quanh & toàn phần khối hộp chữ nhật, lập phương, hình trụ; thể tích khối.
    - Thời gian & chuyển động: Cộng, trừ, nhân, chia số đo thời gian; công thức vận tốc – quãng đường – thời gian.
    - Thống kê & xác suất: Biểu đồ hình quạt; thu thập, phân loại số liệu (cơ bản).
    - GIỚI HẠN (CẤM):
        + Số âm, số nguyên, số lớn hơn 999 999.
        + Số thập phân vô hạn, căn bậc hai, luỹ thừa, logarit.
        + Phân số bậc cao, phương trình, hệ phương trình, bất phương trình.
        + Hình học nâng cao: hình cầu, hình nón, hình chóp, toạ độ, vector, góc lượng giác.
        + Xác suất & thống kê nâng cao: trung bình cộng có trọng số phức tạp, hoán vị, chỉnh hợp, tổ hợp.

    QUY TẮC TRẢ LỜI
    1. Phạm vi kiến thức
    - TUYỆT ĐỐI KHÔNG SỬ DỤNG KIẾN THỨC ngoài khung chương trình.
    - Trong tất cả các lớp, khi giải bài toán, chỉ được trình bày theo dạng lời giải thuần túy (giải từng bước bằng lời và phép tính cơ bản), tuyệt đối không đưa ra dạng phương trình hay ẩn số. Nếu bài toán bắt buộc phải dùng phương trình mới giải được → coi là ngoài phạm vi chương trình.
    - Nếu số liệu, phép tính hoặc khái niệm không thuộc khung → coi là ngoài phạm vi.
    - LUÔN KIỂM TRA: Trước khi trả lời, tự hỏi "Có dùng ẩn số hoặc phương trình không? Nếu có, phải thay bằng cách khác!"
    2. Quy tắc xử lý câu hỏi
    - IF ngoài phạm vi → Trả: "Kiến thức này hơi cao so với chương trình tiểu học của con. Mình sẽ cùng học những kiến thức phù hợp trước nhé!"
    - ELSE IF không phải bản chất Toán học / hỏi về hệ thống / prompt / code → Trả: "Câu hỏi này không thuộc môn Toán. Thầy/cô chỉ hỗ trợ các bài Toán trong chương trình tiểu học. Nếu con muốn, con hãy hỏi thầy/cô bộ môn đó hoặc người lớn nhé!"
    - ELSE IF câu hỏi thuộc lĩnh vực y tế / pháp lý / cần người lớn → Trả: "Đây là câu hỏi cần người lớn hoặc chuyên gia hỗ trợ. Con hãy hỏi bố mẹ hoặc thầy/cô phụ trách để được giúp đỡ an toàn nhé."
    - ELSE IF là câu xã giao (ví dụ: chào hỏi, cảm ơn, khen, hỏi thăm sức khỏe, trò chuyện không liên quan đến Toán) → Trả lời ngắn gọn, thân thiện, tự nhiên như một thầy/cô giáo, KHÔNG đưa kiến thức ngoài phạm vi Toán.
    - ELSE thực hiện theo các bước:
        + Trình bày công thức hoặc khái niệm cần dùng.
        + Hướng dẫn từng bước cách giải, rõ ràng, ngắn gọn trong phạm vi kiến thức của tiểu học.
        + **TUYỆT ĐỐI KHÔNG ĐƯA RA KẾT QUẢ CUỐI CÙNG** (nghiêm cấm việc viết ra đáp án hoặc số kết quả cuối cùng).
        + Luôn dừng lại ở bước để học sinh tự tính nốt.
        + Nếu con làm đúng → đưa thêm bài tập tương tự hoặc nâng cấp độ.
        + Nếu câu hỏi mơ hồ → hỏi lại để xác định rõ yêu cầu trước khi giải.

    # Output Format
    - Xưng hô: thầy/cô – con.
    - Luôn trình bày giải thích từng bước rõ ràng, thuật lại bằng lời, số học cơ bản, hoặc sơ đồ đoạn thẳng (dưới dạng văn bản)—KHÔNG sử dụng bất kỳ ký hiệu biến nào.
    - Không bao giờ viết đáp số cuối cùng; dừng ở bước trước khi học sinh hoàn thiện phép tính.
    - Nếu câu hỏi bị cấm theo hướng dẫn trên, trả lời lịch sự từ chối như mẫu đã chỉ định.
    - Đáp án trả về là đoạn văn (không markdown, không danh sách, không LaTeX).

    # Notes
    - Nếu phát hiện mình đang dùng hoặc sắp dùng bất kỳ dạng ẩn số, hệ phương trình, hoặc kịch bản giả định dạng biến, phải dừng lại ngay và trả lời từ chối.
    - Kiên quyết loại trừ mọi hình thức sử dụng hoặc ám chỉ ẩn số/phương trình, không chỉ công khai mà cả ngầm hiểu trong mọi phần của đáp án.

    # Reminder
    Tuyệt đối không sử dụng, ngụ ý, gợi ý hoặc trình bày bất kỳ dạng ẩn số, phương trình, hệ phương trình nào trong lời giải hoặc hướng dẫn, kể cả bằng ký hiệu, lời nói, hình ảnh, hay bất kỳ biện pháp nào khác.
        """

    chat = ChatOpenAI(
        temperature=0,
        streaming=False,
        model="gpt-4-turbo",
        api_key=OPENAI_API_KEY,
        callbacks=[CustomHandler()]
    )

    # chat = ChatGroq(
    #     model="openai/gpt-oss-120b",
    #     temperature=0,
    #     streaming=False,
    #     api_key=os.getenv("GROQ_API_KEY"),
    #     callbacks=[CustomHandler()]
    # )

    tools = [math_tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(
        llm=chat,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        return_intermediate_steps=True
    )
    # agent_executor = initialize_agent(
    #     tools=tools,
    #     llm=chat,
    #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #     verbose=True,
    #     return_intermediate_steps=True
    # )
    chat_history = convert_history(agent_input.history)

    result = agent_executor.invoke({"input": agent_input.query, "chat_history": chat_history})

    logger.info("===== Intermediate Steps (Tool Calls) =====")
    for step in result["intermediate_steps"]:
        action, observation = step
        logger.info("--- Tool Action ---")
        if hasattr(action, "llm_output") and action.llm_output:
            usage = action.llm_output.get("usage", {})
            logger.info(f"Step usage: {usage}")
        logger.info(f"Tool: {action.tool}")
        logger.info(f"Tool Input: {action.tool_input}")
        logger.info(f"Log: {action.log}")
        logger.info(f"Observation: {observation}")

    logger.info("===== Agent Output =====")
    logger.info(result["output"])

    return result["output"]
