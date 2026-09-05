from typing import Optional

import requests
import os
from dotenv import load_dotenv, find_dotenv
from app.utils import logger
import json
from groq import Groq

if find_dotenv():
    load_dotenv()


def _is_dummy_key(key: str) -> bool:
    if not key:
        return True
    return key.startswith("sk-dummy") or key.startswith("gsk_dummy") or "dummy" in key.lower()

def _mock_response(context, model):
    # Simple mock for demo without real API keys
    last_user = ""
    if context:
        for msg in reversed(context):
            if msg.get("role") == "user":
                last_user = msg.get("content", "")
                break
    mock_text = f"🧪 [DEMO MOCK - chưa cấu hình API key thật] \n\nBạn hỏi: \"{last_user[:200]}\" \n\nĐây là câu trả lời mẫu cho chương trình tiểu học lớp 5:\n\n- Bước 1: Phân tích đề bài và xác định dạng toán\n- Bước 2: Tóm tắt bằng sơ đồ đoạn thẳng (nếu cần)\n- Bước 3: Thực hiện phép tính cơ bản\n- Bước 4: Tự kiểm tra lại kết quả\n\n> Lưu ý: Để có lời giải thật từ AI, hãy điền OPENAI_API_KEY / GROQ_API_KEY thật vào file `src/backend/.env` và restart backend.\nModel yêu cầu: {model}"
    return mock_text

def call_openai_api(
        model: Optional[str] = "gpt-4o",
        context: list = None,
        temperature: float = 1,
        max_tokens: int = 1024,
        stream: bool = True
):
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(f"API key cho OPENAI chưa được thiết lập trong .env")

    # Mock mode for demo without real keys
    if _is_dummy_key(api_key):
        logger.warning(f"Using MOCK OpenAI response (dummy key) for model {model}")
        mock_text = _mock_response(context, model)
        if stream:
            def mock_generator():
                # stream word by word for demo
                for word in mock_text.split(" "):
                    yield word + " "
            return mock_generator()
        return mock_text

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    # Optional: set via env if your OpenAI account requires org/project scoping
    openai_org = os.getenv("OPENAI_ORG_ID")
    openai_project = os.getenv("OPENAI_PROJECT_ID")
    if openai_org:
        headers["OpenAI-Organization"] = openai_org
    if openai_project:
        headers["OpenAI-Project"] = openai_project

    data = {
        "model": model,
        "messages": context,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }

    logger.info(f"📡 Calling Openai API model={model}")

    if stream:
        def generator():
            with requests.post(api_url, headers=headers, json=data, stream=True) as response_stream:
                if response_stream.status_code != 200:
                    logger.error(f"API Error {response_stream.status_code}: {response_stream.text}")
                    return
                for line in response_stream.iter_lines():
                    if line:
                        line_str = line.decode("utf-8")
                        if line_str.startswith("data:"):
                            content = line_str[len("data:"):]
                            if content == "[DONE]":
                                break
                            try:
                                obj = json.loads(content)
                                delta = obj["choices"][0].get("delta", {})
                                text = delta.get("content")
                                if text:
                                    yield text
                            except json.JSONDecodeError:
                                continue

        return generator()
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code != 200:
        logger.error(f"API Error {response.status_code}: {response.text}")
        return ""
    result = response.json()
    return result["choices"][0]["message"]["content"]


def call_groq_api(context, model="openai/gpt-oss-120b", temperature=1.0, max_tokens=1024, stream: bool = True):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY chưa được thiết lập")

    if _is_dummy_key(api_key):
        logger.warning(f"Using MOCK Groq response (dummy key) for model {model}")
        mock_text = _mock_response(context, model)
        if stream:
            def mock_generator():
                for word in mock_text.split(" "):
                    yield word + " "
            return mock_generator()
        return mock_text

    client = Groq(api_key=api_key)
    if stream:
        def generator():
            stream_resp = client.chat.completions.create(
                messages=context,
                model=model,
                temperature=temperature,
                max_completion_tokens=max_tokens,
                stream=True
            )
            for delta in stream_resp:
                content = delta.choices[0].delta.content
                if content:
                    yield content
        return generator()
    response = client.chat.completions.create(
        messages=context,
        model=model,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        stream=False
    )
    return response.choices[0].message.content
