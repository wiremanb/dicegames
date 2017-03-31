# -*- coding: utf-8 -*-
"""
Application Name: Dice Games
Author:           Benjamin Wireman
Date Created:     2017-03-27
Class/Section:    CS 424 02
Last Edited By:   Benjamin Wireman
Last Edited Date: 2017-03-27
Description:      This application allows two players to play their choice of the games Fifty or Pig.
Python Version:   2.7
"""

import random

_playerScores = {"Player 1" : [0, True], "Player 2" : [0, True]} # Keep track of player scores and if it is a first roll
_currentPlayer = None # Keep track of the current player
_nextPlayer = None # Keep track of the next player in line
_currentGame = None # Keep track of the current game being played
_winningValue = 0 # Set the winning value of the game

"""
Print games from which the players can choose
"""
def printGameChoices():
    print "1. Fifty (f)\n" \
          "2. Pig (p)\n" \
          "3. Menu (m)\n" \
          "4. Quit (q)\n"

"""
Print the description for the current game
"""
def printGameDescription(opt):
    print "Description: "
    if opt == "Fifty":
        print "The goal of Fifty is to be the first player to reach {0} points. You get points by rolling doubles.\n".format(_winningValue)

    else:
        print "The goal of Pig is to be the first player to reach {0} points. You get points by rolling a single ".format(_winningValue)
        print "die multiple times and adding the value on each roll of the die to your current score.\n"

"""
Print the instructions for the current game
"""
def printGameInstructions(opt):
    global _winningValue
    print "Instructions: "
    if opt == "Fifty":
        print "A turn consists of a player rolling a pair of dice (with the goal of rolling doubles), "
        print "and scoring the roll as described below. Play continues with each player taking one roll per turn. "
        print "The first player to score {0} or more points is declared the winner.".format(_winningValue)
        print "All doubles except 3s and 6s score 5 points. Double 6s are worth 25 points. "
        print "Double 3s wipe out the player’s entire score, and the player must start again at 0. "
        print "Non-double rolls are 0 points.\n"

    else:
        print "The first player rolls the die as many times as they want. The value of each throw is added onto the "
        print "score until the player decides to end his turn and passes the die to the next player. Play continues until one player reaches {0}.".format(_winningValue)
        print "The value of each throw is added to the current player’s score. If the player rolls a 1, "
        print "the player’s score goes back to 0, and their turn ends. At one extreme, any player who gets a 1 on "
        print "the first roll is immediately out. At the other extreme, the first player could theoretically reach "
        print "the winning score on the first turn, as long as they don’t roll a 1. If the player succeeds, "
        print "the game ends there.\n"

"""
Print the options for the current game
"""
def printGameMenu(opt):
    print "1. Roll (r)\n" \
          "2. Score (s)\n" \
          "3. Game Description (d)\n" \
          "4. Game Instructions (i)\n" \
          "5. Pass (p) - only available in Pig\n" \
          "6. Quit (q)\n"

def printScores():
    global _playerScores
    print "-----Current Scores-----\n" \
          "Player 1: {0}\n" \
          "Player 2: {1}\n" \
          "------------------------\n".format(_playerScores["Player 1"][0], _playerScores["Player 2"][0])

def resetGame():
    global _playerScores
    global _currentPlayer
    global _nextPlayer
    _playerScores["Player 1"][0] = 0
    _playerScores["Player 1"][1] = True
    _playerScores["Player 2"][0] = 0
    _playerScores["Player 2"][1] = True
    _currentPlayer = "Player 1"
    _nextPlayer = "Player 2"

"""
Role die or dice depending on which game it is
"""
def roleDice(num):
    if num == 2:
        return [random.randint(1, 6), random.randint(1, 6)]

    else:
        return random.randint(1, 6)

"""
A quick way to keep track of the current player
"""
def swapPlayers():
    global _currentPlayer
    global _nextPlayer
    tmp = _currentPlayer
    _currentPlayer = _nextPlayer
    _nextPlayer = tmp

"""
Based on the role of the die and the current game, this function will
evaluate the values of the die or dice and determine what needs to happen
to the current player
"""
def evaluateDieValues(opt, values):
    global _currentPlayer
    global _playerScores

    if opt == "Fifty":
        if values[0] == values[1] and values[0] == 6:
            _playerScores[_currentPlayer][0] += 25

        elif values[0] == values[1] and values[0] == 3:
            _playerScores[_currentPlayer][0] = -99

        elif values[0] == values[1]:
            _playerScores[_currentPlayer][0] += 5

        print "{0} rolled -> {1}, {2}".format(_currentPlayer, values[0], values[1])

    elif opt == "Pig":
        if values == 1 and _playerScores[_currentPlayer] == 0 and _playerScores[_currentPlayer][1] is True:
            _playerScores[_currentPlayer][0] = -99

        elif values == 1 and _playerScores[_currentPlayer][1] is False:
            _playerScores[_currentPlayer][0] = 0

        else:
            _playerScores[_currentPlayer][0] += values
            _playerScores[_currentPlayer][1] = False

        print "{0} Rolled: {1}".format(_currentPlayer, values)

    else:
        pass

