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

	def deal(self,num_hands,num_cards): #2 hands, 5 cards
		hands = []
		x = 0
		while x < num_hands :
			for i in range(0,num_cards+1):
				hands[x].add_card(self.pop_card())
				#num_cards = num_cards - 1
			num_hands = num_hands + 1
class Hand:
	# create the Hand with an initial set of cards
	# param: a list of cards
	def __init__(self, init_cards):
			self.cards = init_cards

	# add a card to the hand
	# silently fails if the card is already in the hand
	# param: the card to add
	# returns: nothing
	def add_card(self, card):
		card_strs = []
		for c in self.cards:
			card_strs.append(c.__str__())
		if card.__str__() not in card_strs:
			self.cards.append(card)

	# remove a card from the hand
	# param: the card to remove
	# returns: the card, or None if the card was not in the Hand
	def remove_card(self, card):
		card_strs = []
		for c in self.cards:
			card_strs.append(c.__str__())
		if card.__str__() in card_strs:
			self.cards.remove(card)
			return card
		else:
			return None

	# draw a card from a deck and add it to the hand
	# side effect: the deck will be depleted by one card
	# param:the deck from which to draw
	# returns: nothing
	def draw(self, deck):
		pop = deck.pop_card()
		self.add_card(pop)

	def remove_pairs(self): #4,4,6,7,8,11,6
		for card in self.cards:
			current_card = card
			print(card)
			for card2 in self.cards:
				if (card2.__str__() != card.__str__()):
					if (card2.rank_num == card.rank_num):
						self.remove_card(card)
						self.remove_card(card2)
