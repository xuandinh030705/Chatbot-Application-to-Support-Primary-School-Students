import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { User } from "@/types/types";

interface UserContextType {
    user: User | null;
    setUser: (user: User | null) => void;
    loading: boolean;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUserState] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        try {
            const storedUser = localStorage.getItem("user");
            // console.log("Stored user from localStorage:", storedUser);
            if (storedUser) {
                setUserState(JSON.parse(storedUser));
            }
        } catch (err) {
            // console.error("Lỗi parse user từ localStorage:", err);
            // Nếu lỗi thì xóa user hỏng khỏi localStorage
            localStorage.removeItem("user");
            setUserState(null);
        } finally {
            setLoading(false);
        }
    }, []);

    const setUser = (user: User | null) => {
        // console.log("Setting user:", user);
        setUserState(user);
        if (user) {
            localStorage.setItem("user", JSON.stringify(user));
        } else {
            localStorage.removeItem("user");
        }
    };

    return (
        <UserContext.Provider value={{ user, setUser, loading }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error("useUser must be used within a UserProvider");
    }
    return context;
};
