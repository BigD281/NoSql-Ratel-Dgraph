# -*- coding: utf-8 -*-
"""
Script tạo Slide thuyết trình PowerPoint (.pptx) 18 Slide kèm Lời thoại (Speaker Notes)
Đề tài: Quản trị CSDL Đồ thị Dgraph bằng công cụ GUI Ratel & Ứng dụng HR Graph 360.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PPTX = os.path.join(BASE_DIR, "Slide_ThuyetTrinh_Dgraph_Ratel.pptx")

NAVY = RGBColor(15, 23, 42)
BLUE = RGBColor(29, 78, 216)
LIGHT_BG = RGBColor(248, 250, 252)
WHITE = RGBColor(255, 255, 255)
MUTED = RGBColor(71, 85, 105)
ACCENT = RGBColor(217, 119, 6)
GREEN = RGBColor(21, 128, 61)


def add_header(slide, title_text, subtitle_text, slide_no):
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    banner.fill.solid()
    banner.fill.fore_color.rgb = NAVY
    banner.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.12), Inches(11.5), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    r1.text = title_text
    r1.font.size = Pt(22)
    r1.font.bold = True
    r1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = subtitle_text
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(148, 163, 184)

    badge = slide.shapes.add_textbox(Inches(12.0), Inches(0.25), Inches(1.0), Inches(0.5))
    p_b = badge.text_frame.paragraphs[0]
    p_b.alignment = PP_ALIGN.RIGHT
    rb = p_b.add_run()
    rb.text = f"{slide_no}/18"
    rb.font.size = Pt(13)
    rb.font.bold = True
    rb.font.color.rgb = RGBColor(96, 165, 250)


def add_card(slide, left, top, width, height, heading, bullets, border_color=BLUE):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(Inches(left + 0.18), Inches(top + 0.14), Inches(width - 0.36), Inches(height - 0.28))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    r0 = p0.add_run()
    r0.text = heading
    r0.font.size = Pt(15)
    r0.font.bold = True
    r0.font.color.rgb = border_color

    for b in bullets:
        p = tf.add_paragraph()
        p.space_before = Pt(6)
        r = p.add_run()
        r.text = "• " + b
        r.font.size = Pt(13)
        r.font.color.rgb = NAVY


def add_code_card(slide, left, top, width, height, title, code_str):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = NAVY
    card.line.color.rgb = BLUE
    card.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(Inches(left + 0.18), Inches(top + 0.12), Inches(width - 0.36), Inches(height - 0.24))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    r0 = p0.add_run()
    r0.text = title
    r0.font.size = Pt(13)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(96, 165, 250)

    p1 = tf.add_paragraph()
    p1.space_before = Pt(6)
    r1 = p1.add_run()
    r1.text = code_str.strip()
    r1.font.name = "Consolas"
    r1.font.size = Pt(11.5)
    r1.font.color.rgb = RGBColor(226, 232, 240)


def set_notes(slide, speaker_notes):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = speaker_notes


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    slides_data = [
        # Slide 1
        {
            "title": "ĐỒ ÁN HỆ QUẢN TRỊ CSDL NoSQL: DGRAPH & CÔNG CỤ GUI RATEL",
            "sub": "Đề tài: Quản lý mạng lưới quan hệ giữa Nhân viên, Phòng ban và Dự án trong doanh nghiệp",
            "left_title": "Thông tin Nhóm thực hiện (3 Thành viên)",
            "left_bullets": [
                "1. 2001230519 — Đỗ Văn Minh (Nhóm trưởng)",
                "2. 2001230485 — Nguyễn Phạm Duy Luân",
                "3. 2001230560 — Nguyễn Tiến Nghĩa",
                "Môi trường triển khai: Windows Native v20.11.3 (Không dùng Docker)",
            ],
            "right_title": "Cấu trúc bài thuyết trình (Đáp ứng 10/10 mục điểm)",
            "right_bullets": [
                "Phần 1: Lý thuyết Dgraph & Cài đặt trực tiếp trên Windows",
                "Phần 2: Giải phẫu chức năng Ratel & So sánh với Neo4j Browser",
                "Phần 3: Thiết kế Schema, Dữ liệu (127 đỉnh) & 20 Truy vấn DQL",
                "Phần 4: Import/Export/Backup & Demo Ứng dụng Web HR Graph 360",
            ],
            "notes": "Lời thoại Slide 1: Xin chào thầy/cô và các bạn. Hôm nay nhóm chúng em gồm Nguyễn Phạm Duy Luân, Đỗ Văn Minh và thành viên thứ 3 xin trình bày đồ án tìm hiểu công cụ GUI Ratel quản trị CSDL đồ thị Dgraph và ứng dụng quản lý mạng lưới Nhân viên – Phòng ban – Dự án.",
        },
        # Slide 2
        {
            "title": "1. TỔNG QUAN CSDL ĐỒ THỊ DGRAPH & KIẾN TRÚC PHÂN TÁN",
            "sub": "Mục 1 Thang điểm: Cơ sở lý thuyết về Dgraph (Distributed Graph Database)",
            "left_title": "Đặc trưng cốt lõi của Dgraph",
            "left_bullets": [
                "CSDL đồ thị phân tán gốc (Native Distributed Graph) viết bằng Go.",
                "Phân mảnh ngang tự động theo Vị từ (Predicate-based Sharding).",
                "Lưu trữ dưới dạng Posting Lists trên nền BadgerDB (LSM-Tree).",
                "Đảm bảo giao dịch ACID phân tán và đồng thuận Raft.",
                "Hỗ trợ ngôn ngữ truy vấn DQL (GraphQL+-) và GraphQL chuẩn.",
            ],
            "right_title": "Kiến trúc 3 thành phần chạy trực tiếp trên Windows",
            "right_bullets": [
                "1. Dgraph Zero (:5080 / :6080): Điều phối cụm, cấp phát UID & Timestamp.",
                "2. Dgraph Alpha (:7080 / :8080 / :9080): Lưu trữ Posting Lists (p, w), xử lý truy vấn DQL, Mutation, Schema & Export.",
                "3. Dgraph Ratel (:8000): Giao diện GUI trực quan hóa đồ thị, quản trị Schema và giám sát cụm.",
            ],
            "notes": "Lời thoại Slide 2: Khác với các hệ CSDL đồ thị đơn máy chủ, Dgraph được thiết kế phân tán ngay từ đầu. Hệ thống gồm 3 tiến trình: Zero điều phối cụm, Alpha lưu trữ dữ liệu và xử lý truy vấn tại cổng 8080, và Ratel là giao diện GUI chạy ở cổng 8000.",
        },
        # Slide 3
        {
            "title": "2. CÀI ĐẶT DGRAPH & RATEL TRỰC TIẾP TRÊN WINDOWS (KHÔNG DOCKER)",
            "sub": "Mục 1 Thang điểm: Lựa chọn phiên bản nhị phân gốc Windows & Kiểm chứng thực tế",
            "left_title": "Tại sao chọn bản Windows Native v20.11.3?",
            "left_bullets": [
                "Từ v21.03+, Dgraph ngừng phát hành file .exe cho Windows.",
                "Gói chính thức dgraph-windows-amd64.zip (v20.11.3) đóng gói sẵn cả dgraph.exe, dgraph-ratel.exe và badger.exe.",
                "Chạy trực tiếp trên Windows PowerShell không cần Docker hay WSL2.",
                "Tự động hóa hoàn toàn bằng start_dgraph.bat & stop_dgraph.bat.",
            ],
            "code_title": "Kết quả kiểm chứng thực tế trên máy (scripts/check_dgraph.bat)",
            "code": """Dgraph version   : v20.11.3 (tchalla-3)
