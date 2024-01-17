import pytest
from chess_puzzle import *


def test_location2index1():
    assert location2index("e2") == (5,2)
    assert location2index("a1") == (1,1)
    assert location2index("z26") == (26,26)
    assert location2index("l20") == (12,20)
    assert location2index("s8") == (19,8)
    

def test_index2location1():
    assert index2location(5,2) == "e2"
    assert index2location(1,1) == "a1"
    assert index2location(26,26) == "z26"
    assert index2location(12,20) == "l20"
    assert index2location(19,8) == "s8"

wb1 = Bishop(1,1,True)
wr1 = Rook(1,2,True)
wb2 = Bishop(5,2, True)
bk = King(2,3, False)
br1 = Rook(4,3,False)
br2 = Rook(2,4,False)
br3 = Rook(5,4, False)
wr2 = Rook(1,5, True)
wk = King(3,5, True)

B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
'''
♖ ♔  
 ♜  ♜
 ♚ ♜ 
♖   ♗
♗    
'''

def test_only_king1():
    B = read_board("board_examp.txt")
    assert only_king(False, B) == False
    assert only_king(False, B1) == False

def test_only_king2():
    B = read_board("board_examp.txt")
    assert only_king(True, B) == False
    assert only_king(True, B1) == False 
    
def test_only_king3():
    B = read_board("board_examp_3.txt")
    assert only_king(True, B) == False
    assert only_king(False, B) == True
    
def test_only_king4():
    B = read_board("board_examp_4.txt")
    assert only_king(True, B) == True
    assert only_king(False, B) == True

def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False

def test_piece_at1():
    assert piece_at(4,3, B1) == br1
    assert piece_at(4,3, B1)._side == False
    assert piece_at(4,3, B1).class_name == "Rook"

def test_can_reach1():
    assert wr2.can_reach(4,5, B1) == False

def test_is_piece_at2():
    assert is_piece_at(5,2, B1) == True

def test_piece_at2():
    assert piece_at(2,3, B1) == bk
    assert piece_at(2,3, B1)._side == False
    assert piece_at(2,3, B1).class_name == "King"

def test_can_reach2():
    assert bk.can_reach(4,5, B1) == False
    
def test_is_piece_at3():
    assert is_piece_at(3,3, B1) == False

def test_piece_at3():
    assert piece_at(1,5, B1) == wr2
    assert piece_at(1,5, B1)._side == True
    assert piece_at(1,5, B1).class_name == "Rook"

def test_can_reach3():
    assert wr2.can_reach(1,1, B1) == False
    
def test_is_piece_at4():
    assert is_piece_at(5,2, B1) == True

def test_piece_at4():
    assert piece_at(5,2, B1) == wb2
    assert piece_at(5,2, B1)._side == True
    assert piece_at(5,2, B1).class_name == "Bishop"

def test_can_reach4():
    assert wb2.can_reach(5,3, B1) == False
    
def test_is_piece_at5():
    assert is_piece_at(1,1, B1) == True

def test_piece_at5():
    assert piece_at(1,1, B1) == wb1
    assert piece_at(1,1, B1)._side == True
    assert piece_at(1,1, B1).class_name == "Bishop"

def test_can_reach5():
    assert wb1.can_reach(5,5, B1) == True
    
def test_is_piece_at6():
    assert is_piece_at(3,5, B1) == True

def test_piece_at6():
    assert piece_at(3,5, B1) == wk
    assert piece_at(3,5, B1)._side == True
    assert piece_at(3,5, B1).class_name == "King"
    
def test_can_reach6():
    assert wk.can_reach(2,4, B1) == True
    assert wk.can_move_to(2,4, B1) == False
    
def test_can_reach7():
    assert wr2.can_reach(1,4, B1) == True

br2a = Rook(1,5,False)
wr2a = Rook(2,5,True)

def test_can_move_to1():
    B1 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2a, wk])
    assert wr2a.can_move_to(2,4, B1) == False

def test_is_check1():
    wr2b = Rook(2,4,True)
    B1 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2b, wk])
    assert is_check(True, B1) == True

def test_is_checkmate1():
    br2b = Rook(4,5,False)
    B1 = (5, [wb1, wr1, wb2, bk, br1, br2b, br3, wr2, wk])
    assert is_checkmate(True, B1) == True

