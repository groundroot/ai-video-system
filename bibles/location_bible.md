# Location Bible
## 로케이션 및 미술(Art Direction), 조명 시스템

> 영화/드라마 감독의 관점에서 공간(로케이션)을 헌팅하고, 세트 미술과 조명을 세팅하는 바이블.
> 모든 프롬프트 생성 시 **[로케이션 ID]** 만 참조하여 프롬프트 길이를 최소화하고, 공통 적용할 수 있도록 설계한다.
> **주의:** 이미지 프롬프트 생성 시 타 엔진을 사용하더라도, 프롬프트 문법 자체는 디테일이 가장 강력한 **Midjourney(미드저니)** 스타일의 태그, 조명 명세, 렌즈 스펙 방식을 차용한다.

---

## 🏛️ 로케이션 템플릿 양식

```markdown
## [로케이션 ID: LOC_01] [장소 이름]

### 1. 기본 공간 설명 (Set & Art Direction)
- 공간 개요: 
- 시대적 배경/분위기: 
- 고정 프롬프트 (영어, Midjourney 스타일): 
  `[예: inside a 1990s Korean high school classroom, wooden desks, chalk dust in the air, vintage posters on the wall, highly detailed, architectural photography --ar 16:9]`

### 2. 조명 및 시간대 (Lighting & Time)
- **[L_01] 낮/자연광:** `golden hour sunlight streaming through large windows, soft diffused light, cinematic lighting`
- **[L_02] 밤/인공광:** `harsh fluorescent overhead lights, deep shadows, moody atmosphere, cinematic color grading`

### 3. 카메라 및 렌즈 (Camera & Lens) - Global 적용 권장
- **[CAM_01] 광각/설정 샷 (Establishing):** `shot on 24mm lens, wide angle, deep depth of field, establishing shot`
- **[CAM_02] 클로즈업 (Intimate):** `shot on 85mm lens, f/1.4, shallow depth of field, sharp focus on subject, blurred background, bokeh`

### 4. 금지 요소 (Negative Prompt)
- `modern devices, futuristic, messy, empty, low resolution`
```

---

## 🎬 등록된 로케이션 데이터 (예시: hanroro_0plus0)

### [LOC_01] 90년대 중학교 교실

**1. 기본 공간 설명**
- 공간 개요: 낡은 목판 바닥과 녹색 칠판이 있는 90년대 한국 중학교 교실
- 시대적 배경: 1990년대 후반 아날로그 감성
- 고정 프롬프트: 
  `inside a 1990s vintage Korean middle school classroom, old wooden floorboards, green chalkboard with faint chalk writing, wooden desks arranged in rows, highly detailed, nostalgic atmosphere, analog film photography style`

**2. 조명 및 시간대**
- **[L_01] 따뜻한 오후:** `warm late afternoon sunlight streaming through dusty windows, beautiful dust motes dancing in light beams, soft golden lighting`
- **[L_02] 우중충한 오전:** `overcast daylight, cool blueish tint, soft diffused shadows, moody cinematic lighting`

**3. 금지 요소**
`modern smartboards, smartphones, futuristic furniture, overly clean, 3D render, digital illustration`

---

### [LOC_02] 학교 앞 오래된 문방구

**1. 기본 공간 설명**
- 공간 개요: 장난감과 과자가 가득 쌓여있는 복잡하고 정겨운 학교 앞 문방구
- 시대적 배경: 1990년대 하교 시간
- 고정 프롬프트: 
  `front of an old 1990s Korean stationary store, cluttered with colorful retro toys and snacks, vintage arcade machines outside, highly detailed environment, cinematic composition`

**2. 조명 및 시간대**
- **[L_01] 해 질 녘:** `warm glowing sunset lighting, neon sign faintly buzzing, deep contrast, dramatic shadows`

**3. 금지 요소**
`modern convenience store, clean organized shelves, futuristic, empty streets`

---

## ⚙️ 시스템 적용 방식
- 시놉시스/스토리보드 작성 시 배경 묘사를 길게 적지 않습니다.
- 프롬프트 생성 에이전트는 `[LOC_01] + [L_01] + [CAM_01]` 의 조합값을 이 바이블에서 읽어와 자동으로 영문 프롬프트로 병합(Merge)합니다.
- 항상 **미드저니(Midjourney) 프롬프트 스타일**(콤마로 구분된 명사 위주, 조명, 렌즈, 화질 키워드 포함)로 변환하여 적용합니다.
