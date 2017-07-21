# -*- coding: utf-8 -*-
"""
    codeMarble_Core.errorCode
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    error message class.
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

    def serverError(self, cmd=''):
        return 'server error ' + cmd