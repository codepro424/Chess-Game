#Pygame Initialization
import pygame
pygame.init()
WIDTH = 1100
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.Font('freesansbold.ttf', 20)
timer = pygame.time.Clock()
fps = 60

#Variables
run = True
EnPassantL = False
EnPassantR = False
turn = 0 
counter = 0
game = []
legal_moves = []             # 0 - white to select;  1- white to move;  2-black to select;  3-black to move
white_legal_moves = []
black_legal_moves = []
br1m = 0
br2m = 0
bkm = 0
wr1m = 0
wr2m = 0
wkm = 0
files = 'abcdefgh'
rank = '12345678'

wp = 'white pawn'
bp = 'black pawn'
wq = 'white queen'
bq = 'black queen'
wr = 'white rook'
br = 'black rook'
wk = 'white king'
bk = 'black king'
wn = 'white knight'
bn = 'black knight'
wb = 'white bishop'
bb = 'black bishop'

board = [[br, bn, bb, bq, bk, bb, bn, br],
         [bp, bp, bp, bp, bp, bp, bp, bp],
         [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
         [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
         [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
         [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
         [wp, wp, wp, wp, wp, wp, wp, wp],
         [wr, wn, wb, wq, wk, wb, wn, wr]
         ]

#Loading in images
BQ = pygame.image.load('images/bQ.png')
BQ = pygame.transform.scale(BQ, (100, 100))
WQ = pygame.image.load('images/wQ.png')
WQ = pygame.transform.scale(WQ, (100, 100))
BB = pygame.image.load('images/bB.png')
BB = pygame.transform.scale(BB, (100, 100))
WB = pygame.image.load('images/wB.png')
WB = pygame.transform.scale(WB, (100, 100))
WK = pygame.image.load('images/wK.png')
WK = pygame.transform.scale(WK, (100, 100))
BK = pygame.image.load('images/bK.png')
BK = pygame.transform.scale(BK, (100, 100))
BN = pygame.image.load('images/bN.png')
BN = pygame.transform.scale(BN, (100, 100))
WN = pygame.image.load('images/wN.png')
WN = pygame.transform.scale(WN, (100, 100))
BR = pygame.image.load('images/bR.png')
BR = pygame.transform.scale(BR, (100, 100))
WR = pygame.image.load('images/wR.png')
WR = pygame.transform.scale(WR, (100, 100))
BP = pygame.image.load('images/bP.png')
BP = pygame.transform.scale(BP, (100, 100))
WP = pygame.image.load('images/wP.png')
WP = pygame.transform.scale(WP, (100, 100))


#Functions
def check_legal_moves_of_selected_piece(pieceX, pieceY):
    global white_legal_moves
    piece = board[pieceY][pieceX]
    if 'white' in piece:
        color = 'white'
    else:
        color = 'black'

    if 'knight' in piece:
        legal_moves = CheckKnight(pieceX, pieceY, color)
    elif 'bishop' in piece:
        legal_moves = CheckBishop(pieceX, pieceY, color)
    elif 'pawn' in piece:
        legal_moves = CheckPawn(pieceX, pieceY, color)
    elif 'king' in piece:
        legal_moves = CheckKing(pieceX, pieceY, color)
    elif 'queen' in piece:
        legal_moves = CheckQueen(pieceX, pieceY, color)
    elif 'rook' in piece:
        legal_moves = CheckRook(pieceX, pieceY, color)

    return legal_moves

def check_all_legal_moves():
    white_legal_moves.clear()
    black_legal_moves.clear()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if 'white' in str(board[i][j]):
                l = check_legal_moves_of_selected_piece(j, i)
                for x in l:
                    white_legal_moves.append(x)
                
            elif 'black' in str(board[i][j]):
                l = check_legal_moves_of_selected_piece(j, i)
                for x in l:
                    black_legal_moves.append(x)

def CheckKnight(posX, posY, color):
    legal_moves = []
    possibilities = [(posX+2, posY+1), (posX+2, posY-1), (posX-2, posY+1), (posX-2, posY-1), (posX+1, posY+2), (posX-1, posY+2), (posX+1, posY-2), (posX-1, posY-2)]
    for m in possibilities:
        if m[0] < 8 and m[1] < 8 and m[0] >= 0 and m[1] >= 0:
            if color not in str(board[m[1]][m[0]]):
                legal_moves.append(m)

    return legal_moves

def CheckBishop(posX, posY, color):
    legal_moves = []
    for (a,b) in [(x,y) for x in [1,-1] for y in [1,-1]]:
        for i in [1, 2, 3, 4, 5, 6, 7]:
            if (posX + i*a) < 8 and (posX + i*a) >= 0 and (posY + i*b) < 8 and (posY + i*b) >= 0:
                if board[posY + i*b][posX + i*a] == 0:
                    legal_moves.append((posX + i*a, posY + i*b))
                else:
                    if color not in board[posY + i*b][posX + i*a]:
                        legal_moves.append((posX + i*a, posY + i*b))
                    break
    

    return legal_moves

def CheckPawn(posX, posY, color):
    global EnPassantL
    global EnPassantR
    legal_moves = []
    EnPassantL = False
    EnPassantR = False
    if color == 'white':
        k = -1
    else:
        k = 1
    
    if posY + k >= 0 and posY + k < 8:
        if board[(posY + k)][posX] == 0:
            legal_moves.append((posX, posY + k))
            if (color == 'white' and posY == 6) or (color == 'black' and posY == 1):
                if board[(posY + 2*k)][posX] == 0:
                    legal_moves.append((posX, posY + 2*k))

        if (posX+1) < 8 and board[posY + k][posX + 1] != 0 and color not in board[posY + k][posX + 1]:
            legal_moves.append((posX+1, posY+k))

        if (posX-1) >= 0 and board[posY + k][posX - 1] != 0 and color not in board[posY + k][posX - 1]:
            legal_moves.append((posX-1, posY+k))
    
    if color == 'white' and (posX + 1) < 8 and posY == 3 and game[-1] == Convert_to_chess_notation((posX+1, posY-2), (posX+1, posY)) and board[posY][posX+1] == 'black pawn':
        EnPassantR = True
        legal_moves.append((posX+1, posY-1))

    elif color == 'white' and (posX - 1) >= 0 and posY == 3 and game[-1] == Convert_to_chess_notation((posX-1, posY-2), (posX-1, posY)) and board[posY][posX-1] == 'black pawn':
        EnPassantL = True
        legal_moves.append((posX-1, posY-1))
        
    elif color == 'black' and (posX + 1) < 8 and posY == 4 and game[-1] == Convert_to_chess_notation((posX+1, posY+2), (posX+1, posY)) and board[posY][posX+1] == 'white pawn':
        EnPassantR = True
        legal_moves.append((posX+1, posY+1))
        
    elif color == 'black' and (posX - 1) >= 0 and posY == 4 and game[-1] == Convert_to_chess_notation((posX-1, posY+2), (posX-1, posY)) and board[posY][posX-1] == 'white pawn':
        EnPassantL = True
        legal_moves.append((posX-1, posY+1))
        

    return legal_moves

def CheckKing(posX, posY, color):
    legal_moves = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (posX + i) < 8 and (posX + i) >= 0 and (posY + j) < 8 and (posY + j) >= 0:
                if color not in str(board[posY + j][posX + i]):
                    legal_moves.append((posX+i, posY+j))

    checked = CheckIfChecked()
    if color == 'white' and (posX - 2) >= 0 and wr1m == 0 and wkm == 0 and (posX - 1, posY) not in black_legal_moves and board[posY][posX - 1] == 0 and (posX - 2, posY) not in black_legal_moves and board[posY][posX - 2] == 0 and not checked[0]:
        legal_moves.append((posX - 2, posY))
    elif color == 'white' and (posX + 2) < 8 and wr2m == 0 and wkm == 0 and (posX + 1, posY) not in black_legal_moves and board[posY][posX + 1] == 0 and (posX + 2, posY) not in black_legal_moves and board[posY][posX + 2] == 0 and not checked[0]:
        legal_moves.append((posX + 2, posY))
    elif color == 'black' and (posX - 2) >= 0 and br1m == 0 and bkm == 0 and (posX - 1, posY) not in white_legal_moves and board[posY][posX - 1] == 0 and (posX - 2, posY) not in white_legal_moves and board[posY][posX - 2] == 0 and not checked[1]:
        legal_moves.append((posX - 2, posY))
    elif color == 'black' and (posX + 2) < 8 and br1m == 0 and bkm == 0 and (posX + 1, posY) not in white_legal_moves and board[posY][posX + 1] == 0 and (posX + 2, posY) not in white_legal_moves and board[posY][posX + 2] == 0 and not checked[1]:
        legal_moves.append((posX + 2, posY))

    return legal_moves

def CheckQueen(posX, posY, color):
    a = set(CheckRook(posX, posY, color))
    b = set(CheckBishop(posX, posY, color))
    c = a.union(b)
    legal_moves = list(c)

    return legal_moves

def CheckRook(posX, posY, color):
    legal_moves = []
    plusX = 8
    minusX = -8
    plusY = 8
    minusY = -8

    for i in [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7]:
        if i >= minusX and i <= plusX and (posX + i) >= 0 and (posX + i) < 8:
            if board[posY][posX + i] == 0:
                legal_moves.append((posX + i, posY))
            else:
                if color not in board[posY][posX + i]:
                    legal_moves.append((posX + i, posY))

                if i < 0:
                    minusX = i
                else:
                    plusX = i

    for i in [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7]:
        if i >= minusY and i <= plusY and i != 0 and (posY + i) >= 0 and (posY + i) < 8:
            if board[posY + i][posX] == 0:
                legal_moves.append((posX, posY + i))
            else:
                if color not in board[posY + i][posX]:
                    legal_moves.append((posX, posY + i))

                if i < 0:
                    minusY = i
                else:
                    plusY = i

    return legal_moves

def CheckIfChecked():
    WhiteChecked = False
    BlackChecked = False
    for i in black_legal_moves:
        if board[i[1]][i[0]] == 'white king':
            WhiteChecked = True

    for i in white_legal_moves:
        if board[i[1]][i[0]] == 'black king':
            BlackChecked = True

    return [WhiteChecked, BlackChecked]

def DrawBoard():
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                color = (61, 165, 58)
            else:
                color = 'light yellow'
            pygame.draw.rect(screen, color, [i*100, j*100, 100, 100])

    #Adding pieces to position
    for i in range(len(board)):

        for j in range(len(board[i])):
            if board[i][j] == 'white pawn':
                screen.blit(WP, (j*100, i*100))
            if board[i][j] == 'black pawn':
                screen.blit(BP, (j*100, i*100))
            if board[i][j] == 'white knight':
                screen.blit(WN, (j*100, i*100))
            if board[i][j] == 'white bishop':
                screen.blit(WB, (j*100, i*100))
            if board[i][j] == 'white rook':
                screen.blit(WR, (j*100, i*100))
            if board[i][j] == 'white queen':
                screen.blit(WQ, (j*100, i*100))
            if board[i][j] == 'white king':
                screen.blit(WK, (j*100, i*100))
            if board[i][j] == 'black king':
                screen.blit(BK, (j*100, i*100))
            if board[i][j] == 'black knight':
                screen.blit(BN, (j*100, i*100))
            if board[i][j] == 'black bishop':
                screen.blit(BB, (j*100, i*100))
            if board[i][j] == 'black rook':
                screen.blit(BR, (j*100, i*100))
            if board[i][j] == 'black queen':
                screen.blit(BQ, (j*100, i*100))

    if turn == 1 or turn == 3:
        pygame.draw.rect(screen, 'blue', [selected_piece_pos[0]*100, selected_piece_pos[1]*100, 100, 100], 5)
        if legal_moves != None:
            for i in legal_moves:
                pygame.draw.circle(screen, 'blue', (i[0]*100 + 50, i[1]*100 + 50), 15)
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if 'white king' == board[i][j]:
                wk_pos = (j, i)
            elif 'black king' == board[i][j]:
                bk_pos = (j, i)

    checked = CheckIfChecked()

    if checked[0] and counter < 15:
        pygame.draw.rect(screen, 'dark red', [wk_pos[0]*100, wk_pos[1]*100, 100, 100], 5)
            
    if checked[1] and counter < 15:
        pygame.draw.rect(screen, 'dark red', [bk_pos[0]*100, bk_pos[1]*100, 100, 100], 5)

def Convert_to_chess_notation(sq1, sq2):
    return f'{files[sq1[0]]}{rank[sq1[1]]}-{files[sq2[0]]}{rank[sq2[1]]}'

#Mainloop
while run:
    timer.tick(fps)
    screen.fill('light gray')
    check_all_legal_moves()
    DrawBoard()

    print(f'{EnPassantL}, {EnPassantR}')

    if counter < 30:
        counter += 1
    else:
        counter = 0

    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] <= 800 and event.pos[1] <= 800:

            # Move Piece
            if legal_moves != None and (turn == 1 or turn == 3) and (event.pos[0]//100, event.pos[1]//100) in legal_moves:
                if turn == 3:
                    piece = board[selected_piece_pos[1]][selected_piece_pos[0]]

                    #Check Castling Move
                    if piece == 'black king' and (event.pos[0]//100, event.pos[1]//100) in [(selected_piece_pos[0] + 2, selected_piece_pos[1]), (selected_piece_pos[0] - 2, selected_piece_pos[1])]:
                        board[selected_piece_pos[1]][selected_piece_pos[0]] = 0
                        board[event.pos[1]//100][event.pos[0]//100] = piece
                        if board[selected_piece_pos[1]][selected_piece_pos[0] + 3] == 'black rook':
                            r = board[selected_piece_pos[1]][selected_piece_pos[0] + 3]
                            board[selected_piece_pos[1]][selected_piece_pos[0] + 3] = 0
                            board[selected_piece_pos[1]][selected_piece_pos[0] + 1] = r
                            game.append('O-O')

                        else:
                            r = board[selected_piece_pos[1]][selected_piece_pos[0] - 4]
                            board[selected_piece_pos[1]][selected_piece_pos[0] - 4] = 0
                            board[selected_piece_pos[1]][selected_piece_pos[0] - 1] = r
                            game.append('O-O-O')

                        turn = 0

                    #Check En-Passant Move
                    elif piece == 'black pawn' and event.pos[0]//100 in [selected_piece_pos[0]-1, selected_piece_pos[0]+1] and (EnPassantR or EnPassantL):
                        board[selected_piece_pos[1]][selected_piece_pos[0]] = 0
                        board[event.pos[1]//100][event.pos[0]//100] = piece
                        if (event.pos[0]//100, event.pos[1]//100) == (selected_piece_pos[0]+1, selected_piece_pos[1]+1) and EnPassantR:
                            board[selected_piece_pos[1]][selected_piece_pos[0]+1] = 0
                        else:
                            board[selected_piece_pos[1]][selected_piece_pos[0]-1] = 0
                        

                        turn = 0

                    else:
                        board[selected_piece_pos[1]][selected_piece_pos[0]] = 0
                        otherpiece = board[event.pos[1]//100][event.pos[0]//100]
                        board[event.pos[1]//100][event.pos[0]//100] = piece
                        
                        check_all_legal_moves()
                        checked = CheckIfChecked()
                        if checked[1]:
                            board[selected_piece_pos[1]][selected_piece_pos[0]] = piece
                            board[event.pos[1]//100][event.pos[0]//100] = otherpiece
                            turn = 2

                        else:
                            game.append(Convert_to_chess_notation(selected_piece_pos, (event.pos[0]//100, event.pos[1]//100)))
                            if selected_piece_pos == [0, 0] and piece == 'black rook':
                                br1m = 1
                            elif selected_piece_pos == [7, 0] and piece == 'black rook':
                                br2m = 1
                            elif selected_piece_pos == [4, 0] and piece == 'black king':
                                bkm = 1

                            turn = 0

                else:
                    piece = board[selected_piece_pos[1]][selected_piece_pos[0]]

                    # Check Castling Move
                    if piece == 'white king' and (event.pos[0]//100, event.pos[1]//100) in [(selected_piece_pos[0] + 2, selected_piece_pos[1]), (selected_piece_pos[0] - 2, selected_piece_pos[1])]:
                        board[selected_piece_pos[1]][selected_piece_pos[0]] = 0
                        board[event.pos[1]//100][event.pos[0]//100] = piece
                        if board[selected_piece_pos[1]][selected_piece_pos[0] + 3] == 'white rook':
                            r = board[selected_piece_pos[1]][selected_piece_pos[0] + 3]
                            board[selected_piece_pos[1]][selected_piece_pos[0] + 3] = 0
                            board[selected_piece_pos[1]][selected_piece_pos[0] + 1] = r
                            game.append('O-O')

                        else:
                            r = board[selected_piece_pos[1]][selected_piece_pos[0] - 4]
                            board[selected_piece_pos[1]][selected_piece_pos[0] - 4] = 0
                            board[selected_piece_pos[1]][selected_piece_pos[0] - 1] = r
                            game.append('O-O-O')

                        turn += 1

                    #Check En-Passant Move
                    elif piece == 'white pawn' and (event.pos[0]//100, event.pos[1]//100) in [(selected_piece_pos[0]+1, selected_piece_pos[1]-1), (selected_piece_pos[0]-1, selected_piece_pos[1]-1)] and (EnPassantL or EnPassantR):
                        board[selected_piece_pos[1]][selected_piece_pos[0]] = 0
                        board[event.pos[1]//100][event.pos[0]//100] = piece
                        if (event.pos[0]//100, event.pos[1]//100) == (selected_piece_pos[0]+1, selected_piece_pos[1]+1) and EnPassantR:
                            board[selected_piece_pos[1]][selected_piece_pos[0]+1] = 0

                        else:
                            board[selected_piece_pos[1]][selected_piece_pos[0]-1] = 0

                        turn += 1

                    else:
                        board[selected_piece_pos[1]][selected_piece_pos[0]] = 0
                        otherpiece = board[event.pos[1]//100][event.pos[0]//100]
                        board[event.pos[1]//100][event.pos[0]//100] = piece
                        
                        check_all_legal_moves()
                        checked = CheckIfChecked()
                        if checked[0]:
                            board[selected_piece_pos[1]][selected_piece_pos[0]] = piece
                            board[event.pos[1]//100][event.pos[0]//100] = otherpiece
                            turn = 0

                        else:
                            game.append(Convert_to_chess_notation(selected_piece_pos, (event.pos[0]//100, event.pos[1]//100)))
                            if selected_piece_pos == [0, 7] and piece == 'white rook':
                                wr1m = 1
                            elif selected_piece_pos == [7, 7] and piece == 'white rook':
                                wr2m = 1
                            elif selected_piece_pos == [4, 7] and piece == 'white king':
                                wkm = 1

                            turn += 1

                legal_moves.clear()
            
            # Select Piece
            elif turn == 0 or turn == 2:
                if ('white' in str(board[event.pos[1]//100][event.pos[0]//100]) and turn < 2) or ('black' in str(board[event.pos[1]//100][event.pos[0]//100]) and turn > 1):
                    turn += 1
                    selected_piece_pos = [event.pos[0]//100, event.pos[1]//100]
                    legal_moves = check_legal_moves_of_selected_piece(selected_piece_pos[0], selected_piece_pos[1])
            
            else:
                turn -= 1

    pygame.display.flip()

pygame.quit()