dgraph.exe       : Running (Zero :5080/:6080, Alpha :8080/:9080)
dgraph-ratel.exe : Running (GUI Port :8000)

GET http://localhost:8080/health ->
[{"instance":"alpha","address":"localhost:7080",
  "status":"healthy","version":"v20.11.3"}]""",
            "notes": "Lời thoại Slide 3: Để cài đặt trực tiếp trên Windows không dùng Docker, nhóm sử dụng gói nhị phân chính thức v20.11.3 từ GitHub Releases chứa sẵn dgraph.exe và dgraph-ratel.exe. Nhóm đã viết script start_dgraph.bat kèm cờ --whitelist=0.0.0.0/0,localhost để khởi động chỉ bằng 1 cú nhấp chuột.",
        },
        # Slide 4
        {
            "title": "3. GIẢI PHẪU CHI TIẾT CÁC CHỨC NĂNG CỦA CÔNG CỤ GUI RATEL",
            "sub": "Mục 2 Thang điểm: 6 Phân hệ quản trị đồ thị trực quan trên Ratel (:8000)",
            "left_title": "Nhóm chức năng Truy vấn & Lược đồ",
            "left_bullets": [
                "1. Console (Query): Soạn thảo DQL, vẽ đồ thị tương tác (Graph View), xem JSON & độ trễ thực thi.",
                "2. Console (Mutate): Thêm/sửa/xóa đỉnh & cạnh trực tiếp bằng RDF N-Quads hoặc JSON.",
                "3. Schema Management: Tạo/sửa Predicates & Types, tích chọn Index (exact, term, fulltext, trigram), @reverse, @count, Bulk Edit.",
            ],
            "right_title": "Nhóm chức năng Quản trị Cụm & Hệ thống",
            "right_bullets": [
                "4. Cluster Management: Giám sát sức khỏe nút Zero, Alpha, trạng thái Raft và dung lượng từng vị từ (Tablets).",
                "5. ACL (Access Control): Quản trị người dùng và phân quyền Read/Write/Modify trên vị từ (Trial 30 ngày / Enterprise).",
                "6. Backups & Extra Settings: Cấu hình Server URL, Auth Token, Timeout và kích hoạt sao lưu.",
            ],
            "notes": "Lời thoại Slide 4: Giao diện Ratel gồm 6 phân hệ ở thanh bên trái. Quan trọng nhất là Console (chia làm chế độ Query và Mutate), Schema (cho phép tích chọn chỉ mục trực quan bằng chuột) và Cluster (giám sát các nút Zero, Alpha và các phân mảnh vị từ).",
        },
        # Slide 5
        {
            "title": "4. SO SÁNH RATEL VỚI NEO4J BROWSER, ARANGODB UI & COMPASS",
            "sub": "Mục 3 Thang điểm: Đối sánh đa chiều Ratel với 3 công cụ GUI NoSQL/Đồ thị phổ biến",
            "left_title": "Điểm mạnh của Dgraph Ratel so với đối thủ",
            "left_bullets": [
                "So với Neo4j Browser: Ratel có màn hình Schema bật/tắt Index, @reverse, @count bằng chuột (Neo4j Browser phải gõ lệnh thủ công) và siêu nhẹ (~14,5 MB, không cần JVM).",
                "So với ArangoDB Web UI (Aardvark): Ratel vẽ đồ thị trực tiếp từ kết quả DQL mà không bắt buộc định nghĩa Named Graph phức tạp trước.",
                "So với MongoDB Compass: Ratel trực quan hóa mạng lưới đa tầng, trong khi Compass chỉ hiện kết quả $graphLookup dạng cây JSON lồng nhau.",
            ],
            "right_title": "Điểm hạn chế của Ratel so với các GUI khác",
            "right_bullets": [
                "So với Neo4j Bloom: Ratel ít tùy biến thẩm mỹ (biểu tượng, kích thước đỉnh theo trọng số) và chưa hỗ trợ tìm kiếm No-code bằng ngôn ngữ tự nhiên.",
                "So với ArangoDB UI & MongoDB Compass: Ratel chưa có trình Import file CSV theo dạng bảng kéo-thả mà nhận dữ liệu chuẩn RDF N-Quads hoặc JSON.",
                "Tab ACL & Binary Backup trên Ratel cần giấy phép Enterprise sau 30 ngày dùng thử (tuy nhiên Export RDF/JSON vẫn miễn phí).",
            ],
            "notes": "Lời thoại Slide 5: Nhóm mở rộng so sánh Ratel với cả 3 công cụ: Neo4j Browser/Bloom, ArangoDB Web UI và MongoDB Compass. Ratel vượt trội ở quản trị Schema bằng chuột, giám sát cụm phân tán và dung lượng cực nhẹ, trong khi Neo4j Bloom mạnh hơn về thẩm mỹ trực quan và Compass tiện hơn khi nhập xuất CSV dạng bảng.",
        },
        # Slide 6
        {
            "title": "5. ĐIỂM MẠNH CỦA DGRAPH + RATEL VỚI CÁC ỨNG DỤNG DATABASE",
            "sub": "Mục 4 Thang điểm: Khi nào nên dùng và không nên dùng Dgraph + Ratel?",
            "left_title": "5 Bài toán Dgraph + Ratel phát huy tối đa sức mạnh",
            "left_bullets": [
                "1. Quản trị Mạng lưới Tổ chức & Nhân sự Đa chiều (Bài toán Đồ án): Duyệt cây báo cáo đệ quy, tìm cầu nối liên phòng ban.",
                "2. Đồ thị Tri thức (Enterprise Knowledge Graph & GraphRAG AI).",
                "3. Phát hiện Gian lận Tài chính Thời gian thực (Fraud Ring k-hop).",
                "4. Hệ thống Gợi ý Cá nhân hóa (Collaborative Filtering).",
                "5. Phân tích Phụ thuộc Hạ tầng CNTT & Tác động Sự cố.",
            ],
            "right_title": "Các bài toán KHÔNG phù hợp với Dgraph",
            "right_bullets": [
                "1. Hệ thống kế toán, tài chính thuần bảng phẳng ít quan hệ bắc cầu (RDBMS truyền thống như PostgreSQL phù hợp hơn).",
                "2. Báo cáo kho dữ liệu phân tích lô hàng trăm triệu dòng tuần tự (Columnar OLAP như ClickHouse phù hợp hơn).",
                "3. Dữ liệu chuỗi thời gian cảm biến IoT thuần túy (InfluxDB/TimescaleDB) hoặc lưu trữ file nhị phân lớn.",
            ],
            "notes": "Lời thoại Slide 6: Nhờ cấu trúc Posting Lists và duyệt đồ thị song song, Dgraph + Ratel cực mạnh cho các bài toán có mối liên hệ chằng chịt nhiều tầng như Mạng lưới nhân sự doanh nghiệp, Đồ thị tri thức, Phát hiện gian lận và Hệ thống gợi ý.",
        },
        # Slide 7
        {
            "title": "6. THIẾT KẾ CSDL ĐỒ THỊ CHO BÀI TOÁN DOANH NGHIỆP",
            "sub": "Mục 5 Thang điểm: Mô hình 6 Kiểu Đỉnh (Types) và 11 Cạnh Quan Hệ (Edges + Facets)",
            "left_title": "6 Kiểu Đỉnh (Node Types) trong database/schema.dql",
            "left_bullets": [
                "1. Employee (80 đỉnh): emp_code, full_name, title, level, salary...",
                "2. Department (8 đỉnh): dept_code, dept_name, location, budget...",
                "3. Project (15 đỉnh): proj_code, proj_name, priority, proj_status...",
                "4. Skill (16 đỉnh): skill_code, skill_name, skill_category.",
                "5. Role (5 đỉnh) & 6. AppUser (3 đỉnh phân quyền Web).",
            ],
            "code_title": "Các Cạnh Liên Kết & Chiến lược Đánh Chỉ Mục",
            "code": """# Thuộc tính có chỉ mục tìm kiếm nhanh
