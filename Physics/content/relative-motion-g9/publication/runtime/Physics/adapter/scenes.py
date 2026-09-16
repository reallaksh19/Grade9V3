"""Representation scenes this subject can draw quantitatively.

Registered on the adapter; the shared engine dispatches by declared scene kind and
does not know these exist. Both scenes are axis-based and therefore require axis
labels in addition to the frame and caption the engine requires of every scene.
"""
from __future__ import annotations

from html import escape

from Shared.contracts import require, text
from Shared.publication_host.drawing import (
    HEIGHT, PAD, WIDTH, axes, bound_atom, bounds, label, line, mapping, svg,
)


def _axis_labels(spec):
    for key in ("x_label", "y_label"):
        text(spec.get(key), "FIGURE_CONTEXT_REQUIRED")


def vector(ctx, block):
    """One vector from the origin, at equal coordinate scale, with its components shown."""
    spec = block["scene"]
    _axis_labels(spec)
    text(spec.get("symbol"), "VECTOR_SYMBOL_REQUIRED")
    unit = text(spec.get("unit"), "VECTOR_UNIT_REQUIRED")
    x = bound_atom(ctx, block, spec["x_atom"], unit)
    y = bound_atom(ctx, block, spec["y_atom"], unit)
    box = bounds([x], [y])
    xmin, xmax, ymin, ymax = box
    scale = min((WIDTH - 2 * PAD) / (xmax - xmin), (HEIGHT - 2 * PAD) / (ymax - ymin))
    width = max(280, (xmax - xmin) * scale + 2 * PAD)
    height = max(180, (ymax - ymin) * scale + 2 * PAD)
    point, scales = mapping(box, equal=True, width=width, height=height)
    origin, end = point(0, 0), point(x, y)
    rows = axes(spec, box, point, width=width, height=height)
    rows += [line(origin, point(x, 0), stroke="#7b96ab", stroke_dasharray="5 3"),
             line(point(x, 0), end, stroke="#7b96ab", stroke_dasharray="5 3")]
    if x == y == 0:
        # A zero vector has no direction; drawing an arrow would invent one.
        rows.append(f'<circle cx="{origin[0]}" cy="{origin[1]}" r="4" fill="#135b89"/>')
    else:
        rows.append(line(origin, end, stroke="#135b89", stroke_width="2.5",
                         marker_end="url(#arrow)", data_vector="resultant"))
    rows.append(f'<text x="{width / 2}" y="38" text-anchor="middle" font-size="16">'
                f'<tspan font-weight="bold">{escape(spec["symbol"])}</tspan>'
                f'<tspan> = ({x:g}, {y:g}) {escape(unit)}</tspan></text>')
    return svg(block, rows, dict(kind="VECTOR", components=[x, y], unit=unit,
                                 origin=list(origin), endpoint=list(end), scale=list(scales)), width, height)


def graph(ctx, block):
    """Piecewise-linear plot of source-bound points; no curve is implied between them."""
    spec = block["scene"]
    _axis_labels(spec)
    pairs = spec["points"]
    require(len(pairs) >= 2, "GRAPH_POINTS_REQUIRED")
    values = [(bound_atom(ctx, block, p[0], spec["x_unit"]),
               bound_atom(ctx, block, p[1], spec["y_unit"])) for p in pairs]
    require(all(b[0] > a[0] for a, b in zip(values, values[1:])), "GRAPH_DOMAIN_NOT_INCREASING")
    box = bounds([p[0] for p in values], [p[1] for p in values])
    if "y_min_atom" in spec:
        ymin = bound_atom(ctx, block, spec["y_min_atom"], spec["y_unit"])
        require(ymin <= min(p[1] for p in values) and ymin < box[3], "GRAPH_RANGE_CLIPS_DATA")
        box = (box[0], box[1], ymin, box[3])
    point, scales = mapping(box, equal=False)
    rows = axes(spec, box, point)
    pixels = [point(*v) for v in values]
    for a, b in zip(pixels, pixels[1:]):
        rows.append(line(a, b, stroke="#135b89", stroke_width="2.5", data_graph="segment"))
    for v, p in zip(values, pixels):
        rows.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="3" fill="#135b89"/>')
        rows.append(label(p[0], p[1] - 10, f'({v[0]:g}, {v[1]:g})'))
    return svg(block, rows, dict(kind="GRAPH", points=values, pixels=pixels,
                                 scale=list(scales), y_axis_min=box[2]))


SCENES = {"VECTOR": vector, "GRAPH": graph}
