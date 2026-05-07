# Migration Harness

이 프로젝트는 Claude Code 기반 레거시 마이그레이션 자동화 파이프라인이다.
설계는 고성능 모델(Opus), 구현은 효율 모델(Sonnet)로 분리해 비용을 낮추면서 품질을 유지한다.

## 산출물 경로

모든 산출물은 `.migration-artifacts/{module-id}/` 하위에 저장한다.
`{module-id}`는 사용자가 지정한 마이그레이션 단위(예: `order`, `auth`)이며, `docs/legacy-project.yaml`의 `modules[].id`와 일치해야 한다.

산출물 목록:
- `legacy-spec.md` — 레거시 기능 명세 (작업 명세서)
- `target-context.md` — 타겟 컨벤션·관련 ADR (참고 자료집)
- `migration-plan.md` — 구현 계획서
- `verification-report.md` — 검증 보고서

## 참조 문서

- `docs/legacy-project.yaml` — 레거시 프로젝트 메타정보 (repo path, tech stack, 모듈 정의)
- `docs/migration-policy.yaml` — 마이그레이션 방침 (1:1 vs 재설계, 데드코드 처리, 데이터 전략)
- `docs/target-conventions.yaml` — 타겟 스택 코딩 컨벤션
- `docs/target-adr.yaml` — 타겟 코드베이스의 설계 결정

## 파이프라인 규칙

1. `legacy-project.yaml`의 `path`는 read-only로 다룬다. 레거시 repo를 절대 수정하지 않는다.
2. Sub-agent로 실행하는 단계(specify, explore, verify)는 산출물 디렉토리(`.migration-artifacts/{module-id}/`)에만 쓰기를 수행한다. 본 프로젝트의 소스 코드를 수정하지 않는다.
3. `plan` 단계는 **opus** 모델을 사용하는 sub-agent에게 위임하여 설계 품질을 확보한다.
4. `implement` 단계는 **sonnet** 모델을 사용한다. 분량이 크면 도메인 단위로 sub-agent를 추가 분할한다.
5. `verify`는 (a) `legacy-spec.md`의 기능 항목을 그대로 체크리스트로 변환한 항목별 통과 여부 확인 + (c) UI 모듈에 한해 스크린샷 회귀를 모두 수행한다.
6. 사용자에게 확인을 요청할 때, 모호하여 구체화가 필요한 논의점을 반드시 함께 정리하여 전달한다.
7. base branch는 사용자가 명시하지 않으면 `main`을 기본으로 한다.
