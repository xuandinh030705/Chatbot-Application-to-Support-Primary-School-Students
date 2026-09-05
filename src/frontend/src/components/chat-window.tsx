"use client"

import { useEffect, useRef, useState } from "react"

import Message from "@/components/message"
import InputBox from "@/components/input-box"
import Header from "@/components/header"
import type { Message as MessageType } from "@/types/types"
import Sidebar from "./sidebar"

interface ChatWindowProps {
    messages: MessageType[];
    sendMessage: (text: string) => void;
    sending: boolean;
    model: string;
    setModel: (model: string) => void;
}

function ChatWindow({ messages, sendMessage, sending, model, setModel }: ChatWindowProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null)
    const [sidebarOpen, setSidebarOpen] = useState(false)

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages])

    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth >= 1024) {
                setSidebarOpen(true)
            } else {
                setSidebarOpen(false)
            }
        }

        handleResize()
        window.addEventListener("resize", handleResize)
        return () => window.removeEventListener("resize", handleResize)
    }, [])

    const handleQuestionClick = (question: string) => {
        sendMessage(question)
        if (window.innerWidth < 1024) {
            setSidebarOpen(false)
        }
    }

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen)
    }
    return (
        <div className="flex flex-col h-screen bg-gray-50">
            <Header model={model} setModel={setModel} />

            <div className="flex flex-1 overflow-hidden relative">
                {/* <div className={`absolute top-2 lg:top-4 z-10 transition-all duration-300 ${sidebarOpen ? "left-80 ml-2 lg:ml-4" : "left-2 lg:left-4"}`}  >
                    <button onClick={toggleSidebar} className="p-2 lg:p-3 rounded-xl bg-white/70 backdrop-blur-sm hover:bg-white/90 transition-all duration-200 text-gray-600 hover:text-blue-600 shadow-lg border border-white/20">
                        {sidebarOpen ? (
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M12 17.25h8.25" />
                            </svg>
                        ) : (
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12" />
                            </svg>
                        )}
                    </button>
                </div>

                <Sidebar grade={1} onQuestionClick={handleQuestionClick} isOpen={sidebarOpen} onToggle={toggleSidebar} /> */}

                <div className="flex flex-col flex-1 items-center h-full">
                    <div className="flex-1 overflow-y-auto w-full max-w-4xl lg:max-w-5xl p-3 lg:p-6 space-y-3 lg:space-y-4 hide-scrollbar">
                        {messages.length === 0 && (
                            <div className="flex flex-col items-center justify-center h-full text-center space-y-4 lg:space-y-6 px-4">
                                <h3 className="text-lg lg:text-xl font-semibold text-gray-800 mb-2 lg:mb-3">
                                    Chào mừng đến với Kilovia!
                                </h3>
                                <p className="text-sm lg:text-base text-gray-600 max-w-sm lg:max-w-md leading-relaxed">
                                    Tôi là trợ lý học tập của bạn. Hãy đặt câu hỏi về bài học hoặc cần hỗ trợ gì nhé!
                                </p>
                            </div>
                        )}
                        {messages.map((message) =>
                            message.content.trim() ? (
                                <Message key={message.id} content={message.content} role={message.role} />
                            ) : null
                        )}
                        {/* {messages.length > 0 && messages[messages.length - 1].role === "assistant" && (
                            <SuggestedQuestions onQuestionClick={(question) => sendMessage(question)} />
                        )} */}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="p-2 lg:p-2 pt-0 w-full max-w-4xl lg:max-w-5xl flex flex-col items-center space-y-2 lg:space-y-3">
                        <InputBox sendMessage={sendMessage} sending={sending} />
                        <p className="text-xs text-gray-500 px-4 text-center">Nội dung do AI tạo, có thể có sai sót.</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ChatWindow
