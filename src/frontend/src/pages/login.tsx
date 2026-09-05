"use client"

import type React from "react"
import { useState } from "react"
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useUser } from "@/contexts/user-context"
import Header from "@/components/header"


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;


export default function LoginPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const { setUser } = useUser()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        setLoading(true)
        setError("")

        try {
            const response = await axios.post(
                `${API_BASE_URL}/api/v1/user/login`,
                { email: email },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            if (response.data.success) {
                setUser(response.data.data);
                // console.log("User logged in:", response.data.data)
                navigate("/");
            } else {
                throw new Error("Tài khoản không tồn tại. Vui lòng thử lại.");
            }
        } catch (err: any) {
            // console.error("Login errorrr:", err)
            setError(err.message || "Đăng nhập thất bại")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            <Header setModel={() => { }} model={null} />
            <div className="flex-1 flex items-center justify-center p-6">
                <div className="w-full max-w-md">
                    <div className="text-center mb-8">
                        <h2 className="text-2xl font-semibold text-gray-800 mb-3">Chào mừng trở lại!</h2>
                        <p className="text-gray-600 leading-relaxed">Đăng nhập để tiếp tục hành trình học tập cùng Kilovia</p>
                    </div>

                    <div className="bg-white/70 backdrop-blur-sm rounded-3xl p-8 shadow-lg border border-white/20">
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                                    Email
                                </label>
                                <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Nhập email của bạn"
                                    className="w-full px-4 py-3 rounded-2xl border border-gray-200 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition-all duration-200 outline-none" required />
                            </div>

                            {error && <p className="text-red-500 text-sm">{error}</p>}

                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium py-3 px-6 rounded-2xl transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loading ? "Đang đăng nhập..." : "Đăng nhập"}
                            </button>
                        </form>
                    </div>

                    <p className="text-xs text-gray-500 text-center mt-6">
                        Bằng việc đăng nhập, bạn đồng ý với điều khoản sử dụng của Kilovia
                    </p>
                </div>
            </div>
        </div>
    )
}
