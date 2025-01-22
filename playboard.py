from cell import Cell
from graphics import Point, Line
import time
import random

class PlayBoard:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._current_player = "X"

        self._create_cells()

    def _create_cells(self):
        # Create cells row by row instead of column by column
        for i in range(self._num_rows):
            row_cells = []
            for j in range(self._num_cols):
                row_cells.append(Cell(self._win, self))
            self._cells.append(row_cells)
        
        # Draw cells using the same row-major order
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cell(i, j)

        # whole window is clickable
        self._win.bind_click(self.handle_click)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def handle_click(self, event):
        # Convert the click event to a Point
        click_point = Point(event.x, event.y)
        
        # Check each cell to see if it was clicked
        for cells in self._cells:
            for cell in cells:
                cell.check_click(click_point)
    
    def check_win(self):

        # check vertical
        for row in range(self._num_rows):
            is_win = True
            for col in range(self._num_cols):
                # print(f"Checking row {row}, col {col}: {self._cells[row][col]._symbol}")  # Debugging
                if self._cells[row][col]._symbol != self._current_player:
                    is_win = False
                    break
            if is_win:
                return True
    
        # check horizontal
        for col in range(self._num_cols):
            is_win = True
            for row in range(self._num_rows):
                if self._cells[row][col]._symbol != self._current_player:
                    is_win = False
                    break
            if is_win:
                # mid_point = self._cells[row][0].x1 + 
                # start = self._cells[row][0].x1
                return True

        # check main diagonal
        # remember cols is individual, row is the list
        if self._num_rows == self._num_cols:
            is_win = True
            for i in range(self._num_rows):
                if self._cells[i][i]._symbol != self._current_player:
                    is_win = False
                    break
            if is_win:
                start = Point(self._cells[0][0]._x1, self._cells[0][0]._y1)
                end = Point(self._cells[self._num_rows - 1][self._num_cols - 1]._x2, self._cells[self._num_rows - 1][self._num_cols - 1]._y2)
                self._win.draw_line(Line(start, end))
                return True
                
        # check inverse diagonal
        if self._num_rows == self._num_cols:
            is_win = True
            for i in range(self._num_rows):
                if self._cells[i][self._num_cols - 1 - i]._symbol != self._current_player:
                    is_win = False
                    break
            if is_win:
                start = Point(self._cells[0][self._num_cols - 1]._x1, self._cells[0][self._num_cols - 1]._y2)
                end = Point(self._cells[self._num_rows - 1][0]._x2, self._cells[self._num_rows - 1][0]._y1)
                self._win.draw_line(Line(start, end))
                return True       
        return False
    

    #random first
    def cpu_opps(self):
        if self._current_player == "O":
            # check which is not empty
            # make a list of tuple, x,y
            # randomly pick an index number in that list
            possible_moves = []
            for row in range(self._num_rows):
                for col in range(self._num_cols):
                    if self._cells[row][col]._symbol is None:
                        possible_moves.append((row, col))
            print(possible_moves, "possible moves")
            random_move = random.choice(possible_moves)
            row, col = random_move
            print(random_move, "chosen move")

            self._cells[row][col]._symbol = "O"
            
            self._cells[row][col].draw_O()

            is_win = self.check_win()
            print(is_win, "is_win")
            if is_win:
                print(f"{self._current_player} has won!")
                return
            
            # check draw
            is_draw = self.check_draw()
            if is_draw:
                print("its draw!")
                return

            self._current_player = "X"

    def cpu_smart_opps(self):
        # if cell symbol is O, then go on
        if self._current_player == "O":
            pass


        # check the whole board if x is occupying two spaces
        # block the winning move


        #     so like we count the cols first, 
        #     if x appear same row diff cal 1 less of the num_colls, means
        #     they are about to win

        # check row for blocking move
        for row in range(self._num_rows):
            count_x_row = 0
            empty_cell = None
            for col in range(self._num_cols):
                if self._cells[row][col]._symbol == "X":
                    count_x_row += 1
                elif self._cells[row][col]._symbol is None:
                    empty_cell = (row, col)
            if count_x_row == self._num_rows - 1 and empty_cell != None:
                self._cells[empty_cell[0]][empty_cell[1]]._symbol = "O"
                self._cells[empty_cell[0]][empty_cell[1]].draw_O()
                self._current_player = "X"
                return
        
        # check cols for blocking move
        for col in range(self._num_rows):
            count_x_row = 0
            empty_cell = None
            for row in range(self._num_cols):
                if self._cells[row][col]._symbol == "X":
                    count_x_row += 1
                elif self._cells[row][col]._symbol is None:
                    empty_cell = (row, col)
            if count_x_row == self._num_rows - 1 and empty_cell != None:
                self._cells[empty_cell[0]][empty_cell[1]]._symbol = "O"
                self._cells[empty_cell[0]][empty_cell[1]].draw_O()
                self._current_player = "X"
                return
                        
            # check which is empty then block it
        
        # if not then pick the middle
        # assume its 3x3 then middle is easy to find
        # 4x4 or 5x5 we need something dynamic
        #check diagonal
        count_x = 0
        empty_cell = None
        for i in range(self._num_rows):
            if self._cells[i][i]._symbol == "X":
                count_x += 1
            elif self._cells[i][i]._symbol is None:
                empty_cell = (i, i)
        
        if count_x == self._num_rows - 1 and empty_cell:
            self._cells[empty_cell[0]][empty_cell[1]]._symbol = "O"
            self._cells[empty_cell[0]][empty_cell[1]].draw_O()
            self._current_player = "X"
            return
        
        #check inverse diagonal
        count_x = 0
        empty_cell = None
        for i in range(self._num_rows):
            row = i
            col = self._num_cols - 1 - i
            if self._cells[row][col]._symbol == "X":
                count_x += 1
            elif self._cells[row][col]._symbol is None:
                empty_cell = (row, col)
        
        if count_x == self._num_rows - 1 and empty_cell:
            self._cells[empty_cell[0]][empty_cell[1]]._symbol = "O"
            self._cells[empty_cell[0]][empty_cell[1]].draw_O()
            self._current_player = "X"
            return

        # Find Middle
        if self._num_rows % 2 == 1 and self._num_cols % 2 == 1:
            # Odd-sized grid: one single center
            center = (self._num_rows // 2, self._num_cols // 2)
            if self._cells[center[0]][center[1]]._symbol is None:
                self._cells[center[0]][center[1]]._symbol = "O"
                self._cells[center[0]][center[1]].draw_O()
                self._current_player = "X"
                return
        else:
            # Even-sized grid: four center cells
            center_cells = [
                (self._num_rows // 2 - 1, self._num_cols // 2 - 1),
                (self._num_rows // 2 - 1, self._num_cols // 2),
                (self._num_rows // 2, self._num_cols // 2 - 1),
                (self._num_rows // 2, self._num_cols // 2)
            ]
            for center in center_cells:
                if self._cells[center[0]][center[1]]._symbol is None:
                    self._cells[center[0]][center[1]]._symbol = "O"
                    self._cells[center[0]][center[1]].draw_O()
                    self._current_player = "X"
                    return
                
        # Take a corner if available
        corners = [(0, 0), (0, self._num_cols - 1), (self._num_rows - 1, 0), (self._num_rows - 1, self._num_cols - 1)]
        for corner in corners:
            if self._cells[corner[0]][corner[1]]._symbol is None:
                self._cells[corner[0]][corner[1]]._symbol = "O"
                self._cells[corner[0]][corner[1]].draw_O()
                self._current_player = "X"
                return

        # Random move if no other options
        possible_moves = [(row, col) for row in range(self._num_rows) for col in range(self._num_cols) if self._cells[row][col]._symbol is None]
        if possible_moves:
            random_move = random.choice(possible_moves)
            self._cells[random_move[0]][random_move[1]]._symbol = "O"
            self._cells[random_move[0]][random_move[1]].draw_O()
            self._current_player = "X"
    
    def check_draw(self):
        # this will be called when the board is full and no winners
        for cells in self._cells:
            for cell in cells:
                if cell._symbol is None:
                    return False
        return True

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.005)
