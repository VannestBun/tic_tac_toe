from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Tic Tac Toe")
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height )
        self.__canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)
    
    def draw_circle(self, oval):
        oval.draw(self.__canvas)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False

    def bind_click(self, function):
        # Bind mouse click event to the function
        self.__canvas.bind("<Button-1>", function)

    def get_mouse_click(self, event):
        # Return the coordinates of the mouse click
        return Point(event.x, event.y)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )

class Oval:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def draw(self, canvas):
        padding = 10

        canvas.create_oval(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill="", outline="green", width=2
        )
        