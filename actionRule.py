# -*- coding: utf-8 -*-
"""
    codeMarble_Core.actionRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
    :copyright: (c) 2017 by codeMarble
"""

import os
from errorCode import ErrorCode

error = ErrorCode()


class ActionRule(object):
    def __init__(self):
        pass


    # actionRuleNum(0:script, 1:remove, 2:change), actionRuleOption1(0:script, 1:4direction, 2:8direction, 3:go)
    # actionRuleOption2(0:othello, n:size)
    def checkActionRule(self, actionRuleNum, actionRuleOption1, actionRuleOption2, gameBoard, dataBoard, pos):
        pass


    def removeObject(self, actionRuleNum, actionRuleOption1, actionRuleOption2, gameBoard, dataBoard, pos):
        pass


    def changeObject(self, actionRuleNum, actionRuleOption1, actionRuleOption2, gameBoard, dataBoard, pos):
        pass
