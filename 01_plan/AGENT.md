# 01_plan — Plan Agent 운영 가이드

## 이 폴더의 역할

모든 프로젝트의 **기준 데이터**를 저장한다.  
후속 모든 단계는 이 폴더의 `plan.md`를 참조한다.

---

## 사용 에이전트

`agents/plan_agent.md` 참조

---

## 폴더 구조

```
01_plan/
├── AGENT.md          ← 이 파일
├── templates/
│   └── plan_template.md   ← plan.md 작성 템플릿
└── projects/
    └── [프로젝트명]/
        ├── plan.md
        ├── director_brief.md
        └── revision_log.md
```

---

## 작업 순서

1. `templates/plan_template.md` 복사
2. `projects/[프로젝트명]/plan.md`로 저장
3. Plan Agent 프롬프트 실행 (Qwen Studio)
4. 생성된 내용으로 plan.md 작성
5. `bibles/character_bible.md` 업데이트
6. `bibles/world_bible.md` 업데이트
7. Director Agent에게 완료 보고

---

## 완료 기준

- [ ] plan.md — Character 섹션 완성
- [ ] plan.md — World 섹션 완성
- [ ] plan.md — Style 섹션 완성
- [ ] plan.md — Scene Structure 완성
- [ ] character_bible.md 업데이트 완료
- [ ] world_bible.md 업데이트 완료
- [ ] Director Brief 작성 완료
