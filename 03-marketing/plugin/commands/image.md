# Image (이미지 프롬프트 + 생성)

brief와 draft를 입력으로 이미지 프롬프트를 생성하고 `nanobanana` MCP로 이미지를 생성한다.

## 사용법

```
/mafia-marketing:image <topic-slug>
```

## 실행 방식

이 skill은 sub-agent에 위임하여 실행한다.
이미지 생성에는 `nanobanana` MCP의 `generate_image` 툴을 사용한다.

## 절차

1. `.content-artifacts/{topic-slug}/brief.md`, `draft.md`가 존재하는지 확인한다.
2. `nanobanana` MCP가 사용 가능한지 확인한다. 사용 불가 시 단계를 중단하고 사용자에게 보고한다.
3. **sub-agent를 호출**하여 다음을 수행한다:
   - brief의 `image_tone`과 채널별 비율(channel-formats.yaml)을 입력으로 받는다.
   - 채널별로 필요한 이미지 수와 비율을 계산한다.
     - 예: threads 1:1 1장 + linkedin 1.91:1 1장
   - 각 이미지에 대해 프롬프트를 생성한다. 프롬프트 작성 원칙:
     - 텍스트(타이포그래피)는 이미지에 넣지 않는 것을 default로 한다. (필요 시 brief에서 명시)
     - 브랜드 톤(도발·단정)을 비주얼 메타포로 옮긴다.
     - "VMC", "바이브마피아클럽" 등의 텍스트를 임의로 이미지에 박지 않는다.
   - `nanobanana` MCP의 `generate_image`를 각 프롬프트로 호출한다.
   - 생성된 이미지 파일을 `.content-artifacts/{topic-slug}/images/{channel}-{n}.{ext}` 형태로 저장한다.
4. 생성된 이미지와 프롬프트 목록을 사용자에게 제시한다.
5. 사용자가 재생성을 요청하면 프롬프트 수정 또는 변형 옵션을 제안하고 다시 호출한다.
6. 사용자 수락 후 `image-prompts.md`를 작성한다.

## 산출물 경로

```
.content-artifacts/{topic-slug}/images/{channel}-{n}.{ext}
.content-artifacts/{topic-slug}/images/image-prompts.md
```

## image-prompts.md 구조

```markdown
# Image Prompts — {topic-slug}

## threads-1.png (1:1)
- 의도: ...
- 프롬프트: ...
- 비율: 1:1
- 사용 도구: nanobanana

## linkedin-1.png (1.91:1)
- 의도: ...
- 프롬프트: ...
- 비율: 1.91:1
- 사용 도구: nanobanana
```

## 제약

- `nanobanana` MCP만 사용한다. 다른 이미지 도구를 임의로 시도하지 않는다.
- channel-formats의 이미지 비율 규칙을 준수한다. 위반 시 review 단계에서 FAIL 처리된다.
- 이미지에 텍스트를 박을 때는 사용자 확인을 별도로 받는다 (오타·자모 손상이 잦음).
