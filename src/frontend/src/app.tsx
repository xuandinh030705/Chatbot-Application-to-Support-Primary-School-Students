import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { UserProvider } from "@/contexts/user-context";
import ChatPage from "@/pages/chat";
import LoginPage from "@/pages/login";

export default function App() {
    return (

        <UserProvider>
            <Router basename="/chatbot_kilovia">
                <Routes>
                    <Route path="/" element={<ChatPage />} />
                    <Route path="/login" element={<LoginPage />} />
                </Routes>
            </Router>
        </UserProvider>
    );
}