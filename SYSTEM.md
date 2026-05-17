# AI VIDEO CREATION SYSTEM
## 원고 기반 전문 AI 영상 제작 운영 시스템
**Version:** v2.0 (장편/전문 프로덕션 개편)
**Base:** `/AI Video System/`

---

## 시스템 철학

> "AI는 단순한 생성기가 아니라, 감독의 가상 촬영장(Virtual Set)이다."
> 사람이 원고를 분석해 캐스팅, 로케이션, 미술을 통제하고, AI는 이미지(프롬프트 플랜)와 영상(이미지-to-비디오)을 렌더링한다.

### 핵심 전략
1. **포맷별 전문화 (Format-Specific):** 영화, 드라마, 광고, MV, 쇼츠 등 작품 포맷에 따라 연출 템플릿과 프로세스가 변형되어 적용된다.
2. **프롬프트 최소화 (Global vs Specific):** 
   - **Global (공통 룩):** 카메라 스펙, 전체 조명 톤, 시대적 질감 등은 시스템이 자동으로 덧붙이게 하여 불필요한 반복 입력을 줄인다.
   - **Specific (개별 묘사):** 감독은 씬마다 어떤 배우(`[ACTOR_ID]`), 어떤 의상(`[C_ID]`), 어느 공간(`[LOC_ID]`)에서 행동하는지만 조립한다.
3. **Midjourney 스타일 프롬프팅:** 비록 다양한 엔진(Qwen, Gemini 등)을 사용하더라도, 프롬프트 텍스트 자체는 디테일 통제가 가장 강력한 미드저니(Midjourney)의 문법(명사/형용사 나열, 조명/렌즈 명세)을 기준 언어로 채택한다.

---

## 에이전트 구성

| 에이전트 | 역할 | 위치 |
|---------|------|------|
| Director Agent | 전체 파이프라인 조율, 원고(Manuscript) 해석 | `agents/director_agent.md` |
| Plan Agent | 포맷(영화/광고 등)에 따른 기획 세팅, 캐스팅/로케이션 설계 | `agents/plan_agent.md` |
| Preproduction Agent | 시놉시스/대본 분석 ➜ **이미지 제작 프롬프트 플랜** 생성 | `agents/preproduction_agent.md` |
| Production Agent | 생성된 이미지 기반 ➜ **이미지-to-비디오** 생성 (액션 프롬프트) | `agents/production_agent.md` |
| Release Agent | 업로드 전략, 데이터 분석 | `agents/release_agent.md` |

---

## 전체 프로세스 흐름

```
[Director Agent] (원고/대본 분석)
       │
       ▼
[01_plan] ──── Plan Agent
  plan.md 작성 (포맷: 영화/드라마/쇼츠 결정)
  캐스팅(배우/의상/메이크업), 로케이션(미술/조명) 바이블 세팅
       │
       ▼
[02_preproduction] ──── Preproduction Agent
  스토리보드를 "이미지 제작 프롬프트 플랜"으로 대치
  바이블 ID(예: ACTOR_01 + LOC_02)를 조합해 Midjourney식 프롬프트 생성
  AI (Gemini/Qwen 등) ➜ 씬별 베이스 이미지 생성
       │
       ▼
[03_production] ──── Production Agent
  선택된 이미지를 비디오 엔진에 투입 (Image-to-Video)
  비디오 렌더링용 짧은 액션 프롬프트 적용
  AI (Veo/Wan/Hunyuan 등) ➜ 영상 생성
       │
       ▼
[04_release] ──── Release Agent
```

---

## 폴더 구조

```
AI Video System/
├── SYSTEM.md                 ← 이 파일 (시스템 개요)
├── WORKFLOW.md               ← 전체 워크플로우 상세
├── agents/                   ← 에이전트 프롬프트 모음
├── bibles/                   ← 일관성 유지 바이블 (핵심 통제실)
│   ├── casting_bible.md      ← 배우, 의상, 메이크업 통제
│   ├── location_bible.md     ← 로케이션, 공간, 조명, 미술 통제
│   ├── camera_bible.md       ← 카메라 무브먼트 렌즈 룩 통제
│   └── emotion_bible.md      ← 감정별 미세 표현 통제
├── 01_plan/                  ← 기획 단계 (원고 분석 및 포맷 결정)
├── 02_preproduction/         ← 프리프로덕션 (이미지 제작 프롬프트 플랜)
├── 03_production/            ← 프로덕션 (이미지-to-비디오 생성)
├── 04_release/               ← 릴리즈 (편집은 별도 NLE 툴에서 진행)
├── scripts/                  ← 파이썬 CLI 자동화 시스템 (ai_video_cli.py)
└── assets/                   ← 미디어 에셋 (images, takes, archive 등)
```

---

## 툴 매핑

| 역할 | 툴 |
|------|-----|
| 통합 파이프라인 실행 | `scripts/ai_video_cli.py` (배포된 단일 실행앱) |
| 이미지 생성 (Pre-pro) | Gemini Imagen 3, Qwen Image (Midjourney 문법 사용) |
| 이미지-to-비디오 (Pro) | Gemini Veo, Wan, Hunyuan |
| 노드 기반 미세조정 | ComfyUI |
| 영상 편집 (NLE) | CapCut, Premiere Pro (파이프라인 외부) |
| 음성/음악 | ElevenLabs / Suno (파이프라인 외부) |
