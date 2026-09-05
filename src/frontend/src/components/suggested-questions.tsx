"use client"

interface SuggestedQuestionsProps {
    onQuestionClick: (question: string) => void
}

const suggestedQuestions = [
    "Làm thế nào để cộng hai số có nhớ?",
    "Cách trừ các số có nhiều chữ số?",
    "Làm sao để học bảng cửu chương nhanh?",
    "Hướng dẫn giải toán có lời văn lớp 3?",
    "Cách tính chu vi hình chữ nhật?",
    "Làm sao nhận biết số chẵn và số lẻ?",
];

export default function SuggestedQuestions({ onQuestionClick }: SuggestedQuestionsProps) {
    return (
        <div className="w-full max-w-5xl px-6 pb-4">
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl border border-white/20 shadow-lg p-4">
                <h4 className="text-sm font-medium text-gray-700 mb-3">Câu hỏi gợi ý:</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {suggestedQuestions.map((question, index) => (
                        <button
                            key={index}
                            onClick={() => onQuestionClick(question)}
                            className="text-left p-3 rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 border border-blue-100 hover:border-blue-200 transition-all duration-200 text-sm text-gray-700 hover:text-gray-800 group"
                        >
                            <span className="group-hover:translate-x-1 transition-transform duration-200 inline-block">
                                {question}
                            </span>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    )
}
