# -*- coding: utf-8 -*-
"""
    codeMarble_Core.userProgram
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    manage user code information.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys
import time
import random


class UserProgram(object):
    def __init__(self, language, fileName, path):
        # parameter setting
        self.filePath = os.path.join(path, fileName)
        self.language = language
        self.executionName = "%s_%s" %(str(random.randint(1, 100)) + str(time.time())[2:5])

        self.compileMessage = {'c': ['/usr/bin/gcc', '/usr/bin/gcc', '-o'],
                               'c++': ['/usr/bin/g++', '/usr/bin/g++', '-std=c++11', '-o']}
        self.playMessage = {'c': ['./'+self.executionName, './'+self.executionName, '<'],
                            'c++': ['./'+self.executionName, './'+self.executionName, '<'],
                            'python': ['/usr/bin/python', '/usr/bin/python', './'+self.executionName, '<'],
                            'python3': ['/usr/bin/python3', '/usr/bin/python3', './'+self.executionName, '<']}

        # make execution object

    def compile(self):
        # python is not compiled
        if 'python' in self.language:
            pass

        else:
            # compile parameter setting
            self.compileMessage[self.language].append(self.filePath)
            self.compileMessage[self.language].append(self.executionName)

            # compile with execution object & return result
            return self.compileMessage[self.language]


    def play(self):
         # run program with execution object & return result
        return self.playMessage[self.language]
