#!/usr/bin/env python3
"""Generate the JNS mechanism and diagnostic figures as vector PDFs.

Figure 1 explicitly labels exact and schematic layers.  Figure 2 only reads
the tracked JSON artifact: it performs no RFDE solve, smoothing, or fit.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Sequence

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
DATA_FILE = REPOSITORY / "experiments/results/exact_chart_threshold_convergence.json"

BLUE = HexColor("#2A5C8A")
ORANGE = HexColor("#D06B32")
GRAY = HexColor("#6F7378")
LIGHT_GRAY = HexColor("#C6C9CC")
GRID_GRAY = HexColor("#E2E3E4")
PALE_BLUE = HexColor("#D9E8F2")
INK = HexColor("#202124")
WHITE = HexColor("#FFFFFF")


def register_fonts() -> None:
    base = Path("/usr/share/fonts/truetype/dejavu")
    fonts = {
        "DVSerif": base / "DejaVuSerif.ttf",
        "DVSerif-Bold": base / "DejaVuSerif-Bold.ttf",
    }
    for name, path in fonts.items():
        if not path.is_file():
            raise FileNotFoundError(f"Required embedded font is missing: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))
    math_font = Path("/usr/share/fonts/truetype/noto/NotoSansMath-Regular.ttf")
    if not math_font.is_file():
        raise FileNotFoundError(f"Required mathematical font is missing: {math_font}")
    pdfmetrics.registerFont(TTFont("NotoMath", str(math_font)))
    italic_font = Path("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf")
    if not italic_font.is_file():
        raise FileNotFoundError(f"Required italic font is missing: {italic_font}")
    pdfmetrics.registerFont(TTFont("MathItalic", str(italic_font)))


def metadata(pdf: canvas.Canvas, title: str, subject: str) -> None:
    pdf.setTitle(title)
    pdf.setAuthor("Haibo Lu")
    pdf.setSubject(subject)
    pdf.setCreator("ReportLab; manuscript/jns/figures/generate_figures.py")
    pdf.setKeywords("RFDE, canard, invariant history graph, transverse delay")


def text(pdf: canvas.Canvas, x: float, y: float, value: str, *, size: float = 7,
         font: str = "DVSerif", color: Color = INK, align: str = "left") -> None:
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    if align == "center":
        pdf.drawCentredString(x, y, value)
    elif align == "right":
        pdf.drawRightString(x, y, value)
    else:
        pdf.drawString(x, y, value)


def runs(pdf: canvas.Canvas, x: float, y: float,
         pieces: Sequence[tuple[str, str, float, float]], *,
         color: Color = INK, align: str = "left") -> None:
    """Draw inline font/size/baseline spans with deterministic alignment."""
    widths = [pdfmetrics.stringWidth(value, font, size)
              for value, font, size, _ in pieces]
    total = sum(widths)
    cursor = x - total / 2 if align == "center" else x - total if align == "right" else x
    for (value, font, size, dy), width in zip(pieces, widths):
        text(pdf, cursor, y + dy, value, size=size, font=font, color=color)
        cursor += width


def line(pdf: canvas.Canvas, x0: float, y0: float, x1: float, y1: float, *,
         color: Color = INK, width: float = .8, dash: Sequence[float] | None = None) -> None:
    pdf.setStrokeColor(color)
    pdf.setLineWidth(width)
    pdf.setDash([] if dash is None else list(dash))
    pdf.line(x0, y0, x1, y1)
    pdf.setDash([])


def polyline(pdf: canvas.Canvas, points: Sequence[tuple[float, float]], *,
             color: Color = INK, width: float = .8,
             dash: Sequence[float] | None = None) -> None:
    path = pdf.beginPath()
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    pdf.setStrokeColor(color)
    pdf.setLineWidth(width)
    pdf.setDash([] if dash is None else list(dash))
    pdf.drawPath(path, stroke=1, fill=0)
    pdf.setDash([])


def arrow(pdf: canvas.Canvas, x0: float, y0: float, x1: float, y1: float, *,
          color: Color = INK, width: float = .8, head: float = 4) -> None:
    line(pdf, x0, y0, x1, y1, color=color, width=width)
    angle, spread = math.atan2(y1 - y0, x1 - x0), .5
    p1 = (x1 - head * math.cos(angle - spread), y1 - head * math.sin(angle - spread))
    p2 = (x1 - head * math.cos(angle + spread), y1 - head * math.sin(angle + spread))
    path = pdf.beginPath()
    path.moveTo(x1, y1)
    path.lineTo(*p1)
    path.lineTo(*p2)
    path.close()
    pdf.setFillColor(color)
    pdf.drawPath(path, stroke=0, fill=1)


def double_arrow(pdf: canvas.Canvas, x0: float, y0: float, x1: float, y1: float) -> None:
    arrow(pdf, x0, y0, x1, y1, width=.65, head=3)
    arrow(pdf, x1, y1, x0, y0, width=.65, head=3)


def marker(pdf: canvas.Canvas, x: float, y: float, *, kind: str, color: Color,
           radius: float = 2.2, filled: bool = False) -> None:
    pdf.setLineWidth(.85)
    pdf.setStrokeColor(color)
    pdf.setFillColor(color if filled else WHITE)
    if kind == "square":
        pdf.rect(x - radius, y - radius, 2 * radius, 2 * radius, stroke=1, fill=1)
    else:
        pdf.circle(x, y, radius, stroke=1, fill=1)


def heading(pdf: canvas.Canvas, x: float, y: float, value: str) -> None:
    text(pdf, x, y, value, size=8.2, font="DVSerif-Bold")


def mechanism_panel_a(pdf: canvas.Canvas, x0: float, y0: float, w: float, h: float) -> None:
    heading(pdf, x0, y0 + h - 3, "(a)  Delay projection")
    left, right = x0 + 7, x0 + w - 5
    a, b = left + .34 * (right - left), left + .79 * (right - left)
    yc, yt = y0 + 103, y0 + 49
    line(pdf, left, yc, right, yc, width=.6)
    line(pdf, left, yt, right, yt, width=.6)
    line(pdf, a, yc, a, yc + 15, color=BLUE, width=2)
    line(pdf, b, yc, b, yc + 30, color=BLUE, width=2)
    marker(pdf, a, yc, kind="circle", color=BLUE, radius=1.8, filled=True)
    marker(pdf, b, yc, kind="circle", color=BLUE, radius=1.8, filled=True)
    text(pdf, a, yc + 19, "1/3", color=BLUE, size=6.8, align="center")
    text(pdf, b, yc + 34, "2/3", color=BLUE, size=6.8, align="center")
    runs(pdf, left, yc - 11,
         [("critical:  ", "DVSerif", 6.3, 0), ("ℓ", "MathItalic", 6.7, 0),
          ("T", "DVSerif", 4.1, 3.0), ("B", "DVSerif-Bold", 6.4, 0),
          ("η", "NotoMath", 4.6, -1.7), ("r", "MathItalic", 6.7, 0)],
         color=BLUE)
    text(pdf, right, yc + 18, "fixed", color=BLUE, size=6.3, align="right")
    arrow(pdf, a, yt, a, yt + 22, color=ORANGE, width=.9)
    arrow(pdf, b, yt, b, yt - 22, color=ORANGE, width=.9)
    text(pdf, a + 4, yt + 18, "+ηq", color=ORANGE, size=6.5)
    text(pdf, b - 4, yt - 23, "−ηq", color=ORANGE, size=6.5, align="right")
    runs(pdf, left, yt - 11,
         [("transverse:  ", "DVSerif", 6.1, 0), ("P⊥", "NotoMath", 6.5, 0),
          ("B", "DVSerif-Bold", 6.4, 0), ("η", "NotoMath", 4.6, -1.7),
          ("r", "MathItalic", 6.7, 0)],
         color=ORANGE)
    text(pdf, right, yt + 8, "changes", color=ORANGE, size=6.3, align="right")
    text(pdf, a, y0 + 20, "θ₀", size=6.7, align="center")
    text(pdf, b, y0 + 20, "θ₁", size=6.7, align="center")
    text(pdf, x0 + w / 2, y0 + 5, "atom weights 1/3, 2/3 fixed", size=5.8, align="center")
    text(pdf, x0 + w / 2, y0 - 3, "signed weights +eta q, -eta q vary", size=5.8, align="center")


def mechanism_panel_b(pdf: canvas.Canvas, x0: float, y0: float, w: float, h: float) -> None:
    heading(pdf, x0, y0 + h - 3, "(b)  Complete-history lift")
    text(pdf, x0 + w, y0 + h - 14, "schematic projection", color=GRAY, size=5.7, align="right")
    sheet = [(x0 + 15, y0 + 54), (x0 + 98, y0 + 43),
             (x0 + 132, y0 + 88), (x0 + 47, y0 + 101)]
    path = pdf.beginPath()
    path.moveTo(*sheet[0])
    for point in sheet[1:]:
        path.lineTo(*point)
    path.close()
    pdf.setFillColor(PALE_BLUE)
    pdf.setStrokeColor(BLUE)
    pdf.setLineWidth(.85)
    pdf.drawPath(path, stroke=1, fill=1)
    for segment in [((26, 65), (111, 54)), ((38, 83), (122, 70)),
                    ((36, 51), (76, 97)), ((73, 47), (111, 91))]:
        line(pdf, x0 + segment[0][0], y0 + segment[0][1],
             x0 + segment[1][0], y0 + segment[1][1], color=BLUE, width=.35)
    for xf, yf in [(43, 78), (72, 70), (103, 73)]:
        line(pdf, x0 + xf, y0 + yf + 47, x0 + xf, y0 + yf + 5,
             color=LIGHT_GRAY, width=.7)
        arrow(pdf, x0 + xf, y0 + yf + 29, x0 + xf, y0 + yf + 7,
              color=GRAY, width=.7, head=3.5)
    text(pdf, x0 + 88, y0 + 132, "stable fibres  A/δ", color=GRAY, size=6, align="center")
    history = [(x0 + 29 + 83 * z, y0 + 67 + 8 * math.sin(math.pi * z) + z)
               for z in [i / 80 for i in range(81)]]
    polyline(pdf, history, color=INK, width=1.35)
    arrow(pdf, *history[43], *history[54], color=INK, width=.8, head=3.8)
    marker(pdf, *history[0], kind="square", color=INK, radius=1.8, filled=True)
    marker(pdf, *history[-1], kind="circle", color=INK, radius=1.9, filled=True)
    text(pdf, history[0][0], history[0][1] - 10, "−θ₁", size=6.1, align="center")
    text(pdf, history[-1][0], history[-1][1] - 10, "0", size=6.1, align="center")
    runs(pdf, x0 + w / 2, y0 + 29,
         [("history lift  ", "DVSerif", 6.0, 0), ("ι", "NotoMath", 7.0, 0),
          ("δ,ν,η", "NotoMath", 4.7, -1.8), ("(u)", "NotoMath", 6.5, 0)],
         align="center")
    runs(pdf, x0 + w / 2 + 8, y0 + 105,
         [("h = ", "NotoMath", 6.5, 0), ("H", "MathItalic", 6.8, 0),
          ("δ,ν,η", "NotoMath", 4.6, -1.8),
          ("(u)", "NotoMath", 6.5, 0)], color=BLUE, align="center")
    text(pdf, x0 + 127, y0 + 44, "u₁", size=6.2)
    text(pdf, x0 + 31, y0 + 108, "u₂", size=6.2)
    text(pdf, x0 + 19, y0 + 137, "h", size=6.2)


def mechanism_panel_c(pdf: canvas.Canvas, x0: float, y0: float, w: float, h: float) -> None:
    heading(pdf, x0, y0 + h - 3, "(c)  One-sided connection")
    text(pdf, x0 + w, y0 + h - 14, "colored traces schematic", color=GRAY, size=5.7, align="right")
    left, right, bottom, top = x0 + 20, x0 + w - 5, y0 + 29, y0 + 145
    alpha = math.sqrt(6) / 4
    sx = lambda x: left + (x + 1.30) / 2.60 * (right - left)
    sy = lambda y: bottom + (y + 1.05) / 1.33 * (top - bottom)
    section = sx(0)
    line(pdf, left, sy(0), right, sy(0), width=.55)
    line(pdf, section, bottom, section, top, width=.65)
    text(pdf, section + 3, top - 8, "section  X=0", size=5.9)
    text(pdf, right, sy(0) - 11, "X", size=6.4, font="MathItalic", align="right")
    text(pdf, left - 5, top - 2, "Y", size=6.4, font="MathItalic", align="right")
    xs = [-1.28 + 2.56 * i / 320 for i in range(321)]
    singular = [(sx(x), sy(alpha * x * x - 1 / (2 * alpha))) for x in xs]
    polyline(pdf, singular, color=GRAY, width=.9, dash=(1.5, 2))
    text(pdf, sx(-.96), sy(-.50), "exact  γ₀", color=GRAY, size=5.8)
    xr = [1.23 - 1.23 * i / 120 for i in range(121)]
    tr = [(sx(x), sy(alpha * x*x - 1/(2*alpha) + .105*(1 - x/1.23))) for x in xr]
    xl = [-1.23 + 1.23 * i / 120 for i in range(121)]
    tl = [(sx(x), sy(alpha * x*x - 1/(2*alpha) - .095*(1 + x/1.23))) for x in xl]
    polyline(pdf, tr, color=BLUE, width=1.3)
    polyline(pdf, tl, color=ORANGE, width=1.3, dash=(4, 2))
    arrow(pdf, *tr[55], *tr[69], color=BLUE, width=.8, head=3.8)
    arrow(pdf, *tl[57], *tl[43], color=ORANGE, width=.8, head=3.8)
    text(pdf, sx(.77), sy(-.16), "attracting-side", color=BLUE, size=5.5, align="center")
    text(pdf, sx(-.77), sy(-.16), "repelling-side", color=ORANGE, size=5.5, align="center")
    ya, yr = tr[-1][1], tl[-1][1]
    marker(pdf, section, ya, kind="circle", color=BLUE, radius=2.1)
    marker(pdf, section, yr, kind="square", color=ORANGE, radius=2)
    double_arrow(pdf, section + 8, ya, section + 8, yr)
    runs(pdf, section + 12, (ya + yr) / 2 - 2,
         [("gap  ", "DVSerif", 6.0, 0), ("d", "MathItalic", 7.0, 0),
          ("P", "MathItalic", 4.7, -1.8)])
    runs(pdf, x0 + w / 2, y0 + 8,
         [("d", "MathItalic", 6.7, 0), ("P", "MathItalic", 4.5, -1.7),
          (" = 0 iff complete histories match", "DVSerif", 5.8, 0)], align="center")


def make_mechanism(output: Path) -> None:
    page = (6.8 * inch, 2.8 * inch)
    pdf = canvas.Canvas(str(output), pagesize=page, pageCompression=1, invariant=1,
                        initialFontName="DVSerif", initialFontSize=7)
    metadata(pdf, "Delay redistribution and canonical history connection mechanism",
             "Exact projection identities and schematic complete-history geometry")
    margin, gap = 14, 10
    width = (page[0] - 2 * margin - 2 * gap) / 3
    height, y0 = page[1] - 18, 9
    mechanism_panel_a(pdf, margin, y0, width, height)
    mechanism_panel_b(pdf, margin + width + gap, y0, width, height)
    mechanism_panel_c(pdf, margin + 2 * (width + gap), y0, width, height)
    pdf.showPage()
    pdf.save()


def load_data() -> dict:
    with DATA_FILE.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if "diagnostic" not in data.get("status", "").lower():
        raise ValueError("Input artifact is not labelled diagnostic")
    predicted = float(data["predicted_coefficient"])
    for row in data.get("rows", []):
        if float(row["delta"]) <= 0 or float(row["relative_error"]) <= 0:
            raise ValueError("Log axes require positive data")
        if not math.isclose(float(row["predicted_coefficient"]), predicted, abs_tol=1e-14):
            raise ValueError("Inconsistent predicted coefficient")
        check = abs(float(row["quotient_central"]) - predicted) / abs(predicted)
        if not math.isclose(check, float(row["relative_error"]), rel_tol=2e-12):
            raise ValueError("Inconsistent relative error")
    if len(data.get("rows", [])) < 2:
        raise ValueError("Insufficient diagnostic rows")
    return data


def axes(pdf: canvas.Canvas, box: tuple[float, float, float, float], *,
         xticks: Sequence[tuple[float, str]], yticks: Sequence[tuple[float, str]],
         xlabel: str | None, ylabel: str, show_x: bool) -> None:
    left, bottom, right, top = box
    line(pdf, left, bottom, right, bottom, width=.65)
    line(pdf, left, bottom, left, top, width=.65)
    for xpos, label in xticks:
        line(pdf, xpos, bottom, xpos, top, color=GRID_GRAY, width=.45)
        line(pdf, xpos, bottom, xpos, bottom - 3, width=.6)
        if show_x:
            text(pdf, xpos, bottom - 12, label, size=6.4, align="center")
    for ypos, label in yticks:
        line(pdf, left, ypos, right, ypos, color=GRID_GRAY, width=.45)
        line(pdf, left - 3, ypos, left, ypos, width=.6)
        text(pdf, left - 6, ypos - 2.2, label, size=6.3, align="right")
    if xlabel:
        text(pdf, (left + right) / 2, bottom - 25, xlabel, size=6.9, align="center")
    pdf.saveState()
    pdf.translate(left - 53, (bottom + top) / 2)
    pdf.rotate(90)
    text(pdf, 0, 0, ylabel, size=6.4, align="center")
    pdf.restoreState()


def make_convergence(data: dict, output: Path) -> None:
    rows = sorted(data["rows"], key=lambda row: float(row["delta"]))
    ds = [float(row["delta"]) for row in rows]
    qs = [float(row["quotient_central"]) for row in rows]
    es = [100 * float(row["relative_error"]) for row in rows]
    predicted = float(data["predicted_coefficient"])
    page = (6.2 * inch, 4.7 * inch)
    pdf = canvas.Canvas(str(output), pagesize=page, pageCompression=1, invariant=1,
                        initialFontName="DVSerif", initialFontSize=7)
    metadata(pdf, "Exact-chart threshold diagnostic",
             "Prescribed-history finite-section sign and scale diagnostic")
    left, right = 78, page[0] - 15
    lower, upper = (left, 54, right, 151), (left, 185, right, page[1] - 20)
    lx0, lx1 = math.log10(.002), math.log10(.15)
    sx = lambda value: left + (math.log10(value) - lx0)/(lx1 - lx0)*(right - left)
    syq = lambda value: upper[1] + (value + .2050)/.0095*(upper[3] - upper[1])
    lye0, lye1 = math.log10(.2), math.log10(5)
    sye = lambda value: lower[1] + (math.log10(value) - lye0)/(lye1 - lye0)*(lower[3] - lower[1])
    xticks = [(sx(v), f"{v:g}") for v in [.002, .005, .01, .02, .05, .1]]
    qticks = [(syq(v), f"{v:.3f}") for v in [-.204, -.202, -.200, -.198, -.196]]
    eticks = [(sye(v), f"{v:g}") for v in [.2, .5, 1, 2, 5]]
    axes(pdf, upper, xticks=xticks, yticks=qticks, xlabel=None,
         ylabel="normalized coefficient quotient", show_x=False)
    axes(pdf, lower, xticks=xticks, yticks=eticks, xlabel="fold parameter  δ",
         ylabel="absolute relative discrepancy (%)", show_x=True)
    qpoints = [(sx(d), syq(q)) for d, q in zip(ds, qs)]
    polyline(pdf, qpoints, color=ORANGE, width=1.2)
    for point in qpoints:
        marker(pdf, *point, kind="circle", color=ORANGE, radius=2.5)
    line(pdf, left, syq(predicted), right, syq(predicted), dash=(4, 2.2), width=.9)
    text(pdf, left + 6, upper[3] - 11, "(a)", size=7.3, font="DVSerif-Bold")
    line(pdf, left + 29, upper[3] - 9, left + 50, upper[3] - 9, color=ORANGE, width=1.2)
    marker(pdf, left + 39.5, upper[3] - 9, kind="circle", color=ORANGE, radius=2.2)
    runs(pdf, left + 55, upper[3] - 12,
         [("recorded  ", "DVSerif", 6.3, 0), ("q", "NotoMath", 6.8, 0),
          ("num", "DVSerif", 4.6, -1.7), ("(δ,S)", "NotoMath", 6.5, 0)],
         color=ORANGE)
    line(pdf, left + 157, upper[3] - 9, left + 179, upper[3] - 9, dash=(4, 2.2), width=.9)
    runs(pdf, left + 184, upper[3] - 12,
         [("analytic  ", "DVSerif", 6.2, 0), ("c⊥", "NotoMath", 6.6, 0),
          ("  (not fitted)", "DVSerif", 6.2, 0)])
    arrow(pdf, sx(.09), upper[1] + 16, sx(.035), upper[1] + 16, color=GRAY, width=.65, head=3.5)
    text(pdf, sx(.091), upper[1] + 13, "decreasing δ", color=GRAY, size=6.2, align="right")
    epoints = [(sx(d), sye(e)) for d, e in zip(ds, es)]
    polyline(pdf, epoints, color=BLUE, width=1.1, dash=(4, 2))
    for point in epoints:
        marker(pdf, *point, kind="square", color=BLUE, radius=2.3)
    text(pdf, left + 6, lower[3] - 12, "(b)", size=7.3, font="DVSerif-Bold")
    text(pdf, page[0]/2, 12,
         "Prescribed-history, finite-section diagnostic only; not a complete-history threshold.",
         color=GRAY, size=7.0, align="center")
    pdf.showPage()
    pdf.save()


def main() -> None:
    register_fonts()
    make_mechanism(HERE / "figure1_mechanism.pdf")
    make_convergence(load_data(), HERE / "figure2_threshold_convergence.pdf")


if __name__ == "__main__":
    main()
