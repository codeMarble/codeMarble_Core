# -*- coding: utf-8 -*-
"""
    codeMarble_Core.gameManager
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    manage game process.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys


from execution import Execution
from gameData import GameData
from userProgram import UserProgram
from scriptTemplate import UserRule
from errorCode import ErrorCode


class GameManager(object):
    def __init__(self, challenger, champion, placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption,
                 isEnemyExistNum, enemyExistOption, isExtraExistNum, extraExistOption, actionRuleNum, actionRuleOption1,
                 actionRuleOption2, gameBoard, dataBoard, endingRuleNum, endingRuleOption, scriptPath, limitTime,
                 problemIndex='scriptTemplate'):
        if type(challenger) is not UserProgram and type(champion) is not UserProgram:
            raise TypeError

        sys.path.insert(0, scriptPath)
        exec 'from %s import UserRule' % (problemIndex)

        # parameter setting
        self.challenger = challenger
        self.champion = champion

        self.data = GameData(placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption, isEnemyExistNum,
                 enemyExistOption, isExtraExistNum, extraExistOption, actionRuleNum, actionRuleOption1, actionRuleOption2,
                 endingRuleNum, endingRuleOption, gameBoard, dataBoard)

        self.limitTime = limitTime

        self.positionData = ''
        self.boardData = ''

        # make rule and execution object
        self.rules = UserRule()
        self.execution = Exception()


    def playGame(self):
        flag = False    # Flase : champ turn, True: challenger turn
        userList = [[self.champion, 0], [self.challenger, 0]]

        for _ in range(len(self.gameBoard)*len(self.gameBoard)*2):
            message, time, isSuccess = userList[flag][0].play()  # run user program
            self.data.message = message

            if not isSuccess or time > self.limitTime:
                userList[flag][1] += 1
                result = message

            else:
                result = self.rules.checkPlacementRule(self.data)

                if type(result) is list:
                    self.data.pos = result

                    result = self.rules.checkActionRule(self.data)

                    if result.im_class is not ErrorCode:
                        result = self.rules.checkEndingRule(self.data)

                        if type(result) is str:
                            return result

                else:
                    userList[flag][1] += 1

            if userList[flag][1] > 2:
                return 'Win' if flag else 'Lose'

            # change boarad setting (champ <-> challenger)
            self.changePlayerNBoard(flag, result)
            flag = (not flag)

        return "Draw"


    def changePlayerNBoard(self, flag, pos):
        if flag :   # if challenger
            for i in range(len(self.gameBoard)):
                for k in range(len(self.gameBoard[0])):
                    self.gameBoard[i][k] = -(self.gameBoard[i][k])

            self.addData(pos)

        else:   # if champ
            self.addData(pos)

            for i in range(len(self.gameBoard)):
                for k in range(len(self.gameBoard[0])):
                    self.gameBoard[i][k] = -(self.gameBoard[i][k])


    def addData(self, pos):
        self.positionData += pos

        temp = ''

        for line in self.gameBoard:
            for i in line:
                temp += (str(i) + ' ')

            temp += '\n'