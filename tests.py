import unittest, math, sys, os

from textyplot import *

class TestStringMethods(unittest.TestCase):
    def test_init(self):
        Plotter((-x + 25 for x in range(50)), height=32)
        Plotter((-x - 1000 for x in range(50)))
        Plotter((15 for x in range(50)))
        Plotter((math.sin(x / 10) * 10 for x in range(100)), height=16)

    def test_show(self):
        plotters = []

        plotters.append(Plotter((-x + 25 for x in range(50)), height=4))
        plotters.append(Plotter((-x - 1000 for x in range(50)), height=4))
        plotters.append(Plotter((x + 1000 for x in range(50)), height=4))
        plotters.append(Plotter((15 for x in range(50)), height=4))
        plotters.append(Plotter((0 for x in range(50)), height=4))
        plotters.append(Plotter((math.sin(x / 10) * 10 for x in range(100)), height=4))

        _stdout = sys.stdout
        sys.stdout = null = open(os.devnull, 'w')

        for plotter in plotters:
            plotter.show(border=True)
            plotter.show(fill=False)
            plotter.show(color=True, border=True)
            plotter.show(color=True, border=True, html=True, fill=True)

        null.close()
        sys.stdout = _stdout

    def test_sin(self):
        p = Plotter((math.sin(x / 5) * 5 for x in range(100)), height=4)

        data = p.render().splitlines()

        tops = data[0].split('\xe2\xa3\xbf\xe2\xa3\xbf')
        self.assertEqual(len(tops[1]), len(tops[2]))

        bots = data[-1].split("\xe2\xa3\xbf\xe2\xa3\xbf")
        self.assertEqual(len(tops[1]), len(tops[2]))

        mids = data[1].split("\xe2\xa3\xbf\xcc\xb2\xe2\xa3\xbf\xcc\xb2\xe2\xa3\xbf\xcc\xb2\xe2\xa3\xbf\xcc\xb2\xe2\xa3\xbf\xcc\xb2'")
        self.assertEqual(len(mids[1]), len(mids[2]))

        mids = data[2].split("\xe2\xa3\xbf\xe2\xa3\xbf\xe2\xa3\xbf\xe2\xa3\xbf\xe2\xa3\xbf")
        self.assertEqual(len(mids[1]), len(mids[2]))

    def test_border(self):
        p = Plotter((math.sin(x / 5) * 5 for x in range(100)), height=4)

        data = p.render(border=True).splitlines()

        color_size = 4

        self.assertEqual(len(data[0]) - color_size, data[0].count("\xe2\xa0\x89'"))
        self.assertEqual(len(data[-1]) - color_size * 2, data[-1].count("\xe2\xa3\x80"))

    def test_up(self):
        p = Plotter((x for x in range(8)), height=4)

        data = p.render().splitlines()

        self.assertEqual(data[0][-3], "\xe2\xa0\x80")

        self.assertEqual(data[0].count("\xe2\xa0\x80"), 3)
        self.assertEqual(data[1].count("\xe2\xa0\x80"), 2)
        self.assertEqual(data[2].count("\xe2\xa0\x80"), 1)
        self.assertEqual(data[3].count("\xe2\xa0\x80"), 0)

        self.assertEqual(data[0].count("\xe2\xa3\xbf"), 0)
        self.assertEqual(data[1].count("\xe2\xa3\xbf"), 1)
        self.assertEqual(data[2].count("\xe2\xa3\xbf"), 2)
        self.assertEqual(data[3].count("\xe2\xa3\xbf"), 3)

    def test_down(self):
        p = Plotter((-x for x in range(8)), height=4)

        data = p.render().splitlines()

        self.assertEqual(data[0][-1], "\xe2\xa3\xbf")

        self.assertEqual(data[0].count("\xe2\xa0\x80"), 0)
        self.assertEqual(data[1].count("\xe2\xa0\x80"), 1)
        self.assertEqual(data[2].count("\xe2\xa0\x80"), 2)
        self.assertEqual(data[3].count("\xe2\xa0\x80"), 3)

        self.assertEqual(data[0].count("\xe2\xa3\xbf"), 3)
        self.assertEqual(data[1].count("\xe2\xa3\xbf"), 2)
        self.assertEqual(data[2].count("\xe2\xa3\xbf"), 1)
        self.assertEqual(data[3].count("\xe2\xa3\xbf"), 0)

    def test_write(self):
        plotters = []

        plotters.append(Plotter((-x + 25 for x in range(50)), height=4))
        plotters.append(Plotter((-x - 1000 for x in range(50)), height=4))
        plotters.append(Plotter((x + 1000 for x in range(50)), height=4))
        plotters.append(Plotter((15 for x in range(50)), height=4))
        plotters.append(Plotter((math.sin(x / 10) * 10 for x in range(100)), height=4))

        null = open(os.devnull, 'wb')

        for plotter in plotters:
            plotter.write(null, border=True)
            plotter.write(null, fill=False)
            plotter.write(null, color=True, border=True)
            plotter.write(null, color=True, html=True)

        null.close()

if __name__ == '__main__':
    unittest.main()
