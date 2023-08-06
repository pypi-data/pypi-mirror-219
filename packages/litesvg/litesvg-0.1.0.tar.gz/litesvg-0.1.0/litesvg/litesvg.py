"""
LiteSvg package

LiteSvg package provides tools to create 2D shapes like polylines, add text and save them in .svg format.

Example:

from litesvg import LiteSvg, Polyline, Text

svg = LiteSvg(width=200,height=100,y_up=True)

p = Polyline()
p.add([(0,0),(150,0),(150,10),(140,20),(0,20)])
p.style.set(stroke='none',fill='yellow')
svg.add(p)

p = Polyline()
p.add([(0,0),(50,0),(50,10),(40,20),(0,20)])
p.transform.rotate(45,(25,10))
p.transform.translate((30,20))
p.style.set(stroke='none',fill='red')
svg.add(p)

p = Polyline()
p.add([(0,0),(50,0),(50,10),(40,20),(0,20)])
p.transform.scale(0.8,(0,0))
p.transform.translate((100,40))
p.style.set(stroke='none',fill='blue')
svg.add(p)

t = Text(x=30,y=8,text='LiteSvg')
t.style.set(font_size='0.5em')
svg.add(t)

t = Text(x=45,y=35,text='LiteSvg')
t.transform.rotate(45,(45,35))
t.style.set(font_size='0.5em',fill='#F0F0F0')
svg.add(t)

svg.render()    

"""
import logging
import json

from classattr import ClassAttr,RAISE,FORCE,IGNORE
if __name__ == '__main__':
    from transform import Transform
    from mathplus import is_number
else:
    from .transform import Transform
    from .mathplus import is_number


def _round(x,n=None):
    """
    return round value with n digits if n not None

    n number of digits, default None

    private function

    Example:
    >>> _round(5.326743,2)
    5.33
    >>> _round(5.326743)
    5.326743
    """

    if n == None:
        return x
    else:
        return round(x,n)
    

class Style(ClassAttr):
    """
    Style class containing attributes for svg items

    generic class for Polyline, Rectangle, Ellipse, Path, Text,... styles

    class contains attributes like fill,stroke,stroke_width

    """


    def __init__(self,attr = {},mode=RAISE,**kwargs):
        """
        create a svg style with default parameters
        """
        
        ClassAttr.__init__(self,attr,mode,**kwargs)
    
    def __repr__(self):
        """
        return style parameters like in svg commands
        All underscores in attributes (python compatibility) will be replace by a minus (svg compatibility)
        stroke_width will become stroke-width
        """

        style_attr = self.get()

        keys = list(style_attr.keys())

        for key in keys:
            if '_' in key:
                value = style_attr.pop(key,None)
                if value != None:
                    style_attr[key.replace('_','-')] = value

        return ";".join([key+':'+str(value) for key,value in style_attr.items()])

class PolylineStyle(Style):
    """
    Style class for Polylines containing attributes for svg items

    Examples:
    >>> style = PolylineStyle()
    >>> style.get()
    {'fill': 'none', 'stroke': 'black', 'stroke_width': 0.25}
    >>> style
    fill:none;stroke:black;stroke-width:0.25
    
    >>> style = PolylineStyle(stroke='green')
    >>> style.set(fill='red')
    >>> style.get()
    {'fill': 'red', 'stroke': 'green', 'stroke_width': 0.25}
    """

    fill = "none"
    stroke = "black"
    stroke_width = 0.25


class PathStyle(Style):
    """
    Style class for Path containing attributes for svg items

    Examples:
    >>> style = PathStyle()
    >>> style.get()
    {'fill': 'none', 'stroke': 'black', 'stroke_width': 0.25}
    >>> style
    fill:none;stroke:black;stroke-width:0.25
    
    >>> style = PathStyle(stroke='green')
    >>> style.set(fill='red')
    >>> style.get()
    {'fill': 'red', 'stroke': 'green', 'stroke_width': 0.25}
    """

    fill = "none"
    stroke = "black"
    stroke_width = 0.25


