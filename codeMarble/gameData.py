# -*- coding: utf-8 -*-
"""
    codeMarble_Core.userProgram
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys

class GameData(object):
    def __init__(self, userObjectCount, placementRuleNum, placementRuleOption1, placementRuleOption2, isAllyExistNum,
                 allyExistOption, isEnemyExistNum, enemyExistOption, isExtraExistNum, extraExistOption, actionRuleNum,
                 actionRuleOption1, actionRuleOption2, endingRuleNum, endingRuleOption, gameBoard, dataBoard):
        self.placementRuleNum = placementRuleNum    # int
        self.placementRuleOption1 = placementRuleOption1    # int
        self.placementRuleOption2 = placementRuleOption2    # [[n1, n2],..]
        self.isAllyExistNum = isAllyExistNum    # int
        self.allyExistOption = allyExistOption    # int
        self.isEnemyExistNum = isEnemyExistNum    # int
        self.enemyExistOption = enemyExistOption    # int
        self.isExtraExistNum = isExtraExistNum    # int
        self.extraExistOption = extraExistOption    # int
        self.actionRuleNum = actionRuleNum    # int
        self.actionRuleOption1 = actionRuleOption1    # int
        self.actionRuleOption2 = actionRuleOption2    # int
        self.endingRuleNum = endingRuleNum    # int
        self.endingRuleOption = endingRuleOption    # [n1, n2]
        self.userObjectCount = userObjectCount    # int

        self.gameBoard = gameBoard    # [[n * k] * k]
        self.dataBoard = dataBoard    # [[n * k] * k]

        self.message = None    # None
        self.objectNum = None    # None
        self.pos = None    # None
        self.postPos = None    # None


    def resetData(self):
        self.message = None
        self.objectNum = None
        self.pos = None
        self.postPos = None


    def checkDataType(self):
        pass # return true/false