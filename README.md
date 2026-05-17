# AI Video System

> **원고 기반 장편 · 전문 AI 영상 제작 운영 시스템**  
> AI를 단순 생성기가 아닌 **감독의 가상 촬영장(Virtual Set)** 으로 활용한다.

사람이 원고를 해석해 캐스팅·로케이션·미술을 설계하고, AI가 이를 Midjourney 스타일 프롬프트로 병합해 이미지를 생성한 뒤 영상으로 변환하는 5단계 파이프라인이다.

---

## 파이프라인 개요

```
01_plan → 02_preproduction → 03_production → 04_release
 기획       이미지 프롬프트      이미지→영상      배포·분석
                                    ↓
                              (NLE 편집 툴로 핸드오프)
```

| 단계 | 역할 | 담당 에이전트 | 핵심 출력물 |
|------|------|-------------|-----------|
| **01 Plan** | 포맷 결정, 대본 분석, 바이블 설계 | `plan_agent.md` | `plan.md`, 캐스팅/로케이션 바이블 |
| **02 Preproduction** | 바이블 ID 조합 → Midjourney 프롬프트 생성 → 베이스 이미지 | `preproduction_agent.md` | 씬별 FINAL 이미지 |
| **03 Production** | 이미지-to-Video 엔진 투입 → Take 생성 | `production_agent.md` | 씬별 FINAL mp4 |
| **04 Release** | 채널 업로드, 성과 데이터 분석 | `release_agent.md` | 분석 리포트 |

> **편집(컷 어셈블리, 음악, 자막, 색보정)은 CapCut / Premiere Pro 등 별도 NLE 툴에서 진행한다.**  
> AI 파이프라인은 FINAL take(mp4) 확보로 종료되며, 이후는 사람이 직접 편집한다.

---

## 핵심 구조 — 바이블 시스템

프롬프트 길이를 최소화하면서 캐릭터·공간 일관성을 유지하는 **현장 통제실**이다.  
모든 프롬프트는 바이블에 등록된 ID 태그를 조합해 만든다.

```
[ACTOR_01] + [C_02] + [LOC_03] + [L_01] + [CAM_05]
     ↓ 에이전트가 병합(Merge)
"Korean teenage girl, 17yo, slim build, short black bob hair, navy school uniform ... 
 classroom interior, golden-hour window light ... handheld camera tracking forward ..."
```

| 바이블 파일 | 통제 영역 |
|-----------|---------|
| `bibles/casting_bible.md` | 배우 체형·메이크업·씬별 의상 코드 |
| `bibles/location_bible.md` | 세트·로케이션·조명·미술 |
| `bibles/camera_bible.md` | 카메라 무브먼트·렌즈 룩 |
| `bibles/emotion_bible.md` | 감정별 미세 표현 묘사 |

---

## 폴더 구조

```
AI Video System/
├── SYSTEM.md                      ← 시스템 철학 및 에이전트 구성
├── WORKFLOW.md                    ← 단계별 상세 워크플로우
├── agents/                        ← 에이전트 프롬프트 (LLM에게 역할 부여)
│   ├── director_agent.md          ← 파이프라인 총괄 감독
│   ├── plan_agent.md
│   ├── preproduction_agent.md
│   ├── production_agent.md
│   └── release_agent.md
├── bibles/                        ← 일관성 통제 바이블 (핵심)
│   ├── casting_bible.md
│   ├── location_bible.md
│   ├── camera_bible.md
│   └── emotion_bible.md
├── 01_plan/
│   ├── templates/plan_template.md
│   └── projects/[프로젝트명]/plan.md
├── 02_preproduction/
│   ├── image_prompts/             ← 씬별 이미지 프롬프트 플랜
│   └── storyboards/               ← 스토리보드 참고
├── 03_production/
│   ├── action_prompts/            ← 이미지-to-Video 액션 프롬프트
│   └── takes/                     ← 생성된 영상 Take
├── 04_release/
│   ├── templates/
│   └── analytics/
├── scripts/
│   ├── ai_video_cli.py            ← 통합 자동화 CLI (핵심)
│   ├── requirements.txt
│   └── build_executable.sh        ← Mac 단일 바이너리 빌드
└── assets/
    ├── characters/                ← 생성된 캐릭터 이미지
    ├── exports/images/            ← 씬별 FINAL 이미지 출력
    └── exports/takes/             ← 씬별 FINAL 영상 출력
```

---

## 사용법

### 1. 환경 설정

