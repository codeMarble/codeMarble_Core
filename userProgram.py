# -*- coding: utf-8 -*-
"""
    codeMarble_Core.userProgram
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
    :copyright: (c) 2017 by codeMarble
"""

import os
import time
import random
from execution import Execution


class UserProgram(object):
    def __init__(self, language, fileName, path):
        # parameter setting
        self.filePath = path
        self.language = language
        self.fileName = fileName
        self.executionName = "%s_%s" %(str(random.randint(1, 100)) + str(time.time())[0:3])

        self.compileMessage = {'c': ['/usr/bin/gcc', '/usr/bin/gcc', '-o'],
                               'c++': ['/usr/bin/g++', '/usr/bin/g++', '-std=c++11', '-o']}
        self.playMessage = {'c': ['./'+self.executionName, './'+self.executionName, '<'],
                            'c++': ['./'+self.executionName, './'+self.executionName, '<'],
                            'python': ['/usr/bin/python', '/usr/bin/python', './'+self.executionName, '<'],
                            'python3': ['/usr/bin/python3', '/usr/bin/python3', './'+self.executionName, '<']}

        # make execution object
        self.execution = Execution()

    def compile(self):
        # python is not compiled
        if 'python' in self.language:
            pass

        else:
            # compile parameter setting
            self.compileMessage[self.language].append(self.fileName)
            self.compileMessage[self.language].append(self.executionName)

            # compile with execution object & return result
            return self.execution.executeProgram(self.compileMessage[self.language])


    def play(self):
         # run program with execution object & return result
        return self.execution.executeProgram(self.playMessage[self.language])