def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece._cur_X == piece1._cur_X and piece._cur_Y == piece1._cur_Y and piece._side == piece1._side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece._cur_X == piece1._cur_X and piece._cur_Y == piece1._cur_Y and piece._side == piece1._side and type(piece) == type(piece1):
                found = True
        assert found

def test_conf2unicode1():
    assert conf2unicode(B1) == "♖ ♔  \n ♜  ♜\n ♚ ♜ \n♖   ♗\n♗    "
    
def test_conf2unicode2():
    B1 = read_board("board_examp_3.txt")
    conf2unicode(B1)
    assert conf2unicode(B1) == "  ♚   ♖\n ♖     \n       \n       \n       \n       \n♔      "

def test_conf2unicode3():
    B1 = read_board("board_examp_4.txt")
    conf2unicode(B1)
    assert conf2unicode(B1) == "                         ♚\n" + "                          \n" * 24 + "♔                         "

def test_conf2unicode4():
    B1 = read_board("board_examp_8.txt")
    conf2unicode(B1)
    assert conf2unicode(B1) == "♜ ♝ ♚♝ ♜\n" + "        \n" *6 + "♖ ♗ ♔♗ ♖"
    
def test_compare_files1():
    #single test to make sure save_board outputs files correctly
    B1 = read_board("board_examp.txt")
    save_board("board_examp_s.txt", B1)
    
    assert compare_files("board_examp.txt", "board_examp_s.txt")

#Rook tests
def test_move_to1():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(4,3, B1)
    assert selected_piece.class_name == "Rook"
    
    assert selected_piece.can_move_to(4,7, B1) == False
    B1 = selected_piece.move_to(4,7, B1)
    
def test_move_to2():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(4,3, B1)
    
    assert selected_piece.can_move_to(4,5, B1) == True
    B1 = selected_piece.move_to(4,5, B1)

def test_move_to3():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(4,3, B1)
    
    assert selected_piece.can_move_to(4,1, B1) == True
    B1 = selected_piece.move_to(4,1, B1)
    
def test_move_to4():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(4,3, B1)
    
    assert selected_piece.can_move_to(3,1, B1) == False
    B1 = selected_piece.move_to(3,1, B1)
    
def test_move_to5():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(4,3, B1)
    
    assert selected_piece.can_move_to(2,3, B1) == False
    B1 = selected_piece.move_to(2,3, B1)
    
def test_move_to6():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(5,4, B1)
    
    assert selected_piece.can_move_to(5,1, B1) == False
    B1 = selected_piece.move_to(5,1, B1)
    
def test_move_to7():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(5,4, B1)
    
    assert selected_piece.can_move_to(5,2, B1) == True
    B1 = selected_piece.move_to(5,2, B1)
 
#Bishop tests
def test_move_to8():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(5,2, B1)
    assert selected_piece.class_name == "Bishop"
    
    assert selected_piece.can_move_to(5,4, B1) == False
    B1 = selected_piece.move_to(5,4, B1)
    
def test_move_to9():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(5,2, B1)
    
    assert selected_piece.can_move_to(1,6, B1) == False
    B1 = selected_piece.move_to(1,6, B1)
    
def test_move_to10():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(5,2, B1)
    
    assert selected_piece.can_move_to(3,4, B1) == False
    B1 = selected_piece.move_to(3,4, B1)
    
def test_move_to11():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(5,2, B1)
    
    assert selected_piece.can_move_to(4,3, B1) == True
    B1 = selected_piece.move_to(4,3, B1)

#King tests
def test_move_to12():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(3,5, B1)
    
    assert selected_piece.can_move_to(2,5, B1) == False
    B1 = selected_piece.move_to(2,5, B1)
    
def test_move_to13():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(3,5, B1)
    
    assert selected_piece.can_move_to(1,5, B1) == False
    B1 = selected_piece.move_to(1,5, B1)
    
def test_move_to14():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(3,5, B1)
    
    assert selected_piece.can_move_to(4,5, B1) == False
    B1 = selected_piece.move_to(4,5, B1)
    
def test_move_to15():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(3,5, B1)
    
    assert selected_piece.can_move_to(1,4, B1) == False
    B1 = selected_piece.move_to(1,4, B1)
    
def test_move_to15():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(3,5, B1)
    
    assert selected_piece.can_move_to(2,3, B1) == False
    B1 = selected_piece.move_to(2,3, B1)
    
def test_move_to16():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(2,3, B1)
    
    assert selected_piece.can_move_to(2,4, B1) == False
    B1 = selected_piece.move_to(2,4, B1)
    
