# -*- coding: utf-8 -*-
"""
Script khởi tạo Schema và sinh dữ liệu mẫu cho CSDL Đồ thị Dgraph
Đề tài: Quản lý mạng lưới quan hệ giữa nhân viên, phòng ban và dự án trong doanh nghiệp
Sinh ra:
  - database/data.rdf  (Định dạng N-Quads RDF chuẩn của Dgraph, có kèm Facets)
  - database/data.json (Định dạng JSON Mutation chuẩn của Dgraph)
Và nạp trực tiếp vào Dgraph Alpha qua cổng HTTP 8080.
"""

import json
import os
import random
import sys
import urllib.request
import urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.dql")
RDF_PATH = os.path.join(BASE_DIR, "data.rdf")
JSON_PATH = os.path.join(BASE_DIR, "data.json")
DGRAPH_ALPHA_URL = os.environ.get("DGRAPH_ALPHA_URL", "http://localhost:8080")

random.seed(42)


def build_dataset():
    # 1. Danh sách 8 Phòng ban (Departments)
    departments = [
        {"uid": "_:dept1", "dept_code": "DEPT01", "dept_name": "Ban Giám Đốc Điều Hành", "location": "Tầng 15 - Hà Nội", "budget": 15000000000.0, "established_year": 2016, "mgr_emp": "_:emp1"},
        {"uid": "_:dept2", "dept_code": "DEPT02", "dept_name": "Phòng Kỹ Thuật Phần Mềm", "location": "Tầng 12 - TP.HCM", "budget": 8500000000.0, "established_year": 2017, "mgr_emp": "_:emp2"},
        {"uid": "_:dept3", "dept_code": "DEPT03", "dept_name": "Phòng Khoa Học Dữ Liệu & AI", "location": "Tầng 14 - TP.HCM", "budget": 9200000000.0, "established_year": 2018, "mgr_emp": "_:emp3"},
        {"uid": "_:dept4", "dept_code": "DEPT04", "dept_name": "Phòng Hạ Tầng & Điện Toán Đám Mây", "location": "Tầng 10 - Hà Nội", "budget": 7800000000.0, "established_year": 2017, "mgr_emp": "_:emp4"},
        {"uid": "_:dept5", "dept_code": "DEPT05", "dept_name": "Phòng An Ninh Mạng (SecOps)", "location": "Tầng 11 - Hà Nội", "budget": 6400000000.0, "established_year": 2019, "mgr_emp": "_:emp5"},
        {"uid": "_:dept6", "dept_code": "DEPT06", "dept_name": "Phòng Thiết Kế Sản Phẩm & UI/UX", "location": "Tầng 9 - TP.HCM", "budget": 4500000000.0, "established_year": 2018, "mgr_emp": "_:emp6"},
        {"uid": "_:dept7", "dept_code": "DEPT07", "dept_name": "Phòng Phát Triển Kinh Doanh & Giải Pháp", "location": "Tầng 8 - Đà Nẵng", "budget": 5600000000.0, "established_year": 2019, "mgr_emp": "_:emp7"},
        {"uid": "_:dept8", "dept_code": "DEPT08", "dept_name": "Phòng Quản Trị Nguồn Nhân Lực", "location": "Tầng 7 - TP.HCM", "budget": 3800000000.0, "established_year": 2016, "mgr_emp": "_:emp8"},
    ]

    # 2. Danh sách 16 Kỹ năng (Skills)
    skills = [
        {"uid": "_:skill1", "skill_code": "SK01", "skill_name": "Dgraph & GraphQL", "skill_category": "Database"},
        {"uid": "_:skill2", "skill_code": "SK02", "skill_name": "Python Backend", "skill_category": "Backend"},
        {"uid": "_:skill3", "skill_code": "SK03", "skill_name": "Golang Microservices", "skill_category": "Backend"},
        {"uid": "_:skill4", "skill_code": "SK04", "skill_name": "React & TypeScript", "skill_category": "Frontend"},
        {"uid": "_:skill5", "skill_code": "SK05", "skill_name": "Machine Learning & NLP", "skill_category": "Data & AI"},
        {"uid": "_:skill6", "skill_code": "SK06", "skill_name": "Big Data & Spark", "skill_category": "Data & AI"},
        {"uid": "_:skill7", "skill_code": "SK07", "skill_name": "Kubernetes & Cloud Architecture", "skill_category": "Infrastructure"},
        {"uid": "_:skill8", "skill_code": "SK08", "skill_name": "CI/CD & DevOps Automation", "skill_category": "Infrastructure"},
        {"uid": "_:skill9", "skill_code": "SK09", "skill_name": "Application Security & Pentest", "skill_category": "Security"},
        {"uid": "_:skill10", "skill_code": "SK10", "skill_name": "Zero Trust Network Security", "skill_category": "Security"},
        {"uid": "_:skill11", "skill_code": "SK11", "skill_name": "UI/UX Design System", "skill_category": "Product"},
        {"uid": "_:skill12", "skill_code": "SK12", "skill_name": "Product Management & Agile", "skill_category": "Product"},
        {"uid": "_:skill13", "skill_code": "SK13", "skill_name": "Enterprise Solution Consulting", "skill_category": "Business"},
        {"uid": "_:skill14", "skill_code": "SK14", "skill_name": "Data Visualization & BI", "skill_category": "Data & AI"},
        {"uid": "_:skill15", "skill_code": "SK15", "skill_name": "Distributed Systems Architecture", "skill_category": "Backend"},
        {"uid": "_:skill16", "skill_code": "SK16", "skill_name": "HR Analytics & Talent Ops", "skill_category": "Operations"},
    ]

    # 3. Danh sách 5 Vai trò (Roles)
    roles = [
        {"uid": "_:role1", "role_code": "ROLE_EXEC", "role_name": "Ban Điều Hành Cấp Cao (C-Level)", "permissions": ["all", "approve_budget", "manage_org", "export_backup"]},
        {"uid": "_:role2", "role_code": "ROLE_MGR", "role_name": "Trưởng Phòng Ban (Department Head)", "permissions": ["manage_dept", "assign_project", "view_salary", "run_analytics"]},
        {"uid": "_:role3", "role_code": "ROLE_LEAD", "role_name": "Trưởng Nhóm Kỹ Thuật (Tech Lead)", "permissions": ["lead_project", "assign_task", "run_analytics"]},
        {"uid": "_:role4", "role_code": "ROLE_SR", "role_name": "Chuyên Gia Cao Cấp (Senior Specialist)", "permissions": ["contribute_project", "mentor_staff", "view_graph"]},
        {"uid": "_:role5", "role_code": "ROLE_SPEC", "role_name": "Chuyên Viên Phát Triển (Specialist)", "permissions": ["contribute_project", "view_graph"]},
    ]

    # 4. Danh sách 15 Dự án (Projects)
    projects = [
        {"uid": "_:proj1", "proj_code": "PRJ01", "proj_name": "Hệ Thống Đồ Thị Tri Thức Doanh Nghiệp (Enterprise Knowledge Graph)", "proj_status": "Active", "priority": "Critical", "proj_budget": 4200000000.0, "start_date": "2025-01-15T00:00:00Z", "end_date": "2026-12-31T00:00:00Z", "dept": "_:dept2", "lead": "_:emp2", "req_skills": ["_:skill1", "_:skill2", "_:skill3", "_:skill15"], "depends": []},
        {"uid": "_:proj2", "proj_code": "PRJ02", "proj_name": "Nền Tảng Phát Hiện Gian Lận Giao Dịch Thời Gian Thực (Fraud Graph)", "proj_status": "Active", "priority": "Critical", "proj_budget": 5100000000.0, "start_date": "2025-02-01T00:00:00Z", "end_date": "2026-11-30T00:00:00Z", "dept": "_:dept3", "lead": "_:emp3", "req_skills": ["_:skill1", "_:skill5", "_:skill6", "_:skill9"], "depends": ["_:proj1"]},
        {"uid": "_:proj3", "proj_code": "PRJ03", "proj_name": "Trợ Lý AI Phân Tích Nghiệp vụ Nội Bộ (Enterprise Copilot)", "proj_status": "Active", "priority": "High", "proj_budget": 3600000000.0, "start_date": "2025-03-10T00:00:00Z", "end_date": "2026-10-15T00:00:00Z", "dept": "_:dept3", "lead": "_:emp10", "req_skills": ["_:skill2", "_:skill5", "_:skill4"], "depends": ["_:proj1"]},
        {"uid": "_:proj4", "proj_code": "PRJ04", "proj_name": "Hạ Tầng Đám Mây Đa Vùng Tự Động Hóa (Multi-Cloud Mesh)", "proj_status": "Active", "priority": "High", "proj_budget": 4800000000.0, "start_date": "2025-01-20T00:00:00Z", "end_date": "2026-09-30T00:00:00Z", "dept": "_:dept4", "lead": "_:emp4", "req_skills": ["_:skill7", "_:skill8", "_:skill10"], "depends": []},
        {"uid": "_:proj5", "proj_code": "PRJ05", "proj_name": "Trung Tâm Giám Sát Bảo Mật Zero-Trust (Zero-Trust SOC)", "proj_status": "Active", "priority": "Critical", "proj_budget": 3900000000.0, "start_date": "2025-04-01T00:00:00Z", "end_date": "2026-12-15T00:00:00Z", "dept": "_:dept5", "lead": "_:emp5", "req_skills": ["_:skill9", "_:skill10", "_:skill7"], "depends": ["_:proj4"]},
        {"uid": "_:proj6", "proj_code": "PRJ06", "proj_name": "Cổng Quản Trị Nhân Sự & Mạng Lưới Tổ Chức 360 (HR Graph Portal)", "proj_status": "Active", "priority": "High", "proj_budget": 2400000000.0, "start_date": "2025-05-01T00:00:00Z", "end_date": "2026-08-30T00:00:00Z", "dept": "_:dept8", "lead": "_:emp8", "req_skills": ["_:skill1", "_:skill4", "_:skill11", "_:skill16"], "depends": ["_:proj1"]},
        {"uid": "_:proj7", "proj_code": "PRJ07", "proj_name": "Hệ Thống Gợi Ý Sản Phẩm Cá Nhân Hóa Đa Kênh (Graph Recommender)", "proj_status": "Active", "priority": "High", "proj_budget": 3300000000.0, "start_date": "2025-03-15T00:00:00Z", "end_date": "2026-10-30T00:00:00Z", "dept": "_:dept2", "lead": "_:emp9", "req_skills": ["_:skill1", "_:skill3", "_:skill5", "_:skill14"], "depends": ["_:proj1"]},
        {"uid": "_:proj8", "proj_code": "PRJ08", "proj_name": "Bộ Khung Giao Diện Thiết Kế Thống Nhất (Unified Design System)", "proj_status": "Completed", "priority": "Medium", "proj_budget": 1500000000.0, "start_date": "2024-06-01T00:00:00Z", "end_date": "2025-06-30T00:00:00Z", "dept": "_:dept6", "lead": "_:emp6", "req_skills": ["_:skill4", "_:skill11", "_:skill12"], "depends": []},
        {"uid": "_:proj9", "proj_code": "PRJ09", "proj_name": "Nền Tảng Tích Hợp Dữ Liệu Hồ (Real-time Data Lakehouse)", "proj_status": "Active", "priority": "High", "proj_budget": 4100000000.0, "start_date": "2025-02-10T00:00:00Z", "end_date": "2026-11-15T00:00:00Z", "dept": "_:dept3", "lead": "_:emp11", "req_skills": ["_:skill6", "_:skill2", "_:skill14"], "depends": ["_:proj4"]},
        {"uid": "_:proj10", "proj_code": "PRJ10", "proj_name": "Cổng Giao Tiếp Khách Hàng Doanh Nghiệp B2B (B2B Solution Hub)", "proj_status": "Active", "priority": "Medium", "proj_budget": 2700000000.0, "start_date": "2025-04-15T00:00:00Z", "end_date": "2026-09-01T00:00:00Z", "dept": "_:dept7", "lead": "_:emp7", "req_skills": ["_:skill4", "_:skill12", "_:skill13"], "depends": ["_:proj8"]},
        {"uid": "_:proj11", "proj_code": "PRJ11", "proj_name": "Hệ Thống Kiểm Thử & Triển Khai Tự Động (GitOps Pipeline)", "proj_status": "Completed", "priority": "Medium", "proj_budget": 1900000000.0, "start_date": "2024-08-01T00:00:00Z", "end_date": "2025-07-31T00:00:00Z", "dept": "_:dept4", "lead": "_:emp12", "req_skills": ["_:skill7", "_:skill8", "_:skill3"], "depends": []},
        {"uid": "_:proj12", "proj_code": "PRJ12", "proj_name": "Kiến Trúc Vi Dịch Vụ Cốt Lõi Thế Hệ Mới (Core Go Mesh)", "proj_status": "Active", "priority": "Critical", "proj_budget": 4600000000.0, "start_date": "2025-01-10T00:00:00Z", "end_date": "2026-12-20T00:00:00Z", "dept": "_:dept2", "lead": "_:emp9", "req_skills": ["_:skill3", "_:skill15", "_:skill7"], "depends": ["_:proj11"]},
        {"uid": "_:proj13", "proj_code": "PRJ13", "proj_name": "Hệ Thống Mã Hóa & Định Danh Tập Trung (IAM Shield)", "proj_status": "Planning", "priority": "High", "proj_budget": 2900000000.0, "start_date": "2026-01-01T00:00:00Z", "end_date": "2026-12-31T00:00:00Z", "dept": "_:dept5", "lead": "_:emp13", "req_skills": ["_:skill9", "_:skill10", "_:skill3"], "depends": ["_:proj5"]},
        {"uid": "_:proj14", "proj_code": "PRJ14", "proj_name": "Bảng Điều Khiển Phân Tích Chiến Lược CEO (Executive BI Graph)", "proj_status": "Active", "priority": "Medium", "proj_budget": 2100000000.0, "start_date": "2025-06-01T00:00:00Z", "end_date": "2026-07-30T00:00:00Z", "dept": "_:dept1", "lead": "_:emp14", "req_skills": ["_:skill1", "_:skill14", "_:skill13"], "depends": ["_:proj1", "_:proj9"]},
        {"uid": "_:proj15", "proj_code": "PRJ15", "proj_name": "Dự Án Thử Nghiệm Tối Ưu Truy Vấn Đồ Thị (DQL Performance Lab)", "proj_status": "Active", "priority": "Critical", "proj_budget": 1800000000.0, "start_date": "2025-07-01T00:00:00Z", "end_date": "2026-10-01T00:00:00Z", "dept": "_:dept2", "lead": "_:emp2", "req_skills": ["_:skill1", "_:skill15"], "depends": ["_:proj1"]},
    ]

    # 5. Danh sách 80 Nhân viên (Employees) phân tầng rõ ràng:
    # - emp1: Tổng Giám Đốc (CEO - Level 1)
    # - emp2..emp8: 7 Trưởng phòng ban (Level 2, báo cáo cho emp1)
    #   + emp2: Nguyễn Phạm Duy Luân (Trưởng phòng Kỹ Thuật Phần Mềm - DEPT02)
    #   + emp3: Đỗ Văn Minh (Trưởng phòng Khoa Học Dữ Liệu & AI - DEPT03)
    # - emp9..emp22: 14 Tech Leads / Team Leads (Level 3, báo cáo cho Trưởng phòng)
    # - emp23..emp80: 58 Senior & Specialist (Level 4 & 5, báo cáo cho Tech Lead)
    core_employees = [
        {"uid": "_:emp1", "emp_code": "EMP001", "full_name": "Trần Quang Khải", "title": "Tổng Giám Đốc (CEO)", "level": 1, "dept": "_:dept1", "role": "_:role1", "reports_to": None, "salary": 95000000.0, "hire_date": "2016-01-10T00:00:00Z", "skills": ["_:skill12", "_:skill13", "_:skill15"]},
        {"uid": "_:emp2", "emp_code": "EMP002", "full_name": "Nguyễn Phạm Duy Luân", "title": "Giám Đốc Kỹ Thuật Phần Mềm", "level": 2, "dept": "_:dept2", "role": "_:role2", "reports_to": "_:emp1", "salary": 68000000.0, "hire_date": "2017-03-15T00:00:00Z", "skills": ["_:skill1", "_:skill2", "_:skill3", "_:skill15"]},
        {"uid": "_:emp3", "emp_code": "EMP003", "full_name": "Đỗ Văn Minh", "title": "Giám Đốc Khoa Học Dữ Liệu & AI", "level": 2, "dept": "_:dept3", "role": "_:role2", "reports_to": "_:emp1", "salary": 68000000.0, "hire_date": "2018-02-01T00:00:00Z", "skills": ["_:skill1", "_:skill2", "_:skill5", "_:skill6", "_:skill14"]},
        {"uid": "_:emp4", "emp_code": "EMP004", "full_name": "Lê Hoàng Nam", "title": "Trưởng Phòng Hạ Tầng & Cloud", "level": 2, "dept": "_:dept4", "role": "_:role2", "reports_to": "_:emp1", "salary": 62000000.0, "hire_date": "2017-06-20T00:00:00Z", "skills": ["_:skill7", "_:skill8", "_:skill15"]},
        {"uid": "_:emp5", "emp_code": "EMP005", "full_name": "Phạm Thu Hà", "title": "Trưởng Phòng An Ninh Mạng", "level": 2, "dept": "_:dept5", "role": "_:role2", "reports_to": "_:emp1", "salary": 64000000.0, "hire_date": "2019-01-15T00:00:00Z", "skills": ["_:skill9", "_:skill10", "_:skill7"]},
        {"uid": "_:emp6", "emp_code": "EMP006", "full_name": "Võ Ngọc Ánh", "title": "Trưởng Phòng Sản Phẩm & UI/UX", "level": 2, "dept": "_:dept6", "role": "_:role2", "reports_to": "_:emp1", "salary": 55000000.0, "hire_date": "2018-05-12T00:00:00Z", "skills": ["_:skill11", "_:skill12", "_:skill4"]},
        {"uid": "_:emp7", "emp_code": "EMP007", "full_name": "Đặng Quốc Tuấn", "title": "Trưởng Phòng Kinh Doanh Giải Pháp", "level": 2, "dept": "_:dept7", "role": "_:role2", "reports_to": "_:emp1", "salary": 58000000.0, "hire_date": "2019-03-01T00:00:00Z", "skills": ["_:skill13", "_:skill12", "_:skill14"]},
        {"uid": "_:emp8", "emp_code": "EMP008", "full_name": "Bùi Thanh Trúc", "title": "Trưởng Phòng Quản Trị Nhân Sự", "level": 2, "dept": "_:dept8", "role": "_:role2", "reports_to": "_:emp1", "salary": 52000000.0, "hire_date": "2016-09-01T00:00:00Z", "skills": ["_:skill16", "_:skill12", "_:skill14"]},
    ]

    # 14 Tech Leads (emp9 -> emp22)
    lead_Templates = [
        ("EMP009", "Hoàng Minh Đức", "Tech Lead Backend & Graph", "_:dept2", "_:emp2", ["_:skill1", "_:skill3", "_:skill15"]),
        ("EMP010", "Ngô Bảo Châu", "Tech Lead Trí Tuệ Nhân Tạo", "_:dept3", "_:emp3", ["_:skill2", "_:skill5", "_:skill1"]),
        ("EMP011", "Trịnh Đình Trọng", "Tech Lead Kỹ Thuật Dữ Liệu Lớn", "_:dept3", "_:emp3", ["_:skill6", "_:skill2", "_:skill14"]),
        ("EMP012", "Lý Công Uẩn", "Tech Lead DevOps & Kubernetes", "_:dept4", "_:emp4", ["_:skill7", "_:skill8", "_:skill3"]),
        ("EMP013", "Phan Đình Phùng", "Tech Lead Bảo Mật Ứng Dụng", "_:dept5", "_:emp5", ["_:skill9", "_:skill10", "_:skill2"]),
        ("EMP014", "Vũ Trọng Phụng", "Trưởng Nhóm Phân Tích Chiến Lược", "_:dept1", "_:emp1", ["_:skill13", "_:skill14", "_:skill1"]),
        ("EMP015", "Nguyễn Thị Minh Khai", "Tech Lead Frontend & Web Graph", "_:dept2", "_:emp2", ["_:skill4", "_:skill1", "_:skill11"]),
        ("EMP016", "hồ Xuân Hương", "Trưởng Nhóm Thiết Kế Trải Nghiệm", "_:dept6", "_:emp6", ["_:skill11", "_:skill12", "_:skill4"]),
        ("EMP017", "Đoàn Thị Điểm", "Trưởng Nhóm Tư Vấn Giải Pháp B2B", "_:dept7", "_:emp7", ["_:skill13", "_:skill12", "_:skill1"]),
        ("EMP018", "Lương Thế Vinh", "Trưởng Nhóm Phân Tích Nhân Sự", "_:dept8", "_:emp8", ["_:skill16", "_:skill14", "_:skill2"]),
        ("EMP019", "Trần Hưng Đạo", "Tech Lead Hệ Thống Phân Tán", "_:dept2", "_:emp2", ["_:skill3", "_:skill15", "_:skill7"]),
        ("EMP020", "Nguyễn Bỉnh Khiêm", "Tech Lead Hạ Tầng Đám Mây", "_:dept4", "_:emp4", ["_:skill7", "_:skill8", "_:skill10"]),
        ("EMP021", "Chu Văn An", "Tech Lead Điều Tra An Ninh Số", "_:dept5", "_:emp5", ["_:skill9", "_:skill10", "_:skill6"]),
        ("EMP022", "Lê Quý Đôn", "Tech Lead Khai Phá Đồ Thị", "_:dept3", "_:emp3", ["_:skill1", "_:skill5", "_:skill14"]),
    ]

    for idx, (code, name, title, dept, mgr, sks) in enumerate(lead_Templates, start=9):
        fixed_name = name[0].upper() + name[1:]
        core_employees.append({
            "uid": f"_:emp{idx}",
            "emp_code": code,
            "full_name": fixed_name,
            "title": title,
            "level": 3,
            "dept": dept,
            "role": "_:role3",
            "reports_to": mgr,
            "salary": float(random.randint(38, 48) * 1000000),
            "hire_date": f"20{random.randint(19, 22)}-0{random.randint(1, 9)}-15T00:00:00Z",
            "skills": sks,
        })

    # Sinh tiếp nhân viên emp23 -> emp80 (58 nhân sự cấp Senior=4 và Specialist=5)
    last_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
    middle_names = ["Văn", "Hữu", "Đức", "Minh", "Quốc", "Gia", "Thanh", "Ngọc", "Thị", "Thu", "Phương", "Khánh", "Bảo", "Tuấn", "Hoài"]
    first_names = ["An", "Bình", "Cường", "Dũng", "Giang", "Hải", "Hiếu", "Hùng", "Huy", "Khôi", "Linh", "Long", "Mai", "My", "Nam", "Nga", "Nhung", "Oanh", "Phúc", "Phương", "Quân", "Quỳnh", "Sơn", "Tâm", "Thảo", "Thắng", "Thịnh", "Trang", "Trinh", "Trung", "Tú", "Tùng", "Uyên", "Việt", "Vinh", "Vy", "Yến"]

    dept_leads_map = {
        "_:dept1": ["_:emp14"],
        "_:dept2": ["_:emp9", "_:emp15", "_:emp19"],
        "_:dept3": ["_:emp10", "_:emp11", "_:emp22"],
        "_:dept4": ["_:emp12", "_:emp20"],
        "_:dept5": ["_:emp13", "_:emp21"],
        "_:dept6": ["_:emp16"],
        "_:dept7": ["_:emp17"],
        "_:dept8": ["_:emp18"],
    }

    dept_titles_map = {
        "_:dept1": ("Chuyên Viên Phân Tích Chiến Lược", ["_:skill13", "_:skill14", "_:skill12"]),
        "_:dept2": ("Kỹ Sư Phần Mềm (Software Engineer)", ["_:skill1", "_:skill2", "_:skill3", "_:skill4", "_:skill15"]),
        "_:dept3": ("Kỹ Sư Dữ Liệu & AI (Data/AI Engineer)", ["_:skill1", "_:skill2", "_:skill5", "_:skill6", "_:skill14"]),
        "_:dept4": ("Kỹ Sư Hệ Thống Cloud & SRE", ["_:skill7", "_:skill8", "_:skill3", "_:skill10"]),
        "_:dept5": ("Chuyên Viên An Ninh Mạng (Security Analyst)", ["_:skill9", "_:skill10", "_:skill7", "_:skill2"]),
        "_:dept6": ("Chuyên Viên Thiết Kế Sản Phẩm UI/UX", ["_:skill11", "_:skill12", "_:skill4"]),
        "_:dept7": ("Chuyên Viên Tư Vấn Giải Pháp Doanh Nghiệp", ["_:skill13", "_:skill12", "_:skill14"]),
        "_:dept8": ("Chuyên Viên Quản Trị Nhân Sự & Đào Tạo", ["_:skill16", "_:skill12", "_:skill14"]),
    }

    dept_weights = ["_:dept2"] * 16 + ["_:dept3"] * 12 + ["_:dept4"] * 8 + ["_:dept5"] * 6 + ["_:dept6"] * 5 + ["_:dept7"] * 5 + ["_:dept8"] * 4 + ["_:dept1"] * 2

    for idx in range(23, 81):
        dept_uid = dept_weights[idx - 23]
        leads = dept_leads_map[dept_uid]
        lead_uid = leads[(idx - 23) % len(leads)]
        base_title, dept_skill_pool = dept_titles_map[dept_uid]
        is_senior = (idx % 3 == 0)
        level = 4 if is_senior else 5
        role_uid = "_:role4" if is_senior else "_:role5"
        title = ("Senior " + base_title) if is_senior else base_title
        emp_name = f"{last_names[idx % len(last_names)]} {middle_names[(idx * 3) % len(middle_names)]} {first_names[(idx * 7) % len(first_names)]}"
        chosen_skills = list(set(random.sample(dept_skill_pool, k=min(3, len(dept_skill_pool)))))
        if idx in (25, 31, 42):
            if "_:skill1" not in chosen_skills:
                chosen_skills.append("_:skill1")

        # Cho một số Specialist báo cáo cho Senior để tạo cây đệ quy 5 tầng sâu
        reports_to_uid = lead_uid
        if not is_senior and idx > 35 and (idx - 1) >= 23 and ((idx - 1) % 3 == 0):
            reports_to_uid = f"_:emp{idx - 1}"

        core_employees.append({
            "uid": f"_:emp{idx}",
            "emp_code": f"EMP{idx:03d}",
            "full_name": emp_name,
            "title": title,
            "level": level,
            "dept": dept_uid,
            "role": role_uid,
            "reports_to": reports_to_uid,
            "salary": float(random.randint(25, 36) * 1000000 if is_senior else random.randint(15, 24) * 1000000),
            "hire_date": f"20{random.randint(20, 25)}-0{random.randint(1, 9)}-{random.randint(10, 28)}T00:00:00Z",
            "skills": chosen_skills,
        })

    # 6. Phân công nhân viên vào các dự án (bao gồm cả tham gia chéo phòng ban!)
    # Đặc biệt: PRJ15 chỉ có đúng 2 nhân sự chủ chốt (emp2 và emp9) để minh họa truy vấn phát hiện dự án rủi ro cao (Bus Factor <= 2)
    emp_projects = {e["uid"]: [] for e in core_employees}
    project_members = {p["uid"]: [] for p in projects}

    for p in projects:
        lead_u = p["lead"]
        project_members[p["uid"]].append((lead_u, "Project Lead", 25))
        emp_projects[lead_u].append((p["uid"], "Project Lead", 25))

    # Gán thành viên cho PRJ01..PRJ14 (mỗi dự án 6-12 thành viên từ nhiều phòng ban)
    # Riêng PRJ15 chỉ có đúng 2 người (emp2 và emp9) để làm điểm nhấn phân tích rủi ro Bus Factor
    project_members["_:proj15"].append(("_:emp9", "Core Architect", 20))
    emp_projects["_:emp9"].append(("_:proj15", "Core Architect", 20))

    # Đảm bảo emp2 (Nguyễn Phạm Duy Luân) và emp3 (Đỗ Văn Minh) cùng tham gia PRJ01 & PRJ02 (cầu nối liên phòng ban)
    project_members["_:proj1"].append(("_:emp3", "AI Co-Lead", 15))
    emp_projects["_:emp3"].append(("_:proj1", "AI Co-Lead", 15))
    project_members["_:proj2"].append(("_:emp2", "Graph Architect", 15))
    emp_projects["_:emp2"].append(("_:proj2", "Graph Architect", 15))

    for p in projects:
        if p["uid"] == "_:proj15":
            continue
        p_dept = p["dept"]
        same_dept_emps = [e["uid"] for e in core_employees if e["dept"] == p_dept and e["uid"] != p["lead"]]
        other_dept_emps = [e["uid"] for e in core_employees if e["dept"] != p_dept and e["uid"] not in ("_:emp1", p["lead"])]
        picked_same = random.sample(same_dept_emps, k=min(4, len(same_dept_emps)))
        picked_cross = random.sample(other_dept_emps, k=min(3, len(other_dept_emps)))
        for eu in picked_same + picked_cross:
            if all(existing_u != eu for existing_u, _, _ in project_members[p["uid"]]):
                hrs = random.choice([10, 15, 20, 25])
                role_label = "Cross-Dept Specialist" if eu in picked_cross else "Core Member"
                project_members[p["uid"]].append((eu, role_label, hrs))
                emp_projects[eu].append((p["uid"], role_label, hrs))

    # Đảm bảo mọi nhân viên đều tham gia ít nhất 1 dự án
    for e in core_employees:
        if not emp_projects[e["uid"]]:
            target_p = random.choice(projects[:-1])["uid"]
            project_members[target_p].append((e["uid"], "Member", 15))
            emp_projects[e["uid"]].append((target_p, "Member", 15))

    # 7. Xây dựng mạng lưới cộng tác (collaborated_with) từ các dự án chung + cầu nối chiến lược
    collab_pairs = {}
    for p_uid, members in project_members.items():
        uids = [m[0] for m in members]
        for i in range(len(uids)):
            for j in range(i + 1, min(i + 4, len(uids))):
                u1, u2 = sorted([uids[i], uids[j]])
                pair = (u1, u2)
                collab_pairs[pair] = collab_pairs.get(pair, 0) + 1

    # 8. Tài khoản đăng nhập ứng dụng (AppUser)
    app_users = [
        {"uid": "_:user1", "username": "admin", "password_hash": "admin123", "full_name": "Nguyễn Phạm Duy Luân (Admin)", "user_role": "admin", "linked_employee": "_:emp2"},
        {"uid": "_:user2", "username": "manager", "password_hash": "manager123", "full_name": "Đỗ Văn Minh (Manager)", "user_role": "manager", "linked_employee": "_:emp3"},
        {"uid": "_:user3", "username": "employee", "password_hash": "emp123", "full_name": "Nguyễn Thị Minh Khai (Employee)", "user_role": "employee", "linked_employee": "_:emp15"},
    ]

    return departments, skills, roles, projects, core_employees, emp_projects, collab_pairs, app_users


