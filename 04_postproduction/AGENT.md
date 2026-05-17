# 04_postproduction — Postproduction Agent 운영 가이드

## 이 폴더의 역할

영상의 **감정을 완성**하는 단계다.  
편집, 사운드, 자막, 색보정으로 최종 완성본을 만든다.

---

## 사용 에이전트

`agents/postproduction_agent.md` 참조

---

## 사용 툴

| 목적    | 툴          |
| ----- | ---------- |
| 영상 편집 | CapCut     |
| 음성 생성 | ElevenLabs |
| 음악 생성 | Suno       |
| 자막    | CapCut 내장  |

---

## 폴더 구조

```
04_postproduction/
├── AGENT.md
├── templates/
│   └── postproduction_template.md
└── edit_guides/
    ├── [프로젝트명]_edit_guide.md
    ├── [프로젝트명]_music_brief.md
    └── [프로젝트명]_subtitle_guide.md
```

---

## 작업 순서

1. `03_production/takes/[프로젝트명]/take_log.md` 읽기
2. FINAL take 파일 목록 확인
3. Postproduction Agent 프롬프트 실행
4. 편집 가이드 문서 생성
5. Suno에서 음악 생성
6. ElevenLabs에서 음성 생성 (필요 시)
7. CapCut에서 편집 실행
8. 완성본 `assets/exports/`에 저장
9. Director Agent에게 완료 보고

---

## 완성본 파일명 규칙

```
[프로젝트명]_v1.0.mp4    ← 첫 완성본
[프로젝트명]_v1.1.mp4    ← 자막/색감 수정
[프로젝트명]_v2.0.mp4    ← 씬 변경 등 Major 수정
```

---

## 완료 기준

- [ ] 편집 가이드 작성 완료
- [ ] 음악 브리프 작성 및 Suno 생성 완료
- [ ] 자막 가이드 작성 완료
- [ ] CapCut 편집 완료
- [ ] 완성본 v1.0 출력 완료
- [ ] 오디오 레벨 확인 (-14 LUFS 기준)
- [ ] 최종 시청 및 감독 승인
