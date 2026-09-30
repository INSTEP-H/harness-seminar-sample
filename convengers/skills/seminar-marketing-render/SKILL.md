---
name: seminar-marketing-render
description: 합성된 4 PNG 프레임과 reels 메타를 입력받아 ffmpeg로 인스타 릴스 발행용 mp4를 만든다. BGM이 brief에 지정되어 있으면 함께 합성한다.
---

> 원저작: VIBE MAFIA CLUB (https://github.com/vibemafiaclub/harness-seminar-sample). 라이선스는 원본 README의 License 절(MIT) 그대로입니다. 아래 원문과 저작권 표기는 손대지 않았습니다. 컨벤져스 키트용으로 스킬 이름만 바꿔 옮겼습니다.

# Render (mp4 비디오 렌더)

## 사용

```
/render <topic-slug>
```

## 실행 방식

이 skill은 `reels-renderer` sub-agent에 위임된다.

## 사전 점검

- 로컬 `ffmpeg` 미설치 시 단계 중단하고 보고.
- 4개 프레임 PNG가 모두 존재하고 1080×1920 해상도인지 확인.

## 절차

1. **`reels-renderer` sub-agent 호출**:
   - formatted/reels.md의 프레임별 duration 읽기
   - concat demuxer 입력 파일 작성
   - ffmpeg로 mp4 합성 (H.264 + yuv420p, fps=30)
   - brief의 `bgm` 블록(`pool_id` + `source_url` + `hook`) 기반으로 BGM 합성
     - source_url이 youtube면 `yt-dlp`로 받아 `_render/bgm-source.*`에 캐시
     - `hook.start_sec / duration_sec`로 후크 잘라내고 fade in/out 적용
     - 본 영상에 mix (volume_db, default -18dB; channel-formats.audio.bgm.volume_db)
   - `output.mp4` 저장
2. 결과(파일 경로, 총 길이, BGM 곡 정보)를 사용자에게 보고.

## 산출물 경로

```
.content-artifacts/{topic-slug}/output.mp4
.content-artifacts/{topic-slug}/_render/concat.txt
.content-artifacts/{topic-slug}/_render/silent.mp4   # BGM 합성 전 중간 산출물
```

## 제약

- ffmpeg 외 다른 비디오 도구를 임의로 사용하지 않는다.
- 출력은 9:16 (1080×1920), H.264 + AAC + yuv420p, 인스타 릴스 호환.
- 총 길이 18초(channel-formats.reels.duration_sec_total_max) 초과 시 보고하고 호출자 결정 대기.
- `_render/` 외부에 임시 파일을 만들지 않는다.
