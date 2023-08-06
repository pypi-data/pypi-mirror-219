"""
Transform package

This package provides tools to set transform matrix such as translation, rotation, ...

Example :
>>> a = Transform()
>>> a.is_identity()
True
>>> a.translate((2,3))
>>> a.is_identity()
False
>>> a.get()
'matrix(1.0,0.0,0.0,1.0,2.0,3.0)'
>>> a.clear()
>>> a.rotate(90,(2,1))
>>> a.get()
'matrix(0.0,1.0,-1.0,0.0,3.0,-1.0)'
>>> a.apply((3,1))
(2.0, 2.0)
"""
import numpy as np
import re

from classattr import ClassAttr,RAISE,FORCE,IGNORE


class Matrix2D(object):

    def __init__(self,m = [[1,0,0],[0,1,0]]):
        """
        Create a 2D matrix
        v is a 2 coordinates tuple or list

        Example:
        >>> t = Matrix2D()
        """

        self.matrix = np.array([m[0],m[1],[0,0,1]],dtype=float)

    def __repr__(self):
        """
        return matrix array as a string

        Example:
        >>> t = Matrix2D()
        >>> t
        [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0]]
        """

        return '['+'],'.join(['['+', '.join([str(round(self.matrix[i][j],6)) for j in range(3)]) for i in range(3)])+']]'


    def mul(self,tm):
        """
        left multilply self matrix by tm matrix

        Example:

        >>> t = Matrix2D([[1,0,2],[0,1,3]])
        >>> t2 = Matrix2D([[1,0,5],[0,1,-1]])
        >>> t.mul(t2)
        >>> t
        [[1.0, 0.0, 7.0],[0.0, 1.0, 2.0],[0.0, 0.0, 1.0]]
        """

        self.matrix = np.matmul(tm.matrix,self.matrix)


    def apply(self,v):
        """
        transform a vertice
        v is a 2 coordinates tuple or list

        Example:

        >>> t = Matrix2D([[1,0,2],[0,1,3]])
        >>> t.apply((2,4))
        (4.0, 7.0)
        """

        vec = np.array([v[0],v[1],1])
        return tuple(self.matrix.dot(vec).tolist()[:2])
    

