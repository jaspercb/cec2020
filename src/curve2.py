def MakeCurve(w, h):
    lim = int(w/2)
    xss = list(range(0, lim))
    xs = []

    if h % 2 == 0:
        xss = xss[::-1]

    for x in range(h):
        xs += xss
        xss = xss[::-1]

    xss = list(range(lim, w))
    for x in range(h):
        xs += xss
        xss = xss[::-1]

    ys = []
    for y in range(0, h):
        ys += [y] * lim
    for y in reversed(range(0, h)):
        ys += [y] * (w-lim)

    assert(len(ys) == len(xs))
    return list(zip(ys, xs))


def testcurve(curve):
    for i, e in enumerate(curve[1:]):
        print(e)
        prev = curve[i]
        dx = e[0] - prev[0]
        dy = e[1] - prev[1]
        # print(dx, dy)
        assert(dx in [-1, 0, 1])
        assert(dy in [-1, 0, 1])
        dx_is = bool(dx)
        dy_is = bool(dy)
        assert(dx^dy)


if __name__ == '__main__':
    testcurve(MakeCurve(5, 5))
    testcurve(MakeCurve(4, 5))
    testcurve(MakeCurve(5, 4))
    testcurve(MakeCurve(4, 4))
