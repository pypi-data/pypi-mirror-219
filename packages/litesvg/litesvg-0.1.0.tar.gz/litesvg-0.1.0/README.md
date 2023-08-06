# litesvg package

This package provides tools to make svg objects (file or in a web page) with rectangles, ellipses, polygons and texts.

# Installation

```console
pip install litesvg
```

# First program

```python
from litesvg import LiteSvg, Rectangle,Text

svg = LiteSvg(width=500,height=200)

rect = Rectangle(x=50,width=400,y=50,height=100,rx=8)
rect.style.set(fill='#FFB030',stroke='#0060FF',stroke_width=10)
svg.add(rect)

text = Text(x=250,y=130,text='LITESVG')
text.style.set(font_size=80,font_weight='bold',text_anchor='middle',fill='#0060FF')
svg.add(text)

print(svg.render())

```

This program should print

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="500mm" height="200mm" viewBox="0 0 500 200">
<rect x="50" y="50" rx="8" ry="8" width="400" height="100" style="fill:#FFB030;stroke:#0060FF;stroke-width:10" />
<text x="250" y="130" id="text" style="fill:#0060FF;stroke:none;stroke-width:0.1;text-anchor:middle;font-family:sans-serif;font-weight:bold;font-size:80">LITESVG</text>
</svg>
```
and if you replace the last line of the program by
```python
svg.render('first_program.svg')
```
A file named *first_program.svg* is created containing the xml text above.

By opening it with Inkscape, for example, you will see the picture below.

![render](https://framagit.org/makeforartandscience/litesvg/-/raw/main/examples/first_program.png)

# Second program

```python
from litesvg import LiteSvg, Rectangle

svg = LiteSvg(config='litesvg.json',width=400,height=400,y_up=True)

Rectangle.set_default(width=44,height=44,anchor='center',rx=8)

for j in range(8):
    for i in range(8):
        r = Rectangle(x=25+50*i,y=25+50*j)
        r.style.set(fill='#{:02X}{:02X}80'.format(32*i,32*j))
        svg.add(r)

svg.render('colors.svg')
```

![render](https://framagit.org/makeforartandscience/litesvg/-/raw/main/examples/colors.png)