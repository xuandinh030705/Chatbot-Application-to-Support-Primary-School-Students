from enum import Enum
from pathlib import Path

PROMPT_DIR = Path(__file__).parent.parent / "core" / "prompts"
PROMPT_CLASS_DIR = PROMPT_DIR / "class"


class PromptType(str, Enum):
    MATH_STUDENT = "prompt_math_student"
    MATH_PARENT = "prompt_math_parent"


class SchoolGrade(str, Enum):
    GRADE_1 = "class_1"
    GRADE_2 = "class_2"
    GRADE_3 = "class_3"
    GRADE_4 = "class_4"
    GRADE_5 = "class_5"


def get_school_grade(grade_number: int) -> SchoolGrade:
    mapping = {
        1: SchoolGrade.GRADE_1,
        2: SchoolGrade.GRADE_2,
        3: SchoolGrade.GRADE_3,
        4: SchoolGrade.GRADE_4,
        5: SchoolGrade.GRADE_5,
    }
    if grade_number not in mapping:
        raise ValueError(f"Invalid grade number: {grade_number}. Must be 1–5.")
    return mapping[grade_number]


def load_curriculum(grade: int) -> str:
    # parts = []
    # for g in range(1, grade + 1):
    #     file_path = PROMPT_CLASS_DIR / f"class_{g}.txt"
    #     if not file_path.exists():
    #         raise FileNotFoundError(f"Curriculum file not found: {file_path}")
    #     text = file_path.read_text(encoding="utf-8").strip()
    #     parts.append(f"=== Khung Toán lớp {g} ===\n{text}")
    #
    # return "\n\n".join(parts)

    file_path = PROMPT_CLASS_DIR / f"class_{grade}.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"Curriculum file not found: {file_path}")

    text = file_path.read_text(encoding="utf-8").strip()
    return text


def load_prompt(prompt_type: PromptType) -> str:
    prompt_file = PROMPT_DIR / f"{prompt_type.value}.txt"
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    return prompt_file.read_text(encoding="utf-8")


def build_math_system_message(role: str, user_name: str, grade: int) -> str:
    from app.models.user import UserRole
    system_message_template = (
        load_prompt(PromptType.MATH_STUDENT)
        if role == UserRole.USER.value
        else load_prompt(PromptType.MATH_PARENT)
    )

    curriculum = load_curriculum(grade=grade)

    system_message = system_message_template.format(
        grade=grade,
        curriculum=curriculum,
        user_name=user_name,
    )

    return curriculum, system_message
