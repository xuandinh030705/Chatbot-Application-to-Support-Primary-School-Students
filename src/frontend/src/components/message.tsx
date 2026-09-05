"use client"

import Avatar from "./avatar"
import type { RoleSystem } from "@/types/types"

interface MessageProps {
    content: string
    role: RoleSystem
}

function Message({ content, role }: MessageProps) {
    const isUser = role === "user"
    return (
        <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"}`}>
            <div className="flex items-start space-x-3">
                {!isUser && <Avatar sender="assistant" />}
                <div className={`px-4 py-2 rounded-2xl shadow-sm  whitespace-pre-wrap
                    ${isUser ? "bg-blue-500 text-white" : "bg-white text-gray-900"}
                    `}>
                    {content}
                </div>


                {isUser && <Avatar sender="user" />}
            </div>
        </div>
    )

}

export default Message