def test_move_to17():
    B1 = read_board("board_examp.txt")
    selected_piece = piece_at(1,1, B1)
    B1 = selected_piece.move_to(5,5, B1)
    selected_piece = piece_at(2,4, B1)
    B1 = selected_piece.move_to(4,4, B1)
    
    selected_piece = piece_at(2,3, B1)
    
    assert selected_piece.can_move_to(3,3, B1) == True
    B1 = selected_piece.move_to(3,3, B1)
    
def test_is_check2():
    assert is_check(True, B1) == False
    
def test_is_checkmate2():
    assert is_checkmate(True, B1) == False

def test_is_check3():
    B1[1].append(Rook(3,4,False))

    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 2 and B1[1][i]._cur_Y == 3:
            B1[1].pop(i)
            break
    B1[1].append(King(5,1,False))
    
    assert is_check(True, B1) == True

def test_is_checkmate3():
    B1[1].append(Rook(3,4,False))

    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 2 and B1[1][i]._cur_Y == 3:
            B1[1].pop(i)
            break
    B1[1].append(King(5,1,False))
    
    assert is_checkmate(True, B1) == True
    
def test_is_check4():
    B1 = read_board("board_examp.txt")
    B1[1].append(Rook(3,4,False))

    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 2 and B1[1][i]._cur_Y == 3:
            B1[1].pop(i)
            break
    B1[1].append(King(5,1,False))
    
    selected_piece = piece_at(2,4, B1)
    B1 = selected_piece.move_to(2,3, B1)
    selected_piece = piece_at(3,4, B1)
    B1 = selected_piece.move_to(3,3, B1)
    selected_piece = piece_at(5,4, B1)
    B1 = selected_piece.move_to(5,3, B1)
    
    assert is_check(True, B1) == True

def test_is_checkmate4():
    B1 = read_board("board_examp.txt")
    B1[1].append(Rook(3,4,False))

    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 2 and B1[1][i]._cur_Y == 3:
            B1[1].pop(i)
            break
    B1[1].append(King(5,1,False))
    
    selected_piece = piece_at(2,4, B1)
    B1 = selected_piece.move_to(2,3, B1)
    selected_piece = piece_at(3,4, B1)
    B1 = selected_piece.move_to(3,3, B1)
    selected_piece = piece_at(5,4, B1)
    B1 = selected_piece.move_to(5,3, B1)
    
    assert is_checkmate(True, B1) == False #Bishop can remove Rook that is currently able to take King
    
def test_is_check5():
    B1 = read_board("board_examp.txt")
    B1[1].append(Rook(3,4,False))

    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 2 and B1[1][i]._cur_Y == 3:
            B1[1].pop(i)
            break
    B1[1].append(King(5,1,False))
    
    selected_piece = piece_at(2,4, B1)
    B1 = selected_piece.move_to(2,3, B1)
    selected_piece = piece_at(3,4, B1)
    B1 = selected_piece.move_to(3,3, B1)
    selected_piece = piece_at(5,4, B1)
    B1 = selected_piece.move_to(5,3, B1)
    
    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 1 and B1[1][i]._cur_Y == 1:
            B1[1].pop(i)
            break
    
    assert is_check(True, B1) == True

def test_is_checkmate5():
    B1 = read_board("board_examp.txt")
    B1[1].append(Rook(3,4,False))

    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 2 and B1[1][i]._cur_Y == 3:
            B1[1].pop(i)
            break
    B1[1].append(King(5,1,False))
    
    selected_piece = piece_at(2,4, B1)
    B1 = selected_piece.move_to(2,3, B1)
    selected_piece = piece_at(3,4, B1)
    B1 = selected_piece.move_to(3,3, B1)
    selected_piece = piece_at(5,4, B1)
    B1 = selected_piece.move_to(5,3, B1)
    
    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 1 and B1[1][i]._cur_Y == 1:
            B1[1].pop(i)
            break
    
    assert is_checkmate(True, B1) == True #Bishop is removed
    
