# -*- coding: utf-8 -*-
"""
    codeMarble_Core.gameManager
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
    :copyright: (c) 2017 by codeMarble
"""

import os
import sys
from execution import Execution
from userProgram import UserProgram
from scriptTemplate import UserRule
from errorCode import ErrorCode


class GameManager(object):
    def __init__(self, challenger, champion, placementRuleNum, placementRuleOption, isAllyExistNum, allyExistOption,
                 isEnemyExistNum, enemyExistOption, isExtraExistNum, extraExistOption, actionRuleNum, actionRuleOption,
                 gameBoard, dataBoard, endingRuleNum, endingRuleOption, scriptPath, limitTime, problemIndex='scriptTemplate'):
        if type(challenger) is not UserProgram and type(champion) is not UserProgram:
            raise TypeError

        sys.path.insert(0, scriptPath)
        exec 'from %s import UserRule' % (problemIndex)

        # parameter setting
        self.challenger = challenger
        self.champion = champion

        self.placementRuleNum = placementRuleNum
        self.placementRuleOption = placementRuleOption
        self.isAllyExistNum = isAllyExistNum
        self.allyExistOption = allyExistOption
        self.isEnemyExistNum = isEnemyExistNum
        self.enemyExistOption = enemyExistOption
        self.isExtraExistNum = isExtraExistNum
        self.extraExistOption = extraExistOption
        self.actionRuleNum = actionRuleNum
        self.actionRuleOption = actionRuleOption
        self.endingRuleNum = endingRuleNum
        self.endingRuleOption = endingRuleOption
        self.gameBoard = gameBoard
        self.dataBoard = dataBoard
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
            pos, time, isSuccess = userList[flag][0].play()  # run user program

            if not isSuccess or time > self.limitTime:
                userList[flag][1] += 1

            else:
                if self.rules.checkPlacementRule(self.placementRuleNum, self.placementRuleOption, self.isAllyExistNum,
                                                 self.allyExistOption, self.isEnemyExistNum, self.enemyExistOption,
                                                 self.isExtraExistNum, self.extraExistOption, self.gameBoard,
                                                 self.dataBoard, pos).im_class is not ErrorCode:

                    if self.rules.checkActionRule(self.actionRuleNum, self.actionRuleOption, self.gameBoard,
                                                  self.dataBoard, pos).im_class is not ErrorCode:
                        result = self.rules.checkEndingRule(self.endingRuleNum, self.placementRuleNum, self.endingRuleOption, pos)

                        if type(result) is str:
                            return result

                else:
                    userList[flag][1] += 1

            if userList[flag][1] > 2:
                return 'Win' if flag else 'Lose'

            # change boarad setting (champ <-> challenger)
            self.changePlayerNBoard(flag, pos)
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