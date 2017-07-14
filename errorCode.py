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

    def missPosition(self, row, col):
        return 'miss position(%d, %d)' % (row, col)

    def outOfRange(self, row, col):
        return 'out of range(%d, %d)' % (row, col)

    def timeover(self):
        return 'time over'

    def outputError(self):
        return 'output '

    def typeError(self):
        return 'not correct type'

    def serverError(self):
        return 'server error'