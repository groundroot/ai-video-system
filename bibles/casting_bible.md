# Casting Bible
## 캐스팅 및 분장/의상 일관성 시스템

> 영화/드라마 감독의 관점에서 배우(캐릭터)를 캐스팅하고 의상, 메이크업을 관리하는 바이블.
> 모든 프롬프트 생성 시 **[캐스팅 ID]** 만 참조하여 프롬프트 길이를 최소화하고, 공통 적용할 수 있도록 설계한다.

---

## 🎭 캐스팅 템플릿 양식

```markdown
## [캐스팅 ID: ACTOR_01] [배역 이름]

### 1. 기본 캐스팅 프로필 (고정 외형)
- 나이/역할: 
- 체형/골격: 
- 메이크업 톤/피부: 
- 고정 프롬프트 (영어): 
  `[예: young korean male actor, 25 years old, sharp jawline, pale skin with subtle matte makeup, natural short messy black hair, consistent facial features]`

### 2. 의상 (Costume Wardrobe)
- **[C_01] 기본 의상:** `oversized faded black hoodie, dark washed denim, worn out white sneakers`
- **[C_02] 특별 의상:** `sharp navy tailored suit, white crisp shirt, no tie`

### 3. 감정 및 연기 (Acting & Expression)
- **[E_01] 기본 상태 (Default):** `neutral expression, calm distant gaze, relaxed facial muscles`
- **[E_02] 극적 상태 (Dramatic):** `intense stare, slight frown, subtle tear shining in eye, jaw clenched`

### 4. 금지 요소 (Negative Prompt)
- `inconsistent face, different person, heavy color makeup, modern shiny clothing, cartoonish features`
```

---

## 🎬 등록된 캐스팅 데이터 (예시: hanroro_0plus0)

### [ACTOR_01] 이서현 (주연)

**1. 기본 캐스팅 프로필**
- 나이/역할: 15세, 무리의 비공식 리더
- 메이크업 톤: 노메이크업에 가까운 자연스러운 톤, 연한 주근깨
- 고정 프롬프트: 
  `Korean middle school girl, 15 years old, short straight black bob hair cut at chin length, sharp intelligent dark brown eyes, fair skin with faint freckles, slim slightly tall build, confident natural posture`

**2. 의상 (Wardrobe)**
- **[C_01] 90년대 교복:** `1990s Korean school uniform navy blue jacket, white shirt, plaid skirt, collar slightly unbuttoned`

**3. 감정 및 연기**
- **[E_01] 무심함:** `neutral cool expression, slight downward gaze, relaxed jaw`
- **[E_02] 희미한 웃음:** `unexpected bright smile, eyes crinkling, slightly thrown back head`

**4. 금지 요소**
`different hair length, different hair color, adult appearance, heavy makeup, modern trendy clothing, inconsistent face`

---

### [ACTOR_02] 박도윤 (주연)

**1. 기본 캐스팅 프로필**
- 나이/역할: 15세, 관찰자 및 스케치 담당
- 메이크업 톤: 따뜻한 올리브 톤, 메이크업 없음
- 고정 프롬프트: 
  `Korean middle school boy, 15 years old, slightly wavy black hair slightly longer covering ears, soft gentle dark eyes with slight drooping corners, warm olive skin tone, medium slightly slouched build, pencil tucked behind ear`

**2. 의상 (Wardrobe)**
- **[C_01] 90년대 교복:** `1990s dark navy school uniform jacket, white shirt, dark trousers`

**3. 감정 및 연기**
- **[E_01] 몽상:** `eyes slightly unfocused looking into distance, soft relaxed expression`
- **[E_02] 집중:** `eyes down on sketchbook, slight tension in brow, lip slightly bitten`

**4. 금지 요소**
`short cropped hair, adult appearance, modern clothing, bright eye color, inconsistent face`

---

## ⚙️ 시스템 적용 방식
- 시놉시스/스토리보드 작성 시 프롬프트에 모든 외형을 적지 않습니다.
- 프롬프트 생성 에이전트는 `[ACTOR_01] + [C_01] + [E_01]` 의 조합값을 이 바이블에서 읽어와 자동으로 영문 프롬프트로 병합(Merge)합니다.
- 이를 통해 각 씬마다 프롬프트가 길어지는 것을 방지하고, 일관성을 극대화합니다.
