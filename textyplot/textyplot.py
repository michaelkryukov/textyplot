#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import locale, math, sys, re

if sys.platform == 'darwin':
    locale.setlocale(locale.LC_CTYPE, str('UTF-8'))
else:
    locale.setlocale(locale.LC_ALL, str(''))


sign = lambda x: (1, -1)[x < 0]

base = 10240
line = 818
mask = {
    (0, 3): 1, (1, 3): 8,
    (0, 2): 2, (1, 2): 16,
    (0, 1): 4, (1, 1): 32,
    (0, 0): 64, (1, 0): 128,
}

silent = "\033[0m"
colors = [
    "\033[36m",
    "\033[32m",
    "\033[33m",
    "\033[31m"
]
colors_html = [
    "<span style='color: #0098ff'>",
    "<span style='color: #00c308'>",
    "<span style='color: #ffa200'>",
    "<span style='color: #ff0000'>"
    "<span style='color: black'>"
]
colors_html_end = "</span>"


def normalize_size(value):
    size = math.ceil(value)

    if size % 4:
        return size + (4 - size % 4)

    return size


class Map(object):
    def __init__(self, width, height, fill=True):
        self.width = width + width % 2
        self.height = height + height % 2

        self.offset_x = 0
        self.offset_y = 0

        self.fill = fill

        self.refresh_map()

    def refresh_map(self):
        self.map = [[0] * self.width for _ in range(self.height)]

    def xy(self, x, y):
        return int(x) + self.offset_x, int(y) + self.offset_y

    def check(self, x, y):
        return y >= 0 and y < self.height and x >= 0 and x < self.width

    def set(self, x, y):
        x, y = self.xy(x, y)

        if self.check(x, y):
            self.map[y][x] = 1

        return x, y

    def get(self, x, y):
        x, y = self.xy(x, y)

        if self.fill and x in self.columns:
            for fy, ty in self.columns[x]:
                if fy <= y <= ty:
                    return 1

        if self.check(x, y):
            return self.map[y][x]

        return 0


class Screen(Map):
    def __init__(self, width, height, fill=True):
        super(Screen, self).__init__(width, height, fill)
        self.columns = {}

    def get_block(self, x, y):
        return chr(
            base + sum(v * self.get(x + k[0], y + k[1]) for k, v in mask.items())
        )

    def array(self, draw_line=None):
        text = []

        y = self.height - 4
        while y >= 0:
            text.append("")

            for x in range(0, self.width, 2):
                text[-1] += self.get_block(x, y)

                if draw_line is not None and y == draw_line:
                    text[-1] += chr(line)

            y -= 4

        return text

    def text(self, array=None, draw_line=None):
        return "\n".join(array or self.array(draw_line=draw_line))


class Plotter:
    def __init__(self, points, width=None, height=None):
        self.points = list(points)

        self.width = (width * 2) if width is not None else len(self.points)
        self.height = (height * 4) if height is not None else 24

    def textify_value(self, value):
        sign = "+" if value >= 0 else ""
        avalue = abs(value)

        if avalue >= 1000000000:
            return sign + str(round(value / 1000000)) + "MM"

        if avalue >= 1000000:
            return sign + str(round(value / 1000000)) + "M"

        if avalue >= 100000:
            return sign + str(round(value / 100000)) + "KK"

        if avalue >= 1000:
            return sign + str(round(value / 1000)) + "K"

        return sign + str(round(value))

    def colorize(self, array, meta=(0, 0, 0)):
        max_color = len(colors)
        arrheight = len(array)

        if meta[0] <= 0:
            def get_color(i):
                return colors[max_color - 1 - min(max_color - 1, int(max_color * i / arrheight))]

        else:
            def get_color(i):
                return colors[min(max_color - 1, int(max_color * i / arrheight))]

        newarrray = []

        for i in range(arrheight):
            newarrray.append(get_color(i) + array[i])

        return newarrray

    def htmlize(self, data):
        pattern = "(" + "|".join("(" + re.escape(color) + ")" for color in colors) + "|" + re.escape(silent) + ")"
        mapping = {e: i for i, e in enumerate(colors)}
        mapping[silent] = -1

        meta = [0,]
        def repl(m):
            if meta[0] == 0:
                return colors_html[mapping[m.group()]]

            return colors_html_end + colors_html[mapping[m.group()]]

        html = (
            "<div style='text-align: center; white-space: pre; font-family: Courier, monospace;'>" +
            re.sub(pattern, repl, data).replace("\n", "<br>") +
            "</div>"
        )

        return html

    def analyze_array(self, array):
        return 0, len(array), min(array), max(array)

    def render(self, zoom=True, data=True, border=True, color=False, fill=True, zero=True, html=False, stretch=True):
        if stretch and len(self.points) < self.width:
            points = []

            block = self.width // len(self.points)
            for i, p in enumerate(self.points):
                k = (0 if i + 1 >= len(self.points) else self.points[i + 1] - self.points[i]) / block
                points += [p + i * k for i in range(block)]

        else:
            points = self.points[::]

        lbound, rbound, bbound, ubound = self.analyze_array(points)

        offset_y = self.height // 2

        top, bot, ttop, tbot = ubound, bbound, ubound, bbound

        if zoom:
            zoomed = False

            if ubound < -50 and bbound < -50:
                points = [p - ubound - 0.5 for p in points]
                bot -= ubound - 0.5
                zoomed = True

                lbound, rbound, bbound, ubound = self.analyze_array(points)

            elif ubound > 50 and bbound > 50:
                points = [p - bbound for p in points]
                top -= bbound
                zoomed = True

                lbound, rbound, bbound, ubound = self.analyze_array(points)

            if bbound >= 0:
                offset_y = 0
                bot = 0
            elif ubound <= 0:
                offset_y = self.height
                top = 0

            if not zoomed:
                ttop = top
                tbot = bot

        if not zoomed:
            if top == bot:
                if top > 0:
                    bot = 0
                else:
                    top = 0

            if top != 0 and bot != 0:
                if top > -bot:
                    bot = -top
                else:
                    top = -bot

        screen = Screen(self.width, self.height, fill=fill)

        scale_y = (offset_y or self.height - 1) / (max(abs(ubound), abs(bbound)) or 1)
        scale_x = self.width / (rbound - lbound)

        for x, p in enumerate(points):
            x, y = screen.set(scale_x * x, scale_y * p + offset_y)

            screen.columns[x] = screen.columns.get(x, []) + [sorted([y, offset_y])]

        diagram = screen.array(offset_y - offset_y % 4 if zero and offset_y == self.height / 2 else None)

        if color:
            diagram = self.colorize(diagram, meta=(ubound, bbound, offset_y))

        offset_x = 0
        if data:
            plots = [["", self.textify_value(top)]]
            for i in range(1, len(diagram) - 1):
                plots.append(["", self.textify_value(bot + (top - bot) * (1 - (i + 0.5) / len(diagram)))])
            plots.append(["", self.textify_value(bot)])

            if ttop != tbot:
                if ttop != top and top == 0:
                    plots[0][0] = self.textify_value(ttop) + "]"

                if tbot != bot and bot == 0:
                    plots[-1][0] = self.textify_value(tbot) + "]"

            offset_x_0 = max(len(pack[0]) for pack in plots)
            offset_x_0 = 0 if not offset_x_0 else offset_x_0 + 1

            offset_x_1 = max(len(pack[1]) for pack in plots) + 2

            for i in range(len(diagram)):
                diagram[i] = silent + ("{:<" + str(offset_x_0) + "s}{:<" + str(offset_x_1) + "s}").format(*plots[i]) + diagram[i]

        if border:
            diagram.insert(0, silent + chr(base + 1 + 8) * len(diagram[0]))
            diagram.append(silent + chr(base + 64 + 128) * len(diagram[-1]))

        if html:
            return self.htmlize(screen.text(diagram))

        return screen.text(diagram) + silent

    def write(self, file_out, **kwargs):
        if file_out.mode not in ("wb", "w"):
            raise ValueError("File descriptor is not writable!")

        diagram = self.render(**kwargs)

        if file_out.mode == "wb":
            return file_out.write(bytes(diagram, "utf-8"))

        return file_out.write(diagram)

    def save(self, file_out_name, **kwargs):
        with open(file_out_name, "w") as o:
            return self.write(o, **kwargs)

    def show(self, **kwargs):
        print(self.render(**kwargs))
        print()

