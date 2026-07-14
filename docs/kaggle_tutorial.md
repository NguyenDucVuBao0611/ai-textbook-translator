# Hướng Dẫn Chi Tiết Huấn Luyện (Fine-tuning) Trên Kaggle

Tài liệu này hướng dẫn bạn cách chạy 2 file notebook huấn luyện Stage 1 và Stage 2 trên Kaggle hoàn toàn miễn phí.

---

## 🔑 BƯỚC 1: Lấy Token Quyền Ghi (Write) Trên Hugging Face
Vì sau khi huấn luyện xong, mô hình sẽ được tự động đẩy lên tài khoản Hugging Face của bạn, bạn cần cấp quyền cho Kaggle làm việc này:
1. Truy cập: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Bấm **Create new token** (hoặc **New token**).
3. Đặt tên token (Ví dụ: `kaggle-train`).
4. Tại mục **Role**, chọn **Write** (bắt buộc phải là Write mới đẩy được model lên).
5. Bấm **Generate a token** và copy đoạn mã token hiển thị trên màn hình.

---

## 🛠️ BƯỚC 2: Tạo Notebook Trên Kaggle & Import Code
1. Truy cập [Kaggle](https://www.kaggle.com) và đăng nhập.
2. Tại menu bên trái, bấm vào nút **Code** $\rightarrow$ Chọn **New Notebook**.
3. Tại giao diện notebook mới mở, bấm vào menu **File** (ở góc trên bên trái) $\rightarrow$ Chọn **Import Notebook**.
4. Kéo thả file `notebooks/finetune_stage1.ipynb` từ máy tính của bạn vào và bấm **Import**.

---

## ⚙️ BƯỚC 3: Cấu Hình Môi Trường Chạy (Quan trọng)
Ở cột thuộc tính bên phải màn hình Kaggle (mục **Settings**), bạn cần cấu hình chính xác các mục sau:
1. **Accelerator (Bộ tăng tốc phần cứng):** 
   * Chọn **GPU T4 x2** hoặc **GPU P100** (Kaggle sẽ cấp card đồ họa miễn phí để chạy).
2. **Internet on (Kết nối mạng):** 
   * Bật **On** (chuyển công tắc sang màu xanh). Nếu không bật, Kaggle sẽ không thể tải thư viện và mô hình NLLB từ Hugging Face về.
3. **Secrets (Cấu hình mã bảo mật):**
   * Bấm vào nút **Add-ons** ở thanh menu trên cùng $\rightarrow$ Chọn **Secrets**.
   * Bấm **Add secret**.
   * Cột **Label** nhập: `HF_TOKEN`.
   * Cột **Value** dán đoạn mã Access Token bạn đã copy ở Bước 1.
   * Đánh dấu tích vào ô **Attach** bên cạnh nhãn `HF_TOKEN`.
   * Bấm **Save**.

---

## 📝 BƯỚC 4: Điều Chỉnh Code Trong Notebook Cho Đúng Tài Khoản Của Bạn
Trước khi bấm chạy, bạn cần sửa tên tài khoản Hugging Face của bạn trong code để mô hình đẩy lên đúng trang của bạn:
1. Cuộn xuống ô code số **6** (Cấu hình `Seq2SeqTrainingArguments`).
2. Tìm dòng:
   ```python
   hub_model_id="your_hf_username/nllb-envi-ai-textbook-stage1"
   ```
3. Sửa `"your_hf_username"` thành username tài khoản Hugging Face của bạn. (Ví dụ tài khoản của bạn là `nguyenvubao` thì đổi thành `hub_model_id="nguyenvubao/nllb-envi-ai-textbook-stage1"`).

---

## 🏃‍♂️ BƯỚC 5: Bắt Đầu Chạy
1. Bấm vào nút **Run All** ở góc trên bên phải màn hình (hoặc nhấn phím tắt `Ctrl + Shift + Enter`).
2. Hệ thống sẽ tự động chạy tất cả các bước. Bạn có thể theo dõi tiến độ ở từng ô code.
3. Khi chạy đến ô đăng nhập Hugging Face, nó sẽ tự động lấy token `HF_TOKEN` bạn cấu hình ở Bước 3 để đăng nhập mà bạn không cần phải gõ gì thêm.
4. **Thời gian chạy:** Khoảng 30 phút đến 1 tiếng. Khi hoàn thành, bạn truy cập vào Hugging Face của mình sẽ thấy một repository mới chứa mô hình đã được lưu thành công!

---

## 🔄 BƯỚC 6: Đối Với Stage 2 (Viết Lại Dễ Hiểu)
Sau khi Stage 1 chạy xong, bạn tạo một notebook mới trên Kaggle và import file [notebooks/finetune_stage2.ipynb](file:///c:/Users/Nguyen%20Duc%20Vu%20Bao/ai-textbook-translator/notebooks/finetune_stage2.ipynb) lên.
1. **Tải file dữ liệu mẫu lên Kaggle:**
   * Ở cột bên phải Kaggle, mục **Data** $\rightarrow$ Bấm **Upload data** $\rightarrow$ Chọn file [data/handmade_pairs.csv](file:///c:/Users/Nguyen%20Duc%20Vu%20Bao/ai-textbook-translator/data/handmade_pairs.csv) từ máy tính của bạn lên để mô hình Stage 2 học cách viết lại tiếng Việt.
2. Cấu hình GPU, Internet, Secrets và sửa `your_hf_username` thành username của bạn tương tự như Stage 1.
3. Bấm **Run All** để hoàn tất.
