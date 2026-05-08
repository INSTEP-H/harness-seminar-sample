"""frame-composer 폴백: 9:16 PNG 프레임을 합성한다.

이번 회차 변경:
- F1: 5장 카드 뒷면 (3-2 grid)
- F2: 5초 다이나믹 카운트다운 — 25 sub-frame (200ms × 25 = 5.0s)
- F3: 선택된 카드(The Lovers) 확대 + reading body
- F4: CTA + 3장 노출

총 길이: 2.5 + 5.0 + 6.0 + 2.5 = 16.0s
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "images" / "raw"
OUT = ROOT / "images" / "composed"
OUT.mkdir(parents=True, exist_ok=True)
COUNT_DIR = OUT / "_count"
COUNT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
BG = (59, 27, 27)
BG_DEEP = (38, 16, 16)
CREAM = (244, 233, 216)
GOLD = (212, 162, 76)
GOLD_DIM = (164, 124, 58)
GOLD_BRIGHT = (236, 196, 110)

SAFE_TOP = int(H * 0.08)
SAFE_BOTTOM = int(H * 0.22)
SAFE_SIDE = int(W * 0.06)

FONT_TITLE_PATH = "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf"
FONT_BODY_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"


def load_font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size, index=index)
    except OSError:
        return ImageFont.truetype(path, size)


def make_background() -> Image.Image:
    img = Image.new("RGB", (W, H), BG_DEEP)
    cx, cy = W / 2, H / 2
    max_d = math.hypot(cx, cy)
    px = img.load()
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - cx, y - cy) / max_d
            t = max(0.0, 1.0 - d * 0.55)
            r = int(BG_DEEP[0] + (BG[0] - BG_DEEP[0]) * t)
            g = int(BG_DEEP[1] + (BG[1] - BG_DEEP[1]) * t)
            b = int(BG_DEEP[2] + (BG[2] - BG_DEEP[2]) * t)
            px[x, y] = (r, g, b)
    return img


def draw_logo(img: Image.Image) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    title_font = load_font(FONT_TITLE_PATH, 44)
    cx = W // 2
    margin_top = int(H * 0.04)
    sym_r = 14
    sym_y = margin_top + 12
    draw.ellipse((cx - sym_r, sym_y - sym_r, cx + sym_r, sym_y + sym_r),
                 outline=GOLD, width=2)
    cres = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cres)
    cd.ellipse((cx - 8, sym_y - 8, cx + 8, sym_y + 8), fill=(244, 233, 216, 200))
    cd.ellipse((cx - 4, sym_y - 12, cx + 12, sym_y + 4), fill=(0, 0, 0, 0))
    img.paste(cres, (0, 0), cres)
    text = "DAILY  TAROT"
    bbox = draw.textbbox((0, 0), text, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2, sym_y + 22), text, font=title_font, fill=CREAM)
    draw.line((cx - tw // 2, sym_y + 22 + (bbox[3] - bbox[1]) + 10,
               cx + tw // 2, sym_y + 22 + (bbox[3] - bbox[1]) + 10),
              fill=GOLD_DIM, width=1)


def fit_card(src: Image.Image, target_w: int, target_h: int) -> Image.Image:
    return src.resize((target_w, target_h), Image.LANCZOS)


def draw_index_badge(img: Image.Image, x: int, y: int, n: int) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    badge_font = load_font(FONT_BODY_PATH, 22)
    label = f"{n}"
    pad_x, pad_y = 14, 6
    bbox = draw.textbbox((0, 0), label, font=badge_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bw = tw + pad_x * 2
    bh = th + pad_y * 2
    bx = x - bw // 2
    by = y - bh - 6
    draw.rounded_rectangle((bx, by, bx + bw, by + bh), 8,
                           fill=(38, 16, 16, 220), outline=GOLD, width=1)
    draw.text((bx + pad_x - bbox[0], by + pad_y - bbox[1]), label,
              font=badge_font, fill=GOLD)


def place_grid_3_2(img: Image.Image, cards: list[Image.Image],
                   center_y: int, card_w: int = 260, card_h: int = 390,
                   gap_x: int = 20, gap_y: int = 22,
                   show_index: bool = True) -> None:
    assert len(cards) == 5
    total_w_top = card_w * 3 + gap_x * 2
    start_x_top = (W - total_w_top) // 2
    top_y = center_y - card_h - gap_y // 2
    for i in range(3):
        x = start_x_top + i * (card_w + gap_x)
        sized = fit_card(cards[i], card_w, card_h)
        img.paste(sized, (x, top_y))
        if show_index:
            draw_index_badge(img, x + card_w // 2, top_y, i + 1)
    total_w_bot = card_w * 2 + gap_x
    start_x_bot = (W - total_w_bot) // 2
    bot_y = center_y + gap_y // 2
    for i in range(2):
        x = start_x_bot + i * (card_w + gap_x)
        sized = fit_card(cards[3 + i], card_w, card_h)
        img.paste(sized, (x, bot_y))
        if show_index:
            draw_index_badge(img, x + card_w // 2, bot_y, 4 + i)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
              max_w: int) -> list[str]:
    lines: list[str] = []
    paragraphs = text.split("\n")
    for para in paragraphs:
        if not para.strip():
            lines.append("")
            continue
        cur = ""
        for ch in para:
            test = cur + ch
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] > max_w and cur:
                lines.append(cur)
                cur = ch
            else:
                cur = test
        if cur:
            lines.append(cur)
    return lines


def draw_centered_title(img: Image.Image, text: str, top_y: int,
                        max_w: int, size: int = 56) -> int:
    draw = ImageDraw.Draw(img)
    font = load_font(FONT_TITLE_PATH, size)
    lines = wrap_text(draw, text, font, max_w)
    line_h = int(size * 1.3)
    y = top_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((W // 2 - tw // 2, y), line, font=font, fill=CREAM)
        y += line_h
    return y


def draw_body_paragraphs(img: Image.Image, text: str, top_y: int,
                         max_w: int, size: int = 36) -> int:
    draw = ImageDraw.Draw(img)
    font = load_font(FONT_BODY_PATH, size)
    line_h = int(size * 1.55)
    y = top_y
    paragraphs = text.split("\n\n")
    for pi, para in enumerate(paragraphs):
        lines = wrap_text(draw, para.strip(), font, max_w)
        for line in lines:
            draw.text((SAFE_SIDE + (max_w - draw.textbbox((0, 0), line, font=font)[2]) // 2,
                       y),
                      line, font=font, fill=CREAM)
            y += line_h
        if pi != len(paragraphs) - 1:
            y += int(size * 0.6)
    return y


# ---------------------- frames -----------------------

def frame_1() -> Image.Image:
    img = make_background()
    draw_logo(img)
    title_y = int(H * 0.16)
    draw_centered_title(img, "요즘 티 안내고\n나를 좋아하는 사람",
                        title_y, W - 2 * SAFE_SIDE, size=78)
    back = Image.open(RAW / "card-back.png").convert("RGB")
    cards = [back] * 5
    place_grid_3_2(img, cards, center_y=int(H * 0.56), show_index=True)
    return img


def frame_2_base() -> Image.Image:
    """카운트다운 베이스: 5장 미리보기 카드 + 타이틀.
    카운트다운 숫자는 별도로 sub-frame당 합성."""
    img = make_background()
    draw_logo(img)
    title_y = int(H * 0.16)
    draw_centered_title(img, "직관적으로 끌리는\n한 장을 골라보세요",
                        title_y, W - 2 * SAFE_SIDE, size=68)
    cards = [Image.open(RAW / f"card-preview-{i}.png").convert("RGB")
             for i in range(1, 6)]
    place_grid_3_2(img, cards, center_y=int(H * 0.56), show_index=True)
    return img


def overlay_countdown(base: Image.Image, n: int, t: float) -> Image.Image:
    """카운트다운 숫자 오버레이.

    n: 표시할 숫자 (5..1)
    t: 0.0~1.0, 해당 숫자가 나타난 후 경과 비율 (0=막 등장, 1=다음 숫자로 넘어가기 직전)
    """
    img = base.copy().convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)

    # 숫자 위치 — 카드 그리드 아래
    cx = W // 2
    cy = int(H * 0.86)

    # 펄스 애니메이션:
    # - 등장(0~0.15): scale 0.55 → 1.05, alpha 0 → 1
    # - 안정(0.15~0.6): scale 1.05 → 1.0
    # - 박동(0.6~0.85): scale 1.0 → 1.06
    # - 페이드(0.85~1.0): scale 1.06 → 1.0, alpha 1 → 0.5
    if t < 0.15:
        k = t / 0.15
        scale = 0.55 + (1.05 - 0.55) * (k ** 0.5)
        alpha = int(255 * k)
    elif t < 0.6:
        k = (t - 0.15) / 0.45
        scale = 1.05 - (1.05 - 1.0) * k
        alpha = 255
    elif t < 0.85:
        k = (t - 0.6) / 0.25
        scale = 1.0 + 0.06 * math.sin(math.pi * k)
        alpha = 255
    else:
        k = (t - 0.85) / 0.15
        scale = 1.06 - 0.06 * k
        alpha = int(255 * (1.0 - 0.5 * k))

    base_size = 220
    size = max(40, int(base_size * scale))

    font = load_font(FONT_TITLE_PATH, size)
    label = str(n)

    # 골드 후광 (글로우)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    glow_r = int(140 * scale)
    glow_alpha = int(120 * (alpha / 255))
    gd.ellipse((cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r),
               fill=(*GOLD, glow_alpha // 3))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(40))
    img.alpha_composite(glow_layer)

    # 외곽 골드 링 (펄스)
    ring_r = int(120 * scale)
    ring_alpha = alpha
    rd = ImageDraw.Draw(canvas)
    rd.ellipse((cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r),
               outline=(*GOLD, ring_alpha), width=4)
    rd.ellipse((cx - ring_r + 12, cy - ring_r + 12,
                cx + ring_r - 12, cy + ring_r - 12),
               outline=(*GOLD_DIM, ring_alpha), width=1)

    # 숫자 (중앙 정렬)
    bbox = d.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer)
    td.text((cx - tw // 2 - bbox[0], cy - th // 2 - bbox[1]),
            label, font=font, fill=(*GOLD_BRIGHT, alpha))
    img.alpha_composite(canvas)
    img.alpha_composite(text_layer)

    # 진행 호 (12시 시작, 시계방향, 남은 비율만큼)
    arc_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ad = ImageDraw.Draw(arc_layer)
    ar = ring_r + 18
    # 0 → 360도, t에 비례
    sweep = 360 * (1 - t)
    # PIL: arc start=0이 3시 방향. 12시는 -90.
    ad.arc((cx - ar, cy - ar, cx + ar, cy + ar),
           start=-90, end=-90 + sweep,
           fill=(*GOLD_BRIGHT, ring_alpha), width=6)
    img.alpha_composite(arc_layer)

    return img.convert("RGB")


def frame_3() -> Image.Image:
    img = make_background()
    draw_logo(img)
    revealed = Image.open(RAW / "card-revealed.png").convert("RGB")
    card_w, card_h = 460, 690
    card_x = (W - card_w) // 2
    card_y = int(H * 0.17)
    sized = revealed.resize((card_w, card_h), Image.LANCZOS)
    img.paste(sized, (card_x, card_y))
    draw = ImageDraw.Draw(img, "RGBA")
    badge_font = load_font(FONT_TITLE_PATH, 36)
    label = "3번"
    bbox = draw.textbbox((0, 0), label, font=badge_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 22, 10
    bw = tw + pad_x * 2
    bh = th + pad_y * 2
    bx = (W - bw) // 2
    by = card_y - bh - 12
    draw.rounded_rectangle((bx, by, bx + bw, by + bh), 10,
                           fill=(38, 16, 16, 220), outline=GOLD, width=2)
    draw.text((bx + pad_x - bbox[0], by + pad_y - bbox[1]),
              label, font=badge_font, fill=GOLD)

    body = (
        "이 카드를 고른 당신, 요즘 가까이에서 당신의 하루를\n"
        "조용히 지켜봐 주는 사람이 있는 것 같아요.\n\n"
        "그 사람의 마음 안쪽에는 \"내가 너무 티 내면 어쩌지\" 하는\n"
        "망설임이 한 줄 남아 있어요.\n"
        "그래서 인사도, 챙김도 늘 한 발짝 모자란 듯 다가오는 거예요.\n\n"
        "곧 그 사람의 작은 신호가 한 번 더 보일 거예요.\n"
        "조금만 기다려보세요. 답은 의외로 가까이에 있어요."
    )
    body_top = card_y + card_h + 30
    draw_body_paragraphs(img, body, body_top, W - 2 * SAFE_SIDE, size=34)
    return img


def frame_4() -> Image.Image:
    img = make_background()
    draw_logo(img)
    title_y = int(H * 0.20)
    draw_centered_title(img, "더 궁금한 카드가 있으셨나요",
                        title_y, W - 2 * SAFE_SIDE, size=58)
    card_w, card_h = 280, 420
    gap_x = 30
    total_w = card_w * 3 + gap_x * 2
    start_x = (W - total_w) // 2
    row_y = int(H * 0.42)
    for i, n in enumerate([2, 3, 4]):
        c = Image.open(RAW / f"card-preview-{n}.png").convert("RGB")
        sized = c.resize((card_w, card_h), Image.LANCZOS)
        x = start_x + i * (card_w + gap_x)
        img.paste(sized, (x, row_y))
        draw_index_badge(img, x + card_w // 2, row_y, n)
    cta_y = row_y + card_h + 60
    draw_centered_title(img, "댓글로 카드 번호를 남겨주세요",
                        cta_y, W - 2 * SAFE_SIDE, size=44)
    draw = ImageDraw.Draw(img)
    sub_font = load_font(FONT_BODY_PATH, 28)
    sub = "해석은 DM으로 보내드릴게요"
    bbox = draw.textbbox((0, 0), sub, font=sub_font)
    sw = bbox[2] - bbox[0]
    draw.text((W // 2 - sw // 2, cta_y + 76), sub, font=sub_font, fill=GOLD)
    return img


def main() -> None:
    # 정적 프레임
    builders = {"frame-1.png": frame_1,
                "frame-3.png": frame_3,
                "frame-4.png": frame_4}
    for name, fn in builders.items():
        img = fn()
        path = OUT / name
        img.save(path, "PNG", optimize=True)
        print(f"wrote {path} ({path.stat().st_size // 1024} KB)")

    # F2 base + 카운트다운 sub-frame 25장 (5초 × 5fps)
    base = frame_2_base()
    base.save(OUT / "frame-2.png", "PNG", optimize=True)
    print(f"wrote {OUT / 'frame-2.png'} (base, no countdown)")

    # 5초 × 5fps = 25 sub-frames; 각 숫자(5..1)당 5장
    sub_per_sec = 5
    total = 5 * sub_per_sec
    for i in range(total):
        sec = i // sub_per_sec  # 0..4
        n = 5 - sec  # 5,4,3,2,1
        t = (i % sub_per_sec) / sub_per_sec  # 0, 0.2, 0.4, 0.6, 0.8
        # 한 숫자는 정확히 1초간 펄스 (t=0..1)
        out = overlay_countdown(base, n, t + 1.0 / sub_per_sec * 0)
        # 더 자연스러운 펄스: t를 0~1 범위로 매핑
        t_normalized = (i % sub_per_sec + 1) / sub_per_sec  # 0.2, 0.4, 0.6, 0.8, 1.0
        out = overlay_countdown(base, n, t_normalized)
        path = COUNT_DIR / f"f2-c{n}-{i % sub_per_sec:02d}.png"
        out.save(path, "PNG", optimize=True)
    print(f"wrote {total} countdown sub-frames -> {COUNT_DIR}")


if __name__ == "__main__":
    main()