def playGame():
    global _currentPlayer
    global _playerScores
    global _currentGame
    global _winningValue

    printGameDescription(_currentGame)
    printGameInstructions(_currentGame)
    printGameMenu(_currentGame)
    exitGame = False
    while exitGame is False:
        userInput = raw_input("{0} >> ".format(_currentPlayer))
        print

        if userInput == "Roll" or userInput == "roll" or userInput == "r":
            if _currentGame == "Fifty":
                evaluateDieValues("Fifty", roleDice(2))
                if _playerScores[_currentPlayer][0] >= int(_winningValue):
                    print "\nCONGRATULATIONS {0}!!! YOU WON!!!!\n".format(_currentPlayer)
                    printScores()
                    print
                    exitGame = True

                elif _playerScores[_currentPlayer][0] == -99:
                    print "\n{0} rolled a pair of 3s... your score is now 0! Better luck next time! :(\n".format(_currentPlayer)
                    _playerScores[_currentPlayer][0] = 0

                else:
                    print "{0} score: {1}\n".format(_currentPlayer, _playerScores[_currentPlayer][0])
                    swapPlayers()

            else: # Else the game is Pig
                evaluateDieValues("Pig", roleDice(1))
                if _playerScores[_currentPlayer][0] >= int(_winningValue):
                    print "\nCONGRATULATIONS {0}!!! YOU WON!!!!\n".format(_currentPlayer)
                    printScores()
                    print
                    exitGame = True
                elif _playerScores[_currentPlayer][0] == 0:
                    print "\n{0} rolled a 1.. your score is now 0! Better luck next time! :(\n".format(_currentPlayer)
                    swapPlayers()
                elif _playerScores[_currentPlayer][0] == -99:
                    print "\n{0} rolled a 1 on the first try!! Your luck is the worst I have ever seen. GAME OVER!!!!! XD\n".format(_currentPlayer)
                    exitGame = True
                else:
                    print "\n{0} score: {1}\n".format(_currentPlayer, _playerScores[_currentPlayer][0])

        elif userInput == "Score" or userInput == "score" or userInput == "s":
            printScores()

        elif userInput == "\nDescription" or userInput == "description" or userInput == "d":
            printGameDescription(_currentGame)

        elif userInput == "Instructions" or userInput == "instructions" or userInput == "i":
            printGameInstructions(_currentGame)

        elif userInput == "Pass" or userInput == "pass" or userInput == "p" and _currentGame == "Pig":
            print "{0} decided to pass. {1} it is your turn!\n".format(_currentPlayer, _nextPlayer)
            swapPlayers()

        elif userInput == "Quit" or userInput == "quit" or userInput == "q":
            exitGame = True

        else:
            print "[!] -> That is not the correct input... try again!\n"

"""
Play the game Fifty
"""
def playFifty():
    playGame()
    print "Thank you for playing Fifty! We look forward to your playing with us again! :D\n"

"""
Play the game Pig
"""
def playPig():
    playGame()
    print "Thank you for playing Pig! We look forward to your playing with us again! :D\n"

"""
The main function where all of the magic happens.
"""
def main():
    quit = False
    global _currentPlayer
    global _nextPlayer
    global _currentGame
    global _winningValue
    global _playerScores
    while quit is False:
        resetGame()
        printGameChoices()
        userInput = raw_input("Which game would you like to play? ")
        if userInput == "Fifty" or userInput == "fifty" or userInput == "f":
            _currentGame = "Fifty"
            print "You have chosen to play the game Fifty. May the odds be ever in your favor!\n"
            gameValue = raw_input("To what point value would you like to play? ")
            _winningValue = gameValue
            playFifty()

        elif userInput == "Pig" or userInput == "pig" or userInput == "p":
            _currentGame = "Pig"
            print "You have chosen to play the game Pig. Please, do your best to avoid 1.\n"
            gameValue = raw_input("To what point value would you like to play? ")
            _winningValue = gameValue
            playPig()

        elif userInput == "Menu" or userInput == "menu" or userInput == "m":
            continue

        elif userInput == "Quit" or userInput == "quit" or userInput == "q":
            print "We HATE to see you leave! Come back soon!! :D"
            quit = True

        else:
            print "That is not the correct input... try again!\n"

if __name__ == "__main__":
    main()