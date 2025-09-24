# 📅 Planner-Backtracking

![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232a?logo=react&logoColor=61dafb)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=yellow)
![License](https://img.shields.io/badge/license-MIT-green)

Ứng dụng **Planner lịch học** với thuật toán **Backtracking** để sắp xếp thời khóa biểu tối ưu.  
Dự án gồm 2 phần chính:

- 🖥 **Frontend (ReactJS + Bootstrap)** → Nhập dữ liệu lớp/môn, hiển thị kết quả  
- ⚙️ **Backend (FastAPI + Python)** → Xử lý backtracking, kiểm tra ràng buộc, trả về lịch  

---



## 📦 Cấu trúc dự án

```
planner-backtracking/
├── backend/               # FastAPI server + solver backtracking
│   ├── main.py
│   └── ...
├── frontend/              # React app hiển thị + nhập liệu
│   ├── src/
│   │   ├── App.js
│   │   └── component/
│   │       └── ScheduleGrid.js
│   └── package.json
└── README.md
```

---

## 🚀 Cài đặt & chạy

### 🔹 Backend (FastAPI)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS/Linux

pip install fastapi uvicorn pydantic

uvicorn main:app --reload --port 8000
```

### 🔹 Frontend (ReactJS)

```bash
cd frontend
npm install
npm start
```

Truy cập **http://localhost:3000**, nhập lớp/môn → `Solve` → xem lịch.  

---

## 🧩 Tính năng hiện có

- ✅ Nhập lớp môn: `id`, `giáo viên`, `nhóm`, `số sinh viên`, `số tiết (duration)`  
- ✅ Backend sử dụng thuật toán **Backtracking + kiểm tra ràng buộc**:
  - Giáo viên không trùng tiết  
  - Nhóm không trùng lịch  
  - Phòng học đủ sức chứa  
- ✅ Nếu frontend không cung cấp phòng → backend tự tạo phòng mặc định  
- ✅ Hiển thị lịch học dưới dạng **grid timeslot** (môn + phòng)  

---

## 🔧 Cách dùng

1. Ở tab **nhập dữ liệu** → điền các lớp môn → bấm **Thêm lớp**  
2. Nhấn **Solve lịch** → backend chạy backtracking  
3. Nếu hợp lệ → chuyển sang tab **Kết quả** hiển thị dạng grid/bảng  

---

## ⚠️ Hạn chế & gợi ý mở rộng

- ⚡ Khi số lớp lớn → backtracking có thể **rất chậm** → nên cân nhắc ILP hoặc **Google OR-Tools**  
- ❌ Chưa có giao diện để **xóa / chỉnh sửa lớp** sau khi thêm  
- 🚫 Chưa hỗ trợ ràng buộc phức tạp như: ưu tiên slot, khoảng nghỉ, dạy liên tục  
- 🎨 UI còn cơ bản → có thể cải thiện: drag & drop, màu phân biệt theo giáo viên/nhóm  

---

## 📌 Ghi chú Git

Nếu repo chưa có remote:  

```bash
git remote add origin <link-github-repo>
git push -u origin main
```

Nếu chưa có commit nào:  

```bash
git add .
git commit -m "Initial commit"
git push
```

---

## 📜 Giấy phép

Dự án phát hành theo giấy phép **MIT License**.  
Bạn có thể tự do sử dụng, sửa đổi và phân phối.  

---
👨‍💻 Tác giả: **Văn Hữu Kiên**
