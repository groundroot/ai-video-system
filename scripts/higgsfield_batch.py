#!/usr/bin/env python3
"""
Higgsfield 배치 이미지 생성기
hanroro_0plus0 이미지 프롬프트 42개를 GPT Image 2로 순차 제출 + 병렬 대기
출력: assets/characters/shot_XX_v1.png
"""

import asyncio
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_FILE = BASE_DIR / "02_preproduction" / "image_prompts" / "hanroro_0plus0_image_prompts.md"
OUTPUT_DIR = BASE_DIR / "assets" / "characters"
MODEL = "imagegen_2_0"
ASPECT_RATIO = "16:9"
SUBMIT_DELAY = 3      # 제출 사이 대기(초) — rate limit 회피
MAX_WAIT_CONCURRENT = 8  # 동시 wait 최대 수


def parse_shots(filepath: Path) -> list[tuple[int, str]]:
    content = filepath.read_text(encoding="utf-8")
    pattern = re.compile(r"###\s+Shot\s+(\d+)[^\n]*\n.*?```\n(.*?)```", re.DOTALL)
    shots = [(int(m.group(1)), m.group(2).strip()) for m in pattern.finditer(content)]
    return sorted(shots, key=lambda x: x[0])


def output_path(shot_num: int) -> Path:
    return OUTPUT_DIR / f"shot_{shot_num:02d}_v1.png"


async def run_cmd(*args) -> tuple[int, str, str]:
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout.decode(), stderr.decode()


async def submit_shot(shot_num: int, prompt: str) -> dict:
    """잡 제출 (--wait 없음). 재시도 포함."""
    for attempt in range(5):
        rc, out, err = await run_cmd(
            "higgsfield", "generate", "create", MODEL,
            "--prompt", prompt,
            "--aspect_ratio", ASPECT_RATIO,
            "--json",
        )
        if rc != 0:
            try:
                err_data = json.loads(err.replace("Error: ", "", 1))
                if err_data.get("error_type") == "rate_limit_reached":
                    wait = 30 * (attempt + 1)
                    print(f"[Shot {shot_num:02d}] rate_limit — {wait}초 대기 후 재시도...")
                    await asyncio.sleep(wait)
                    continue
            except Exception:
                pass
            print(f"[Shot {shot_num:02d}] 제출 실패: {err.strip()}")
            return {"shot": shot_num, "status": "error", "error": err.strip()}

        data = json.loads(out)
        # CLI는 job_id 리스트 반환: ["uuid"]
        job_id = data[0] if isinstance(data, list) else data.get("id")
        if not job_id:
            return {"shot": shot_num, "status": "error", "error": f"job_id 없음: {data}"}

        print(f"[Shot {shot_num:02d}] 제출 완료 → {job_id}")
        return {"shot": shot_num, "status": "submitted", "job_id": job_id}

    return {"shot": shot_num, "status": "error", "error": "재시도 초과"}


async def wait_and_download(sem: asyncio.Semaphore, shot_num: int, job_id: str) -> dict:
    out_path = output_path(shot_num)
    async with sem:
        print(f"[Shot {shot_num:02d}] 대기 중...")
        rc, out, err = await run_cmd(
            "higgsfield", "generate", "wait", job_id, "--json"
        )
        if rc != 0:
            print(f"[Shot {shot_num:02d}] wait 실패: {err.strip()}")
            return {"shot": shot_num, "status": "error", "error": err.strip()}

        data = json.loads(out)
        job = data[0] if isinstance(data, list) else data
        result_url = job.get("result_url")
        if not result_url:
            return {"shot": shot_num, "status": "error", "error": f"result_url 없음: {job}"}

        urllib.request.urlretrieve(result_url, out_path)
        print(f"[Shot {shot_num:02d}] 저장 완료 → {out_path.name}")
        return {"shot": shot_num, "status": "ok", "path": str(out_path)}


async def main():
    shots = parse_shots(PROMPTS_FILE)
    if not shots:
        print("프롬프트를 찾을 수 없습니다.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 이미 생성된 샷 제외
    pending = [(n, p) for n, p in shots if not output_path(n).exists()]
    skipped_count = len(shots) - len(pending)
    if skipped_count:
        print(f"{skipped_count}개 이미 존재 → 스킵")
    print(f"{len(pending)}개 Shot 생성 시작 (제출 간격: {SUBMIT_DELAY}초)")

    # Phase 1: 순차 제출
    submitted = []
    for i, (num, prompt) in enumerate(pending):
        result = await submit_shot(num, prompt)
        submitted.append(result)
        if i < len(pending) - 1:
            await asyncio.sleep(SUBMIT_DELAY)

    ok_submitted = [r for r in submitted if r["status"] == "submitted"]
    failed_submit = [r for r in submitted if r["status"] == "error"]
    print(f"\n제출 완료: {len(ok_submitted)}개 / 실패: {len(failed_submit)}개")

    # Phase 2: 병렬 대기 + 다운로드
    sem = asyncio.Semaphore(MAX_WAIT_CONCURRENT)
    wait_tasks = [
        wait_and_download(sem, r["shot"], r["job_id"])
        for r in ok_submitted
    ]
    results = await asyncio.gather(*wait_tasks)

    ok = [r for r in results if r["status"] == "ok"]
    errors = [r for r in results if r["status"] == "error"] + failed_submit

    print(f"\n=== 완료 ===")
    print(f"성공: {len(ok)}개 / 스킵: {skipped_count}개 / 실패: {len(errors)}개")
    if errors:
        for e in errors:
            print(f"  [Shot {e['shot']:02d}] {e.get('error', '')}")


if __name__ == "__main__":
    asyncio.run(main())
