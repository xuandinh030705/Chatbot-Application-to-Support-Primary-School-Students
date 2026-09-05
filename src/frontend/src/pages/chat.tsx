import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ChatWindow from "@/components/chat-window";
import Loading from "@/components/loading";
import { useUser } from "@/contexts/user-context";
import { useChat } from "@/libs/hooks/use-chat";

function ChatPage() {
  const navigate = useNavigate();
  const { user, loading: userLoading } = useUser();
  const [model, setModel] = useState("gpt4o");

  const { messages, loading, sending, sendMessage } = useChat({
    initialModel: model,
  });

  useEffect(() => {
    if (!user && !userLoading) {
      navigate("/login");
    }
  }, [user, userLoading, navigate]);

  if (userLoading || loading) {
    return <Loading />;
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100 text-gray-900">
      <ChatWindow
        messages={messages}
        sendMessage={sendMessage}
        sending={sending}
        model={model}
        setModel={setModel}
      />
    </div>
  );
}

export default ChatPage;
