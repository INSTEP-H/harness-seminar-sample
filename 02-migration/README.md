# MAFIA Migration harness

Claude Code 기반 레거시 마이그레이션 자동화 파이프라인.

> 별도 repo의 레거시 코드베이스를 타겟 스택으로 모듈 단위로 이관할 때 사용합니다.

> 하네스와 파이프라인에 대한 자세한 설명은 [영상](https://www.youtube.com/watch?v=CfLhrS0ww5w)을 참고해주세요.

## Quick Start

1. 플러그인을 설치합니다.

   ```sh
   # claude code 실행
   claude

   # 플러그인 설치
   /plugin marketplace add vibemafiaclub/mafia-migration-harness
   /plugin install mafia-migration
   ```

2. `docs/legacy-project.yaml`, `docs/migration-policy.yaml`, `docs/target-conventions.yaml`, `docs/target-adr.yaml`을 복사한 뒤 상황에 맞게 수정합니다.
3. Claude Code에서 `/mafia-migration:auto <module-id>`를 실행하세요.

## 파이프라인 흐름

```
/mafia-migration:auto <module-id>
  → [1] 상태 점검 (legacy-project.yaml 검증)
  → [2] Specify (Sub-agent)        — 레거시 코드 → 기능 명세
  → [3] Explore (Sub-agent)        — 타겟 컨벤션·관련 ADR 수집
  → [4] Plan (Opus Sub-agent)      — 명세 + 컨텍스트로 설계
  → [5] Implement (Sonnet, main)   — 설계 기반 구현
  → [6] Verify (Sub-agent)         — 명세 체크리스트 + 스크린샷 회귀
```

## 모델 분리

설계는 고성능 모델, 구현은 효율 모델로 분리해 비용을 줄이면서 품질을 유지합니다.

| 단계      | 모델             | 이유                     |
| --------- | ---------------- | ------------------------ |
| Specify   | sonnet           | 텍스트 추출·요약 작업    |
| Explore   | sonnet           | 코드 검색·분류 작업      |
| Plan      | **opus**         | 설계 품질이 결과를 좌우  |
| Implement | sonnet           | 분량 큼, 비용 민감       |
| Verify    | sonnet           | 규칙 비교 + 시각 회귀    |

## Skill 목록

| 커맨드                          | 설명                                |
| ------------------------------- | ----------------------------------- |
| `/mafia-migration:auto`         | 전체 파이프라인 오케스트레이션      |
| `/mafia-migration:specify`      | 레거시 코드 → 기능 명세 추출        |
| `/mafia-migration:explore`      | 타겟 코드베이스 컨텍스트 수집       |
| `/mafia-migration:plan`         | 마이그레이션 구현 계획 작성         |
| `/mafia-migration:implement`    | 계획 기반 구현                      |
| `/mafia-migration:verify`       | 명세 체크리스트 + 시각 회귀 검증    |
| `/mafia-migration:update-docs`  | policy / convention / ADR 항목 관리 |

## 산출물

작업별 산출물은 `.migration-artifacts/{module-id}/`에 저장됩니다.

- `legacy-spec.md` — 레거시 기능 명세 (작업 명세서)
- `target-context.md` — 타겟 컨벤션·관련 ADR (참고 자료집)
- `migration-plan.md` — 구현 계획서
- `verification-report.md` — 검증 보고서

## License

MIT
