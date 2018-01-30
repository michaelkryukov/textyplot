Textyplot
=========
Simple, light project for drawing your diagrams with only text.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b61f81c2d568445fb297b1ff6caff8d6)](https://www.codacy.com/app/michaelkrukov/textyplot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=michaelkrukov/textyplot&amp;utm_campaign=Badge_Grade) [![Build Status](https://travis-ci.org/michaelkrukov/textyplot.svg?branch=master)](https://travis-ci.org/michaelkrukov/textyplot) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/b61f81c2d568445fb297b1ff6caff8d6)](https://www.codacy.com/app/michaelkrukov/textyplot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=michaelkrukov/textyplot&amp;utm_campaign=Badge_Coverage)

Features
========
 * Fast
 * Simple
 * Working with Python 3
 * Supports zooming and adjusting the view.
 * Text graphics with UTF-8 (⣧⡇⢸ )
 * Supports python3+

Installation
============
It's recommended to use pip to install/update.

To install:
```
sudo pip install textyplot
```

To update:
```
sudo pip install -U textyplot
```

To install from github:
```
sudo pip install git+https://github.com/michaelkrukov/textyplot.git
```

Code
===========
```
import textyplot

plotter = textyplot.Plotter(points, width=80, height=8)

plotter.show(
  zoom=True, data=True, border=True,
  color=False, fill=True, zero=True,
  html=False, stretch=True
)

plotter.save("file.txt", border=True)

with open("file.txt", "w") as o:
  plotter.write(o, color=True, html=True)
```

Code examples
=============
```
import textyplot

plotter = textyplot.Plotter([1, 2, 3, 4, 5, 3, 2, 1], width=80)
plotter.show()

plotter = textyplot.Plotter(i for i in range(100))
plotter.show()
```
![Result](/docs/code0.png)

```
import textyplot

plotter = textyplot.Plotter((i for i in range(100)), width=50)
plotter.show(color=True, fill=False)
```
![Result](/docs/code1.png)

```
import textyplot, math

plotter = textyplot.Plotter((math.sin(i / 5) * 5 for i in range(100)), width=50)
plotter.show(color=True, fill=False)
```
![Result](/docs/code2.png)

```
import textyplot, math

plotter = textyplot.Plotter((math.log(i) for i in range(1, 500)), width=80)
plotter.show(color=True, fill=False)
```
![Result](/docs/code3.png)

```
import textyplot, random

maximum = 48
plotter = textyplot.Plotter(
    random.random() * (maximum / 2 - abs(maximum / 2 - i)) for i in range(maximum)
)
plotter.show(color=True)
```
![Result](/docs/code4.png)

Command-line usage
============
```
usage: textyplot [-h] [-Z] [-B] [-D] [-C] [-F] [-G] [-H] [-S] [-R]
                 [-X characters] [-Y characters]

Text mode diagrams with possible colors usin UTF-8 colors.


optional arguments:
  -h, --help            show this help message and exit
  -Z, --no-zoom         zoom diagram (default: yes)
  -B, --no-border       draw border (default: yes)
  -D, --no-data         draw values (default: yes)
  -C, --no-color        use colors (default: yes)
  -F, --no-fill         fill diagram (default: yes)
  -G, --no-groud        draw zero line (default: yes)
  -H, --html            render to html (default: no)
  -S, --stretch         stretch points to width
  -R, --reverse         reverse points
  -X characters, --width characters
                        drawing max width (default: 80)
  -Y characters, --height characters
                        drawing height (default: 8)
```

Command-line examples
=======
```./bin/random 100 | python textyplot```
![Example #1](/docs/cmd1.png)

```./bin/random 100 | python textyplot -C```
![Example #2](/docs/cmd2.png)

```./bin/random 10 | python textyplot -X 80```
![Example #3](/docs/cmd3.png)

```./bin/random 10 | python textyplot -X 80 -S```
![Example #4](/docs/cmd4.png)

```./bin/random 400 | python textyplot```
![Example #5](/docs/cmd5.png)

```python ./bin/bitcoin.py | python textyplot -f 50```
![Example #6](/docs/cmd6.png)