emp_code: string @index(exact, term) @upsert .
full_name: string @index(term, fulltext, trigram) .
salary: float @index(float) .

# Cạnh đồ thị 2 chiều (@reverse) và đếm nhanh (@count)
belongs_to_dept: uid @reverse .
reports_to: uid @reverse .
works_on: [uid] @reverse @count .
has_skill: [uid] @reverse @count .
collaborated_with: [uid] @reverse @count .""",
            "notes": "Lời thoại Slide 7: Nhóm thiết kế lược đồ đồ thị gồm 6 kiểu đỉnh và 11 vị từ cạnh. Đặc biệt nhóm khai báo @reverse trên các cạnh quan trọng để duyệt 2 chiều bằng dấu ngã (~) và gắn @facets lên cạnh works_on, has_skill, collaborated_with.",
        },
        # Slide 8
        {
            "title": "7. KHỞI TẠO CSDL & SINH DỮ LIỆU MẪU THỰC TẾ (127 ĐỈNH)",
            "sub": "Mục 5 Thang điểm: Script database/seed_data.py sinh 2.356 dòng N-Quads RDF kèm Facets",
            "left_title": "Quy mô & Đặc điểm Bộ dữ liệu đã nạp",
            "left_bullets": [
                "80 Nhân viên chia 5 cấp: CEO (EMP001) -> 7 Trưởng phòng (gồm Nguyễn Phạm Duy Luân EMP002 & Đỗ Văn Minh EMP003) -> 14 Tech Leads -> 58 Kỹ sư.",
                "8 Phòng ban tại Hà Nội, TP.HCM, Đà Nẵng.",
                "15 Dự án trọng điểm có nhân sự tham gia chéo liên phòng ban.",
                "Riêng dự án PRJ15 chỉ có 2 thành viên để kiểm thử phát hiện rủi ro Bus Factor.",
            ],
            "code_title": "Mẫu dữ liệu RDF N-Quads kèm Facets (database/data.rdf)",
            "code": """<_:emp2> <dgraph.type> "Employee" .