def generate_rdf_and_json():
    departments, skills, roles, projects, employees, emp_projects, collab_pairs, app_users = build_dataset()
    rdf_lines = []

    def add_quad(s, p, o_val, is_uid=False, facets=None):
        facet_str = ""
        if facets:
            parts = []
            for fk, fv in facets.items():
                if isinstance(fv, bool):
                    parts.append(f"{fk}={'true' if fv else 'false'}")
                elif isinstance(fv, str):
                    parts.append(f'{fk}="{fv}"')
                else:
                    parts.append(f"{fk}={fv}")
            facet_str = " (" + ", ".join(parts) + ")"
        if is_uid:
            rdf_lines.append(f"<{s}> <{p}> <{o_val}>{facet_str} .")
        else:
            escaped = str(o_val).replace('\\', '\\\\').replace('"', '\\"')
            rdf_lines.append(f'<{s}> <{p}> "{escaped}"{facet_str} .')

    # Departments
    for d in departments:
        u = d["uid"]
        add_quad(u, "dgraph.type", "Department")
        add_quad(u, "dept_code", d["dept_code"])
        add_quad(u, "dept_name", d["dept_name"])
        add_quad(u, "location", d["location"])
        add_quad(u, "budget", d["budget"])
        add_quad(u, "established_year", d["established_year"])
        add_quad(u, "managed_by", d["mgr_emp"], is_uid=True)

    # Skills
    for sk in skills:
        u = sk["uid"]
        add_quad(u, "dgraph.type", "Skill")
        add_quad(u, "skill_code", sk["skill_code"])
        add_quad(u, "skill_name", sk["skill_name"])
        add_quad(u, "skill_category", sk["skill_category"])

    # Roles
    for r in roles:
        u = r["uid"]
        add_quad(u, "dgraph.type", "Role")
        add_quad(u, "role_code", r["role_code"])
        add_quad(u, "role_name", r["role_name"])
        for perm in r["permissions"]:
            add_quad(u, "permissions", perm)

    # Projects
    for p in projects:
        u = p["uid"]
        add_quad(u, "dgraph.type", "Project")
        add_quad(u, "proj_code", p["proj_code"])
        add_quad(u, "proj_name", p["proj_name"])
        add_quad(u, "proj_status", p["proj_status"])
        add_quad(u, "priority", p["priority"])
        add_quad(u, "proj_budget", p["proj_budget"])
        add_quad(u, "start_date", p["start_date"])
        add_quad(u, "end_date", p["end_date"])
        add_quad(u, "owned_by_dept", p["dept"], is_uid=True)
        add_quad(u, "led_by", p["lead"], is_uid=True)
        for sk_uid in p["req_skills"]:
            add_quad(u, "requires_skill", sk_uid, is_uid=True, facets={"mandatory": True})
        for dep_proj in p["depends"]:
            add_quad(u, "depends_on_project", dep_proj, is_uid=True)

    # Employees
    for idx, e in enumerate(employees, start=1):
        u = e["uid"]
        add_quad(u, "dgraph.type", "Employee")
        add_quad(u, "emp_code", e["emp_code"])
        add_quad(u, "full_name", e["full_name"])
        add_quad(u, "email", f"{e['emp_code'].lower()}@enterprise-graph.vn")
        add_quad(u, "phone", f"09{idx:02d}{100000 + idx * 137:06d}"[:10])
        add_quad(u, "title", e["title"])
        add_quad(u, "level", e["level"])
        add_quad(u, "hire_date", e["hire_date"])
        add_quad(u, "salary", e["salary"])
        add_quad(u, "status", "Active")
        add_quad(u, "belongs_to_dept", e["dept"], is_uid=True)
        add_quad(u, "has_role", e["role"], is_uid=True)
        if e["reports_to"]:
            add_quad(u, "reports_to", e["reports_to"], is_uid=True)
        for sk_i, sk_uid in enumerate(e["skills"]):
            prof = 5 if e["level"] <= 3 else (4 if sk_i == 0 else 3)
            add_quad(u, "has_skill", sk_uid, is_uid=True, facets={"proficiency": prof, "years": max(1, 7 - e["level"])})
        for proj_uid, role_in_proj, hrs in emp_projects[u]:
            add_quad(u, "works_on", proj_uid, is_uid=True, facets={"role_in_project": role_in_proj, "hours_per_week": hrs})

    # Collaborations (symmetric edges for shortest path & cross-dept bridge analysis)
    for (u1, u2), shared_cnt in collab_pairs.items():
        score = min(10, 5 + shared_cnt * 2)
        add_quad(u1, "collaborated_with", u2, is_uid=True, facets={"projects_together": shared_cnt, "trust_score": score})
        add_quad(u2, "collaborated_with", u1, is_uid=True, facets={"projects_together": shared_cnt, "trust_score": score})

    # AppUsers
    for au in app_users:
        u = au["uid"]
        add_quad(u, "dgraph.type", "AppUser")
        add_quad(u, "username", au["username"])
        add_quad(u, "password_hash", au["password_hash"])
        add_quad(u, "full_name", au["full_name"])
        add_quad(u, "user_role", au["user_role"])
        add_quad(u, "linked_employee", au["linked_employee"], is_uid=True)

    with open(RDF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(rdf_lines) + "\n")

    # Đồng thời xuất file JSON Mutation tương đương để minh họa nạp JSON
    json_export = {
        "departments_count": len(departments),
        "skills_count": len(skills),
        "roles_count": len(roles),
        "projects_count": len(projects),
        "employees_count": len(employees),
        "app_users_count": len(app_users),
        "rdf_triples_count": len(rdf_lines),
        "sample_departments": departments[:3],
        "sample_employees": employees[:5],
    }
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(json_export, f, ensure_ascii=False, indent=2)

    return len(rdf_lines), len(employees), len(departments), len(projects), len(skills)