class RectangleStyle(Style):
    """
    Style class for Rectangle containing attributes for svg items

    Examples:
    >>> style = RectangleStyle()
    >>> style.get()
    {'fill': 'black', 'stroke': 'none', 'stroke_width': 0.25}
    """
    
    fill = "black"
    stroke = "none"
    stroke_width = 0.25
    
class EllipseStyle(Style):
    """
    Style class for Ellipse containing attributes for svg items

    Examples:
    >>> style = EllipseStyle()
    >>> style.get()
    {'fill': 'black', 'stroke': 'none', 'stroke_width': 0.25}
    """
    
    fill = "black"
    stroke = "none"
    stroke_width = 0.25

class TextStyle(Style):
    """
    Style class for Text
    class contains attributes fill,stroke,stroke_width
    but also text_anchor, font_family, font_size

    Examples:
    >>> style = TextStyle()
    >>> style.get()
    {'fill': 'black', 'stroke': 'none', 'stroke_width': 0.1, 'text_anchor': 'start', 'font_family': 'sans-serif', 'font_size': '0.2em'}
    """

    fill = 'black'
    stroke = 'none'
    stroke_width = 0.1
    text_anchor = 'start'
    font_family = 'sans-serif'
    font_weight = 'normal'
    font_size = '0.2em'


class Element(ClassAttr):
    """
    Element class is meta class for svg object like Polygon, Text, ...

    """
    
    def __init__(self,attr={},mode=RAISE,item_id='element',**kwargs):
        """
        Create a new element
        """

        self.item_id = item_id

        ClassAttr.__init__(self,attr,mode,**kwargs)

class PShape(Element):
    """
    PShape is a primitive class for Rectangle, Ellipse
    """

    x = 0
    y = 0
    width = 100
    height = 50
    anchor = 'topleft'

    def __init__(self,attr={},mode=RAISE,item_id='shape',**kwargs):
        """
        create a new PShape
        """

        self.transform = Transform()

        Element.__init__(self,attr,mode,item_id,**kwargs)

    
    def set(self,attr={},mode=RAISE,**kwargs):
        """
        set parameters of the PShape like anchor
        
        """

        attr = {**attr,**kwargs}

        anchors = ('topleft','top','topright','left','center','right','bottomleft','bottom','bottomright')
        for key,value in attr.items():
            if key == 'anchor':
                if value not in anchors:
                    raise ValueError('Unvalid value {} for {}. Available values are {}'.format(value,key,anchors))

        super().set(attr=attr,mode=mode)

    def output(self,n=None):
        """
        return the PShape as a svg command
        
        Examples:
        >>> item = Rectangle(x=50,y=40,width=30,height=60)
        >>> item.style.set(fill='red')
        >>> print(item.output())
        <rect x="50" y="40" rx="0" ry="0" width="30" height="60" style="fill:red;stroke:none;stroke-width:0.25" />
        """

        if self.transform.y_up:
            y = self.transform.height - self.y
        else:
            y = self.y
            
        if self.anchor in ('left','center','right'):
            y -= self.height/2
        elif self.anchor in ('bottomleft','bottom','bottomright'):
            y -= self.height


        if self.anchor in ('top','center','bottom'):
            x = self.x - self.width/2
        elif self.anchor in ('topright','right','bottomright'):
            x = self.x - self.width
        else:
            x = self.x

        if isinstance(self,Rectangle):

            if self.ry == None:
                ry = self.rx
            else:
                ry = self.ry

            if self.transform.is_identity():
                return '<rect x="{}" y="{}" rx="{}" ry="{}" width="{}" height="{}" style="{}" />'.format(_round(x,n),_round(y,n),_round(self.rx,n),
                                                                                                         _round(ry,n),_round(self.width,n),
                                                                                                         _round(self.height,n),self.style.__repr__())
            else:
                return '<rect x="{}" y="{}" rx="{}" ry="{}" width="{}" height="{}" transform="{}" style="{}" />'.format(_round(x,n),_round(y,n),
                                                                                                                        _round(self.rx,n),_round(ry,n),
                                                                                                                        _round(self.width,n),
                                                                                                                        _round(self.height,n),
                                                                                                                        self.transform.get(),
                                                                                                                        self.style.__repr__())

        if isinstance(self,Ellipse):
            if self.transform.is_identity():
                return '<ellipse cx="{}" cy="{}" rx="{}" ry="{}" style="{}" />'.format(_round(x+self.width/2,n),_round(y+self.height/2,n),
                                                                                       _round(self.width/2,n),_round(self.height/2,n),
                                                                                       self.style.__repr__())
            else:
                return '<ellipse cx="{}" cy="{}" rx="{}" ry="{}" transform="{}" style="{}" />'.format(_round(x+self.width/2,n),
                                                                                                      _round(y+self.height/2,n),
                                                                                                      _round(self.width/2,n),
                                                                                                      _round(self.height/2,n),
                                                                                                      self.transform.get(),self.style.__repr__())

        else:
            raise ValueError('Impossible to output {} type'.format(type(self).__name__))

