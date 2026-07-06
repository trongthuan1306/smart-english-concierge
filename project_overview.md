# 🚀 Tài liệu Kiến trúc Dự án: Smart English Concierge

**Smart English Concierge** là một ứng dụng AI Fullstack thông minh được thiết kế để giúp người dùng luyện tập và cải thiện tiếng Anh. Dự án sử dụng cấu trúc Multi-agent linh hoạt với sự hỗ trợ của mô hình ngôn ngữ lớn Google Gemini.

Dự án bao gồm 2 phần chính:
- **Backend**: Xây dựng bằng Python/FastAPI, giao tiếp với PostgreSQL thông qua SQLAlchemy, và tích hợp Google Gemini API.
- **Frontend**: Xây dựng bằng ReactJS, Vite và TailwindCSS.

---

## 🏗️ Cấu trúc Thư mục (Directory Structure)

```text
smart-english-concierge/
├── backend/
│   ├── agents/
│   │   ├── router.py             # Multi-Agent Graph Router (Điều hướng chính)
│   │   ├── security.py           # Bảo mật: Lọc PII & Prompt Injection
│   │   └── skills/               # Định nghĩa các kỹ năng (Skills) của Agent
│   │       ├── vocab-saver/
│   │       │   ├── SKILL.md      # Định nghĩa kỹ năng cho LLM (LLM Tool Spec)
│   │       │   └── scripts/handler.py # Code thực thi logic lưu từ vựng
│   │       └── ... (Các skills khác)
│   ├── database/                 # Layer Cơ sở dữ liệu (PostgreSQL)
│   │   ├── database.py           # Khởi tạo SQLAlchemy Engine & Session
│   │   ├── models.py             # Định nghĩa Table Schema (Vocabulary)
│   │   └── crud.py               # Các hàm tương tác với DB (Create, Read...)
│   ├── models/
│   │   └── schemas.py            # Pydantic models (Validate Request/Response)
│   ├── main.py                   # Điểm vào của FastAPI (FastAPI Entry Point)
│   └── .env                      # Lưu trữ biến môi trường (Gemini API, DB URL)
└── frontend/                     # React + Vite + TailwindCSS
    ├── src/
    │   ├── components/           # Các UI component (ChatWindow, Dashboard...)
    │   └── services/api.js       # Gọi API backend qua Axios
    ├── package.json
    └── vite.config.js
```

---

## 🧠 Phân tích chi tiết Source Code (Backend)

### 1. `main.py` - Điểm khởi đầu (Entry Point)
Là nơi khởi tạo ứng dụng FastAPI và định nghĩa các API routes chính. 
- **DB Initialization:** Gọi `Base.metadata.create_all(bind=engine)` để tự động tạo bảng trong PostgreSQL.
- **API `/api/chat` (POST):**
  - **Luồng hoạt động (Data Flow):** 
    1. Nhận tin nhắn từ người dùng (`ChatRequest`).
    2. Đi qua **Security Guardrail** (`security.py`) để lọc dữ liệu nhạy cảm (PII) hoặc chặn Prompt Injection.
    3. Truyền tin nhắn an toàn vào **Router** (`router_instance.route(sanitized_message)`).
    4. Trả về kết quả dưới dạng `ChatResponse`.
- **API `/api/vocabulary` (GET):**
  - Lấy danh sách từ vựng đã lưu. Endpoint này được sử dụng `def` thay vì `async def` để đồng bộ hoá an toàn với SQLAlchemy, tránh lỗi treo Event Loop của FastAPI.

### 2. Hệ thống Cơ sở dữ liệu (`database/`)
Hệ thống sử dụng SQLAlchemy làm ORM để giao tiếp với PostgreSQL.
- **`database.py`:** Đọc `DATABASE_URL` từ `.env`, tạo `engine` và `SessionLocal`. Hàm `get_db()` được dùng để Dependency Injection session vào các API.
- **`models.py`:** Định nghĩa class `Vocabulary` map với bảng `vocabulary` trong CSDL, chứa các cột như `word`, `meaning`, `example`, `created_at`.
- **`crud.py`:** Đóng gói các truy vấn SQL thành các hàm Python như `get_all_vocabulary(db)` hay `get_vocabulary_by_word(db, word)`.

### 3. Hệ thống Định tuyến Agent (`agents/router.py`)
Đây là bộ não của ứng dụng (Orchestrator).
- Tự động quét (auto-discovery) thư mục `skills/` và đọc các file `SKILL.md` để khởi tạo danh sách các công cụ (Tools) cung cấp cho mô hình Gemini.
- Chứa logic gọi API `genai.Client` của Google Gemini.
- Nhận phân tích ý định từ LLM, tự động gọi đúng Tool và mapping parameters để chạy file `handler.py` tương ứng của Skill đó.

### 4. Hệ thống Kỹ năng linh hoạt (`agents/skills/`)
Cấu trúc dạng modular. Mỗi skill hoạt động độc lập:
- Ví dụ: `vocab-saver`
  - `SKILL.md`: Chứa thông tin mô tả kỹ năng cho LLM đọc để biết khi nào thì cần gọi (ví dụ: "Lưu từ vựng này giúp tôi").
  - `scripts/handler.py`: Script thực thi lấy các tham số (word, meaning) từ LLM và kết nối vào DB (thông qua `crud.py`) để lưu từ.

### 5. Lớp Bảo mật (`agents/security.py`)
Được thiết kế để chặn các tin nhắn độc hại:
- Sử dụng RegEx để che giấu (redact) số điện thoại, email trước khi gửi cho LLM (bảo vệ quyền riêng tư).
- Chặn các câu lệnh cố tình "tẩy não" LLM (Prompt Injection).

---

## 🎨 Cấu trúc Frontend
Phần Frontend sử dụng ReactJS và TailwindCSS để tạo ra một giao diện hiện đại, bóng bẩy (Rich Aesthetics).
- **Vite:** Công cụ build siêu nhanh.
- **Axios (`services/api.js`):** Quản lý các requests tới Backend (port 8000).
- **Giao diện:** Tập trung vào các hiệu ứng glassmorphism, dark mode và micro-animations để tăng trải nghiệm người dùng.

---

## 📌 Tổng kết luồng dữ liệu (Data Flow)

> [!NOTE]
> **Người dùng gửi tin nhắn** ➔ **FastAPI (`main.py`)** ➔ **Security Guardrail** ➔ **Agent Router (Gemini LLM suy luận)** ➔ **Skill Handler (Code logic & Database)** ➔ **FastAPI trả kết quả về Frontend** ➔ **Cập nhật giao diện.**

Kiến trúc này cho phép mở rộng không giới hạn các Agent/Skill mới bằng cách chỉ cần tạo một thư mục mới trong `skills/` mà không cần sửa core logic của router.
