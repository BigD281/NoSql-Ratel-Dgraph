# ĐỒ ÁN MÔN HỆ QUẢN TRỊ CSDL NoSQL: DGRAPH & CÔNG CỤ GUI RATEL

**Đề tài**: Tìm hiểu công cụ GUI **Ratel** quản trị CSDL đồ thị **Dgraph** và Xây dựng ứng dụng **"Hệ thống Quản lý Mạng lưới Quan hệ Nhân sự, Phòng ban & Dự án" (HR Graph 360)**

---

## 1. Thông tin Nhóm thực hiện

- **Đỗ Văn Minh** (Nhóm trưởng)
- **Nguyễn Phạm Duy Luân**
- **Nguyễn Tiến Nghĩa**

---

## 2. Điểm nổi bật của Đồ án

- **Cài đặt trực tiếp trên Windows Native**: Sử dụng bộ nhị phân chính thức v20.11.3 (không dùng Docker, không máy ảo).
- **Giao diện Web Demo trực quan, tinh gọn**: Quản trị dữ liệu nhân sự, dự án, phòng ban và trực quan hóa mạng lưới tương tác qua Cytoscape.js (tùy chọn hiển thị 15 / 24 / 50 nút).
- **Chu trình Dữ liệu hoàn chỉnh**: Hỗ trợ đầy đủ **Import** (tệp RDF/JSON hoặc nạp nhanh), **Export** (.rdf.gz, .json.gz), **Backup & Restore**.
- **So sánh đa công cụ GUI**: Đối sánh đa chiều giữa Ratel, Neo4j Browser/Bloom, ArangoDB Web UI và MongoDB Compass.
- **20 Câu truy vấn DQL đã kiểm chứng**: 10 câu cơ bản (Q01–Q10) và 10 câu nâng cao (A01–A10: `@recurse`, `shortest`, `@cascade`, `var`, `Bus Factor`, `Impact Analysis`...).

---

## 3. Cấu trúc Thư mục Dự án

```text
├── BaoCao_DoAn_Dgraph_Ratel_CapNhat.docx  # Báo cáo Word hoàn chỉnh (5 Chương + Phụ lục)
├── Slide_ThuyetTrinh_Dgraph_Ratel.pptx    # Slide thuyết trình (18 Slide kèm Lời thoại)
├── README.md                              # Hướng dẫn dự án
├── requirements.txt                       # Thư viện Python phụ trợ
├── .env                                   # Cấu hình cổng kết nối
│
├── dgraph-bin\                            # Bộ nhị phân Windows gốc (dgraph.exe, dgraph-ratel.exe)
├── database\                              # Schema, dữ liệu mẫu RDF/JSON & 20 truy vấn DQL
├── app\                                   # Mã nguồn ứng dụng Web HR Graph 360 (Python + Cytoscape.js)
├── scripts\                               # Các kịch bản tự động hóa (.bat / .py)
├── backups\                               # Thư mục chứa các bản Export và sao lưu
└── docs\
    └── Bo_18_CauHoi_BaoVe.md              # 18 Câu hỏi và Đáp án bảo vệ đồ án
```

---

## 4. Hướng dẫn Vận hành Nhanh

### Bước 1: Khởi động Dgraph và Ratel GUI
Mở terminal tại thư mục dự án và chạy:
```powershell
.\scripts\start_dgraph.bat
```
- **Dgraph Alpha API**: `http://localhost:8080/health`
- **Giao diện Ratel GUI**: `http://localhost:8000/?local` (kết nối tới `http://localhost:8080`)

### Bước 2: Nạp CSDL mẫu ban đầu
```powershell
python .\database\seed_data.py
```

### Bước 3: Khởi động Ứng dụng Web (HR Graph 360)
```powershell
.\scripts\run_app.bat
```
Truy cập ứng dụng tại: **`http://127.0.0.1:5000`**

### Dừng dịch vụ khi hoàn tất:
```powershell
.\scripts\stop_dgraph.bat
```

---

## 5. Các Chức năng Chính trên Ứng dụng Web (`http://127.0.0.1:5000`)

1. **Tổng quan & Sơ đồ mạng lưới**: Xem biểu đồ mạng lưới quan hệ đa chiều, điều chỉnh số lượng nút hiển thị, bấm vào nút để xem thông tin chi tiết.
2. **Phân tích Quan hệ & Dự án**:
   - Tra cứu cây quản lý phân cấp đệ quy (`@recurse`).
   - Tìm chuỗi đồng nghiệp kết nối ngắn nhất giữa 2 nhân viên (`shortest`).
   - Gợi ý nhân sự cho dự án theo kỹ năng (`@cascade` & `var`).
   - Đánh giá mức độ phụ thuộc và rủi ro nhân sự (`Bus Factor` & `Impact Analysis`).
3. **Quản lý Dữ liệu & Sao lưu**:
   - Thêm, sửa, xóa nhân viên và liên kết quan hệ (kèm thuộc tính *Facets*).
   - **Import**: Nạp file `.rdf`, `.json` hoặc dán trực tiếp chuỗi N-Quads.
   - **Export & Backup/Restore**: Xuất bản sao lưu `.gz` và nút khôi phục CSDL chuẩn.
4. **Truy vấn DQL**: Soạn thảo và thực thi trực tiếp các câu lệnh DQL kèm bộ mẫu 20 câu.
5. **Tài khoản & Phân quyền**: Đăng nhập và quản lý 3 cấp quyền: `admin` (toàn quyền), `manager` (quản lý), `employee` (chỉ xem).

---

## 6. Tổng kết Đánh giá Thang điểm (10/10)

- **Mục 1–4**: Lý thuyết, cài đặt Windows không Docker, khảo sát chi tiết Ratel, so sánh 4 GUI NoSQL và ứng dụng phù hợp.
- **Mục 5–6**: Thiết kế CSDL (127 đỉnh, 2.356 bộ ba RDF), đủ quy trình Import, Export, Backup và Restore.
- **Mục 7**: 10 truy vấn cơ bản và 10 truy vấn nâng cao có kiểm chứng kết quả thực tế.
- **Mục 8–9**: Kết nối ứng dụng qua HTTP API, demo đầy đủ 4 nhóm tính năng (User RBAC, CRUD+Backup, Nghiệp vụ đồ thị, Trực quan hóa).
- **Mục 10**: Đầy đủ Báo cáo Word, Slide PowerPoint, Source code và Bộ 18 câu hỏi bảo vệ.
