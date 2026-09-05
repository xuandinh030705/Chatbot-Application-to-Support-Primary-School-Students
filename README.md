# Chatbot Kilovia — Application to Support Primary School Students

Chatbot Kilovia là ứng dụng hỗ trợ học sinh tiểu học (lớp 1–5) giải toán thông qua trợ lý AI. Hệ thống sử dụng LLM (OpenAI / Groq) kết hợp với LangChain agents và prompt chuyên biệt theo chương trình từng khối lớp để trả lời bằng lời giải từng bước, không dùng ẩn số/phương trình vượt cấp.

> Repository: https://github.com/xuandinh030705/Chatbot-Application-to-Support-Primary-School-Students

## Features

- **Chat Toán tiểu học 1–5**: giải bài tập theo từng bước, bám sát ví dụ tham khảo và khung chương trình từng lớp
- **Phân loại dạng toán**: tự động nhận diện 15+ dạng bài (chu vi/diện tích, cấu tạo số, trung bình cộng, tổng-hiệu, tỉ số, vận tốc-quãng đường-thời gian, v.v.)
- **Agent kiểm duyệt (Solver → Checker)**: mô hình Groq `openai/gpt-oss-120b` giải và kiểm duyệt để tránh dùng phương pháp vượt cấp
- **Quản lý hội thoại**: lưu lịch sử chat theo user/conversation trong MySQL (SQLAlchemy)
- **Xác thực đơn giản**: đăng nhập/đăng ký bằng email + grade, phân biệt role `USER`/`PARENT`
- **Streaming**: endpoint SSE `/api/v1/chat/ask-stream` cho trải nghiệm trả lời theo thời gian thực
- **Frontend hiện đại**: React 19 + Vite + Tailwind, hỗ trợ markdown, gợi ý câu hỏi

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11, FastAPI 0.115, Uvicorn, SQLAlchemy 2.0, PyMySQL, Pydantic, dependency-injector |
| **LLM / AI** | OpenAI API (`gpt-4-turbo` / `gpt-4o`), Groq (`openai/gpt-oss-120b`), LangChain, LangChain-Groq |
| **Database** | MySQL 8.0 |
| **Frontend** | React 19, Vite 7, TypeScript 5.9, Tailwind CSS 4, React Router 7, Axios, React Markdown, PrismJS |
| **Infra** | Docker, Docker Compose, Nginx (production frontend) |

## Project Structure

