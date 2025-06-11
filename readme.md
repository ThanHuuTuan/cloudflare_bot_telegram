# 🌐 Hướng Dẫn Tạo Cloudflare Worker

Cloudflare Workers cho phép bạn chạy JavaScript (hoặc TypeScript) trên edge network của Cloudflare, rất hữu ích cho việc tạo API, xử lý request, v.v.

## 📌 Yêu cầu

- Tài khoản Cloudflare: [https://dash.cloudflare.com/](https://dash.cloudflare.com/)
- (Khuyến nghị) Cài đặt `Wrangler CLI`: công cụ quản lý Worker từ dòng lệnh.

---

## 🔧 Cách 1: Tạo Worker Trực Tiếp Trên Dashboard (UI)

### Bước 1: Đăng nhập Cloudflare
- Truy cập: [https://dash.cloudflare.com/](https://dash.cloudflare.com/)

### Bước 2: Chọn tab **"Workers & Pages"**
- Trong menu bên trái, chọn **"Workers & Pages"**.

### Bước 3: Tạo một Worker mới
- Bấm nút **"Create application"** hoặc **"Create Worker"**.
- Chọn **"Worker"** (không chọn Pages).
- Đặt tên cho Worker, ví dụ: `my-first-worker`.
- Chọn "Start from scratch" (bắt đầu từ đầu) hoặc chọn từ template có sẵn.

### Bước 4: Viết mã cho Worker/Lấy trong file worker.js thay thế
```js
export default {
  async fetch(request) {
    return new Response('Hello from Cloudflare Worker!', {
      headers: { 'content-type': 'text/plain' },
    });
  },
};


# 🌐 Thay thế các tham số
### Sửa telegram_bot_api.py
- Thay  **"api_url"** thành url worker của bạn.
### Thay token sample_bot và trải nghiệm
