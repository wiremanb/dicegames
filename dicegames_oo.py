# -*- coding: utf-8 -*-
"""
Application Name: Dice Games
Author:           Benjamin Wireman
Date Created:     2017-03-30
Last Edited By:   Benjamin Wireman
Last Edited Date: 2017-03-30
Description:      This application allows two players to play their choice of the games Fifty or Pig.
Python Version:   2.7
"""

import random

class Player:
    _name=None
    _score=None
    _firstRoll=None

    def __init__(self, name):
        self._name = name
        self._score = 0
        self._firstRoll = True

    def getName(self):
        return self._name

    def getScore(self):
        return self._score

    def getFirstRoll(self):
        return self._firstRoll

    def setName(self, name):
        self._name = name

    def setScore(self, score):
        self._score = score

    def setFirstRoll(self, firstRoll):
        self._firstRoll = firstRoll

class Game:
    _gameType=None
    _numberOfPlayers=None
    _players=[]
    _winningScore=None
    _currentPlayer=None
    _nextPlayer=None

    def __init__(self, type, players, winningScore):
        self._gameType = type
        self._numberOfPlayers = len(players)
        self._players = players
        self._winningScore = winningScore
        self._currentPlayer = self._players[0]
        self._nextPlayer = self._players[1]

    def getPlayers(self):
        return self._players

    """
    Print the options for the current game
    """
    def printGameMenu(self):
        print "1. Roll (r)\n" \
              "2. Score (s)\n" \
              "3. Game Description (d)\n" \
              "4. Game Instructions (i)\n" \
              "5. Pass (p) - only available in Pig\n" \
              "6. Quit (q)\n"

    """
    Print the description for the current game
    """
    def printGameDescription(self):
        print "Description: "
        if self._gameType == "Fifty":
            print "The goal of Fifty is to be the first player to reach {0} points. You get points by rolling doubles.\n".format(self._winningScore)

        else:
            print "The goal of Pig is to be the first player to reach {0} points. You get points by rolling a single ".format(self._winningScore)
            print "die multiple times and adding the value on each roll of the die to your current score.\n"

    """
    Print the instructions for the current game
    """
    def printGameInstructions(self):
        print "Instructions: "
        if self._gameType == "Fifty":
            print "A turn consists of a player rolling a pair of dice (with the goal of rolling doubles), "
            print "and scoring the roll as described below. Play continues with each player taking one roll per turn. "
            print "The first player to score {0} or more points is declared the winner.".format(self._winningScore)
            print "All doubles except 3s and 6s score 5 points. Double 6s are worth 25 points. "
            print "Double 3s wipe out the player’s entire score, and the player must start again at 0. "
            print "Non-double rolls are 0 points.\n"

        else:
            print "The first player rolls the die as many times as they want. The value of each throw is added onto the "
            print "score until the player decides to end his turn and passes the die to the next player. Play continues until one player reaches {0}.".format(self._winningScore)
            print "The value of each throw is added to the current player’s score. If the player rolls a 1, "
            print "the player’s score goes back to 0, and their turn ends. At one extreme, any player who gets a 1 on "
            print "the first roll is immediately out. At the other extreme, the first player could theoretically reach "
            print "the winning score on the first turn, as long as they don’t roll a 1. If the player succeeds, "
            print "the game ends there.\n"

    def printScores(self):
        print "-----Current Scores-----\n" \
              "Player 1: {0}\n" \
              "Player 2: {1}\n" \
              "------------------------\n".format(self._players[0].getScore(), self._players[1].getScore())

    def resetGame(self):
        self._players[0].setScore(0)
        self._players[0].setFirstRoll(True)
        self._players[1].setScore(0)
        self._players[1].setFirstRoll(True)
        self._currentPlayer = self.getPlayers()[0]
        self._nextPlayer = self.getPlayers()[1]

    """
    Role die or dice depending on which game it is
    """
    def roleDice(self, num):
        if num == 2:
            return [random.randint(1, 6), random.randint(1, 6)]

        else:
            return random.randint(1, 6)

    """
    Based on the role of the die and the current game, this function will
    evaluate the values of the die or dice and determine what needs to happen
    to the current player
    """
    def evaluateDieValues(self, values):
        if self._gameType == "Fifty":
            if values[0] == values[1] and values[0] == 6:
                self._currentPlayer.setScore(self._currentPlayer.getScore()+25)

            elif values[0] == values[1] and values[0] == 3:
                self._currentPlayer.setScore(-99)

            elif values[0] == values[1]:
                self._currentPlayer.setScore(self._currentPlayer.getScore()+5)

            print "{0} rolled -> {1}, {2}".format(self._currentPlayer.getName(), values[0], values[1])

        elif self._gameType == "Pig":
            if values == 1 and self._currentPlayer.getScore() == 0 and self._currentPlayer.getFirstRoll() is True:
                self._currentPlayer.setScore(-99)

            elif values == 1 and self._currentPlayer.getFirstRoll() is False:
                self._currentPlayer.setScore(0)

            else:
                self._currentPlayer.setScore(self._currentPlayer.getScore()+values)
                self._currentPlayer.setFirstRoll(False)

            print "{0} Rolled: {1}".format(self._currentPlayer.getName(), values)

        else:
            pass

    """
    A quick way to keep track of the current player
    """
    def swapPlayers(self):
        tmp = self._currentPlayer
        self._currentPlayer = self._nextPlayer
        self._nextPlayer = tmp

    def playGame(self):
        self.printGameDescription()
        self.printGameInstructions()
        self.printGameMenu()
        exitGame = False
        while exitGame is False:
            userInput = raw_input("{0} >> ".format(self._currentPlayer.getName()))
            print

            if userInput == "Roll" or userInput == "roll" or userInput == "r":
                if self._gameType == "Fifty":
                    self.evaluateDieValues(self.roleDice(2))
                    if self._currentPlayer.getScore() >= int(self._winningScore):
                        print "\nCONGRATULATIONS {0}!!! YOU WON!!!!\n".format(self._currentPlayer.getName())
                        self.printScores()
                        print
                        exitGame = True

                    elif self._currentPlayer.getScore() == -99:
                        print "\n{0} rolled a pair of 3s... your score is now 0! Better luck next time! :(\n".format(self._currentPlayer.getName())
                        self._currentPlayer.setScore(0)

                    else:
                        print "{0} score: {1}\n".format(self._currentPlayer.getName(), self._currentPlayer.getScore())
                        self.swapPlayers()

                else:  # Else the game is Pig
                    self.evaluateDieValues(self.roleDice(1))
                    if self._currentPlayer.getScore() >= int(self._winningScore):
                        print "\nCONGRATULATIONS {0}!!! YOU WON!!!!\n".format(self._currentPlayer.getName())
                        self.printScores()
                        print
                        exitGame = True
                    elif self._currentPlayer.getScore() == 0:
                        print "\n{0} rolled a 1.. your score is now 0! Better luck next time! :(\n".format(self._currentPlayer.getName())
                        self.swapPlayers()
                    elif self._currentPlayer.getScore() == -99:
                        print "\n{0} rolled a 1 on the first try!! Your luck is the worst I have ever seen. GAME OVER!!!!! XD\n".format(self._currentPlayer.getName())
                        exitGame = True
                    else:
                        print "\n{0} score: {1}\n".format(self._currentPlayer.getName(), self._currentPlayer.getScore())

            elif userInput == "Score" or userInput == "score" or userInput == "s":
                self.printScores()

            elif userInput == "\nDescription" or userInput == "description" or userInput == "d":
                self.printGameDescription()

            elif userInput == "Instructions" or userInput == "instructions" or userInput == "i":
                self.printGameInstructions()

            elif userInput == "Pass" or userInput == "pass" or userInput == "p" and self._gameType == "Pig":
                print "{0} decided to pass. {1} it is your turn!\n".format(self._currentPlayer.getName(), self._nextPlayer.getName())
                self.swapPlayers()

            elif userInput == "Quit" or userInput == "quit" or userInput == "q":
                exitGame = True

            else:
                print "[!] -> That is not the correct input... try again!\n"

