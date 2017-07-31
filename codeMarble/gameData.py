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
    def __init__(self, userObjectCount, placementRuleNum, placementRuleOption1, placementRuleOption2, existRuleNum,
                 existRuleOption, actionRuleNum, actionRuleOption1, actionRuleOption2, endingRuleNum, endingRuleOption,
                 gameBoard, dataBoard):
        self.placementRuleNum = placementRuleNum    # int
        self.placementRuleOption1 = placementRuleOption1    # int
        self.placementRuleOption2 = placementRuleOption2    # [[n1, n2],..]
        self.existRuleNum = existRuleNum    # [n1,n2,n3], n=1or2
        self.existRuleOption = existRuleOption    # [n1,n2,n3], 1<=n<=3
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

        self.checkDataType()


    def resetData(self):
        self.message = None
        self.objectNum = None
        self.pos = None
        self.postPos = None


    def checkDataType(self):
        intList = [self.placementRuleNum, self.placementRuleOption1,self.actionRuleNum, self.actionRuleOption1,
                   self.actionRuleOption2, self.endingRuleNum, self.userObjectCount]

        lst2dList = [self.existRuleNum, self.existRuleOption, self.placementRuleOption2, self.endingRuleOption]
        squareList = [self.gameBoard, self.dataBoard]

        if not all(type(var) is int for var in intList) or \
                not all(type(var) is list and var and type(var[0]) is list for var in lst2dList) or \
                not all(type(var) is list and var and type(var[0]) is list and len(var) == len(var[0]) for var in squareList):
            return False

        return True