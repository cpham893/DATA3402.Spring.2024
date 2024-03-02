class shapes:
    def __init__(self, x, y):
        self.__coor=(x,y)   

    def get_coordinates(self):
        return self.__coor

    def get_points(self):
        raise NotImplementedError
        
    def check_coordinate(self):
        raise NotImplementedError
    
    def is_overlap(self, other):        
        my_points = self.get_points()
        other_points = other.get_points()

        for p in other_points:
            if self.check_coordinate(p[0], p[1]):
                return True

        for p in my_points:
            if other.check_coordinate(p[0], p[1]):
                return True
            else:
                return False

    def paint(self, canvas): 
        pass

class rectangle(shapes):
    def __init__(self, length, width, x, y, init_parent=True):
        if init_parent:
            super(rectangle,self).__init__(x, y)
        self.__l=length
        self.__w=width

    def area(self):
        self.__a=self.__l*self.__w

    def perimeter(self):
        self.__p=(2*self.__l)+(2*self.__w)

    def get_area(self):
        return self.__a

    def get_perimeter(self):
        return self.__p

    def check_coordinate(self, check_x=None, check_y=None): # coordinate is in the bottom left corner of the rectangle
        if (self.get_coordinates()[0] <= check_x <= self.get_coordinates()[0]+self.__w) and \
            (self.get_coordinates()[1] <= check_y <= self.get_coordinates()[1]+self.__l):
            return True
        else:
            return False

    def perimeter_points(self, point=16):
        p_points=[]
        p_points.append((self.get_coordinates()[0], self.get_coordinates()[1])) #bottom left
        p_points.append((self.get_coordinates()[0] + self.__w, self.get_coordinates()[1])) #bottom right
        p_points.append((self.get_coordinates()[0], self.get_coordinates()[1] + self.__l)) #top left        
        p_points.append((self.get_coordinates()[0] + self.__w, self.get_coordinates()[1] + self.__l)) #top right

        for i in range(1,4):
            top = self.get_coordinates()[0] + (self.__w * i / 4)
            p_points.append((top, self.get_coordinates()[1] + self.__l))

        for i in range(1, 4):
            right = self.get_coordinates()[1] + (self.__l * i / 4)
            p_points.append((self.get_coordinates()[0] + self.__w, right))

        for i in range(1, 4):
            bottom = self.get_coordinates()[0] + (self.__w * (4 - i) / 4)
            p_points.append((bottom, self.get_coordinates()[1]))

        for i in range(1, 4):
            left = self.get_coordinates()[1] + (self.__l * (4 - i) / 4)
            p_points.append((self.get_coordinates()[0], left))

        return p_points

    def paint(self, canvas):
        points = self.perimeter_points()
        for x, y in points:
            canvas.set_pixel(int(x), int(y))
        
class circle(shapes):
    def __init__(self, radius, x, y, init_parent=True):
        if init_parent:
            super(circle,self).__init__(x, y)
        self.__r=radius
        self.__i=None
        self.__j=None

    def area(self):
        self.__a=math.pi*self.__r**2

    def perimeter(self):
        self.__p=2*math.pi*self.__r

    def get_area(self):
        return self.__a

    def get_perimeter(self):
        return self.__p

    def check_coordinate(self, check_x=None, check_y=None): # coordinate is at the center of the circle
        dist_=(((check_x-self.get_coordinates()[0])**2)+((check_y-self.get_coordinates()[1])**2))**0.5
        if dist_<=self.__r:
            return True
        else:
            return False

    def perimeter_points(self, point=16):
        p_points=[]  
        for i in range(point):
            a=2*math.pi*i/point
            x=self.get_coordinates()[0] + self.__r*math.cos(a)
            y=self.get_coordinates()[1] + self.__r*math.sin(a)
            p_points.append((x,y))

        return p_points

    def paint(self, canvas):
        points = self.perimeter_points()
        for x, y in points:
            canvas.set_pixel(int(x), int(y))

class triangle(shapes):
    def __init__(self, x1, y1, x2, y2, x3, y3, init_parent=True):
        if init_parent:
            super(triangle,self).__init__(x1, y1)
        self.__coor1=(x1,y1)
        self.__coor2=(x2,y2)
        self.__coor3=(x3,y3)
        self.__a=None
        self.__p=None    

    def is_triangle(self):
        self.__one = math.dist(self.__coor1, self.__coor2)
        self.__two = math.dist(self.__coor2, self.__coor3)
        self.__three = math.dist(self.__coor3, self.__coor1)

        if (self.__one+self.__two>self.__three) and (self.__one+self.__three>self.__two) and (self.__two+self.__three>self.__one):
            return True
        else:
            print("not a triangle")
            return False
    
    def area(self):
        if self.is_triangle()==True:
            s=0.5*(self.__one+self.__two+self.__three)
            self.__a=(s*(s-self.__one)*(s-self.__two)*(s-self.__three))**0.5

    def perimeter(self):
        if self.is_triangle()==True:
            self.__p=self.__one+self.__two+self.__three

    def get_area(self):
        return self.__a

    def get_perimeter(self):
        return self.__p

    def check_coordinate(self, check_x=None, check_y=None): # coordinates are at each corner
        d=((self.__coor2[1] - self.__coor3[1]) * \
           (self.__coor1[0] - self.__coor3[0]) + (self.__coor3[0] - self.__coor2[0]) * \
           (self.__coor1[1] - self.__coor3[1]))
        
        if d==0:
            return False

        u = ((self.__coor2[1] - self.__coor3[1]) * (check_x - self.__coor3[0]) + \
             (self.__coor3[0] - self.__coor2[0]) * (check_y - self.__coor3[1])) / d
        v = ((self.__coor3[1] - self.__coor1[1]) * (check_x - self.__coor3[0]) + \
             (self.__coor1[0] - self.__coor3[0]) * (check_y - self.__coor3[1])) / d
        w = 1 - u - v

        if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1:
            return True
        else:
            return False

    def perimeter_points(self, points=16):
        p_points = []
        p_points.append(self.__coor1)
        p_points.append(self.__coor2)
        p_points.append(self.__coor3)


        for i in range(1, 5):
            x = self.__coor1[0] + (i / 5) * (self.__coor2[0] - self.__coor1[0])
            y = self.__coor1[1] + (i / 5) * (self.__coor2[1] - self.__coor1[1])
            p_points.append((x, y))
        for i in range(1, 5):
            x = self.__coor2[0] + (i / 5) * (self.__coor3[0] - self.__coor2[0])
            y = self.__coor2[1] + (i / 5) * (self.__coor3[1] - self.__coor2[1])
            p_points.append((x, y))
        for i in range(1, 6):
            x = self.__coor3[0] + (i / 6) * (self.__coor1[0] - self.__coor3[0])
            y = self.__coor3[1] + (i / 6) * (self.__coor1[1] - self.__coor3[1])
            p_points.append((x, y))

        return p_points

    def paint(self, canvas):
        points = self.perimeter_points()
        for x, y in points:
            canvas.set_pixel(int(x), int(y))

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))