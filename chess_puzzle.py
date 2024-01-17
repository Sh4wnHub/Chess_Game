import os
import filecmp
import copy
import random
from typing import Any

def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    return (ord(loc[0])-96,int(loc[1:])) #should ignore whitespace at end
	
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    return chr(x + 96) + str(y)

class Piece:
    _cur_X : int	
    _cur_Y : int
    _side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side : bool):
        '''sets initial values'''
        self._cur_X = pos_X
        self._cur_Y = pos_Y
        self._side = side
        self.class_name = self.__class__.__name__
        self.message = ""

    def list_squares(self, pos_X : int, pos_Y : int, B: tuple[int, list[Any]]) -> list[tuple[int,int]]:
        pass

    def can_reach(self, pos_X : int, pos_Y : int, B: tuple[int, list[Any]]) -> bool:
        pass

    def can_move_to(self, pos_X : int, pos_Y : int, B: tuple[int, list[Any]]) -> bool:
        pass

    def move_to(self, pos_X : int, pos_Y : int, B: tuple[int, list[Any]]) -> tuple[int, list[Any]]:
        pass

Board = tuple[int, list[Piece]]

def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pos_X, pos_Y of board B'''
    for piece in B[1]:
        if piece._cur_X == pos_X and piece._cur_Y == pos_Y:
            return True
    return False
	
def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pos_X, pos_Y of board B 
    assumes some piece at coordinates pos_X, pos_Y of board B is present
    '''
    for piece in B[1]:
        if piece._cur_X == pos_X and piece._cur_Y == pos_Y:
            break
    return piece

class Rook(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side)
        
    def __str__(self):
        if self._side: return "\u2656"
        else: return "\u265C"
    
    def list_squares(self, pos_X : int, pos_Y : int, B: Board) -> list[tuple[int,int]]:
        '''
        creates list of squares in between current position and new position
        and makes sure that all squares are empty'''
        square_list = []
        if self._cur_X == pos_X:
            square_list = [(self._cur_X, i) for i in range(min(self._cur_Y, pos_Y) + 1,  max(self._cur_Y, pos_Y))]
        elif self._cur_Y == pos_Y:
            square_list = [(i, self._cur_Y) for i in range(min(self._cur_X, pos_X) + 1,  max(self._cur_X, pos_X))]
        return square_list
        
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule2] and [Rule4](see section Intro)
        '''
        #Within Board Check
        if (pos_X > B[0] or pos_X < 1) or (pos_Y > B[0] or pos_Y < 1):
            self.message = "\n\n" + "\033[93m" + "Coordinates provided are not within board" + "\033[0m" + "\n\n"
            return False
        elif pos_X == self._cur_X and pos_Y == self._cur_Y:
            self.message = "\n\n" + "\033[93m" + "Coordinates are the same as current position" + "\033[0m" + "\n\n"
            return False
        
        if self._cur_X == pos_X or self._cur_Y == pos_Y:#Rook move test
            squares_check = self.list_squares(pos_X, pos_Y, B)
            for square in squares_check:#Test nothing is blocking path
                if is_piece_at(square[0], square[1], B):
                    self.message = "\n\n" + "\033[93m" + "A piece is blocking this move" + "\033[0m" + "\n\n"
                    return False
        else:
            self.message = "\n\n" + "\033[93m" + "A Rook cannot make this move" + "\033[0m" + "\n\n"
            return False
        
        if is_piece_at(pos_X, pos_Y, B):
            if piece_at(pos_X, pos_Y, B)._side == self._side:
                self.message = "\n\n" + "\033[93m" + "There is already a piece from your side in this position" + "\033[0m" + "\n\n"
                return False
            
        self.message = f"\n\n\033[92mMoving {self.class_name} from {index2location(self._cur_X, self._cur_Y)} to {index2location(pos_X, pos_Y)}\033[0m\n\n"
        
        return True

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        '''
        valid = self.can_reach(pos_X, pos_Y, B)#checks if piece can reach square according to specific rules for that class
        if valid:
            B1 = copy.deepcopy(B)#take copy of board and pieces so for checking rules are applicable to move
            if is_piece_at(pos_X, pos_Y, B1):#check if there's a piece at position being moved to
                remove = piece_at(pos_X, pos_Y, B1)
                for i in range(len(B1[1])):#remove the piece at the position being moved to
                    if B1[1][i] == remove:
                        B1[1].pop(i)
                        break
                self.message = f"\n\n\033[92mRemoved opposition {remove.class_name} and moved {self.class_name} from {index2location(self._cur_X, self._cur_Y)} to {index2location(pos_X, pos_Y)}\033[0m\n\n"
            for piece in B1[1]:#update position of piece to on test board
                if piece._cur_X == self._cur_X and piece._cur_Y == self._cur_Y:
                    piece._cur_X = pos_X
                    piece._cur_Y = pos_Y
            
            if is_check(self._side, B1):#check that board isn't in check after move
                self.message = f"\n\n\033[93mCannot complete move as it leaves your side in check\033[0m\n\n"
                valid = False

            return valid
        else:
            return valid
        
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        if is_piece_at(pos_X, pos_Y, B):
            for i in range(len(B[1])):
                if B[1][i]._cur_X == pos_X and B[1][i]._cur_Y == pos_Y:
                    B[1].pop(i)
                    break
        self._cur_X = pos_X
        self._cur_Y = pos_Y
        
        return B

