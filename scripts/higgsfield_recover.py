#!/usr/bin/env python3
"""
이미 완료된 Higgsfield 잡을 Shot에 매칭해 다운로드하고,
미완성 Shot을 순차 제출 후 대기·저장한다.
"""

import asyncio
import json
import re
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_FILE = BASE_DIR / "02_preproduction" / "image_prompts" / "hanroro_0plus0_image_prompts.md"
OUTPUT_DIR = BASE_DIR / "assets" / "characters"
MODEL = "imagegen_2_0"
ASPECT_RATIO = "16:9"
SUBMIT_DELAY = 4
MAX_WAIT_CONCURRENT = 8


def parse_shots(filepath: Path) -> list[tuple[int, str]]:
    content = filepath.read_text(encoding="utf-8")
    pattern = re.compile(r"###\s+Shot\s+(\d+)[^\n]*\n.*?```\n(.*?)```", re.DOTALL)
    return sorted(
        [(int(m.group(1)), m.group(2).strip()) for m in pattern.finditer(content)],
        key=lambda x: x[0],
    )


def output_path(shot_num: int) -> Path:
    return OUTPUT_DIR / f"shot_{shot_num:02d}_v1.png"


async def run_cmd(*args) -> tuple[int, str, str]:
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    return proc.returncode, out.decode(), err.decode()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


async def fetch_existing_jobs() -> list[dict]:
    rc, out, _ = await run_cmd("higgsfield", "generate", "list", "--json")
    if rc != 0:
        return []
    return json.loads(out)


async def match_and_download(shots: list[tuple[int, str]]) -> list[int]:
    """기존 완료 잡과 Shot 프롬프트를 매칭, 다운로드. 성공한 shot 번호 반환."""
    jobs = await fetch_existing_jobs()
    completed = [j for j in jobs if j.get("status") == "completed" and j.get("result_url")]

    downloaded = []
    for shot_num, prompt in shots:
        out = output_path(shot_num)
        if out.exists():
            downloaded.append(shot_num)
            continue

        prompt_norm = normalize(prompt[:120])
        best_job = None
        for job in completed:
            job_prompt = normalize((job.get("params", {}).get("prompt") or "")[:120])
            if job_prompt and prompt_norm.startswith(job_prompt[:80]) or job_prompt[:80] == prompt_norm[:80]:
                best_job = job
                break

        if best_job:
            try:
                urllib.request.urlretrieve(best_job["result_url"], out)
                print(f"[Shot {shot_num:02d}] 기존 잡 매칭 다운로드 완료 → {out.name}")
                downloaded.append(shot_num)
                completed.remove(best_job)
            except Exception as e:
                print(f"[Shot {shot_num:02d}] 다운로드 실패: {e}")

    return downloaded


async def submit_shot(shot_num: int, prompt: str) -> dict:
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
        job_id = data[0] if isinstance(data, list) else data.get("id")
        if not job_id:
            return {"shot": shot_num, "status": "error", "error": f"job_id 없음: {data}"}

        print(f"[Shot {shot_num:02d}] 제출 완료 → {job_id}")
        return {"shot": shot_num, "status": "submitted", "job_id": job_id}

    return {"shot": shot_num, "status": "error", "error": "재시도 초과"}


async def wait_and_download(sem: asyncio.Semaphore, shot_num: int, job_id: str) -> dict:
    out_path = output_path(shot_num)
    async with sem:
        print(f"[Shot {shot_num:02d}] 완료 대기 중...")
        rc, out, err = await run_cmd("higgsfield", "generate", "wait", job_id, "--json")
        if rc != 0:
            return {"shot": shot_num, "status": "error", "error": err.strip()}

        data = json.loads(out)
        job = data[0] if isinstance(data, list) else data
        result_url = job.get("result_url")
        if not result_url:
            return {"shot": shot_num, "status": "error", "error": f"result_url 없음"}

        urllib.request.urlretrieve(result_url, out_path)
        print(f"[Shot {shot_num:02d}] 저장 완료 → {out_path.name}")
        return {"shot": shot_num, "status": "ok", "path": str(out_path)}


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shots = parse_shots(PROMPTS_FILE)

    # 1단계: 기존 완료 잡 매칭 다운로드
    print("=== 1단계: 기존 완료 잡 다운로드 ===")
    downloaded = await match_and_download(shots)
    print(f"다운로드 완료: {len(downloaded)}개\n")

    # 2단계: 아직 없는 Shot 목록
    pending = [(n, p) for n, p in shots if not output_path(n).exists()]
    print(f"=== 2단계: 미완성 {len(pending)}개 순차 제출 ===")

    submitted = []
    for i, (num, prompt) in enumerate(pending):
        result = await submit_shot(num, prompt)
        submitted.append(result)
        if i < len(pending) - 1:
            await asyncio.sleep(SUBMIT_DELAY)

    ok_submitted = [r for r in submitted if r["status"] == "submitted"]
    failed_submit = [r for r in submitted if r["status"] == "error"]
    print(f"\n제출 성공: {len(ok_submitted)}개 / 실패: {len(failed_submit)}개\n")

    # 3단계: 병렬 대기 + 저장
    if ok_submitted:
        print(f"=== 3단계: {len(ok_submitted)}개 완료 대기 ===")
        sem = asyncio.Semaphore(MAX_WAIT_CONCURRENT)
        results = await asyncio.gather(*[
            wait_and_download(sem, r["shot"], r["job_id"]) for r in ok_submitted
        ])
        ok = [r for r in results if r["status"] == "ok"]
        errors = [r for r in results if r["status"] == "error"] + failed_submit
    else:
        ok = []
        errors = failed_submit

    total_ok = len(downloaded) + len(ok)
    print(f"\n=== 최종 결과 ===")
    print(f"전체 저장: {total_ok} / 42개")
    print(f"실패: {len(errors)}개")
    if errors:
        for e in errors:
            print(f"  [Shot {e['shot']:02d}] {e.get('error', '')}")


if __name__ == "__main__":
    asyncio.run(main())