def post_to_dgraph(path, data_bytes, content_type):
    url = f"{DGRAPH_ALPHA_URL}{path}"
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": content_type}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def seed_database():
    print("1. Sinh file dữ liệu mẫu RDF và JSON...")
    triples_cnt, emp_cnt, dept_cnt, proj_cnt, sk_cnt = generate_rdf_and_json()
    print(f"   -> Đã tạo {RDF_PATH} ({triples_cnt} dòng N-Quads RDF)")
    print(f"   -> Đã tạo {JSON_PATH} ({emp_cnt} Nhân viên, {dept_cnt} Phòng ban, {proj_cnt} Dự án, {sk_cnt} Kỹ năng)")

    print("2. Xóa dữ liệu cũ (Drop Data) để đảm bảo CSDL sạch và không trùng lặp...")
    drop_res = post_to_dgraph("/alter", b'{"drop_op": "DATA"}', "application/json")
    print("   -> Kết quả Drop Data:", drop_res)

    print("3. Nạp Schema + Index từ database/schema.dql vào Dgraph Alpha...")
    with open(SCHEMA_PATH, "rb") as f:
        schema_bytes = f.read()
    alter_res = post_to_dgraph("/alter", schema_bytes, "application/octet-stream")
    print("   -> Kết quả Alter Schema:", alter_res)

    print("4. Thực thi Mutation nạp toàn bộ RDF vào Dgraph Alpha (/mutate?commitNow=true)...")
    with open(RDF_PATH, "r", encoding="utf-8") as f:
        raw_rdf = f.read()
    wrapped_rdf = "{\n  set {\n" + raw_rdf + "\n  }\n}"
    mutate_res = post_to_dgraph("/mutate?commitNow=true", wrapped_rdf.encode("utf-8"), "application/rdf")
    uids_created = len(mutate_res.get("data", {}).get("uids", {}))
    print(f"   -> Nạp thành công! Tổng số đỉnh (Nodes) được cấp phát UID: {uids_created}")


if __name__ == "__main__":
    seed_database()
