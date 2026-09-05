from app.models.agent import AgentInput
from app.utils import build_math_system_message, logger
from app.schemas.chat import Model
from app.utils.call_llm_api import call_openai_api, call_groq_api


def math_agent(agent_input: AgentInput):
    _, system_message = build_math_system_message(
        role=agent_input.role.value,
        user_name=agent_input.user_name,
        grade=agent_input.grade
    )

    logger.info(f"System message {system_message}")
    chat_messages = [{"role": "system", "content": system_message}]
    for msg in agent_input.history:
        chat_messages.append({
            "role": msg.role,
            "content": msg.content.strip()
        })
    chat_messages.append({"role": "user", "content": agent_input.query})
    if agent_input.model == Model.gpt4o:
        api_caller = call_openai_api
        model = "gpt-4o"
    elif agent_input.model == Model.gpt4omini:
        api_caller = call_openai_api
        model = "gpt-4omini"
    else:
        api_caller = call_groq_api
        model = "openai/gpt-oss-120b" if agent_input.model == Model.gptoss120b else "openai/gpt-oss-20b"
    logger.info(f"Calling API: {api_caller.__name__}, model: {model}")

    if agent_input.stream:
        for chunk in api_caller(context=chat_messages, model=model):
            yield chunk
    else:
        result = api_caller(context=chat_messages, model=model, stream=False)
        return result
