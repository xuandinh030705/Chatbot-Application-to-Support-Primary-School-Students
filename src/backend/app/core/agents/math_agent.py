from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from enum import Enum
from typing import Dict, Optional
import os
from dotenv import load_dotenv
from app.utils.logger_utils import logger

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")


# =========================
# ProblemType với mô tả chi tiết
# =========================
class ProblemType(Enum):
    # KHỐI 3
    RECTANGLE_AREA_PERIMETER = (1, "Chu vi, diện tích hình vuông/hình chữ nhật")
    NUMBER_STRUCTURE = (2, "Cấu tạo số: tách số, ghép số, thay đổi chữ số")
    FRACTION_OF_NUMBER = (3, "Tìm 1/2, 1/3,... của số")
    FORGOT_DIGIT_MULTIPLY = (4, "Nhân số quên chữ số, tính sai tích")
    BACKWARD_PROBLEM = (5, "Giải ngược từ cuối, tìm số ban đầu")

    # KHỐI 4
    AVERAGE = (6, "Tính trung bình cộng của các số liệu")
    SUM_DIFFERENCE = (7, "Tìm hai số khi biết tổng và hiệu")
    TWO_DIFFERENCES = (8, "Hai hiệu số trong bài toán liên quan đến nhiều đại lượng")
    TWO_RATIOS = (9, "Bài toán có 2 tỉ số, tỉ lệ giữa hai nhóm")
    ELIMINATION = (10, "Bài toán khử để tìm giá trị ẩn")
    BACKWARD_FLOWERS = (11, "Giải ngược từ cuối dạng hoa quả hoặc số lượng")

    # KHỐI 5
    RATIO_EXPLICIT = (12, "Tỉ số giữa hai số, biết tổng hoặc hiệu dạng rõ ràng")
    RATIO_HIDDEN = (13, "Tỉ số có tổng/hiệu ẩn, cần suy luận để tìm")
    DECIMAL_MISPLACED = (14, "Dời dấu phẩy hoặc quên dấu phẩy")
    SPEED_DISTANCE_TIME = (15, "Quãng đường – vận tốc – thời gian, tính toán thực tế")

    def __init__(self, value, description):
        self._value_ = value
        self.description = description


