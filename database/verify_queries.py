# -*- coding: utf-8 -*-
"""
Script thực thi và kiểm chứng toàn bộ 10 Truy vấn Cơ bản (Q01-Q10)
và 10 Truy vấn Nâng cao (A01-A10) trực tiếp trên Dgraph Alpha (http://localhost:8080/query).
Lưu toàn bộ kết quả thực tế đã kiểm chứng vào database/query_results_verified.json.
"""

import json
import os
import re
import sys
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASIC_PATH = os.path.join(BASE_DIR, "queries_basic.dql")
ADV_PATH = os.path.join(BASE_DIR, "queries_advanced.dql")
OUT_PATH = os.path.join(BASE_DIR, "query_results_verified.json")
DGRAPH_URL = "http://localhost:8080/query"


def parse_dql_blocks(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    blocks = []
    pattern = re.compile(r"#\s*\[([QA]\d+)\]\s*(.+?)\n(?:#.*\n)*(\{[\s\S]+?\n\})", re.MULTILINE)
    for m in pattern.finditer(text):
        qid = m.group(1).strip()
        title = m.group(2).strip()
        dql = m.group(3).strip()
        blocks.append((qid, title, dql))
    return blocks


def run_dql(dql_query):
    req = urllib.request.Request(
        DGRAPH_URL,
        data=dql_query.encode("utf-8"),
        headers={"Content-Type": "application/dql"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    basic_blocks = parse_dql_blocks(BASIC_PATH)
    adv_blocks = parse_dql_blocks(ADV_PATH)
    all_results = {"basic": {}, "advanced": {}}

    print(f"=== KIỂM CHỨNG {len(basic_blocks)} TRUY VẤN CƠ BẢN ===")
    for qid, title, dql in basic_blocks:
        res = run_dql(dql)
        errors = res.get("errors")
        data = res.get("data", {})
        status = "ERROR" if errors else "OK"
        row_counts = {k: len(v) if isinstance(v, list) else 1 for k, v in data.items()}
        print(f"  [{qid}] {status} | {title} -> {row_counts}")
        if errors:
            print("     Lỗi:", errors)
        all_results["basic"][qid] = {
            "title": title,
            "dql": dql,
            "row_counts": row_counts,
            "sample_data": data,
        }

    print(f"\n=== KIỂM CHỨNG {len(adv_blocks)} TRUY VẤN NÂNG CAO ===")
    for qid, title, dql in adv_blocks:
        res = run_dql(dql)
        errors = res.get("errors")
        data = res.get("data", {})
        status = "ERROR" if errors else "OK"
        row_counts = {k: len(v) if isinstance(v, list) else 1 for k, v in data.items()}
        print(f"  [{qid}] {status} | {title} -> {row_counts}")
        if errors:
            print("     Lỗi:", errors)
        all_results["advanced"][qid] = {
            "title": title,
            "dql": dql,
            "row_counts": row_counts,
            "sample_data": data,
        }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n[HOÀN TẤT] Đã lưu toàn bộ kết quả thực thi thực tế tại: {OUT_PATH}")


if __name__ == "__main__":
    main()

