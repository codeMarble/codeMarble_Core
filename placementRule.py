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
    def checkPlacementRule(self, placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption, isEnemyExistNum,
                           enemyExistOption, isExtraExistNum, extraExistOption, gameBoard, dataBoard, message):
        matrixRange = len(gameBoard)

        if placementRuleNum is 1:
            if type(placementRuleOption) is not int:
                return error.serverError()

            direct = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [-1,1], [-1,-1], [1,-1]]
            checkSize = 4 if placementRuleOption is 1 else 8

            try:
                row, col = [int(i) for i in message.split()]

            except Exception as e:
                return error.outputError

            for i in range(checkSize):
                tr, tc = row + direct[i][0], col + direct[i][1]
                if (tr < matrixRange and tr >= 0) and (tc < matrixRange and tc >= 0):
                    if gameBoard[tr][tc] > 0 and gameBoard[tr][tc] < 4:
                        break
            else:
                return error.missPosition(row, col)

        elif placementRuleNum is 2:
            if type(placementRuleOption) is not list:
                return error.serverError()

            try:
                posData = message.split('>')
                row1, col1 = [int(i) for i in posData[0].split()]
                row2, col2 = [int(i) for i in posData[1].split()]

            except Exception as e:
                return error.outputError

        else:
            return error.serverError

        try:
            if self.applyAllyExistRule(placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption, isEnemyExistNum,
                                       enemyExistOption, isExtraExistNum, extraExistOption, gameBoard, dataBoard, [row, col]):
                if self.applyEnemyExistRule(placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption,
                                            isEnemyExistNum, enemyExistOption, isExtraExistNum, extraExistOption, gameBoard, dataBoard, [row, col]):
                    if self.applyExtraExistRule(placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption,
                                                isEnemyExistNum, enemyExistOption, isExtraExistNum, extraExistOption, gameBoard, dataBoard, [row, col]):
                        return [row, col]

            return False

        except Exception as e:
            return error.serverError


    def applyAllyExistRule(self, placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption, isEnemyExistNum,
                           enemyExistOption, isExtraExistNum, extraExistOption, gameBoard, dataBoard, pos):
        pass


    def applyEnemyExistRule(self, placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption, isEnemyExistNum,
                            enemyExistOption, isExtraExistNum, extraExistOption, gameBoard, dataBoard, pos):
        pass


    def applyExtraExistRule(self, placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption, isEnemyExistNum,
                            enemyExistOption, isExtraExistNum, extraExistOption, gameBoard, dataBoard, pos):
        pass


    def additionalExtraExistRule(self, placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption, isEnemyExistNum,
                                 enemyExistOption, isExtraExistNum, extraExistOption, gameBoard, dataBoard, pos):
        pass