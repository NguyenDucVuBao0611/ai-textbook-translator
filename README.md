# AI Textbook Translator (Anh - Việt)

Ứng dụng web dịch giáo trình/sách AI từ tiếng Anh sang tiếng Việt, sử dụng mô hình dịch máy được fine-tune riêng, kèm khả năng diễn giải thuật ngữ chuyên ngành cho người mới học và trợ lý AI tương tác để hỏi thêm ngay trong tài liệu.

Dự án cá nhân, mục tiêu học tập/đồ án.

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng chính](#tính-năng-chính)
- [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cài đặt](#cài-đặt)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
- [Huấn luyện model](#huấn-luyện-model)
- [Kết quả đánh giá](#kết-quả-đánh-giá)
- [Lộ trình phát triển](#lộ-trình-phát-triển)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Giấy phép](#giấy-phép)

---

## Giới thiệu

Các công cụ dịch máy tổng quát (Google Translate, model dịch chung...) thường dịch đúng nghĩa đen nhưng khó hiểu với thuật ngữ chuyên ngành AI/ML, đặc biệt với người mới học. Dự án này giải quyết vấn đề đó bằng cách:

1. Fine-tune một model dịch máy mã nguồn mở (NLLB-200) riêng cho domain giáo trình AI
2. Xây dựng glossary thuật ngữ AI/ML kèm bản diễn giải dễ hiểu, dựa trên cách hiểu thực tế qua giáo trình và bài giảng
3. Cung cấp 2 chế độ dịch: **Academic** (giữ thuật ngữ chuẩn) và **Beginner** (dịch diễn giải, định dạng: `Thuật ngữ gốc (thuật ngữ dịch dễ hiểu)` - ví dụ: `Gradient Descent (thuật toán xuống dốc)`)
4. Tích hợp trợ lý AI tương tác: bôi đen đoạn văn để hỏi thêm ngay trong ứng dụng

## Tính năng chính

- Upload và dịch tài liệu định dạng `.docx`, `.pdf`, `.txt`
- Xử lý được tài liệu lớn (cả chương sách) nhờ chunking thông minh, giữ thuật ngữ nhất quán xuyên suốt
- Cơ chế dịch streaming theo trang: dịch xong trang nào hiển thị ngay trang đó trên giao diện, giảm thời gian chờ đợi
- Giữ nguyên công thức toán, bảng biểu, heading khi dịch
- 2 chế độ dịch: Academic / Beginner (định dạng `Thuật ngữ gốc (dịch diễn giải)` ví dụ: `Gradient Descent (thuật toán xuống dốc)`)
- Hỗ trợ Tooltip thông minh: hover chuột vào từ dịch tiếng Việt sẽ hiển thị thuật ngữ tiếng Anh gốc tương ứng
- Trợ lý AI tương tác: bôi đen văn bản → chuột phải → "Hỏi AI" → panel giải thích bên cạnh. Hỗ trợ lưu lịch sử hỏi AI theo từng tài liệu và vị trí dưới dạng ghi chú (không bị mất khi mở lại tài liệu)
- Tích hợp linh hoạt AI Panel: hỗ trợ API bên ngoài (Claude/GPT) hoặc chạy LLM local qua Ollama (Llama 3,...) để tiết kiệm chi phí
- Chụp màn hình nội dung trong app để hỏi AI trực tiếp
- Theo dõi tiến độ dịch theo thời gian thực (xử lý bất đồng bộ)

## Kiến trúc hệ thống

```
┌─────────────┐      upload file       ┌──────────────────┐
│   Frontend   │ ─────────────────────▶ │  FastAPI Backend  │
│ (Web App UI) │ ◀───────────────────── │                   │
└─────────────┘      kết quả dịch       └─────────┬─────────┘
       │                                          │
       │ bôi đen / screenshot                     ▼
       ▼                                 ┌───────────────────┐
┌─────────────┐                          │  Translation Engine│
│  AI Panel    │◀──── gọi API ngoài / ───│  - Stage 1: NLLB   │
│(Claude/GPT/ │     Ollama local         │    (dịch nghĩa)    │
│   Ollama)   │                          │  - Stage 2: Rewrite│
└─────────────┘                          │    (dễ hiểu hơn)   │
                                          │  - Glossary lookup │
                                          └───────────────────┘
```

Model dịch (Stage 1 + Stage 2) chạy độc lập, không cần internet sau khi tải về (fine-tune xong và host trên máy/Hugging Face). Module trợ lý AI tương tác dùng API bên ngoài (Claude/OpenAI), tách biệt hoàn toàn khỏi phần dịch chính.

## Giải pháp xử lý tài liệu phức tạp

Để đảm bảo tài liệu sau khi dịch không bị lỗi cấu trúc và vẫn dịch được các nội dung phi văn bản thô, hệ thống áp dụng các kỹ thuật sau:

1. **Công thức toán học (Formulas):**
   - Sử dụng kỹ thuật **Masking/Placeholder**: Dùng Regex nhận diện các ký tự công thức (LaTeX/MathML) và thay thế bằng các nhãn tạm thời `[MATH_0]`, `[MATH_1]` trước khi dịch.
   - Sau khi dịch xong văn bản thô, hệ thống sẽ khôi phục (Unmasking) công thức gốc vào đúng vị trí nhãn tạm.

2. **Bảng biểu (Tables):**
   - Duyệt và dịch theo từng ô (**Cell-by-Cell**): Sử dụng thư viện cấu trúc (`python-docx` hoặc `pdfplumber`) để đọc dữ liệu của từng ô trong bảng, giữ nguyên định dạng (in đậm, in nghiêng, cỡ chữ) và chỉ dịch phần chữ bên trong từng ô, sau đó ghi đè lại cấu trúc bảng.
   - **Tối ưu hóa layout:** Thiết lập `autofit = False` và cho phép các cột tự động co giãn chiều cao dòng thay vì cố định kích thước để tránh chữ bị cắt/mất nét khi bản dịch tiếng Việt dài hơn bản gốc.

3. **Hình ảnh & Đồ thị (Images & Graphs):**
   - Áp dụng phương pháp **Dịch đè chữ trên ảnh (Image Translation)**:
     - **OCR (Nhận diện chữ):** Sử dụng `EasyOCR` hoặc `Tesseract OCR` để định vị tọa độ và nhận diện chữ tiếng Anh trên hình ảnh/đồ thị. Xử lý OCR đối với chữ viết dọc trên đồ thị bằng cách thử nghiệm nhiều góc xoay ảnh khác nhau, tích hợp cơ chế fallback giữ nguyên hình ảnh gốc nếu độ tin cậy (confidence score) quá thấp.
     - **Dịch thuật:** Dịch các nhãn/chữ tìm được sang tiếng Việt bằng model dịch.
     - **Inpainting (Xóa chữ cũ):** Dùng kỹ thuật xử lý ảnh để xóa vùng chữ tiếng Anh cũ và lấp đầy bằng màu nền tương ứng.
     - **Render Text (Vẽ chữ mới):** Vẽ đè chữ tiếng Việt đã dịch lên đúng vị trí tọa độ cũ bằng thư viện đồ họa (`Pillow` / `OpenCV`). Hỗ trợ tự động thay đổi kích thước phông chữ (auto-resize font) hoặc tự động rút gọn chữ (ưu tiên dùng bản glossary ngắn thay vì bản diễn giải dài) khi bản dịch tiếng Việt dài hơn bản gốc để tránh hiện tượng tràn khung (text overflow).
     - **Ngưỡng cảnh báo & Fallback:** Nếu bản dịch trong hình dài hơn bản gốc quá nhiều (ví dụ > 40-50%), hệ thống tự động fallback giữ nguyên bản tiếng Anh trong hình và thêm chú thích dịch bên dưới/bên cạnh hình thay vì cố vẽ đè.
     - **Tránh vẽ đè đồ thị phức tạp:** Đối với sơ đồ kiến trúc mạng nhiều nhánh hoặc đồ thị dày đặc nhãn, hệ thống sẽ giữ nguyên ảnh gốc và bổ sung phần dịch dưới dạng chú thích riêng bên dưới ảnh để tránh rủi ro vỡ cấu trúc và lem nhem hình ảnh.

4. **Lưu lịch sử hỏi đáp AI (AI Chat History Storage):**
   - Để tránh mất lịch sử hỏi đáp khi đóng ứng dụng hoặc mở lại tài liệu, hệ thống sử dụng một cơ sở dữ liệu lightweight **SQLite** ở backend.
   - Dữ liệu được lưu trữ theo bảng gồm các trường chính: `document_id` (hash MD5 của file tài liệu), `selection_text` (đoạn text được bôi đen), `position_metadata` (tọa độ/vị trí trang để đánh dấu highlight), và `chat_history` (chuỗi JSON chứa các lượt hội thoại hỏi đáp với AI).

### Hướng xử lý chống vỡ Layout & Giới hạn Scope dự án

Khi dịch tài liệu từ tiếng Anh sang tiếng Việt, độ dài văn bản thường tăng lên (reflow), dễ gây vỡ cấu trúc trang. Dự án áp dụng các nguyên tắc thiết kế thực tế sau:
- **Chấp nhận reflow tự nhiên (Khuyên dùng cho scope đồ án):** Không cố định số trang của tài liệu đầu ra khớp 100% với tài liệu gốc. Để trình đọc Word/PDF tự tính toán lại layout và phân trang khi văn bản dịch dài ra. Đây là cách xử lý đơn giản, hiệu quả và được áp dụng phổ biến ở cả các công cụ dịch thương mại.
- **Giới hạn scope thực tế:** Dịch giữ nguyên 100% layout gốc của các định dạng tài liệu phức tạp là một bài toán cực kỳ khó. Dự án sẽ tập trung tối ưu hóa chất lượng dịch thuật và cấu trúc văn bản thô, phần hình ảnh phức tạp chỉ thực hiện demo xử lý ở mức cơ bản và ghi nhận đây là giới hạn kỹ thuật (known limitation) trong báo cáo.

## Cấu trúc thư mục

```
translate-ai-textbook/
├── README.md
├── .gitignore
├── requirements.txt
├── backend/
│   ├── main.py                # FastAPI app, định nghĩa các endpoint
│   ├── translate.py           # Load model, gọi inference Stage 1 & 2
│   ├── file_processor.py      # Trích xuất/ghép text từ docx, pdf, txt
│   ├── chunking.py            # Chia nhỏ văn bản theo đoạn/câu
│   ├── glossary.py            # Logic tra cứu & thay thế thuật ngữ
│   └── ai_assistant.py        # Module gọi API AI cho tính năng hỏi-đáp
├── frontend/
│   ├── index.html / App.jsx   # Giao diện upload, hiển thị kết quả
│   └── components/
│       └── AIPanel.jsx        # Side panel hỏi AI
├── data/
│   ├── glossary.csv           # Bảng thuật ngữ AI/ML: EN | VI chuẩn | VI diễn giải
│   ├── handmade_pairs.csv     # Cặp câu "khó → cách bạn diễn giải" tự viết
│   └── sample_sentences.csv   # Vài câu mẫu để test nhanh (không phải full dataset)
├── notebooks/
│   ├── baseline_test.ipynb    # Test NLLB gốc, ghi nhận lỗi
│   ├── finetune_stage1.ipynb  # Fine-tune dịch nghĩa (chạy trên Kaggle)
│   └── finetune_stage2.ipynb  # Fine-tune viết lại dễ hiểu (chạy trên Kaggle)
└── docs/
    └── report.md              # Báo cáo, số liệu BLEU, case study
```

## Cài đặt

### Yêu cầu

- Python 3.10+
- Không bắt buộc GPU cho backend/frontend (chỉ dùng CPU để inference, chậm hơn nhưng chạy được)
- Tài khoản [Kaggle](https://www.kaggle.com) (để fine-tune, có GPU miễn phí)
- Tài khoản [Hugging Face](https://huggingface.co) (để lưu và tải model đã fine-tune)
- API key Claude hoặc OpenAI (cho tính năng trợ lý AI tương tác, tùy chọn)

### Các bước

```bash
# Clone repo
git clone https://github.com/<your-username>/translate-ai-textbook.git
cd translate-ai-textbook

# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Cài thư viện
pip install -r requirements.txt
```

Tạo file `.env` ở thư mục gốc:

```
HF_MODEL_STAGE1=your-username/nllb-envi-ai-textbook-stage1
HF_MODEL_STAGE2=your-username/nllb-envi-ai-textbook-stage2
ANTHROPIC_API_KEY=your_api_key_here   # cho tính năng trợ lý AI (tùy chọn)
```

Chạy backend:

```bash
cd backend
uvicorn main:app --reload
```

Chạy frontend (nếu dùng React):

```bash
cd frontend
npm install
npm start
```

## Hướng dẫn sử dụng

1. Mở ứng dụng, upload file giáo trình (`.docx`, `.pdf`, `.txt`)
2. Chọn chế độ dịch: **Academic** (giữ thuật ngữ chuẩn) hoặc **Beginner** (diễn giải dễ hiểu)
3. Theo dõi thanh tiến độ khi hệ thống xử lý (với tài liệu lớn có thể mất vài phút, xử lý bất đồng bộ)
4. Xem/tải file kết quả sau khi dịch xong
5. Trong lúc đọc bản dịch, bôi đen bất kỳ đoạn nào và chọn "Hỏi AI" để mở panel giải thích thêm
6. Có thể chụp ảnh màn hình nội dung trong app và gửi kèm câu hỏi cho AI

## Huấn luyện model

Model được huấn luyện theo 2 giai đoạn, chạy trên Kaggle (GPU T4/P100 miễn phí):

**Stage 1 — Dịch nghĩa (literal translation)**
- Model nền: NLLB-200 distilled (600M)
- Dữ liệu: PhoMT + OPUS (nền chung) + tập câu AI/ML tự thu thập/đối chiếu
- Notebook: `notebooks/finetune_stage1.ipynb`

**Stage 2 — Viết lại dễ hiểu (explanatory rewrite)**
- Input: bản dịch nghĩa đen từ Stage 1
- Output: bản diễn giải dựa trên cách hiểu thực tế (dữ liệu tự viết + AI-assisted augmentation, đã qua review thủ công)
- Notebook: `notebooks/finetune_stage2.ipynb`
- Fallback: nếu Stage 2 không đạt chất lượng mong muốn, hệ thống dùng rule-based thay thế theo `glossary.csv`

Sau khi huấn luyện, model được đẩy lên Hugging Face Hub:

```python
model.push_to_hub("your-username/nllb-envi-ai-textbook-stage1")
tokenizer.push_to_hub("your-username/nllb-envi-ai-textbook-stage1")
```

Model weights **không** được lưu trong repo GitHub này (xem `.gitignore`), chỉ tải qua Hugging Face khi chạy backend.

## Kết quả đánh giá

| Model | BLEU (tập test chung) | BLEU (tập test AI/ML) | Ghi chú |
|---|---|---|---|
| NLLB gốc (chưa fine-tune) | _đang cập nhật_ | _đang cập nhật_ | Baseline |
| Stage 1 (fine-tune PhoMT + AI domain) | _đang cập nhật_ | _đang cập nhật_ | |
| Stage 1 + Stage 2 (rewrite) | — | _đánh giá bằng human evaluation_ | BLEU không phù hợp đo độ dễ hiểu |

Đánh giá bổ sung: khảo sát người đọc (chưa quen thuật ngữ AI) về mức độ dễ hiểu của bản dịch chế độ Beginner so với bản Academic. Chi tiết xem `docs/report.md`.

## Lộ trình phát triển

Dự án phát triển theo các milestone tuần. Chi tiết kế hoạch, các đầu việc cụ thể và tiêu chí hoàn thành của từng milestone xem tại [docs/roadmap.md](file:///c:/Users/Nguyen%20Duc%20Vu%20Bao/ai-textbook-translator/docs/roadmap.md).

Tóm tắt lộ trình chính:
1. Nền tảng + test baseline NLLB
2. Xây glossary + dữ liệu tự viết (câu khó → diễn giải)
3. Fine-tune Stage 1 (dịch nghĩa nền) trên Kaggle
4. Fine-tune Stage 2 (viết lại dễ hiểu) trên Kaggle
5. Xử lý tài liệu lớn (chunking, giữ định dạng) + Backend
6. Frontend + Web app cơ bản
7. Trợ lý AI tương tác (bôi đen hỏi AI, chụp màn hình hỏi AI)
8. Đánh giá tổng thể + hoàn thiện báo cáo

## Công nghệ sử dụng

- **Model dịch:** NLLB-200 (Meta), Hugging Face `transformers`, `datasets`
- **Huấn luyện:** Kaggle Notebook (GPU T4/P100 miễn phí)
- **Lưu trữ model:** Hugging Face Hub
- **Backend:** Python, FastAPI (hỗ trợ Server-Sent Events / WebSockets cho cơ chế Dịch Streaming)
- **Cơ sở dữ liệu:** SQLite / SQLAlchemy (lưu trữ lịch sử hội thoại AI và metadata vị trí note)
- **Xử lý file:** `python-docx`, `pdfplumber`
- **Xử lý ảnh & OCR:** `EasyOCR` / `Tesseract`, `Pillow` (PIL), `opencv-python`
- **Frontend:** React (hoặc HTML/CSS/JS thuần)
- **Trợ lý AI tương tác:** Claude API / OpenAI API hoặc Local LLM (**Ollama / Llama 3**) qua cổng API cục bộ
- **Đánh giá:** `sacrebleu` (BLEU score), human evaluation

## Giấy phép

Dự án cá nhân phục vụ mục đích học tập. Dữ liệu huấn luyện tham khảo từ các nguồn công khai (PhoMT, OPUS) và tài liệu tự tổng hợp — vui lòng kiểm tra điều khoản sử dụng của từng nguồn dữ liệu trước khi tái sử dụng cho mục đích khác.
