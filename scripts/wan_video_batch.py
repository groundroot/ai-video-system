#!/usr/bin/env python3
"""
Alibaba Cloud DashScope Wan I2V 배치 영상 생성기
- 이미지: assets/characters/shot_XX_v1.png
- 이미지 URL 확보: OSS 업로드 (OSS 환경변수 필요)
- 영상 생성: wanx2.1-i2v-turbo (DashScope)
- 출력: 03_production/takes/hanroro_0plus0/shot_XX_take01.mp4

필수 환경변수:
  DASHSCOPE_API_KEY       DashScope API 키
  OSS_ACCESS_KEY_ID       Alibaba Cloud AccessKey ID
  OSS_ACCESS_KEY_SECRET   Alibaba Cloud AccessKey Secret
  OSS_BUCKET_NAME         OSS 버킷 이름 (예: my-video-bucket)
  OSS_ENDPOINT            OSS 엔드포인트 (예: oss-cn-hangzhou.aliyuncs.com)
"""

import asyncio
import json
import os
import re
import sys
import time
import urllib.request
from http import HTTPStatus
from pathlib import Path

import oss2
import dashscope
from dashscope import VideoSynthesis

# ─── 경로 설정 ───────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
ACTION_PROMPTS_FILE = (
    BASE_DIR / "03_production" / "action_prompts"
    / "hanroro_0plus0_action_prompts_v3.md"
)
IMAGE_DIR = BASE_DIR / "assets" / "characters"
OUTPUT_DIR = BASE_DIR / "03_production" / "takes" / "hanroro_0plus0"

# ─── 모델 설정 ───────────────────────────────────────────
MODEL = VideoSynthesis.Models.wanx_2_1_i2v_turbo   # wanx2.1-i2v-turbo
# 더 높은 품질 원하면: VideoSynthesis.Models.wanx_2_1_i2v_plus

# duration: Wan I2V는 4s / 8s 고정. 5s·6s 샷은 8s 생성 후 편집에서 트림
DURATION_MAP = {4: 4, 5: 8, 6: 8}

NEGATIVE_PROMPT = (
    "no CGI, no computer graphics, no animation, no digital effects, "
    "no light rays effect, no particle effects, no glow effect, no lens flare effect, "
    "no color grading filter, no vignette effect, no film grain effect, "
    "no motion blur effect, not a music video with effects, "
    "not Hollywood movie style, not anime, not illustration, "
    "not rendered, not computer generated"
)

OSS_PREFIX = "hanroro_0plus0/images/"   # 버킷 내 경로
MAX_CONCURRENT = 3                       # 동시 생성 수 (rate limit 고려)
SUBMIT_DELAY = 2                         # 제출 간격(초)


# ─── 파싱 ────────────────────────────────────────────────

def parse_shots(filepath: Path) -> list[tuple[int, str, int]]:
    """(shot_num, action_prompt, duration_s) 리스트 반환."""
    content = filepath.read_text(encoding="utf-8")
    header_pat = re.compile(
        r"###\s+Shot\s+(\d+).*?\*\*Duration:\*\*\s*(\d+)s.*?```\n(.*?)```",
        re.DOTALL,
    )
    shots = []
    for m in header_pat.finditer(content):
        num = int(m.group(1))
        dur = int(m.group(2))
        prompt = m.group(3).strip()
        shots.append((num, prompt, dur))
    return sorted(shots, key=lambda x: x[0])


# ─── OSS ─────────────────────────────────────────────────

def get_oss_bucket() -> oss2.Bucket:
    key_id = os.environ["OSS_ACCESS_KEY_ID"]
    key_secret = os.environ["OSS_ACCESS_KEY_SECRET"]
    bucket_name = os.environ["OSS_BUCKET_NAME"]
    endpoint = os.environ["OSS_ENDPOINT"]
    auth = oss2.Auth(key_id, key_secret)
    return oss2.Bucket(auth, f"https://{endpoint}", bucket_name)


def upload_image_to_oss(bucket: oss2.Bucket, local_path: Path) -> str:
    """이미지를 OSS에 업로드하고 공개 URL을 반환."""
    oss_key = OSS_PREFIX + local_path.name
    # 이미 업로드된 경우 스킵
    try:
        bucket.head_object(oss_key)
        # 이미 존재 → URL만 반환
    except oss2.exceptions.NoSuchKey:
        with open(local_path, "rb") as f:
            bucket.put_object(oss_key, f)
    endpoint = os.environ["OSS_ENDPOINT"]
    bucket_name = os.environ["OSS_BUCKET_NAME"]
    return f"https://{bucket_name}.{endpoint}/{oss_key}"


# ─── 영상 생성 ───────────────────────────────────────────

def output_path(shot_num: int) -> Path:
    return OUTPUT_DIR / f"shot_{shot_num:02d}_take01.mp4"


def submit_video_job(
    api_key: str,
    shot_num: int,
    prompt: str,
    duration_s: int,
    img_url: str,
) -> str | None:
    """DashScope VideoSynthesis 잡 제출. task_id 반환."""
    wan_duration = DURATION_MAP.get(duration_s, 8)
    response = VideoSynthesis.async_call(
        api_key=api_key,
        model=MODEL,
        prompt=prompt,
        img_url=img_url,
        negative_prompt=NEGATIVE_PROMPT,
        duration=wan_duration,
    )
    if response.status_code == HTTPStatus.OK:
        task_id = response.output.get("task_id")
        print(f"[Shot {shot_num:02d}] 제출 완료 → task_id={task_id} ({wan_duration}s)")
        return task_id
    else:
        print(f"[Shot {shot_num:02d}] 제출 실패: {response.code} {response.message}")
        return None