class Rectangle(PShape):
    """
    Rectangle class
    
    Example:
    >>> item = Rectangle(x=20,y=20,width=30,height=10)
    >>> item.style.set(stroke='blue')
    >>> print(item.output())
    <rect x="20" y="20" rx="0" ry="0" width="30" height="10" style="fill:black;stroke:blue;stroke-width:0.25" />
    """

    rx = 0
    ry = None

    def __init__(self,attr={},mode=RAISE,item_id='rectangle',**kwargs):
        """
        create a new Rectangle

        Example:
        >>> item = Rectangle(x=20,y=20,width=30,height=10,rx=6)
        """
        self.style = RectangleStyle()
        PShape.__init__(self,attr,mode,item_id,**kwargs)

class Ellipse(PShape):
    """
    Elleipse class
    
    Example:
    >>> item = Ellipse(x=20,y=20,width=30,height=10)
    >>> item.style.set(stroke='blue')
    """

    def __init__(self,attr={},mode=RAISE,item_id='rectangle',**kwargs):
        """
        create a new Ellipse

        Example:
        >>> item = Ellipse(x=50,y=30,width=60,height=40)
        """
        
        self.style = EllipseStyle()
        PShape.__init__(self,attr,mode,item_id,**kwargs)
      
class Polyline(Element):
    """
    Polyline is a closed or open polygon defined by vertices

    Examples:
    >>> item = Polyline()
    >>> item.add([(0,0),(1,0),(0.5,0.5)])
    >>> print(item.output())
    <path d="M 0,0 L 1,0 0.5,0.5 Z" id="path" style="fill:none;stroke:black;stroke-width:0.25"/>
    """

    closed = True

    def __init__(self,attr={},mode=RAISE,item_id='path',**kwargs):
        """
        create a new polyline

        Examples:
        >>> item = Polyline(item_id='new_poly')
        >>> item.style.set(stroke='red')
        """

        self.style = PolylineStyle()
        self.transform = Transform()

        self.clear()
        
        Element.__init__(self,attr,mode,item_id,**kwargs)
        
    def clear(self):
        """
        remove all vertices and set transform to none

        Examples:
        >>> item = Polyline()
        >>> item.add([(0,0),(1,0),(0.5,0.5)])
        >>> item.clear()
        """

        self.vertices = []
        self.transform.clear()
        

    def add(self,vertices):
        """
        add vertices to the polyline

        Examples:
        >>> item = Polyline()
        >>> item.add([(0,0),(1,0)])
        >>> item.add([(0.5,0.5)])
        >>> print(item.output())
        <path d="M 0,0 L 1,0 0.5,0.5 Z" id="path" style="fill:none;stroke:black;stroke-width:0.25"/>
        """

        self.vertices.extend(vertices)


    def output(self,n=None):
        """
        return the polygon as a svg command
        
        Examples:
        >>> item = Polyline()
        >>> item.style.set(fill='red')
        >>> item.add([(0,0),(1,0),(0.5,0.5)])
        >>> print(item.output())
        <path d="M 0,0 L 1,0 0.5,0.5 Z" id="path" style="fill:red;stroke:black;stroke-width:0.25"/>
        >>> item.set(closed=False,item_id='triangle')
        >>> item.style.set(fill='none')
        >>> print(item.output())
        <path d="M 0,0 L 1,0 0.5,0.5" id="triangle" style="fill:none;stroke:black;stroke-width:0.25"/>
        >>> item.transform.set(y_up=True,height=1)
        >>> print(item.output())
        <path d="M 0,1 L 1,1 0.5,0.5" id="triangle" style="fill:none;stroke:black;stroke-width:0.25"/>
        
        """

        if len(self.vertices) > 1:
            if self.transform.y_up:
                v = [(x[0],self.transform.height-x[1]) for x in self.vertices]
            else:
                v = self.vertices

            if not self.transform.is_identity():
                v = [self.transform.apply(x) for x in v]


            m = str(_round(v[0][0],n))+','+str(_round(v[0][1],n))
            path = 'M {} L {}'.format(m,' '.join([str(_round(x[0],n))+','+str(_round(x[1],n)) for x in v[1:]]))
                

            if self.closed:
                path += ' Z'

            return '<path d="{}" id="{}" style="{}"/>'.format(path,self.item_id,self.style.__repr__())

        else:
            return ''

