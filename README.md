# Eustace-Euchre-Bot
### Calvin Isch, Ethan Eldridge

Our goal in this repository is to create the classes and algorithms necessary to create an AI Euchre player and an interface that a human player can utilize to engage with that AI.

There are three files in this repository with various functionalities. These files are: (1) Game.py (a class that holds all of the items relevantto the game) (2) Euchre.py (this holds the artifical intelligence player and the functions related to that) and (3) manual_player.py (that holds all of the functions that enable a human to play with the AI). The game file is the largest class, a game holds four player classes that can be any combination of manual players and AI players.

# Game.py : 
Has an optional attribute "orig" that can enable a child class to be created with many of the same characteristics as the parent class.

Attributes:
 (1) -Team1Score - Number 
 (2)  -Team2Score - Number
 (3)  -Player1 - a player class (manual or AI)
 (4)  -Player2 - a player class (manual or AI)
 (5)  -Player3 - a player class (manual or AI)
 (6)  -Player4 - a player class (manual or AI)
 (7) -whoCalled - number of the team who called a round
 (8)  -NumTricksTeam1 - number
 (9)  -NumTricksTeam2 - number
 (10)  -Dealer - number
 (11)  -offering - a string representing the first card offered
 (12)  -trump - a letter representing the trump suit
 (13)  -trump2 - a string representing the trump suit
 (14)  -VisibleCards - a list of all cards seen so far
 (15)  -BuriedCards - a list of all cards that are invisible
 (16)  -Order - a list with the ordering of the players
 
 Functions:
 (1)  -assign_cards - shuffles a deck and passes out five cards to each player
 (2)  -initalize - prints out the steup of the game and goes through the first steps necessary to call a suit
 (3)  -get_order - assigns ordering based on the dealer
 (4) -order_next_trick - gets a new ordering of players based on who won the previous trick
 (5) -getChild - creates a child that is the same as the current class
 (6) -scoreRound - Based on the tricks won and who called the suit scores the round
 (7) -updateNumTricks - after everyone has played sees who won the trick
 (8) -score_Cards_Trick - a helper function that get's the scores of all the cards in the trick
 (9) -play_trick - prints the statements and runs the functions necessary for a given trick
 (10) -play_round - prints the statements and runs the functions necessary for a given round
 (11) -play_game  - prints the statements and runs the functions necessary for a given game
 (12) -play_game_fast - runs multiple games to compare the different algorithms
  
  
  # Euchre.py
  This file holds the class of our AI euchre playing agent. It has the following attributes and functions: 
  
  Attributes:
   (1)  hand - a list of cards available to play
   (2)  name - a string for its name
   (3)  partner - to hold the class of the player who is its partner
   (4)  maxDepth - number for AB pruning
   (5)  team_number - either team one or two
   (6)  P1_WIN_SCORE - for AB pruning (1000)
   (7)  P2_WIN_SCORE - for AB pruning (-1000)
   (8)  tricks - a list of lists of four cards to hold all of the tricks that have been one
   
  Functions:
   (1)  score_cards - given a trump suit, returns a dictionary of the scores for cards
   (2)  initial_offering - given a trump card and a dealer, determines if the dealer should pick it up or not
   (3)  second_chance - given a trump card and a dealer, determines if they should call a suit after the offering card has been turned over
   (4)  pick_it_up - for the dealer in the instance that they are forced to pick up a card
   (5)  getAllValidMoves - given a lead suit and a trump suit determines what can be played
   (6)  play_heuristic - for AB pruning and Minimax, scores the game
   (7)  play_simple - our simple heuristic function that always plays the highest card
   (8)  play_random - plays a random playable card
   (9)  minimax - plays as the minimax algorithm
   (10)  findPlay - calls the minimax algorithm
   (11)  alphaBeta - plays as the alpha-beta algorithm,
   (12)  findPlay2 - calls the alphaBeta algorithm
   (13)  MonteCarlo - plays the montecarlo algorithm
  
  
  # manual_player.py
  This file holds the functions and attributes of the manual player:
  
  Attributes:
   (1)  hand - a list of cards available to play
   (2)  name - a string for its name
   (3)  partner - to hold the class of the player who is its partner
   (4)  team_number - either team one or two
   (5)  tricks - a list of lists of four cards to hold all of the tricks that have been one
  
  Functions:
   (1)  play - asks the player to play a card
   (2)  score_cards - gets a dictionary to determine the playable cards and to be compatable with the minimax algorithm
   (3)  findPlay - also neededfor the minimax algorithm, just asks the dealer what to play
   (4)  findPlay2 - calls findPlay - necessary for the alphabeta algorithm from the Euchre.py
   (5)  MonteCarlo - calls findPlay - necessary for the montecarlo function
   (6)  Initial_offering - asks the user to call a suit.
   (7)  getAllValidMoves - important for checking what the user can play
   (8)  second_chance - for the second round of calling suits
