"""nanobanana 폴백: Pillow로 카드 raw 이미지 7장을 절차 생성.

- card-back, card-preview-1..5, card-revealed (= preview-3 확대 변형)
- 2:3 비율, 600x900px
- 다크 버건디 배경 + 골드 테두리 + 카드별 모티프
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "images" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 600, 900
CORNER_R = int(W * 0.08)  # 8% radius
GOLD = (212, 162, 76)
GOLD_DIM = (164, 124, 58)
BURGUNDY_BG = (59, 27, 27)
BURGUNDY_DEEP = (38, 16, 16)
CREAM = (244, 233, 216)
MUSK = (139, 90, 60)


def card_canvas(bg_inner: tuple[int, int, int] | None = None) -> Image.Image:
    """Burgundy gradient card with rounded corners and gold border."""
    bg = bg_inner or BURGUNDY_BG
    img = Image.new("RGB", (W, H), BURGUNDY_DEEP)
    draw = ImageDraw.Draw(img)
    # radial-ish vignette: lighter center, darker edges
    cx, cy = W / 2, H / 2
    max_d = math.hypot(cx, cy)
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - cx, y - cy) / max_d
            t = max(0.0, 1.0 - d * 0.9)
            r = int(BURGUNDY_DEEP[0] + (bg[0] - BURGUNDY_DEEP[0]) * t)
            g = int(BURGUNDY_DEEP[1] + (bg[1] - BURGUNDY_DEEP[1]) * t)
            b = int(BURGUNDY_DEEP[2] + (bg[2] - BURGUNDY_DEEP[2]) * t)
            img.putpixel((x, y), (r, g, b))
    # rounded mask
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, W - 1, H - 1), CORNER_R, fill=255)
    out = Image.new("RGB", (W, H), (0, 0, 0))
    out.paste(img, (0, 0), mask)
    # gold border (1.5% width visually)
    border = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(border)
    bd.rounded_rectangle((4, 4, W - 5, H - 5), CORNER_R - 2, outline=GOLD, width=4)
    out_rgba = out.convert("RGBA")
    out_rgba.alpha_composite(border)
    return out_rgba.convert("RGB")


def card_back() -> Image.Image:
    img = card_canvas()
    draw = ImageDraw.Draw(img, "RGBA")
    cx, cy = W // 2, H // 2

    # outer ring
    draw.ellipse((cx - 170, cy - 170, cx + 170, cy + 170), outline=GOLD, width=3)
    draw.ellipse((cx - 140, cy - 140, cx + 140, cy + 140), outline=GOLD_DIM, width=1)

    # sun rays (simple radiating lines)
    for i in range(16):
        a = math.radians(i * (360 / 16))
        x1 = cx + math.cos(a) * 95
        y1 = cy + math.sin(a) * 95
        x2 = cx + math.cos(a) * 130
        y2 = cy + math.sin(a) * 130
        draw.line((x1, y1, x2, y2), fill=GOLD, width=2)

    # central sun disc
    draw.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=BURGUNDY_DEEP, outline=GOLD, width=2)
    # crescent moon overlay (offset cream disc + burgundy mask to suggest crescent)
    moon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(moon)
    md.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=(244, 233, 216, 170))
    md.ellipse((cx - 30, cy - 60, cx + 70, cy + 40), fill=(0, 0, 0, 0))
    img.paste(moon, (0, 0), moon)
    # corner ornaments (small diamond at each inner corner)
    for (x, y) in [(40, 40), (W - 40, 40), (40, H - 40), (W - 40, H - 40)]:
        draw.polygon([(x, y - 8), (x + 8, y), (x, y + 8), (x - 8, y)], fill=GOLD)
    # subtle outer art-deco arches at top/bottom
    for k, base_y in enumerate([60, H - 60]):
        draw.arc((W // 2 - 60, base_y - 12, W // 2 + 60, base_y + 12), 0, 360, fill=GOLD_DIM, width=1)
    return img


def _scene_card(draw_fn, bg=None) -> Image.Image:
    img = card_canvas(bg)
    draw_fn(img)
    return img


def _draw_path(img: Image.Image) -> None:
    """길/도로 — 비 온 뒤 골목길, 멀리 가로등."""
    draw = ImageDraw.Draw(img, "RGBA")
    # ground perspective: trapezoid
    draw.polygon([(W * 0.45, H * 0.55), (W * 0.55, H * 0.55),
                  (W * 0.85, H * 0.92), (W * 0.15, H * 0.92)],
                 fill=(70, 40, 36))
    # wet reflection band
    for i in range(8):
        y = int(H * (0.62 + i * 0.04))
        x_l = int(W * (0.45 - i * 0.04))
        x_r = int(W * (0.55 + i * 0.04))
        draw.line((x_l, y, x_r, y), fill=(180, 130, 70, 60), width=2)
    # distant lantern glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = W // 2, int(H * 0.5)
    for r in range(120, 0, -8):
        a = max(8, int(120 - r))
        gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(212, 162, 76, a))
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    img.paste(glow, (0, 0), glow)
    # walls hinted by darker side rectangles
    draw.rectangle((0, int(H * 0.25), int(W * 0.30), int(H * 0.92)), fill=(48, 22, 22))
    draw.rectangle((int(W * 0.70), int(H * 0.25), W, int(H * 0.92)), fill=(48, 22, 22))


def _draw_water(img: Image.Image) -> None:
    """물가 — 호숫가 + 종이배."""
    draw = ImageDraw.Draw(img, "RGBA")
    # water bands (horizontal gradient stripes)
    for i in range(16):
        y = int(H * 0.45 + i * 18)
        if y >= H - 20:
            break
        alpha = 70 + (i % 4) * 18
        draw.line((40, y, W - 40, y), fill=(120, 160, 170, alpha), width=2)
    # horizon line
    draw.line((40, int(H * 0.45), W - 40, int(H * 0.45)), fill=(180, 140, 90), width=1)
    # paper boat (triangular)
    bx, by = W // 2, int(H * 0.65)
    draw.polygon([(bx - 50, by + 18), (bx + 50, by + 18), (bx + 30, by + 36), (bx - 30, by + 36)],
                 fill=CREAM)
    draw.polygon([(bx - 30, by + 18), (bx, by - 30), (bx + 30, by + 18)], fill=CREAM)
    draw.line((bx, by - 30, bx, by + 18), fill=GOLD, width=1)
    # ripple
    for r in range(20, 90, 14):
        draw.ellipse((bx - r, by + 30 - r // 5, bx + r, by + 30 + r // 5),
                     outline=(212, 162, 76, 80), width=1)


def _draw_plant(img: Image.Image) -> None:
    """꽃/식물 — 책상 위 화분, 비스듬한 햇빛."""
    draw = ImageDraw.Draw(img, "RGBA")
    # desk surface
    draw.rectangle((0, int(H * 0.72), W, H), fill=(78, 50, 40))
    draw.line((0, int(H * 0.72), W, int(H * 0.72)), fill=GOLD_DIM, width=2)
    # slanted sunlight beam (parallelogram, soft)
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    bd.polygon([(int(W * 0.05), 0), (int(W * 0.55), 0),
                (int(W * 0.85), int(H * 0.95)), (int(W * 0.35), int(H * 0.95))],
               fill=(244, 233, 216, 30))
    beam = beam.filter(ImageFilter.GaussianBlur(18))
    img.paste(beam, (0, 0), beam)
    # pot
    pot_x = W // 2
    pot_top = int(H * 0.55)
    pot_bot = int(H * 0.78)
    draw.polygon([(pot_x - 80, pot_top), (pot_x + 80, pot_top),
                  (pot_x + 60, pot_bot), (pot_x - 60, pot_bot)],
                 fill=MUSK, outline=GOLD, width=2)
    # plant leaves (soft ellipses)
    leaf_color = (130, 150, 100)
    for dx, dy, w, h, ang in [
        (-40, -40, 80, 130, -25),
        (10, -90, 70, 140, 10),
        (50, -30, 70, 110, 30),
        (-10, -110, 50, 100, -5),
    ]:
        leaf = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        ld = ImageDraw.Draw(leaf)
        ld.ellipse((100 - w // 2, 100 - h // 2, 100 + w // 2, 100 + h // 2),
                   fill=leaf_color + (220,))
        leaf = leaf.rotate(ang, resample=Image.BICUBIC)
        img.paste(leaf, (pot_x + dx - 100, pot_top + dy - 100), leaf)
    # tiny golden bloom highlights
    for (dx, dy) in [(-20, -120), (30, -80), (60, -10)]:
        cx_, cy_ = pot_x + dx, pot_top + dy
        draw.ellipse((cx_ - 6, cy_ - 6, cx_ + 6, cy_ + 6), fill=GOLD)


def _draw_room(img: Image.Image) -> None:
    """실내 공간 — 커튼 사이 빛, 빈 의자."""
    draw = ImageDraw.Draw(img, "RGBA")
    # back wall slightly lighter
    draw.rectangle((0, 0, W, int(H * 0.78)), fill=(70, 36, 32))
    # floor
    draw.rectangle((0, int(H * 0.78), W, H), fill=(50, 26, 22))
    draw.line((0, int(H * 0.78), W, int(H * 0.78)), fill=GOLD_DIM, width=1)
    # curtain — vertical light stripes in cream alpha
    curtain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curtain)
    for i in range(6):
        x = int(W * 0.55) + i * 20
        cd.rectangle((x, 30, x + 12, int(H * 0.78)),
                     fill=(244, 233, 216, 35 + (i % 3) * 12))
    curtain = curtain.filter(ImageFilter.GaussianBlur(2))
    img.paste(curtain, (0, 0), curtain)
    # light beam through curtain (diagonal)
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    bd.polygon([(int(W * 0.55), 30), (int(W * 0.85), 30),
                (int(W * 0.55), int(H * 0.92)), (int(W * 0.30), int(H * 0.92))],
               fill=(244, 233, 216, 22))
    beam = beam.filter(ImageFilter.GaussianBlur(20))
    img.paste(beam, (0, 0), beam)
    # chair silhouette (left)
    cx_ = int(W * 0.30)
    cy_ = int(H * 0.62)
    draw.rectangle((cx_ - 50, cy_, cx_ + 50, cy_ + 70), fill=(40, 18, 16))
    draw.rectangle((cx_ - 50, cy_ - 80, cx_ - 35, cy_), fill=(40, 18, 16))
    draw.rectangle((cx_ + 35, cy_ - 80, cx_ + 50, cy_), fill=(40, 18, 16))
    # chair leg
    draw.line((cx_ - 40, cy_ + 70, cx_ - 40, int(H * 0.92)), fill=(40, 18, 16), width=4)
    draw.line((cx_ + 40, cy_ + 70, cx_ + 40, int(H * 0.92)), fill=(40, 18, 16), width=4)


def _draw_city(img: Image.Image) -> None:
    """도시 야경 — 창가, 도시 불빛."""
    draw = ImageDraw.Draw(img, "RGBA")
    # window frame
    draw.rectangle((40, 40, W - 40, H - 40), outline=GOLD_DIM, width=3)
    # cross mullions
    draw.line((W // 2, 40, W // 2, H - 40), fill=GOLD_DIM, width=2)
    draw.line((40, H // 2, W - 40, H // 2), fill=GOLD_DIM, width=2)
    # buildings silhouette
    rng = random.Random(7)
    base_y = int(H * 0.62)
    x = 60
    while x < W - 60:
        bw = rng.randint(28, 56)
        bh = rng.randint(80, 220)
        draw.rectangle((x, base_y - bh, x + bw, base_y), fill=(28, 12, 12))
        # window lights
        for wy in range(base_y - bh + 14, base_y - 10, 18):
            for wx in range(x + 6, x + bw - 6, 14):
                if rng.random() < 0.45:
                    draw.rectangle((wx, wy, wx + 5, wy + 6),
                                   fill=(240, 200, 110))
        x += bw + 6
    # ground city glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rectangle((40, base_y - 4, W - 40, base_y + 4), fill=(212, 162, 76, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    img.paste(glow, (0, 0), glow)
    # condensation streaks (faint)
    for sx in [W * 0.30, W * 0.55, W * 0.78]:
        draw.line((sx, 60, sx + 4, H - 60), fill=(244, 233, 216, 40), width=2)


def card_revealed_from(preview: Image.Image) -> Image.Image:
    """preview-3을 reveal용으로 약간 확대·디테일 강화."""
    base = preview.copy()
    # sharpen-ish: slight contrast boost via overlay
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # extra warm rim glow
    for r in range(W // 2, W // 2 - 200, -10):
        a = max(0, int(80 - (W // 2 - r) * 0.6))
        od.ellipse((W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r),
                   outline=(212, 162, 76, a // 2), width=2)
    overlay = overlay.filter(ImageFilter.GaussianBlur(6))
    base = base.convert("RGBA")
    base.alpha_composite(overlay)
    return base.convert("RGB")


def main() -> None:
    files: list[tuple[str, Image.Image]] = []

    files.append(("card-back.png", card_back()))
    files.append(("card-preview-1.png", _scene_card(_draw_path)))
    files.append(("card-preview-2.png", _scene_card(_draw_water)))
    p3 = _scene_card(_draw_plant)
    files.append(("card-preview-3.png", p3))
    files.append(("card-preview-4.png", _scene_card(_draw_room)))
    files.append(("card-preview-5.png", _scene_card(_draw_city)))
    files.append(("card-revealed.png", card_revealed_from(p3)))

    for name, img in files:
        path = OUT / name
        img.save(path, "PNG", optimize=True)
        print(f"wrote {path} ({path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
