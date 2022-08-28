# A euchre player in Python


class man_Player:
	# initialize a player with their hand of cards and also an empty list
	# with their tricks
	def __init__(self, hand, team_number, name):
		self.hand = hand
		self.name = name
		self.partner = None
		self.team_number = team_number
		self.tricks = []

	# manual player plays
	def play(self, lead, plays, trump):

		# show the user which cards they have available
		print("You have the following cards:")
		for i in range(len(self.hand)):
			print(i+1, self.hand[i])
		print("Which would you like to play? \n (Press the number corresponding to desired card)")

		# chooses card corresponding to their input, updates hand accordingly
		choice = int(input())-1
		plays = self.hand[choice]
		self.hand.pop(choice)
		return plays

	# To score the cards, is necessary for Minimax.
	def score_cards(self, trump):
		
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

	def findPlay(self, g, d):
		# show the user which cards they have available
		print("You have the following cards:")
		for i in range(len(self.hand)):
			print(i+1, self.hand[i])
		print("Which would you like to play? \n (Press the number corresponding to desired card)")

		# chooses card corresponding to their input, updates hand accordingly
		choice = int(input())-1
		plays = self.hand[choice]
		self.hand.pop(choice)
		print(plays)
		return plays

	def findPlay2(self, g, d):
		return self.findPlay(g,d)

	def MonteCarlo(self, g):
		d =1
		return self.findPlay(g,d)

	# the initial offering round 
	def initial_offering(self, trump_card, dealer):
		# Show the player their cards
		print("You have the following cards:")
		for i in range(len(self.hand)):
			print(i+1, self.hand[i])
		
		# Asks for their input
		print("Would you like the dealer, ", dealer.name," to pick up the",trump_card,"? \n 1: 'Pick it up! \n 2: 'Pass.'")
		
		# Either Picks it up or passes
		if int(input()) == 1:
			return("Pick it up.")
		else: 
			return("Pass.")

	# What to do when you are told to pick up a card
	def pick_it_up(self, trump_card):

		# Show them their cards
		print("You have the following cards:")
		for i in range(len(self.hand)):
			print(i+1, self.hand[i])

		print("Trump is ", trump_card)
		# Ask which one they'd like to replace
		print("Which would you like to replace the trump card with?")
		choice = int(input())-1

		# Replace that card
		self.hand.pop(choice)
		self.hand.append(trump_card)

	# Important for the minimax algorithm.
	def getAllValidMoves(self, lead, trump):
	# other wise play the best option

		Dict = self.score_cards(trump)
		options = []
		score_2 = []
		if lead == None:
			score_2 = []
			for i in self.hand:
				score_2.append(Dict[i])
			return self.hand, score_2

		# See which cards are available to play
		lead_suit = lead[-1:]
		if trump == "D" and lead == "JH":
			lead_suit = "D"
		if trump == "S" and lead == "JC":
			lead_suit = "S"
		if trump == "H" and lead == "JD":
			lead_suit = "H"
		if trump == "C" and lead == "JS":
			lead_suit = "C"

		for i in self.hand:
			if trump == "C" and i == "JS":
				options.append(i)
			if trump == "S" and i == "JC":
				options.append(i)
			if trump == "D" and i == "JH":
				options.append(i)
			if trump == "H" and i == "JD":
				options.append(i)
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

	def second_chance(self, trump_card, dealer):
		# Show them their cards
		print("You have the following cards:")
		for i in range(len(self.hand)):
			print(i+1, self.hand[i])

		# Get the suits you can still call it
		suits = ["H","D","S","C"]
		suits2 = ["Hearts","Diamonds","Spades","Clubs"]
		suits2.pop(suits.index(trump_card[-1:]))

		# Ask for their input
		print("The trump card was ",trump_card)
		print("Would you like to call a suite trump?")
		for i in range(len(suits2)):
			print(i+1,":",suits2[i])
		if dealer.name != self.name:
			print(4, ":","Pass.")

		choice = int(input())-1
		if choice == 3:
			return("Pass.")
		else:
			return(suits2[choice])





if __name__ == "__main__":

	p = man_Player(['JS','JC','AS','KS','QS'],1)

	print(p.play())

