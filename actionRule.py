# -*- coding: utf-8 -*-
"""
    codeMarble_Core.actionRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
    :copyright: (c) 2017 by codeMarble
"""

import os
from errorCode import ErrorCode

error = ErrorCode()


class ActionRule(object):
    def __init__(self):
        pass

    # actionRuleNum(0:script, 1:remove, 2:change), actionRuleOption1(0:script, 1:＋dir, 2:×dir, 3:8dir, 4:go)
    # actionRuleOption2(0:othello, n:size)
    def checkActionRule(self, data):
        try:
            if type(data.actionRuleNum) is not int:
                return error.serverError('type not matched.')

            if actionRuleNum is 1:
                return self.removeObject(data.actionRuleNum)

            elif actionRuleNum is 2:
                return self.changeObject(data.actionRuleNum)

            else:
                return error.serverError('unknown actionRuleNum : {}'.format(data.actionRuleNum))

        except Exception as e:
            return error.serverError()

    # actionRuleOption1(0:script, 1:＋dir, 2:×dir, 3:8dir, 4:go)
    # actionRuleOption2(0:othello, n:size)
    # actionRuleOption1, actionRuleOption2, gameBoard, dataBoard, pos
    def removeObject(self, data):
        try:
            if type(data.actionRuleOption1) != int or type(data.actionRuleOption2) != int or type(data.pos[0]) != int or type(data.pos[1]) != int:
                return error.serverError('type not matched.')

            elif len(data.gameBoard) !=  len(data.gameBoard[0]):
                return error.serverError('gameboard size not matched. [row : {}, col : {}]'.format(len(data.gameBoard), len(data.gameBoard[0])))

            if data.actionRuleOption2 > len(data.gameBoard):
                return error.serverError('The size you want to erase is larger than the size of the board. [erase size : {}, board size : {}]'.format(data.actionRuleOption2, len(data.gameBoard)))


            if 1 <= data.actionRuleOption1 <= 3: # remove size or othello
                if data.actionRuleOption2 == 0: # othello
                    return self.actionObjectByOthello(data.gameBoard, pos, 0)
                else: # size
                    return self.actionObjectBySize(data.gameBoard, pos, data.actionRuleOption2, 0)
            elif data.actionRuleOption1 == 4:  # remove go rule
                return self.actionObjectByGo(gameBoard, data.pos, 0)
            else:
                return error.serverError('unknown actionRuleOption1 : {}'.format(data.actionRuleOption1))

        except Exception as e:
            return error.serverError()

    def actionObjectByGo(self, board, pos, value):
        pi, pj = pos
        me = board[pi][pj]
        you = -me

        goRule = GoRule()

        yous = goRule.findYou(board, pos)
        for (i, j) in yous:
            if goRule.checkBoard(board, (i, j)):
                goRule.remove(board, (i, j), value)

        return True

    def actionObjectBySize(self, board, pos, actionRuleOption1, value):
        pi, pj = pos
        directions = self.getDirection(actionRuleOption1)

        for i in range(1, actionRuleOption1 + 1):
            for d in directions:
                try:
                    board[pi + d[0] * i][pj + d[1] * i] = value
                except Exception as e:
                    continue

        return True

    def actionObjectByOthello(self, board, pos, value):
        pi, pj = pos
        dirs = self.getDirection(1)
        me = board[pi][pj]
        you = -me

        for d in dirs:
            for i in range(len(board)):
                try:
                    ni, nj = pi + i * d[0], pj + i * d[1]
                    if board[ni][nj] == me:
                        i, j = pi, pj
                        while i+d[0] != ni or j+d[1] != nj:
                            board[i+d[0]][j+d[1]] = value
                            i, j = i + d[0], j + d[1]
                        break

                except Exception as e:
                    break

        return True

    def getDirection(self, actionRuleOption1):
        if actionRuleOption1 is 1:
            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]

        elif actionRuleOption1 is 2:
            dirs = [[-1, -1], [-1, 1], [1, -1], [1, 1]]

        elif actionRuleOption1 is 3:
            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1], [-1, -1], [-1, 1], [1, -1], [1, 1]]

        elif actionRuleOption1 is 4:
            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]

        else:
            return error.serverError('unknown actionRuleOption1 : {}'.format(actionRuleOption1))

        return dirs

    # actionRuleNum, actionRuleOption1, actionRuleOption2, gameBoard, dataBoard, pos
    def changeObject(self, data):
        try:
            if type(data.actionRuleOption1) != int or type(data.actionRuleOption2) != int or type(
                    data.pos[0]) != int or type(data.pos[1]) != int:
                return error.serverError('type not matched.')

            elif len(data.gameBoard) != len(data.gameBoard[0]):
                return error.serverError('gameboard size not matched. [row : {}, col : {}]'.format(len(data.gameBoard),
                                                                                                   len(data.gameBoard[
                                                                                                           0])))

            if data.actionRuleOption2 > len(data.gameBoard):
                return error.serverError(
                    'The size you want to erase is larger than the size of the board. [erase size : {}, board size : {}]'.format(
                        data.actionRuleOption2, len(data.gameBoard)))

            if 1 <= data.actionRuleOption1 <= 3:  # remove size or othello
                if data.actionRuleOption2 == 0:  # othello
                    return self.actionObjectByOthello(data.gameBoard, pos, data.gameBoard[pos[0]][pos[1]])
                else:  # size
                    return self.actionObjectBySize(data.gameBoard, pos, data.actionRuleOption2, data.gameBoard[pos[0]][pos[1]])
            elif data.actionRuleOption1 == 4:  # remove go rule
                return self.actionObjectByGo(gameBoard, data.pos, data.gameBoard[pos[0]][pos[1]])
            else:
                return error.serverError('unknown actionRuleOption1 : {}'.format(data.actionRuleOption1))

        except Exception as e:
            return error.serverError()

    def actionObjectByScript(self, data):

        pass

    class GoRule:
        def checkBoard(self, board, pos):
            pi, pj = pos
            me = board[pi][pj]
            you = -me

            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            visit = [[0 for i in range(len(board[0]))] for j in range(len(board))]
            stack = [[pi, pj]]

            while stack:
                i, j = stack.pop()
                visit[i][j] = 1

                for d in dirs:
                    ni, nj = d[0] + i, d[1] + j
                    if board[ni][nj] == you or board[ni][nj] == me and visit[ni][nj]:
                        continue
                    elif board[ni][nj] == me and not visit[ni][nj]:
                        stack.append([ni, nj])
                    else:
                        return False

            return True

        def remove(self, board, pos, value):
            pi, pj = pos
            me = board[pi][pj]
            you = -me

            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            visit = [[0 for i in range(len(board[0]))] for j in range(len(board))]
            stack = [[pi, pj]]

            while stack:
                i, j = stack.pop()
                visit[i][j] = 1
                board[i][j] = value

                for d in dirs:
                    ni, nj = d[0] + i, d[1] + j
                    if board[ni][nj] == you or visit[ni][nj]:
                        continue
                    elif board[ni][nj] == me and not visit[ni][nj]:
                        stack.append([ni, nj])
                    else:
                        return False

            return True

        def findYou(self, board, pos):
            pi, pj = pos
            me = board[pi][pj]
            you = -me
            dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
            lst = list()

            for d in dirs:
                try:
                    ni, nj = d[0] + pi, d[1] + pj
                    if board[ni][nj] == you:
                        lst.append([ni, nj])
                except Exception as e:
                    pass

            return lst