# Lộ Trình Phát Triển Tăng Tốc (Có AI Hỗ Trợ) - AI Textbook Translator

Với sự hỗ trợ đắc lực từ AI (cặp lập trình viên AI Antigravity), nhiều đầu việc về lập trình, viết code mẫu, sinh dữ liệu và sửa lỗi có thể thực hiện song song hoặc tự động hóa. Lộ trình được nén từ **7 tuần xuống còn 15 ngày (3 tuần làm việc)**.

---

## 📌 Tổng Quan Lộ Trình Tăng Tốc (15 Ngày)

```mermaid
gantt
    title Lộ trình tăng tốc có AI hỗ trợ (15 Ngày)
    dateFormat  DD
    axisFormat Ngày %d
    section Phát triển
    P1: Setup, Baseline & Dữ liệu (AI sinh) :active, p1, 01, 4d
    P2: Backend, Fine-tune & Xử lý ảnh : p2, after p1, 6d
    P3: Frontend, AI Panel & E2E Test    : p3, after p2, 5d
```

---

## 🛠️ Chi Tiết Kế Hoạch 15 Ngày

### 📋 PHA 1: Khởi Tạo, Đánh Giá Baseline & Chuẩn Bị Dữ Liệu (Ngày 1 - Ngày 4)
*Mục tiêu: Thiết lập dự án, chuẩn bị tập dữ liệu huấn luyện (AI bootstrap) và đo điểm Baseline.*

*   **Ngày 1: Setup Dự án & Baseline**
    *   *Đầu việc:* Khởi tạo khung thư mục (`backend`, `frontend`, `data`, `notebooks`, `docs`), cài đặt môi trường ảo và dependencies.
    *   *AI hỗ trợ:* Tạo nhanh file `requirements.txt` và khung code kết nối mô hình NLLB-200.
    *   *Kết quả:* Chạy được script dịch thử câu đơn giản bằng NLLB gốc.
*   **Ngày 2: AI Bootstrap Glossary & Dữ liệu Dịch**
    *   *Đầu việc:* Tạo bảng thuật ngữ `glossary.csv` và tập câu huấn luyện mẫu `handmade_pairs.csv` (~1000 câu).
    *   *AI hỗ trợ:* AI tự động dịch và viết giải nghĩa cho 300+ thuật ngữ AI/ML phổ biến sang 2 chế độ (Academic/Beginner), người dùng chỉ cần kiểm duyệt lại.
*   **Ngày 3 - 4: Thiết kế CSDL & Đo Điểm Baseline**
    *   *Đầu việc:* Thiết kế SQLite schema (SQLAlchemy); Hoàn thiện và chạy `baseline_test.ipynb` trên tập dữ liệu mẫu để đo điểm BLEU ban đầu.
    *   *AI hỗ trợ:* AI sinh mã nguồn SQLite database helper và chạy viết các hàm đánh giá điểm BLEU.
    *   *Kết quả:* Có file SQLite sẵn sàng kết nối và bảng số liệu đánh giá baseline.

---

### ⚙️ PHA 2: Huấn Luyện Model, Xây Dựng Backend & Xử Lý Ảnh (Ngày 5 - Ngày 10)
*Mục tiêu: Hoàn thành huấn luyện mô hình và xây dựng bộ máy dịch cốt lõi (Backend).*

*   **Ngày 5 - 6: Huấn luyện Song Song Mô Hình (Stage 1 & Stage 2)**
    *   *Đầu việc:* Chạy fine-tune mô hình dịch NLLB (Stage 1) và mô hình viết lại (Stage 2) trên Kaggle, sau đó đẩy lên Hugging Face.
    *   *AI hỗ trợ:* AI viết toàn bộ code cho 2 file notebook huấn luyện, người dùng chỉ cần import vào Kaggle và ấn nút Chạy (Run).
*   **Ngày 7 - 8: Xây dựng Backend & API Streaming**
    *   *Đầu việc:* Viết code tách/ghép file (`file_processor.py`), module chia nhỏ văn bản (`chunking.py`), và logic dịch chính. Xây dựng API FastAPI hỗ trợ Server-Sent Events (SSE) để truyền dữ liệu dạng streaming.
    *   *AI hỗ trợ:* AI tự động viết code xử lý file DOCX/PDF phức tạp và tối ưu hóa xử lý bất đồng bộ (Async background tasks).
*   **Ngày 9 - 10: Xử lý Dịch Ảnh & Tránh Vỡ Hình**
    *   *Đầu việc:* Tích hợp OCR, thuật toán Inpainting xóa chữ cũ và vẽ đè chữ mới (có auto-resize font và cơ chế fallback giữ nguyên ảnh + dịch chú thích bên dưới).
    *   *AI hỗ trợ:* AI viết code tích hợp OpenCV/Pillow và cấu hình OCR xoay góc để phát hiện chữ viết dọc trên đồ thị.

---

### 🎨 PHA 3: Phát Triển Frontend, Tích Hợp AI Panel & E2E Testing (Ngày 11 - Ngày 15)
*Mục tiêu: Xây dựng giao diện React trực quan, kết nối AI Panel và kiểm thử hoàn thiện báo cáo.*

*   **Ngày 11 - 12: Phát triển Frontend Song Ngữ & Streaming**
    *   *Đầu việc:* Tạo giao diện upload file, giao diện đọc sách Side-by-side song ngữ, tooltip hiển thị từ gốc khi hover và cơ chế hiển thị cuốn chiếu từng trang qua SSE.
    *   *AI hỗ trợ:* AI sinh nhanh các React Component đẹp mắt bằng CSS thuần hiện đại và xử lý kết nối EventSource SSE.
*   **Ngày 13: Tích hợp AI Panel (Cloud & Local Ollama)**
    *   *Đầu việc:* Xây dựng thanh công cụ bên phải (AIPanel), kết nối với API Claude/OpenAI hoặc LLM cục bộ (Ollama / Llama 3) và SQLite để lưu lịch sử ghi chú.
    *   *AI hỗ trợ:* AI viết code kết nối API và xử lý lưu/truy vấn lịch sử ghi chú theo vị trí tài liệu.
*   **Ngày 14 - 15: Kiểm Thử E2E, Human Evaluation & Viết Báo Cáo**
    *   *Đầu việc:* Dịch thử các file giáo trình thực tế, khảo sát nhanh mức độ dễ hiểu của bản dịch và viết báo cáo hoàn thiện dự án (`docs/report.md`).
    *   *AI hỗ trợ:* AI hỗ trợ phân tích kết quả case study, tự động sinh khung báo cáo kết quả chi tiết.

---

## 📈 Cách Phân Chia Vai Trò để Tối Ưu Tốc Độ

*   **AI (Antigravity):**
    *   Viết code chức năng nhanh chóng (Backend, Frontend React Components, SQL DB helper).
    *   Soạn thảo và đề xuất nội dung Glossary, sinh dữ liệu huấn luyện mẫu (Data Augmentation).
    *   Tìm và sửa lỗi (Debugging) trong suốt quá trình chạy thử.
*   **Bạn (Người dùng / Lập trình viên chính):**
    *   Duyệt và kiểm tra chất lượng dữ liệu AI sinh ra.
    *   Chạy huấn luyện trên Kaggle (do AI đã viết sẵn code).
    *   Kiểm thử trực quan giao diện và trải nghiệm đọc thực tế.
