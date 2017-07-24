# -*- coding: utf-8 -*-
"""
    codeMarble_Core.endingRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    check and manage ending & winning rule.
    :copyright: (c) 2017 by codeMarble
"""

import os
from errorCode import ErrorCode

error = ErrorCode()


class EndingRule(object):
    def __init__(self):
        pass

    # endingRuleNum(1:checkRemove, 2:오목, 3:objectCount(돌 추가일때만))
    # endingRuleOption([objectNum, pivotCnt] or [direction, count])
    # objectNum:제거확인object, pivotCnt:기준개수(이하), direction:actionRule과 동일, count:정렬개수
    # me, you, draw, pass
    def checkEndingRule(self, data):
        # type check if statement
        # result, (pred, real) = data.isValidTypeData():
        # if not result:
        #     return ErrorCode.typeError(pred, real)

        if data.endingRuleNumber is 1:
            return self.checkRemoveObject(data)
        elif data.endingRuleNumber is 2:
            return self.checkGomoku(data)
        elif data.endingRuleNumber is 3:
            return self.checkCountObject(data)
        else:
            # return ErrorCode.valueError(data.endingRuleNumber)
            pass

    def checkRemoveObject(self, data):
        pivotObject, pivotCnt = data.endingRuleOption
        objectCnt = sum([gameBoardRow.count(pivotObject) for gameBoardRow in data.gameBoard])

        return objectCnt <= pivotCnt

    def checkGomoku(self, data):
        # [direction, count]
        gomokuDirection, gomokuCount = data.endingRuleOption

        def checkPlusLine():
            lines = [[data.gameBoard[i + k][j] for k in range(gomokuCount)] for j in range(len(data.gameBoard)) for i in
                     range(len(data.gameBoard) - gomokuCount + 1)]
            for line in lines:
                if len(set(line)) is 1:
                    return line[0]
            lines = [[data.gameBoard[i][j + k] for k in range(gomokuCount)] for j in range(len(data.gameBoard) - gomokuCount + 1) for i in
                     range(len(data.gameBoard))]
            for line in lines:
                if len(set(line)) is 1:
                    return line[0]

            return False

        def checkCrossLine():
            lines = [[data.gameBoard[i + k][j + k] for k in range(gomokuCount)] for j in range(len(data.gameBoard) - gomokuCount + 1) for i in
                     range(len(data.gameBoard) - gomokuCount + 1)]
            for line in lines:
                if len(set(line)) is 1:
                    return line[0]
            lines = [[data.gameBoard[i + k][j - k] for k in range(gomokuCount)] for j in range(len(data.gameBoard) - gomokuCount + 1) for i in
                     range(len(data.gameBoard))]
            for line in lines:
                if len(set(line)) is 1:
                    return line[0]

            return False

        def checkAllLine():
            return checkPlusLine() or checkCrossLine()

        result = {1: checkPlusLine, 2: checkCrossLine, 3: checkAllLine}
        try:
            return result[gomokuDirection]()
        except KeyError as e:
            # return ErrorCode.valueError()
            pass

    def checkCountObject(self, data):
        from collections import Counter
        objectCounter = Counter([object for gameBoardRow in data.gameBoard for object in gameBoardRow])

        if objectCounter[0] != 0:
            return "pass"

        object1, object2 = objectCounter.most_common(2)

        if object1[1] < object2[1]:
            return "me"
        elif object1[1] > object2[1]:
            return "you"
        else:
            return "draw"
