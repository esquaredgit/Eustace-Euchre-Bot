# A euchre player in Python
import itertools 
import math
import random as rn
import copy

class Player:
	# initialize a player with their hand of cards and also an empty list
	# with their tricks
	def __init__(self, hand, team_number, name):
		self.hand = hand
		self.name = name
		self.partner = None
		self.maxDepth = 3
		'''
		We need to figure out how to implement Max/Min heuristic values and what to judge each heuristic on during each round.
		For example, during Stage 3 (Playing the Round), should we prioritize moves that benefit either player on the team,
		or should we prioritize the player's moves first?
		'''
		self.team_number = team_number

		self.P1_WIN_SCORE = 1000
		self.P2_WIN_SCORE= -1000

		# Keeps track of which of the five tricks the player's team has won. This will be empty if the team has not won any.
		# We could use this at some point in scoring to award two points to the team that has won all of the tricks 
		# –> (check to see if their trick array is full or if opponents'is empty)
		self.tricks = []
	
	# A function that, given a trump suit returns a dictionary
	# of scores for cards given what is trump
	def score_cards(self, trump):
		'''
		****Scoring system for cards in a hand****

		Based on the suit of the trump card, each card in the Player's hand will have a different value.
		The following is a hierarchy list for card scoring:
		- Offsuit 9's: 1
		- Offsuit 10's: 2
		- Offsuit J's: 3
		- Offsuit Q's: 4
		- Offsuit K's: 5
		- Offsuit A's: 6
		- Trump 9's: 7
		- Trump 10's: 8
		- Trump Q's: 9
		- Trump K's: 10
		- Trump A's: 11
		- Left Bower J: 12
		- Right Bower J: 13
		'''
		if trump == "D":
			Dict = {
			'9S':1,'10S':2,'JS':3,'QS':4,'KS':5, "AS":6, 
			'9C':1,'10C':2,'JC':3,'QC':4,'KC':5,"AC":6,
			'9H':1,'10H':2,'JH':12,'QH':4,'KH':5,"AH":6,
			'9D':7,'10D':8,'JD':13,'QD':9,'KD':10,"AD":11
			}

		if trump == "H":
			Dict = {
			'9S':1,'10S':2,'JS':3,'QS':4,'KS':5, "AS":6, 
			'9C':1,'10C':2,'JC':3,'QC':4,'KC':5,"AC":6,
			'9H':7,'10H':8,'JH':13,'QH':9,'KH':10,"AH":11,
			'9D':1,'10D':2,'JD':12,'QD':4,'KD':5,"AD":6
			}

		if trump == "C":
			Dict = {
			'9S':1,'10S':2,'JS':12,'QS':4,'KS':5, "AS":6, 
			'9C':7,'10C':8,'JC':13,'QC':9,'KC':10,"AC":11,
			'9H':1,'10H':2,'JH':3,'QH':4,'KH':5,"AH":6,
			'9D':1,'10D':2,'JD':3,'QD':4,'KD':5,"AD":6
			}

		if trump == "S":
			Dict = {
			'9S':7,'10S':8,'JS':13,'QS':9,'KS':10, "AS":11, 
			'9C':1,'10C':2,'JC':12,'QC':4,'KC':5,"AC":6,
			'9H':1,'10H':2,'JH':3,'QH':4,'KH':5,"AH":6,
			'9D':1,'10D':2,'JD':3,'QD':4,'KD':5,"AD":6
			}

		return(Dict)

	# A heuristic that tells you whether or not to pick up a card in an initial offering
	def initial_offering(self, trump_card, dealer):
		score = 0

		# get's a dictionary with the score for cards based on what's trump
		Dict = self.score_cards(trump_card[-1:])

		# if the dealer is on your team add the trump card to the overall score
		if dealer.team_number == self.team_number:
			score += Dict[trump_card]

		# score all of the cards in your hand off of what is trump
		for c in self.hand:
			score += Dict[c]

		# if the score reaches a threshold, pick it up. Otherwise, pass.
		if score >= 39:
			return("Pick it up.")
		else:
			return("Pass.")

	# A heuristic to call a suite after the initial round
	def second_chance(self, trump_card, dealer):
		# Looks at all suits
		suits = ["H","D","S","C"]
		all_suits = []

		# for each of the suits
		for i in suits:
			score = 0
			# scores all of the cards in your hand

			# if the suit was the original trump card give score 0
			if trump_card[-1:] == i:
				all_suits.append(0)
				next
			else: 
				# otherwise score normally
				Dict = self.score_cards(i)
				for c in self.hand:
					score += Dict[c]
				all_suits.append(score)
		suits2 = ["Hearts","Diamonds","Spades","Clubs"]

		# if the value for a suit reaches a threshold call it, otherwise pass.
		if max(all_suits) >= 39:
			return(suits2[all_suits.index(max(all_suits))])
		elif dealer.name == self.name:
			return(suits2[all_suits.index(max(all_suits))])
		else:
			return("Pass.")

	# Pick up the trump card if you are the dealer
	def pick_it_up(self, trump_card):
		Dict = self.score_cards(trump_card[-1:])
		hand_scored = []
		# Score all of the cards in your hand
		for i in self.hand:
			hand_scored.append(Dict[i])
		choice = hand_scored.index(min(hand_scored))
		self.hand.pop(choice)
		self.hand.append(trump_card)

	# Looks at a lead card and determines which cards player can play
	def getAllValidMoves(self, lead, trump):
	

		Dict = self.score_cards(trump)
		options = []
		score_2 = []
		if lead == None:
			score_2 = []
			for i in self.hand:
				score_2.append(Dict[i])
			return self.hand, score_2

		# See which cards are available to play

		# First check to see if it's the left that led
		lead_suit = lead[-1:]
		if trump == "D" and lead == "JH":
			lead_suit = "D"
		if trump == "S" and lead == "JC":
			lead_suit = "S"
		if trump == "H" and lead == "JD":
			lead_suit = "H"
		if trump == "C" and lead == "JS":
			lead_suit = "C"

		# Then look at the cards in your hand
		for i in self.hand:
			# Again check to see if you have the left
			if trump == "C" and lead_suit == "C" and i == "JS":
				options.append(i)
				score_2.append(Dict[i])
			if trump == "S" and lead_suit == "S"and i == "JC":
				options.append(i)
				score_2.append(Dict[i])
			if trump == "D" and lead_suit== "D" and i == "JH":
				options.append(i)
				score_2.append(Dict[i])
			if trump == "H" and lead_suit== "H"and i == "JD":
				options.append(i)
				score_2.append(Dict[i])
			if i[-1:] == lead_suit:
				options.append(i)
				score_2.append(Dict[i])


		# if none you can play them all!
		if options == []:
			options = self.hand
			score_2 = []
			for i in self.hand:
				score_2.append(Dict[i])

		return options, score_2			


	# takes a game state and returns a heuristic value based on how good it
	# is for the person.
	# Good positions for team 1 should be positive and
    # good positions for team 2 should be negative
	def play_heuristic(self, buried_cards, tricks_Team1, tricks_Team2, trick_players, trick_cards, trump, game):
		# Should consider 
			# 1. # of tricks per team so far
			# 2. Cards left in hand
			# 3. Who has the current trick
			# 4. Cards left that are buried

		score = 0
		score_cards = 0

		# 30 points to the score for every trick a team has
		score += 30 * tricks_Team1
		score += -30 * tricks_Team2

		# Simply adds the value of each one of the cards in your hand
		Dict = self.score_cards(trump)
		for i in self.hand:
			if self.team_number == 1:
				score_cards += Dict[i]
			else:
				score_cards -= Dict[i]

		# Looks at who is winning the given trick
		score_played = []
		for i in trick_cards:
			score_played.append(Dict[i])

		# Give points based on who is currently winning a trick
		if score_played != []:
			winner = trick_players[game.score_cards_trick()]
			if winner.team_number == 1:
				score += 15
			else:
				score -= 15

		# Has a sharply discounted score for the buried cards
		# the idea is that you want to keep track of what's been
		# played and draw out powerful cards from your opponents
		for i in buried_cards:
			if self.team_number == 1:
				score_cards += -(Dict[i] * .05)
			else:
				score_cards += Dict[i] * .05

		if self.team_number == 1:
			score = score + score_cards
		else:
			score = score - score_cards
		return score

	# A simple heuristic that plays the max card for each trick
	def play_simple(self, lead, plays, trump):

		# Get the dictionary of scores
		Dict = self.score_cards(trump)

		# Score all cards in the hand
		scores = []
		for i in self.hand:
			scores.append(Dict[i])

		# If no one has played yet it's your turn. Play the highest
		if lead == None:
			play = scores.index(max(scores))
			card = self.hand[play]
			self.hand.pop(play)
			return card

		# other wise play the best option
		options, score_2 = self.getAllValidMoves(lead, trump)
		#if score_2 == []:
		#	card = options[0]
		#else:
		play = score_2.index(max(score_2))
		card = options[play]
		self.hand.pop(self.hand.index(card))


		return card

	# current play class
	def play(self, lead, plays, trump):
		return self.play_simple(lead, plays, trump)

	# A random player
	def play_random(self, lead, trump):
		# other wise play the best option
		options, score_2 = self.getAllValidMoves(lead, trump)
		rn.shuffle(options)
		card = options[0]
		self.hand.pop(self.hand.index(card))
		return card


    # performs minimax on board with depth.
    # returns the best move and best score as a tuple
	def minimax(self, game, depth):
		finished = game.scoreRound()
		# First checks to see if we've reached a solution
		if finished == 2:
			return None, self.P1_WIN_SCORE
		if finished == 1:
			return None, self.P1_WIN_SCORE / 2
		if finished == -1:
			return None, self.P2_WIN_SCORE
		if finished == -2:
			return None, self.P2_WIN_SCORE / 2

		# Second checks to see if we are at the end of the depth
		if depth == 0:
			return None, self.play_heuristic(game.BuriedCards,game.NumTricksTeam1,game.NumTricksTeam2,game.players,game.plays, game.trump, game)

		# If everyone has played we need to find a new order based on winner
		if len(game.players) == 4:

			# See which card was the highest, that person is the winner
			winner = game.players[game.score_cards_trick()]

			# Update the gamestate based on who has won
			game.updateNumTricks(winner)
			game.order_next_trick(winner)
			game.players = []
			game.plays = []
			game.lead = None

			# Call the function again with the new game state for modified order
			return self.minimax(game, depth)

		# get the player in question (e.g. the person who's next in order)
		i = game.order[len(game.players)]

		# Starts with bestMove being None
		bestMove = None

		# Get's all of the possible moves
		moves, scores = i.getAllValidMoves(game.lead,game.trump)
		
		# if team_number is one it maximizes
		if i.team_number == 1:
			# MAX get the minimum score
			bestVal = self.P2_WIN_SCORE

			# Looks at all possible moves
			for p in moves:
				# creates a child for each move
				child = game
				child.getChild(p, i)

				# gets the move and value for that move
				m, v = self.minimax(child, depth-1)
				if v > bestVal:
					bestVal = v
					bestMove = p

			# if the best move is a none-type just provide your minimum card		
			if bestMove is None:
				bestMove = moves[scores.index(min(scores))]
			return bestMove, bestVal
		
		# If team number is not one it minimizes 
		else:
			# MIN gets the maximum score
			bestVal = self.P1_WIN_SCORE

			# looks at all possible moves 
			for p in moves:
				child = game
				child.getChild(p, i)

				# gets the move and value for that move
				m, v = self.minimax(child,depth-1)
				if v < bestVal:
					bestVal = v
					bestMove = p

			# if the best move is a none-type just provide your minimum card
			if bestMove is None:
				bestMove = moves[scores.index(min(scores))]
			return bestMove, bestVal

	# max depth = 4
	def findPlay(self, game, depth):
		card, score = self.minimax(game, depth)
		self.hand.pop(self.hand.index(card))
		return card
	
	# Add alpha-beta pruning to improve minimax run time
	def alphaBeta(self, alpha, beta, game, depth):
		finished = game.scoreRound()
		# First checks to see if we've reached a solution
		if finished == 2:
			return None, self.P1_WIN_SCORE
		if finished == 1:
			return None, self.P1_WIN_SCORE / 2
		if finished == -1:
			return None, self.P2_WIN_SCORE
		if finished == -2:
			return None, self.P2_WIN_SCORE / 2

		# Second checks to see if we are at the end of the depth
		if depth == 0:
			return None, self.play_heuristic(game.BuriedCards,game.NumTricksTeam1,game.NumTricksTeam2,game.players,game.plays, game.trump, game)

		# If everyone has played we need to find a new order based on winner
		if len(game.players) == 4:

			# See which card was the highest, that person is the winner
			winner = game.players[game.score_cards_trick()]

			# Update the gamestate based on who has won
			game.updateNumTricks(winner)
			game.order_next_trick(winner)
			game.players = []
			game.plays = []
			game.lead = None

			# Call the function again with the new game state for modified order
			return self.alphaBeta(alpha, beta, game, depth)

		# get the player in question (e.g. the person who's next in order)
		i = game.order[len(game.players)]

		# Starts with bestMove being None
		bestMove = None

		# Get's all of the possible moves
		moves, scores = i.getAllValidMoves(game.lead,game.trump)

		# if team_number is one it maximizes
		if i.team_number == 1:
			# MIN gets the maximum score
			bestVal = self.P2_WIN_SCORE

			# Looks at all possible moves
			for p in moves:
				# creates a child for each move
				child = game
				child.getChild(p, i)

				# gets the move and value for that move
				m, v = self.alphaBeta(alpha, beta, child, depth-1)
				alpha = max(v, alpha)
				if v > bestVal:
					bestVal = v
					bestMove = p

				if beta <= alpha: 
					m = None
					break

			# if the best move is a none-type just provide your minimum card
			if bestMove is None:
				bestMove = moves[scores.index(min(scores))]
			return bestMove, bestVal

		else:
			# MIN gets the maximum score
			bestVal = self.P1_WIN_SCORE

			# looks at all possible moves 
			for p in moves:
				child = game
				child.getChild(p, i)

				# gets the move and value for that move
				m, v = self.alphaBeta(alpha, beta, child, depth-1)
				beta = min(v, beta)
				if v < bestVal:
					bestVal = v
					bestMove = p
				if beta <= alpha: 
					m = None
					break

			# if the best move is a none-type just provide your minimum card
			if bestMove is None:
				bestMove = moves[scores.index(min(scores))]
			return bestMove, bestVal		

	def findPlay2(self, game, depth):
		card, score = self.alphaBeta(-math.inf, math.inf, game, depth)
		self.hand.pop(self.hand.index(card))
		return card


	# Pretty pretty algorithm pls work pretty pls
	def MonteCarlo(self, game):
		"""
		This algorithm examines the possible outcomes posed by choosing each of the valid moves at a certain game state.
		For each of the valid moves, the rest of the current round is randomly simulated over a certain number of iterations and the outcome is recorded. 
		The valid move that shows the best outcomes is chosen as the next move.
		"""
		# Scores holds the expected outcome for choosing each valid move 
		scores = []
		# Dict holds the dictionary of all cards in the game and their scores given the current trump card in play.
		Dict = self.score_cards(game.trump)
		a = self.getAllValidMoves(game.lead, game.trump)[0]
		# For each valid move.
		for m in range(0,len(a)):
			move = a[m]

			# Calculates where you are currently in the playing order of the round
			tricksSoFar = game.NumTricksTeam1 + game.NumTricksTeam2 + 1
			# Plays is a list that holds the player object for each player who has already played in this trick. If it is empty, this player will be the first player to go.
			# beenPlayed holds the cards that each of the players in Plays played already.
			# These two lists are matched by index.
			plays = game.players
			beenPlayed = game.plays
			all_cards = ['9S','10S','JS','QS','KS', "AS", 
						 '9C','10C','JC','QC','KC',"AC",
						 '9H','10H','JH','QH','KH',"AH",
						 '9D','10D','JD','QD','KD',"AD"]
			# teamOne and teamTwoTricks keep a tally of the tricks won in each simulation.
			teamOneTricks = 0
			teamTwoTricks = 0
			allValids2 = copy.copy(a)
			# Because you are making a move, you need to remove it from the list of valid moves left to take:
			del allValids2[m]
			# This sequence finds the remaining possible cards in the round
			still_left = [x for x in all_cards if x not in game.VisibleCards]
			still_left = [x for x in still_left if x not in self.hand]
			still_left = [x for x in still_left if x not in game.plays]
			# Begins random simulations. Change SIMULATIONS to add/subtract more.
			SIMULATIONS = 1000
			for i in range(0, SIMULATIONS):
				
				# Begins simulation by finishing current trick
				rn.shuffle(still_left)
				
				# Create a copy of the remaining buried cards
				still_left2 = copy.copy(still_left)
				# beenPlayed2 simulates the progression of the current trick
				beenPlayed2 = copy.copy(beenPlayed)
				beenPlayed2.append(move)
				# playersLeft calculates how many players have yet to go after you have made your move
				playersLeft = 4 - len(beenPlayed2)
				for p in range(0, playersLeft):
					beenPlayed2.append(still_left2.pop(0))
				
				"""
				score_played = []
				# This loop is accumulating the card values for each card in the trick to see who has won the trick:
				for c in beenPlayed2:
					score_played.append(Dict[c])
				"""
				# Winner is assigned the index of the highest-valued card in score_played
				winner = game.score_cards_trick(beenPlayed2)

				# Checking to see if the winner is a partner or an opponent
				if winner < len(beenPlayed):

					# Plays is being update, but players is not
					person = plays[winner]
					if person.team_number == self.team_number:
						teamOneTricks += 1
					else:
						teamTwoTricks += 1
				elif winner == len(beenPlayed):
					teamOneTricks += 1
				# 0.28 is the probability that the person with the higher card was your partner
				else: 
					x = rn.randint(0, 100)
					if x > 28:
						teamTwoTricks += 1
					else:
						teamOneTricks += 1
				
				allValids3 = copy.copy(self.hand)
				del allValids3[m]

				# Now that the current trick is over, we will simulate the remaining tricks in the round by choosing random cards from the cards that are left...
				for j in range(0,(5-tricksSoFar)):

					# firstRand chooses a random vaild move to represent your play
					firstRand = rn.choice(allValids3)
					allValids3.remove(firstRand)
					# beenPlayed3 will eventually contain all of the cards from the trick, with your play as the first entry
					beenPlayed3 = [firstRand]
					for p in range(0, 3):
						beenPlayed3.append(still_left2.pop(0))
					# Scoring process same as above:
					"""
					score_played2 = []
					for c in beenPlayed3:
						score_played2.append(Dict[c])
					winner = score_played2.index(max(score_played2))
					"""
					winner = game.score_cards_trick(beenPlayed3)

					# Given that your move was the first entry in beenPlayed3, your team will be credited the point
					if winner == 0:
						teamOneTricks += 1
					# If you are not the winner, there is a 1/3 chance that your partner will be the winner from the remaining three players
					else:
						r = rn.randint(0,100)
						if r > 33:
							teamTwoTricks += 1
						else:
							teamOneTricks += 1
			# Accumulate the total tricks your team won from the simulations of this valid move
			scores.append(teamOneTricks)
		# Returns the move with the best outcomes over all random simulations
		card = a[scores.index(max(scores))]
		self.hand.pop(self.hand.index(card))
		return card



if __name__ == "__main__":

	p = Player(['JS','JC','AS','KS','QS'],1,"Player 1")
	p2 = Player(['10H','JS','QD','9H','AH'])

	print(p.initial_offering('10S',"partner"))
	print(p.second_offering('10S',"partner"))
	print(p.play_simple('9H',['9S','10H'],'S'))
	print(p2.initial_offering('10S',"partner"))
	print(p2.second_offering('10S',"partner"))
	print(p2.play_simple('9H',['9S','10H'],'S'))