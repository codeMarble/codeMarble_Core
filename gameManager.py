# -*- coding: utf-8 -*-
"""
    codeMarble_Core.gameManager
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    로그인 확인 데코레이터와 로그인 처리 모듈.
    :copyright: (c) 2017 by codeMarble
"""

import os
from execution import Execution


class gameManager(object):
    def __init__(self, challenger, champion, gameStyle, gameBoard):
        # parameter setting
        self.challenger = challenger
        self.champion = champion

        self.challengerTurnOverCnt = 0
        self.championTurnOverCnt = 0

        self.gameType = gameStyle[0]
        self.detailRule = gameStyle[1]
        self.range = gameStyle[2]
        self.gameBoard = gameBoard

        # make referee/execution object
        self._referee = referee.Referee(self.gameType, self.detailRule, self.range)
        self.execution = Exception()

        self.positionData = ''
        self.boardData = ''


    def playGame(self):
        flag = False    # Flase : champ turn, True: challenger turn
        userData = [[self.champion, self.championTurnOverCnt], [self.challenger, self.challengerTurnOverCnt]]

        while self.boradChacek():

            pos, userData[flag][1] = self.player(userData[flag][0], userData[flag][1])

            if userData[flag][1] > 2:
                return 'challenger' if flag else 'champion'

            # change boarad setting (champ <-> challenger)
            self.changePlayerNBoard(flag, pos)

            flag = (not flag)

        return self._referee.countObject(self.gameBoard)


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


    def player(self, player, turnOverCnt):
        pos, time, result = player.play()   # run user program

        if not result:  # if result is False
            turnOverCnt += 1

        else:
            try:
                data = [i for i in pos.split()]

                 # position check
                if self.gameBoard[int(data[0])][int(data[1])] is not 0: # wrong position
                    pos = 'position miss\n'
                    turnOverCnt += 1

                else:
                    self.gameBoard[data[0]][data[1]] = 1    # change number of position

                    self._referee.middleProcess(self.gameBoard, data)   # reset board & check game result

                    pos = '%s %s\n' % (data[0], data[1])

            except Execution as e:
                pass

        return pos, turnOverCnt


    def addData(self, pos):
        self.positionData += pos

        temp = ''

        for line in self.gameBoard:
            for i in line:
                temp += (str(i) + ' ')

            temp += '\n'