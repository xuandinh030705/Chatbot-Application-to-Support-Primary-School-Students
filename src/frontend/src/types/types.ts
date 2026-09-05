export type RoleSystem = 'student' | 'parent' | 'teacher' | 'user' | 'assistant';



export interface Message {
    id: string;
    role: RoleSystem;
    content: string;
    created_at: string;
}

export interface AskRequest {
    sender_id: string;
    content: string;
    provider_model: string
}

export interface AskResponse {
    question: Message;
    answer: Message;
}

export interface User {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
    role: RoleSystem;
    grade: number;
}

