"use client"

import { useState, type FormEvent, type ChangeEvent, type KeyboardEvent } from "react"
import { PaperAirplaneIcon } from "@heroicons/react/24/solid"

interface InputBoxProps {
    sendMessage: (text: string) => void
    sending: boolean
}

function InputBox({ sendMessage, sending }: InputBoxProps) {
    const [input, setInput] = useState("")
    const sendMessageHandler = async (text: string) => {
        if (!text.trim()) return
        setInput("")
        await sendMessage(text)
    }

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault()
        sendMessageHandler(input)
    }

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            sendMessageHandler(input)
        }
    }

    const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
        setInput(e.target.value)
    }


    return (
        <form onSubmit={handleSubmit} className="relative w-full">
            <div className="relative flex items-end space-x-3 p-4 bg-white rounded-2xl border border-gray-200 shadow-lg hover:shadow-xl transition-shadow duration-200">
                <div className="relative flex-1">
                    <textarea value={input} onChange={handleChange} onKeyDown={handleKeyDown}
                        placeholder="Nhập câu hỏi của bạn..."
                        className="w-full p-0 bg-transparent text-gray-800 placeholder:text-gray-400 border-none focus:outline-none resize-none hide-scrollbar text-sm leading-relaxed"
                        rows={1} style={{ minHeight: "25px", maxHeight: "120px" }}
                        onInput={(e) => {
                            const target = e.target as HTMLTextAreaElement
                            target.style.height = "auto"
                            target.style.height = `${Math.min(target.scrollHeight, 120)}px`
                        }}
                    />
                </div>
                <div className="flex items-center space-x-2">
                    <button type="submit"
                        className={`p-2 rounded-sm transition-all duration-200 flex items-center justify-center ${input.trim() && !sending
                            ? "bg-blue-500 hover:bg-blue-600 shadow-md hover:shadow-sm transform hover:scale-102"
                            : "bg-blue-500 cursor-not-allowed"
                            }`}
                        disabled={!input.trim() || sending} title="Gửi tin nhắn" >
                        {sending ? (
                            <div className="w-5 h-5 border-2 border-transparent border-t-white border-r-white rounded-full animate-spin" />
                        ) : (
                            <PaperAirplaneIcon className="w-5 h-5 text-white" />
                        )}
                    </button>
                </div>
            </div>
        </form>
    )
}

export default InputBox
