#!/usr/bin/env python3
"""
korean-persona-search/download.py

nvidia/Nemotron-Personas-Korea Parquet shard를 로컬 캐시로 다운로드한다.
최초 실행 시 전체 shard, 이후 실행은 캐시 hit이면 no-op.

캐시 경로:
  KOREAN_PERSONA_CACHE_DIR 환경변수, 미설정 시 ~/.cache/korean-persona-search/

사용법:
  python download.py                # 전체 다운로드
  python download.py --shards 1     # 첫 N개 shard만 (개발/테스트)
  python download.py --check        # 다운로드 없이 캐시 상태만 보고
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


REPO_ID = "nvidia/Nemotron-Personas-Korea"
DEFAULT_CACHE = Path.home() / ".cache" / "korean-persona-search"


def cache_dir() -> Path:
    return Path(os.environ.get("KOREAN_PERSONA_CACHE_DIR", DEFAULT_CACHE))


def check_deps() -> None:
    missing = []
    try:
        import huggingface_hub  # noqa: F401
    except ImportError:
        missing.append("huggingface_hub")
    try:
        import pyarrow  # noqa: F401
    except ImportError:
        missing.append("pyarrow")
    if missing:
        sys.stderr.write(
            "[korean-persona-search] 누락된 의존성: "
            + ", ".join(missing)
            + "\n  pip install " + " ".join(missing)
            + "\n  (또는) uv pip install " + " ".join(missing) + "\n"
        )
        sys.exit(2)


def list_parquet_files() -> list[str]:
    from huggingface_hub import HfApi
    api = HfApi()
    files = api.list_repo_files(REPO_ID, repo_type="dataset")
    parquet = sorted(f for f in files if f.endswith(".parquet"))
    return parquet


def report_status() -> None:
    target = cache_dir()
    if not target.exists():
        print(f"[status] 캐시 없음: {target}")
        return
    files = sorted(target.rglob("*.parquet"))
    total_bytes = sum(f.stat().st_size for f in files)
    print(f"[status] 캐시 경로: {target}")
    print(f"[status] parquet 파일 수: {len(files)}")
    print(f"[status] 총 크기: {total_bytes / 1e9:.2f} GB")
    if files:
        print(f"[status] 예시: {files[0].name}")


def download(shards: int | None) -> None:
    from huggingface_hub import snapshot_download

    target = cache_dir()
    target.mkdir(parents=True, exist_ok=True)

    parquet_files = list_parquet_files()
    if not parquet_files:
        sys.stderr.write("[error] parquet 파일을 찾지 못했습니다.\n")
        sys.exit(1)

    if shards is not None and shards > 0:
        selected = parquet_files[:shards]
        print(f"[download] {len(selected)}/{len(parquet_files)} shard만 받습니다 (--shards={shards})")
    else:
        selected = parquet_files
        print(f"[download] 전체 {len(selected)}개 shard 받습니다 (수 GB 소요)")

    snapshot_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        local_dir=str(target),
        allow_patterns=selected,
    )
    print(f"[done] 캐시 위치: {target}")


def main() -> None:
    p = argparse.ArgumentParser(description="Nemotron-Personas-Korea 캐시 다운로더")
    p.add_argument("--shards", type=int, default=None, help="첫 N개 shard만 받기 (테스트용)")
    p.add_argument("--check", action="store_true", help="캐시 상태만 보고 (다운로드 없음)")
    args = p.parse_args()

    check_deps()

    if args.check:
        report_status()
        return

    download(args.shards)
    report_status()


if __name__ == "__main__":
    main()