def wait_for_video(api_key: str, shot_num: int, task_id: str) -> str | None:
    """완료될 때까지 폴링. video_url 반환."""
    for attempt in range(120):  # 최대 10분
        response = VideoSynthesis.fetch(task_id, api_key=api_key)
        if response.status_code != HTTPStatus.OK:
            print(f"[Shot {shot_num:02d}] fetch 오류: {response.code}")
            return None
        status = response.output.get("task_status")
        if status == "SUCCEEDED":
            url = response.output.get("video_url") or response.output.get("output_video_url")
            if not url:
                # 중첩 구조 탐색
                videos = response.output.get("video_urls", [])
                url = videos[0] if videos else None
            return url
        elif status in ("FAILED", "CANCELED"):
            msg = response.output.get("message", "")
            print(f"[Shot {shot_num:02d}] 생성 실패: {status} {msg}")
            return None
        time.sleep(5)
    print(f"[Shot {shot_num:02d}] 타임아웃")
    return None


async def process_shot(
    sem: asyncio.Semaphore,
    api_key: str,
    bucket: oss2.Bucket,
    shot_num: int,
    prompt: str,
    duration_s: int,
) -> dict:
    out = output_path(shot_num)
    if out.exists():
        print(f"[Shot {shot_num:02d}] 이미 존재 → 스킵")
        return {"shot": shot_num, "status": "skipped"}

    img_local = IMAGE_DIR / f"shot_{shot_num:02d}_v1.png"
    if not img_local.exists():
        print(f"[Shot {shot_num:02d}] 소스 이미지 없음: {img_local.name}")
        return {"shot": shot_num, "status": "error", "error": "no source image"}

    async with sem:
        # OSS 업로드
        try:
            img_url = await asyncio.get_event_loop().run_in_executor(
                None, upload_image_to_oss, bucket, img_local
            )
            print(f"[Shot {shot_num:02d}] OSS URL 확보 완료")
        except Exception as e:
            print(f"[Shot {shot_num:02d}] OSS 업로드 실패: {e}")
            return {"shot": shot_num, "status": "error", "error": str(e)}

        # 영상 잡 제출
        task_id = await asyncio.get_event_loop().run_in_executor(
            None, submit_video_job, api_key, shot_num, prompt, duration_s, img_url
        )
        if not task_id:
            return {"shot": shot_num, "status": "error", "error": "submit failed"}

        # 완료 대기
        video_url = await asyncio.get_event_loop().run_in_executor(
            None, wait_for_video, api_key, shot_num, task_id
        )
        if not video_url:
            return {"shot": shot_num, "status": "error", "error": "generation failed"}

        # 다운로드
        urllib.request.urlretrieve(video_url, out)
        print(f"[Shot {shot_num:02d}] 저장 완료 → {out.name}")
        return {"shot": shot_num, "status": "ok", "path": str(out)}


async def main():
    # 환경변수 확인
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("오류: DASHSCOPE_API_KEY 환경변수가 없습니다.")
        sys.exit(1)

    required_oss = ["OSS_ACCESS_KEY_ID", "OSS_ACCESS_KEY_SECRET",
                    "OSS_BUCKET_NAME", "OSS_ENDPOINT"]
    missing = [k for k in required_oss if not os.environ.get(k)]
    if missing:
        print(f"오류: OSS 환경변수 누락 — {', '.join(missing)}")
        print("  OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, OSS_BUCKET_NAME,")
        print("  OSS_ENDPOINT (예: oss-cn-hangzhou.aliyuncs.com)")
        sys.exit(1)

    # 초기화
    dashscope.api_key = api_key
    bucket = get_oss_bucket()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    shots = parse_shots(ACTION_PROMPTS_FILE)
    if not shots:
        print("액션 프롬프트를 파싱할 수 없습니다.")
        sys.exit(1)

    pending = [(n, p, d) for n, p, d in shots if not output_path(n).exists()]
    skipped = len(shots) - len(pending)
    print(f"총 {len(shots)}개 | 대기: {len(pending)}개 | 스킵: {skipped}개")
    print(f"모델: {MODEL} | 동시 처리: {MAX_CONCURRENT}개\n")

    sem = asyncio.Semaphore(MAX_CONCURRENT)
    tasks = []
    for i, (num, prompt, dur) in enumerate(pending):
        tasks.append(process_shot(sem, api_key, bucket, num, prompt, dur))
        if i < len(pending) - 1:
            await asyncio.sleep(SUBMIT_DELAY)

    results = await asyncio.gather(*tasks)

    ok = [r for r in results if r["status"] == "ok"]
    errors = [r for r in results if r["status"] == "error"]
    print(f"\n=== 완료 ===")
    print(f"성공: {len(ok) + skipped}개 / 실패: {len(errors)}개")
    if errors:
        for e in errors:
            print(f"  [Shot {e['shot']:02d}] {e.get('error', '')}")


if __name__ == "__main__":
    asyncio.run(main())