class Transform(ClassAttr):

    y_up = False
    height = 0
    
    def __init__(self,attr = {},mode=RAISE,**kwargs):
        """
        create a 2D transform matrix

        corresponding to the mathematical transformation matrix
        (a b c)
        (d e f)
        (0 0 1)

        Example:

        >>> t = Transform()
        >>> t
        [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0]]
        """

        self.clear()
        
        ClassAttr.__init__(self,attr,mode,**kwargs)
        

    def set(self,attr = {},mode=RAISE,**kwargs):

        ClassAttr.set(self,attr,mode,**kwargs)
        self.matrix = self.get_matrix()
        

    def clear(self):
        """
        clear the transform matrix

        corresponding to set the mathematical transformation matrix to
        (1 0 0)
        (0 1 0)
        (0 0 1)

        Example:

        >>> t = Transform()
        >>> t.translate((2,3))
        >>> t
        [[1.0, 0.0, 2.0],[0.0, 1.0, 3.0],[0.0, 0.0, 1.0]]
        >>> t.clear()
        >>> t
        [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0]]
        """

        self.transform = ''
        self.matrix = self.get_matrix()


    def __repr__(self):
        """
        return Transform matrix as string 

        Example
        
        >>> t = Transform()
        >>> t.translate((2,3))
        >>> t
        [[1.0, 0.0, 2.0],[0.0, 1.0, 3.0],[0.0, 0.0, 1.0]]
        """

        return self.get_matrix().__repr__()

       
    def translate(self,v):
        """
        add a translation
        v is a 2 coordinates tuple or list (x,y)
        corresponding to multiply by the mathematical matrix
        (1 0 v.x)
        (0 1 v.y)
        (0 0  1 )

        Example:

        >>> t = Transform()
        >>> t.translate((2,-3))
        >>> t
        [[1.0, 0.0, 2.0],[0.0, 1.0, -3.0],[0.0, 0.0, 1.0]]
        """
        
        if self.transform != '':
            self.transform += '*'
        self.transform += 't,{}'.format(','.join([str(round(x,6)) for x in v]))

        self.matrix = self.get_matrix()
              

    def scale(self,k,center=(0,0)):
        """
        add a scale
        center is center coordinates tuple or list (x,y) 
        k is a number
        
        corresponding to multiply by the mathematical matrix
        (k 0 x*(1+k))
        (0 k y*(1-k))
        (0 0 1)

        Example:

        >>> t = Transform()
        >>> t.scale(2)
        >>> t
        [[2.0, 0.0, 0.0],[0.0, 2.0, 0.0],[0.0, 0.0, 1.0]]
        >>> t.clear()
        >>> t.scale(2,(2,1))
        """
        
        if self.transform != '':
            self.transform += '*'
        self.transform += 's,{},{}'.format(str(round(k,6)),','.join([str(round(x,6)) for x in center]))

        self.matrix = self.get_matrix()
        

    def flip(self,mode = 'H',center=(0,0)):
        """
        add a flip
        mode can be 'H'(horizontal flip) or 'V'(vertical flip) or 'O'(center flip)
        center is center coordinates tuple (x,y)
        
        Example:

        >>> t = Transform()
        >>> t.flip('H')
        >>> t
        [[1.0, 0.0, 0.0],[0.0, -1.0, 0.0],[0.0, 0.0, 1.0]]
        """

        if self.transform != '':
            self.transform += '*'
        if mode in ('H','V','O'):
            self.transform += 'f,{},{}'.format(mode,','.join([str(round(x,6)) for x in center]))
        else:
            raise ValueError('Wrong mode value {}, should be H(horizontal), V(vertical), O(origin)'.format(mode)) 

        self.matrix = self.get_matrix()


    def rotate(self,a,center=(0,0)):
        """
        add a rotation
        center is center coordinates tuple (x,y) 
        a is the angle in degrees, positive value is clockwise
        
        corresponding to multiply by the mathematical matrix
        (cos(a) -sin(a) x(1-cos(a))+ysin(a))
        (sin(a) cos(a)  y(1-cos(a))-xsin(a))
        (0      0       1                  )

        Example:

        >>> t = Transform()
        >>> t.rotate(90,(1,3))
        >>> t
        [[0.0, -1.0, 4.0],[1.0, 0.0, 2.0],[0.0, 0.0, 1.0]]
        """

        if self.transform != '':
            self.transform += '*'
        self.transform += 'r,{},{}'.format(a,','.join([str(round(x,6)) for x in center]))

        self.matrix = self.get_matrix()

        
    def apply(self,v):
        """
        apply the transform to a vertice
        v is a 2 coordinates tuple or list

        Example:

        >>> t = Transform()
        >>> t.scale(2)
        >>> t.translate((10,-5))
        >>> t.apply((2,3))
        (14.0, 1.0)
        """

        vec = np.array([v[0],v[1],1])

        return tuple(self.matrix.matrix.dot(vec).tolist()[:2])


    def get_matrix(self):
        """
        return mathematical matrix
        (a b c)
        (d e f)
        (0 0 1)

        Example:

        >>> t = Transform()
        >>> t.scale(2)
        >>> t.translate((10,-5))
        >>> t.get_matrix()
        [[2.0, 0.0, 10.0],[0.0, 2.0, -5.0],[0.0, 0.0, 1.0]]
        """

        matrix = np.identity(3)

        l = self.transform

        if l:
            for t in l.split('*'):
                o = t.split(',')
                if o[0] == 't':
                    x = float(o[1])
                    if self.y_up:
                        y = -float(o[2])
                    else:
                        y = float(o[2])
                    tm = np.array([[1,0,x],[0,1,y],[0,0,1]],dtype=float)
                    matrix = np.matmul(tm,matrix)
                    
                elif o[0] == 's':
                    k = float(o[1])
                    x = float(o[2])
                    if self.y_up:
                        y = self.height-float(o[3])
                    else:
                        y = float(o[3])
                    tm = np.array([[k,0,x*(1-k)],[0,k,y*(1-k)],[0,0,1]],dtype=float)
                    matrix = np.matmul(tm,matrix)
                    
                elif o[0] == 'r':
                    a = float(o[1])
                    x = float(o[2])
                    if self.y_up:
                        y = self.height-float(o[3])
                    else:
                        y = float(o[3])
                    cosa = np.cos(np.radians(a))
                    sina = np.sin(np.radians(a))
                    tm = np.array([[cosa,-sina,x*(1-cosa)+y*sina],[sina,cosa,y*(1-cosa)-x*sina],[0,0,1]],dtype=float)
                    matrix = np.matmul(tm,matrix)
                    
                elif o[0] == 'f':
                    mode = o[1]
                    x = float(o[2])
                    if self.y_up:
                        y = self.height-float(o[3])
                    else:
                        y = float(o[3])

                    if mode =='H':
                        tm = np.array([[1,0,0],[0,-1,2*y],[0,0,1]],dtype=float)
                    elif mode =='V':
                        tm = np.array([[-1,0,2*x],[0,1,0],[0,0,1]],dtype=float)
                    elif mode =='O':
                        tm = np.array([[-1,0,2*x],[0,-1,2*y],[0,0,1]],dtype=float)
                    else:
                        raise ValueError('Wrong mode value {}, should be H(horizontal), V(vertical), O(origin)'.format(mode)) 
                    matrix = np.matmul(tm,matrix)
                else:
                    raise ValueError('Wrong transform')
                    
        return Matrix2D(matrix)


    def get(self):
        """
        return transform matrix as a 6 numbers string

        if mathematical matrix is
        (a b c)
        (d e f)
        (0 0 1)
        then return 'matrix(a,d,b,e,c,f)'

        Example:

        >>> t = Transform()
        >>> t.scale(2)
        >>> t.translate((10,-5))
        >>> t.get()
        'matrix(2.0,0.0,0.0,2.0,10.0,-5.0)'
        """
        
        b = self.get_matrix().matrix
        o = (b[0][0],b[1][0],b[0][1],b[1][1],b[0][2],b[1][2])

        return 'matrix('+','.join([str(round(x,6)) for x in o])+')'


    def is_identity(self):
        """
        return True if trandform matrix is no transform else False

        Example:

        >>> t = Transform()
        >>> t.is_identity()
        True
        >>> t.translate((10,-5))
        >>> t.is_identity()
        False
        """

        if self.get() == 'matrix(1.0,0.0,0.0,1.0,0.0,0.0)':
            return True
        else:
            return False


if __name__ == "__main__":

    import doctest
    doctest.testmod()
