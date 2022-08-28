# A euchre game in Python
import random
import time
from Euchre import Player
from manual_player import man_Player

class Euchre(object):

	def __init__(self, orig = None):
		# If given a game state copies it
		if not orig is None: 
			# Things that are necessary for each game
			self.Team1Score = orig.Team1Score
			self.Team2Score = orig.Team2Score
			self.Player1 = orig.Player1
			self.Player2 = orig.Player2
			self.Player3 = orig.Player3
			self.Player4 = orig.Player4

			# Things that are necessary each hand
			self.whoCalled = orig.whoCalled
			self.NumTricksTeam1 = orig.NumTricksTeam1
			self.NumTricksTeam2 = orig.NumTricksTeam2
			self.dealer = orig.dealer
			self.offering = orig.offering
			self.trump = orig.trump
			self.trump2 = orig.trump2
			self.VisibleCards = orig.VisibleCards
			self.BuriedCards = orig.BuriedCards
			self.order = orig.order

			# things that are necessary for each trick
			self.lead = orig.lead
			self.players = orig.players
			self.plays = orig.plays

			# For alphabeta
			self.depth = orig.depth

		# Things that are necessary for each game
		self.Team1Score = 0
		self.Team2Score = 0
		self.Player1 = None
		self.Player2 = None
		self.Player3 = None
		self.Player4 = None

		# Things that are necessary each hand
		self.whoCalled = None
		self.NumTricksTeam1 = 0
		self.NumTricksTeam2 = 0
		self.dealer = 1
		self.offering = 'JS'
		self.trump = None
		self.trump2 = None
		self.VisibleCards = []
		self.BuriedCards = []
		self.order = []

		# things that are necessary for each trick
		self.lead = None
		self.players = []
		self.plays = []

		# For minimax and alphabeta
		self.depth = 8


	# Shuffles the deck and assigns each of the players 5 cards
	# Also creates a trump card
	def assign_cards(self):
		# All of the cards in the deck
		Deck = ['9S','10S','JS','QS','KS',"AS", '9C',
			'10C','JC','QC','KC',"AC",'9H','10H','JH','QH',
			'KH',"AH",'9D','10D','JD','QD','KD',"AD"]

		# Shuffle the cards
		random.shuffle(Deck)

		# Assign the offering, visible, and buried cards
		self.offering = Deck[20]
		self.VisibleCards.append(Deck[20])
		self.BuriedCards = Deck[21:]

		# Create the players
		self.Player1 = man_Player(Deck[0:5],1, "Player 1")
		self.Player2 = Player(Deck[5:10],2, "Player 2")
		self.Player3 = Player(Deck[10:15],1, "Player 3")
		self.Player4 = Player(Deck[15:20],2, "Player 4")	
	
	# For setting up a game	
	def initialize(self):
		print("We had better shuffle the deck.")
		for i in range(3):
			print("Shuffle")

		# Deal out the cards
		self.assign_cards()
		print("Player 1:", self.Player1.hand)
		print("Player 2:", self.Player2.hand)
		print("Player 3:", self.Player3.hand)
		print("Player 4:", self.Player4.hand)

		
		print("\nThe offering card is: ", self.offering)
		self.get_order()
		dealer = self.order[-1]
		print("The dealer is: ", dealer.name)

		# goes through the initial offering
		for i in self.order:
			print("\n\nIt's ", i.name,"'s turn to call it.")
			answer = i.initial_offering(self.offering, dealer)
			print(i.name, " says ", answer)
			if answer != "Pass.":
				self.trump = self.offering[-1:]
				self.whoCalled = i.team_number
				dealer.pick_it_up(self.offering)
				break

		# goes through the second offering
		if self.trump == None:
			print("No one called it. We're going to flip over the trump card")
			for i in self.order:
				print("\n\nIt's ", i.name,"'s turn to call it.")
				answer = i.second_chance(self.offering, dealer)
				print(i.name, " says ", answer)
				if answer != "Pass.":
					self.trump = answer[0:1]
					self.whoCalled = i.team_number
					break

		print("And the trump suit is...",self.trump)
		# Get the dictionary so we can compare who wins
		Dict = self.Player4.score_cards(self.trump)

	# Finds the order that we should play
	def get_order(self):
		# Find's the order of play based on who is the dealer
		self.order = [self.Player4,self.Player1,self.Player2,self.Player3]
		if self.dealer % 4 == 0:
			self.order = [self.Player1,self.Player2,self.Player3,self.Player4]
		if self.dealer % 4 == 1:
			self.order = [self.Player2,self.Player3,self.Player4,self.Player1]
		if self.dealer % 4 == 2:
			self.order = [self.Player3,self.Player4,self.Player1,self.Player2]
		# changes the dealer for the next round
		self.dealer += 1

	# After a trick, creates a new order based on who won it.
	def order_next_trick(self, winner):
		self.order = [self.Player4,self.Player1,self.Player2,self.Player3]
		if winner.name == "Player 1": 
			self.order = [self.Player1,self.Player2,self.Player3,self.Player4]
		if winner.name == "Player 2": 
			self.order = [self.Player2,self.Player3,self.Player4,self.Player1]
		if winner.name == "Player 3": 
			self.order = [self.Player3,self.Player4,self.Player1,self.Player2]

	# Creates a "child" gamestate based on a played card, useful for Minimax
	def getChild(self, card, player):
		child = Euchre(self)
		child.VisibleCards.append(card)
		child.players.append(player)
		child.plays.append(card)
		return child

	# score a round based on the rules of Euchre (i.e. number of tricks one)
	def scoreRound(self):
		if self.NumTricksTeam2 + self.NumTricksTeam1 < 5:
			return 0
		if self.whoCalled == 1:
			if self.NumTricksTeam1 == 5:
				self.Team1Score += 2
				return 2
			elif self.NumTricksTeam1 >= 3:
				self.Team1Score += 1
				return 1
			else:
				self.Team2Score += 2
				return -2
		else:
			if self.NumTricksTeam2 == 5:
				self.Team2Score += 2
				return -2
			elif self.NumTricksTeam2 >= 3:
				self.Team2Score += 1
				return -1
			else:
				self.Team1Score += 2
				return 2

	# Updates the tricks
	def updateNumTricks(self, who):
		self.players[who].tricks.append(self.plays)
		if self.players[who].name == "Player 1" or self.players[who].name == "Player 3":
			self.NumTricksTeam1 += 1
		else:
			self.NumTricksTeam2 += 1
		# Update Visible Cards
		for i in self.plays:
			self.VisibleCards.append(i)

	# Should be run any time all four players have played to determine the winner
	def score_cards_trick(self, cards = None):
		if cards == None:
			cards = self.plays
		Dict = self.Player1.score_cards(self.trump)
		score = []
		for i in cards:
			# Check to see if it's the left.
			if game.trump[-1:] == "D" and i == "JH":
				score.append(Dict[i])
			elif game.trump[-1:] == "S" and i == "JC":
				score.append(Dict[i])
			elif game.trump[-1:] == "H" and i == "JD":
				score.append(Dict[i])
			elif game.trump[-1:] == "C" and i == "JS":
				score.append(Dict[i])
			# Checks to see if you're the first to play
			elif game.lead == None:
				score.append(Dict[i])
			# Next see if it's the same suit as the lead
			elif game.lead[-1:] == i[-1:]:
				score.append(Dict[i])
			# See if it's trump
			elif game.trump[-1:] == i[-1:]:
				score.append(Dict[i])
			# Otherwise it doesn't match the lead or trump and is worth 0
			else:
				score.append(0)

		# Return the index of the player who won.
		return score.index(max(score))

	# Plays an individual trick out of a round
	def play_trick(self):
		for player in self.order:
			print("\n\n")
			print("It's", player.name,"'s turn to play!")
			if self.plays != []:
	
				print("Don't forget that the trump suit is: ",self.trump)
				time.sleep(1)
				print("So far the following cards have been played:")
				time.sleep(1)
				for i in range(len(self.plays)):
					print(self.players[i].name,":",self.plays[i])


			# let them play the .play can also be .findPlay
			# play = player.play(self.lead, self.plays, self.trump)
			# play = player.MonteCarlo(self)
			play = player.findPlay(self, self.depth)
			# play = player.findPlay2(self, self.depth) == AB
			# play = player.play(self, self.lead, self.plays, self.trump) == Simple Heuristic
			print(player.name,"decided to play the",play)
			time.sleep(1)

			# update the plays accordingly
			if self.lead == None:
				self.lead = play

			self.players.append(player)
			self.plays.append(play)

		# see who had the highest card, that person is the winner
		who = self.score_cards_trick()
		time.sleep(1)
		print("\n\n\n")
		print(self.players[who].name, "won that trick with the",self.plays[who],"!!!")
		time.sleep(2)
		
		# Give them their trick
		self.updateNumTricks(who)

		# Update the order for next trick
		self.order_next_trick(self.players[who])

		# Reset the trick to be 0
		self.plays = []
		self.players = []
		self.lead = None


	# Game Play for a single round
	def play_round(self):
		print("It's time for the next round!!!")
		print("")
		print("We had better shuffle the deck.")
		for i in range(3):
			time.sleep(1)
			print("Shuffle")
		
		# Deal out the cards
		self.assign_cards()
		
		print("\nDon't forget, the teams are \n Team 1: Player 1 and Player 3 \n Team 2: Player 2 and Player 4")
		time.sleep(2)
		print("\nThe offering card is: ", self.offering)
		time.sleep(1)
		# Get the order that we should play.
		self.get_order()
		dealer = self.order[-1]
		print("The dealer is: ", dealer.name)
		time.sleep(1)

		# goes through the initial offering
		for i in self.order:
			print("\n\nIt's ", i.name,"'s turn to call it.")
			time.sleep(1)
			answer = i.initial_offering(self.offering, dealer)
			print(i.name, " says ", answer)
			if answer != "Pass.":
				self.trump = self.offering[-1:]
				self.whoCalled = i.team_number
				dealer.pick_it_up(self.offering)
				break

		# goes through the second offering
		if self.trump == None:
			print("No one called it. We're going to flip over the trump card")
			time.sleep(1)
			for i in self.order:
				print("\n\nIt's ", i.name,"'s turn to call it.")
				time.sleep(1)
				answer = i.second_chance(self.offering, dealer)
				print(i.name, " says ", answer)
				if answer != "Pass.":
					self.trump = answer[0:1]
					self.whoCalled = i.team_number
					break

		# Get the dictionary so we can compare who wins
		Dict = self.Player4.score_cards(self.trump)

		# At this point cards are out and trump has been selected
		# time to play.
		for i in range(5):
			print("\n\n\n")
			print("#############################################")
			print("###    We are in Trick", i+1,"of the Round.    ###")
			print("#############################################")
			print("Don't forget that the trump suit is",self.trump)
			print("\nSo far team 1 has",self.NumTricksTeam1,"tricks and team 2 has",self.NumTricksTeam2,"tricks.")
			time.sleep(1)
			self.play_trick()

			

		print("In that round the teams got:")
		print("\n Team 1:",self.NumTricksTeam1,"tricks.\n Team 2:",self.NumTricksTeam2,"tricks.\n")
		print("Since Team", self.whoCalled,"called it the scores will change as follows.")
		print("The old scores were:\n Team 1 -",self.Team1Score, "\n Team 2 -",self.Team2Score)
		self.scoreRound()
		print("The new scores are:\n Team 1 -",self.Team1Score, "\n Team 2 -",self.Team2Score)
		self.NumTricksTeam1 = 0
		self.NumTricksTeam2 = 0
		self.VisibleCards =[]
		self.BuriedCards = []
		self.whoCalled = None
		self.trump = None


	def play_game(self):

		print("\n\n\nWelcome to the game of Euchre!!!!")
		print("You are about to play our AI. Good luck!")
		time.sleep(2)
		r = 1

		# Keep playing rounds until someone has won!
		while self.Team1Score < 10 and self.Team2Score < 10:
			print("\n\n\n+--------------------------------------+")
			print("|    You are on round",r,"of the game.   |")
			print("+--------------------------------------+")
			print("\nThe current score is: \n Team 1:",self.Team1Score,"\n Team 2:", self.Team2Score)
			time.sleep(1)
			r += 1
			self.play_round()

		print("The final scores were \n Team 1:",self.Team1Score,"\n Team 2:", self.Team2Score, "\nThanks for playing, we hope you enjoyed!")

	def play_game_fast(self, amount, t1 = None, t2 = None):

		# Play in rounds, not games
		while self.Team1Score + self.Team2Score < amount:
			
			# Deal out the cards
			Deck = ['9S','10S','JS','QS','KS',"AS", '9C',
				'10C','JC','QC','KC',"AC",'9H','10H','JH','QH',
				'KH',"AH",'9D','10D','JD','QD','KD',"AD"]

			# Shuffle the cards
			random.shuffle(Deck)

			# Assign the offering, visible, and buried cards
			self.offering = Deck[20]
			self.VisibleCards.append(Deck[20])
			self.BuriedCards = Deck[21:]

			# Create the players
			self.Player1 = Player(Deck[0:5],1, "Player 1")
			self.Player2 = Player(Deck[5:10],2, "Player 2")
			self.Player3 = Player(Deck[10:15],1, "Player 3")
			self.Player4 = Player(Deck[15:20],2, "Player 4")

			# put them in order	
			self.get_order()
			dealer = self.order[-1]

			first_worked = 0
			# goes through the initial offering
			for i in self.order:
				answer = i.initial_offering(self.offering, dealer)
				if answer != "Pass.":
					first_worked = 1
					self.trump = self.offering[-1:]
					self.whoCalled = i.team_number
					dealer.pick_it_up(self.offering)
					break

			# goes through the second offering
			if first_worked == 0:
				for i in self.order:
					answer = i.second_chance(self.offering, dealer)
					if answer != "Pass.":
						self.trump = answer[0:1]
						self.whoCalled = i.team_number
						break
			
			#print("Team",self.whoCalled,"went with the following trump:",self.trump)

			# Get the dictionary so we can compare who wins
			Dict = self.Player4.score_cards(self.trump)

			# At this point cards are out and trump has been selected
			# time to play.
			for i in range(5):

				for player in self.order:
				
					# let them play the .play can also be .findPlay
					# play = player.play(self.lead, self.plays, self.trump)
					if player.team_number == 1 or player.team_number == 3:
						if t1 == "AB":
							play = player.findPlay2(self, self.depth)
						elif t1 == "Mini":
							play = player.findPlay(self, self.depth)
						elif t1 == "Simple":
							play = player.play(self.lead, self.plays, self.trump)
						elif t1 == "Random":
							play = player.play_random(self.lead, self.trump)
						else:
							play = player.MonteCarlo(self)
					if player.team_number == 2 or player.team_number == 4:
						if t2 == "AB":
							play = player.findPlay2(self, self.depth)
						elif t2 == "Mini":
							play = player.findPlay(self, self.depth)
						elif t2 == "Simple":
							play = player.play(self.lead, self.plays, self.trump)
						elif t2 == "Random":
							play = player.play_random(self.lead, self.trump)
						else:
							play = player.MonteCarlo(self)

					# update the plays accordingly
					if self.lead == None:
						self.lead = play

					self.players.append(player)
					self.plays.append(play)
					"""
					if self.plays != []:
						for i in range(len(self.plays)):
					"""
							

				# see who had the highest card, that person is the winner
				who = self.score_cards_trick()
				
				# Give them their trick
				self.updateNumTricks(who)
				
				# Update the order for next trick
				self.order_next_trick(self.players[who])

				# Reset the trick to be 0
				self.plays = []
				self.players = []
				self.lead = None
			
			# After the trick has been played, score it!
			if self.whoCalled == 1 and self.NumTricksTeam1 == 5:
				self.Team1Score += 2
			elif self.whoCalled == 1 and self.NumTricksTeam1 >= 3:
				self.Team1Score += 1
			elif self.whoCalled == 1:
				self.Team2Score += 2
			elif self.whoCalled == 2 and self.NumTricksTeam2 == 5:
				self.Team2Score += 2
			elif self.whoCalled == 2 and self.NumTricksTeam2 >= 3:
				self.Team2Score += 1
			else:
				self.Team1Score += 2
			
			# If you want to check on interim progress uncomment these lines
			#print("That round team 1 had", self.NumTricksTeam1,"Team 2 had:",self.NumTricksTeam2)
			print("Team 1 score:",self.Team1Score,"\nTeam 2 score:",self.Team2Score)
			
			# Reset the game state
			self.NumTricksTeam1 = 0
			self.NumTricksTeam2 = 0
			self.VisibleCards = []
			self.BuriedCards = []
			self.whoCalled = None
			self.trump = None

		print("Team",t1,"score:",self.Team1Score,"\nTeam",t2,"score:",self.Team2Score)

if __name__ == "__main__":

	game = Euchre() 
	
	# If you want to play the ai
	game.play_game()

	# If you want to compare a couple algorithms 
	#game.play_game_fast(1000,"AB","MC")

	# If you want to time the AI
	#a = "MC"
	#t0 = time.time()
	#game.play_game_fast(100,a,a)
	#t1 = time.time()
	#print(a,"had a time of",t1-t0,"seconds for 100 games.")

	#game.initialize()
	#game.Player1.findPlay2(game,game.depth)
	#game.Player2.findPlay2(game,game.depth)