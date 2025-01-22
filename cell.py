from graphics import Line, Point, Oval
import time

class Cell:
    def __init__(self, window, playboard):
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._window = window
        self._playboard = playboard
        self._symbol = None
    
    def draw(self, x1, y1, x2, y2):

        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
    

        top_line = Line(Point(x1, y1), Point(x2, y1))
        self._window.draw_line(top_line)

        left_line = Line(Point(x1, y1), Point(x1, y2))
        self._window.draw_line(left_line)

        right_line = Line(Point(x2, y1), Point(x2, y2))
        self._window.draw_line(right_line)

        bottom_line = Line(Point(x1, y2), Point(x2, y2))
        self._window.draw_line(bottom_line)
    
    def check_click(self, click_point):
        if self._x1 <= click_point.x <= self._x2 and self._y1 <= click_point.y <= self._y2:
            # print(f"Cell clicked at: ({click_point.x}, {click_point.y})")
            if self._symbol is None and self._playboard._current_player == "X":
                self._symbol = "X"
                self.draw_X()

                # check win condition
                is_win = self._playboard.check_win()
                print(is_win, "is_win")
                if is_win:
                    print(f"{self._playboard._current_player} has won!")
                    return
                # check draw
                is_draw = self._playboard.check_draw()
                if is_draw:
                    print("its draw!")
                    return

                self._playboard._current_player = "O"
                # # call cpu
                # self._playboard.cpu_opps()

                # call smart cpu
                self._playboard.cpu_smart_opps()

            if self._symbol is None and self._playboard._current_player == "O":
                self._symbol = "O"
                self.draw_O()

                # check win condition
                is_win = self._playboard.check_win()
                print(is_win, "is_win")
                if is_win:
                    print(f"{self._playboard._current_player} has won!")
                    return
                
                 # check draw
                is_draw = self._playboard.check_draw()
                if is_draw:
                    print("its draw!")
                    return

                self._playboard._current_player = "X"

    def draw_X(self):

        padding = 30

        diagonal_one = Line(Point(self._x1 + padding, self._y1 + padding), Point(self._x2 - padding, self._y2 - padding))
        self._window.draw_line(diagonal_one, "red")

        diagonal_two = Line(Point(self._x2 - padding, self._y1 + padding), Point(self._x1 + padding, self._y2 - padding))
        self._window.draw_line(diagonal_two, "red")

    def draw_O(self):
        padding = 30

        self._window.draw_circle(Oval(Point(self._x1 + padding, self._y1 + padding), Point(self._x2 - padding, self._y2 - padding)))

