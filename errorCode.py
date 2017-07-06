# -*- coding: utf-8 -*-
"""
    codeMarble_Core.errorCode
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
    :copyright: (c) 2017 by codeMarble
"""

import os


class ErrorCode(object):
    def __init__(self):
        pass

    def missPosition(self):
        return 'miss position'

    def timeover(self):
        return 'time over'

    def outOfRange(self):
        return 'out of range'