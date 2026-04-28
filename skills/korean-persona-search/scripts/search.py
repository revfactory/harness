#!/usr/bin/env python3
"""
korean-persona-search/search.py

캐싱된 Nemotron-Personas-Korea Parquet shard에서 다축 필터·다양성 샘플링으로
정규화된 퍼소나 카드 N개를 JSON으로 출력한다.

사용 예:
  python search.py --province 서울 --age-min 28 --age-max 38 \
      --occupation-contains 개발 --diversity sex,district --n 5

옵션은 references/filter-cookbook.md 참조.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from collections import defaultdict
from pathlib import Path


DEFAULT_CACHE = Path.home() / ".cache" / "korean-persona-search"

PERSONA_TEXT_FIELDS = [
    "persona",
    "professional_persona",
    "sports_persona",
    "arts_persona",
    "travel_persona",
    "culinary_persona",
    "family_persona",
]

PERSONA_TYPE_MAP = {
    "summary": "persona",
    "professional": "professional_persona",
    "sports": "sports_persona",
    "arts": "arts_persona",
    "travel": "travel_persona",
    "culinary": "culinary_persona",
    "family": "family_persona",
}


def cache_dir() -> Path:
    return Path(os.environ.get("KOREAN_PERSONA_CACHE_DIR", DEFAULT_CACHE))


def check_deps() -> None:
    try:
        import pyarrow  # noqa: F401
        import pyarrow.dataset  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "[korean-persona-search] 누락된 의존성: pyarrow\n"
            "  pip install pyarrow\n"
        )
        sys.exit(2)


def find_parquet_files(target: Path, shard_only: int | None) -> list[Path]:
    if not target.exists():
        sys.stderr.write(
            f"[error] 캐시 없음: {target}\n"
            "먼저 다운로드하세요:\n"
            "  python skills/korean-persona-search/scripts/download.py\n"
        )
        sys.exit(1)
    files = sorted(target.rglob("*.parquet"))
    if not files:
        sys.stderr.write(f"[error] {target} 안에 parquet 파일이 없습니다.\n")
        sys.exit(1)
    if shard_only and shard_only > 0:
        files = files[:shard_only]
    return files


def build_filter(args):
    import pyarrow.compute as pc

    expr = None

    def add(e):
        nonlocal expr
        expr = e if expr is None else expr & e

    if args.province:
        add(pc.field("province") == args.province)
    if args.district:
        add(pc.field("district") == args.district)
    if args.sex:
        add(pc.field("sex") == args.sex)
    if args.age_min is not None:
        add(pc.field("age") >= args.age_min)
    if args.age_max is not None:
        add(pc.field("age") <= args.age_max)
    if args.education_level:
        add(pc.field("education_level") == args.education_level)
    if args.bachelors_field:
        add(pc.field("bachelors_field") == args.bachelors_field)
    if args.marital_status:
        add(pc.field("marital_status") == args.marital_status)
    if args.family_type:
        add(pc.field("family_type") == args.family_type)
    if args.housing_type:
        add(pc.field("housing_type") == args.housing_type)
    if args.military_status:
        add(pc.field("military_status") == args.military_status)
    if args.occupation_contains:
        add(pc.match_substring(pc.field("occupation"), args.occupation_contains))

    return expr


def keyword_filter_table(table, keywords: list[str]):
    """Apply OR-substring filter across persona text fields."""
    import pyarrow.compute as pc

    if not keywords:
        return table
    mask = None
    for col in PERSONA_TEXT_FIELDS:
        if col not in table.column_names:
            continue
        col_data = table[col]
        for kw in keywords:
            m = pc.match_substring(col_data, kw)
            mask = m if mask is None else pc.or_(mask, m)
    if mask is None:
        return table
    return table.filter(mask)


def age_band(age) -> str:
    try:
        n = int(age)
    except (TypeError, ValueError):
        return "?"
    if n < 20:
        return "10대"
    return f"{(n // 10) * 10}대"


def occupation_root(occ: str | None) -> str:
    if not occ:
        return ""
    parts = re.split(r"[  /,(\[]", occ.strip(), maxsplit=1)
    return parts[0] if parts else occ


def diversity_keys(row: dict, keys: list[str]) -> tuple:
    out = []
    for k in keys:
        if k == "age_band":
            out.append(age_band(row.get("age")))
        elif k == "occupation_root":
            out.append(occupation_root(row.get("occupation")))
        else:
            out.append(str(row.get(k, "")))
    return tuple(out)


def diversity_sample(rows: list[dict], n: int, keys: list[str], seed: int) -> list[dict]:
    rng = random.Random(seed)
    if not keys:
        if len(rows) <= n:
            shuffled = list(rows)
            rng.shuffle(shuffled)
            return shuffled
        return rng.sample(rows, n)

    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        buckets[diversity_keys(row, keys)].append(row)

    for v in buckets.values():
        rng.shuffle(v)

    bucket_keys = list(buckets.keys())
    rng.shuffle(bucket_keys)

    picked: list[dict] = []
    while len(picked) < n and any(buckets.values()):
        for k in bucket_keys:
            if buckets[k]:
                picked.append(buckets[k].pop())
                if len(picked) >= n:
                    break
    return picked[:n]


def split_list(text: str | None) -> list[str]:
    if not text:
        return []
    parts = re.split(r"[,;·•\n]+", text)
    return [p.strip() for p in parts if p and p.strip()]


def normalize(row: dict, persona_types: list[str]) -> dict:
    personas_out: dict[str, str | None] = {}
    for ptype in persona_types:
        col = PERSONA_TYPE_MAP.get(ptype)
        if col and col in row:
            personas_out[ptype] = row[col]

    skills_src = row.get("skills_and_expertise_list") or row.get("skills_and_expertise") or ""
    hobbies_src = row.get("hobbies_and_interests_list") or row.get("hobbies_and_interests") or ""

    return {
        "uuid": row.get("uuid"),
        "demographics": {
            "sex": row.get("sex"),
            "age": row.get("age"),
            "marital_status": row.get("marital_status"),
            "military_status": row.get("military_status"),
            "education_level": row.get("education_level"),
            "bachelors_field": row.get("bachelors_field"),
            "occupation": row.get("occupation"),
            "province": row.get("province"),
            "district": row.get("district"),
            "family_type": row.get("family_type"),
            "housing_type": row.get("housing_type"),
        },
        "personas": personas_out,
        "context": {
            "cultural_background": row.get("cultural_background"),
            "skills_and_expertise": split_list(skills_src),
            "hobbies_and_interests": split_list(hobbies_src),
            "career_goals_and_ambitions": row.get("career_goals_and_ambitions"),
        },
        "_attribution": "NVIDIA Nemotron-Personas-Korea (CC BY 4.0)",
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Korean Persona 검색")
    p.add_argument("--province")
    p.add_argument("--district")
    p.add_argument("--sex", choices=["남자", "여자"])
    p.add_argument("--age-min", type=int)
    p.add_argument("--age-max", type=int)
    p.add_argument("--education-level")
    p.add_argument("--bachelors-field")
    p.add_argument("--marital-status")
    p.add_argument("--family-type")
    p.add_argument("--housing-type")
    p.add_argument("--military-status")
    p.add_argument("--occupation-contains")
    p.add_argument("--keywords", help="comma-separated substrings (OR over persona text)")

    p.add_argument("--n", type=int, default=5)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--diversity", help="comma-separated diversity keys")
    p.add_argument(
        "--persona-types",
        default="summary,professional",
        help="summary,professional,sports,arts,travel,culinary,family 중 콤마 구분",
    )
    p.add_argument("--shard-only", type=int, default=None, help="첫 N개 shard만 사용")
    p.add_argument("--out", help="JSON 저장 경로 (기본: stdout)")
    p.add_argument(
        "--limit-pre-sample",
        type=int,
        default=20000,
        help="필터 후 샘플링 전에 자르는 행 수 상한 (메모리 보호)",
    )
    args = p.parse_args()

    check_deps()

    import pyarrow.dataset as ds

    files = find_parquet_files(cache_dir(), args.shard_only)
    dataset = ds.dataset([str(f) for f in files], format="parquet")
    expr = build_filter(args)

    base_cols = [
        "uuid", "sex", "age", "marital_status", "military_status",
        "family_type", "housing_type", "education_level", "bachelors_field",
        "occupation", "district", "province",
        "cultural_background",
        "skills_and_expertise", "skills_and_expertise_list",
        "hobbies_and_interests", "hobbies_and_interests_list",
        "career_goals_and_ambitions",
    ] + PERSONA_TEXT_FIELDS

    avail = set(dataset.schema.names)
    project_cols = [c for c in base_cols if c in avail]

    table = dataset.to_table(columns=project_cols, filter=expr)

    if args.keywords:
        kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        table = keyword_filter_table(table, kws)

    if table.num_rows > args.limit_pre_sample:
        rng = random.Random(args.seed)
        idx = sorted(rng.sample(range(table.num_rows), args.limit_pre_sample))
        table = table.take(idx)

    rows = table.to_pylist()
    if not rows:
        sys.stderr.write("[warn] 결과 0건. 필터를 완화하세요.\n")
        print("[]")
        return

    diversity = [k.strip() for k in (args.diversity or "").split(",") if k.strip()]
    picked = diversity_sample(rows, args.n, diversity, args.seed)

    persona_types = [t.strip() for t in args.persona_types.split(",") if t.strip()]
    invalid = [t for t in persona_types if t not in PERSONA_TYPE_MAP]
    if invalid:
        sys.stderr.write(f"[error] 알 수 없는 persona-type: {invalid}\n")
        sys.exit(2)

    cards = [normalize(r, persona_types) for r in picked]
    out_json = json.dumps(cards, ensure_ascii=False, indent=2)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_json, encoding="utf-8")
        sys.stderr.write(f"[saved] {out_path} ({len(cards)} cards)\n")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