# =========================
# Database ví dụ + giải pháp
# =========================
PROBLEM_DATABASE: Dict[ProblemType, Dict[str, object]] = {
    # KHỐI 3
    ProblemType.RECTANGLE_AREA_PERIMETER: {
        "example": "Hình chữ nhật có chu vi 72cm, giảm chiều rộng 6cm, diện tích giảm 120cm². Tìm chiều dài và chiều rộng.",
        "solution": [
            "Chiều dài hình chữ nhật: 120 ÷ 6 = 20 cm",
            "Nửa chu vi: 72 ÷ 2 = 36 cm",
            "Chiều rộng: 36 – 20 = 16 cm",
            "Đáp số: Chiều dài: 20cm; Chiều rộng: 16cm"
        ]
    },
    ProblemType.NUMBER_STRUCTURE: {
        "example": "Tìm số 3 chữ số, xoá chữ số 7 ở hàng đơn vị, số mới kém số cũ 331.",
        "solution": [
            "Giảm số do xoá chữ số 7: 331 – 7 = 324",
            "324 ứng với 9 phần (10-1)",
            "Số mới: 324 ÷ 9 = 36",
            "Số cũ: 36 × 10 + 7 = 367",
            "Đáp số: 367"
        ]
    },
    ProblemType.FRACTION_OF_NUMBER: {
        "example": "Một đội sửa đoạn đường dài 369m. Ngày 1 sửa 1/3. Hỏi còn bao nhiêu?",
        "solution": [
            "Ngày 1 sửa: 369 ÷ 3 = 123m",
            "Còn lại: 369 – 123 = 246m"
        ]
    },
    ProblemType.FORGOT_DIGIT_MULTIPLY: {
        "example": "Nhân một số 2 chữ số với 6, quên chữ số 2 ở hàng chục. Tích giảm bao nhiêu?",
        "solution": [
            "Tích giảm: 20 × 6 = 120"
        ]
    },
    ProblemType.BACKWARD_PROBLEM: {
        "example": "Chia số cho 6, cộng 6, được số nhỏ nhất 2 chữ số. Tìm số?",
        "solution": [
            "Số nhỏ nhất 2 chữ số: 10",
            "Sau chia +6: 10 – 6 = 4",
            "Số cần tìm: 4 × 6 = 24"
        ]
    },
    # KHỐI 4
    ProblemType.AVERAGE: {
        "example": "Xe 1 chở 25 tấn, xe 2 chở 35 tấn. Xe 3 chở bằng trung bình 3 xe. Hỏi xe 3?",
        "solution": [
            "Tổng 3 xe = 3 phần, phần 1 là xe 3",
            "Tổng xe 1 + 2 = 60 tấn = 2 phần",
            "Phần 1 = 60 ÷ 2 = 30 tấn",
            "Xe 3 chở 30 tấn"
        ]
    },
    ProblemType.SUM_DIFFERENCE: {
        "example": "Tìm hai số tổng 2345, giữa chúng có 24 số khác nhau.",
        "solution": [
            "Hiệu = 24 +1 = 25",
            "Số bé = (2345 – 25) ÷ 2 = 1160",
            "Số lớn = 1160 + 25 = 1185"
        ]
    },
    ProblemType.TWO_DIFFERENCES: {
        "example": "Hai bể TN 1200 lít, TH 1000 lít. Hai vòi chảy 200, 150 lít/giờ. Khi nào bằng nhau?",
        "solution": [
            "Hiệu nước ban đầu: 200 l",
            "Hiệu chảy/giờ: 50 l",
            "Thời gian: 200 ÷ 50 = 4 giờ"
        ]
    },
    ProblemType.TWO_RATIOS: {
        "example": "Lớp 5A trồng 3/4 số cây 5B, 5B giảm 5 cây → 5A = 6/7 5B. Tính số cây mỗi lớp.",
        "solution": [
            "Số cây 5A không đổi",
            "Số cây 5B lúc đầu = 4/3 số 5A",
            "Số cây 5B lúc sau = 7/6 số 5A",
            "5 cây = 1/6 số cây 5A → 5A = 30 cây",
            "5B = 30 ÷ 3 × 4 = 40 cây"
        ]
    },
    ProblemType.ELIMINATION: {
        "example": "Minh mua 5 vở + 8 sách 121 000, Tâm 3 sách + 10 vở 86 000. Giá mỗi loại?",
        "solution": [
            "Gấp 2 lần: 10 vở + 16 sách = 242 000",
            "Giá 13 sách = 242 000 – 86 000 = 156 000 → 1 sách = 12 000",
            "Giá 1 vở = (86 000 – 36 000) ÷ 10 = 5 000"
        ]
    },
    ProblemType.BACKWARD_FLOWERS: {
        "example": "Mai có số hoa, tặng 1/4 cho Nga, 1/3 còn lại cho Đào, cuối còn 8 bông. Hỏi ban đầu?",
        "solution": [
            "8 bông = 2/3 số còn lại → số còn lại = 12",
            "12 bông = 3/4 số ban đầu → số ban đầu = 16 bông"
        ]
    },
    # KHỐI 5
    ProblemType.RATIO_EXPLICIT: {
        "example": "Tỉ số giữa hai số là 0,4. Số lớn hơn số bé 45 đơn vị. Tìm hai số",
        "solution": [
            "0,4 = 2/5",
            "Số bé: 2 phần = 15 → 30",
            "Số lớn = 30 + 45 = 75"
        ]
    },
    ProblemType.RATIO_HIDDEN: {
        "example": "Cho phân số 35/45, bớt a đơn vị → phân số 2/3",
        "solution": [
            "Hiệu: 45 – 35 = 10",
            "Tử số mới: 10 × 2 = 20",
            "a = 35 – 20 = 15"
        ]
    },
    ProblemType.DECIMAL_MISPLACED: {
        "example": "Dời dấu phẩy sang phải 1 chữ số → số mới hơn 21,06",
        "solution": [
            "Số lúc đầu: 21,06 ÷ (10-1) = 2,34"
        ]
    },
    ProblemType.SPEED_DISTANCE_TIME: {
        "example": "Xe đi từ A→B: 45km/h dự định, 35km/h thực tế, chậm 40 phút. Tính thời gian thực tế",
        "solution": [
            "t1/t2 = 35/45 = 5/9",
            "Thời gian thực tế: 40 ÷ (9-5) × 9 = 90 phút"
        ]
    }
}