<_:emp2> <emp_code> "EMP002" .
<_:emp2> <full_name> "Nguyễn Phạm Duy Luân" .
<_:emp2> <belongs_to_dept> <_:dept2> .
<_:emp2> <reports_to> <_:emp1> .
<_:emp2> <has_skill> <_:skill1> (proficiency=5, years=5) .
<_:emp2> <works_on> <_:proj1> (role_in_project="Project Lead", hours_per_week=25) .
<_:emp2> <collaborated_with> <_:emp3> (projects_together=2, trust_score=9) .""",
            "notes": "Lời thoại Slide 8: Bộ dữ liệu được sinh tự động bằng seed_data.py tạo ra 2.356 dòng N-Quads chuẩn RDF và nạp vào Dgraph Alpha cấp phát 127 UID. Trên slide là ví dụ thực tế của đỉnh EMP002 Nguyễn Phạm Duy Luân cùng các cạnh có gắn Facets.",
        },
        # Slide 9
        {
            "title": "8. TỔNG HỢP 10 TRUY VẤN CƠ BẢN TRÊN RATEL (Q01 – Q10)",
            "sub": "Mục 7a Thang điểm (0,5đ): Đã chạy kiểm chứng 10/10 câu trên Dgraph Alpha",
            "left_title": "Danh mục 10 Truy vấn Cơ bản (queries_basic.dql)",
            "left_bullets": [
                "Q01: Danh sách 8 Phòng ban kèm Trưởng phòng (type, orderasc).",
                "Q02: Tìm kiếm nhân viên Nguyễn Phạm Duy Luân & Đỗ Văn Minh (allofterms).",
                "Q03: Liệt kê nhân sự Phòng Kỹ Thuật Phần Mềm (~belongs_to_dept).",
                "Q04: Lọc 5 dự án Active có độ ưu tiên Critical (@filter).",
                "Q05: Hồ sơ 360 độ của nhân viên EMP002 kèm @facets.",
            ],
            "code_title": "Q06 – Q10 & Minh họa Câu Q05 (Hồ sơ 360 độ + Facets)",
            "code": """# Q06: Phân trang Top 10 nhân viên lương >= 45 triệu
