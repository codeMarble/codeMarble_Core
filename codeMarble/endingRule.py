# -*- coding: utf-8 -*-
"""
    codeMarble_Core.endingRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    check and manage ending & winning rule.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys

from errorCode import *


class EndingRule(object):
    def __init__(self):
        self.result = {'pass': 0, 'me': 1, 'you': 2, 'draw': 3}

    # endingRuleNum(1:checkRemove, 2:gomoku, 3:objectCount(돌 추가일때만))
    # endingRuleOption([objectNum, pivotCnt] or [direction, count])
    # objectNum:제거확인object, pivotCnt:pivotCount(<=), direction:actionRule과 동일, count:정렬개수
    # me, you, draw, pass
    def checkEndingRule(self, data):
        if data.endingRuleNumber is 1:
            return self.checkRemoveObject(data)
        elif data.endingRuleNumber is 2:
            return self.checkGomoku(data)
        elif data.endingRuleNumber is 3:
            return self.checkCountObject(data)
        else:
            return GAME_ERROR

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
            directions = [[-1, 0], [1, 0], [0, 1], [0, -1], [-1, 1], [1, 1], [1, -1], [-1, -1]]
        else:
            return GAME_ERROR

        # me, you, draw, pass
        for direction in directions:
            di, dj = direction
            try:
                for k in range(gomokuCount):
                    if data.gameBoard[pi][pj] != data.gameBoard[pi + di * k][pj + dj * k]:
                        break
                # return who is winner
                else:
                    return self.result['me'] if data.gameBoard[pi][pj] > 0 else self.result['you']
            # out of range
            except Exception as e:
                continue

        if self.checkCountObject(data) == self.result['draw']:
            return self.result['draw']
        else:
            return self.result['pass']

    def checkCountObject(self, data):
        from collections import Counter
        objectCounter = Counter([object for gameBoardRow in data.gameBoard for object in gameBoardRow])

        if objectCounter[0] != 0:
            return self.result['pass']

        object1, object2 = objectCounter.most_common(2)

        if object1[1] < object2[1]:
            return self.result['me']
        elif object1[1] > object2[1]:
            return self.result['you']
        else:
            return self.result['draw']