class Path(Element):

    def __init__(self,attr={},mode=RAISE,item_id='path',**kwargs):
        """
        create a new path

        Examples:
        >>> item = Path(item_id='new_path',path='m 50,0 l 100,0 -50,50 z')
        >>> item.style.set(stroke='red')
        >>> print(item.output())
        <path d="M 50.0,0.0 L 150.0,0.0 100.0,50.0 Z" id="new_path" style="fill:none;stroke:red;stroke-width:0.25"/>
        """

        self.path = ''
        self.abspath = []
        self.style = PathStyle()
        self.transform = Transform()
       
        Element.__init__(self,attr,mode,item_id,**kwargs)


    def _absolute(self):
        """
        return path as a list of commands with absolute vertices

        private function

        """
           
        path = self.path.split()
        l = len(path)
        for i in range(l):
            if ',' in path[i]:
                path[i] = tuple([float(x) for x in path[i].split(',')])
            elif is_number(path[i]):
                path[i] = float(path[i])

        # make absolute path
        xpos = 0
        ypos = 0
        xstart = 0
        ystart = 0
        i = 0
        current = None

        while i < l:
            if path[i] == 'M':  # absolute first position
                xpos,ypos = path[i+1]
                xstart,ystart = (xpos,ypos)
                i += 2
                if i < l and isinstance(path[i],tuple):
                    path.insert(i,'L')
                    l +=1
                current = 'M'
            elif path[i] == 'm':  # relative first position
                path[i] = 'M'
                xpos += path[i+1][0]
                ypos += path[i+1][1]
                xstart,ystart = (xpos,ypos)
                path[i+1] = (xpos,ypos)
                i += 2
                if i < l and isinstance(path[i],tuple):
                    path.insert(i,'l')
                    l += 1
                current = 'M'
            elif path[i] == 'L':  # absolute line
                if current == 'L':
                    path.pop(i)
                    l -= 1
                else:
                    i += 1
                while i < l and isinstance(path[i],tuple):
                    xpos,ypos = path[i]
                    i += 1
                current = 'L'
            elif path[i] == 'l':  # relative line to absolute
                if current == 'L':
                    path.pop(i)
                    l -= 1
                else:
                    path[i] = 'L'
                    i += 1
                while i < l and isinstance(path[i],tuple):
                    xpos += path[i][0]
                    ypos += path[i][1]
                    path[i] = (xpos,ypos)
                    i += 1
                current = 'L'
            elif path[i] == 'H':  # absolute horizontal to absolute line
                if current == 'L':
                    path.pop(i)
                    l -= 1
                else:
                    path[i] = 'L'
                    i += 1
                while i < l and is_number(path[i]):
                    xpos = path[i]
                    path[i] = (xpos,ypos)
                    i += 1
                current = 'L'
            elif path[i] == 'h':  # relative horizontal to absolute line
                if current == 'L':
                    path.pop(i)
                    l -= 1
                else:
                    path[i] = 'L'
                    i += 1
                while i < l and is_number(path[i]):
                    xpos += path[i]
                    path[i] = (xpos,ypos)
                    i += 1
                current = 'L'
            elif path[i] == 'V':  # absolute vertical to absolute line
                if current == 'L':
                    path.pop(i)
                    l -= 1
                else:
                    path[i] = 'L'
                    i += 1
                while i < l and is_number(path[i]):
                    ypos = path[i]
                    path[i] = (xpos,ypos)
                    i += 1
                current = 'L'
            elif path[i] == 'v': # relative vertical to absolute line
                if current == 'L':
                    path.pop(i)
                    l -= 1
                else:
                    path[i] = 'L'
                    i += 1
                while i < l and is_number(path[i]):
                    ypos += path[i]
                    path[i] = (xpos,ypos)
                    i += 1
                current = 'L'
            elif path[i] == 'C': # absolute cubic
                i += 1
                while i+3 < l and isinstance(path[i+3],tuple):
                    i += 3
                xpos,ypos = path[i+2]
                i += 3
                current = 'C'
            elif path[i] == 'c':  # relative cubic to absolute
                path[i] = 'C'
                i += 1
                for k in range(3):
                    path[i+k] = (xpos+path[i+k][0],ypos+path[i+k][1])
                xpos,ypos = path[i+2]
                while i+3 < l and isinstance(path[i+3],tuple):
                    i += 3
                    for k in range(3):
                        path[i+k] = (xpos+path[i+k][0],ypos+path[i+k][1])
                    xpos,ypos = path[i+2]
                i += 3
                current = 'C'
            elif path[i] == 'Z':  # closepath
                xpos,ypos = (xstart,ystart)
                i += 1
            elif path[i] == 'z':  # closepath
                xpos,ypos = (xstart,ystart)
                path[i] = 'Z'
                i += 1                
            else:
                raise ValueError('unexpected {} at {}'.format(path[i],i))

        self.abspath = path


    def output(self,n=None):
        """
        return the path as a svg command
        
        Examples:
        >>> item = Path(item_id='new_path',path='m 50,0 l 100,0 -50,50 z')
        >>> print(item.output())
        <path d="M 50.0,0.0 L 150.0,0.0 100.0,50.0 Z" id="new_path" style="fill:none;stroke:black;stroke-width:0.25"/>
        >>> item.transform.set(y_up=True,height=200)
        >>> print(item.output())
        <path d="M 50.0,200.0 L 150.0,200.0 100.0,150.0 Z" id="new_path" style="fill:none;stroke:black;stroke-width:0.25"/>
        """

        if len(self.path) > 1:

            self._absolute()


            if self.transform.y_up:
                p = [(x[0],self.transform.height-x[1]) if not isinstance(x,str) else x for x in self.abspath]
            else:
                p = self.abspath

            if not self.transform.is_identity():
                p = [self.transform.apply(x) if not isinstance(x,str) else x for x in p]

            p = ' '.join([str(_round(x[0],n))+','+str(_round(x[1],n)) if not isinstance(x,str) else x for x in p])

            return '<path d="{}" id="{}" style="{}"/>'.format(p,self.item_id,self.style.__repr__())

        else:
            return ''


