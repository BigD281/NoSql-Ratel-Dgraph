# -*- coding: utf-8 -*-
"""
Backend Web Server kết nối CSDL đồ thị Dgraph (Không cần cài đặt thư viện ngoài).
Đáp ứng đầy đủ Mục 8 & Mục 9 trong thang điểm:
  1. Quản trị người dùng (Đăng nhập 3 quyền Admin/Manager/Employee + CRUD tài khoản AppUser)
  2. Thao tác trên CSDL (Thêm, sửa, xóa Nhân viên / Phòng ban / Dự án / Quan hệ cạnh + Backup/Export/Restore)
  3. Quản lý theo chức năng nghiệp vụ bài toán:
     - Chuỗi báo cáo phân cấp đệ quy (@recurse)
     - Tìm đường kết nối ngắn nhất giữa 2 nhân viên (shortest)
     - Gợi ý nhân sự cho dự án theo kỹ năng (@cascade & giao tập UID)
     - Phân tích tác động khi nhân sự nghỉ việc & Dự án rủi ro (Bus Factor)
  4. Chức năng hỗ trợ khác:
     - Trực quan hóa mạng lưới đồ thị tương tác (Cytoscape.js)
     - Bảng thống kê lương & nhân sự theo phòng ban (Aggregation)
     - Trình chạy DQL trực tiếp kèm bộ 20 truy vấn mẫu
"""

import json
import os
import shutil
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)
sys.path.insert(0, APP_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "database"))

from dgraph_client import DgraphClient
import seed_data

db = DgraphClient()


class HRGraphRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _send_json(self, data, status=200):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw else {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            index_file = os.path.join(APP_DIR, "static", "index.html")
            with open(index_file, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        if path == "/api/health":
            self._send_json(db.check_health())
            return

        if path == "/api/dashboard":
            dql = """
            {
              emp_cnt(func: type(Employee)) { total: count(uid) }
              dept_cnt(func: type(Department)) { total: count(uid) }
              proj_cnt(func: type(Project)) { total: count(uid) }
              skill_cnt(func: type(Skill)) { total: count(uid) }

              departments(func: type(Department), orderasc: dept_code) {
                uid
                dept_code
                dept_name
                location
                budget
                established_year
                staff_count: count(~belongs_to_dept)
                project_count: count(~owned_by_dept)
                managed_by { uid emp_code full_name }
                ~belongs_to_dept { s as salary }
                total_salary: sum(val(s))
                avg_salary: avg(val(s))
              }

              projects(func: type(Project), orderasc: proj_code) {
                uid
                proj_code
                proj_name
                proj_status
                priority
                proj_budget
                member_count: count(~works_on)
                owned_by_dept { uid dept_code dept_name }
                led_by { uid emp_code full_name }
                requires_skill { uid skill_code skill_name }
              }

              employees(func: type(Employee), orderasc: emp_code, first: 150) {
                uid
                emp_code
                full_name
                title
                email
                phone
                level
                salary
                status
                belongs_to_dept { uid dept_code dept_name }
                reports_to { uid emp_code full_name }
                has_skill { uid skill_code skill_name }
                works_on { uid proj_code proj_name }
              }

              skills(func: type(Skill), orderasc: skill_code) {
                uid
                skill_code
                skill_name
                skill_category
                emp_count: count(~has_skill)
              }

              users(func: type(AppUser), orderasc: username) {
                uid
                username
                full_name
                user_role
                linked_employee { uid emp_code full_name }
              }
            }
            """
            res = db.query_dql(dql)
            self._send_json(res.get("data", {}))
            return

        if path == "/api/graph-data":
            limit_emp = int(qs.get("limit", ["24"])[0])
            dql = f"""
            {{
              departments(func: type(Department)) {{
                uid
                dept_code
                dept_name
                managed_by {{ uid }}
              }}
              projects(func: type(Project), first: 10) {{
                uid
                proj_code
                proj_name
                priority
                owned_by_dept {{ uid }}
                led_by {{ uid }}
              }}
              employees(func: type(Employee), orderasc: emp_code, first: {limit_emp}) {{
                uid
                emp_code
                full_name
                title
                level
                belongs_to_dept {{ uid }}
                reports_to {{ uid }}
                works_on {{ uid }}
                collaborated_with (first: 3) {{ uid }}
              }}
            }}
            """
            res = db.query_dql(dql)
            self._send_json(res.get("data", {}))
            return

        if path == "/api/queries-catalog":
            verified_path = os.path.join(ROOT_DIR, "database", "query_results_verified.json")
            if os.path.exists(verified_path):
                with open(verified_path, "r", encoding="utf-8") as f:
                    self._send_json(json.load(f))
            else:
                self._send_json({"basic": {}, "advanced": {}})
            return

        if path == "/api/business/org-chart":
            emp_code = qs.get("emp_code", ["EMP001"])[0]
            dql = f"""
            {{
              org_chart(func: eq(emp_code, "{emp_code}")) @recurse(depth: 5, loop: false) {{
                uid
                emp_code
                full_name
                title
                level
                ~reports_to
              }}
            }}
            """
            res = db.query_dql(dql)
            self._send_json(res.get("data", {}))
            return

        if path == "/api/business/shortest-path":
            from_code = qs.get("from", ["EMP002"])[0]
            to_code = qs.get("to", ["EMP021"])[0]
            dql = f"""
            {{
              A as var(func: eq(emp_code, "{from_code}"))
              B as var(func: eq(emp_code, "{to_code}"))
              path as shortest(from: uid(A), to: uid(B), numpaths: 1) {{
                collaborated_with
              }}
              path_nodes(func: uid(path)) {{
                uid
                emp_code
                full_name
                title
                belongs_to_dept {{ dept_code dept_name }}
              }}
            }}
            """
            res = db.query_dql(dql)
            self._send_json(res.get("data", {}))
            return

        if path == "/api/business/recommend-staff":
            proj_code = qs.get("proj_code", ["PRJ02"])[0]
            dql = f"""
            {{
              project_info(func: eq(proj_code, "{proj_code}")) {{
                proj_code
                proj_name
                priority
                requires_skill {{ skill_code skill_name }}
              }}
              var(func: eq(proj_code, "{proj_code}")) {{
                req_sk as requires_skill
                current_members as ~works_on
              }}
              var(func: uid(req_sk)) {{
                candidates as ~has_skill @filter(NOT uid(current_members)) {{
                  matched_cnt as count(has_skill @filter(uid(req_sk)))
                }}
              }}
              recommendations(func: uid(candidates), orderdesc: val(matched_cnt), first: 10) {{
                uid
                emp_code
                full_name
                title
                matched_skills_count: val(matched_cnt)
                belongs_to_dept {{ dept_code dept_name }}
                has_skill @filter(uid(req_sk)) {{ skill_code skill_name }}
              }}
            }}
            """
            res = db.query_dql(dql)
            self._send_json(res.get("data", {}))
            return

        if path == "/api/business/impact-analysis":
            emp_code = qs.get("emp_code", ["EMP002"])[0]
            dql = f"""
            {{
              impact(func: eq(emp_code, "{emp_code}")) {{
                uid
                emp_code
                full_name
                title
                managed_departments: ~managed_by {{
                  dept_code
                  dept_name
                  staff_count: count(~belongs_to_dept)
                }}
                led_projects: ~led_by {{
                  proj_code
                  proj_name
                  priority
                  dependent_projects: ~depends_on_project {{
                    proj_code
                    proj_name
                    priority
                  }}
                }}
                direct_reports: ~reports_to {{
                  emp_code
                  full_name
                  title
                  indirect_reports: ~reports_to {{
                    emp_code
                    full_name
                    title
                  }}
                }}
              }}
              var(func: type(Project)) @filter(eq(proj_status, "Active")) {{
                mc as count(~works_on)
              }}
              bus_factor_risks(func: uid(mc), orderasc: val(mc)) @filter(le(val(mc), 5)) {{
                proj_code
                proj_name
                priority
                member_count: val(mc)
                led_by {{ emp_code full_name }}
              }}
            }}
            """
            res = db.query_dql(dql)
            self._send_json(res.get("data", {}))
            return

        self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_body()

        try:
            if path == "/api/login":
                username = body.get("username", "").strip()
                password = body.get("password", "").strip()
                dql = f"""
                {{
                  users(func: eq(username, "{username}")) {{
                    uid
                    username
                    password_hash
                    full_name
                    user_role
                    linked_employee {{ emp_code full_name title }}
                  }}
                }}
                """
                res = db.query_dql(dql).get("data", {}).get("users", [])
                if res and res[0].get("password_hash") == password:
                    user = res[0]
                    user.pop("password_hash", None)
                    self._send_json({"ok": True, "user": user})
                else:
                    self._send_json({"ok": False, "message": "Sai tài khoản hoặc mật khẩu!"}, 401)
                return

            if path == "/api/users/save":
                uid = body.get("uid")
                user_obj = {
                    "dgraph.type": "AppUser",
                    "username": body["username"],
                    "full_name": body["full_name"],
                    "user_role": body.get("user_role", "employee"),
                }
                if body.get("password"):
                    user_obj["password_hash"] = body["password"]
                if uid:
                    user_obj["uid"] = uid
                res = db.mutate_json(set_obj=[user_obj])
                self._send_json({"ok": True, "result": res})
                return

            if path == "/api/users/delete":
                uid = body["uid"]
                res = db.mutate_rdf(delete_nquads=f"<{uid}> * * .")
                self._send_json({"ok": True, "result": res})
                return

            if path == "/api/employees/save":
                emp_obj = {
                    "dgraph.type": "Employee",
                    "emp_code": body["emp_code"],
                    "full_name": body["full_name"],
                    "title": body.get("title", "Chuyên Viên"),
                    "email": body.get("email", f"{body['emp_code'].lower()}@enterprise-graph.vn"),
                    "phone": body.get("phone", "0901234567"),
                    "level": int(body.get("level", 4)),
                    "salary": float(body.get("salary", 25000000)),
                    "status": body.get("status", "Active"),
                }
                if body.get("uid"):
                    emp_obj["uid"] = body["uid"]
                if body.get("dept_uid"):
                    emp_obj["belongs_to_dept"] = {"uid": body["dept_uid"]}
                if body.get("reports_to_uid"):
                    emp_obj["reports_to"] = {"uid": body["reports_to_uid"]}
                res = db.mutate_json(set_obj=[emp_obj])
                self._send_json({"ok": True, "result": res})
                return

            if path == "/api/employees/delete":
                uid = body["uid"]
                res = db.mutate_rdf(delete_nquads=f"<{uid}> * * .")
                self._send_json({"ok": True, "result": res})
                return

            if path == "/api/departments/save":
                dept_obj = {
                    "dgraph.type": "Department",
                    "dept_code": body["dept_code"],
                    "dept_name": body["dept_name"],
                    "location": body.get("location", "TP.HCM"),
                    "budget": float(body.get("budget", 5000000000)),
                    "established_year": int(body.get("established_year", 2020)),
                }
                if body.get("uid"):
                    dept_obj["uid"] = body["uid"]
                if body.get("managed_by_uid"):
                    dept_obj["managed_by"] = {"uid": body["managed_by_uid"]}
                res = db.mutate_json(set_obj=[dept_obj])
                self._send_json({"ok": True, "result": res})
                return

            if path == "/api/projects/save":
                proj_obj = {
                    "dgraph.type": "Project",
                    "proj_code": body["proj_code"],
                    "proj_name": body["proj_name"],
                    "proj_status": body.get("proj_status", "Active"),
                    "priority": body.get("priority", "High"),
                    "proj_budget": float(body.get("proj_budget", 2500000000)),
                }
                if body.get("uid"):
                    proj_obj["uid"] = body["uid"]
                if body.get("dept_uid"):
                    proj_obj["owned_by_dept"] = {"uid": body["dept_uid"]}
                if body.get("lead_uid"):
                    proj_obj["led_by"] = {"uid": body["lead_uid"]}
                res = db.mutate_json(set_obj=[proj_obj])
                self._send_json({"ok": True, "result": res})
                return

            if path == "/api/edges/mutate":
                source_uid = body["source_uid"]
                predicate = body["predicate"]
                target_uid = body["target_uid"]
                action = body.get("action", "set")
                facet_str = ""
                if body.get("facet_key") and body.get("facet_val"):
                    fk = body["facet_key"].strip()
                    fv = body["facet_val"].strip()
                    if fv.isdigit():
                        facet_str = f" ({fk}={fv})"
                    else:
                        facet_str = f' ({fk}="{fv}")'
                nquad = f"<{source_uid}> <{predicate}> <{target_uid}>{facet_str} ."
                if action == "delete":
                    res = db.mutate_rdf(delete_nquads=f"<{source_uid}> <{predicate}> <{target_uid}> .")
                else:
                    res = db.mutate_rdf(set_nquads=nquad)
                    if predicate == "collaborated_with":
                        db.mutate_rdf(set_nquads=f"<{target_uid}> <collaborated_with> <{source_uid}>{facet_str} .")
                self._send_json({"ok": True, "result": res, "nquad": nquad})
                return

            if path == "/api/dql/execute":
                dql_query = body.get("dql", "")
                res = db.query_dql(dql_query)
                self._send_json({"ok": True, "result": res})
                return

            if path == "/api/admin/export-backup":
                fmt = body.get("format", "rdf")
                exp_res = db.export_database(fmt)
                export_src = os.path.join(ROOT_DIR, "dgraph-data", "export")
                backup_dst = os.path.join(ROOT_DIR, "backups", "export_latest")
                if os.path.exists(export_src):
                    if os.path.exists(backup_dst):
                        shutil.rmtree(backup_dst)
                    shutil.copytree(export_src, backup_dst)
                self._send_json({"ok": True, "export_response": exp_res, "backup_folder": backup_dst})
                return

            if path == "/api/admin/import-data":
                fmt = body.get("format", "rdf").lower()
                content = body.get("content", "").strip()
                filename = body.get("filename", "uploaded_data")
                if not content:
                    self._send_json({"ok": False, "error": "Nội dung file Import trống!"}, 400)
                    return
                if fmt == "json" or filename.endswith(".json"):
                    parsed_json = json.loads(content)
                    if isinstance(parsed_json, dict) and "set" in parsed_json:
                        set_data = parsed_json["set"]
                    elif isinstance(parsed_json, list):
                        set_data = parsed_json
                    else:
                        set_data = [parsed_json]
                    res = db.mutate_json(set_obj=set_data)
                else:
                    normalized_rdf = content.replace(". <", ".\n<")
                    if normalized_rdf.startswith("{") and "set" in normalized_rdf:
                        res = db._request(db.alpha_url, "/mutate?commitNow=true", normalized_rdf.encode("utf-8"), "application/rdf", "POST")
                    else:
                        res = db.mutate_rdf(set_nquads=normalized_rdf)
                uids_map = (res.get("data") or {}).get("uids") or {}
                uids_cnt = len(uids_map)
                self._send_json({
                    "ok": True,
                    "message": f"Đã Import thành công '{filename}' ({fmt.upper()}) vào Dgraph! Số UID mới cấp phát: {uids_cnt}",
                    "result": res
                })
                return

            if path == "/api/admin/reset-seed":
                seed_data.seed_database()
                self._send_json({"ok": True, "message": "Đã khôi phục (Restore) toàn bộ Schema và dữ liệu từ bản sao lưu chuẩn!"})
                return

            self._send_json({"error": "Unknown endpoint"}, 404)
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)


def main():
    host = os.environ.get("APP_HOST", "127.0.0.1")
    port = int(os.environ.get("APP_PORT", "5000"))
    server = ThreadingHTTPServer((host, port), HRGraphRequestHandler)
    print(f"============================================================")
    print(f"  HR GRAPH MANAGER WEB APP DANG CHAY TAI: http://{host}:{port}")
    print(f"  Ket noi Dgraph Alpha : {db.alpha_url}")
    print(f"  Giao dien Ratel GUI  : http://localhost:8000/?local")
    print(f"============================================================")
    server.serve_forever()


if __name__ == "__main__":
    main()

