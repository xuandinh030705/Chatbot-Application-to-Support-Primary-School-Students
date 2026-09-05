from enum import Enum
from typing import Dict, Optional
from langchain_core.tools import tool
from app.utils.logger_utils import logger


# =========================
# 1. Enum các dạng bài
# =========================
class ProblemType(Enum):
    # KHỐI 3
    RECTANGLE_AREA_PERIMETER = 1  # Chu vi, diện tích hình vuông, hình chữ nhật
    NUMBER_STRUCTURE = 2  # Cấu tạo số
    FRACTION_OF_NUMBER = 3  # Tìm 1/2, 1/3,... của số
    FORGOT_DIGIT_MULTIPLY = 4  # Quên chữ số, sai số tích
    BACKWARD_PROBLEM = 5  # Giải ngược từ cuối

    # KHỐI 4
    AVERAGE = 6  # Trung bình cộng
    SUM_DIFFERENCE = 7  # Tìm hai số khi biết tổng và hiệu
    TWO_DIFFERENCES = 8  # Hai hiệu số
    TWO_RATIOS = 9  # Bài toán có 2 tỉ số
    ELIMINATION = 10  # Bài toán khử
    BACKWARD_FLOWERS = 11  # Giải ngược từ cuối (hoa)

    # KHỐI 5
    RATIO_EXPLICIT = 12  # Tổng – hiệu tỉ dạng tường minh
    RATIO_HIDDEN = 13  # Tổng – hiệu tỉ có tổng/hiệu ẩn
    DECIMAL_MISPLACED = 14  # Dời dấu phẩy, quên dấu phẩy
    SPEED_DISTANCE_TIME = 15  # Quãng đường – vận tốc – thời gian


# =========================
# 2. Database dạng bài
# =========================
PROBLEM_DATABASE: Dict[ProblemType, Dict[str, object]] = {
    # ========== KHỐI 3 ==========
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

    # ========== KHỐI 4 ==========
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

    # ========== KHỐI 5 ==========
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
# 3. Retrieval Tool
# =========================
@tool
def math_tool(problem_type: str) -> Optional[Dict[str, object]]:
    """
    Purpose: Retrieve example + solution for a specific math problem type.

    How to use:
    1. Analyze the user's question.
    2. Map it into exactly one of these categories (Grade 3 → 5):

       - RECTANGLE_AREA_PERIMETER       : Perimeter and area of square/rectangle
       - NUMBER_STRUCTURE               : Number composition
       - FRACTION_OF_NUMBER             : Find 1/2, 1/3,... of a number
       - FORGOT_DIGIT_MULTIPLY          : Forgot a digit, multiplication error
       - BACKWARD_PROBLEM               : Work backward from the end

       - AVERAGE                        : Average (mean)
       - SUM_DIFFERENCE                 : Find two numbers given sum and difference
       - TWO_DIFFERENCES                : Find two numbers given two differences
       - TWO_RATIOS                     : Problems involving two ratios
       - ELIMINATION                    : Elimination problems
       - BACKWARD_FLOWERS               : Work backward (flowers problem)

       - RATIO_EXPLICIT                 : Total-difference ratio (explicit)
       - RATIO_HIDDEN                   : Total-difference ratio (sum or difference hidden)
       - DECIMAL_MISPLACED              : Decimal point shift / forgot decimal
       - SPEED_DISTANCE_TIME            : Distance-Speed-Time problems

    3. Call this tool with the category string.
    4. Receive the example + solution from the database.

    Rules:
    - Do NOT solve directly without calling this tool.
    - Do NOT create new categories.
    - If unsure, choose the closest category.
    """
    try:
        logger.info("Call math_tool with problem type %s", problem_type)
        problem_enum = ProblemType[problem_type]
    except KeyError:
        return None
    return PROBLEM_DATABASE.get(problem_enum)
