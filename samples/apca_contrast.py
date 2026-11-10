#!/usr/bin/env python3
"""Text-contrast gate: WCAG 2 ratio and APCA lightness contrast (Lc), with a size/weight floor.

Why both: WCAG ratio is the familiar yardstick for UI; APCA is perceptual and polarity-aware, so it
catches thin light type on strong colour that still 'passes' WCAG. The studio measures this on the
ENCODED video frame (not on the design inputs) before a card is accepted. This sample works on two
sRGB colours. APCA constants are the public APCA-W3 0.1.9 values (github.com/Myndex/SAPC-APCA).
Run the self-test:  python3 apca_contrast.py
"""
K = dict(trc=2.4, r=0.2126729, g=0.7151522, b=0.0721750, normBG=0.56, normTXT=0.57, revTXT=0.62,
         revBG=0.65, blkThrs=0.022, blkClmp=1.414, scale=1.14, offset=0.027, loClip=0.1, dY=0.0005)


def apca_y(rgb):
    r, g, b = (c / 255.0 for c in rgb)
    return r ** K["trc"] * K["r"] + g ** K["trc"] * K["g"] + b ** K["trc"] * K["b"]


def _clamp(y):
    return y + (K["blkThrs"] - y) ** K["blkClmp"] if y < K["blkThrs"] else y


def apca_lc(text_rgb, bg_rgb):
    """Signed Lc: positive = dark text on light background, negative = light text on dark."""
    yt, yb = _clamp(apca_y(text_rgb)), _clamp(apca_y(bg_rgb))
    if abs(yb - yt) < K["dY"]:
        return 0.0
    if yb > yt:
        s = (yb ** K["normBG"] - yt ** K["normTXT"]) * K["scale"]
        return 0.0 if s < K["loClip"] else (s - K["offset"]) * 100
    s = (yb ** K["revBG"] - yt ** K["revTXT"]) * K["scale"]
    return 0.0 if s > -K["loClip"] else (s + K["offset"]) * 100


def wcag_ratio(a, b):
    def rel(rgb):
        c = [v / 255.0 for v in rgb]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    hi, lo = sorted((rel(a), rel(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


# Minimum |Lc| by font size (px on the canvas) and weight column; thinner and smaller needs more.
FLOOR = {40: {300: None, 400: 90, 600: 75}, 64: {300: 90, 400: 60, 600: 55}, 104: {300: 60, 400: 45, 600: 45}}


def passes(text_rgb, bg_rgb, size, weight_col):
    floor = FLOOR[size][weight_col]
    if floor is None:
        return False, "this size/weight is not allowed"
    lc = abs(apca_lc(text_rgb, bg_rgb))
    return lc >= floor, "Lc %.1f vs floor %d" % (lc, floor)


if __name__ == "__main__":
    white, black = (255, 255, 255), (0, 0, 0)
    assert round(wcag_ratio(white, black), 1) == 21.0
    assert abs(apca_lc(black, white) - 106.0) < 1.0        # reference value for black on white
    assert abs(apca_lc(white, black) + 107.9) < 1.0        # reference value for white on black
    assert passes(white, (139, 26, 26), 64, 400)[0]        # white on dark red, regular weight
    assert not passes((200, 200, 200), white, 64, 300)[0]  # light grey thin type on white
    print("apca_contrast: 5 checks passed")