```bash
# 의존성 설치
pip install -r scripts/requirements.txt

# API 키 설정 (.env 파일 생성)
cp .env.example .env
# .env 에 GOOGLE_API_KEY 등 필요한 키 입력
```

`.env` 예시:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

### 2. 새 프로젝트 시작

```bash
# 프로젝트 폴더 생성
mkdir 01_plan/projects/[프로젝트명]

# plan.md 템플릿 복사
cp 01_plan/templates/plan_template.md 01_plan/projects/[프로젝트명]/plan.md
```

`plan.md` 상단에서 **[영상 포맷]** 을 반드시 결정한다.
> `영화` / `드라마` / `MV` / `광고` / `쇼츠` — 포맷에 따라 연출 밀도와 컷 리듬이 달라진다.

---

### 3. 바이블 세팅

`bibles/casting_bible.md`와 `bibles/location_bible.md`에 프로젝트 배우·공간을 등록한다.

```markdown
## [ACTOR_01] 김나영
- 나이: 17세 / 체형: 슬림, 162cm
- 기본 메이크업: 자연스러운 교복 룩, 연한 립
- 의상 [C_01]: 하복 교복 (흰 블라우스 + 네이비 체크 스커트)
- 의상 [C_02]: 체육복 (회색 + 학교 로고)
```

---

### 4. 이미지 프롬프트 플랜 작성

`02_preproduction/image_prompts/` 에 마크다운 파일을 만들고 Shot 단위로 작성한다.

````markdown
### Shot 01
```
[ACTOR_01] [C_01] [LOC_01] [L_02] [CAM_03],
looking out the window with a distant expression, spring afternoon
```
````

에이전트가 이 짧은 ID 조합을 완성형 Midjourney 프롬프트로 병합해준다.

---

### 5. CLI로 이미지·영상 자동 생성

```bash
# 대화형 CLI 실행
python scripts/ai_video_cli.py
```

CLI 메뉴에서 엔진과 동작을 선택한다:

```
[1] Generate Images (Gemini Imagen)
[2] Generate Images (Qwen)
[3] Generate Videos (Veo)
[4] Generate Videos (Wan / Hunyuan)
[q] Quit
```

출력 경로:
- 이미지: `assets/exports/images/shot_01_v1.png`
- 영상: `assets/exports/takes/shot_01_take1.mp4`

---

### 6. Mac 단일 바이너리 빌드 (선택)

```bash
bash scripts/build_executable.sh
# 결과: scripts/dist/ai_video_cli_mac
./scripts/dist/ai_video_cli_mac
```

---

## 파일명 규칙

| 구분 | 형식 | 예시 |
|------|------|------|
| 이미지 (최종 선택) | `shot_[번호]_v[버전]_FINAL.png` | `shot_01_v3_FINAL.png` |
| 영상 Take | `shot_[번호]_take[번호].mp4` | `shot_01_take2.mp4` |
| 완성본 | `[프로젝트명]_v[버전].mp4` | `hanroro_v1.0.mp4` |
| 마이너 수정 | `_v1.1` | 프롬프트 미세조정 수준 |
| 메이저 수정 | `_v2.0` | 씬 구조·스토리 변경 수준 |

---

## 지원 AI 엔진

| 역할 | 엔진 | 파이프라인 포함 |
|------|------|:---:|
| 이미지 생성 | Gemini Imagen 3, Qwen Image | O |
| 이미지→영상 | Gemini Veo, Wan, Hunyuan | O |
| 노드 기반 미세조정 | ComfyUI | O |
| 영상 편집 (NLE) | CapCut, Premiere Pro | 외부 |
| 음성·나레이션 | ElevenLabs | 외부 |
| 배경음악 | Suno | 외부 |

---

## 트러블슈팅

| 문제 | 해결 |
|------|------|
| 캐릭터 외형이 씬마다 달라짐 | `casting_bible.md` 의상·메이크업 고정 프롬프트 재확인 |
| 프롬프트가 너무 길어 AI 오작동 | Specific 묘사 제거 후 Global 룩을 템플릿 상단에 분리 |
| Shot 번호가 이미지·영상 파일과 불일치 | `image_prompts`와 `action_prompts` 양쪽 `### Shot XX` 헤더 일치 여부 확인 |
| `.env` API 키 인식 안 됨 | CLI를 실행하는 디렉터리에 `.env` 파일이 있어야 함 |

---

## 라이선스

이 저장소는 개인 프로덕션 워크플로우용으로 제작되었습니다.
