"""Representation scenes this subject can draw.

A number line is the representation that carries this subject's weight at this level:
it shows where a solution sits, whether an endpoint is included, and that an exact
value and its decimal approximation are not the same point. Physics vector scenes are
not reused -- an arrow from an origin makes a claim about direction that a solution
set does not make.
"""
from __future__ import annotations

import math
from fractions import Fraction

from Shared.contracts import require, text
from Shared.publication_host.drawing import PAD, WIDTH, bound_atom, label, line, svg

HEIGHT = 190
MARK_RADIUS = 6
TIER = 34  # vertical step for a mark lifted clear of one it would otherwise overpaint


def number_line(ctx, block):
    """Marked points on a single axis, drawn at exact rational positions."""
    spec = block["scene"]
    text(spec.get("x_label"), "FIGURE_CONTEXT_REQUIRED")
    unit = text(spec.get("unit"), "NUMBER_LINE_UNIT_REQUIRED")
    marks = spec.get("marks")
    require(isinstance(marks, list) and marks, "NUMBER_LINE_MARKS_REQUIRED")

    points = []
    for mark in marks:
        value = bound_atom(ctx, block, mark["atom"], unit)
        text(mark.get("label"), "NUMBER_LINE_MARK_LABEL_REQUIRED")
        require(mark.get("closed") in (True, False), "NUMBER_LINE_ENDPOINT_UNDECLARED",
                f'{mark["atom"]}: an endpoint must say whether it is included')
        points.append((value, mark["label"], mark["closed"]))

    # The axis runs to the integers enclosing the marks, never to a mark itself. A
    # value drawn at the end of the line reads as the end of the number system; a
    # value drawn between two ticks reads as a number sitting between two integers,
    # which is the claim a non-integer solution actually makes.
    low = min(0, min(p[0] for p in points))
    high = max(0, max(p[0] for p in points))
    low, high = math.floor(low), math.ceil(high)
    if low == high:
        low, high = low - 1, high + 1
    span = high - low
    baseline = HEIGHT / 2

    def place(value):
        # A drawn position is a pixel, so it is approximate by construction. The
        # approximation is confined to this line; the value itself stays exact,
        # which is what lets an exact solution and its truncation carry distinct
        # labels even when they land on the same pixel.
        return float(PAD + (value - low) / span * (WIDTH - 2 * PAD))

    rows = [line((PAD, baseline), (WIDTH - PAD, baseline), stroke="#64748b",
                 marker_end="url(#arrow)")]
    for step in range(low, high + 1):
        x = place(step)
        rows.append(line((x, baseline - 5), (x, baseline + 5), stroke="#94a3b8"))
        rows.append(label(x, baseline + 22, str(step)))

    # Two marks can be numerically distinct and land on the same pixel -- an exact
    # value and a long truncation of it do exactly that. Drawing them both on the axis
    # would let one overpaint the other, hiding whichever endpoint was drawn first and
    # with it whether that endpoint is included. A colliding mark is therefore lifted
    # off the axis on a leader line: the leader still reports the position, and both
    # circles stay visible. No mark is ever moved horizontally, because its horizontal
    # position is the claim it makes.
    placed: list[float] = []
    for value, mark_label, closed in sorted(points, key=lambda p: p[0]):
        x = place(value)
        tier = sum(1 for seen in placed if abs(seen - x) < 2 * MARK_RADIUS)
        placed.append(x)
        y = baseline - tier * TIER
        if tier:
            rows.append(line((x, baseline), (x, y), stroke="#94a3b8", stroke_dasharray="3 3"))
        fill = "#135b89" if closed else "white"
        rows.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{MARK_RADIUS}" fill="{fill}" '
                    f'stroke="#135b89" stroke-width="2.5"/>')
        rows.append(label(x, y - 14, mark_label))
    rows.append(label(WIDTH / 2, HEIGHT - 8, spec["x_label"]))

    # The digest records each mark as the subject recorded it: a Fraction prints as
    # an exact ratio, a float as the approximation it is. Two marks a pixel apart but
    # numerically different therefore produce different digests.
    marked = [str(value) if isinstance(value, Fraction) else repr(float(value))
              for value, _, _ in points]
    return svg(block, rows, dict(kind="NUMBER_LINE", marks=marked, unit=unit,
                                 span=[float(low), float(high)]), WIDTH, HEIGHT)


SCENES = {"NUMBER_LINE": number_line}