class Bishop(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side)
    
    def __str__(self):
        if self._side: return "\u2657"
        else: return "\u265D"
        
    def list_squares(self, pos_X : int, pos_Y : int, B: Board) -> list[tuple[int,int]]:
        '''
        creates list of squares in between current position and new position
        and makes sure that all squares are empty'''
        col_list = []
        row_list = []
        if self._cur_X < pos_X:
            col_list = [i for i in range(min(self._cur_X, pos_X) + 1,  max(self._cur_X, pos_X))]
        elif self._cur_X > pos_X:
            col_list = [i for i in range(max(self._cur_X, pos_X) - 1,  min(self._cur_X, pos_X), -1)]
        if self._cur_Y < pos_Y:
            row_list = [i for i in range(min(self._cur_Y, pos_Y) + 1,  max(self._cur_Y, pos_Y))]
        elif self._cur_Y > pos_Y:
            row_list = [i for i in range(max(self._cur_Y, pos_Y) - 1,  min(self._cur_Y, pos_Y), -1)]
        return list(zip(col_list, row_list))
        
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule2] and [Rule4](see section Intro)
        Hint: use is_piece_at
        '''
        #Within Board Check
        if (pos_X > B[0] or pos_X < 1) or (pos_Y > B[0] or pos_Y < 1):
            self.message = "\n\n" + "\033[93m" + "Coordinates provided are not within board" + "\033[0m" + "\n\n"
            return False
        elif pos_X == self._cur_X and pos_Y == self._cur_Y:
            self.message = "\n\n" + "\033[93m" + "Coordinates are the same as current position" + "\033[0m" + "\n\n"
            return False
        
        if abs(self._cur_X - pos_X) == abs(self._cur_Y - pos_Y):#Bishop move test
            squares_check = self.list_squares(pos_X, pos_Y, B)
            for square in squares_check:#Test nothing is blocking path
                if is_piece_at(square[0], square[1], B):
                    self.message = "\n\n" + "\033[93m" + "A piece is blocking this move" + "\033[0m" + "\n\n"
                    return False
        else:
            self.message = "\n\n" + "\033[93m" + "A Bishop cannot make this move" + "\033[0m" + "\n\n"
            return False
        
        if is_piece_at(pos_X, pos_Y, B):
            if piece_at(pos_X, pos_Y, B)._side == self._side:
                self.message = "\n\n" + "\033[93m" + "There is already a piece from your side in this position" + "\033[0m" + "\n\n"
                return False
            
        self.message = f"\n\n\033[92mMoving {self.class_name} from {index2location(self._cur_X, self._cur_Y)} to {index2location(pos_X, pos_Y)}\033[0m\n\n"

        return True

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        '''
        valid = self.can_reach(pos_X, pos_Y, B)#checks if piece can reach square according to specific rules for that class
        if valid:
            B1 = copy.deepcopy(B)#take copy of board and pieces so for checking rules are applicable to move
            if is_piece_at(pos_X, pos_Y, B1):#check if there's a piece at position being moved to
                remove = piece_at(pos_X, pos_Y, B1)
                for i in range(len(B1[1])):#remove the piece at the position being moved to
                    if B1[1][i] == remove:
                        B1[1].pop(i)
                        break
                self.message = f"\n\n\033[92mRemoved opposition {remove.class_name} and moved {self.class_name} from {index2location(self._cur_X, self._cur_Y)} to {index2location(pos_X, pos_Y)}\033[0m\n\n"
            for piece in B1[1]:#update position of piece to on test board
                if piece._cur_X == self._cur_X and piece._cur_Y == self._cur_Y:
                    piece._cur_X = pos_X
                    piece._cur_Y = pos_Y
            
            if is_check(self._side, B1):#check that board isn't in check after move
                self.message = f"\n\n\033[93mCannot complete move as it leaves your side in check\033[0m\n\n"
                valid = False

            return valid
        else:
            return valid
        
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        if is_piece_at(pos_X, pos_Y, B):
            for i in range(len(B[1])):
                if B[1][i]._cur_X == pos_X and B[1][i]._cur_Y == pos_Y:
                    B[1].pop(i)
                    break
        self._cur_X = pos_X
        self._cur_Y = pos_Y
        
        return B    

