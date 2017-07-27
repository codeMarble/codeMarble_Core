# -*- coding: utf-8 -*-
"""
    codeMarble_Core.gameManager
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    manage game process.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys
from copy import deepcopy

from execution import Execution
from gameData import GameData
from userProgram import UserProgram
from scriptTemplate import UserRule
from errorCode import *


class GameManager(object):
    def __init__(self, challenger, champion, placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption,
                 isEnemyExistNum, enemyExistOption, isExtraExistNum, extraExistOption, actionRuleNum, actionRuleOption1,
                 actionRuleOption2, endingRuleNum, endingRuleOption, limitTime, gameBoard, dataBoard, scriptPath=None,
                 problemIndex='scriptTemplate'):
        if type(challenger) is not UserProgram and type(champion) is not UserProgram:
            raise TypeError

        if scriptPath:
            sys.path.insert(0, scriptPath)
        exec 'from %s import UserRule' % (problemIndex)

        # parameter setting
        self.challenger = challenger
        self.champion = champion

        self.data = GameData(placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption, isEnemyExistNum,
                             enemyExistOption, isExtraExistNum, extraExistOption, actionRuleNum, actionRuleOption1,
                             actionRuleOption2, endingRuleNum, endingRuleOption, gameBoard, dataBoard)

        self.limitTime = limitTime

        self.positionData = ''
        self.boardData = ''

        # make rule and execution object
        self.rules = UserRule()
        self.execution = Execution()


    def playGame(self):
        flag = False    # Flase : champ turn, True: challenger turn
        userList = [[self.champion, 0], [self.challenger, 0]]

        self.compileUserCode()

        for _ in range(len(self.gameBoard)*len(self.gameBoard)*2):
            message, time, isSuccess = self.execution.executeProgram(userList[flag][0].play())  # run user program
            self.data.message = message

            if not isSuccess:
                userList[flag][1] += 1
                result = message

            else:
                result = self.rules.checkPlacementRule(self.data)

                if type(result) is not str:
                    originalGameBoard = deepcopy(self.data.gameBoard)
                    originalDataBoard = deepcopy(self.data.dataBoard)

                    result = self.rules.checkActionRule(self.data)

                    if type(result) is not str:
                        result = self.rules.checkEndingRule(self.data)

                        if type(result) is int and result:
                            if result is 1:
                                return 'win' if flag else 'lose'

                            elif result is 2:
                                return 'lose' if flag else 'win'

                            else:
                                return 'draw'

                if result == 'server error':
                    return SERVER_ERROR

                else:
                    userList[flag][1] += 1
                    self.data.gameBoard = deepcopy(originalGameBoard)
                    self.data.dataBoard = deepcopy(originalDataBoard)

            if userList[flag][1] > 2:
                return 'lose' if flag else 'win'

            # change boarad setting (champ <-> challenger)
            self.changePlayerNBoard(flag, result)
            flag = (not flag)

        return 'draw'


    def changePlayerNBoard(self, flag, result):
        if flag :   # if challenger
            for i in range(len(self.gameBoard)):
                for k in range(len(self.gameBoard[0])):
                    self.gameBoard[i][k] = -(self.gameBoard[i][k])

            self.addData(result)

        else:   # if champ
            self.addData(result)

            for i in range(len(self.gameBoard)):
                for k in range(len(self.gameBoard[0])):
                    self.gameBoard[i][k] = -(self.gameBoard[i][k])


    def addData(self, result):
        self.positionData += str(result) + '\n'

        temp = ''
        for line in self.gameBoard:
            for i in line:
                temp += (str(i) + ' ')

            temp += '\n'


    def compileUserCode(self):
        self.execution.executeProgram(self.challenger.compile())
        self.execution.executeProgram(self.champion.compile())
