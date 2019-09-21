import random
import unittest

class Card(object):
	suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
	rank_levels = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

	def __init__(self, suit=0,rank=2):
		self.suit = self.suit_names[suit]
		if rank in self.faces: # self.rank handles printed representation
			self.rank = self.faces[rank]
		else:
			self.rank = rank
		self.rank_num = rank # To handle winning comparison

	def __str__(self):
		return "{} of {}".format(self.rank,self.suit)

class Deck(object):
	def __init__(self): # Don't need any input to create a deck of cards
		# This working depends on Card class existing above
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card) # appends in a sorted order

	def __str__(self):
		total = []
		for card in self.cards:
			total.append(card.__str__())
		# shows up in whatever order the cards are in
		return "\n".join(total) # returns a multi-line string listing each card

	def pop_card(self, i=-1):
		# removes and returns a card from the Deck
		# default is the last card in the Deck
		return self.cards.pop(i) # this card is no longer in the deck -- taken off

	def shuffle(self):
		random.shuffle(self.cards)

	def replace_card(self, card):
		card_strs = [] # forming an empty list
		for c in self.cards: # each card in self.cards (the initial list)
			card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
		if card.__str__() not in card_strs: # if the string representing this card is not in the list already
			self.cards.append(card) # append it to the list

	def sort_cards(self):
		# Basically, remake the deck in a sorted way
		# This is assuming you cannot have more than the normal 52 cars in a deck
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card)

	# remove all pairs from hand
	# params: number of hands, number of cards per hand
	# returns: list of hands
	def deal(self, num_hands=2, num_cards=-1):
		# calculate total number of cards to be dealt
		if num_cards == -1:
			deal_cards = len(self.cards)
		else:
			deal_cards = num_hands * num_cards
		# initialize list
		dealt_hands = []
		# deal # number of cards
		while deal_cards > 0:
			# distribute across Hands
			for h in range(num_hands):
				# check if any cards left in deck
				if deal_cards > 0:
					# check if Hand has been created
					if len(dealt_hands) < num_hands:
						# initialize Hand with first card
						dealt_hands.append(Hand([self.pop_card()]))
					else:
						# move top card of Deck to Hand
						dealt_hands[h].add_card(self.pop_card())
					# counting down number of cards to deal
					deal_cards -= 1
		# return list of hands
		return(dealt_hands)

class Hand(object):
	# create the Hand with an initial set of cards
	# param: a list of cards
	def __init__(self, init_cards):
		self.cards = init_cards
		self.books = []
		
	# add a card to the hand
	# silently fails if the card is already in the hand
	# param: the card to add
	# returns: nothing
	def add_card(self, card):
		# create empty list
		card_strs = []
		# loop through cards in hand, append string version of card to list
		for d in self.cards:
			card_strs.append(d.__str__()) # 
		# if new card is not found in list, append it
		if card.__str__() not in card_strs:
			self.cards.append(card)

	# remove a card from the hand
	# param: the card to remove
	# returns: the card, or None if the card was not in the Hand
	def remove_card(self, card):
		# loop through cards in hand
		for i, card_hand in enumerate(self.cards):
			# if card is found in list, remove it
			if card_hand.__str__() == card.__str__():
				self.cards.pop(i)
				return(card_hand)

	# draw a card from a deck and add it to the hand
	# side effect: the deck will be depleted by one card
	# param: the deck from which to draw
	# returns: nothing
	def draw(self, deck):
		# draw a card from given deck
		new_card = deck.pop_card()
		# add card to hand
		self.add_card(new_card)

	######## EXTRA CREDIT 2 - REMOVE PAIRS ########
	# remove all pairs from hand
	# param: nothing
	# returns: nothing
	def remove_pairs(self):
		# create empty list
		card_val = [] # our original list of cards
		card_rem = [] # our manipulated list of cards for reference
		# loop through cards in hand, append string version of card to lists
		for c in self.cards:
			card_val.append(c.rank)
			card_rem.append(c.rank)
		# loop through every card in reverse order, so that indexes do not change during operation
		# reference for reversed(list(enumerate(list_variable))): https://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python
		for c, card in reversed(list(enumerate(card_val))):
			# if there is an even number of a specific card in a hand, remove all
			# if there is an odd number of a specific card in a hand, leave one in hand
			if card_rem.count(card) > (card_val.count(card) % 2):
				# remove card
				card_rem.pop(c)
				self.cards.pop(c)

def play_gofish(num_players = 2, AI = False):
	# start game by initializing deck and dealing out cards
	deck = Deck()
	deck.shuffle()
	players = deck.deal(num_players, 7) #hands
	turn = 0
	book_count = 0

	# loop until all cards are in books
	while book_count < 13:
		# some turn logic
		event = ''
		player = players[turn]
		if turn + 1 == num_players:
			oppo = players[0]
		else:
			oppo = players[turn + 1]

		# print out list of current player's cards
		print('Player {}\'s turn: These are your cards.'.format(turn + 1))
		for c in range(len(player.cards)):
			print(player.cards[c])

		# request card choice
		if AI == False:
			request = int(input('Player {}\'s turn: What card rank (1-13) would you like to request? '.format(turn + 1)))
		else:
			request = player.cards[random.randint(0, len(player.cards) - 1)].rank

		# look for matching cards in opponent's hand
		loot = []
		for i in range(4):
			steal = oppo.remove_card(Card(i, request))
			if steal:
				loot.append(steal)

		if len(loot) > 0:
			# add to own hand
			player.cards.extend(loot)
			print('You stole {} card(s)!'.format(len(loot)))
			event = 'steal'
		elif len(deck.cards) > 0:
			# none found, so draw from pool
			player.draw(deck)
			print('You took a card from the pool.')
			event = 'pool'
		
		# if four cards of the same rank in a player's hand, add to book:

		# dictionary of frequencies of ranks
		rank_frequencies = {}
		for i in range(len(player.cards)):
			if player.cards[i].rank_num not in rank_frequencies:
				rank_frequencies[player.cards[i].rank_num] = 0
			rank_frequencies[player.cards[i].rank_num] += 1

		rank_to_remove = 0
		for rank in rank_frequencies:
			if rank_frequencies[rank] == 4:
				rank_to_remove = rank_frequencies[rank] 
		
		for i in range(len(player.cards)): 
			if player.cards[i].rank_num == rank_to_remove:
				player.books.append[palyer.cards[i]]
				player.remove_card(player.cards[i])
				print("Rank {} added to book".format(rank_to_remove))







		# count books
		book_count = 0
		for p in range(num_players):
			book_count += len(players[p].books)

		

		# end of turn
		if player.cards[-1].rank == request and event == 'pool':
			# if player drew from pool and card matched request, player goes again
			print('-------- End of turn, Player {} goes again --------'.format(turn + 1))
		else:
			# more turn logic
			turn += 1
			if turn >= num_players:
				turn = 0
			print('-------- End of turn, Player {} goes next --------'.format(turn + 1))

# play the game
# params: 	num_players: number of players (default: 2)
# 			AI: set True for a bot-only game (default: False)
play_gofish()