class Text(Element):
    """
    Text is a text string in svg drawing

    main parameters are
    text is a text string
    x and y anchor coordinates bottom left 

    Examples:
    >>> item = Text(x=20,y=30,text='Hello world!')
    >>> item.output()
    '<text x="20" y="30" id="text" style="fill:black;stroke:none;stroke-width:0.1;text-anchor:start;font-family:sans-serif;font-size:0.2em">Hello world!</text>'
    """

    def __init__(self,attr={},mode=RAISE,item_id='text',**kwargs):
        """
        Create a new text object

        Examples:
        >>> item = Text()
        >>> item.set(x=20,y=30,text='Hello world!')

        >>> item = Text(x=20,y=30,text='Hello world!')
        """

        self.x = 0
        self.y = 0
        self.text = ''
        self.style = TextStyle()
        self.transform = Transform()

        Element.__init__(self,attr,mode,item_id,**kwargs)

    def output(self,n=None):
        """
        render svg command for text object
        
        Examples:
        >>> item = Text(x=20,y=30,text='Hello world!')
        >>> item.output()
        '<text x="20" y="30" id="text" style="fill:black;stroke:none;stroke-width:0.1;text-anchor:start;font-family:sans-serif;font-size:0.2em">Hello world!</text>'
        >>> item.transform.set(y_up=True,height=100)
        >>> item.output()
        '<text x="20" y="70" id="text" style="fill:black;stroke:none;stroke-width:0.1;text-anchor:start;font-family:sans-serif;font-size:0.2em">Hello world!</text>'
        """

        if self.transform.y_up:
            y = self.transform.height - self.y
        else:
            y = self.y

        if self.transform.is_identity():
            return '<text x="{}" y="{}" id="{}" style="{}">{}</text>'.format(_round(self.x,n),_round(y,n),self.item_id,self.style.__repr__(),
                                                                             self.text)
        else:
            return '<text x="{}" y="{}" id="{}" transform="{}" style="{}">{}</text>'.format(_round(self.x,n),_round(y,n),self.item_id,
                                                                                            self.transform.get(),self.style.__repr__(),self.text)

     