def test_is_check6():
    B1 = read_board("board_examp.txt")
    B1[1].append(Rook(3,4,False))

    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 2 and B1[1][i]._cur_Y == 3:
            B1[1].pop(i)
            break
    B1[1].append(King(5,1,False))
    
    selected_piece = piece_at(2,4, B1)
    B1 = selected_piece.move_to(2,3, B1)
    selected_piece = piece_at(3,4, B1)
    B1 = selected_piece.move_to(3,3, B1)
    selected_piece = piece_at(5,4, B1)
    B1 = selected_piece.move_to(5,3, B1)
    
    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 1 and B1[1][i]._cur_Y == 1:
            B1[1].pop(i)
            break
            
    B1[1].append(Rook(5,4,True))
    
    assert is_check(True, B1) == True

def test_is_checkmate6():
    B1 = read_board("board_examp.txt")
    B1[1].append(Rook(3,4,False))

    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 2 and B1[1][i]._cur_Y == 3:
            B1[1].pop(i)
            break
    B1[1].append(King(5,1,False))
    
    selected_piece = piece_at(2,4, B1)
    B1 = selected_piece.move_to(2,3, B1)
    selected_piece = piece_at(3,4, B1)
    B1 = selected_piece.move_to(3,3, B1)
    selected_piece = piece_at(5,4, B1)
    B1 = selected_piece.move_to(5,3, B1)
    
    for i in range(len(B1[1])):
        if B1[1][i]._cur_X == 1 and B1[1][i]._cur_Y == 1:
            B1[1].pop(i)
            break
            
    B1[1].append(Rook(5,4,True))
    
    assert is_checkmate(True, B1) == False #Rook can block the check
    
def test_read_board2():
    #shouldn't work as board is in check
    with pytest.raises(IOError) as e:
        read_board("board_examp_1.txt")
    assert str(e.value) == "Board is already in checkmate"
        
def test_read_board3():
    #shouldn't work as white has no king
    with pytest.raises(IOError) as e:
        read_board("board_examp_2.txt")
    assert str(e.value) == "White doesn't have the correct number of kings"
        
def test_read_board4():
    B1 = read_board("board_examp_3.txt")
    
def test_read_board5():
    B1 = read_board("board_examp_4.txt")
    
def test_read_board6():
    #shouldn't work as size is too large
    with pytest.raises(IOError) as e:
        read_board("board_examp_5.txt")
    assert str(e.value) == "Board size is too large"
    
def test_read_board7():
    #shouldn't work as size is too large
    with pytest.raises(IOError) as e:
        read_board("board_examp_6.txt")
    assert str(e.value) == "Not all pieces are within board"
    
def test_read_board8():
    #shouldn't work as size is too large
    with pytest.raises(IOError) as e:
        read_board("board_examp_7.txt")
    assert str(e.value) == "Pieces overlap"
    
def test_is_check7():
    B1 = read_board("board_examp_3.txt")
    assert is_check(False, B1) == True
    
def test_is_checkmate7():
    B1 = read_board("board_examp_3.txt")
    assert is_checkmate(False, B1) == False
    
def test_is_check7():
    B1 = read_board("board_examp_3.txt")
    selected_piece = piece_at(2,6, B1)
    assert selected_piece.class_name == "Rook"
    B1 = selected_piece.move_to(7,6, B1)
    assert is_check(False, B1) == True
    
def test_is_checkmate7():
    B1 = read_board("board_examp_3.txt")
    selected_piece = piece_at(2,6, B1)
    assert selected_piece.class_name == "Rook"
    B1 = selected_piece.move_to(7,6, B1)
    assert is_checkmate(False, B1) == True
    
def test_is_check8():
    B1 = read_board("board_examp_3.txt")
    selected_piece = piece_at(2,6, B1)
    assert selected_piece.class_name == "Rook"
    B1 = selected_piece.move_to(7,6, B1)
    B1[1].append(Rook(6,4,False))
    assert is_check(False, B1) == True
    
def test_is_checkmate8():
    B1 = read_board("board_examp_3.txt")
    selected_piece = piece_at(2,6, B1)
    assert selected_piece.class_name == "Rook"
    B1 = selected_piece.move_to(7,6, B1)
    B1[1].append(Rook(6,4,False))
    assert is_checkmate(False, B1) == False
    
def test_is_check9():
    B1 = read_board("board_examp_3.txt")
    selected_piece = piece_at(2,6, B1)
    assert selected_piece.class_name == "Rook"
    B1 = selected_piece.move_to(7,6, B1)
    B1[1].append(Rook(6,4,False))
    B1[1].append(Bishop(7,3,True))
    assert is_check(False, B1) == True
    