"""
Print games from which the players can choose
"""
def printMenu():
    print "1. Fifty (f)\n" \
          "2. Pig (p)\n" \
          "3. Menu (m)\n" \
          "4. Quit (q)\n"

def main():
    quit = False
    while quit is False:
        printMenu()
        userInput = raw_input("Which game would you like to play? ")
        if userInput == "Fifty" or userInput == "fifty" or userInput == "f":
            print "You have chosen to play the game Fifty. May the odds be ever in your favor!\n"
            gameValue = raw_input("To what point value would you like to play? ")
            fifty = Game("Fifty", [Player("Player 1"), Player("Player 2")], gameValue)
            fifty.playGame()
            fifty.resetGame()

        elif userInput == "Pig" or userInput == "pig" or userInput == "p":
            print "You have chosen to play the game Pig. Please, do your best to avoid 1.\n"
            gameValue = raw_input("To what point value would you like to play? ")
            pig = Game("Pig", [Player("Player 1"), Player("Player 2")], gameValue)
            pig.playGame()
            pig.resetGame()

        elif userInput == "Menu" or userInput == "menu" or userInput == "m":
            continue

        elif userInput == "Quit" or userInput == "quit" or userInput == "q":
            print "We HATE to see you leave! Come back soon!! :D"
            quit = True

        else:
            print "That is not the correct input... try again!\n"

if __name__ == "__main__":
    main()