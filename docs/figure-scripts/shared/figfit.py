"""Measure a drawn string instead of guessing its width.

Guessing at character widths fails for bold text and for long labels, and the
first pass of every figure in this chapter overflowed a box because of it. Draw
the string, ask the renderer how wide it actually came out, and fail loudly if
it does not fit the space it was given.
"""
FAILURES = []


def width_in(fig, artist):
    """The drawn width of a text artist, in inches."""
    fig.canvas.draw()
    bb = artist.get_window_extent(fig.canvas.get_renderer())
    return bb.width / fig.dpi, bb.height / fig.dpi


def must_fit(fig, artist, max_w_in, what):
    w, _ = width_in(fig, artist)
    if w > max_w_in:
        FAILURES.append(f'{what}: drawn {w:.2f} in exceeds {max_w_in:.2f} in')
    return w


def report():
    if FAILURES:
        raise SystemExit('layout does not fit:\n  ' + '\n  '.join(FAILURES))
    print('layout fits')
