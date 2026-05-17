# 02_preproduction — Preproduction Agent 운영 가이드

## 이 폴더의 역할

`plan.md`를 기반으로 **정적 시각 설계**를 완성한다.  
이미지 프롬프트 생성, 스토리보드 제작, 이미지 생성 결과 관리.

---

## 사용 에이전트

`agents/preproduction_agent.md` 참조

---

## 사용 툴

| 목적 | 툴 |
|------|-----|
| AI 이미지 생성 | Qwen Studio |
| 콘셉트 아트 | Qwen Image |
| 스토리보드 레이아웃 | Canva |
| 결과 정리 | Obsidian |

---

## 폴더 구조

```
02_preproduction/
├── AGENT.md
├── templates/
│   └── preproduction_template.md
├── storyboards/
│   └── [프로젝트명]_storyboard.md
└── image_prompts/
    └── [프로젝트명]_prompts.md
```

---

## 작업 순서

1. `01_plan/projects/[프로젝트명]/plan.md` 읽기
2. Preproduction Agent 프롬프트 실행
3. 씬별 이미지 프롬프트 생성
4. Qwen Studio에서 이미지 생성
5. 결과 이미지 `assets/characters/` 또는 `assets/worlds/`에 저장
6. 스토리보드 문서 작성
7. Director Agent에게 완료 보고

---

## 파일 저장 규칙

```
scene_01_v1.png   ← 첫 번째 시도
scene_01_v2.png   ← 수정 버전
scene_01_v3.png   ← 최종 선택
```

최종 선택 파일에 `_FINAL` 태그:
```
scene_01_v3_FINAL.png
```

---

## 완료 기준

- [ ] 전 씬 이미지 프롬프트 작성 완료
- [ ] 전 씬 이미지 최소 1장 이상 생성 완료
- [ ] 스토리보드 문서 작성 완료
- [ ] character_bible 일관성 확인 완료
- [ ] world_bible 일관성 확인 완료
