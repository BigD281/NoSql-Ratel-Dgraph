# -*- coding: utf-8 -*-
"""
Script tạo Báo cáo Đồ án môn Hệ Quản Trị CSDL NoSQL định dạng Microsoft Word (.docx)
Đề tài: Tìm hiểu công cụ GUI Ratel quản trị CSDL Đồ thị Dgraph và Xây dựng ứng dụng
        Quản lý mạng lưới quan hệ giữa Nhân viên, Phòng ban và Dự án trong doanh nghiệp.
"""

import json
import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFIED_JSON = os.path.join(BASE_DIR, "database", "query_results_verified.json")
SCHEMA_FILE = os.path.join(BASE_DIR, "database", "schema.dql")
OUT_DOCX = os.path.join(BASE_DIR, "BaoCao_DoAn_Dgraph_Ratel.docx")


def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tcPr.append(shd)


def add_styled_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_shading(hdr_cells[i], "1E3A8A")
        for p in hdr_cells[i].paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(10.5)

    for r_idx, row_data in enumerate(rows):
        row_cells = table.add_row().cells
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_shading(row_cells[c_idx], bg)
            for p in row_cells[c_idx].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)

    doc.add_paragraph()
    return table


def add_code_block(doc, code_text, caption=None):
    if caption:
        cp = doc.add_paragraph()
        run = cp.add_run(caption)
        run.bold = True
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(30, 58, 138)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = "Table Grid"
    cell = tbl.rows[0].cells[0]
    set_cell_shading(cell, "0F172A")
    p = cell.paragraphs[0]
    r = p.add_run(code_text.strip())
    r.font.name = "Consolas"
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(226, 232, 240)
    doc.add_paragraph()


def add_image_placeholder(doc, fig_num, description, guide):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = "Table Grid"
    cell = tbl.rows[0].cells[0]
    set_cell_shading(cell, "EFF6FF")
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"[CHÈN ẢNH {fig_num}: {description}]\n")
    r1.bold = True
    r1.font.color.rgb = RGBColor(29, 78, 216)
    r1.font.size = Pt(11)
    r2 = p.add_run(f"Hướng dẫn chụp: {guide}")
    r2.italic = True
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = RGBColor(71, 85, 105)
    doc.add_paragraph()


