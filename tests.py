#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import unittest, tempfile, math, sys, os

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

        data = p.render(border=False).splitlines()

        tops = data[0].split(u"⣿⣿")
        self.assertEqual(len(tops[1]), len(tops[2]))

        bots = data[-1].split(u"⣿⣿")
        self.assertEqual(len(tops[1]), len(tops[2]))

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

    def test_file(self):
        plotters = []

        plotters.append(Plotter((-x + 25 for x in range(50)), height=4))
        plotters.append(Plotter((-x - 1000 for x in range(50)), height=4))
        plotters.append(Plotter((x + 1000 for x in range(50)), height=4))
        plotters.append(Plotter((15 for x in range(50)), height=4))
        plotters.append(Plotter((math.sin(x / 10) * 10 for x in range(100)), height=4))

        null1 = open(os.devnull, 'wb')
        null2 = open(os.devnull, 'w')

        for plotter in plotters:
            plotter.write(null1, border=True)
            plotter.write(null1, fill=False)
            plotter.write(null1, color=True, border=True)
            plotter.write(null1, color=True, html=True)

            plotter.write(null2, border=True)
            plotter.write(null2, fill=False)
            plotter.write(null2, color=True, border=True)
            plotter.write(null2, color=True, html=True)

            _, filename = tempfile.mkstemp()
            plotter.save(filename, border=True)
            plotter.save(filename, fill=False)
            plotter.save(filename, color=True, border=True)
            plotter.save(filename, color=True, html=True)
            os.remove(filename)

        null1.close()
        null2.close()

if __name__ == '__main__':
    unittest.main()
