import { SparklesIcon } from "@heroicons/react/24/outline"
import { Link } from "react-router-dom"
import { useUser } from "@/contexts/user-context"
import { useState } from "react"
interface HeaderProps {
    model: string | null;
    setModel: (model: string) => void;
}

export default function Header({ model, setModel }: HeaderProps) {
    const { user, loading, setUser } = useUser()
    const [open, setOpen] = useState(false)

    let supportText = "Hỗ trợ học sinh cấp 1"
    if (!loading && user) {
        supportText = `Xin chào, ${user.last_name}`
    }

    const handleLogout = () => {
        console.log("Logging out...")
        setUser(null)
        setOpen(false)
    }

    return (
        <header className="flex w-full justify-center p-3 px-10 border-b border-gray-500 glass-effect relative">
            <div className="flex w-full  justify-between items-center">
                <div className="flex items-center space-x-4">
                    <Link to="/" aria-label="Đi đến trang chủ">
                        <img src="/chatbot_kilovia/logo.png" alt="Kilovia Logo" className="w-35 h-10 object-cover" />
                    </Link>
                    <div className="hidden lg:flex flex-col">
                        <h1 className="text-2xl font-bold text-gray-800">Kilovia</h1>
                        <p className="text-sm text-gray-600">Trợ lý học tập thông minh</p>
                    </div>
                </div>
                <div className="flex flex-row space-x-2 items-center justify-center">
                    <button onClick={() => setOpen(!open)} className="hidden lg:flex items-center space-x-2 px-4 py-2 bg-blue-50 rounded-full border border-blue-100 hover:bg-blue-100 transition">
                        <SparklesIcon className="w-4 h-4 text-blue-500" />
                        <span className="text-sm font-medium text-blue-600">
                            {supportText}
                        </span>
                    </button>
                    {model !== null && (
                        <select
                            value={model}
                            onChange={(e) => setModel(e.target.value)}
                            className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
                        >
                            <option value="gpt4o">GPT-4o</option>
                            <option value="gpt4omini">GPT-4o-mini</option>
                            <option value="gptoss120b">GPT-OSS-120B</option>
                            <option value="gptoss20b">GPT-OSS-20B</option>
                        </select>
                    )}

                    {user && (
                        <div className="w-30 bg-white border border-gray-200 rounded-lg">
                            <button onClick={handleLogout} className=" w-full text-left px-4 py-2 text-sm text-red-600 font-semibold bg-white 0 rounded-md shadow-sm hover:bg-red-50 hover:text-red-700 transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-red-300 " >
                                Đăng xuất
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </header >
    )
}
