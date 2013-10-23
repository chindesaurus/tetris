'''
tetris.py

Usage: python tetris.py

@author chindesaurus
'''

from graphics import *
import random


############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int

        Specifies the position on the tetris board
        in terms of the square grid.
    '''

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)


    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            Checks if the block can move dx squares in the x direction
            and dy squares in the y direction.
            Returns True if it can, and False otherwise.
        '''
        return board.can_move(self.x + dx, self.y + dy)
   
     
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            Moves the block dx squares in the x direction
            and dy squares in the y direction.
        '''
        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)


############################################################
# SHAPE CLASS
############################################################

class Shape():
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = -1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False
        
        for pos in coords:
            self.blocks.append(Block(pos, color))


    def get_blocks(self):
        ''' Returns the list of blocks.
        '''
        return self.blocks


    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block.
        ''' 
        for block in self.blocks:
            block.draw(win)


    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks.
        '''
        for block in self.blocks:
            block.move(dx, dy)


    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            Checks if the shape can move dx squares in the x direction
            and dy squares in the y direction, i.e.
            check if each of the blocks can move.
            Returns True if all of them can, and False otherwise.
        '''
        for block in self.blocks:
            if not(block.can_move(board, dx, dy)):
                return False 
        return True

 
    def get_rotation_dir(self):
        ''' Return value: type: int
        
            Returns the current rotation direction.
            1 indicates clockwise, -1 indicates counterclockwise
        '''
        return self.rotation_dir


    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated.
            
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False
                        
            Otherwise all is good, return True.
        '''
        # the rotation direction
        rot_dir = self.get_rotation_dir() 

        # the center of the shape 
        center = self.blocks[1];

        # don't allow any of the blocks in the shape move
        # beyond the board boundaries or into an occupied square
        for block in self.blocks:
            x = center.x - rot_dir * center.y + rot_dir * block.y
            y = center.y + rot_dir * center.x - rot_dir * block.x
            if not(board.can_move(x, y)):
                return False

        return True


    def rotate(self, board):
        ''' Parameters: board - type: Board object

            Rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position
        '''    
        # the rotation direction
        rot_dir = self.get_rotation_dir()
    
        # the center of the shape 
        center = self.blocks[1];

        if self.can_rotate(board):

            for block in self.blocks:
                x = center.x - rot_dir * center.y + rot_dir * block.y
                y = center.y + rot_dir * center.x - rot_dir * block.x
                if board.can_move(x, y):
                    block.move(x - block.x, y - block.y)

        ### Default behavior is that a piece will only shift
        ### rotation direction after a successful rotation. This ensures that 
        ### pieces which switch rotations definitely remain within their 
        ### accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1

        

############################################################
# ALL SHAPE CLASSES
############################################################

 
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]

class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')        
        self.center_block = self.blocks[1]

class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')        
        self.center_block = self.blocks[1]


class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x   , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')
        self.center_block = self.blocks[0]

    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return 

class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1


class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'yellow')
        self.center_block = self.blocks[1]


class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'magenta')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True
        self.rotation_dir = -1      



############################################################
# BOARD CLASS
############################################################

class Board():
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}


    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            Draws the shape on the board if there is space for it
            and returns True, else returns False.
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        return False


    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. Check if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False.

            2. If there is already a block at that postion, can't move there
            return False.

            3. Otherwise return True.
            
        '''
        # boolean - is position x,y within the board boundaries?
        withinBoard = (x in range(Tetris.BOARD_WIDTH) and y in range(Tetris.BOARD_HEIGHT))

        # boolean - is there a block at position x,y?
        occupied = ((x, y) in self.grid)

        return (withinBoard and not occupied)


    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            Add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key.
        '''
        # the list of blocks
        listBlocks = shape.get_blocks()

        # add to dictionary: (x,y) coordinates as key, block as value
        for block in listBlocks:
            self.grid.update({(block.x, block.y):block})


    def delete_row(self, y):
        ''' Parameters: y - type:int

            Remove all the blocks in row y.
        '''
        # remove all blocks in row y from the grid
        # and undraw them
        for x in range(Tetris.BOARD_WIDTH):
            self.grid[x, y].undraw()
            del self.grid[x, y]
        
 
    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            For each block in row y
            check if there is a block in the grid (use the in operator).
            If there is one square that is not occupied, return False
            otherwise return True.
        '''
        # for each block in row y
        for x in range(Tetris.BOARD_WIDTH):

            # if there is not a block in the row
            if not((x, y) in self.grid):
                return False
        return True
   
 
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            Moves all rows above y_start (inclusive) down one square.

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position
        '''
        for y in range(y_start, -1, -1):
            for x in range(Tetris.BOARD_WIDTH):
                if (x, y) in self.grid:

                    block = self.grid[(x, y)]
 
                    # remove it from the grid
                    del self.grid[(x, y)]

                    # move the block object down on the screen
                    block.move(0, 1)
    
                    # place block back in the grid in the new position
                    self.grid[(x, y + 1)] = block
                   
 
    def remove_complete_rows(self):
        ''' Removes all the complete rows
            1. for each row, y, 
            2. check if the row is complete
                if it is,
                    delete the row
                    move all rows down starting at row y - 1
        '''
        # for each row y
        for y in range(Tetris.BOARD_HEIGHT):
            
            # if the row is complete 
            if self.is_row_complete(y):
               
                # delete the row 
                self.delete_row(y)

                # move all rows down starting at row y - 1
                self.move_down_rows(y - 1)


    def game_over(self):
        ''' Display "Game Over !!!" message in the center of the board
        '''
        message = Text(Point(150, 150), "Game Over !!!\n Thanks for playing.")
        message.setSize(32)
        message.draw(self.canvas)


############################################################
# TETRIS CLASS
############################################################

class Tetris():
    ''' Tetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shape - type: Shape - the current moving shape on the board
    '''
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
   
 
    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        self.delay = 1000 # milliseconds

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # draw the current_shape on the board
        Board.draw_shape(self.board, self.current_shape)

        # For Step 9:  animate the shape!
        self.animate_shape()


    def create_new_shape(self):
        ''' Return value: type: Shape
            
            Creates a random new shape that is centered
            at y = 0 and x = int(self.BOARD_WIDTH/2).
            Returns the shape.
        '''

        # generate a pseudorandom integer in this range (inclusive)
        index = random.randint(0, len(Tetris.SHAPES) - 1)

        # select a shape
        shape = Tetris.SHAPES[index]

        # center the shape at this point
        point = Point(int(self.BOARD_WIDTH / 2), 0)

        if shape == I_shape:
            ref = I_shape(point)
        elif shape == J_shape:
            ref = J_shape(point)
        elif shape == L_shape:
            ref = L_shape(point)
        elif shape == O_shape:
            ref = O_shape(point)
        elif shape == S_shape:
            ref = S_shape(point)
        elif shape == T_shape:
            ref = T_shape(point)
        else:
            ref = Z_shape(point)

        # return a reference to the new Shape object
        return ref
     
    
    def animate_shape(self):
        ''' Animate the shape - move down at equal intervals
            specified by the delay attribute.
        '''
        self.do_move('Down')
        self.win.after(self.delay, self.animate_shape)
   
 
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any 
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            Return False
        '''
        # get the x and y displacements from DIRECTION attribute
        displacement = self.DIRECTION.get(direction)
        x = displacement[0]
        y = displacement[1]

        # move the shape (if possible)
        if self.current_shape.can_move(self.board, x, y):
            self.current_shape.move(x, y)

            return True

        # else the piece has hit the bottom
        else:
            # if the last failed move was Down
            if direction == 'Down':

                # add the current shape to the board
                self.board.add_shape(self.current_shape)

                # remove completed rows (if any)
                self.board.remove_complete_rows()

                # update Tetris.current_shape with a new random shape
                self.current_shape = self.create_new_shape()

                # draw the new shape on the board
                # if not possible, then the game is over
                if not self.board.draw_shape(self.current_shape):
                    self.board.game_over()
                return False
            

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can.
        '''
        self.current_shape.rotate(self.board)
   
 
    def key_pressed(self, event):
        ''' This function is called when a key is pressed on the keyboard.

            If the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction.

            If the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board.

            If the user presses the 'Up' arrow key,
            the shape rotates.
        '''
        key = event.keysym
        #print key   # for debugging

        # move left, right, and down
        if key in self.DIRECTION: 
            self.do_move(key)

        # drop piece
        elif key == "space":
            while (self.current_shape.can_move(self.board, 0, 1)):
                self.current_shape.move(0, 1)

        # rotate 
        elif key == "Up":
            self.do_rotate()

       
################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()
