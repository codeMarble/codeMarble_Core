# -*- coding: utf-8 -*-
"""
    codeMarble_Core.placementRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
    :copyright: (c) 2017 by codeMarble
"""

import os
from errorCode import ErrorCode

error = ErrorCode()


class PlacementRule(object):
    def __init__(self):
        pass


    # placementRuleNum(0:script, 1:add, 2:move), placementRuleOption(0:no option, 1or2: add option, [n1,n2]: move option)
    # isAllyExistNum, isEnemyExistNum, isExtraExistNum(1:don't placement, 2:remove, 3:modify)
    # existOption([1or2]:remove option, [n1,n2]:modify option)
    def checkPlacementRule(self, data):
        matrixSize = len(data.gameBoard)

        # if placementRule is adding object
        if data.placementRuleNum is 1:
            if type(data.placementRuleOption) is not int:   # if placementRule is 1, option must be integer
                return error.serverError

            direct = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [-1,1], [-1,-1], [1,-1]]
            checkSize = [0, 4, 8]

            try:
                row, col = [int(i) for i in data.message.split()]   # extract placement position

                if row < 0 or row >= matrixSize or col < 0 or col >= matrixSize:    # check placement position is in gameBoard
                    data.pos = [row, col]
                    return error.outOfRange

            except Exception as e:
                data.pos = [row, col]
                return error.outputError

            for i in range(checkSize[data.placementRuleOption]):    # check option for adding rule.
                tr, tc = row + direct[i][0], col + direct[i][1]
                if (tr < matrixSize and tr >= 0) and (tc < matrixSize and tc >= 0):
                    if data.gameBoard[tr][tc] > 0 and data.gameBoard[tr][tc] < 4:   # if it fits option rule, break for statement
                        break
            else:
                return error.missPosition

        # if placementRule is moving object
        elif data.placementRuleNum is 2:
            if type(data.placementRuleOption) is not list:  # if placementRule is 2, option must be list
                return error.serverError

            try:
                posData = data.message.split('>')
                pastRow, pastCol = [int(i) for i in posData[0].split()]
                row, col = [int(i) for i in posData[1].split()] # extract placement position

                if row < 0 or row >= matrixSize or col < 0 or col >= matrixSize:    # check placement position is in gameBoard
                    data.pos = [row, col]
                    return error.outOfRange

                rowMovingSize = abs(pastRow - row)
                colMovingSize = abs(pastCol - col)  # claculate object moving size

            except Exception as e:
                data.pos = [row, col]
                return error.outputError

            objectNum = data.gameBoard[pastRow][pastCol]
            if objectNum < 0 or objectNum > 3:
                data.pos = [row, col]
                return error.missPosition

            if rowMovingSize != data.placementRuleOption[objectNum - 1][0] or colMovingSize != data.placementRuleOption[objectNum - 1][1]:
                data.pos = [row, col]
                return error.missPosition

        else:
            return error.serverError

        try:
            if self.applyAllyExistRule(data, [row, col]):
                if self.applyEnemyExistRule(data, [row, col]):
                    if self.applyExtraExistRule(data, [row, col]):
                        data.pos = [row, col]
                        return data.pos

            return False

        except Exception as e:
            return error.serverError


    def applyAllyExistRule(self, data, pos):
        pass


    def applyEnemyExistRule(self, data, pos):
        pass


    def applyExtraExistRule(self, data, pos):
        pass


    def additionalExtraExistRule(self, data, pos):
        pass