def flow(parsed):
    import time

    amount, text, p = 0, "", Plotter([], width=parsed.width, height=parsed.height)

    while True:
        value = sys.stdin.readline().strip()

        try:
            p.points.append(float(value))
            amount += 1
        except ValueError:
            break

        if amount > parsed.flow:
            p.points = p.points[- parsed.flow  + amount % 2:]

        if text:
            command = ""
            for i in range(parsed.height + 2):
                command += "\033[F\033[K"
            print(command, end="")

        text = p.render(
            zoom=parsed.zoom, border=parsed.border, data=parsed.data, color=parsed.color,
            fill=parsed.fill, zero=parsed.zero, html=parsed.html, stretch=parsed.stretch
        )

        print(text)

        time.sleep(0.02)

    return

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Text mode diagrams with possible colors usin UTF-8 colors.')
    parser.add_argument('-Z', '--no-zoom', dest='zoom', action='store_const', const=False, default=True, help='zoom diagram (default: yes)')
    parser.add_argument('-B', '--no-border', dest='border', action='store_const', const=False, default=True, help='draw border (default: yes)')
    parser.add_argument('-D', '--no-data', dest='data', action='store_const', const=False, default=True, help='draw values (default: yes)')
    parser.add_argument('-C', '--no-color', dest='color', action='store_const', const=False, default=True, help='use colors (default: yes)')
    parser.add_argument('-F', '--no-fill', dest='fill', action='store_const', const=False, default=True, help='fill diagram (default: yes)')
    parser.add_argument('-G', '--no-groud', dest='zero', action='store_const', const=False, default=True, help='draw zero line (default: yes)')
    parser.add_argument('-H', '--html', dest='html', action='store_const', const=True, default=False, help='render to html (default: no)')
    parser.add_argument('-S', '--stretch', dest='stretch', action='store_const', const=False, default=True, help='stretch points to width')
    parser.add_argument('-R', '--reverse', dest='reverse', action='store_const', const=True, default=False, help='reverse points')
    parser.add_argument('-f', '--flow', default=0, type=int, metavar='points', help='enable drawing diagram at runtime (only specified amount of poitns are drawn)')
    parser.add_argument('-X', '--width', default=80, type=int, metavar='characters', help='drawing max width (default: 80)')
    parser.add_argument('-Y', '--height', default=8, type=int, metavar='characters', help='drawing height (default: 8)')
    parsed = parser.parse_args()

    if parsed.flow:
        try:
            return flow(parsed)
        except KeyboardInterrupt:
            return

    points = []

    while True:
        value = sys.stdin.readline().strip()

        try:
            points.append(float(value))
        except ValueError:
            break

    Plotter(points[::-1] if parsed.reverse else points, width=parsed.width, height=parsed.height).show(
        zoom=parsed.zoom, border=parsed.border, data=parsed.data, color=parsed.color,
        fill=parsed.fill, zero=parsed.zero, html=parsed.html, stretch=parsed.stretch
    )

if __name__ == '__main__':
    main()
