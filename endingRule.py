# -*- coding: utf-8 -*-
"""
    codeMarble_Core.endingRule
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
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
        pass