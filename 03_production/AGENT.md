# 03_production — Production Agent 운영 가이드

## 이 폴더의 역할

스토리보드 이미지를 **움직이는 영상**으로 변환한다.  
액션 프롬프트 설계, 영상 생성, take 관리가 핵심이다.

---

## 사용 에이전트

`agents/production_agent.md` 참조

---

## 사용 툴

| 목적 | 툴 |
|------|-----|
| 영상 생성 (일반) | Wan |
| 영상 생성 (고품질) | Hunyuan |
| 노드 기반 생성 | ComfyUI |
| 프롬프트 설계 | Qwen Studio |

---

## 폴더 구조

```
03_production/
├── AGENT.md
├── templates/
│   └── production_template.md
├── action_prompts/
│   └── [프로젝트명]_action_prompts.md
└── takes/
    └── [프로젝트명]/
        ├── scene_01_take01.mp4
        ├── scene_01_take02.mp4
        └── take_log.md
```

---

## 작업 순서

1. `02_preproduction/image_prompts/[프로젝트명]_prompts.md` 읽기
2. 선택된 FINAL 이미지 파일 확인
3. Production Agent 프롬프트 실행
4. 씬별 액션 프롬프트 생성
5. Wan / Hunyuan에서 영상 생성
6. take 결과 기록
7. 최적 take 선택 → `_FINAL` 태그
8. Director Agent에게 완료 보고

---

## 파일 저장 규칙

```
scene_01_take01.mp4
scene_01_take02.mp4
scene_01_take03_FINAL.mp4   ← 최종 선택
```

---

## Take 평가 기준

| 항목 | 확인 사항 |
|------|---------|
| 움직임 | 자연스럽고 의도에 맞는가 |
| 캐릭터 일관성 | character_bible과 일치하는가 |
| 카메라 무브 | 설계한 무브먼트가 구현됐는가 |
| 배경 일관성 | world_bible과 일치하는가 |
| 감정 전달 | 씬 감정이 시각적으로 느껴지는가 |

---

## 완료 기준

- [ ] 전 씬 액션 프롬프트 작성 완료
- [ ] 전 씬 최소 take 1개 이상 생성
- [ ] 전 씬 FINAL take 선택 완료
- [ ] take_log.md 작성 완료
- [ ] 총 러닝타임 확인 (목표 ±10% 이내)
