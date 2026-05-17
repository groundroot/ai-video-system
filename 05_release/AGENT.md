# 05_release — Release Agent 운영 가이드

## 이 폴더의 역할

완성 영상을 **업로드하고 데이터를 수집**한다.  
분석 결과는 다음 프로젝트의 plan.md에 반영된다.

---

## 사용 에이전트

`agents/release_agent.md` 참조

---

## 사용 툴

| 목적 | 툴 |
|------|-----|
| 장편 업로드 | YouTube |
| 숏츠 업로드 | Instagram Reels / YouTube Shorts |
| 분석 | YouTube Analytics |

---

## 폴더 구조

```
05_release/
├── AGENT.md
├── templates/
│   └── release_template.md
└── analytics/
    ├── [프로젝트명]_week1_report.md
    └── [프로젝트명]_feedback.md
```

---

## 작업 순서

1. `assets/exports/[프로젝트명]_v1.0.mp4` 확인
2. Release Agent 프롬프트 실행
3. 제목/설명/태그 생성
4. 썸네일 제작 (Canva)
5. 플랫폼별 업로드
6. 1주일 후 분석 데이터 수집
7. `analytics/[프로젝트명]_week1_report.md` 작성
8. 다음 프로젝트 피드백 문서 작성

---

## 업로드 체크리스트

- [ ] 완성본 파일 확인 (`_FINAL` 버전)
- [ ] 해상도 및 비율 확인
- [ ] 오디오 레벨 확인
- [ ] 제목 작성 (50자 이내 권장)
- [ ] 설명 작성 (CTA 포함)
- [ ] 태그 작성 (15-20개)
- [ ] 썸네일 업로드
- [ ] 자막 파일 업로드 (SRT)
- [ ] 카테고리 설정
- [ ] 예약 또는 즉시 발행

---

## 완료 기준

- [ ] 플랫폼 업로드 완료
- [ ] URL 기록
- [ ] 1주 후 분석 보고서 작성
- [ ] 피드백 문서 작성
- [ ] 프로젝트 아카이브 (`assets/archive/`)
