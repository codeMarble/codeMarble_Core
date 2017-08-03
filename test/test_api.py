#-*- encoding: utf-8 -*-
import copy
import pytest
from codeMarble import gameData
from codeMarble import placementRule

initBoard = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,1,-1,0,0,0],
             [0,0,0,-1,1,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]

# placementRuleNum(1:add, 2:move), placementRuleOption1(1or2or3), placementRuleOption2([[n1, n2],...] or none: move option)
# existRuleNum([ally, enemy, extra], 1or2), existRuleOption([ally, enemy, extra], 1or2or3)
# userObjectCount(n)
# actionRuleNum(0:script, 1:remove, 2:change), actionRuleOption1(0:script, 1:＋dir, 2:×dir, 3:8dir, 4:go)
# actionRuleOption2(0:othello, n:size)
# endingRuleNum(1:checkRemove, 2:gomoku, 3:objectCount(only add))
# endingRuleOption([objectNum, pivotCnt] or [direction, count])
# objectNum:check del object, pivotCnt:pivotCount(<=), direction:==actionRule, count:count
# 1(me), 2(you), 3(draw), 0(pass)

def checkPlacementRule(data):
    testObject = placementRule.PlacementRule()
    outputMessage = ['2 4', '1 2 4', '3 3 > 2 4']

    data.message, data.userObjectCount, data.placementRuleNum = '2 4', 1, 1
    data.placementRuleOption1, data.placementRuleOption2 = 1, None

    assert True == testObject.applyPlacementRule(data) and data.pos == [2, 4] and \
           data.gameBoard == [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,1,0,0,0], [0,0,0,1,-1,0,0,0], [0,0,0,-1,1,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]



def checkActionRule(data):
    pass


def checkEndingRule(data):
    pass


if __name__ == '__main__':
    data = gameData.GameData(1, 1, 1, [[1,1],[2,1]], [1, 1, 1, 1], [1, 1, 1, 1], 1, 1, 1, 2, [1, 4],
                             copy.deepcopy(initBoard), copy.deepcopy(initBoard))

    checkPlacementRule(data)
    checkActionRule(data)
    checkEndingRule(data)

#userObjectCount, placementRuleNum, placementRuleOption1, placementRuleOption2, existRuleNum,
#existRuleOption, actionRuleNum, actionRuleOption1, actionRuleOption2, endingRuleNum, endingRuleOption,
#gameBoard, dataBoard