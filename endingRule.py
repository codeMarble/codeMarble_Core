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


    def checkEndingRule(self, endingRuleNum, placementRuleNum=None, endingRuleOption=None):
        pass


    # 다음 착수 가능 확인(placementRuleNum==1), 오브젝트 제거(endingRuleNum==1), 오목 규칙(endingRuleNum==2), 돌 개수(endingRuleNum==3)
    # 오브젝트 제거(endingRuleOption==제거 오프젝트 번호(int)), 오목 규칙(endingRuleOption==[direction, 개수](list))
    # 4방(direction==1), 8방(direction==2)