# -*- coding: utf-8 -*-
"""
    codeMarble_Core.placementRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    extract placement position data from output message and apply placement rule.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys

from errorCode import *


class PlacementRule(object):
    def __init__(self):
        pass


    # placementRuleNum(1:add, 2:move), placementRuleOption1(1or2or3), placementRuleOption2([[n1, n2],...] or none: move option)
    # existRuleNum([ally, enemy, extra], 1or2), existRuleOption([ally, enemy, extra], 1or2or3)
    # userObjectCount(n)
    def checkPlacementRule(self, data):
        try:
            interResult = self.applyPlacementRule(data)
            destinationState = data.gameBoard[data.pos[0]][data.pos[1]]

            if abs(destinationState) > 3:
                self.applyExtraExistRule(data)

            elif destinationState > 0:
                self.applyAllyExistRule(data)

            else:
                self.applyEnemyExistRule(data)

            return interResult

        except Exception as e:
            return SERVER_ERROR


    def applyPlacementRule(self,data):
        matrixSize = len(data.gameBoard)

        if not self.splitUserOutput(data):
            return OUTPUT_ERROR

        try:
            row, col = data.pos
            if row < 0 or row >= matrixSize or col < 0 or col >= matrixSize:  # check placement position is in gameBoard
                return OUT_OF_RANGE + '(%d,%d)' % (row, col)

        except Exception as e:
            return OUTPUT_ERROR

        # if placementRule is adding object
        if data.placementRuleNum is 1:
            direct1 = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            direct2 = [[1, 1], [-1, 1], [-1, -1], [1, -1]]



            if data.placementRuleOption1 < 3:
                direct = direct1 if data.placementRuleOption is 1 else direct2

            else:
                direct = direct1 + direct2

            for dRow, dCol in direct:  # check option for adding rule.
                tr, tc = row + dRow, col + dCol
                if (tr < matrixSize and tr >= 0) and (tc < matrixSize and tc >= 0):
                    if data.gameBoard[tr][tc] > 0 and data.gameBoard[tr][tc] < 4:  # if it fits option rule, break for statement
                        break
            else:
                return MISS_POSITION + '(%d,%d)'%(row, col)

        # if placementRule is moving object
        elif data.placementRuleNum is 2:
            try:
                pastRow, pastCol = data.pastPos

                rowMovingSize = abs(pastRow - row)
                colMovingSize = abs(pastCol - col)  # calculate object moving size

                if (not rowMovingSize) and (not colMovingSize):
                    return MISS_POSITION + '(%d,%d)'%(row, col)

            except Exception as e:
                return OUTPUT_ERROR

            # check the object to move
            if data.objectNum < 0 or data.objectNum > 3:
                return MISS_POSITION + '(%d,%d)'%(row, col)

            # check the rule to move object
            if data.placementRuleOption1 < 3:    # check move size each object's direction
                if data.placementRuleOption2[data.objectNum - 1][0] is 1:    # ＋ dir
                    if not self.checkMovingDirction1(data, rowMovingSize, colMovingSize):
                        return MISS_POSITION + '(%d,%d)'%(row, col)

                elif data.placementRuleOption2[data.objectNum - 1][0] is 2:  # × dir
                    if not self.checkMovingDirction2(data, rowMovingSize, colMovingSize):
                        return MISS_POSITION + '(%d,%d)'%(row, col)

                elif data.placementRuleOption2[data.objectNum - 1][0] is 3:  # 8 dir
                    if (not self.checkMovingDirction1(data, rowMovingSize, colMovingSize)) or \
                        (not self.checkMovingDirction2(data, rowMovingSize, colMovingSize)):
                        return MISS_POSITION + '(%d,%d)'%(row, col)

                else:
                    return GAME_ERROR

            else:  # check each object's move path and size
                if rowMovingSize != data.placementRuleOption2[data.objectNum - 1][0] or \
                    colMovingSize != data.placementRuleOption2[data.objectNum - 1][1]:
                    return MISS_POSITION + '(%d,%d)'%(row, col)

        else:
            return SERVER_ERROR

        return True


    def applyAllyExistRule(self, data):
        if data.existRuleNum[0] is 1:
            return MISS_POSITION + '(%d,%d)'%(data.pos[0], data.pos[1])

        elif data.existRuleNum[0] is 2:
            if data.existRuleOption[0] is 1:
                data.gameBoard[data.pos[0]][data.pos[1]] = data.objectNum

            else:
                pass

        else:
            return SERVER_ERROR

        return True


    def applyEnemyExistRule(self, data):
        if data.existRuleNum[1] is 1:
            return MISS_POSITION + '(%d,%d)'%(data.pos[0], data.pos[1])

        elif data.existRuleNum[1] is 2: #remove
            if data.existRuleOption[1] is 1:  # delete enemy and not move object
                data.gameBoard[data.pos[0]][data.pos[1]] = 0

            elif data.existRuleOption[1] is 2:   # delete enemy and move object
                data.gameBoard[data.pos[0]][data.pos[1]] = data.objectNum
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

            else:   # delete all object
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

        else:
            return GAME_ERROR

        return True


    def applyExtraExistRule(self, data):
        if data.existRuleNum[2] is 1:
            return MISS_POSITION + '(%d,%d)'%(data.pos[0], data.pos[1])

        elif data.existRuleNum[2] is 2:  # remove
            if data.existRuleOption[2] is 1:  # delete enemy and not move object
                data.gameBoard[data.pos[0]][data.pos[1]] = 0

            elif data.existRuleOption[2] is 2:  # delete enemy and move object
                data.gameBoard[data.pos[0]][data.pos[1]] = data.objectNum
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

            else:  # delete all object
                data.gameBoard[data.pastPos[0]][data.pastPos[1]] = 0

        else:
            return GAME_ERROR

        return True


    def splitUserOutput(self, data):
        try:
            if data.placementRuleNum is 1:
                if data.userObjectCount is 1:
                    data.pos = [int(i) for i in data.message.split()]
                    data.objectNum = 1

                else:
                    tempData = [int(i) for i in data.message.split()]
                    data.objectNum = tempData[0]
                    data.pos = tempData[1:]

            elif data.placementRuleNum is 2:
                posData = data.message.split('>')

                data.pastPos = [int(i) for i in posData[0].split()]
                data.pos = [int(i) for i in posData[1].split()]
                data.objectNum = data.gameBoard[data.pastPost[0]][data.pastPost[1]]

            else:
                return False

        except Exception as e:
            return False


    def checkMovingDirction1(self, data, rowMovingSize, colMovingSize):
        totalSize = rowMovingSize + colMovingSize

        if totalSize == rowMovingSize or totalSize == colMovingSize:
            if data.placementRuleOption1 is 1:
                if rowMovingSize != data.placementRuleOption2[data.objectNum - 1][1] and \
                    colMovingSize != data.placementRuleOption2[data.objectNum - 1][1]:
                        return False

            else:
                if data.placementRuleOption2[data.objectNum - 1][1]:
                    posList = zip(range(data.postPos[0]+1, data.pos[0]), [data.postPos[1]]*(totalSize-1)) if totalSize == rowMovingSize \
                              else zip([data.postPos[0]]*totalSize, range(data.postPos[1]+1, data.pos[1]+1))

                    for tRow, tCol in posList:
                        if -4 < data.gameBoard[tRow][tCol] < 0:
                            return False
        return True


    def checkMovingDirction2(self, data, rowMovingSize, colMovingSize):
        if data.placementRuleOption1 is 1:
            if rowMovingSize != colMovingSize or rowMovingSize != data.placementRuleOption2[data.objectNum - 1][1]:
                return False

        else:
            if data.placementRuleOption2[data.objectNum - 1][1]:
                for tRow, tCol in zip(range(data.postPos[0], data.pos[0]), range(data.postPos[1], data.pos[1])):
                    if tRow == data.postPos[0]:
                        continue

                    elif -4 < data.gameBoard[tRow][tCol] < 0:
                        return False

        return True
