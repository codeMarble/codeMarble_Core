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

        pi, pj = data.pos

        if gomokuDirection is 1:
            directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        elif gomokuDirection is 2:
            directions = [[-1, 1], [1, 1], [-1, 1], [-1, -1]]
        elif gomokuDirection is 3:
            directions = [[-1, 0], [1, 0], [0, 1], [0, -1], [-1, 1], [1, 1], [-1, 1], [-1, -1]]
        else:
            # return ErrorCode.valueError(gomokuDirection)
            return False

        # me, you, draw, pass
        for direction in directions:
            di, dj = direction
            try:
                for k in range(gomokuCount):
                    if data.gameBoard[pi][pj] != data.gameBoard[pi + di * k][pj + dj * k]:
                        break
                # return who is winner
                else:
                    return "me" if data.gameBoard[pi][pj] > 0 else "you"
            # out of range
            except Exception as e:
                continue

        if self.checkCountObject(data) == "draw":
            return "draw"
        else:
            return "pass"

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
