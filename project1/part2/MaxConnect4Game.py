#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

from copy import copy, deepcopy
from errno import ESTALE
import random
import sys
from enum import Enum

class Direction(Enum):
    UP_LEFT = 1
    UP = 2
    UP_RIGHT = 3
    LEFT = 4
    RIGHT = 5
    DOWN_LEFT = 6
    DOWN = 7
    DOWN_RIGHT = 8

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.counter = 0
        random.seed()

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        for row in self.gameBoard:
            print(row)
        print()


    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1
    
    # test what columns are valid for minimax to work on 
    def valid_columns(self):
        valid_columns = list()

        for column in range(7):
            if not self.gameBoard[0][column]:
                for i in range(5, -1, -1):
                    if not self.gameBoard[i][column]:
                        valid_columns.append(column)
                        break
        
        return valid_columns

    def score_heuristic(self, score):
        if score == 4:
            return 100
        elif score == 3:
            return 50
        elif score == 2:
            return 25
        elif score == 1:
            return 1
        else:
            return 0

    def count_pieces(self, board_state, position, agent):
        score = 0
        count = 0
        row = position[0] # row
        col = position[1] # col
        # test horizontal
        for i in range(col):
            if i != 0:
                if board_state[row][col-i] == 0 or board_state[row][col-i] != agent:
                    break
                elif board_state[row][col-i] == agent:
                    count += 1

                if count == 4:
                    break
        
        score += self.score_heuristic(count)
        count = 0


        for i in range(7-col):
            if i != 0:
                if board_state[row][col+i] == 0 or board_state[row][col+i] != agent:
                    break
                elif board_state[row][col+i] == agent:
                    count += 1

                if count == 4:
                    break

        score += self.score_heuristic(count)
        count = 0

        # test vertical
        for i in range(row):
            if i != 0:
                if board_state[row-i][col] == 0 or board_state[row-i][col] != agent:
                    break
                elif board_state[row-i][col] == agent:
                    count += 1

                if count == 4:
                    break

        score += self.score_heuristic(count)
        count = 0

        for i in range(6-row):
            if i != 0:
                if board_state[row+i][col] == 0 or board_state[row+i][col] != agent:
                    break
                elif board_state[row+i][col] == agent:
                    count += 1

                if count == 4:
                    break

        score += self.score_heuristic(count)
        count = 0

        tmp_row = row
        tmp_col = col
        # test diagonal left
        for i in range(row+col):
            if i != 0:
                if tmp_col > 0 and tmp_col < 7 and tmp_row > 0 and tmp_row < 6:
                    if board_state[tmp_row][tmp_col] == 0 or board_state[tmp_row][tmp_col] != agent:
                        break
                    elif board_state[tmp_row][tmp_col] == agent:
                        count += 1

                    if count == 4:
                        break
                else:
                    break
                tmp_col -= 1
                tmp_row += 1

        score += self.score_heuristic(count)
        count = 0

        tmp_row = row
        tmp_col = col
        for i in range(row+col):
            if i != 0:
                if tmp_col > 0 and tmp_col < 7 and tmp_row > 0 and tmp_row < 6:
                    if board_state[tmp_row][tmp_col] == 0 or board_state[tmp_row][tmp_col] != agent:
                        break
                    elif board_state[tmp_row][tmp_col] == agent:
                        count += 1

                    if count == 4:
                        break
                else:
                    break
                tmp_col -= 1
                tmp_row += 1

        score += self.score_heuristic(count)
        count = 0

        # test diagonal right
        tmp_row = row
        tmp_col = col

        for i in range(row+col):
            if i != 0:
                if tmp_col > 0 and tmp_col < 7 and tmp_row > 0 and tmp_row < 6:
                    if board_state[tmp_row][tmp_col] == 0 or board_state[tmp_row][tmp_col] != agent:
                        break
                    elif board_state[tmp_row][tmp_col] == agent:
                        count += 1

                    if count == 4:
                        break
                else:
                    break
                tmp_col += 1
                tmp_row += 1

        score += self.score_heuristic(count)
        count = 0

        tmp_row = row
        tmp_col = col
        for i in range(row+col):
            if i != 0:
                if tmp_col > 0 and tmp_col < 7 and tmp_row > 0 and tmp_row < 6:
                    if board_state[tmp_row][tmp_col] == 0 or board_state[tmp_row][tmp_col] != agent:
                        break
                    elif board_state[tmp_row][tmp_col] == agent:
                        count += 1

                    if count == 4:
                        break
                else:
                    break
                tmp_col -= 1
                tmp_row -= 1

        score += self.score_heuristic(count)
        count = 0

        return score

    # heuristic to determine score of current board
    def heuristic(self, board_state):
        score = 0
        opponent = 0
        if self.currentTurn == 1:
            opponent = 2
        else:
            opponent = 1

        storeScore1 = self.player1Score
        storeScore2 = self.player2Score

        tmpBoard = deepcopy(board_state)
        self.gameBoard = tmpBoard

        self.countScore()

        if self.currentTurn == 1 and self.player1Score > 0:
            score += 100*self.player1Score
            self.player1Score = storeScore1
            self.player2Score = storeScore2
            self.gameBoard = board_state
        elif self.currentTurn == 2 and self.player2Score > 0:
            score += 100*self.player2Score
            self.player1Score = storeScore1
            self.player2Score = storeScore2
            self.gameBoard = board_state

        # evaluate 4 in a rows
        for x in range(6):
            for y in range(7):
                if(board_state[x][y] == 0):
                    score += self.count_pieces(board_state, (x,y), self.currentTurn)
                    score -= self.count_pieces(board_state, (x,y), opponent)

        self.gameBoard = board_state

        return score

    def flipTurn(self):
        if self.currentTurn == 1:
            self.currentTurn = 2
        else:
            self.currentTurn = 1

    # minimax algorithm
    def minimax(self, board_state, depth):
        val, col = self.maxPlayer(deepcopy(board_state), -9999, 9999, depth-1)
        return col

    def minPlayer(self, state, alpha, beta, depth):
        storeBoard = deepcopy(state)
        self.gameBoard = storeBoard

        val = 9999
        minCol = 9999

        columns = self.valid_columns()

        for column in columns:
            if depth > 0:
                self.flipTurn()
                storeBoard = deepcopy(state)
                self.gameBoard = storeBoard
                self.playPiece(column)

                self.flipTurn()

                tstVal, maxCol = self.maxPlayer(self.gameBoard, alpha, beta, depth-1)

            else:
                tstVal = self.heuristic(storeBoard)

            if tstVal < val:
                val = tstVal
                minCol = column

            if tstVal < beta:
                beta = tstVal
                    
            if tstVal <= beta:
                break

        storeBoard = deepcopy(state)
        self.gameBoard = storeBoard

        return val, minCol

    def maxPlayer(self, state, alpha, beta, depth):
        # row, col
        storeBoard = deepcopy(state)
        self.gameBoard = storeBoard

        columns = self.valid_columns()
        val = -9999
        maxCol = -9999

        for column in columns:
            if depth > 0:
                storeBoard = deepcopy(state)
                self.gameBoard = storeBoard
                self.playPiece(column)

                tstVal, minCol = self.minPlayer(self.gameBoard, alpha, beta, depth-1)

            else:
                tstVal = self.heuristic(storeBoard)

            if tstVal > val:
                val = tstVal
                maxCol = column

            if tstVal > alpha:
                alpha = tstVal
                    
            if tstVal >= beta:
                break
 
        storeBoard = deepcopy(state)
        self.gameBoard = storeBoard
        
        return val, maxCol
       

    # The AI section. Currently plays randomly.
    def aiPlay(self, depth):
        storeBoard = deepcopy(self.gameBoard)
        pieceCount = deepcopy(self.pieceCount)
        player1score = deepcopy(self.player1Score)
        player2score = deepcopy(self.player2Score)
        column = self.minimax(self.gameBoard, depth)

        # reset the board back to original
        self.gameBoard = storeBoard
        self.player1Score = player1score
        self.player2Score = player2score
        self.pieceCount = pieceCount

        self.playPiece(column)


    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0
        self.player2Score = 0

        #self.printGameBoard()

        # Check horizontally
        for row in self.gameBoard:
            #print(row)
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1