class LiteSvg(ClassAttr):
    """
    Lite Svg manages very simple svg object

    Examples:
    
    svg = LiteSvg(y_up=True)

    p = Polyline()
    p.add([(0,0),(10,0),(43,6),(10,50),(20,17)])
    p.style.set(stroke='red')
    svg.add(p)
    
    svg.add(Polyline(vertices=[(0,0),(100,0),(30,60)]))

    t = Text(x=20,y=35,text='Test')
    t.style.set(fill='blue')
    svg.add(t)

    svg.save_as('test.svg')    
    
    """

    header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg width="{0}mm" height="{1}mm" viewBox="0 0 {0} {1}">\n'
    footer ='</svg>\n'
    web_header = '<svg width="{0}mm" height="{1}mm">\n'
    web_footer ='</svg>\n'
    width = 100
    height = 100
    y_up = False

    def __init__(self,config='',**kwargs):
        """
        Create a new svg

        config is config file
        you can add extra parameters as
        width number is picture width, default is 100 or value in config file
        height number is picture height, default is 100 or value in config file
        y_up boolean if True positive y are up else down, default is False or value in config file

        Examples:
        >>> svg = LiteSvg()
        >>> svg.width
        100

        >>> svg = LiteSvg(width = 600, height = 400)
        >>> svg.width
        600
        >>> svg = LiteSvg(width = 600, height = 400, y_up = True)
        """

        self.items = []
        self.current = None

        if config:
            try:
                with open(config) as f:
                    attr = json.load(f)
            except:
                logging.basicConfig(format='Warning : %(message)s')
                logging.warning('Unable to read config file {}'.format(config))
                attr = {}

            classes = (LiteSvg,Path,Polyline,Rectangle,Ellipse,Text,PathStyle,PolylineStyle,RectangleStyle,EllipseStyle,TextStyle)
            for c in classes:
                if c.__name__ in attr:
                    c.set_default(attr = attr[c.__name__])

        ClassAttr.set(self,**kwargs)


    def _item_id(self, item_id):
        """
        return item_id if it doesn't exist in paths
        else return item_id followed by a dot and a unique number

        private function 
        """

        ids = [p.get('item_id') for p in self.items]
        
        if item_id in ids:
            # si le nom existe deja
            if len(item_id.split('.')) == 1:
                new_id = [item_id, '1']
            else:
                try:
                    i = int(item_id.split('.')[-1])
                    new_id = ['.'.join(item_id.split('.')[0:-1]), str(i+1)]
                except ValueError:
                    new_id = [item_id, '1']
            while '.'.join(new_id) in ids:
                new_id[1] = str(int(new_id[1]) + 1)
            return '.'.join(new_id)
        else:
            return item_id
        
    def add(self,item):
        """
        add a polygon, text, ... to svg object and return item id

        Example:
        >>> svg = LiteSvg(y_up=True)

        >>> p = Polyline(vertices=[(0,0),(10,0),(43,6),(10,50),(20,17)])
        >>> svg.add(p)
        'path'
        """
        item.item_id  = self._item_id(item.item_id)

        self.items.append(item)
        self.current = item

        return item.item_id


    def select(self,item_id):
        """
        set an item to current using its item_id.
        returnTrue if found else False
        
        Example:
        >>> svg = LiteSvg(y_up=True)

        >>> svg.add(Text(x=0,y=0,text='Hello'))
        'text'
        >>> svg.add(Polyline(vertices=[(0,0),(10,0),(43,6),(10,50),(20,17)]))
        'path'
        >>> svg.current.item_id
        'path'
        >>> svg.select('text')
        True
        >>> svg.current.item_id
        'text'
        >>> svg.select('wrong_id')
        False
        >>> print(svg.current)
        None
        """

        for item in self.items:
            if item.item_id == item_id:
                self.current = item
                return True
        self.current = None
        return False


    def render(self,filename='',web=False,n=4):
        """
        return svg object if filename is empty else save svg object in file filename

        Parameters :
        filename str filename used to save the render, if empty print return the string, default empty
        web boolean, default False if True use web_header and web_footer parameters else header and footer 

        Examples : 

        >>> svg = LiteSvg(width=200,height=100,y_up=True)
        >>> p = Polyline(vertices=[(100,0),(200,0),(200,50)])
        >>> p.style.set(fill='yellow',stroke='none')
        >>> svg.add(p)
        'path'
        >>> svg.add(Text(x=20,y=10,text='LiteSvg'))
        'text'
        >>> print(svg.render())
        <?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg width="200mm" height="100mm" viewBox="0 0 200 100">
        <path d="M 100,100 L 200,100 200,50 Z" id="path" style="fill:yellow;stroke:none;stroke-width:0.25"/>
        <text x="20" y="90" id="text" style="fill:black;stroke:none;stroke-width:0.1;text-anchor:start;font-family:sans-serif;font-size:0.2em">LiteSvg</text>
        </svg>
        <BLANKLINE>
        >>> print(svg.render(web=True))
        <svg width="200mm" height="100mm">
        <path d="M 100,100 L 200,100 200,50 Z" id="path" style="fill:yellow;stroke:none;stroke-width:0.25"/>
        <text x="20" y="90" id="text" style="fill:black;stroke:none;stroke-width:0.1;text-anchor:start;font-family:sans-serif;font-size:0.2em">LiteSvg</text>
        </svg>
        <BLANKLINE>
        """

        if web:
            header = self.web_header
            footer = self.web_footer
        else:
            header = self.header
            footer = self.footer

        content = header.format(self.width,self.height)

        for item in self.items:
            item.transform.set(y_up = self.y_up,height=self.height)
            content += item.output(n)+'\n'
           
        content += self.footer

        if filename: 
            with open(filename,'w') as f:
                f.write(content)
        else:
            return content

if __name__ == '__main__':

    import doctest
    doctest.testmod()