```text
.
├── docker-compose.yaml          # Orchestrate MySQL + Backend + Frontend
├── .gitignore
├── .env.example                 # Root env template
├── README.md
├── data/                        # Tài liệu chương trình (docx placeholder)
└── src/
    ├── backend/
    │   ├── app/
    │   │   ├── main.py          # FastAPI entry, CORS, request_id middleware
    │   │   ├── containers.py    # DI container (UserService, ChatService)
    │   │   ├── api/
    │   │   │   └── v1/
    │   │   │       ├── chat_routes.py
    │   │   │       └── user_routes.py
    │   │   ├── core/
    │   │   │   ├── db.py        # SQLAlchemy engine (MySQL)
    │   │   │   ├── agents/
    │   │   │   │   ├── math_agent.py        # Main agent (OpenAI)
    │   │   │   │   ├── math_agent_ver3.py   # Solver→Checker (Groq)
    │   │   │   │   └── tools/math_tool.py
    │   │   │   └── prompts/
    │   │   │       ├── prompt_math_student.txt
    │   │   │       ├── prompt_math_parent.txt
    │   │   │       └── class/class_1..5.txt
    │   │   ├── models/          # SQLAlchemy models: user, chat
    │   │   ├── schemas/         # Pydantic schemas
    │   │   ├── services/        # chat_service, user_service
    │   │   └── utils/           # call_llm_api, prompt_utils, logger_utils
    │   ├── db/schema.sql        # DDL: users, conversations, messages
    │   ├── logs/                # Rotating logs (ignored, keep .gitkeep)
    │   ├── data.json            # Sample problem database
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── .env.example
    └── frontend/
        ├── public/              # Static assets (logo_*.png)
        ├── src/
        │   ├── components/      # chat-window, message, sidebar, input-box, header
        │   ├── pages/           # chat.tsx, login.tsx
        │   ├── contexts/user-context.tsx
        │   ├── libs/hooks/use-chat.tsx  # SSE via EventSource
        │   ├── types/types.ts
        │   ├── app.tsx          # Router with basename /chatbot_kilovia
        │   ├── main.tsx
        │   └── index.css
        ├── index.html
        ├── vite.config.js       # base: /chatbot_kilovia/, dev port 3999
        ├── tsconfig.json
        ├── package.json
        ├── Dockerfile           # Multi-stage build + Nginx
        └── .env.example
```

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL 8.0 (hoặc Docker)
- API keys: [OpenAI](https://platform.openai.com/api-keys) và [Groq](https://console.groq.com/keys)

### Option A — Docker Compose (Recommended)

```bash
# 1. Clone
git clone https://github.com/xuandinh030705/Chatbot-Application-to-Support-Primary-School-Students.git
cd Chatbot-Application-to-Support-Primary-School-Students

# 2. Cấu hình env backend
copy src\backend\.env.example src\backend\.env
# Linux/macOS: cp src/backend/.env.example src/backend/.env
# Chỉnh OPENAI_API_KEY, GROQ_API_KEY trong src/backend/.env

# 3. Cấu hình env frontend (optional, mặc định đã có trong compose)
copy src\frontend\.env.example src\frontend\.env
# Đảm bảo VITE_API_BASE_URL=http://localhost:8000

# 4. Chạy toàn bộ stack
docker compose up --build
```

Services sau khi chạy:

| Service | URL |
|---------|-----|
| Frontend (docker vite) | http://localhost:5173 |
| Backend (FastAPI) | http://localhost:8000 |
| MySQL | localhost:3400 (user: `chatbot_user` / pass: `chatbot_pass` / db: `chatbot_db`) |
| API Docs (Swagger) | http://localhost:8000/docs |

### Option B — Run Locally (không Docker)

**Backend:**

```bash
cd src/backend

# 1. Tạo venv
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# 2. Env
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
# Điền OPENAI_API_KEY, GROQ_API_KEY, DB_*

# 3. Chuẩn bị MySQL
# Tạo database chatbot_db và chạy schema:
# mysql -u root -p < db/schema.sql
# Hoặc chạy MySQL Docker riêng:
# docker run --name mysql_chatbot -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=chatbot_db -e MYSQL_USER=chatbot_user -e MYSQL_PASSWORD=chatbot_pass -p 3400:3306 -d mysql:8.0

# 4. Chạy backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**

```bash
cd src/frontend

npm install

copy .env.example .env        # Windows
# cp .env.example .env

# .env phải chứa:
# VITE_API_BASE_URL=http://localhost:8000

npm run dev
# Vite chạy tại http://localhost:3999 (config) hoặc http://localhost:5173
# Base path: /chatbot_kilovia/
npm run build   # build production -> dist/
npm run preview # preview build
```

## Configuration

### Backend — `src/backend/.env`

```env
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
OPENAI_ORG_ID=           # optional
OPENAI_PROJECT_ID=       # optional
GOOGLE_CAPTCHA_SECRET=

DB_HOST=localhost
DB_PORT=3400
DB_NAME=chatbot_db
DB_USER=chatbot_user
DB_PASSWORD=chatbot_pass

FRONTEND_URL=http://localhost:5173
```

### Frontend — `src/frontend/.env`

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Docker Compose Environment

`docker-compose.yaml` đã cấu hình sẵn MySQL và inject `DATABASE_URL` cho backend. Nếu chạy backend ngoài Docker, dùng `DB_*` trong `.env`; nếu chạy qua compose, backend tự nhận `DATABASE_URL` từ compose env.

## Usage

1. Mở Frontend `http://localhost:5173` (docker) hoặc `http://localhost:3999` (local vite).
2. Đăng nhập bằng email đã tồn tại (hoặc gọi API `/api/v1/user/register` để tạo user mới).
3. Nhập câu hỏi Toán lớp 1–5, ví dụ:
   - `Tìm một số thập phân, biết rằng nếu dời dấu phẩy sang phải 1 chữ số ta sẽ được số mới lớn hơn số phải tìm là 21,06`
   - `Cho phân số 35/45, bớt cả tử và mẫu đi a đơn vị thì được 2/3. Tìm a`
4. Chat lưu theo `conversation_id` (tự tạo nếu chưa có active conversation cho user).

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/chat/health` | Health check |
| `GET` | `/api/v1/chat/user/{user_id}` | Lấy lịch sử hội thoại (10 tin gần nhất) |
| `POST` | `/api/v1/chat/ask` | Hỏi đáp (non-stream) — body: `{sender_id, content}` |
| `GET` | `/api/v1/chat/ask-stream?sender_id=&content=&model=` | Streaming SSE |
| `POST` | `/api/v1/user/login` | Đăng nhập — body: `{email}` |
| `POST` | `/api/v1/user/register` | Đăng ký — body: `{email, first_name, last_name, grade}` |

Swagger: `http://localhost:8000/docs`

## Database

Schema tại `src/backend/db/schema.sql`:

```sql
users(id, email, role, first_name, last_name, grade, created_at)
conversations(id, user_id, status, created_at)
messages(id, conversation_id, role, content, created_at)
```

## Future Improvements

- Thêm xác thực JWT / OAuth thay vì email-only
- RAG với tài liệu SGK để tăng độ chính xác theo chương trình
- Hỗ trợ LaTeX rendering cho công thức toán
- Đánh giá tự động (evaluation) cho từng dạng toán
- Rate limiting và kiểm duyệt nội dung đầu vào

## License

Chưa khai báo license. Mặc định giữ bản quyền tác giả. Nếu muốn open-source, cân nhắc thêm `MIT` hoặc `Apache-2.0`.

---

> Lưu ý: `.env` chứa secrets — không commit. Dùng `.env.example` làm template.
