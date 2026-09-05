"use client"

import { useState } from "react"

interface SidebarProps {
    grade: number,
    onQuestionClick: (question: string) => void
    isOpen: boolean
    onToggle: () => void
}

export default function Sidebar({ grade, onQuestionClick, isOpen, onToggle }: SidebarProps) {
    const [expandedCategories, setExpandedCategories] = useState<number[]>([0])

    const toggleCategory = (index: number) => {
        setExpandedCategories((prev) => (prev.includes(index) ? prev.filter((i) => i !== index) : [...prev, index]))
    }

    const mathCurriculum = [
        {
            grade: 1,
            titles: [
                {
                    title: "Số học",
                    questions: [
                        "Các số trong phạm vi 10, 20, 100",
                        "Cộng, trừ trong phạm vi 10, 20, 100",
                        "So sánh các số tự nhiên nhỏ"
                    ]
                },
                {
                    title: "Hình học",
                    questions: [
                        "Nhận biết hình tròn, hình vuông, hình tam giác, hình chữ nhật",
                        "Thực hành vẽ, ghép, chia hình đơn giản"
                    ]
                },
                {
                    title: "Đại lượng và đo lường",
                    questions: [
                        "Đo độ dài bằng thước",
                        "Xem giờ đúng, nửa giờ",
                        "Thực hành đo lường đơn giản"
                    ]
                },
                {
                    title: "Giải toán có lời văn",
                    questions: [
                        "Bài toán cộng, trừ một bước",
                        "Giải thích và trình bày bài toán bằng lời"
                    ]
                }
            ]
        },
        {
            grade: 2,
            titles: [
                {
                    title: "Số học",
                    questions: [
                        "Các số trong phạm vi 1000",
                        "Cộng, trừ có nhớ trong phạm vi 1000",
                        "Nhân, chia trong phạm vi 100",
                        "Bảng nhân, bảng chia"
                    ]
                },
                {
                    title: "Hình học",
                    questions: [
                        "Đường thẳng, đoạn thẳng",
                        "Chu vi hình vuông, hình chữ nhật",
                        "Xem giờ: chính xác đến 5 phút"
                    ]
                },
                {
                    title: "Đại lượng và đo lường",
                    questions: [
                        "Đơn vị đo độ dài: cm, m, km",
                        "Đơn vị đo khối lượng: kg",
                        "Đơn vị đo thời gian: giờ, ngày, tháng"
                    ]
                },
                {
                    title: "Giải toán có lời văn",
                    questions: [
                        "Bài toán về nhiều hơn, ít hơn",
                        "Bài toán về gấp lên, giảm đi một số lần",
                        "Bài toán có 2 phép tính"
                    ]
                }
            ]
        },
        {
            grade: 3,
            titles: [
                {
                    title: "Số học",
                    questions: [
                        "Các số đến 100.000",
                        "Phép nhân, phép chia số có nhiều chữ số",
                        "Giới thiệu phân số",
                        "Tính giá trị biểu thức có dấu ngoặc"
                    ]
                },
                {
                    title: "Hình học",
                    questions: [
                        "Diện tích hình chữ nhật, hình vuông",
                        "Nhận biết góc vuông, góc nhọn, góc tù",
                        "Vẽ và đo độ dài đoạn thẳng"
                    ]
                },
                {
                    title: "Đại lượng và đo lường",
                    questions: [
                        "Đơn vị đo độ dài: mm, cm, m, km",
                        "Đơn vị đo khối lượng: g, kg",
                        "Đơn vị đo thời gian: giờ, phút, giây"
                    ]
                },
                {
                    title: "Giải toán có lời văn",
                    questions: [
                        "Bài toán về rút về đơn vị",
                        "Bài toán về tìm một phần mấy của một số",
                        "Bài toán có 2–3 bước tính"
                    ]
                }
            ]
        },
        {
            grade: 4,
            titles: [
                {
                    title: "Số học",
                    questions: [
                        "Các số đến 100.000, 1.000.000",
                        "Phép tính với số tự nhiên lớn",
                        "Phân số: so sánh, rút gọn, quy đồng",
                        "Thực hiện phép cộng, trừ, nhân, chia phân số",
                        "Hỗn số và phép tính với hỗn số"
                    ]
                },
                {
                    title: "Hình học",
                    questions: [
                        "Hình bình hành, hình thoi",
                        "Diện tích hình bình hành, hình thoi",
                        "Chu vi các hình đa giác",
                        "Góc nhọn, góc tù, góc vuông"
                    ]
                },
                {
                    title: "Đại lượng và đo lường",
                    questions: [
                        "Đơn vị đo diện tích: cm², m², km²",
                        "Đơn vị đo khối lượng: tấn, tạ",
                        "Đơn vị đo thời gian: thế kỉ",
                        "Đơn vị đo thể tích: lít, ml"
                    ]
                },
                {
                    title: "Giải toán có lời văn",
                    questions: [
                        "Bài toán tìm hai số khi biết tổng và hiệu",
                        "Bài toán tìm hai số khi biết tổng và tỉ số",
                        "Bài toán tìm hai số khi biết hiệu và tỉ số"
                    ]
                }
            ]
        },
        {
            grade: 5,
            titles: [
                {
                    title: "Số học",
                    questions: [
                        "Số thập phân: đọc, viết, so sánh",
                        "Cộng, trừ, nhân, chia số thập phân",
                        "Quan hệ giữa phân số và số thập phân",
                        "Tỉ số phần trăm và bài toán liên quan"
                    ]
                },
                {
                    title: "Hình học",
                    questions: [
                        "Chu vi, diện tích hình tròn",
                        "Thể tích hình hộp chữ nhật, hình lập phương",
                        "Ứng dụng tính toán thực tế"
                    ]
                },
                {
                    title: "Đại lượng và đo lường",
                    questions: [
                        "Ôn tập tất cả đơn vị đo: độ dài, diện tích, thể tích, khối lượng, thời gian",
                        "Chuyển đổi giữa các đơn vị đo",
                        "Ứng dụng đo lường trong bài toán thực tế"
                    ]
                },
                {
                    title: "Giải toán có lời văn",
                    questions: [
                        "Bài toán về tỉ số phần trăm",
                        "Bài toán về chuyển động đều",
                        "Bài toán nâng cao: nhiều bước tính"
                    ]
                }
            ]
        }
    ]

    const selectedGrade = mathCurriculum.find((c) => c.grade === grade)

    return (
        <div className={`${isOpen ? "w-80" : "w-0"} h-full bg-white/70 backdrop-blur-sm border-r border-white/20 shadow-lg overflow-hidden transition-all duration-300`}>
            <div className="p-6 w-80 h-full flex flex-col">
                <div className="flex-shrink-0">
                    <button className="w-full flex items-center justify-center space-x-2 p-3 mb-4 rounded-xl bg-blue-500 hover:bg-blue-600 text-white transition-all duration-200">
                        <svg
                            className="w-5 h-5"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            strokeWidth={1.5}
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                            />
                        </svg>
                        <span className="font-medium">
                            Tạo cuộc trò chuyện mới
                        </span>
                    </button>
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                            Câu hỏi gợi ý
                        </h2>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto pr-2 space-y-4 custom-scrollbar">
                    {selectedGrade?.titles.map((title, titleIndex) => (
                        <div key={titleIndex} className="space-y-2">
                            <button
                                onClick={() => toggleCategory(titleIndex)}
                                className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-white/30 transition-all duration-200 group">
                                <h3 className="text-sm font-medium text-gray-700 uppercase tracking-wide group-hover:text-blue-600">
                                    {title.title}
                                </h3>
                                <svg className={`w-4 h-4 text-gray-500 group-hover:text-blue-600 transition-all duration-200 ${expandedCategories.includes(titleIndex) ? "rotate-180" : ""}`} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" ><path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                                </svg>
                            </button>

                            <div
                                className={`overflow-hidden transition-all duration-300 ${expandedCategories.includes(titleIndex) ? "max-h-96 opacity-100" : "max-h-0 opacity-0"
                                    }`}
                            >
                                <div className="space-y-2 pl-2">
                                    {title.questions.map((question, questionIndex) => (
                                        <button
                                            key={questionIndex}
                                            onClick={() => onQuestionClick(question)}
                                            className="w-full text-left p-3 rounded-xl bg-white/50 hover:bg-white/80 border border-white/30 hover:border-blue-200 transition-all duration-200 text-sm text-gray-700 hover:text-blue-600 group"
                                        >
                                            <div className="flex space-x-2">
                                                <div className="mt-2 w-1.5 h-1.5 min-w-[6px] min-h-[6px] rounded-full bg-blue-400 group-hover:bg-blue-600 transition-colors flex-shrink-0"></div>
                                                <span>{question}</span>
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="p-4 border-t border-white/30 bg-white/50 text-xs text-gray-500 text-center">
                    “Mỗi ngày học thêm một điều mới 🌱”
                </div>
            </div>
        </div>
    )
}