def test_is_checkmate9():
    B1 = read_board("board_examp_3.txt")
    selected_piece = piece_at(2,6, B1)
    assert selected_piece.class_name == "Rook"
    B1 = selected_piece.move_to(7,6, B1)
    B1[1].append(Rook(6,4,False))
    B1[1].append(Bishop(7,3,True))
    assert is_checkmate(False, B1) == True
    
wb11 = Bishop(3,2,True)
wb12 = Bishop(3,4, True)
wr11 = Rook(2,2,True)
wk1 = King(3,5, True)
bk1 = King(1,5, False)


B2 = (5, [wb11, wb12, wr11, wk1, bk1])

def test_conf2unicode5():
    assert conf2unicode(B2) == "♚ ♔  \n  ♗  \n     \n ♖♗  \n     "

def test_only_king5():
    assert only_king(True, B2) == False
    assert only_king(False, B2) == True

def test_is_check10():
    assert is_check(False, B2) == False
    
def test_is_checkmate10():
    assert is_checkmate(False, B2) == True

def test_find_black_move1():
    B1 = read_board("board_examp_3.txt")
    black_piece, x_move, y_move = find_black_move(B1)
    assert (black_piece.class_name, black_piece._side, x_move, y_move) == ("King", False, 2, 6)
    
def test_find_black_move2():
    B1 = read_board("board_examp_3.txt")
    selected_piece = piece_at(2,6, B1)
    B1 = selected_piece.move_to(7,6, B1)
    B1[1].append(Rook(6,4,False))
    black_piece, x_move, y_move = find_black_move(B1)
    assert (black_piece.class_name, black_piece._side, x_move, y_move) == ("Rook", False, 6, 7)
    
wr21 = Rook(1,1,True)
wr22 = Rook(8,1,True)
wb23 = Bishop(3,1, True)
wb24 = Bishop(6,1, True)
wk2 = King(5,1, True)
br21 = Rook(1,8, False)
br22 = Rook(8,8, False)
bb23 = Bishop(3,8, False)
bb24 = Bishop(6,8, False)
bk2 = King(5,8, False)

B3 = (8, [wr21, wr22, wb23, wb24, wk2, br21, br22, bb23, bb24, bk2])

def test_read_board9():
    B = read_board("board_examp_8.txt")
    assert B[0] == 8
    assert B3[0] == 8 

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B3[1]:
            if piece._cur_X == piece1._cur_X and piece._cur_Y == piece1._cur_Y and piece._side == piece1._side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B3[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece._cur_X == piece1._cur_X and piece._cur_Y == piece1._cur_Y and piece._side == piece1._side and type(piece) == type(piece1):
                found = True
        assert found
        
def test_list_squares1():
    B = read_board("board_examp_8.txt")
    selected_piece = piece_at(1,8, B)
    assert selected_piece.list_squares(1,1, B) == [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7)]
    
def test_list_squares2():
    B = read_board("board_examp_8.txt")
    selected_piece = piece_at(1,8, B)
    assert selected_piece.list_squares(8,8, B) == [(2,8), (3,8), (4,8), (5,8), (6,8), (7,8)]
    
def test_list_squares3():
    B = read_board("board_examp_8.txt")
    selected_piece = piece_at(8,1, B)
    assert selected_piece.list_squares(1,1, B) == [(2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
    
def test_list_squares4():
    B = read_board("board_examp_8.txt")
    selected_piece = piece_at(8,1, B)
    assert selected_piece.list_squares(8,8, B) == [(8,2), (8,3), (8,4), (8,5), (8,6), (8,7)]
    
def test_list_squares5():
    B = read_board("board_examp_8.txt")
    selected_piece = piece_at(3,8, B)
    assert selected_piece.list_squares(8,3, B) == [(4,7), (5,6), (6,5), (7,4)]
    
def test_list_squares6():
    B = read_board("board_examp_8.txt")
    selected_piece = piece_at(6,8, B)
    assert selected_piece.list_squares(1,3, B) == [(5,7), (4,6), (3,5), (2,4)]
    
def test_list_squares7():
    B = read_board("board_examp_8.txt")
    selected_piece = piece_at(3,1, B)
    assert selected_piece.list_squares(8,6, B) == [(4,2), (5,3), (6,4), (7,5)]
    
def test_list_squares8():
    B = read_board("board_examp_8.txt")
    selected_piece = piece_at(6,1, B)
    assert selected_piece.list_squares(1,6, B) == [(5,2), (4,3), (3,4), (2,5)]