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
    def __init__(self, userObjectCount, placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption,
                 isEnemyExistNum, enemyExistOption, isExtraExistNum, extraExistOption, actionRuleNum, actionRuleOption1,
                 actionRuleOption2, endingRuleNum, endingRuleOption, gameBoard, dataBoard):
        self.placementRuleNum = placementRuleNum
        self.placementRuleOption = placementRuleOption
        self.isAllyExistNum = isAllyExistNum
        self.allyExistOption = allyExistOption
        self.isEnemyExistNum = isEnemyExistNum
        self.enemyExistOption = enemyExistOption
        self.isExtraExistNum = isExtraExistNum
        self.extraExistOption = extraExistOption
        self.actionRuleNum = actionRuleNum
        self.actionRuleOption1 = actionRuleOption1
        self.actionRuleOption2 = actionRuleOption2
        self.endingRuleNum = endingRuleNum
        self.endingRuleOption = endingRuleOption
        self.userObjectCount = userObjectCount


        self.gameBoard = gameBoard
        self.dataBoard = dataBoard

        self.message = None
        self.pos = None
        self.postPos = None