# =========================
# Phân loại câu hỏi nhiều dạng
# =========================
def _get_related_problems_with_llm(chat: ChatOpenAI, question: str) -> Optional[list]:
    descriptions = "\n".join([f"{e.name}: {e.description}" for e in ProblemType])
    classification_prompt = f"""
Bạn là giáo viên Toán lớp 3 → 5.
Phân loại câu hỏi sau, trả về tất cả các dạng bài Enum có thể liên quan (cách nhau bằng dấu phẩy):
{descriptions}

Nếu câu hỏi **không thuộc kiến thức Toán lớp 3 → 5**, trả về "OUT_OF_SCOPE".
Câu hỏi: {question}

Trả lời **chỉ với tên Enum, phân tách bằng dấu phẩy** hoặc "OUT_OF_SCOPE".
"""

    messages = [
        SystemMessage(content="Bạn là giáo viên Toán lớp 3 → 5, phân loại câu hỏi."),
        HumanMessage(content=classification_prompt)
    ]

    result = chat.invoke(messages)
    output = result.content.strip().upper()
    logger.info("output: {}".format(output))

    if output == "OUT_OF_SCOPE":
        return None

    related_names = [name.strip() for name in output.split(",")]
    related_problems = []
    for name in related_names:
        if name in ProblemType.__members__:
            related_problems.append(PROBLEM_DATABASE[ProblemType[name]])

    return related_problems if related_problems else None


# =========================
# Giải bài toán step-by-step dựa trên nhiều ví dụ
# =========================
def _solve_with_llm_multiple(chat: ChatOpenAI, question: str, problem_infos: list, chat_history: list) -> str:
    examples_text = ""
    for idx, p in enumerate(problem_infos, 1):
        examples_text += f"Ví dụ {idx}: {p['example']}\nCác bước: {', '.join(p['solution'])}\n\n"

    system_message = f"""
    Bạn là giáo viên Toán lớp 5, chuyên nghiệp và tường minh.
    Nhiệm vụ:
    1. Giải bài toán **chỉ dựa trên ví dụ tham khảo**, không dùng cách giải khác, không đặt ẩn số, không dùng phương pháp cao hơn lớp 5.
    2. Trình bày các bước giải **rõ ràng, tuần tự, logic**, hoàn toàn bằng tiếng Việt.
    3. Nếu bài toán không thể giải theo bất kỳ ví dụ nào hoặc không thuộc chương trình Toán lớp 5, trả về duy nhất câu: "Bài toán này chưa có trong cơ sở dữ liệu hoặc vượt quá kiến thức lớp 5."

    Ví dụ tham khảo: 
    {examples_text}

    Bài toán cần giải: {question}
    """

    messages = [{"role": "system", "content": system_message}]
    messages.append({"role": "user", "content": question})

    response = chat.invoke(messages)
    output_text = response.content

    logger.info("===== LLM Output =====")
    logger.info(output_text)

    return output_text


# =========================
# Agent chính cập nhật
# =========================
def math_agent(question: str, chat_history: list = None) -> str:
    if chat_history is None:
        chat_history = []

    chat = ChatOpenAI(
        temperature=0,
        model="gpt-4-turbo",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    problem_infos = _get_related_problems_with_llm(chat, question)
    if not problem_infos:
        return "Bài toán này chưa có trong cơ sở dữ liệu dạng bài hoặc không thuộc chương trình Toán lớp 3 → 5."

    solution_text = _solve_with_llm_multiple(chat, question, problem_infos, chat_history)
    return solution_text


# =========================
# Test
# =========================
if __name__ == "__main__":
    test_question = "Tìm một số thập phân, biết rằng nếu dời dấu phẩy của số đó sang phải 1 chữ số ta sẽ được một số mới lớn hơn số phải tìm là 21,06"
    test_chat_history = []

    result = math_agent(test_question, test_chat_history)
    print("===== Kết quả LLM =====")
    print(result)