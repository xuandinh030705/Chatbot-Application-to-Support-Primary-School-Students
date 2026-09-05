from langchain_core.messages import HumanMessage, AIMessage

def convert_history(history):
    lc_history = []
    for msg in history:
        if msg.role == "user":
            lc_history.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_history.append(AIMessage(content=msg.content))
    return lc_history