# Q07: Thống kê 16 Kỹ năng & đếm số người sở hữu
# Q08: Lọc Quản lý/Tech Lead gia nhập 2017-2020
# Q09: Chi tiết dự án PRJ01 & thành viên tham gia
# Q10: Danh sách cấp dưới trực tiếp của CEO & EMP002
{
  employee_360(func: eq(emp_code, "EMP002")) {
    emp_code full_name title salary
    belongs_to_dept { dept_name }
    has_skill @facets(proficiency, years) { skill_name }
    works_on @facets(role_in_project, hours_per_week) { proj_name }
  }
}""",
            "notes": "Lời thoại Slide 9: Nhóm đã xây dựng và chạy kiểm chứng 10 câu truy vấn cơ bản từ Q01 đến Q10 bao quát đầy đủ các phép tìm kiếm chỉ mục, lọc điều kiện, duyệt cạnh ngược, lấy thuộc tính trên cạnh @facets và phân trang.",
        },
        # Slide 10
        {
            "title": "9. TRUY VẤN NÂNG CAO (PHẦN 1): ĐỆ QUY @RECURSE & SHORTEST PATH",
            "sub": "Mục 7b Thang điểm (0,5đ): Duyệt cây phân cấp tổ chức (A01) & Đường đi ngắn nhất (A02)",
            "code_title": "Câu A01: Đệ quy Sơ đồ tổ chức (@recurse) & Câu A02: Đường kết nối ngắn nhất (shortest)",
            "code": """# [A01] Duyệt đệ quy 5 tầng từ Tổng Giám Đốc (EMP001) xuống toàn công ty
{
  org_chart_recurse(func: eq(emp_code, "EMP001")) @recurse(depth: 5, loop: false) {
    uid emp_code full_name title level ~reports_to
  }
}

