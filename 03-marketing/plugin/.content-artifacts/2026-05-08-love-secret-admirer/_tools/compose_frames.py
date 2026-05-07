"""frame-composer 폴백: 4개의 9:16 프레임 PNG를 합성한다.

- 캔버스: 1080x1920 (channel-formats.reels.canvas)
- safe_zones: top 8% / bottom 22% / side 6%
- 배경: #3B1B1B, 텍스트: #F4E9D8, 강조: #D4A24C
- title_font: AppleMyungjo (serif, 한글 명조)
- body_font: AppleSDGothicNeo (sans-serif, 한글 고딕)
- 로고: 텍스트 로고 "DAILY TAROT" + 골드 sun-moon 모티프 (assets/brand-logo.svg 부재)
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "images" / "raw"
OUT = ROOT / "images" / "composed"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
BG = (59, 27, 27)
BG_DEEP = (38, 16, 16)
CREAM = (244, 233, 216)
GOLD = (212, 162, 76)
GOLD_DIM = (164, 124, 58)

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
    # subtle vignette
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
    """Top-center brand logo (text + small sun-moon symbol)."""
    draw = ImageDraw.Draw(img, "RGBA")
    title_font = load_font(FONT_TITLE_PATH, 44)
    cx = W // 2
    margin_top = int(H * 0.04)
    # symbol — circle with crescent
    sym_r = 14
    sym_y = margin_top + 12
    draw.ellipse((cx - sym_r, sym_y - sym_r, cx + sym_r, sym_y + sym_r),
                 outline=GOLD, width=2)
    # crescent inside
    cres = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cres)
    cd.ellipse((cx - 8, sym_y - 8, cx + 8, sym_y + 8), fill=(244, 233, 216, 200))
    cd.ellipse((cx - 4, sym_y - 12, cx + 12, sym_y + 4), fill=(0, 0, 0, 0))
    img.paste(cres, (0, 0), cres)
    # wordmark
    text = "DAILY  TAROT"
    bbox = draw.textbbox((0, 0), text, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw // 2, sym_y + 22), text, font=title_font, fill=CREAM)
    # underline accent
    draw.line((cx - tw // 2, sym_y + 22 + (bbox[3] - bbox[1]) + 10,
               cx + tw // 2, sym_y + 22 + (bbox[3] - bbox[1]) + 10),
              fill=GOLD_DIM, width=1)


def fit_card(src: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resize a 2:3 card to fit target dimensions, preserving ratio."""
    return src.resize((target_w, target_h), Image.LANCZOS)


def draw_index_badge(img: Image.Image, x: int, y: int, n: int) -> None:
    """Small gold-bordered index badge above a card."""
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
                   center_y: int, card_w: int = 280, card_h: int = 420,
                   gap_x: int = 20, gap_y: int = 28,
                   show_index: bool = True) -> None:
    """Place 5 cards in 3 (top) + 2 (bottom) grid centered horizontally."""
    assert len(cards) == 5
    # top row of 3
    total_w_top = card_w * 3 + gap_x * 2
    start_x_top = (W - total_w_top) // 2
    top_y = center_y - card_h - gap_y // 2
    for i in range(3):
        x = start_x_top + i * (card_w + gap_x)
        sized = fit_card(cards[i], card_w, card_h)
        img.paste(sized, (x, top_y))
        if show_index:
            draw_index_badge(img, x + card_w // 2, top_y, i + 1)
    # bottom row of 2
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
    """Greedy wrap by character (Korean has no spaces between words)."""
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
    """Body text supporting paragraph breaks (\\n\\n)."""
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
            y += int(size * 0.6)  # paragraph gap
    return y


def frame_1() -> Image.Image:
    """hook — question + 5 card-backs grid."""
    img = make_background()
    draw_logo(img)

    # title (question)
    title_y = int(H * 0.16)
    draw_centered_title(img, "요즘 티 안내고\n나를 좋아하는 사람",
                        title_y, W - 2 * SAFE_SIDE, size=78)

    # 5 card-backs
    back = Image.open(RAW / "card-back.png").convert("RGB")
    cards = [back] * 5
    place_grid_3_2(img, cards, center_y=int(H * 0.56),
                   card_w=260, card_h=390, gap_y=22, show_index=True)

    return img


def frame_2() -> Image.Image:
    """selection — question_full + 5 distinct preview cards."""
    img = make_background()
    draw_logo(img)

    title_y = int(H * 0.16)
    draw_centered_title(img, "직관적으로 끌리는\n한 장을 골라보세요",
                        title_y, W - 2 * SAFE_SIDE, size=68)

    cards = [Image.open(RAW / f"card-preview-{i}.png").convert("RGB")
             for i in range(1, 6)]
    place_grid_3_2(img, cards, center_y=int(H * 0.56),
                   card_w=260, card_h=390, gap_y=22, show_index=True)

    return img


def frame_3() -> Image.Image:
    """reveal — selected card (n=3) enlarged + reading body."""
    img = make_background()
    draw_logo(img)

    # selected card (centered, larger)
    revealed = Image.open(RAW / "card-revealed.png").convert("RGB")
    card_w, card_h = 460, 690  # 2:3
    card_x = (W - card_w) // 2
    card_y = int(H * 0.17)
    sized = revealed.resize((card_w, card_h), Image.LANCZOS)
    img.paste(sized, (card_x, card_y))
    # index "3번" badge above the card
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

    # reading body below
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
    """cta — 3 cards in row + cta text."""
    img = make_background()
    draw_logo(img)

    # title above row
    title_y = int(H * 0.20)
    draw_centered_title(img, "더 궁금한 카드가 있으셨나요",
                        title_y, W - 2 * SAFE_SIDE, size=58)

    # 3 cards (preview 2, 3, 4) horizontally
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

    # cta text below
    cta_y = row_y + card_h + 60
    draw_centered_title(img, "댓글로 카드 번호를 남겨주세요",
                        cta_y, W - 2 * SAFE_SIDE, size=44)
    # supporting muted line
    draw = ImageDraw.Draw(img)
    sub_font = load_font(FONT_BODY_PATH, 28)
    sub = "해석은 DM으로 보내드릴게요"
    bbox = draw.textbbox((0, 0), sub, font=sub_font)
    sw = bbox[2] - bbox[0]
    draw.text((W // 2 - sw // 2, cta_y + 76), sub, font=sub_font, fill=GOLD)

    return img


def main() -> None:
    builders = [frame_1, frame_2, frame_3, frame_4]
    for n, fn in enumerate(builders, start=1):
        img = fn()
        path = OUT / f"frame-{n}.png"
        img.save(path, "PNG", optimize=True)
        print(f"wrote {path} ({path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
