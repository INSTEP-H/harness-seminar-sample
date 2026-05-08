"""실제 RWS(라이더-웨이트-스미스) 카드를 브랜드 톤으로 마감해 7장의 raw 이미지를 만든다.

매핑:
- preview-1 (길/도로)        ← The Fool (0)
- preview-2 (물가)           ← The Star (XVII)
- preview-3 (꽃/식물, 선택) ← The Lovers (VI)
- preview-4 (실내 공간)      ← The Hermit (IX)
- preview-5 (도시 야경)      ← The Moon (XVIII)
- card-back                 ← 브랜드 자체 디자인 (아르누보 골드 패턴)
- card-revealed             ← The Lovers + 글로우 강화

Public domain: Pamela Colman Smith died 1951; RWS art is in the public domain
worldwide (life+70). Source: Wikimedia Commons.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "images" / "raw"
RWS = RAW / "_rws"

W, H = 600, 900
CORNER_R = int(W * 0.06)
GOLD = (212, 162, 76)
GOLD_DIM = (164, 124, 58)
GOLD_BRIGHT = (236, 196, 110)
BURGUNDY = (59, 27, 27)
BURGUNDY_DEEP = (38, 16, 16)
CREAM = (244, 233, 216)
PARCHMENT = (240, 224, 196)


def _radial_gradient(size: tuple[int, int], inner: tuple[int, int, int],
                     outer: tuple[int, int, int]) -> Image.Image:
    """Radial gradient — inner color at center, outer at corners."""
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    cx, cy = w / 2, h / 2
    max_d = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            t = math.hypot(x - cx, y - cy) / max_d
            t = min(1.0, t * 1.05)
            px[x, y] = (
                int(inner[0] + (outer[0] - inner[0]) * t),
                int(inner[1] + (outer[1] - inner[1]) * t),
                int(inner[2] + (outer[2] - inner[2]) * t),
            )
    return img


def _rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1),
                                        radius, fill=255)
    return m


def _vintage_treatment(art: Image.Image) -> Image.Image:
    """RWS 원화에 살짝 빈티지 톤. 너무 진하면 안 됨 — 카드 정체성 유지."""
    art = art.convert("RGB")
    # 살짝 채도 낮춤
    art = ImageEnhance.Color(art).enhance(0.92)
    # 살짝 따뜻한 sepia overlay
    sepia = Image.new("RGB", art.size, (212, 162, 76))
    art = Image.blend(art, sepia, 0.06)
    # 미세 비네팅
    vignette = _radial_gradient(art.size, (255, 255, 255), (160, 130, 100))
    art = Image.blend(art, vignette, 0.10)
    return art


def _ornate_corner(img: Image.Image, x: int, y: int, size: int,
                   rotate_deg: int = 0) -> None:
    """아르누보 풍 코너 장식: 작은 골드 곡선 + 다이아몬드."""
    layer = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # 곡선 두 개 (아르누보 ‘덩굴’ 모티프)
    d.arc((size * 0.05, size * 0.05, size * 1.6, size * 1.6), 180, 280,
          fill=GOLD, width=3)
    d.arc((size * 0.25, size * 0.25, size * 1.4, size * 1.4), 200, 290,
          fill=GOLD_DIM, width=2)
    # 끝의 작은 다이아몬드 (입자)
    d.polygon([(size * 1.45, size * 0.55), (size * 1.55, size * 0.65),
               (size * 1.45, size * 0.75), (size * 1.35, size * 0.65)],
              fill=GOLD_BRIGHT)
    layer = layer.rotate(rotate_deg, resample=Image.BICUBIC,
                         center=(size, size))
    img.paste(layer, (x - size, y - size), layer)


def _frame_card(art: Image.Image,
                bg: tuple[int, int, int] = BURGUNDY,
                ornate: bool = True) -> Image.Image:
    """600x900 브랜드 프레임에 art를 넣는다.

    레이아웃: burgundy gradient 배경 + 골드 이중 테두리 + 코너 아르누보 + 매팅 안의 RWS art.
    """
    canvas = _radial_gradient((W, H), bg, BURGUNDY_DEEP)
    canvas.paste(canvas, (0, 0), _rounded_mask((W, H), CORNER_R))
    out = Image.new("RGB", (W, H), (0, 0, 0))
    out.paste(canvas, (0, 0), _rounded_mask((W, H), CORNER_R))
    out = out.convert("RGBA")

    # 매팅 영역 (art가 들어갈 공간) — 8% 인셋
    mat_pad = int(W * 0.06)
    mat_box = (mat_pad, mat_pad, W - mat_pad, H - mat_pad)
    mat_w = mat_box[2] - mat_box[0]
    mat_h = mat_box[3] - mat_box[1]

    # art 비율 유지하며 매팅에 fit (letterbox, no crop)
    aw, ah = art.size
    scale = min(mat_w / aw, mat_h / ah)
    new_w, new_h = int(aw * scale), int(ah * scale)
    art_resized = art.resize((new_w, new_h), Image.LANCZOS)

    # 매팅 안쪽 배경 (약간 어두운 burgundy 매트)
    mat_layer = Image.new("RGBA", (mat_w, mat_h), (50, 22, 22, 255))
    mat_corners = _rounded_mask((mat_w, mat_h), int(W * 0.04))
    art_box = Image.new("RGBA", (mat_w, mat_h), (0, 0, 0, 0))
    art_box.paste(art_resized,
                  ((mat_w - new_w) // 2, (mat_h - new_h) // 2))
    art_box.putalpha(mat_corners)
    mat_layer.paste(art_box, (0, 0), art_box)
    mat_layer.putalpha(mat_corners)
    out.alpha_composite(mat_layer, (mat_box[0], mat_box[1]))

    # 골드 이중 테두리 (외곽)
    d = ImageDraw.Draw(out, "RGBA")
    d.rounded_rectangle((4, 4, W - 5, H - 5), CORNER_R - 2,
                        outline=GOLD, width=3)
    d.rounded_rectangle((10, 10, W - 11, H - 11), CORNER_R - 4,
                        outline=GOLD_DIM, width=1)
    # 매팅 안쪽 골드 라인 (액자 효과)
    d.rounded_rectangle((mat_box[0] - 2, mat_box[1] - 2,
                         mat_box[2] + 1, mat_box[3] + 1),
                        int(W * 0.04), outline=GOLD, width=2)

    if ornate:
        cs = 38
        _ornate_corner(out, 28, 28, cs, rotate_deg=0)
        _ornate_corner(out, W - 28, 28, cs, rotate_deg=90)
        _ornate_corner(out, W - 28, H - 28, cs, rotate_deg=180)
        _ornate_corner(out, 28, H - 28, cs, rotate_deg=270)

    return out.convert("RGB")


def card_back() -> Image.Image:
    """브랜드 카드 뒷면 — 아르누보 골드 패턴, 중앙 sun-moon."""
    canvas = _radial_gradient((W, H), BURGUNDY, BURGUNDY_DEEP)
    out = Image.new("RGB", (W, H), (0, 0, 0))
    out.paste(canvas, (0, 0), _rounded_mask((W, H), CORNER_R))
    out = out.convert("RGBA")
    d = ImageDraw.Draw(out, "RGBA")

    cx, cy = W // 2, H // 2

    # 외곽 이중 테두리
    d.rounded_rectangle((4, 4, W - 5, H - 5), CORNER_R - 2,
                        outline=GOLD, width=3)
    d.rounded_rectangle((14, 14, W - 15, H - 15), CORNER_R - 4,
                        outline=GOLD_DIM, width=1)

    # 안쪽 마름모 액자 (아르누보)
    diamond_pad_y = int(H * 0.10)
    diamond_pad_x = int(W * 0.10)
    pts = [
        (W // 2, diamond_pad_y),
        (W - diamond_pad_x, H // 2),
        (W // 2, H - diamond_pad_y),
        (diamond_pad_x, H // 2),
    ]
    d.polygon(pts, outline=GOLD, width=2)
    # 마름모 안쪽 라인 (이중)
    inner_pts = [(W // 2, diamond_pad_y + 14),
                 (W - diamond_pad_x - 14, H // 2),
                 (W // 2, H - diamond_pad_y - 14),
                 (diamond_pad_x + 14, H // 2)]
    d.polygon(inner_pts, outline=GOLD_DIM, width=1)

    # 중앙 외곽 원 (sun ray base)
    d.ellipse((cx - 130, cy - 130, cx + 130, cy + 130), outline=GOLD, width=2)
    d.ellipse((cx - 100, cy - 100, cx + 100, cy + 100),
              outline=GOLD_DIM, width=1)

    # 16방향 sun-rays (얇은 + 두꺼운 교대)
    for i in range(32):
        a = math.radians(i * (360 / 32))
        r1 = 102
        r2 = 128 if i % 2 == 0 else 122
        x1 = cx + math.cos(a) * r1
        y1 = cy + math.sin(a) * r1
        x2 = cx + math.cos(a) * r2
        y2 = cy + math.sin(a) * r2
        w = 2 if i % 2 == 0 else 1
        d.line((x1, y1, x2, y2), fill=GOLD, width=w)

    # 중앙 sun disc
    d.ellipse((cx - 78, cy - 78, cx + 78, cy + 78),
              fill=BURGUNDY_DEEP, outline=GOLD, width=2)

    # 그 안에 crescent moon (오프셋 마스크 트릭)
    moon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(moon)
    md.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), fill=CREAM + (210,))
    # crescent: 원에서 burgundy 원을 빼서 초승달
    cut = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cut)
    cd.ellipse((cx - 30, cy - 70, cx + 78, cy + 38),
               fill=(38, 16, 16, 255))
    moon.alpha_composite(cut)
    out.alpha_composite(moon)
    # 별 8각 (sun 안쪽 작은 별)
    for r, w in [(36, 2), (24, 1)]:
        for i in range(8):
            a = math.radians(i * 45)
            x1 = cx + math.cos(a) * r
            y1 = cy + math.sin(a) * r
            d.line((cx, cy, x1, y1), fill=GOLD, width=w)

    # 상하 작은 아르누보 모티프 (덩굴)
    for base_y in (60, H - 60):
        d.arc((W // 2 - 90, base_y - 18, W // 2 + 90, base_y + 18),
              0, 180, fill=GOLD_DIM, width=2)
        d.line((W // 2 - 90, base_y, W // 2 + 90, base_y),
               fill=GOLD_DIM, width=1)

    # 코너 다이아몬드 4개
    for (x, y) in [(50, 50), (W - 50, 50), (50, H - 50), (W - 50, H - 50)]:
        d.polygon([(x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)],
                  fill=GOLD)
        d.polygon([(x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)],
                  fill=GOLD_BRIGHT)

    # 4코너 아르누보 곡선
    cs = 40
    _ornate_corner(out, 30, 30, cs, rotate_deg=0)
    _ornate_corner(out, W - 30, 30, cs, rotate_deg=90)
    _ornate_corner(out, W - 30, H - 30, cs, rotate_deg=180)
    _ornate_corner(out, 30, H - 30, cs, rotate_deg=270)

    return out.convert("RGB")


def revealed_from(art: Image.Image) -> Image.Image:
    """F3용 reveal 카드: 브랜드 프레임 + 골드 글로우 후광."""
    framed = _frame_card(art, ornate=True).convert("RGBA")
    # 외곽에 살짝 골드 글로우
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(0, 24, 2):
        a = max(0, 90 - r * 4)
        gd.rounded_rectangle((r, r, W - 1 - r, H - 1 - r),
                             CORNER_R - r, outline=(*GOLD, a), width=2)
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    framed.alpha_composite(glow)
    return framed.convert("RGB")


def main() -> None:
    mapping = [
        ("card-preview-1.png", "00_Fool.jpg"),
        ("card-preview-2.png", "17_Star.jpg"),
        ("card-preview-3.png", "06_Lovers.jpg"),
        ("card-preview-4.png", "09_Hermit.jpg"),
        ("card-preview-5.png", "18_Moon.jpg"),
    ]
    arts: dict[str, Image.Image] = {}
    for out_name, src in mapping:
        src_path = RWS / src
        art = Image.open(src_path).convert("RGB")
        art = _vintage_treatment(art)
        framed = _frame_card(art, ornate=True)
        framed.save(RAW / out_name, "PNG", optimize=True)
        arts[out_name] = framed
        print(f"wrote {RAW / out_name} ({(RAW / out_name).stat().st_size // 1024} KB)")

    back = card_back()
    back.save(RAW / "card-back.png", "PNG", optimize=True)
    print(f"wrote {RAW / 'card-back.png'}")

    # revealed = preview-3 (The Lovers) 그대로 + glow
    lovers_art = _vintage_treatment(Image.open(RWS / "06_Lovers.jpg").convert("RGB"))
    revealed = revealed_from(lovers_art)
    revealed.save(RAW / "card-revealed.png", "PNG", optimize=True)
    print(f"wrote {RAW / 'card-revealed.png'}")


if __name__ == "__main__":
    main()