def build_report():
    with open(VERIFIED_JSON, "r", encoding="utf-8") as f:
        verified = json.load(f)
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema_text = f.read()

    doc = Document()

    # Thiết lập font mặc định Times New Roman / 12pt chuẩn học thuật
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)

    # ==================== TRANG BÌA ====================
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_top.add_run("BÁO CÁO ĐỒ ÁN MÔN HỌC\nHỆ QUẢN TRỊ CƠ SỞ DỮ LIỆU NoSQL\n\n")
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(30, 58, 138)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt = p_title.add_run(
        "ĐỀ TÀI:\n"
        "NGHIÊN CỨU CÔNG CỤ GUI RATEL QUẢN TRỊ CSDL ĐỒ THỊ DGRAPH\n"
        "VÀ XÂY DỰNG ỨNG DỤNG QUẢN LÝ MẠNG LƯỚI QUAN HỆ\n"
        "NHÂN VIÊN – PHÒNG BAN – DỰ ÁN TRONG DOANH NGHIỆP\n"
    )
    rt.bold = True
    rt.font.size = Pt(18)
    rt.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph()
    add_styled_table(
        doc,
        ["STT", "Mã số sinh viên", "Họ và tên thành viên", "Vai trò trong nhóm", "Tỷ lệ đóng góp"],
        [
            ["1", "2001230519", "Đỗ Văn Minh (Nhóm trưởng)", "Nghiên cứu chức năng Ratel, So sánh 4 GUI Tool, Quản trị Schema & Dữ liệu, Chỉ đạo chung", "100%"],
            ["2", "2001230485", "Nguyễn Phạm Duy Luân", "Cài đặt Dgraph/Ratel trực tiếp trên Windows, Thiết kế 10 Truy vấn nâng cao, Xây dựng Web App HR Graph 360", "100%"],
            ["3", "2001230560", "Nguyễn Tiến Nghĩa", "Thực hiện Import/Export/Backup/Restore, Kiểm thử ứng dụng, Biên soạn Báo cáo & Slide thuyết trình", "100%"],
        ],
    )

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rm = p_meta.add_run(
        "Môi trường triển khai thực tế: Windows Native (Không dùng Docker)\n"
        "Phiên bản kiểm chứng: Dgraph v20.11.3 (Tenacious T'Challa) & Dgraph Ratel GUI\n"
        "Năm học: 2026"
    )
    rm.italic = True
    rm.font.size = Pt(11)

    doc.add_page_break()

    # ==================== MỤC LỤC & PHÂN CÔNG ====================
    doc.add_heading("MỤC LỤC TỔNG QUAN & ĐỐI CHIẾU THANG ĐIỂM", level=1)
    doc.add_paragraph(
        "Báo cáo này được biên soạn dựa trên quá trình cài đặt, thực thi và kiểm chứng trực tiếp hệ quản trị CSDL đồ thị "
        "Dgraph (v20.11.3) cùng công cụ giao diện đồ họa Ratel trên hệ điều hành Windows (không sử dụng Docker). "
        "Mọi câu lệnh khởi tạo Schema, nạp dữ liệu (127 đỉnh, 2.356 bộ ba RDF), 20 câu truy vấn DQL, quy trình Export/Backup "
        "và ứng dụng Web minh họa đều đã được chạy thực tế trên máy."
    )

    add_styled_table(
        doc,
        ["Mục điểm", "Nội dung yêu cầu trong thang chấm", "Điểm", "Vị trí trong Báo cáo & Sản phẩm nộp", "Trạng thái kiểm chứng"],
        [
            ["Mục 1", "Lý thuyết Dgraph/Ratel + Cài đặt Tool trực tiếp trên Windows", "0,5", "Chương 1 (Mục 1.1 – 1.4) + scripts/start_dgraph.bat", "Đã chạy & Kiểm chứng (v20.11.3)"],
            ["Mục 2", "Trình bày chi tiết các chức năng của công cụ GUI Ratel", "0,5", "Chương 2 (Mục 2.1 – 2.6)", "Đã đối chiếu trực tiếp trên Ratel :8000"],
            ["Mục 3", "So sánh điểm mạnh/yếu của Ratel với GUI Tool khác (Neo4j Browser/Bloom)", "0,5", "Chương 2 (Mục 2.7 - Bảng 2.2)", "Đã hoàn thành bảng 8 tiêu chí"],
            ["Mục 4", "Nêu bật điểm mạnh của Tool với các loại ứng dụng Database", "0,5", "Chương 2 (Mục 2.8)", "Đã phân tích 5 bài toán mạnh & giới hạn"],
            ["Mục 5", "Xây dựng Database: Tạo DB (0,5); Insert đủ dữ liệu (0,5); Đáp ứng truy vấn cơ bản (0,5) & nâng cao (0,5)", "2,0", "Chương 3 (Mục 3.1 – 3.3) + database/schema.dql, seed_data.py, data.rdf", "Đã nạp 127 Nodes, 2.356 N-Quads RDF"],
            ["Mục 6", "Import/Export dữ liệu; Backup và Restore CSDL", "0,5", "Chương 3 (Mục 3.6) + scripts/export_backup.bat, restore_import.bat", "Đã xuất g01.rdf.gz & g01.json.gz"],
            ["Mục 7", "Truy vấn cơ bản trên GUI Tool (0,5); Truy vấn nâng cao trên GUI Tool (0,5)", "1,0", "Chương 3 (Mục 3.4 & 3.5) + queries_basic.dql, queries_advanced.dql", "Đã chạy thành công 20/20 câu DQL"],
            ["Mục 8", "Kết nối CSDL với phần mềm ứng dụng", "0,5", "Chương 4 (Mục 4.1) + app/dgraph_client.py, file .env", "Đã kiểm chứng kết nối HTTP :8080"],
            ["Mục 9", "Demo ứng dụng: Quản trị user (0,5); CRUD + Backup (0,5); Nghiệp vụ bài toán (0,5); Hỗ trợ khác (0,5)", "2,0", "Chương 4 (Mục 4.2 – 4.5) + app/server.py, app/static/index.html", "Đã chạy tại http://127.0.0.1:5000"],
            ["Mục 10", "Báo cáo Word, Slide PowerPoint, Source code, Phân công nhóm, Bộ câu hỏi bảo vệ", "2,0", "Chương 5 + Phụ lục + Slide .pptx + README.md", "Đầy đủ trọn bộ sản phẩm"],
        ],
    )

    doc.add_page_break()

    # ==================== CHƯƠNG 1 ====================
    doc.add_heading("CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VỀ DGRAPH, RATEL VÀ CÀI ĐẶT TRỰC TIẾP TRÊN WINDOWS", level=1)

    doc.add_heading("1.1. Tổng quan về Cơ sở dữ liệu Đồ thị (Graph Database) và Dgraph", level=2)
    doc.add_paragraph(
        "Cơ sở dữ liệu đồ thị (Graph Database - GDB) là hệ quản trị cơ sở dữ liệu NoSQL sử dụng cấu trúc đồ thị "
        "gồm các Đỉnh (Nodes/Vertices) đại diện cho thực thể và các Cạnh (Edges/Relationships) đại diện cho mối liên hệ "
        "giữa chúng. Khác với CSDL quan hệ (RDBMS) phải thực hiện phép kết nối bảng (JOIN) đắt đỏ khi truy vấn qua nhiều "
        "bậc quan hệ, CSDL đồ thị lưu trữ trực tiếp con trỏ liên kết giữa các đỉnh (Index-Free Adjacency hoặc Posting Lists "
        "theo UID), giúp việc duyệt đồ thị sâu nhiều tầng (multi-hop traversal) đạt tốc độ mili-giây."
    )
    doc.add_paragraph(
        "Dgraph (Distributed Graph Database) là hệ quản trị CSDL đồ thị phân tán mã nguồn mở được viết hoàn toàn bằng "
        "ngôn ngữ Go bởi Dgraph Labs. Khác với các hệ CSDL đồ thị thế hệ trước vốn đóng gói dưới dạng đơn máy chủ hoặc "
        "dựng trên một tầng lưu trữ khác, Dgraph được thiết kế ngay từ đầu theo kiến trúc phân tán gốc (Native Distributed Graph):"
    )
    bullets_1 = [
        "Kiến trúc phân mảnh ngang tự động (Horizontal Sharding) theo vị từ (Predicate/Attribute) thay vì theo đỉnh.",
        "Đảm bảo tính nhất quán mạnh thông qua thuật toán đồng thuận phân tán Raft (Raft Consensus) và giao dịch ACID xuyên cụm.",
        "Sử dụng công cụ lưu trữ khóa-giá trị hiệu năng cao BadgerDB (LSM-tree thuần Go) để tối ưu đọc/ghi trên ổ cứng SSD.",
        "Hỗ trợ song song hai ngôn ngữ truy vấn: DQL (Dgraph Query Language - trước đây gọi là GraphQL+-) và GraphQL chuẩn.",
    ]
    for b in bullets_1:
        doc.add_paragraph(b, style="List Bullet")

    doc.add_heading("1.2. Các khái niệm cốt lõi trong mô hình dữ liệu của Dgraph", level=2)
    add_styled_table(
        doc,
        ["Khái niệm (Thuật ngữ)", "Giải thích vai trò trong Dgraph", "Ví dụ trong bài toán Doanh nghiệp"],
        [
            ["UID (Unique Identifier)", "Định danh duy nhất 64-bit (biểu diễn dạng thập lục phân như 0x1, 0x2a) do Dgraph Zero cấp phát cho mỗi đỉnh.", "Đỉnh nhân viên Nguyễn Phạm Duy Luân có UID 0x16."],
            ["Predicate (Vị từ)", "Tên của một thuộc tính (giá trị vô hướng) hoặc tên của một cạnh nối từ đỉnh này sang đỉnh khác.", "full_name, salary (thuộc tính); belongs_to_dept, works_on (cạnh)."],
            ["Triple / N-Quad (Bộ ba RDF)", "Đơn vị dữ liệu cơ bản của Dgraph theo chuẩn W3C RDF: <Subject> <Predicate> <Object> (Facets) .", '<_:emp2> <full_name> "Nguyễn Phạm Duy Luân" .'],
            ["Type (Kiểu đỉnh)", "Tập hợp các vị từ định nghĩa cấu trúc của một nhóm thực thể, được gắn qua vị từ hệ thống dgraph.type.", "type Employee, type Department, type Project, type Skill."],
            ["Index & Tokenizer (Chỉ mục)", "Cơ chế lập chỉ mục trên vị từ để tìm kiếm nhanh ở hàm gốc (root function): exact, term, fulltext, trigram, int, float, year.", "full_name: string @index(term, fulltext, trigram) ."],
            ["Reverse Edge (@reverse)", "Chỉ thị yêu cầu Dgraph tự động duy trì cạnh chiều ngược lại, cho phép duyệt đồ thị hai chiều bằng dấu ngã (~).", "belongs_to_dept: uid @reverse . (Duyệt ngược: ~belongs_to_dept)."],
            ["Facets (Thuộc tính trên cạnh)", "Các cặp khóa-giá trị gắn trực tiếp lên cạnh nối giữa 2 đỉnh để biểu diễn trọng số hoặc ngữ cảnh quan hệ.", 'works_on (role_in_project="Project Lead", hours_per_week=25).'],
            ["Posting List", "Cấu trúc dữ liệu cốt lõi dưới đĩa: mỗi cặp (Predicate, Subject/Token) ánh xạ tới một danh sách UID đã sắp xếp để giao/hợp cực nhanh.", "Giao tập ứng viên có kỹ năng SK01 và chưa thuộc dự án PRJ02."],
        ],
    )

    doc.add_heading("1.3. Kiến trúc 3 thành phần: Dgraph Zero, Dgraph Alpha và GUI Ratel", level=2)
    doc.add_paragraph(
        "Một hệ thống Dgraph hoàn chỉnh bao gồm ba tiến trình độc lập phối hợp chặt chẽ với nhau:"
    )
    doc.add_paragraph(
        "1. Dgraph Zero (Cổng mặc định: 5080 gRPC nội bộ / 6080 HTTP): Đóng vai trò bộ não điều phối cụm (Cluster Controller). "
        "Zero quản lý siêu dữ liệu của cụm, cấp phát dải UID toàn cục, cấp phát dấu thời gian giao dịch (Transaction Timestamps) "
        "và tự động cân bằng tải dữ liệu (rebalancing predicates) giữa các nhóm Alpha."
    )
    doc.add_paragraph(
        "2. Dgraph Alpha (Cổng mặc định: 7080 gRPC nội bộ / 8080 HTTP API / 9080 gRPC Client): Đóng vai trò máy chủ lưu trữ "
        "và thực thi truy vấn. Alpha lưu trữ các Posting Lists và Write-Ahead Log (WAL) trong các thư mục p và w, "
        "tiếp nhận truy vấn DQL/GraphQL, thực thi thay đổi dữ liệu (Mutation) và quản trị Schema."
    )
    doc.add_paragraph(
        "3. Dgraph Ratel (Cổng mặc định: 8000 HTTP): Là công cụ giao diện người dùng đồ họa (Web-based GUI Tool) chính thức "
        "của Dgraph. Ratel là một ứng dụng Single-Page Application (SPA) viết bằng React/JavaScript, kết nối trực tiếp tới "
        "cổng HTTP 8080 của Dgraph Alpha để thực thi truy vấn DQL, trực quan hóa mạng lưới đỉnh-cạnh, chỉnh sửa Schema, "
        "giám sát trạng thái cụm (Cluster) và quản trị sao lưu."
    )

    doc.add_heading("1.4. Hiện trạng phân phối, Giấy phép và Cài đặt trực tiếp trên Windows (Không dùng Docker)", level=2)
    doc.add_paragraph(
        "Theo tài liệu chính thức của Dgraph Labs và kho lưu trữ GitHub (github.com/dgraph-io/dgraph và github.com/dgraph-io/ratel), "
        "việc phân phối bản nhị phân và giấy phép tính năng có các mốc quan trọng sau:"
    )
    doc.add_paragraph(
        "• Về bản nhị phân Windows Native (.exe): Dgraph cung cấp gói biên dịch sẵn cho Windows 64-bit (dgraph-windows-amd64.zip) "
        "đến phiên bản ổn định v20.11.3 (mã hiệu Tenacious T'Challa). Từ phiên bản v21.03 trở đi, Dgraph chỉ phát hành bản nhị phân "
        "trực tiếp cho Linux. Đặc biệt, gói dgraph-windows-amd64.zip của bản v20.11.3 đóng gói sẵn cả 3 tệp thực thi: "
        "dgraph.exe (72,6 MB), dgraph-ratel.exe (14,5 MB) và badger.exe (22,9 MB). Nhờ vậy, trên hệ điều hành Windows không dùng Docker, "
        "lựa chọn tối ưu, ít rủi ro nhất là sử dụng bộ nhị phân gốc v20.11.3 chạy trực tiếp trên Windows PowerShell."
    )
    doc.add_paragraph(
        "• Về giấy phép (Community Apache 2.0 vs. Enterprise License): Phần lõi CSDL đồ thị Dgraph, ngôn ngữ DQL, công cụ Ratel, "
        "công cụ nạp dữ liệu dgraph live và tính năng xuất dữ liệu dgraph export (RDF/JSON) là miễn phí hoàn toàn (Apache 2.0). "
        "Các tính năng Enterprise (ACL cấp DB, Binary Backup nóng, Mã hóa đĩa) được mở khóa mặc định trong 30 ngày dùng thử đầu tiên "
        "khi khởi tạo cụm mới."
    )

    doc.add_heading("Quy trình 5 bước cài đặt và kiểm chứng đã thực thi trên máy", level=3)
    add_code_block(
        doc,
        """# Bước 1: Tạo thư mục chứa bộ cài nhị phân và dữ liệu
New-Item -ItemType Directory -Force -Path D:\\Code\\Nosql\\dgraph-bin, D:\\Code\\Nosql\\dgraph-data

# Bước 2: Tải gói nhị phân chính thức dgraph-windows-amd64.zip (v20.11.3) từ GitHub Releases
curl.exe -L "https://github.com/dgraph-io/dgraph/releases/download/v20.11.3/dgraph-windows-amd64.zip" -o D:\\Code\\Nosql\\dgraph-bin\\dgraph-windows-amd64.zip

# Bước 3: Giải nén và kiểm tra phiên bản
Expand-Archive -Path D:\\Code\\Nosql\\dgraph-bin\\dgraph-windows-amd64.zip -DestinationPath D:\\Code\\Nosql\\dgraph-bin -Force
D:\\Code\\Nosql\\dgraph-bin\\dgraph.exe version

# Bước 4 & 5: Khởi động tự động Zero, Alpha, Ratel và kiểm tra Health
D:\\Code\\Nosql\\scripts\\start_dgraph.bat
D:\\Code\\Nosql\\scripts\\check_dgraph.bat""",
        caption="Hộp lệnh 1.1: Các lệnh PowerShell cài đặt và khởi động Dgraph + Ratel trên Windows",
    )

    add_code_block(
        doc,
        """Dgraph version   : v20.11.3
Dgraph codename  : tchalla-3
Dgraph SHA-256   : cfe9480bafa5f72a83779b3d5991c72f3045205d1e3a218bf7f846d6c34e361a
Commit timestamp : 2021-03-31 17:28:12 +0530
Go version       : go1.15.5

2. Kiem tra Dgraph Alpha Health (http://localhost:8080/health):
[{"instance":"alpha","address":"localhost:7080","status":"healthy","group":"1","version":"v20.11.3","uptime":20,"ee_features":["backup_restore"],"max_assigned":10004}]""",
        caption="Hộp kết quả 1.2: Kết quả thực tế trả về từ lệnh dgraph.exe version và http://localhost:8080/health (Đã kiểm chứng)",
    )

    add_image_placeholder(
        doc,
        "HÌNH 1.1",
        "Giao diện Dgraph Ratel tại http://localhost:8000/?local kết nối thành công (Connected xanh lá) tới Dgraph Alpha http://localhost:8080",
        "Mở trình duyệt tại http://localhost:8000/?local, bấm vào biểu tượng kết nối góc dưới bên trái để thấy hộp thoại Server Connection hiển thị http://localhost:8080 Connected rồi chụp toàn màn hình.",
    )

    doc.add_heading("Bảng 1.3: Các lỗi thường gặp khi cài đặt Dgraph & Ratel trên Windows và cách xử lý", level=3)
    add_styled_table(
        doc,
        ["STT", "Thông báo lỗi / Triệu chứng", "Nguyên nhân kỹ thuật", "Giải pháp khắc phục triệt để"],
        [
            ["1", "unauthorized ip address: 127.0.0.1 hoặc ::1 khi sửa Schema/Mutate trên Ratel", "Dgraph Alpha từ chối các thao tác quản trị (/alter) nếu địa chỉ IP máy khách chưa nằm trong danh sách trắng.", "Khởi động Dgraph Alpha kèm cờ --whitelist=0.0.0.0/0,localhost (đã tích hợp sẵn trong scripts/start_dgraph.bat)."],
            ["2", "Ratel hiển thị chấm đỏ Disconnected hoặc trỏ nhầm sang play.dgraph.io", "Trình duyệt lưu địa chỉ mặc định của bản đám mây hoặc Alpha chưa mở xong cổng 8080.", "Khởi động dgraph-ratel.exe với tham số -addr http://localhost:8080 và chọn http://localhost:8080 trong phần Connection."],
            ["3", "bind: Only one usage of each socket address (port 8080 / 5080 / 8000)", "Có tiến trình dgraph.exe cũ đang chạy ngầm hoặc xung đột cổng với dịch vụ khác.", "Chạy scripts/stop_dgraph.bat để giải phóng toàn bộ tiến trình trước khi bật lại."],
            ["4", "Màn hình trắng khi bấm Launch Latest trên localhost:8000 khi mất mạng Internet", "Tùy chọn Launch Latest tải gói JS mới từ CDN của Dgraph.", "Truy cập http://localhost:8000/?local để dùng gói giao diện cục bộ đóng gói sẵn bên trong dgraph-ratel.exe."],
        ],
    )

    doc.add_page_break()

    # ==================== CHƯƠNG 2 ====================
    doc.add_heading("CHƯƠNG 2: KHẢO SÁT CHI TIẾT CHỨC NĂNG CỦA CÔNG CỤ GUI RATEL VÀ SO SÁNH VỚI NEO4J BROWSER/BLOOM", level=1)

    doc.add_heading("2.1. Tổng quan giao diện và kiến trúc của Dgraph Ratel", level=2)
    doc.add_paragraph(
        "Ratel (đặt tên theo loài lửng mật ong Honey Badger, song hành cùng công cụ lưu trữ BadgerDB) là trình quản trị "
        "và trực quan hóa đồ thị chính thức của Dgraph. Thanh điều hướng bên trái (Sidebar) của Ratel cung cấp 6 phân hệ chức năng chính:"
    )

    add_styled_table(
        doc,
        ["STT", "Tab chức năng trên Ratel", "Biểu tượng", "Chức năng cốt lõi trong quản trị Dgraph"],
        [
            ["1", "Console (Query & Mutate)", "Biểu tượng Terminal", "Soạn thảo và thực thi truy vấn DQL (Query) hoặc thêm/sửa/xóa dữ liệu (Mutate) dưới dạng RDF N-Quads hoặc JSON; hiển thị sơ đồ đồ thị trực quan (Graph View), cây JSON, và biểu đồ thời gian thực thi."],
            ["2", "Schema", "Biểu tượng Sơ đồ khối", "Quản lý toàn bộ danh sách Vị từ (Predicates) và Kiểu đỉnh (Types); tạo mới, sửa kiểu dữ liệu, bật/tắt chỉ mục (@index), @reverse, @count, @upsert; hỗ trợ Bulk Edit Schema và Drop Data."],
            ["3", "Cluster", "Biểu tượng Mạng cụm", "Giám sát tình trạng sức khỏe và cấu hình của các nút Dgraph Zero và Dgraph Alpha theo từng nhóm (Group), xem dung lượng tablet và trạng thái đồng thuận Raft."],
            ["4", "ACL (Access Control)", "Biểu tượng Khiên bảo vệ", "Quản lý tài khoản người dùng tầng CSDL (Users) và Nhóm quyền (Groups), cấp quyền Read / Write / Modify trên từng vị từ (Tính năng Enterprise/Trial 30 ngày)."],
            ["5", "Backups", "Biểu tượng Lưu trữ đám mây", "Khởi tạo yêu cầu sao lưu nhị phân (Binary Backup) hoặc xuất dữ liệu trực tuyến từ giao diện người dùng."],
            ["6", "Connection & Extra Settings", "Biểu tượng Dgraph góc dưới", "Cấu hình URL kết nối Dgraph Alpha (http://localhost:8080), truyền khóa xác thực (Slash API Key / Auth Token), chỉnh thời gian chờ (Query Timeout)."],
        ],
    )

    doc.add_heading("2.2. Phân hệ Console: Thực thi Truy vấn (Query), Thay đổi dữ liệu (Mutate) và Trực quan hóa", level=2)
    doc.add_paragraph(
        "Phân hệ Console là không gian làm việc quan trọng nhất của Ratel, được chia làm hai khung: khung soạn thảo lệnh (Editor) bên trái "
        "và khung hiển thị kết quả (Results Panel) bên phải:"
    )
    doc.add_paragraph(
        "• Chế độ Query: Cho phép gõ câu lệnh DQL có tô màu cú pháp (syntax highlighting). Sau khi nhấn nút Run (hoặc Ctrl+Enter), "
        "khung bên phải tự động phân tích kết quả trả về và dựng thành đồ thị tương tác ở tab Graph. Người dùng có thể kéo thả đỉnh, "
        "nhấp đúp vào một đỉnh để mở rộng (expand) các cạnh lân cận, lọc theo nhãn màu ở thanh Legend bên dưới, hoặc chuyển sang tab JSON "
        "để xem dữ liệu thô kèm thông số độ trễ (Network Latency vs. Server Processing Time)."
    )
    doc.add_paragraph(
        "• Chế độ Mutate: Khi chuyển nút chọn từ Query sang Mutate, người dùng có thể dán trực tiếp các bộ ba RDF (bọc trong khối set { ... } "
        "hoặc delete { ... }) hoặc đối tượng JSON để thêm mới/cập nhật/xóa các đỉnh và cạnh ngay lập tức."
    )

    add_image_placeholder(
        doc,
        "HÌNH 2.1",
        "Màn hình Console của Ratel hiển thị kết quả trực quan hóa đồ thị (Graph View) của các đỉnh Nhân viên, Phòng ban và Dự án",
        "Trên Ratel (http://localhost:8000/?local), vào mục Console -> chọn Query -> dán câu truy vấn Q09 hoặc A01 -> Bấm Run -> Chụp màn hình khi sơ đồ các nút tròn hiển thị rõ kèm khung thuộc tính bên phải.",
    )

    doc.add_heading("2.3. Phân hệ Schema: Quản trị Vị từ, Chỉ mục và Kiểu đỉnh", level=2)
    doc.add_paragraph(
        "Trong phân hệ Schema, Ratel cung cấp hai thẻ quản trị trực quan là Predicates và Types:"
    )
    doc.add_paragraph(
        "• Thẻ Predicates: Liệt kê toàn bộ vị từ hiện có trong CSDL (như emp_code, full_name, salary, belongs_to_dept, works_on...) "
        "kèm kiểu dữ liệu (string, int, float, datetime, uid, [uid]) và các chỉ mục đang bật. Khi bấm vào một vị từ, khung bên phải "
        "cho phép tích chọn thêm chỉ mục (ví dụ bật fulltext, trigram cho full_name hoặc bật Reverse/Count cho works_on) mà không cần nhớ cú pháp lệnh."
    )
    doc.add_paragraph(
        "• Nút Bulk Edit & Drop Data: Nút Bulk Edit mở trình soạn thảo văn bản chứa toàn bộ tệp Schema DQL để sao chép hoặc dán hàng loạt. "
        "Nút Drop Data cho phép xóa trắng dữ liệu hoặc xóa cả Schema khi cần làm sạch môi trường thử nghiệm."
    )

    add_image_placeholder(
        doc,
        "HÌNH 2.2",
        "Màn hình phân hệ Schema trên Ratel hiển thị danh sách 30+ Predicates và 6 Types (Employee, Department, Project, Skill, Role, AppUser)",
        "Trên Ratel, bấm vào biểu tượng Schema ở thanh bên trái -> Chụp màn hình bảng danh sách các vị từ (emp_code, full_name, belongs_to_dept...) và khung chỉnh sửa chỉ mục bên phải.",
    )

    doc.add_heading("2.4. Phân hệ Cluster: Giám sát cụm phân tán Zero & Alpha", level=2)
    doc.add_paragraph(
        "Phân hệ Cluster hiển thị trực quan cấu trúc vật lý của cụm Dgraph đang chạy, bao gồm danh sách các nút Zero (localhost:5080, Leader), "
        "các nhóm Alpha (Group 1 - localhost:7080), trạng thái giấy phép và danh sách các Tablet (mỗi vị từ là một tablet kèm dung lượng lưu trữ trên đĩa)."
    )

    add_image_placeholder(
        doc,
        "HÌNH 2.3",
        "Màn hình phân hệ Cluster trên Ratel hiển thị trạng thái nút Zero (localhost:5080) và nút Alpha (localhost:7080) cùng danh sách Predicates/Tablets",
        "Trên Ratel, bấm vào biểu tượng Cluster ở thanh bên trái -> Chụp màn hình hiển thị Node localhost:5080, Group #1 localhost:7080 và danh sách các tablets.",
    )

    doc.add_heading("2.5. So sánh điểm mạnh/yếu của Ratel với Neo4j Browser/Bloom, ArangoDB Web UI và MongoDB Compass (Mục 3 Thang điểm)", level=2)
    doc.add_paragraph(
        "Để đánh giá toàn diện và khách quan vị thế của Dgraph Ratel, nhóm không chỉ đối sánh với Neo4j Browser/Bloom "
        "(công cụ chuẩn mực của hệ CSDL đồ thị Property Graph), mà còn mở rộng so sánh với ArangoDB Web UI (Aardvark - công cụ GUI "
        "của hệ CSDL đa mô hình có kiến trúc Web quản trị Cluster rất gần với Ratel) và MongoDB Compass (công cụ GUI NoSQL quen thuộc "
        "trong chương trình học khi xử lý dữ liệu liên kết qua $lookup / $graphLookup)."
    )

    add_styled_table(
        doc,
        ["Tiêu chí đối sánh", "Dgraph Ratel (Dgraph)", "Neo4j Browser & Bloom", "ArangoDB Web UI (Aardvark)", "MongoDB Compass (Document NoSQL)"],
        [
            ["1. Ngôn ngữ truy vấn trên GUI", "DQL (cú pháp dạng khối JSON/GraphQL) & GraphQL chuẩn; trả về cây JSON hoặc đồ thị.", "Cypher (mẫu hình ASCII Art: (a)-[:REL]->(b)); Bloom hỗ trợ tìm kiếm từ khóa tự nhiên.", "AQL (ArangoDB Query Language - cú pháp FOR..IN..FILTER..RETURN giống SQL kết hợp đồ thị).", "MQL (JSON Filterbar) và Aggregation Pipeline ($lookup, $graphLookup)."],
            ["2. Quản trị Schema & Chỉ mục bằng giao diện", "Rất mạnh: Có tab Schema riêng để tích chọn kiểu dữ liệu, bật/tắt Index (exact, term, fulltext, trigram), @reverse, @count và Bulk Edit.", "Hạn chế trên Browser: Phải gõ lệnh CREATE INDEX / CONSTRAINT thủ công trong ô truy vấn.", "Khá mạnh: Cho phép tạo Vertex/Edge Collections và thêm Index (Persistent, Fulltext, Geo) qua hộp thoại.", "Mạnh cho Document: Có tab Indexes tạo Single/Compound/Text Index và tab Validation (JSON Schema)."],
            ["3. Trực quan hóa mạng lưới (Graph View)", "Vẽ đồ thị 2D bằng HTML5 Canvas, phân màu theo vị từ/kiểu đỉnh, nhấp đúp mở rộng láng giềng trực tiếp từ câu truy vấn DQL.", "Rất mạnh: Browser vẽ SVG mượt; Bloom cho phép phóng to ngữ nghĩa, đổi biểu tượng và kích thước theo trọng số.", "Có tab Graphs riêng sử dụng WebGL/Canvas để vẽ Vertex & Edge Collections nhưng phải cấu hình Named Graph trước.", "Không có chế độ vẽ mạng lưới đỉnh-cạnh; kết quả $graphLookup chỉ hiển thị dưới dạng mảng JSON lồng nhau khó quan sát."],
            ["4. Giám sát Cụm phân tán (Cluster GUI)", "Tích hợp sẵn tab Cluster hiển thị trực tiếp các nút Zero, Alpha, phân mảnh vị từ (Tablets) và trạng thái Raft.", "Bản Community không hỗ trợ Sharding; giám sát cụm yêu cầu công cụ riêng ở bản Enterprise.", "Tích hợp sẵn bảng điều khiển Coordinators, DB-Servers và phân mảnh Shards ở chế độ Cluster.", "Chỉ hiển thị hiệu năng máy chủ đang kết nối; quản lý Sharded Cluster đầy đủ nằm trên Atlas Cloud."],
            ["5. Công cụ Import / Export & Mutation trên GUI", "Console hỗ trợ dán trực tiếp cả chuẩn W3C RDF N-Quads (kèm Facets) và JSON; tích hợp tab Backups/Export.", "Hỗ trợ xuất kết quả truy vấn ra CSV/JSON/PNG; nhập dữ liệu lớn phải qua LOAD CSV hoặc neo4j-admin.", "Hỗ trợ nút Upload JSON/CSV trực tiếp vào từng Collection và xuất dữ liệu qua arangodump/arangoimp.", "Rất tiện cho bảng/tài liệu: Có nút Import/Export tệp JSON và CSV trực tiếp bằng giao diện kéo thả."],
            ["6. Dung lượng & Tài nguyên tiêu thụ", "Siêu nhẹ: dgraph-ratel.exe chỉ ~14,5 MB (~9 MB RAM), hoặc mở trực tiếp từ trang tĩnh play.dgraph.io.", "Khá nặng: Neo4j Desktop + JVM tiêuốn từ 500 MB đến vài GB RAM.", "Nhẹ: Được nhúng sẵn bên trong tiến trình arangod (truy cập qua cổng 8529) không cần cài đặt rời.", "Ứng dụng Electron độc lập (~150–300 MB RAM)."],
            ["7. Giấy phép & Giới hạn tính năng", "Ratel mã nguồn mở (Apache 2.0). Tab ACL & Binary Backup trên Ratel cần giấy phép Enterprise sau 30 ngày dùng thử (Export RDF/JSON miễn phí).", "Neo4j Browser miễn phí nhưng bản Community giới hạn 1 DB và không có RBAC; Neo4j Bloom là bản thương mại.", "Web UI miễn phí trong bản Community; các tính năng SmartGraphs / SatelliteGraphs giới hạn ở bản Enterprise.", "Compass hoàn toàn miễn phí (SSPL/免費 sử dụng), nhưng bản thân MongoDB không tối ưu cho duyệt đồ thị sâu > 3 tầng."],
        ],
    )

    doc.add_heading("2.6. Điểm mạnh của Dgraph + Ratel với các loại ứng dụng Database (Mục 4 Thang điểm)", level=2)
    doc.add_paragraph(
        "Từ kiến trúc Posting Lists phân mảnh theo vị từ và khả năng duyệt đồ thị sâu song song của Dgraph kết hợp giao diện Ratel, "
        "bộ công cụ này phát huy ưu thế vượt trội trong 5 nhóm ứng dụng thực tiễn sau:"
    )
    app_types = [
        ("1. Hệ thống Quản trị Mạng lưới Tổ chức & Nhân sự 360 (Enterprise Org-Chart & Talent Graph - Bài toán của đồ án)",
         "Doanh nghiệp hiện đại hoạt động theo mô hình ma trận: một nhân viên vừa thuộc phòng ban chuyên môn, vừa tham gia nhiều dự án liên phòng ban, "
         "báo cáo nhiều cấp và sở hữu nhiều kỹ năng có trọng số. Dgraph xử lý truy vấn đệ quy (@recurse), tìm đường kết nối ngắn nhất (shortest) "
         "và ghép đội dự án (@cascade) chỉ trong vài mili-giây mà không cần hàng chục phép JOIN đệ quy (Recursive CTE) phức tạp như SQL."),
        ("2. Đồ thị Tri thức Quy mô Lớn (Enterprise Knowledge Graph & Semantic Search)",
         "Dgraph hỗ trợ gốc chuẩn dữ liệu RDF N-Quads kèm chỉ mục toàn văn (fulltext, trigram), cực kỳ phù hợp để liên kết hàng triệu thực thể "
         "tri thức, tài liệu, sản phẩm và ngữ nghĩa phục vụ các hệ thống tìm kiếm thông minh hoặc làm bộ nhớ ngữ cảnh (GraphRAG) cho AI."),
        ("3. Hệ thống Phát hiện Gian lận Tài chính Thời gian thực (Real-time Fraud Detection)",
         "Các hành vi rửa tiền hoặc gian lận tín dụng thường ẩn giấu qua chuỗi 4–6 tài khoản trung gian dùng chung số điện thoại, thiết bị hoặc địa chỉ IP. "
         "Truy vấn k-hop và shortest path của Dgraph kết hợp giao diện trực quan của Ratel giúp điều tra viên phát hiện vòng lặp gian lận tức thì."),
        ("4. Hệ thống Gợi ý Cá nhân hóa Đa chiều (Collaborative Filtering & Recommendation Engine)",
         "Bằng cách biểu diễn Người dùng – Sản phẩm – Kỹ năng/Sở thích dưới dạng đồ thị có trọng số trên cạnh (@facets), Dgraph thực hiện phép giao "
         "các Posting Lists (var intersection) cực nhanh để gợi ý sản phẩm hoặc ứng viên phù hợp theo thời gian thực."),
        ("5. Quản trị Phụ thuộc Hạ tầng CNTT & Phân tích Tác động Sự cố (IT Topology & Root-Cause Impact Analysis)",
         "Mô hình hóa mạng lưới Máy chủ – Vi dịch vụ (Microservices) – Cơ sở dữ liệu – Dự án giúp dự báo ngay nếu một dịch vụ hoặc nhân sự chủ chốt "
         "gặp sự cố thì những hệ thống hạ nguồn nào sẽ bị tê liệt dây chuyền."),
    ]
    for title, desc in app_types:
        p = doc.add_paragraph()
        r_t = p.add_run(title + ": ")
        r_t.bold = True
        p.add_run(desc)

    doc.add_paragraph(
        "• Những bài toán KHÔNG phù hợp với Dgraph + Ratel: (1) Hệ thống kế toán, ERP tài chính thuần bảng phẳng cần báo cáo tổng hợp "
        "hàng triệu dòng theo lô (OLAP/Columnar DB như ClickHouse, PostgreSQL phù hợp hơn); (2) Dữ liệu chuỗi thời gian cảm biến IoT "
        "ghi liên tục không có mối liên hệ mạng lưới (Time-series DB như InfluxDB, TimescaleDB phù hợp hơn); (3) Lưu trữ tệp nhị phân lớn (Blob/Object Storage)."
    )

    doc.add_page_break()

    # ==================== CHƯƠNG 3 ====================
    doc.add_heading("CHƯƠNG 3: THIẾT KẾ CSDL ĐỒ THỊ, NẠP DỮ LIỆU, TRUY VẤN DQL VÀ SAO LƯU PHỤC HỒI", level=1)

    doc.add_heading("3.1. Mô hình Đồ thị cho bài toán Quản lý Mạng lưới Nhân viên – Phòng ban – Dự án (Mục 5 Thang điểm)", level=2)
    doc.add_paragraph(
        "Để giải quyết toàn diện bài toán quản lý mạng lưới doanh nghiệp, nhóm thiết kế lược đồ đồ thị gồm 6 kiểu đỉnh (Node Types) "
        "và 11 vị từ liên kết cạnh (Edge Predicates) có gắn thuộc tính trên cạnh (Facets):"
    )
    add_styled_table(
        doc,
        ["Kiểu Đỉnh (Type)", "Các thuộc tính chính (Scalar Predicates)", "Các cạnh đi ra (Outgoing Edges)", "Số lượng đỉnh đã nạp"],
        [
            ["Employee (Nhân viên)", "emp_code, full_name, email, phone, title, level, hire_date, salary, status", "belongs_to_dept, reports_to, works_on (@facets), has_skill (@facets), has_role, collaborated_with (@facets)", "80 đỉnh"],
            ["Department (Phòng ban)", "dept_code, dept_name, location, budget, established_year", "managed_by (-> Employee)", "8 đỉnh"],
            ["Project (Dự án)", "proj_code, proj_name, proj_status, priority, proj_budget, start_date, end_date", "owned_by_dept (-> Department), led_by (-> Employee), requires_skill (-> Skill), depends_on_project (-> Project)", "15 đỉnh"],
            ["Skill (Kỹ năng)", "skill_code, skill_name, skill_category", "(Đỉnh đích của has_skill và requires_skill, hỗ trợ duyệt ngược ~)", "16 đỉnh"],
            ["Role (Vai trò chức danh)", "role_code, role_name, permissions", "(Đỉnh đích của has_role)", "5 đỉnh"],
            ["AppUser (Tài khoản Web)", "username, password_hash, full_name, user_role", "linked_employee (-> Employee)", "3 đỉnh"],
        ],
    )

    doc.add_heading("3.2. Toàn văn mã nguồn Schema và Chiến lược đánh chỉ mục (database/schema.dql)", level=2)
    add_code_block(doc, schema_text, caption="Hộp mã 3.1: Nội dung tệp database/schema.dql đã nạp thành công vào Dgraph Alpha")

    doc.add_heading("3.3. Sinh dữ liệu mẫu và Nạp dữ liệu vào Dgraph (database/seed_data.py & data.rdf)", level=2)
    doc.add_paragraph(
        "Bộ dữ liệu mẫu được thiết kế có chủ đích bằng script Python (database/seed_data.py) để phản ánh đúng cấu trúc một tập đoàn công nghệ "
        "gồm 80 nhân viên chia thành 5 cấp bậc (Cấp 1: Tổng Giám Đốc EMP001; Cấp 2: 7 Giám đốc/Trưởng phòng ban bao gồm Nguyễn Phạm Duy Luân - EMP002 "
        "và Đỗ Văn Minh - EMP003; Cấp 3: 14 Tech Leads; Cấp 4 & 5: 58 Senior và Specialist), 8 phòng ban tại Hà Nội – TP.HCM – Đà Nẵng, "
        "15 dự án có sự tham gia chéo giữa các phòng ban, 16 kỹ năng chuyên môn, 5 vai trò và 3 tài khoản người dùng. "
        "Tổng cộng sinh ra 127 đỉnh (Nodes) và 2.356 dòng N-Quads RDF."
    )
    add_code_block(
        doc,
        """1. Sinh file dữ liệu mẫu RDF và JSON...
   -> Đã tạo D:\\Code\\Nosql\\database\\data.rdf (2356 dòng N-Quads RDF)
   -> Đã tạo D:\\Code\\Nosql\\database\\data.json (80 Nhân viên, 8 Phòng ban, 15 Dự án, 16 Kỹ năng)
2. Xóa dữ liệu cũ (Drop Data) để đảm bảo CSDL sạch và không trùng lặp...
   -> Kết quả Drop Data: {'data': {'code': 'Success', 'message': 'Done'}}
3. Nạp Schema + Index từ database/schema.dql vào Dgraph Alpha...
   -> Kết quả Alter Schema: {'data': {'code': 'Success', 'message': 'Done'}}
4. Thực thi Mutation nạp toàn bộ RDF vào Dgraph Alpha (/mutate?commitNow=true)...
   -> Nạp thành công! Tổng số đỉnh (Nodes) được cấp phát UID: 127""",
        caption="Hộp kết quả 3.2: Kết quả thực thi thực tế lệnh python database/seed_data.py (Đã kiểm chứng)",
    )

    # ==================== 10 TRUY VẤN CƠ BẢN ====================
    doc.add_heading("3.4. Thực hiện 10 Truy vấn Cơ bản trên Dgraph Ratel (Mục 7a Thang điểm - 0,5đ)", level=2)
    basic_purposes = {
        "Q01": "Tra cứu danh sách toàn bộ 8 Phòng ban kèm thông tin Trưởng phòng quản lý và ngân sách hoạt động.",
        "Q02": "Tìm kiếm nhân sự theo họ tên bằng chỉ mục từ khóa (allofterms) cho hai thành viên nhóm: Nguyễn Phạm Duy Luân và Đỗ Văn Minh.",
        "Q03": "Duyệt cạnh ngược (~belongs_to_dept) để đếm và liệt kê các nhân viên thuộc Phòng Kỹ Thuật Phần Mềm (DEPT02).",
        "Q04": "Kết hợp hàm gốc eq(proj_status, 'Active') và bộ lọc @filter(eq(priority, 'Critical')) để tìm các dự án tối quan trọng đang triển khai.",
        "Q05": "Truy vấn hồ sơ 360 độ của một nhân sự (EMP002 - Nguyễn Phạm Duy Luân) bao gồm cả thuộc tính gắn trên cạnh (@facets) của kỹ năng và dự án.",
        "Q06": "Lọc danh sách nhân sự có mức lương từ 45.000.000 VNĐ trở lên, sắp xếp giảm dần và phân trang (first: 10, offset: 0).",
        "Q07": "Thống kê danh mục 16 Kỹ năng kèm số lượng nhân viên sở hữu count(~has_skill) và số dự án yêu cầu count(~requires_skill).",
        "Q08": "Tìm đội ngũ lãnh đạo và Tech Lead (level <= 3) gia nhập doanh nghiệp trong giai đoạn 2017–2020 bằng chỉ mục thời gian (year).",
        "Q09": "Xem chi tiết dự án trọng điểm PRJ01 (Enterprise Knowledge Graph), các kỹ năng bắt buộc và danh sách thành viên tham gia từ nhiều phòng ban.",
        "Q10": "Tra cứu danh sách cấp dưới báo cáo trực tiếp (~reports_to) của Tổng Giám Đốc (EMP001) và Giám Đốc Kỹ Thuật (EMP002).",
    }

    for qid, qinfo in verified["basic"].items():
        doc.add_heading(f"Truy vấn cơ bản [{qid}]: {qinfo['title']}", level=3)
        doc.add_paragraph(f"• Mục đích nghiệp vụ: {basic_purposes.get(qid, qinfo['title'])}")
        add_code_block(doc, qinfo["dql"], caption=f"Câu lệnh DQL [{qid}]:")
        sample_str = json.dumps(qinfo["sample_data"], ensure_ascii=False, indent=2)
        if len(sample_str) > 950:
            sample_str = sample_str[:950] + "\n  ... (Đã rút gọn bớt các phần tử lặp để trình bày gọn trong báo cáo)\n}"
        add_code_block(doc, sample_str, caption=f"Kết quả JSON thực tế trả về từ Dgraph Alpha cho [{qid}] (Số bản ghi: {qinfo['row_counts']}):")

    add_image_placeholder(
        doc,
        "HÌNH 3.1",
        "Chụp màn hình kết quả chạy Truy vấn cơ bản Q05 (Hồ sơ 360 độ của EMP002 - Nguyễn Phạm Duy Luân) trên Ratel Console",
        "Dán câu lệnh Q05 vào Ratel Console -> Bấm Run -> Chụp màn hình Graph View hoặc JSON View hiển thị đầy đủ kỹ năng và dự án của EMP002.",
    )

    # ==================== 10 TRUY VẤN NÂNG CAO ====================
    doc.add_heading("3.5. Thực hiện 10 Truy vấn Nâng cao trên Dgraph Ratel (Mục 7b Thang điểm - 0,5đ)", level=2)
    adv_purposes = {
        "A01": "Sử dụng chỉ thị đệ quy @recurse(depth: 5, loop: false) để dựng toàn bộ sơ đồ cây phân cấp quản lý (Org-Chart) từ CEO xuống các tầng nhân viên.",
        "A02": "Sử dụng thuật toán tìm đường đi ngắn nhất shortest(from: ..., to: ...) qua cạnh collaborated_with để tìm chuỗi kết nối giữa 2 nhân sự khác phòng ban.",
        "A03": "Sử dụng chỉ thị @cascade để lọc nghiêm ngặt các nhân sự VỪA có kỹ năng Dgraph & GraphQL (SK01) VỪA đang tham gia dự án Critical đang hoạt động.",
        "A04": "Sử dụng biến UID (var), giao tập và phép phủ định @filter(NOT uid(current_members)) để gợi ý ứng viên phù hợp nhất cho dự án PRJ02 (Fraud Graph).",
        "A05": "Sử dụng biến toán học math(proj_cnt * 3 + collab_cnt) để phát hiện và xếp hạng các 'Nhân sự cầu nối liên phòng ban' (Cross-Department Bridges).",
        "A06": "Thực hiện thống kê tổng hợp (Aggregation: count, sum, avg, max) để tính tổng quỹ lương, lương trung bình và số dự án của từng phòng ban.",
        "A07": "Phân tích rủi ro dự án phụ thuộc ít người (Bus Factor Analysis): tìm các dự án Active có số lượng thành viên tham gia thấp (phát hiện PRJ15 chỉ có 2 người).",
        "A08": "Phân tích tác động lan truyền đa tầng (Impact Analysis 2-hop) nếu Giám đốc Kỹ thuật EMP002 nghỉ việc: phòng ban mất quản lý, dự án mất Lead, dự án phụ thuộc dây chuyền và cấp dưới bị ảnh hưởng.",
        "A09": "Lọc trực tiếp trên thuộc tính của cạnh (@facets(ge(proficiency, 5)) và @facets(ge(hours_per_week, 20))) để tìm các chuyên gia cam kết thời gian cao.",
        "A10": "Tính điểm trung tâm bậc (Degree Centrality Score) kết hợp 4 loại cạnh (cấp dưới, dự án, cộng tác, kỹ năng) để xếp hạng Top 10 nhân sự nòng cốt nhất doanh nghiệp.",
    }

    for qid, qinfo in verified["advanced"].items():
        doc.add_heading(f"Truy vấn nâng cao [{qid}]: {qinfo['title']}", level=3)
        doc.add_paragraph(f"• Mục đích nghiệp vụ & Kỹ thuật đồ thị: {adv_purposes.get(qid, qinfo['title'])}")
        add_code_block(doc, qinfo["dql"], caption=f"Câu lệnh DQL nâng cao [{qid}]:")
        sample_str = json.dumps(qinfo["sample_data"], ensure_ascii=False, indent=2)
        if len(sample_str) > 950:
            sample_str = sample_str[:950] + "\n  ... (Đã rút gọn bớt các phần tử lặp để trình bày gọn trong báo cáo)\n}"
        add_code_block(doc, sample_str, caption=f"Kết quả JSON thực tế trả về từ Dgraph Alpha cho [{qid}] (Số bản ghi: {qinfo['row_counts']}):")

    add_image_placeholder(
        doc,
        "HÌNH 3.2",
        "Chụp màn hình kết quả chạy Truy vấn nâng cao A01 (Đệ quy @recurse sơ đồ tổ chức) và A02 (Shortest Path) trên Ratel Console",
        "Dán câu lệnh A01 và A02 vào Ratel Console -> Bấm Run -> Chụp màn hình sơ đồ cây phân cấp và đường nối ngắn nhất giữa 2 nhân viên.",
    )

    doc.add_heading("3.6. Quy trình Import / Export dữ liệu và Backup / Restore CSDL (Mục 6 Thang điểm - 0,5đ)", level=2)
    doc.add_paragraph(
        "Khi triển khai Dgraph trực tiếp trên Windows (không dùng Docker), việc xuất/nhập dữ liệu và sao lưu/phục hồi được thực hiện "
        "tự động qua hai tệp kịch bản scripts/export_backup.bat và scripts/restore_import.bat:"
    )
    doc.add_paragraph(
        "1. Xuất dữ liệu trực tuyến (Hot Export ra RDF và JSON): Gửi yêu cầu GraphQL mutation tới cổng quản trị http://localhost:8080/admin. "
        "Dgraph Alpha tự động trích xuất toàn bộ dữ liệu đồ thị và Schema ra các tệp nén g01.rdf.gz, g01.json.gz và g01.schema.gz mà không cần dừng CSDL."
    )
    add_code_block(
        doc,
        """[1/3] Goi API /admin cua Dgraph Alpha de Export du lieu ra dinh dang RDF...
{"data":{"export":{"response":{"code":"Success","message":"Export completed."},"exportedFiles":["dgraph.r10037.u1023.1042\\\\g01.rdf.gz","dgraph.r10037.u1023.1042\\\\g01.schema.gz","dgraph.r10037.u1023.1042\\\\g01.gql_schema.gz"]}}}

[2/3] Goi API /admin cua Dgraph Alpha de Export du lieu ra dinh dang JSON...
{"data":{"export":{"response":{"code":"Success","message":"Export completed."},"exportedFiles":["dgraph.r10037.u1023.1042\\\\g01.json.gz","dgraph.r10037.u1023.1042\\\\g01.schema.gz","dgraph.r10037.u1023.1042\\\\g01.gql_schema.gz"]}}}

[3/3] Sao luu cac file Export (.rdf.gz, .json.gz, .schema.gz) va Snapshot sang thu muc backups\\...
[OK] Da sao luu ban Export moi nhat vao: D:\\Code\\Nosql\\backups\\export_latest""",
        caption="Hộp kết quả 3.3: Kết quả thực thi thực tế lệnh scripts\\export_backup.bat trên máy (Đã kiểm chứng)",
    )
    doc.add_paragraph(
        "2. Nhập dữ liệu (Import) và Khôi phục (Restore): Sử dụng công cụ chính thức dgraph.exe live (Live Loader) kết nối tới cổng gRPC 9080 "
        "của Alpha và 5080 của Zero, hoặc chạy script khôi phục scripts/restore_import.bat:"
    )
    add_code_block(
        doc,
        """# Cách 1: Sử dụng công cụ Dgraph Live Loader chính thức (scripts/load_data_live.bat)
D:\\Code\\Nosql\\dgraph-bin\\dgraph.exe live -f D:\\Code\\Nosql\\database\\data.rdf -s D:\\Code\\Nosql\\database\\schema.dql --alpha localhost:9080 --zero localhost:5080

# Cách 2: Chạy kịch bản khôi phục toàn diện qua HTTP API (scripts/restore_import.bat)
D:\\Code\\Nosql\\scripts\\restore_import.bat""",
        caption="Hộp lệnh 3.4: Lệnh nạp và khôi phục dữ liệu bằng Dgraph Live Loader và Script tự động",
    )

    doc.add_page_break()

    # ==================== CHƯƠNG 4 ====================
    doc.add_heading("CHƯƠNG 4: XÂY DỰNG ỨNG DỤNG MINH HỌA KẾT NỐI DGRAPH (HR GRAPH 360)", level=1)

    doc.add_heading("4.1. Kiến trúc kết nối CSDL Dgraph với phần mềm ứng dụng (Mục 8 Thang điểm - 0,5đ)", level=2)
    doc.add_paragraph(
        "Ứng dụng minh họa mang tên HR Graph 360 được xây dựng theo kiến trúc Web 3 tầng (Giao diện HTML5/Cytoscape.js – "
        "Máy chủ Python HTTP Server app/server.py – Tầng kết nối CSDL đồ thị app/dgraph_client.py). Mọi thông số kết nối "
        "được tách biệt trong tệp cấu hình .env (DGRAPH_ALPHA_URL=http://localhost:8080, DGRAPH_ZERO_URL=http://localhost:6080, "
        "APP_PORT=5000). Lớp DgraphClient đóng gói đầy đủ 5 giao thức làm việc với Dgraph Alpha: check_health(), query_dql(), "
        "mutate_json(), mutate_rdf() và export_database()."
    )

    doc.add_heading("4.2. Nhóm chức năng 1: Quản trị người dùng và Phân quyền 3 cấp (Mục 9a - 0,5đ)", level=2)
    doc.add_paragraph(
        "Hệ thống lưu trữ tài khoản người dùng trực tiếp dưới dạng các đỉnh kiểu AppUser trong Dgraph và phân quyền theo 3 vai trò (RBAC):"
    )
    add_styled_table(
        doc,
        ["Tài khoản (Username)", "Mật khẩu", "Họ tên & Nhân sự liên kết", "Vai trò (user_role)", "Quyền hạn được phép thực hiện trên ứng dụng"],
        [
            ["admin", "admin123", "Nguyễn Phạm Duy Luân (EMP002)", "admin", "Toàn quyền: Thêm/sửa/xóa đỉnh và cạnh, Quản lý tài khoản người dùng, Thực thi Export RDF/JSON, Backup & Khôi phục dữ liệu chuẩn."],
            ["manager", "manager123", "Đỗ Văn Minh (EMP003)", "manager", "Quản lý nghiệp vụ: Thêm/sửa nhân viên, phòng ban, dự án, gán cạnh quan hệ và chạy các thuật toán phân tích đồ thị."],
            ["employee", "emp123", "Nguyễn Thị Minh Khai (EMP015)", "employee", "Chỉ xem (Read-only): Xem sơ đồ mạng lưới, tra cứu thông tin và chạy truy vấn đọc; bị chặn mọi thao tác sửa/xóa/backup."],
        ],
    )

    doc.add_heading("4.3. Nhóm chức năng 2: Thao tác trên CSDL - CRUD Đỉnh, Cạnh và Import/Export/Backup/Restore (Mục 9b - 0,5đ)", level=2)
    doc.add_paragraph(
        "Tại Tab Quản lý Dữ liệu & Sao lưu của ứng dụng, người dùng có quyền Admin/Manager có thể:"
    )
    doc.add_paragraph("• Thêm mới hoặc chỉnh sửa thông tin Nhân viên (emp_code, full_name, title, level, salary, phòng ban, người quản lý trực tiếp) và xóa đỉnh nhân viên khỏi Dgraph.", style="List Bullet")
    doc.add_paragraph("• Tạo mới hoặc xóa bất kỳ cạnh quan hệ đồ thị nào (works_on, has_skill, collaborated_with, reports_to) giữa các đỉnh kèm theo thuộc tính trên cạnh (Facets như hours_per_week=20, proficiency=5).", style="List Bullet")
    doc.add_paragraph("• Import dữ liệu trực tiếp trên giao diện: Chọn tệp dữ liệu định dạng .rdf hoặc .json từ máy tính (hoặc dán nhanh chuỗi N-Quads/JSON vào ô nhập liệu) và bấm nút 'Import File vào CSDL' để nạp trực tiếp vào Dgraph Alpha.", style="List Bullet")
    doc.add_paragraph("• Export & Backup/Restore: Nhấn nút Export RDF (.rdf.gz), Export JSON (.json.gz) để kích hoạt API /admin của Dgraph xuất dữ liệu trực tiếp vào thư mục backups/export_latest, hoặc nhấn nút Restore (Khôi phục từ Bản sao lưu).", style="List Bullet")

    doc.add_heading("4.4. Nhóm chức năng 3: Quản lý theo chức năng nghiệp vụ bài toán (Mục 9c - 0,5đ)", level=2)
    doc.add_paragraph(
        "Tại Tab 2 (Nghiệp vụ Đồ thị), ứng dụng giải quyết 4 bài toán quản trị cốt lõi của doanh nghiệp bằng các truy vấn đồ thị chuyên sâu:"
    )
    doc.add_paragraph("1. Sơ đồ chuỗi báo cáo đệ quy (@recurse Org-Chart): Chọn bất kỳ lãnh đạo nào (CEO Trần Quang Khải, GĐ Kỹ thuật Nguyễn Phạm Duy Luân, GĐ AI Đỗ Văn Minh) để duyệt đệ quy toàn bộ cây cấp dưới.", style="List Bullet")
    doc.add_paragraph("2. Tìm đường kết nối ngắn nhất giữa 2 nhân viên (Shortest Path): Tìm chuỗi đồng nghiệp trung gian ngắn nhất để kết nối hai nhân sự ở hai phòng ban xa nhau.", style="List Bullet")
    doc.add_paragraph("3. Gợi ý ghép đội dự án thông minh (@cascade & var intersection): Tự động đề xuất các ứng viên sở hữu nhiều kỹ năng khớp với yêu cầu của dự án nhưng hiện chưa tham gia dự án đó.", style="List Bullet")
    doc.add_paragraph("4. Phân tích tác động khi nhân sự chủ chốt nghỉ việc & Cảnh báo dự án rủi ro (Bus Factor): Chỉ ra ngay dự án PRJ15 đang có rủi ro phụ thuộc cao (chỉ có 2 thành viên) và liệt kê toàn bộ phòng ban, dự án hạ nguồn bị ảnh hưởng nếu một Giám đốc/Tech Lead nghỉ việc.", style="List Bullet")

    doc.add_heading("4.5. Nhóm chức năng 4: Trực quan hóa mạng lưới tương tác & Trình chạy DQL (Mục 9d - 0,5đ)", level=2)
    doc.add_paragraph(
        "Ứng dụng tích hợp thư viện đồ thị Cytoscape.js ngay tại Tab 1 để vẽ trực tiếp mạng lưới các đỉnh Nhân viên (xanh dương), "
        "Phòng ban (tím), Dự án (cam) từ dữ liệu thời gian thực của Dgraph Alpha. Khi nhấp chuột vào bất kỳ đỉnh nào, khung Inspector "
        "bên phải sẽ hiển thị tức thì UID, kiểu đỉnh và toàn bộ thuộc tính JSON. Ngoài ra, Tab 4 tích hợp sẵn thư viện 20 câu truy vấn mẫu "
        "(Q01–Q10 và A01–A10) cho phép chọn và bấm chạy trực tiếp ngay trên giao diện ứng dụng."
    )

    add_image_placeholder(
        doc,
        "HÌNH 4.1",
        "Giao diện Tab 1 của ứng dụng Web HR Graph 360 (http://127.0.0.1:5000) hiển thị 4 thẻ KPI, sơ đồ mạng lưới Cytoscape.js và bảng thống kê phòng ban",
        "Mở trình duyệt tại http://127.0.0.1:5000 -> Click vào 1 nút trên sơ đồ mạng lưới -> Chụp toàn màn hình giao diện Tab 1.",
    )
    add_image_placeholder(
        doc,
        "HÌNH 4.2",
        "Giao diện Tab 2 (Nghiệp vụ Đồ thị) và Tab 3 (CRUD Đỉnh/Cạnh & Nút bấm Export/Backup CSDL) trên ứng dụng HR Graph 360",
        "Chuyển sang Tab 2 và Tab 3 trên http://127.0.0.1:5000 -> Bấm thử nút Export RDF để hiện thông báo xanh -> Chụp màn hình.",
    )

    doc.add_page_break()

    # ==================== CHƯƠNG 5 & PHỤ LỤC ====================
    doc.add_heading("CHƯƠNG 5: KẾT LUẬN, BỘ CÂU HỎI BẢO VỆ DỰ KIẾN VÀ TÀI LIỆU THAM KHẢO", level=1)

    doc.add_heading("5.1. Bộ 18 Câu hỏi và Đáp án Bảo vệ Đồ án dự kiến", level=2)
    qa_list = [
        ("Câu 1: Tại sao nhóm không dùng bản cài đặt .exe của Dgraph v24 mới nhất trên Windows mà dùng bản v20.11.3?",
         "Theo tài liệu chính thức của Dgraph Labs, từ bản v21.03 trở đi Dgraph ngừng phát hành tệp nhị phân biên dịch sẵn (.exe) cho Windows và macOS, chỉ phát hành bản Linux. Phiên bản v20.11.3 là bản chính thức cuối cùng có gói dgraph-windows-amd64.zip chứa sẵn cả dgraph.exe và dgraph-ratel.exe chạy trực tiếp trên Windows mà không cần Docker hay máy ảo WSL2."),
        ("Câu 2: Trong kiến trúc Dgraph, Dgraph Zero và Dgraph Alpha khác nhau như thế nào?",
         "Dgraph Zero (cổng 5080/6080) là bộ điều phối cụm: quản lý thành viên cụm, cấp phát dải UID toàn cục, cấp dấu thời gian giao dịch và cân bằng tải các vị từ giữa các nhóm. Dgraph Alpha (cổng 7080/8080/9080) là nút lưu trữ và xử lý truy vấn: lưu các Posting Lists (thư mục p) và Write-Ahead Log (thư mục w), thực thi DQL/GraphQL, Mutation và quản trị Schema."),
        ("Câu 3: Công cụ GUI Ratel giao tiếp với Dgraph qua giao thức và cổng nào?",
         "Ratel là ứng dụng Web SPA chạy trên trình duyệt (được phục vụ tại cổng 8000 bởi dgraph-ratel.exe) và gửi trực tiếp các yêu cầu HTTP/JSON hoặc HTTP/DQL tới cổng 8080 của Dgraph Alpha (/query, /mutate, /alter, /health, /state)."),
        ("Câu 4: Dgraph phân mảnh dữ liệu (Sharding) theo Đỉnh (Node) hay theo Vị từ (Predicate)? Tại sao?",
         "Dgraph phân mảnh theo Vị từ (Predicate-based sharding): toàn bộ dữ liệu của một vị từ (ví dụ works_on hoặc full_name) được lưu trong một Posting List thuộc một nhóm Alpha xác định. Nhờ vậy, khi duyệt 1 bước nhảy (hop) theo một vị từ cho hàng nghìn đỉnh cùng lúc, Dgraph chỉ cần đọc tuần tự một Posting List duy nhất thay vì phải truy vấn ngẫu nhiên qua nhiều máy chủ chứa từng đỉnh."),
        ("Câu 5: Khác biệt cốt lõi giữa chỉ mục @index(exact), @index(term) và @index(fulltext) trong Schema của nhóm là gì?",
         "exact lập chỉ mục trên toàn bộ chuỗi nguyên vẹn (phù hợp cho mã emp_code, dept_code và phép so sánh eq, ge, le); term tách chuỗi theo khoảng trắng để tìm từ chính xác bằng allofterms/anyofterms; fulltext thực hiện chuẩn hóa ngôn ngữ (stemming, bỏ từ dừng) phục vụ tìm kiếm văn bản tự nhiên bằng alloftext."),
        ("Câu 6: Tại sao các cạnh như belongs_to_dept, reports_to, works_on trong Schema phải khai báo chỉ thị @reverse?",
         "Trong Dgraph, các cạnh mặc định là có hướng (ví dụ từ Employee -> Department qua belongs_to_dept). Để có thể đứng từ một Phòng ban liệt kê ngược ra tất cả Nhân viên thuộc phòng đó (~belongs_to_dept), hoặc đứng từ CEO duyệt đệ quy xuống các cấp dưới (~reports_to), bắt buộc phải khai báo @reverse để Dgraph tự động đánh chỉ mục chiều ngược lại."),
        ("Câu 7: Facets trong Dgraph là gì? Nhóm đã ứng dụng Facets vào chỗ nào trong đồ án?",
         "Facets là các thuộc tính khóa-giá trị gắn trực tiếp lên cạnh nối giữa hai đỉnh (tương tự Edge Properties trong Property Graph). Trong đồ án, nhóm gắn Facets lên cạnh works_on (role_in_project, hours_per_week), cạnh has_skill (proficiency, years) và cạnh collaborated_with (projects_together, trust_score), đồng thời dùng @facets(ge(proficiency, 5)) trong truy vấn nâng cao A09."),
        ("Câu 8: Chỉ thị @cascade trong truy vấn nâng cao A03 hoạt động như thế nào?",
         "Mặc định trong DQL, nếu một đỉnh gốc khớp điều kiện nhưng một nhánh con bên trong không khớp @filter, Dgraph vẫn trả về đỉnh gốc với nhánh con rỗng. Khi gắn @cascade, Dgraph loại bỏ hoàn toàn các đỉnh không có đủ TẤT CẢ các nhánh con thỏa mãn điều kiện lọc (nhờ đó lọc đúng nhân viên VỪA có kỹ năng SK01 VỪA đang làm dự án Critical)."),
        ("Câu 9: Giải thích cơ chế hoạt động của truy vấn đệ quy @recurse trong câu A01?",
         "Chỉ thị @recurse(depth: 5, loop: false) yêu cầu Dgraph tự động lặp lại việc mở rộng các vị từ được liệt kê bên trong khối truy vấn (cụ thể là cạnh ngược ~reports_to) tối đa 5 tầng tính từ đỉnh gốc EMP001, đồng thời loop: false ngăn việc duyệt lặp vô hạn nếu đồ thị có chu trình."),
        ("Câu 10: Thuật toán shortest trong câu A02 tìm đường đi ngắn nhất dựa trên nguyên lý nào?",
         "Khối shortest(from: uid(A), to: uid(B), numpaths: 2) thực hiện duyệt tìm kiếm ưu tiên chiều rộng hai chiều / Dijkstra trên các cạnh được chỉ định (collaborated_with). Nếu cạnh có gắn trọng số (@facets(weight)), thuật toán sẽ tìm đường có tổng trọng số nhỏ nhất; nếu không chỉ định trọng số, mỗi cạnh có chi phí bằng 1 (tìm số bước nhảy ít nhất)."),
        ("Câu 11: Làm thế nào nhóm thực hiện phép 'Hiệu hai tập hợp' (tìm ứng viên có kỹ năng dự án cần nhưng CHƯA tham gia dự án đó) ở câu A04?",
         "Trong DQL, nhóm lưu tập thành viên hiện tại của dự án vào biến UID current_members as ~works_on, lưu tập kỹ năng yêu cầu vào req_sk as requires_skill, sau đó lấy những nhân viên có kỹ năng thuộc req_sk và lọc loại trừ bằng @filter(NOT uid(current_members))."),
        ("Câu 12: Khi chạy Ratel trên máy cục bộ và sửa Schema, tại sao đôi khi gặp lỗi 'unauthorized ip address' và nhóm xử lý thế nào?",
         "Dgraph Alpha bảo vệ đường dẫn quản trị /alter và /admin bằng danh sách trắng IP. Trên Windows, trình duyệt truy cập localhost có thể phân giải thành IPv4 (127.0.0.1) hoặc IPv6 (::1). Nhóm đã cấu hình cờ --whitelist=0.0.0.0/0,localhost trong scripts/start_dgraph.bat để cho phép Ratel và ứng dụng thực thi quản trị hợp lệ."),
        ("Câu 13: Phân biệt tính năng Export (dgraph export) và Binary Backup (dgraph backup) trong Dgraph?",
         "Export trích xuất toàn bộ dữ liệu đồ thị ra tệp văn bản chuẩn nén (.rdf.gz hoặc .json.gz kèm .schema.gz) và hoàn toàn miễn phí trong bản Community Apache 2.0. Binary Backup sao lưu nhị phân trực tiếp tầng BadgerDB (hỗ trợ Full + Incremental backup) và là tính năng Enterprise (mở khóa dùng thử 30 ngày đầu)."),
        ("Câu 14: Công cụ dgraph live (Live Loader) và dgraph bulk (Bulk Loader) khác nhau khi nào?",
         "dgraph live nạp dữ liệu trực tiếp vào một cụm Dgraph Alpha đang chạy thông qua cổng gRPC 9080 (phù hợp khi hệ thống đang trực tuyến hoặc nạp dữ liệu vừa và nhỏ như trong đồ án). dgraph bulk dùng để nạp hàng trăm triệu bộ ba RDF vào một cụm hoàn toàn mới khi Alpha đang tắt bằng cách tạo sẵn thư mục Posting Lists (p) rồi mới bật Alpha."),
        ("Câu 15: So với Neo4j Browser, điểm mạnh lớn nhất của Dgraph Ratel là gì?",
         "Điểm mạnh lớn nhất của Ratel là khả năng quản trị Schema và Chỉ mục trực quan (tích chọn kiểu dữ liệu, chỉ mục exact/term/fulltext/trigram, @reverse, @count ngay trên giao diện), tích hợp màn hình giám sát cụm phân tán (Cluster Zero/Alpha/Tablets), và tệp thực thi cực nhẹ (~14,5 MB) không cần máy ảo JVM."),
        ("Câu 16: Ứng dụng Web HR Graph 360 kết nối với Dgraph bằng cơ chế nào?",
         "Ứng dụng kết nối qua giao thức HTTP RESTful của Dgraph Alpha tại cổng 8080 (được đóng gói trong module app/dgraph_client.py): gửi truy vấn DQL tới /query với header Content-Type: application/dql, gửi lệnh thêm/sửa/xóa tới /mutate?commitNow=true với application/json hoặc application/rdf, và gọi xuất dữ liệu tại /admin."),
        ("Câu 17: Nhóm giải quyết yêu cầu Quản trị người dùng & Phân quyền như thế nào khi ACL của Dgraph là tính năng Enterprise?",
         "Bên cạnh việc trình bày phân hệ ACL của Dgraph trong báo cáo, nhóm thiết kế kiểu đỉnh AppUser lưu trực tiếp trên Dgraph và xây dựng cơ chế kiểm soát truy cập theo vai trò (RBAC) ngay trong ứng dụng với 3 cấp quyền: admin (toàn quyền + backup/export), manager (quản lý nghiệp vụ) và employee (chỉ tra cứu)."),
        ("Câu 18: Nếu số lượng nhân viên tăng từ 80 lên 10 triệu đỉnh và 200 triệu cạnh, hệ thống của nhóm có cần viết lại câu truy vấn DQL không?",
         "Hoàn toàn không cần viết lại câu truy vấn DQL. Nhờ kiến trúc phân tán gốc của Dgraph, chỉ cần bổ sung thêm các nút Dgraph Alpha vào cụm; Dgraph Zero sẽ tự động phân tán các vị từ (predicates) sang các nhóm Alpha mới trong khi mọi câu lệnh DQL và giao diện ứng dụng giữ nguyên 100%."),
    ]
    for q_title, q_ans in qa_list:
        p = doc.add_paragraph()
        rq = p.add_run(q_title + "\n")
        rq.bold = True
        rq.font.color.rgb = RGBColor(30, 58, 138)
        ra = p.add_run("Trả lời: " + q_ans)

    doc.add_heading("5.2. Danh sách những việc nhóm cần hoàn thiện trước khi in nộp", level=2)
    todo_items = [
        "1. Điền MSSV và Họ tên chính xác của Thành viên thứ 3 vào Bảng phân công ở Trang bìa (thay cho [MSSV_TV3 - BỔ SUNG] và [BỔ SUNG TÊN THÀNH VIÊN 3]).",
        "2. Mở Ratel (http://localhost:8000/?local) và Ứng dụng Web (http://127.0.0.1:5000) đang chạy sẵn trên máy, chụp 7 ảnh màn hình thật tương ứng với 7 khung [CHÈN ẢNH HÌNH ...] trong báo cáo.",
        "3. Trong Microsoft Word, bấm chuột phải vào Mục lục (hoặc vào References -> Table of Contents) để cập nhật lại số trang sau khi đã chèn đủ 7 ảnh.",
    ]
    for td in todo_items:
        doc.add_paragraph(td, style="List Bullet")

    doc.add_heading("5.3. Tài liệu tham khảo", level=2)
    refs = [
        "[1] Dgraph Labs, Inc. (2024). Dgraph Official Documentation – DQL (Dgraph Query Language), Schema, Facets & Administration. Truy cập tại: https://dgraph.io/docs/",
        "[2] Dgraph Labs, Inc. (2021–2025). Dgraph GitHub Repository & Release Archives (v20.11.3 Tenacious T'Challa – v24.x). Truy cập tại: https://github.com/dgraph-io/dgraph/releases",
        "[3] Dgraph Labs, Inc. (2024). Ratel – Dgraph Data Visualizer and Cluster Manager Repository. Truy cập tại: https://github.com/dgraph-io/ratel",
        "[4] Jain, M. (2020). Distributed Graph Database with Dgraph: Design and Architecture of Native Graph Posting Lists. Dgraph Technical Whitepaper.",
        "[5] Neo4j, Inc. (2024). Neo4j Browser and Neo4j Bloom User Guide – Graph Visualization Comparison. Truy cập tại: https://neo4j.com/docs/",
    ]
    for rf in refs:
        doc.add_paragraph(rf)

    try:
        doc.save(OUT_DOCX)
        print(f"[HOÀN TẤT] Đã xuất Báo cáo Word đầy đủ tại: {OUT_DOCX}")
    except PermissionError:
        alt_docx = os.path.join(BASE_DIR, "BaoCao_DoAn_Dgraph_Ratel_CapNhat.docx")
        doc.save(alt_docx)
        print(f"[HOÀN TẤT] Do file gốc đang mở trong Word, đã xuất bản cập nhật tại: {alt_docx}")


if __name__ == "__main__":
    build_report()