# [A02] Tìm đường cộng tác ngắn nhất từ EMP002 (Phòng Kỹ Thuật) sang EMP021 (Phòng An Ninh Mạng)
{
  A as var(func: eq(emp_code, "EMP002"))
  B as var(func: eq(emp_code, "EMP021"))
  path as shortest(from: uid(A), to: uid(B), numpaths: 2) { collaborated_with }
  shortest_connection(func: uid(path)) {
    emp_code full_name title belongs_to_dept { dept_name }
  }
}
# -> Kết quả thực tế: EMP002 (Nguyễn Phạm Duy Luân) -> EMP005 (Phạm Thu Hà) -> EMP021 (Chu Văn An)""",
            "left_title": "Giá trị Nghiệp vụ Đồ thị",
            "left_bullets": [
                "@recurse giúp dựng cây tổ chức N tầng chỉ bằng 7 dòng lệnh thay vì viết Recursive CTE phức tạp trong SQL.",
                "shortest path tìm ra ngay nhân sự trung gian (EMP005) để kết nối hai phòng ban khác nhau chỉ qua 2 bước nhảy.",
            ],
            "notes": "Lời thoại Slide 10: Sang phần truy vấn nâng cao, câu A01 dùng chỉ thị @recurse để lấy toàn bộ cây phân cấp 5 tầng từ CEO. Câu A02 dùng thuật toán shortest tìm ra đường kết nối ngắn nhất giữa EMP002 ở Phòng Kỹ thuật và EMP021 ở Phòng An Ninh Mạng thông qua cầu nối EMP005.",
        },
        # Slide 11
        {
            "title": "10. TRUY VẤN NÂNG CAO (PHẦN 2): @CASCADE & GHÉP ĐỘI DỰ ÁN",
            "sub": "Mục 7b Thang điểm: Lọc lan truyền @cascade (A03) & Giao/Hiệu tập biến UID (A04, A05)",
            "code_title": "Câu A04: Gợi ý ứng viên có kỹ năng dự án PRJ02 cần nhưng CHƯA tham gia PRJ02",
            "code": """{
  var(func: eq(proj_code, "PRJ02")) {
    req_sk as requires_skill
    current_members as ~works_on
  }
  var(func: uid(req_sk)) {
    candidates as ~has_skill @filter(NOT uid(current_members)) {
      matched_skills_count as count(has_skill @filter(uid(req_sk)))
    }
  }
  recommended_candidates(func: uid(candidates), orderdesc: val(matched_skills_count), first: 5) {
    emp_code full_name matched_skills: val(matched_skills_count)
    belongs_to_dept { dept_name }
    has_skill @filter(uid(req_sk)) { skill_name }
  }
}""",
            "left_title": "Các kỹ thuật nâng cao A03 – A05",
            "left_bullets": [
                "A03 (@cascade): Tìm đúng 12 chuyên gia VỪA có kỹ năng Dgraph (SK01) VỪA đang đánh dự án Critical.",
                "A04 (Biến UID & NOT uid): Tìm ứng viên khớp nhiều kỹ năng nhất cho dự án PRJ02 mà chưa thuộc dự án đó.",
                "A05 (Math Score): Phát hiện Top 10 'Nhân sự cầu nối liên phòng ban'.",
            ],
            "notes": "Lời thoại Slide 11: Ở câu A03 và A04, nhóm kết hợp chỉ thị @cascade và biến UID (var) để giải bài toán ghép đội dự án thông minh: tìm những nhân sự có nhiều kỹ năng khớp với dự án PRJ02 nhất nhưng loại trừ những người đã ở trong dự án đó.",
        },
        # Slide 12
        {
            "title": "11. TRUY VẤN NÂNG CAO (PHẦN 3): RỦI RO BUS FACTOR & TÁC ĐỘNG NGHỈ VIỆC",
            "sub": "Mục 7b Thang điểm: Aggregation (A06), Bus Factor (A07), Impact Analysis (A08), Centrality (A10)",
            "left_title": "Tổng hợp kết quả chạy thật Câu A06 – A10",
            "left_bullets": [
                "A06 (Aggregation): Tính tổng quỹ lương, lương TB & max của 8 phòng ban.",
                "A07 (Bus Factor): Phát hiện dự án Critical PRJ15 chỉ phụ thuộc vào đúng 2 thành viên (EMP002 & EMP009).",
                "A08 (Impact Analysis 2-hop): Mô phỏng nếu EMP002 nghỉ việc -> ảnh hưởng DEPT02 (20 người), 3 dự án làm Lead và 4 dự án phụ thuộc dây chuyền.",
                "A09 (@facets filter) & A10 (Top 10 Degree Centrality).",
            ],
            "code_title": "Câu A07: Phát hiện Dự án rủi ro cao vì phụ thuộc ít người",
            "code": """{
  var(func: type(Project)) @filter(eq(proj_status, "Active")) {
    member_cnt as count(~works_on)
  }
  high_risk_projects(func: uid(member_cnt), orderasc: val(member_cnt))
    @filter(le(val(member_cnt), 5)) {
    proj_code proj_name priority
    bus_factor_members: val(member_cnt)
    ~works_on { emp_code full_name }
  }
}
# -> Phát hiện ngay PRJ15 (DQL Performance Lab): chỉ có 2 người!""",
            "notes": "Lời thoại Slide 12: Các câu A06 đến A10 khai thác sức mạnh phân tích quản trị: câu A07 tự động phát hiện dự án PRJ15 có rủi ro Bus Factor vì chỉ có 2 người nắm giữ; câu A08 mô phỏng tác động dây chuyền nếu một Giám đốc kỹ thuật nghỉ việc.",
        },
        # Slide 13
        {
            "title": "12. IMPORT / EXPORT DỮ LIỆU VÀ BACKUP / RESTORE CSDL",
            "sub": "Mục 6 Thang điểm (0,5đ): Quy trình thực thi không dùng Docker trên Windows",
            "left_title": "Cơ chế Xuất/Nhập & Sao lưu đã thực hiện",
            "left_bullets": [
                "1. Hot Export (RDF & JSON): Gọi GraphQL mutation tới http://localhost:8080/admin xuất ra g01.rdf.gz, g01.json.gz và g01.schema.gz.",
                "2. Backup tự động (scripts/export_backup.bat): Sao lưu toàn bộ bản nén Export & Schema vào thư mục backups/export_latest.",
                "3. Import & Restore (scripts/restore_import.bat & dgraph.exe live): Khôi phục lại toàn bộ 127 đỉnh và 2.356 bộ ba RDF.",
            ],
            "code_title": "Kết quả chạy thật scripts/export_backup.bat trên máy",
            "code": """POST http://localhost:8080/admin
mutation { export(input: { format: "rdf" }) {
  response { code message } exportedFiles
}}
-> {"code":"Success","message":"Export completed.",
    "exportedFiles":[
      "dgraph.r10037.u1023.1042\\g01.rdf.gz",
      "dgraph.r10037.u1023.1042\\g01.json.gz",
      "dgraph.r10037.u1023.1042\\g01.schema.gz"
    ]}""",
            "notes": "Lời thoại Slide 13: Về mục Import/Export và Backup/Restore không dùng Docker, nhóm đã xây dựng script export_backup.bat gọi trực tiếp API /admin của Dgraph Alpha để xuất cả 2 định dạng RDF và JSON nén, đồng thời khôi phục qua dgraph.exe live hoặc restore_import.bat.",
        },
        # Slide 14
        {
            "title": "13. KIẾN TRÚC ỨNG DỤNG WEB MINH HỌA: HR GRAPH 360",
            "sub": "Mục 8 Thang điểm (0,5đ): Kết nối CSDL Dgraph với phần mềm ứng dụng qua HTTP API",
            "left_title": "Kiến trúc 3 tầng gọn nhẹ, chạy ngay không cần cài đặt",
            "left_bullets": [
                "Cấu hình kết nối tách biệt qua file .env (DGRAPH_ALPHA_URL=http://localhost:8080, APP_PORT=5000).",
                "Tầng kết nối dữ liệu (app/dgraph_client.py): Đóng gói query_dql(), mutate_json(), mutate_rdf(), export_database().",
                "Backend Python HTTP Server (app/server.py) & Giao diện Web tương tác Cytoscape.js (app/static/index.html).",
            ],
            "code_title": "Trích đoạn Module kết nối app/dgraph_client.py",
            "code": """class DgraphClient:
    def __init__(self, alpha_url=None):
        self.alpha_url = alpha_url or os.environ.get(
            "DGRAPH_ALPHA_URL", "http://localhost:8080"
        )
    def query_dql(self, dql_string):
        return self._request(self.alpha_url, "/query",
            dql_string.encode("utf-8"), "application/dql", "POST")
    def mutate_json(self, set_obj=None, delete_obj=None):
        return self._request(self.alpha_url, "/mutate?commitNow=true",
            json.dumps({"set": set_obj}).encode("utf-8"),
            "application/json", "POST")""",
            "notes": "Lời thoại Slide 14: Để minh họa việc kết nối Dgraph với phần mềm ứng dụng, nhóm xây dựng ứng dụng Web HR Graph 360 chạy tại cổng 5000. Module dgraph_client.py đọc cấu hình từ file .env và giao tiếp trực tiếp với Dgraph Alpha.",
        },
        # Slide 15
        {
            "title": "14. DEMO ỨNG DỤNG (1): QUẢN TRỊ NGƯỜI DÙNG & THAO TÁC CSDL",
            "sub": "Mục 9a & 9b Thang điểm (1,0đ): Phân quyền 3 cấp (RBAC), CRUD Đỉnh/Cạnh & Nút Backup",
            "left_title": "Quản trị Người dùng & Phân quyền (Tab 5)",
            "left_bullets": [
                "Lưu trữ tài khoản bằng kiểu đỉnh AppUser ngay trong Dgraph.",
                "1. Admin (admin / Nguyễn Phạm Duy Luân): Toàn quyền CRUD, quản lý user, bấm nút Export RDF/JSON & Reset Seed.",
                "2. Manager (manager / Đỗ Văn Minh): Thêm/sửa nhân sự, gán cạnh dự án, chạy phân tích đồ thị.",
                "3. Employee (employee): Chỉ có quyền xem & tra cứu (chặn ghi/xóa).",
            ],
            "right_title": "Thao tác CRUD Đỉnh, Cạnh & Backup trên GUI (Tab 3)",
            "right_bullets": [
                "Thêm mới, chỉnh sửa, xóa trực tiếp đỉnh Nhân viên (Employee).",
                "Trình tạo/xóa cạnh đồ thị (works_on, has_skill, collaborated_with, reports_to) có gắn kèm Facets (hours_per_week, proficiency).",
                "Tích hợp nút bấm Export RDF (.rdf.gz), Export JSON (.json.gz) và Khôi phục dữ liệu chuẩn ngay trên màn hình Web.",
            ],
            "notes": "Lời thoại Slide 15: Ứng dụng đáp ứng đầy đủ 4 nhóm chức năng demo. Thứ nhất là hệ thống đăng nhập 3 quyền Admin, Manager, Employee. Thứ hai là màn hình CRUD cho phép thêm/sửa/xóa đỉnh nhân viên, tạo/xóa cạnh kèm Facets và bấm nút Export/Backup ngay trên giao diện.",
        },
        # Slide 16
        {
            "title": "15. DEMO ỨNG DỤNG (2): NGHIỆP VỤ ĐỒ THỊ & TRỰC QUAN HÓA",
            "sub": "Mục 9c & 9d Thang điểm (1,0đ): 4 Mô-đun Nghiệp vụ Đồ thị & Sơ đồ Mạng lưới Cytoscape.js",
            "left_title": "4 Chức năng Nghiệp vụ Bài toán (Tab 2)",
            "left_bullets": [
                "1. Tra cứu Chuỗi báo cáo đệ quy (@recurse Org-Chart) theo từng lãnh đạo.",
                "2. Tìm đường kết nối ngắn nhất (Shortest Path) giữa 2 nhân viên bất kỳ.",
                "3. Gợi ý ghép đội dự án thông minh theo kỹ năng (@cascade & var).",
                "4. Phân tích tác động khi nhân sự nghỉ việc & Cảnh báo dự án rủi ro Bus Factor.",
            ],
            "right_title": "Chức năng Hỗ trợ & Trực quan hóa (Tab 1 & Tab 4)",
            "right_bullets": [
                "Sơ đồ mạng lưới tương tác Cytoscape.js: kéo thả đỉnh Nhân viên (xanh), Phòng ban (tím), Dự án (cam); click xem chi tiết UID & JSON.",
                "Bảng thống kê gom nhóm quỹ lương & nhân sự theo từng phòng ban.",
                "Trình chạy DQL trực tiếp tích hợp sẵn thư viện 20 câu truy vấn mẫu (Q01–Q10 & A01–A10).",
            ],
            "notes": "Lời thoại Slide 16: Nhóm chức năng thứ 3 và thứ 4 trên ứng dụng gồm: sơ đồ mạng lưới tương tác vẽ bằng Cytoscape.js, 4 công cụ phân tích đồ thị chuyên sâu ở Tab 2, và trình chạy DQL tích hợp sẵn cả 20 câu truy vấn ở Tab 4.",
        },
        # Slide 17
        {
            "title": "16. BẢNG ĐỐI CHIẾU KẾT QUẢ THỰC HIỆN VỚI THANG ĐIỂM",
            "sub": "Mục 10 Thang điểm: Kiểm chứng hoàn thành 100% yêu cầu đề tài",
            "left_title": "Mục 1 đến Mục 6 (4,5 điểm)",
            "left_bullets": [
                "Mục 1 (0,5đ): Lý thuyết + Cài đặt Dgraph v20.11.3 & Ratel trên Windows.",
                "Mục 2 (0,5đ): Giải phẫu chi tiết 6 tab chức năng của Ratel.",
                "Mục 3 (0,5đ): Bảng so sánh 8 tiêu chí Ratel vs Neo4j Browser/Bloom.",
                "Mục 4 (0,5đ): Phân tích 5 nhóm ứng dụng Dgraph mạnh & giới hạn.",
                "Mục 5 (2,0đ): Schema 6 kiểu đỉnh + Nạp 127 đỉnh, 2.356 dòng RDF.",
                "Mục 6 (0,5đ): Export RDF/JSON (.gz) + Script Backup & Restore.",
            ],
            "right_title": "Mục 7 đến Mục 10 (5,5 điểm)",
            "right_bullets": [
                "Mục 7 (1,0đ): 10 Truy vấn cơ bản (Q01–Q10) + 10 Truy vấn nâng cao (A01–A10) đã kiểm chứng kết quả thật.",
                "Mục 8 (0,5đ): Module kết nối DgraphClient qua .env.",
                "Mục 9 (2,0đ): Web App HR Graph 360 đủ 4 nhóm chức năng demo.",
                "Mục 10 (2,0đ): Báo cáo Word, Slide PowerPoint 18 trang, Source code, README & 18 câu hỏi bảo vệ.",
            ],
            "notes": "Lời thoại Slide 17: Trên đây là bảng tổng kết đối chiếu từng mục trong thang điểm của giảng viên với các sản phẩm thực tế mà nhóm đã hoàn thành và kiểm chứng.",
        },
        # Slide 18
        {
            "title": "17. KẾT LUẬN & PHIÊN HỎI ĐÁP BẢO VỆ ĐỒ ÁN (Q&A)",
            "sub": "Cảm ơn Giảng viên và các bạn đã theo dõi — Nhóm sẵn sàng Demo trực tiếp & Trả lời câu hỏi",
            "left_title": "Tổng kết đóng góp của Đồ án",
            "left_bullets": [
                "Triển khai thành công Dgraph & Ratel trực tiếp trên Windows không cần Docker.",
                "Xây dựng bộ CSDL đồ thị doanh nghiệp hoàn chỉnh (127 đỉnh, 2.356 N-Quads) và kiểm chứng 20 câu truy vấn DQL từ cơ bản đến nâng cao.",
                "Phát triển ứng dụng Web HR Graph 360 trực quan hóa và giải quyết bài toán quản trị mạng lưới nhân sự – phòng ban – dự án.",
            ],
            "right_title": "Sẵn sàng Demo trực tiếp trên máy",
            "right_bullets": [
                "1. Giao diện công cụ GUI Dgraph Ratel: http://localhost:8000/?local",
                "2. Ứng dụng Web HR Graph 360: http://127.0.0.1:5000",
                "3. Kiểm tra trạng thái Dgraph Alpha: http://localhost:8080/health",
                "Xin mời Thầy/Cô đặt câu hỏi cho nhóm (Nguyễn Phạm Duy Luân, Đỗ Văn Minh & TV3)!",
            ],
            "notes": "Lời thoại Slide 18: Nhóm xin kết thúc phần trình bày slide tại đây và xin phép chuyển sang màn hình trình duyệt để demo trực tiếp trên công cụ Ratel (cổng 8000) và ứng dụng HR Graph 360 (cổng 5000). Rất mong nhận được câu hỏi và góp ý của thầy/cô!",
        },
    ]

    for idx, sdata in enumerate(slides_data, start=1):
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = LIGHT_BG

        add_header(slide, sdata["title"], sdata["sub"], idx)

        if "code" in sdata:
            add_card(slide, 0.5, 1.45, 5.6, 5.55, sdata["left_title"], sdata["left_bullets"], border_color=BLUE)
            add_code_card(slide, 6.3, 1.45, 6.53, 5.55, sdata["code_title"], sdata["code"])
        else:
            add_card(slide, 0.5, 1.45, 6.0, 5.55, sdata["left_title"], sdata["left_bullets"], border_color=BLUE)
            add_card(slide, 6.8, 1.45, 6.0, 5.55, sdata["right_title"], sdata["right_bullets"], border_color=GREEN)

        set_notes(slide, sdata["notes"])

    prs.save(OUT_PPTX)
    print(f"[HOÀN TẤT] Đã xuất 18 Slide PowerPoint kèm Lời thoại tại: {OUT_PPTX}")


if __name__ == "__main__":
    build_presentation()

