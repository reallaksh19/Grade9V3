"""Quantitative SVG primitives and the scene dispatcher.

The mechanics of drawing -- coordinate mapping, equal scaling, axes, arrow markers,
the SVG envelope and its scene digest -- are subject-neutral and live here. Which
*scenes* exist is not: a vector construction, a function plot with excluded values,
a particle diagram are different claims about different subject matter. A subject
registers its scene renderers on its adapter; this module dispatches to them and
never enumerates them.

Every scene, whatever the subject, must declare the frame it is drawn in and a
caption. Anything further -- axis labels, units, symbols, particle identities -- is
the renderer's own requirement, because not every representation has axes.
"""
from __future__ import annotations

from html import escape

from Shared.contracts import digest, require, text
from .science import numeric_atom

WIDTH, HEIGHT, PAD = 560, 360, 58


def figure(ctx, block):
    spec = block["scene"]
    kind = spec.get("kind")
    scenes = ctx["adapter"].scenes
    require(isinstance(kind, str) and kind in scenes, "FIGURE_FAMILY_UNSUPPORTED", str(kind))
    for key in ("frame", "caption"):
        text(spec.get(key), "FIGURE_CONTEXT_REQUIRED")
    return scenes[kind](ctx, block)


def bound_atom(ctx, block, atom_id, unit):
    """A figure may only draw values it declared as its own source atoms."""
    require(atom_id in block["source_atom_ids"], "FIGURE_SOURCE_BINDING_MISSING")
    return numeric_atom(ctx, atom_id, unit)


def bounds(xs, ys):
    xmin, xmax, ymin, ymax = min(0, *xs), max(0, *xs), min(0, *ys), max(0, *ys)
    if xmin == xmax:
        xmin, xmax = -1, 1
    if ymin == ymax:
        ymin, ymax = -1, 1
    return xmin, xmax, ymin, ymax


def mapping(box, equal, width=WIDTH, height=HEIGHT):
    xmin, xmax, ymin, ymax = box
    sx, sy = (width - 2 * PAD) / (xmax - xmin), (height - 2 * PAD) / (ymax - ymin)
    if equal:
        sx = sy = min(sx, sy)
    left = (width - (xmax - xmin) * sx) / 2
    top = (height - (ymax - ymin) * sy) / 2
    return lambda x, y: (left + (x - xmin) * sx, top + (ymax - y) * sy), (sx, sy)


def line(p, q, **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k, v in attrs.items())
    return f'<line x1="{p[0]:.6f}" y1="{p[1]:.6f}" x2="{q[0]:.6f}" y2="{q[1]:.6f}" {extra}/>'


def label(x, y, value, anchor="middle"):
    return f'<text x="{x:.3f}" y="{y:.3f}" text-anchor="{anchor}" font-size="14">{escape(str(value))}</text>'


def axes(spec, box, point, width=WIDTH, height=HEIGHT):
    xmin, xmax, ymin, ymax = box
    axis_x = 0 if xmin <= 0 <= xmax else xmin
    axis_y = 0 if ymin <= 0 <= ymax else ymin
    rows = [line(point(xmin, axis_y), point(xmax, axis_y), stroke="#64748b"),
            line(point(axis_x, ymin), point(axis_x, ymax), stroke="#64748b")]
    rows += [label(width / 2, height - 10, spec["x_label"]),
             label(10, 20, spec["y_label"], "start"),
             label(point(axis_x, axis_y)[0] - 10, point(axis_x, axis_y)[1] + 20, f'{axis_x:g}')]
    if axis_y != 0:
        rows.append(label(point(axis_x, axis_y)[0] - 8, point(axis_x, axis_y)[1], f'{axis_y:g}', 'end'))
    return rows


def svg(block, rows, evidence, width=WIDTH, height=HEIGHT):
    title = escape(block["scene"]["caption"])
    rows = ['<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#135b89"/></marker></defs>'] + rows
    xml = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
           f'role="img" aria-label="{title}" data-scene-digest="{digest(block["scene"])}">'
           f'<title>{title}</title><rect width="100%" height="100%" fill="white"/><g font-family="sans-serif" fill="#172c42">'
           + "".join(rows) + '</g></svg>')
    return xml, {**evidence, "frame": block["scene"]["frame"], "quantitative": True,
                 "width": width, "height": height, "minimum_label_px": 14}