class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side)
        
    def __str__(self):
        if self._side: return "\u2654"
        else: return "\u265A"
        
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule3] and [Rule4]'''
        #Within Board Check
        if (pos_X > B[0] or pos_X < 1) or (pos_Y > B[0] or pos_Y < 1):
            self.message = "\n\n" + "\033[93m" + "Coordinates provided are not within board" + "\033[0m" + "\n\n"
            return False
        elif pos_X == self._cur_X and pos_Y == self._cur_Y:
            self.message = "\n\n" + "\033[93m" + "Coordinates are the same as current position" + "\033[0m" + "\n\n"
            return False
        
        #King move test
        if abs(self._cur_X - pos_X) <= 1 and abs(self._cur_Y - pos_Y) <= 1:
            pass
        else:
            self.message = "\n\n" + "\033[93m" + "A King cannot make this move" + "\033[0m" + "\n\n"
            return False
        
        #No piece from own side test
        if is_piece_at(pos_X, pos_Y, B):
            if piece_at(pos_X, pos_Y, B)._side == self._side:
                self.message = "\n\n" + "\033[93m" + "There is already a piece from your side in this position" + "\033[0m" + "\n\n"
                return False
            
        self.message = f"\n\n\033[92mMoving {self.class_name} from {index2location(self._cur_X, self._cur_Y)} to {index2location(pos_X, pos_Y)}\033[0m\n\n"
        
        return True

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        '''
        valid = self.can_reach(pos_X, pos_Y, B)#checks if piece can reach square according to specific rules for that class
        if valid:
            B1 = copy.deepcopy(B)#take copy of board and pieces so for checking rules are applicable to move
            if is_piece_at(pos_X, pos_Y, B1):#check if there's a piece at position being moved to
                remove = piece_at(pos_X, pos_Y, B1)
                for i in range(len(B1[1])):#remove the piece at the position being moved to
                    if B1[1][i] == remove:
                        B1[1].pop(i)
                        break
                self.message = f"\n\n\033[92mRemoved opposition {remove.class_name} and moved {self.class_name} from {index2location(self._cur_X, self._cur_Y)} to {index2location(pos_X, pos_Y)}\033[0m\n\n"
            for piece in B1[1]:#update position of piece to on test board
                if piece._cur_X == self._cur_X and piece._cur_Y == self._cur_Y:
                    piece._cur_X = pos_X
                    piece._cur_Y = pos_Y
            
            if is_check(self._side, B1):#check that board isn't in check after move
                self.message = f"\n\n\033[93mCannot complete move as it leaves your side in check\033[0m\n\n"
                valid = False

            return valid
        else:
            return valid
        
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        if is_piece_at(pos_X, pos_Y, B):
            for i in range(len(B[1])):
                if B[1][i]._cur_X == pos_X and B[1][i]._cur_Y == pos_Y:
                    B[1].pop(i)
                    break
        self._cur_X = pos_X
        self._cur_Y = pos_Y
        
        return B     

