# WORKFLOW
## 전문 장편 영상 파이프라인 가이드

이 문서는 대본(원고)을 기반으로 캐스팅, 로케이션을 통제하고 이를 최소화된 프롬프트로 병합하여 영상을 렌더링하는 구체적인 프로세스를 담고 있습니다.

---

## Step 0 — 프로젝트 초기화 및 포맷 결정

```bash
# 프로젝트 폴더 생성
mkdir 01_plan/projects/[프로젝트명]

# plan.md 생성
cp 01_plan/templates/plan_template.md 01_plan/projects/[프로젝트명]/plan.md
```
- **중요:** 가장 먼저 `plan.md` 상단의 **[영상 포맷]** (영화, 드라마, 광고, MV, 쇼츠 등)을 결정해야 합니다. 이 포맷에 따라 이어지는 프로세스의 속도와 밀도가 달라집니다.

---

## Step 1 — Plan (기획 및 세팅)

**담당:** Plan Agent (`agents/plan_agent.md`)  
**폴더:** `01_plan/`

### 1-1. 원고(Manuscript) 분석 및 포맷 적용
- 감독(사용자)의 대본/원고 아이디어를 기반으로 전체 기획안(`plan.md`) 작성
- 영상 포맷에 맞춰 전역(Global) 컨셉, 카메라 룩(Look & Feel)을 확정.

### 1-2. 바이블(Bible) 세팅 (현장 통제실)
- **`bibles/casting_bible.md`:** 씬에 등장할 배우들을 확정. 각 배우의 체형, 메이크업, 씬별 의상 코드를 등록 (`[ACTOR_01]`, `[C_01]`).
- **`bibles/location_bible.md`:** 촬영될 장소, 세트, 조명 톤을 등록 (`[LOC_01]`, `[L_01]`).

**완료 신호:** `plan.md` 완료 및 캐스팅/로케이션 바이블 세팅 완료

---

## Step 2 — Preproduction (이미지 제작 프롬프트 플랜)

**담당:** Preproduction Agent (`agents/preproduction_agent.md`)  
**폴더:** `02_preproduction/`

이 단계는 과거의 "스토리보드"를 넘어서, **"이미지 제작 프롬프트 플랜"**을 구축하는 단계입니다. 
긴 묘사를 적는 대신, 1단계에서 만든 바이블의 **ID 태그**만을 씬마다 조립합니다.

### 2-1. 프롬프트 플랜 조립
- 원고 내용에 따라 각 씬에 다음과 같이 매핑합니다.
  - 씬 1: `[ACTOR_01] + [C_01] + [LOC_01] + [L_01] + [CAM_01]`
- 에이전트는 이 짧은 기호를 바탕으로 **Midjourney(미드저니)** 스타일의 고밀도 영문 프롬프트로 병합(Merge)해줍니다.

### 2-2. 베이스 이미지 생성
- `ai_video_cli.py` (또는 수동 Qwen/Gemini) 실행
- 씬별 최소 3개 이미지를 생성하여 가장 완벽한 구도와 조명을 가진 이미지를 `FINAL`로 선택.

**완료 신호:** 전 씬 FINAL 베이스 이미지 확보 완료

---

## Step 3 — Production (이미지-to-비디오 생성)

**담당:** Production Agent (`agents/production_agent.md`)  
**폴더:** `03_production/`

이 단계는 2단계에서 만든 완벽한 이미지를 **비디오 엔진(Image-to-Video)** 에 넣고 움직임을 부여하는 단계입니다. 과거의 "실제 촬영"을 완전히 대치합니다.

### 3-1. 비디오용 액션 프롬프트 작성
- 베이스 이미지가 이미 완벽한 룩과 조명을 가지고 있으므로, 영상 프롬프트는 매우 간결해야 합니다.
- 예: `camera slowly tracking forward, the girl turns her head slightly, hair blowing in the wind`
- 텍스트-to-비디오가 아닌 **이미지-to-비디오 전용** 프롬프팅 방식을 사용합니다.

### 3-2. 영상(Take) 생성 및 취합
- `ai_video_cli.py` 를 통해 Veo, Wan, Hunyuan 등의 비디오 엔진으로 렌더링을 돌립니다.
- 씬별 최소 2개 이상의 Take를 생성합니다.

**완료 신호:** 전 씬 FINAL take (mp4) 확보 완료

---

## Step 4 — Release (릴리즈)

**담당:** Release Agent (`agents/release_agent.md`)  
**폴더:** `04_release/`

> 편집(컷 어셈블리, 음악, 자막, 색보정)은 CapCut, Premiere Pro 등 **별도 NLE 툴**에서 진행한다.  
> AI 파이프라인은 FINAL take 확보로 종료된다.

### 4-1. 업로드 및 데이터 분석
- YouTube / Instagram 등 채널 특성에 맞춘 제목 및 설명 생성.
- 영상 업로드 및 성과 데이터 수집.

---

## 핵심 요약: Global vs Specific 구조

1. **Global (공통 적용 컨셉):** 
   - 영상 포맷 (영화적, 90년대 빈티지 등)
   - 카메라 룩, 베이스 조명 톤
   - *이는 시스템이 프롬프트 끝에 항상 자동으로 삽입합니다.*
2. **Specific (씬별 변동 사항):** 
   - `[캐스팅 번호]`, `[의상 번호]`, `[로케이션 번호]`, 짧은 모션 서술.
   - *사용자와 에이전트는 기획/프롬프트 플랜 작성 시 이 Specific 기호들만 가지고 씬을 레고처럼 조립합니다.*
