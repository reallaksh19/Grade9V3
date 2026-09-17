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




def _operand(ctx, block, spec, key, unit):
    """One named vector of the construction, read from declared data rather than computed."""
    part = spec.get(key)
    require(isinstance(part, dict), "VECTOR_SUBTRACTION_OPERAND_REQUIRED", key)
    symbol = text(part.get("symbol"), "VECTOR_SUBTRACTION_OPERAND_REQUIRED")
    for axis in ("x_atom", "y_atom"):
        text(part.get(axis), "VECTOR_SUBTRACTION_OPERAND_REQUIRED", )
    return (symbol,
            bound_atom(ctx, block, part["x_atom"], unit),
            bound_atom(ctx, block, part["y_atom"], unit))


def vector_subtraction(ctx, block):
    """P minus Q as a construction: reverse Q, place it at the head of P, read the result.

    Not a component readout. VECTOR draws one vector against axes and would hide the
    reversal, which is the only thing this figure exists to show -- the contract records
    that distinction under this kind's `limits`.

    The resultant is read from declared data and then checked against the construction,
    rather than computed and drawn. A figure that computed it could never disagree with
    itself, and so could never catch a library whose stated answer and whose stated
    operands are not the same claim.
    """
    spec = block["scene"]
    _axis_labels(spec)
    unit = text(spec.get("unit"), "VECTOR_SUBTRACTION_UNIT_REQUIRED")
    (p_symbol, px, py) = _operand(ctx, block, spec, "minuend", unit)
    (q_symbol, qx, qy) = _operand(ctx, block, spec, "subtrahend", unit)
    (r_symbol, rx, ry) = _operand(ctx, block, spec, "resultant", unit)

    # A zero vector has no direction, so there is no arrow to reverse and the
    # construction has nothing to demonstrate. Drawing it anyway would show a resultant
    # equal to P and teach that subtraction leaves a vector alone.
    require((qx, qy) != (0, 0), "VECTOR_SUBTRACTION_NOTHING_TO_REVERSE",
            f"{q_symbol} is the zero vector")
    require((rx, ry) == (px - qx, py - qy), "VECTOR_SUBTRACTION_RESULTANT_DISAGREES",
            f"{r_symbol} is declared ({rx:g}, {ry:g}); {p_symbol} - {q_symbol} "
            f"is ({px - qx:g}, {py - qy:g})")

    # Every point the construction touches, so one scale covers the reversed vector and
    # the resultant as well as the two operands. Scaling to the operands alone would
    # push the tail-to-head step off the frame in exactly the cases that need it most.
    xs, ys = [px, qx, rx, px + (-qx)], [py, qy, ry, py + (-qy)]
    box = bounds(xs, ys)
    point, scales = mapping(box, equal=True)
    origin = point(0, 0)
    head_p, head_r = point(px, py), point(rx, ry)

    rows = axes(spec, box, point)
    rows += [
        line(origin, point(qx, qy), stroke="#94a3b8", stroke_width="2",
             marker_end="url(#arrow)", data_vector="subtrahend"),
        line(origin, head_p, stroke="#135b89", stroke_width="2.5",
             marker_end="url(#arrow)", data_vector="minuend"),
        # Tail-to-head, and translated without rotation: the reversed vector starts where
        # the first one ends and keeps its own direction, which is the whole construction.
        line(head_p, head_r, stroke="#b45309", stroke_width="2.5",
             marker_end="url(#arrow)", data_vector="reversed_subtrahend"),
        line(origin, head_r, stroke="#166534", stroke_width="3",
             marker_end="url(#arrow)", data_vector="resultant"),
    ]
    rows += [
        label(*_midpoint(origin, point(qx, qy)), q_symbol),
        label(*_midpoint(origin, head_p), p_symbol),
        label(*_midpoint(head_p, head_r), f"-{q_symbol}"),
        label(*_midpoint(origin, head_r), r_symbol),
    ]
    rows.append(f'<text x="{WIDTH / 2}" y="30" text-anchor="middle" font-size="16">'
                f'<tspan font-weight="bold">{escape(r_symbol)}</tspan>'
                f'<tspan> = {escape(p_symbol)} + (-{escape(q_symbol)}) = '
                f'({rx:g}, {ry:g}) {escape(unit)}</tspan></text>')
    return svg(block, rows, dict(kind="VECTOR_SUBTRACTION", unit=unit,
                                 minuend=[px, py], subtrahend=[qx, qy], resultant=[rx, ry],
                                 reversed_from=list(head_p), scale=list(scales)))


def _midpoint(a, b):
    """Where a vector's label goes: beside its middle, lifted clear of the line itself."""
    return (a[0] + b[0]) / 2 + 10, (a[1] + b[1]) / 2 - 6


SCENES = {"VECTOR": vector, "VECTOR_SUBTRACTION": vector_subtraction,
          "GRAPH": graph}
