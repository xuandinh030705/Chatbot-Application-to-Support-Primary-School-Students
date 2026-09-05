import { useState, useEffect } from "react";
import { Message } from "@/types/types";
import { useUser } from "@/contexts/user-context";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

interface UseChatProps {
    initialModel?: string;
}

export function useChat({ initialModel = "gptoss120b" }: UseChatProps) {
    const { user } = useUser();
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(true);
    const [sending, setSending] = useState(false);

    useEffect(() => {
        if (!user) return;
        setLoading(true);
        fetch(`${API_BASE_URL}/api/v1/chat/user/${user.id}`)
            .then(res => res.json())
            .then(data => {
                if (!data.success) throw new Error(data.error);
                setMessages(data.data);
            })
            .catch(err => console.error("Failed to load chat history:", err))
            .finally(() => setLoading(false));
    }, [user]);

    const sendMessage = (input: string) => {
        if (!user) return;

        const userMessage: Message = {
            id: crypto.randomUUID(),
            content: input,
            role: "user",
            created_at: new Date().toISOString(),
        };
        setMessages(prev => [...prev, userMessage]);

        const assistantMsg: Message = {
            id: crypto.randomUUID(),
            content: "",
            role: "assistant",
            created_at: new Date().toISOString(),
        };

        setSending(true);

        try {
            const eventSource = new EventSource(
                `${API_BASE_URL}/api/v1/chat/ask-stream?model=${initialModel}&sender_id=${user.id}&content=${encodeURIComponent(input)}`
            );
            setMessages(prev => [...prev, assistantMsg]);
            eventSource.onmessage = (e) => {
                if (e.data === "[DONE]") {
                    eventSource.close();
                    setSending(false);
                    return;
                }
                if (e.data.startsWith("[ERROR]")) {
                    console.error(e.data);
                    eventSource.close();
                    setSending(false);
                    return;
                }

                assistantMsg.content += e.data;

                setMessages(prev =>
                    prev.map(m => m.id === assistantMsg.id ? { ...m, content: assistantMsg.content } : m)
                );
            };

            eventSource.onerror = (err) => {
                console.error("Streaming error:", err);
                eventSource.close();
                setSending(false);
            };
        } catch (err) {
            console.error(err);
            assistantMsg.content = "Lỗi khi gửi tin nhắn";
            setMessages(prev =>
                prev.map(m => m.id === assistantMsg.id ? { ...m, content: assistantMsg.content } : m)
            );
            setSending(false);
        }
    };

    return {
        messages,
        loading,
        sending,
        sendMessage,
        setMessages,
    };
}