def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    '''
    for piece in B[1]:#get king piece for side
        if piece._side == side and piece.class_name == "King":
            king = piece

    for piece in B[1]:#check if any piece can reach king piece
        if piece._side != side and piece.can_reach(king._cur_X, king._cur_Y, B):
            return True
    return False

def only_king(side: bool, B: Board) -> bool:
    #checks if there's a single king left on the side to see if piece could be in checkmate without being in check
    count = 0
    for piece in B[1]:
        if piece._side == side:
            count += 1
    if count > 1:
        return False
    else:
        return True

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side
    '''
    if not is_check(side, B) and not only_king(side, B):
        return False
    
    for piece in B[1]:
        if piece._side == side and piece.class_name == "King":
            king = piece

    #King Move Test
    for i in range(-1,2):
        for j in range(-1,2):
            if king.can_move_to(king._cur_X+i, king._cur_Y+j, B):
                return False
    
    #Block Test
    for piece in B[1]:
        if piece._side != side and piece.can_reach(king._cur_X, king._cur_Y, B):#checks which pieces can take king
            block_check = piece.list_squares(king._cur_X, king._cur_Y, B) + [(piece._cur_X, piece._cur_Y)]
            for square in block_check:#gets list of the squares moved over to take king
                for block in B[1]:
                    if block._side == side and block != king and block.can_move_to(square[0], square[1], B):#checks if any piece can block the check and not leave board still in check
                        return False
                
    return True

def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    f = open(filename, "r")
    size = int(f.readline())
    if size > 26:#check board is smaller than 26
        print("Board size is too large")
        raise IOError("Board size is too large")
    B0: Board
    B0 = (size, []) #create board with size and empty list
    colour = ["White", "Black"]
    c_bool = [True, False]
    c = 0
    for line in f:
        b = 0
        r = 0
        k = 0
        for piece in line.split(", "):
            piece = piece.strip()
            x, y = location2index(piece[1:])
            if is_piece_at(x, y, B0):#check no pieces already exist at same position
                print("Pieces overlap")
                raise IOError("Pieces overlap")
            if x > size or y > size:#check all pieces are within the board size
                print("Not all pieces are within board")
                raise IOError("Not all pieces are within board")
            if piece[0] == "B":
                B0[1].append(Bishop(x, y, c_bool[c]))
                b+=1
            elif piece[0] == "R":
                B0[1].append(Rook(x, y, c_bool[c]))
                r+=1
            elif piece[0] == "K":
                B0[1].append(King(x, y, c_bool[c]))
                k+=1
        if k != 1:#check there's at least one King and no more
            print(f"{colour[c]} doesn't have the correct number of kings")
            raise IOError(f"{colour[c]} doesn't have the correct number of kings")
        c+=1
    f.close
    if is_checkmate(False, B0):#check inital board isn't in checkmate
        print("Board is already in checkmate")
        raise IOError("Board is already in checkmate")
    return B0    

def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    f = open(filename, "w")
    f.write(f"{str(B[0])}\n")
    for i in range(1,-1,-1):
        file_string = ""
        for piece in B[1]:
            if piece._side == i:
                file_string += f"{piece.class_name[0]}{index2location(piece._cur_X, piece._cur_Y)}, "
        f.write(f"{file_string[:-2]}\n")

def compare_files(file1: str, file2: str) -> bool:
    return filecmp.cmp(file1, file2)

def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''
    moved = False
    while not moved:
        selected = B[1][random.randint(0,len(B[1])-1)]
        if selected._side == False:
            pos_X = random.randint(1,B[0])
            pos_Y = random.randint(1,B[0])
            if selected.can_move_to(pos_X, pos_Y, B):
                moved = True
    return selected, pos_X, pos_Y

