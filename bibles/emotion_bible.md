# Emotion Bible
## 감정 설계 시스템

> 영상의 힘은 감정에서 온다. 모든 씬은 감정을 먼저 정의한다.

---

## 감정 스펙트럼

```
기쁨 ←————————————→ 슬픔
희망 ←————————————→ 절망
평화 ←————————————→ 긴장
사랑 ←————————————→ 분노
용기 ←————————————→ 두려움
```

---

## 감정별 시각 언어

| 감정 | 색감 | 조명 | 카메라 | 음악 템포 |
|------|------|------|--------|---------|
| 기쁨 | 밝은 노랑, 크림 | 밝고 고른 조명 | 와이드, 로우 앵글 | 빠름 |
| 슬픔 | 차가운 블루, 그레이 | 어둡고 단방향 | 클로즈업, 하이 앵글 | 느림 |
| 희망 | 오렌지, 골드 | 황혼, 역광 | 크레인 업, 와이드 | 점진적 상승 |
| 절망 | 탈색, 흑백 근접 | 최소 조명 | 더치 앵글, 핸드헬드 | 불규칙 |
| 평화 | 소프트 그린, 크림 | 부드러운 자연광 | 스태틱, 미디엄 | 없거나 매우 느림 |
| 긴장 | 고채도 레드, 딥 블루 | 강한 대비 | 핸드헬드, 클로즈업 | 빠르고 불규칙 |
| 그리움 | 따뜻한 앰버, 세피아 | 골든 아워 | 슬로우 달리 아웃 | 중간, 멜로딕 |
| 용기 | 클리어 블루, 화이트 | 전면 밝은 조명 | 로우 앵글, 크레인 | 점진적 강화 |

---

## 감정 프롬프트 키워드 라이브러리

```markdown
## 기쁨
pensive smile, bright eyes, warm expression, 
cheerful atmosphere, vibrant colors, lively movement

## 슬픔
downcast eyes, trembling lip, heavy silence,
melancholic atmosphere, muted colors, still movement

## 희망
eyes lifting toward light, quiet determination,
dawn breaking, soft golden glow, slow rising movement

## 긴장
tight jaw, rapid eye movement, heightened alertness,
sharp shadows, high contrast, quick cuts

## 평화
relaxed features, soft breath, stillness,
gentle wind, soft natural light, imperceptible movement

## 그리움
distant gaze, half-smile of memory, gentle sorrow,
warm faded tones, slow motion, quiet reflection
```

---

## 감정 아크 설계

### 3막 구조
```
Act 1 (Setup):     현재 감정 상태 확립
                   [예: 두려움, 외로움]
        ↓
Act 2 (Journey):   감정 변화와 도전
                   [예: 두려움 → 갈등 → 용기]
        ↓
Act 3 (Resolution): 감정 해소 또는 전환
                   [예: 용기 → 평화, 또는 슬픔의 수용]
```

### 단순 구조 (Shorts 60초)
```
감정 A (0-20초) → 전환점 (20-40초) → 감정 B (40-60초)
```

---

## 사용 규칙

1. 씬 작성 전 감정 먼저 정의
2. 감정 색감 → world_bible 색감 팔레트에 반영
3. 감정 카메라 → camera_bible 참조
4. 급격한 감정 전환 씬에는 반드시 전환 씬(transition scene) 추가
