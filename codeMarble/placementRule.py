# -*- coding: utf-8 -*-
"""
    codeMarble_Core.placementRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    extract placement position data from output message and apply placement rule.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys
from errorCode import ErrorCode

error = ErrorCode()


class PlacementRule(object):
    def __init__(self):
        self.objectNum = 0


    # placementRuleNum(1:add, 2:move), placementRuleOption(1or2: add option, [1or2, n1, n2]: move option)
    # isAllyExistNum, isEnemyExistNum, isExtraExistNum(1:don't placement, 2:remove), existOption(1or2or3:remove option)
    # userObjectCount(n)
    def checkPlacementRule(self, data):
        try:
            interResult = self.applyPlacementRule(data)
            destinationState = data.gameBoard[data.pos[0]][data.pos[1]]

            if abs(destinationState) > 3:
                self.applyExtraExistRule(data)

            elif destinationState > 0:
                self.applyAllyExistRule(data)

            elif destinationState < 0:
                self.applyEnemyExistRule(data)

            else:
                pass

            return interResult

        except Exception as e:
            return error.serverError()


    def applyPlacementRule(self,data):
        matrixSize = len(data.gameBoard)

        if not self.splitUserOutput(data):
            return error.outputError()

        # if placementRule is adding object
        if data.placementRuleNum is 1:
            if type(data.placementRuleOption) is not int:  # if placementRule is 1, option must be integer
                return error.serverError()

            direct = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [-1, -1], [1, -1]]
            checkSize = [0, 4, 8]

            try:
                row, col = data.pos
                if row < 0 or row >= matrixSize or col < 0 or col >= matrixSize:  # check placement position is in gameBoard
                    return error.outOfRange(row, col)

            except Exception as e:
                return error.outputError()

            for i in range(checkSize[data.placementRuleOption]):  # check option for adding rule.
                tr, tc = row + direct[i][0], col + direct[i][1]
                if (tr < matrixSize and tr >= 0) and (tc < matrixSize and tc >= 0):
                    if data.gameBoard[tr][tc] > 0 and data.gameBoard[tr][tc] < 4:  # if it fits option rule, break for statement
                        break
            else:
                return error.missPosition(row, col)

        # if placementRule is moving object
        elif data.placementRuleNum is 2:
            if type(data.placementRuleOption) is not list:  # if placementRule is 2, option must be list
                return error.serverError()

            try:
                pastRow, pastCol = data.pastPos
                row, col = data.pos

                if row < 0 or row >= matrixSize or col < 0 or col >= matrixSize:  # check placement position is in gameBoard
                    return error.outOfRange(row, col)

                rowMovingSize = abs(pastRow - row)
                colMovingSize = abs(pastCol - col)  # claculate object moving size

                if (not rowMovingSize) and (not colMovingSize):
                    return error.missPosition(row, col)

            except Exception as e:
                return error.outputError()

            # check the object to move
            if self.objectNum < 0 or self.objectNum > 3:
                return error.missPosition(row, col)

            # check the rule to move object
            if data.placementRuleOption[0] is 1:    # check move size each object's direction
                if data.placementRuleOption[1] is 1:    # ＋ dir
                    if not self.checkMovingDirction1(data, rowMovingSize, colMovingSize):
                        return error.missPosition(row, col)

                elif data.placementRuleOption[1] is 2:  # × dir
                    if not self.checkMovingDirction2(data, rowMovingSize, colMovingSize):
                        return error.missPosition(row, col)

                elif data.placementRuleOption[1] is 3:  # 8 dir
                    if (not self.checkMovingDirction1(data, rowMovingSize, colMovingSize)) and \
                        (not self.checkMovingDirction2(data, rowMovingSize, colMovingSize)):
                        return error.missPosition(row, col)

                else:
                    return error.serverError()

            elif data.placementRuleOption[0] is 2:  # check each object's move path and size
                if rowMovingSize != data.placementRuleOption[self.objectNum - 1][1] or \
                    colMovingSize != data.placementRuleOption[self.objectNum - 1][2]:
                    return error.missPosition(row, col)

            else:
                return error.serverError()

        else:
            return error.serverError()

        return True


    def applyAllyExistRule(self, data):
        if data.isAllyExist is 1:
            return error.missPosition(data.pos[0], data.pos[1])

        elif data.isAllyExist is 2:
            if data.allyExistOption is 1:
                data.gameBoard[data.pos[0]][data.pos[1]] = self.objectNum

            else:
                pass

        else:
            return error.serverError()

        return True


    def applyEnemyExistRule(self, data):
        if data.isEnemyExist is 1:
            return error.missPosition(data.pos[0], data.pos[1])

        elif data.isEnemyExist is 2: #remove
            if data.enemyExistOption is 1:  # delete enemy and not move object
                data.gameBoard[data.pos[0]][data.pos[1]] = 0

            elif data.enemyExistOption is 2:   # delete enemy and move object
                data.gameBoard[data.pos[0]][data.pos[1]] = self.objectNum
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

            else:   # delete all object
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

        else:
            error.serverError()

        return True


    def applyExtraExistRule(self, data):
        if data.isExtraExist is 1:
            return error.missPosition(data.pos[0], data.pos[1])

        elif data.isEnemyExist is 2:  # remove
            if data.enemyExistOption is 1:  # delete enemy and not move object
                data.gameBoard[data.pos[0]][data.pos[1]] = 0

            elif data.enemyExistOption is 2:  # delete enemy and move object
                data.gameBoard[data.pos[0]][data.pos[1]] = self.objectNum
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

            else:  # delete all object
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

        else:
            error.serverError()

        return True


    def splitUserOutput(self, data):
        try:
            if data.placementRuleNum is 1:
                if data.userObjectCount is 1:
                    data.pos = [int(i) for i in data.message.split()]
                    self.objectNum = 1

                else:
                    tempData = [int(i) for i in data.message.split()]
                    self.objectNum = tempData[0]
                    data.pos = tempData[1:]

            elif data.placementRuleNum is 2:
                posData = data.message.split('>')

                data.pastPos = [int(i) for i in posData[0].split()]
                data.pos = [int(i) for i in posData[1].split()]
                self.objectNum = data.gameBoard[data.pastPost[0]][data.pastPost[1]]

            else:
                return False

        except Exception as e:
            return False


    def checkMovingDirction1(self, data, rowMovingSize, colMovingSize):
        if rowMovingSize == data.placementRuleOption[2] or colMovingSize == data.placementRuleOption[1]:
            if rowMovingSize == colMovingSize:
                return False

            else:
                return True

        else:
            return False


    def checkMovingDirction2(self, data, rowMovingSize, colMovingSize):
        if rowMovingSize == colMovingSize:
            if rowMovingSize != data.placementRuleOption[2]:
                return False

            else:
                return True

        else:
            return False