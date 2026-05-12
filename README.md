# Harness Seminar Sample

Claude Code 기반 하네스(harness) 세미나 샘플 모음입니다.
각 디렉터리는 서로 다른 도메인에 맞게 설계된 독립 실행 가능한 Claude Code 플러그인을 포함합니다.

> 하네스와 파이프라인에 대한 자세한 설명은 [영상](https://www.youtube.com/watch?v=CfLhrS0ww5w)을 참고해주세요.

## 하네스 목록

### [01-codereview](./01-codereview)

PR 작성부터 코드리뷰, 반영, QA까지를 자동화하는 **코드리뷰 파이프라인**.

```sh
/plugin marketplace add vibemafiaclub/mafia-codereview-harness
/plugin install mafia-codereview

# Claude Code 안에서
/mafia-codereview:auto
```

### [02-migration](./02-migration)

레거시 코드베이스를 모듈 단위로 타겟 스택으로 옮길 때 사용하는 **마이그레이션 파이프라인**.
Specify → Explore → Plan → Implement → Verify 단계별로 모델을 분리해 비용과 품질을 함께 챙깁니다.

```sh
/plugin marketplace add vibemafiaclub/mafia-migration-harness
/plugin install mafia-migration

# Claude Code 안에서
/mafia-migration:auto <module-id>
```

### [03-marketing](./03-marketing)

타로/사주 운세 릴스(reels) 콘텐츠 제작을 자동화하는 **마케팅 파이프라인**.
주제 선정 → 기획 → 카피 → 이미지 생성/합성 → mp4 렌더 → 검수까지 한 번에 진행합니다.

```sh
/plugin marketplace add vibemafiaclub/mafia-marketing-harness
/plugin install mafia-marketing

# Claude Code 안에서
/auto
```

> 외부 의존: `nanobanana` MCP, ImageMagick(또는 Pillow/sharp), `ffmpeg`

## 디렉터리 구조

```
.
├── 01-codereview/   # 코드리뷰 하네스 (플러그인 + 문서)
├── 02-migration/    # 마이그레이션 하네스 (플러그인 + 문서)
├── 03-marketing/    # 마케팅 하네스 (플러그인 + 문서)
└── practices/       # 세미나 실습용 자료
```

각 하네스 디렉터리의 `README.md`에서 파이프라인 흐름, Skill 목록, 산출물 구조 등 세부 사용법을 확인할 수 있습니다.

## License

MIT
