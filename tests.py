#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import unittest, tempfile, math, sys, os, io

from textyplot import *

kwargs_pack = [
    {},
    {"zero": False},
    {"fill": False},
    {"html": True},
    {"stretch": False},
    {"border": False},
    {"data": False},
    {"zero": False, "fill": False, "html": True},
    {"data": False, "border": False, "color": True},
    {"color": True},
    {"color": True, "html": True},
]

points_pack = [
    [i for i in range(50)],
    [-i for i in range(50)],
    [50 - i for i in range(50)],
    [i - 50 for i in range(50)],
    [math.sin(i / 5) * 5 for i in range(50)],
    [math.log(i) for i in range(1, 51)],
    [math.cos(i / 5) * 5 for i in range(50)],
    [2 ** i for i in range(50)],
    [i ** 2 for i in range(50)],
    [0 for i in range(50)],
    [-100 for i in range(50)],
    [100 for i in range(50)],
    [100 + i for i in range(50)],
    [-100 - i for i in range(50)],
    [5 for i in range(50)],
    [-5 for i in range(50)],
]

class TestTextyplot(unittest.TestCase):
    @staticmethod
    def test_init():
        Plotter((-x + 25 for x in range(50)), height=32)
        Plotter((-x - 1000 for x in range(50)))
        Plotter((15 for x in range(50)))
        Plotter((0 for x in range(50)), width=64, height=2)
        Plotter((math.sin(x / 10) * 10 for x in range(100)), height=16)

    @staticmethod
    def test_height():
        Plotter((-x + 25 for x in range(50)), height=30).render()
        Plotter((-x + 25 for x in range(50)), height=7).render()
        Plotter((-x + 25 for x in range(50)), height=1).render()
        Plotter((-x + 25 for x in range(50)), height=2).render()

    @staticmethod
    def test_stretch():
        Plotter((x for x in range(50)), width=100).render()
        Plotter((25 - x for x in range(50)), width=100).render()
        Plotter((math.log(x * 10) for x in range(1, 51)), width=100).render()

    @staticmethod
    def test_points():
        for i in range(100):
            Plotter([10 ** i]).render()

    @staticmethod
    def test_command_line():
        points = "\n".join(str(i) for i in points_pack[0])

        _stdin, _stdout = sys.stdin, sys.stdout
        sys.stdout = null = open(os.devnull, "w")

        sys.stdin = io.StringIO(points)
        run([])
        sys.stdin.close()

        sys.stdin = io.StringIO(points)
        run(["-f", "20"])
        sys.stdin.close()

        sys.stdin = io.StringIO(points)
        run(["-C"])
        sys.stdin.close()

        null.close()
        sys.stdin, sys.stdout = _stdin, _stdout


    def test_write_fail(self):
        null = open(os.devnull, 'r')

        with self.assertRaises(ValueError):
            Plotter(x for x in range(50)).write(null)

        null.close()

    @staticmethod
    def test_show():
        plotters = [Plotter(pack, height=4) for pack in points_pack]

        _stdout = sys.stdout
        sys.stdout = null = open(os.devnull, 'w')

        for plotter in plotters:
            for kwargs in kwargs_pack:
                plotter.show(**kwargs)

        null.close()
        sys.stdout = _stdout

    @staticmethod
    def test_file():
        plotters = [Plotter(pack, height=4) for pack in points_pack]

        nulls = [open(os.devnull, 'wb'), open(os.devnull, 'w')]

        for plotter in plotters:
            for null in nulls:
                for kwargs in kwargs_pack:
                    plotter.write(null, **kwargs)

            _, filename = tempfile.mkstemp()

            for kwargs in kwargs_pack:
                plotter.save(filename, **kwargs)

            os.remove(filename)

        nulls[0].close()
        nulls[1].close()

    def test_sin(self):
        p = Plotter((math.sin(x / 5) * 5 for x in range(100)), height=4)

        data = p.render(border=False).splitlines()

        tops = data[0].split(u"⣿⣿")
        self.assertEqual(len(tops[1]), len(tops[2]))

        bots = data[-1].split(u"⣿⣿")
        try:
            self.assertEqual(len(bots[1]), len(bots[2]))
        except AssertionError:
            self.assertEqual(len(bots[1]) - 1, len(bots[2]))

        mids = data[1].split(u"⣿̲⣿̲⣿̲⣿̲")
        self.assertEqual(len(mids[1]), len(mids[2]))

        mids = data[2].split(u"⣿⣿⣿⣿")
        self.assertEqual(len(mids[1]), len(mids[2]))

    def test_border(self):
        p = Plotter((math.sin(x / 5) * 5 for x in range(80)), height=4)

        data = p.render(border=True).splitlines()

        color_size = 4

        self.assertEqual(len(data[0]) - color_size, data[0].count(u"⠉"))
        self.assertEqual(len(data[-1]) - color_size * 2, data[-1].count(u"⣀"))

    def test_up(self):
        p = Plotter((x for x in range(8)), height=4)

        data = p.render(border=False).splitlines()

        self.assertEqual(data[0][-3], u"⠀")

        self.assertEqual(data[0].count(u"⠀"), 3)
        self.assertEqual(data[1].count(u"⠀"), 2)
        self.assertEqual(data[2].count(u"⠀"), 1)
        self.assertEqual(data[3].count(u"⠀"), 0)

        self.assertEqual(data[0].count(u"⣿"), 0)
        self.assertEqual(data[1].count(u"⣿"), 1)
        self.assertEqual(data[2].count(u"⣿"), 2)
        self.assertEqual(data[3].count(u"⣿"), 3)

    def test_down(self):
        p = Plotter((-x for x in range(8)), height=4)

        data = p.render(border=False).splitlines()

        self.assertEqual(data[0][-1], u"⣿")

        self.assertEqual(data[0].count(u"⠀"), 0)
        self.assertEqual(data[1].count(u"⠀"), 1)
        self.assertEqual(data[2].count(u"⠀"), 2)
        self.assertEqual(data[3].count(u"⠀"), 3)

        self.assertEqual(data[0].count(u"⣿"), 3)
        self.assertEqual(data[1].count(u"⣿"), 2)
        self.assertEqual(data[2].count(u"⣿"), 1)
        self.assertEqual(data[3].count(u"⣿"), 0)


if __name__ == '__main__':
    unittest.main()
