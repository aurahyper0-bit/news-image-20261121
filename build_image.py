#!/usr/bin/env python3
"""Draw the news-image-20261121 front page and save it as entry.png.

A one-image front page summing up 21 November 2026 world news:
a dark masthead, one large lead story, three columns underneath,
and a strip of shorter items along the bottom.
"""
import os

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
PLAIN = os.path.join(FONT_DIR, "DejaVuSans.ttf")

W, H = 1024, 1024
MARGIN = 44
BG = (16, 18, 24)
PANEL = (26, 32, 48)
WHITE = (245, 245, 245)
GREY = (205, 208, 214)
DIM = (150, 155, 165)
RED = (214, 48, 49)
RULE = (70, 76, 90)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap: returns a list of lines fitting max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    title_f = font(BOLD, 52)
    title = "THE WORLD IN ONE IMAGE"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 26), title, font=title_f, fill=WHITE)

    date_f = font(BOLD, 26)
    date = "Friday, 21 November 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 96), date, font=date_f, fill=RED)
    d.line([(MARGIN, 142), (W - MARGIN, 142)], fill=RULE, width=2)

    # --- lead story ---
    head_f = font(BOLD, 56)
    lead_head = "Iran strikes US bases in Bahrain"
    y = draw_lines(d, wrap(d, lead_head, head_f, W - 2 * MARGIN),
                   head_f, MARGIN, 162, WHITE, 64)

    body_f = font(PLAIN, 24)
    lead_body = (
        "Revolutionary Guards said they hit two US positions (al-Riffa, Awali); "
        "Bahrain said a civilian industrial site caught fire, no injuries, "
        "and air defences intercepted other attacks."
    )
    y = draw_lines(d, wrap(d, lead_body, body_f, W - 2 * MARGIN),
                   body_f, MARGIN, y + 14, GREY, 32)
    d.line([(MARGIN, y + 18), (W - MARGIN, y + 18)], fill=RULE, width=2)

    # --- three columns ---
    cols = [
        ("Mexico captures 'El Chapo Isidro'",
         "Fausto Isidro Meza Flores, FBI 10 most wanted, captured in Guasave, "
         "Sinaloa, with US intelligence help; at least 11 died in the violence "
         "that followed."),
        ("Missile hits Kryvyi Rih",
         "Russian ballistic missile struck Zelenskyy's hometown, killing 2 "
         "(incl. a 7-year-old boy) and wounding 60 in a double-tap attack."),
        ("COP31 talks into overtime",
         "Antalya summit missed its deadline, no deal yet; earlier draft did "
         "not mention fossil fuels."),
    ]
    col_w = (W - 2 * MARGIN - 2 * 28) // 3
    col_y = y + 44
    col_h_f = font(BOLD, 25)
    col_b_f = font(PLAIN, 21)
    for i, (heading, body) in enumerate(cols):
        x = MARGIN + i * (col_w + 28)
        d.rectangle([(x, col_y), (x + 44, col_y + 6)], fill=RED)
        y2 = draw_lines(d, wrap(d, heading, col_h_f, col_w),
                        col_h_f, x, col_y + 16, WHITE, 30)
        draw_lines(d, wrap(d, body, col_b_f, col_w),
                   col_b_f, x, y2 + 8, GREY, 27)

    # --- bottom strip ---
    strip_y = 820
    d.rectangle([(0, strip_y), (W, 978)], fill=PANEL)
    strip_f = font(BOLD, 27)
    d.text((MARGIN, strip_y + 16), "ALSO TODAY", font=strip_f, fill=WHITE)
    strip_b_f = font(PLAIN, 21)
    strip = (
        "US stocks slide into correction (Nasdaq erased 2026 gains) \u2022 "
        "drones hit Russian cargo ship Sparta II in the Gulf of Finland \u2022 "
        "EU\u2013Indonesia sign trade deal (98.5% of tariffs on EU goods removed) \u2022 "
        "Anthropic mathematician claims AI-assisted Riemann proof "
        "(worded as a claim)"
    )
    draw_lines(d, wrap(d, strip, strip_b_f, W - 2 * MARGIN),
               strip_b_f, MARGIN, strip_y + 52, GREY, 27)

    # --- footer ---
    foot_f = font(PLAIN, 18)
    foot = "Compiled from major wire reports \u2022 21 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 988), foot, font=foot_f, fill=DIM)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print(f"wrote {out} {W}x{H}")


if __name__ == "__main__":
    main()
