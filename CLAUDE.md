# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and Gemini Agents when working with code in this repository.

---

## 시스템 개요

이 저장소는 **원고 기반 장편/전문 AI 영상 제작 운영 시스템**이다. 
단순 스크립트 실행 환경이 아니며, 영화 감독이 현장을 통제하듯 **캐스팅, 로케이션, 미술, 포맷을 통제하는 아키텍처**를 가진다.

핵심 철학: AI는 단순 생성기가 아닌 **감독의 가상 촬영장(Virtual Set)**이다.
사람이 원고를 해석하여 Global(전역 룩)과 Specific(씬별 묘사)을 분리하고, AI는 이를 Midjourney 방식의 프롬프트로 병합해 이미지를 뽑고(Image Prompt Plan), 이를 영상화(Image-to-Video)한다.

---

## 5단계 파이프라인

```
01_plan (원고 및 포맷 설정) → 02_preproduction (이미지 프롬프트 플랜) → 03_production (이미지-to-비디오) → 04_postproduction → 05_release
```

| 단계 | 역할 | 에이전트 프롬프트 | 핵심 출력물 |
|------|----|----------------|---------|
| Plan | 포맷 설정, 대본 분석, 바이블(캐스팅/로케이션) 구축 | `plan_agent.md` | `plan.md`, 바이블 세팅 |
| Preproduction | 시놉시스 기반 이미지 프롬프트 플랜 생성 | `preproduction_agent.md` | 베이스 이미지 (FINAL) |
| Production | 이미지를 비디오 엔진으로 전송 (액션 프롬프팅) | `production_agent.md` | take 영상 (FINAL) |
| Postproduction| 편집 가이드에 따른 컷 편집, 음향 입히기 | `postproduction_agent.md` | 완성본 |
| Release | 플랫폼 업로드 전략 및 데이터 리포트 | `release_agent.md` | 분석 데이터 |

**Director Agent** (`agents/director_agent.md`)는 파이프라인 총괄 및 바이블 일관성 감시.

---

## 바이블 시스템 (현장 통제실)

이 저장소의 심장부로, 프롬프트 길이를 최소화하고 일관성을 유지하는 핵심이다.
모든 프롬프트는 아래 파일에 등록된 ID (`[ACTOR_01]`, `[LOC_01]` 등)를 조합(Merge)하여 만들어진다.

- **`casting_bible.md`** — 배우 프로필, 의상(Costume), 메이크업 시스템 통제.
- **`location_bible.md`** — 세트장, 로케이션, 공간적 미술, 조명 세팅 통제.
- **`camera_bible.md`** — 카메라 무브먼트 라이브러리.
- **`emotion_bible.md`** — 감정별 표현 미세 묘사 통제.

*프롬프트 생성 전략:* 최종 프롬프트는 타 엔진을 쓰더라도 가장 정교한 **Midjourney 언어 문법(콤마 분리, 카메라/조명 명세)**을 따르도록 설계한다.

---

## Python 통합 CLI (ai_video_cli.py)

엔진(Gemini, Qwen, Wan, Hunyuan 등)을 선택하여 이미지와 영상을 자동 생성하는 통합 터미널 도구.

```bash
# 의존성 설치
pip install -r scripts/requirements.txt

# 실행 (대화형 CLI 인터페이스)
python scripts/ai_video_cli.py

# 또는 배포된 Mac 전용 바이너리 실행 (빌드된 경우)
./scripts/dist/ai_video_cli_mac
```

---

## 새 프로젝트 초기화

```bash
mkdir 01_plan/projects/[프로젝트명]
cp 01_plan/templates/plan_template.md 01_plan/projects/[프로젝트명]/plan.md
```
- 반드시 `plan.md` 최상단에서 작품의 **[영상 포맷: 영화/드라마/MV/광고/쇼츠]** 을 결정해야 한다.

---

## 파일명 규칙

- `_FINAL` 접미사: 해당 씬의 최종 선택 이미지/영상
- Minor 변경: `v1.1` / Major 변경(스토리·씬 구조): `v2.0`

```
이미지:    assets/exports/images/shot_01_v3_FINAL.png
영상 take: assets/exports/takes/shot_01_take2.mp4
완성본:    assets/exports/[프로젝트명]_v1.0.mp4
```

---

## 트러블슈팅

| 문제 | 해결 방법 |
|------|---------|
| 캐스팅 일관성 깨짐 | `casting_bible.md` 의상/메이크업 고정 프롬프트 재확인 |
| 프롬프트가 너무 길어 AI가 오작동함 | 개별(Specific) 묘사를 지우고, 공통(Global) 룩을 템플릿 상단에 묶어 분리 |
| 스크립트 실행 시 Shot 불일치 | 이미지 프롬프트 문서와 액션 프롬프트 문서 양쪽에 동일한 헤더(`### Shot 01`) 존재 여부 확인 |
