import os
from dotenv import load_dotenv
load_dotenv()
# Nếu chỉ có GROQ key thật (không có OPENAI thật) thì dùng ver1 (hỗ trợ Groq streaming)
# Nếu có OPENAI thật thì dùng ver2
_openai = os.getenv("OPENAI_API_KEY", "")
_groq = os.getenv("GROQ_API_KEY", "")
if _groq and "dummy" not in _groq.lower() and (not _openai or "dummy" in _openai.lower()):
    from .math_agent_ver1 import math_agent as math_agent
    from .math_agent_ver2 import math_agent as math_agent_ver2
else:
    from .math_agent_ver2 import math_agent as math_agent
    from .math_agent_ver1 import math_agent as math_agent_ver1
