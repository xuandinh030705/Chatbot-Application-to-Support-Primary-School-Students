from datetime import datetime
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError

from app.core.agents import math_agent
from app.core.db import SessionLocal
from app.models.agent import AgentInput
from app.models.chat import ChatRole, ConversationStatus, Conversation, ChatHistory
from app.schemas.chat import AskResponse, Message, Model
from app.utils import logger


class ChatService:
    def __init__(
            self,
            user_service: any
    ):
        self.db = SessionLocal()
        self.user_service = user_service
        logger.info("Chat service initialized")

    def get_or_create_active_conversation_id(self, user_id: str) -> str:
        try:
            conv_id = (
                self.db.query(Conversation.id)
                .filter(
                    Conversation.user_id == user_id,
                    Conversation.status == ConversationStatus.ACTIVE.value
                )
                .order_by(Conversation.created_at.desc())
                .first()
            )
            if conv_id:
                return conv_id[0]

            conv = Conversation(user_id=user_id, status=ConversationStatus.ACTIVE.value)
            self.db.add(conv)
            self.db.commit()
            self.db.refresh(conv)
            return conv.id
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Failed to get or create conversation for user {user_id}: {e}")
            return None

    def add(self, conversation_id: str, role: str, content: str):
        try:
            chat = ChatHistory(
                conversation_id=conversation_id,
                role=role,
                content=content,
                created_at=datetime.now()
            )
            self.db.add(chat)
            self.db.commit()
            self.db.refresh(chat)
            return chat
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Failed to create chat for conversation {conversation_id}: {e}")
            return None

    def get_messages(
            self,
            conversation_id: str,
            limit: int = 10
    ) -> Optional[List[Message]]:
        try:
            logger.info(f"Getting chats for conversation {conversation_id}")
            self.db.expire_all()

            results = (
                self.db.query(ChatHistory)
                .filter(ChatHistory.conversation_id == conversation_id)
                .order_by(ChatHistory.created_at.desc())
                .limit(limit)
                .all()
            )
            logger.info("results: {}".format(results))
            results = list(reversed(results))
            messages = [
                Message(
                    id=r.id,
                    role=r.role,
                    content=r.content,
                    created_at=r.created_at.isoformat()
                )
                for r in results
            ]
            return messages

        except SQLAlchemyError as e:
            logger.info(f"Failed to get chats for conversation {conversation_id}: {e}")
            return None

    def get_conversation(self, user_id):
        conv_id = self.get_or_create_active_conversation_id(user_id)
        result = self.get_messages(conversation_id=conv_id)
        return result

    def ask(self, sender_id: str, content: str, stream: bool = False, model: Model = None):
        conv_id = self.get_or_create_active_conversation_id(sender_id)
        max_words = 200

        def _create_response(user_msg, assistant_text: str) -> AskResponse:
            assistant_chat = self.add(conv_id, ChatRole.ASSISTANT, assistant_text)
            return AskResponse(
                question=Message(
                    id=str(user_msg.id), role=user_msg.role, content=user_msg.content,
                    created_at=user_msg.created_at.isoformat()
                ),
                answer=Message(
                    id=str(assistant_chat.id), role=assistant_chat.role, content=assistant_chat.content,
                    created_at=assistant_chat.created_at.isoformat()
                )
            )

        if len(content.split()) > max_words:
            logger.warning(f"User {sender_id} gửi input quá dài ({len(content.split())} từ)")
            warning_text = f"⚠️ Input quá dài (tối đa {max_words} từ). Vui lòng rút ngắn nội dung."
            user_chat = self.add(conv_id, ChatRole.USER, content)
            if stream:
                def _gen():
                    for w in warning_text.split(" "):
                        yield w + " "
                return _gen()
            return _create_response(user_chat, warning_text)

        history = self.get_messages(conversation_id=conv_id, limit=5) or []
        logger.info(f"History: {history}")

        user = self.user_service.get(sender_id)
        if not user:
            logger.error(f"User not found: {sender_id}")
            err_text = "Người dùng không tồn tại. Vui lòng đăng nhập lại."
            if stream:
                def _err_gen():
                    yield err_text
                return _err_gen()
            # create dummy user msg for response
            user_chat = self.add(conv_id, ChatRole.USER, content)
            return _create_response(user_chat, err_text)

        user_chat = self.add(conv_id, ChatRole.USER, content)

        # Handle model param - try to map string to Model enum
        model_enum = None
        if model is not None:
            if isinstance(model, Model):
                model_enum = model
            elif isinstance(model, str):
                try:
                    model_enum = Model(model)
                except ValueError:
                    logger.warning(f"Unknown model {model}, default to gptoss120b")
                    model_enum = Model.gptoss120b
            else:
                model_enum = model

        agent_input = AgentInput(
            model=model_enum,
            stream=stream,
            query=content,
            role=user.role,
            user_name=user.last_name,
            grade=user.grade,
            history=history
        )

        # Streaming mode: return generator that yields chunks and saves final
        if stream:
            result = math_agent(agent_input)
            # math_agent may return generator (mock) or string
            if hasattr(result, '__iter__') and not isinstance(result, (str, bytes)):
                # generator case
                def _stream_gen():
                    full_text = ""
                    try:
                        for chunk in result:
                            if chunk:
                                full_text += chunk
                                yield chunk
                    except Exception as e:
                        logger.error(f"Streaming error: {e}")
                        yield f"[ERROR] {str(e)}"
                    # Save final assistant message after streaming
                    if full_text:
                        try:
                            self.add(conv_id, ChatRole.ASSISTANT, full_text)
                            logger.info(f"Saved streamed response length {len(full_text)}")
                        except Exception as e:
                            logger.error(f"Failed to save streamed response: {e}")
                return _stream_gen()
            else:
                # string case - split into chunks for SSE
                full_text = str(result)
                def _str_gen():
                    for w in full_text.split(" "):
                        yield w + " "
                    # save
                    try:
                        self.add(conv_id, ChatRole.ASSISTANT, full_text)
                    except Exception as e:
                        logger.error(f"Failed to save streamed response: {e}")
                return _str_gen()

        response_text = math_agent(agent_input)
        # If math_agent returned generator even in non-stream (should not), handle
        if hasattr(response_text, '__iter__') and not isinstance(response_text, (str, bytes)):
            # collect generator
            response_text = "".join(list(response_text))

        response = _create_response(user_chat, response_text)
        logger.info(f"Response: {response}")
        return response


def close(self):
    try:
        self.db.close()
    except Exception as e:
        logger.warning(f"Error closing DB session: {e}")