def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
    string_board = ""
    for j in range(B[0],0,-1):
        for i in range(1,B[0]+1):
            p = False
            for piece in B[1]:
                if piece._cur_X == i and piece._cur_Y == j:
                    string_board += str(piece)
                    p = True
            if not p: string_board += "\u2001"                
        if j > 1:
            string_board += "\n"
    return string_board

def human_move(B: Board, side_name: str, side_dict: dict[str, bool]) -> Board:
    #function to ask human what move they want to perform and to return the new board
    next_move = input(f"Next move of {side_name}: ")
    
    moved = False
    while not moved:
        if next_move == "QUIT":#check if player wants to quit at any point and save the config
            filename = input("File name to store the configuration: ")
            save_board(filename, B)
            quit()
        else:
            for l in range(1,len(next_move)):
                if next_move[l].isalpha():#check for split
                    cur_x, cur_y = location2index(next_move[:l])#get current coordinates
                    pos_X, pos_Y = location2index(next_move[l:])#get coordinates of new location
                    
                    if is_piece_at(cur_x, cur_y, B):#check piece exists
                        selected = piece_at(cur_x, cur_y, B)
                        
                        if selected._side == side_dict[side_name]:#check selected piece is on correct side
                            
                            if selected.can_move_to(pos_X, pos_Y, B):#check selected piece can make the move
                                print(selected.message)
                                B1 = selected.move_to(pos_X, pos_Y, B)
                                moved = True
                                
                            else:
                                print(selected.message)
                                next_move = input(f"This is not a valid move. Next move of {side_name}: ")
                                
                        elif selected._side != side_dict[side_name]:
                            print(f"\n\n\033[93mThat {selected.class_name} is not yours!\033[0m\n\n")
                            next_move = input(f"This is not a valid move. Next move of {side_name}: ")
                            
                    elif not is_piece_at(cur_x, cur_y, B):
                        print("\n\n" + "\033[93m" + "No piece at that location..."  + "\033[0m" + "\n\n")
                        next_move = input(f"This is not a valid move. Next move of {side_name}: ")
    
    return (B)

def input_file() -> Board:
    input_file = False
    filename = ""
    while not input_file:
        try:
            if filename == "":
                filename = input("File name for initial configuration: ")
                if filename == "QUIT":
                    quit()
                else:
                    B1 = read_board(filename)
                    input_file = True
                    print("The initial configuration is: ")
                    print(conf2unicode(B1))
            else:
                B1 = read_board(filename)
                input_file = True
                print("The initial configuration is: ")
                print(conf2unicode(B1))
        except KeyboardInterrupt:
            break
        except IOError:#IOError raised in read board and caught here
            filename = input("This is not a valid file. File name for initial configuration: ")
            if filename == "QUIT":
                quit()
                
    return B1

def main() -> None:
    '''
    runs the play
    ...
    '''
    
    playing = True
    side_dict = {"White": True, "Black": False}
    two_player = False
    
    B1 = input_file()
    
    while playing:
        for move in range(len(side_dict)):#keep calling both moves while playing is still true
            cur_side = list(side_dict)[move]
            if not playing:
                break
            if move == 0:#call white move
                B1 = human_move(B1, cur_side, side_dict)
            elif move == 1:#call black move
                if two_player:#two player mode for testing
                    B1 = human_move(B1, cur_side, side_dict)
                else:
                    selected, pos_X, pos_Y = find_black_move(B1)
                    print(f"Next move of Black is {index2location(selected._cur_X, selected._cur_Y)}{index2location(pos_X, pos_Y)}.", end=" ")
                    B1 = selected.move_to(pos_X, pos_Y, B1)
                    
            print(f"The configuration after {cur_side}'s move is:")
            print(conf2unicode(B1))
            if is_checkmate(not side_dict[cur_side], B1):#check is new configuation is checkmate for opposition and end the game
                print(f"Game over. {cur_side} wins.")
                playing = False               
                    
if __name__ == '__main__': #keep this in
   main()
