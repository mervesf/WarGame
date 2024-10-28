# -*- coding: utf-8 -*-
"""MilestoneProject.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1k1LValQf4fWVXAVKKfJ8tb38VxHzcdYm
"""

import random
import numpy as np
from collections import Counter

#WAR-CARD GAME
class Card():
  def __init__(self,value,color):
    self.value=value
    self.color=color
  def sort_value(self):
    list_value=['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    return list_value.index(self.value)+1

class Deck():
  def __init__(self,deck_quantity):
    self.deck_quantity=deck_quantity
    self.deck_list=[]
  def add_card(self,value,color):
    if len(self.deck_list)<self.deck_quantity:
      self.deck_list.append(Card(value,color))
    else:
      print("You are attempting to add more cards than the deck can hold")
  def take_out_card(self,card_object):
    if len(self.deck_list)>0:
      self.deck_list.remove(card_object)
    else:
      print("You are attempting to take out a card more than in the deck")
  def delete_deck(self):
    del self
  def show_value(self):
    value_list=[]
    for j in range(len(self.deck_list)):
      value_list.append(self.deck_list[j].sort_value())
    return value_list

class Player():
  def __init__(self,name,cards_deck):
    self.name=name
    self.cards_deck=cards_deck
    self.number_cards_=len(self.cards_deck.deck_list)
  def select_card(self,amount=1):
    temp=[]
    if ((len(self.cards_deck.deck_list)>=amount)&(amount!=0)):
      temp.extend(self.cards_deck.deck_list[:amount])
      del self.cards_deck.deck_list[:amount]
      return temp
    else:
      print("The amount you specified can not be withdrawn.")
      return temp
  def get_cards(self,cards_list):
      self.cards_deck.deck_list.extend([j[0][0] for j in cards_list])
  def get_prize(self,prize):
      self.cards_deck.deck_list.extend(prize)

class Game():
  def __init__(self,card_list,number_player):
    self.state=['The game has been started','The cards are being compared','A state of war is being maintained','Card Game\'s winners have been obvious and the game is over.','The end of the round','The cards is being dealt.']
    self.player_list=[]
    self.condition=0
    self.winner=0
    self.card_list=card_list
    self.number_player=number_player
    self.prize_pile=[]
    self.war_indis=[]
    self.cards_drawn=[]
  def deal_card(self):
    random_value=[]
    temp=self.card_list.deck_list
    for j in range(self.number_player):
      random_value.append(random.sample(temp,len(self.card_list.deck_list)//self.number_player))
      temp=[temp[i] for i in range(len(temp)) if temp[i] not in random_value[j]]
    for j in range(len(self.player_list)):
      for i in range(len(random_value[j])):
         self.player_list[j].cards_deck.add_card(random_value[j][i].value,random_value[j][i].color)
  def add_player(self,name):
    if len(self.player_list)<self.number_player:
      self.player_list.append(Player(name,Deck(len(self.card_list.deck_list)//self.number_player)))
    else:
      print("You cannot keep adding player.")
  def remove_player(self):
    for j in range(len(self.player_list)):
      if len(self.player_list[j].cards_deck.deck_list)==0:
        del self.player_list[j]
  def start_game(self,name_player):
    if len(name_player)==self.number_player:
      for j in range(len(name_player)):
        self.add_player(name_player[j])
      self.deal_card()
      self.condition=5
    else:
      print('You are trying to add name more than the value of player number you specified!')
    self.show_round()
  def show_round(self):
    print(self.state[self.condition])
    print('**************************************************')
    print(f"The available players in the game:{[j.name for j in self.player_list]} ")
    print(f"The cards' number of the players' decks in the game:{[len(j.cards_deck.deck_list) for j in self.player_list]} ")
    print(f"The cards drawn on the last round :{[str(j[0][0].value)+' '+str(j[0][0].color) for j in self.cards_drawn]} ")
    print('**************************************************')
  def compare_and_collect(self):
    if not self.is_over():
      sort=[self.cards_drawn[j][0][0].sort_value() for j in range(len(self.cards_drawn))]
      counter_=Counter(sort)
      counter_list=sorted(counter_.items(), key=lambda x: x[0], reverse=True)
      if (counter_list[-1][1]>1):
        self.condition=2
        self.war_indis=[self.cards_drawn[j][1] for j in range(len(self.cards_drawn)) if self.cards_drawn[j][0][0].sort_value()==counter_list[-1][0]]
        self.select_cards_()
        if self.condition==2:
          self.compare_and_collect()
      else:
        indis_=[k[1] for k in self.cards_drawn if counter_list[-1][0]==k[0][0].sort_value()]
        self.player_list[indis_[0]].get_cards(self.cards_drawn)
        self.player_list[indis_[0]].get_prize(self.prize_pile)
        self.prize_pile=[]
      self.condition=4
      self.show_round()
      self.cards_drawn=[]
    else:
      print(f"The winner of the game has been obvious: Here is the winner :{game.player_list[0].name}")
      self.condition=3
  def select_cards_(self):
    print(len(self.player_list))
    if self.condition==2:
      self.prize_pile.extend([i[0][0] for i in self.cards_drawn])
      self.cards_drawn=[]
      for i in self.war_indis:
        self.prize_pile.extend(self.player_list[i].select_card(3))
        self.cards_drawn.append((self.player_list[i].select_card(),i))
    else:
      for j in range(len(self.player_list)):
        self.cards_drawn.append((self.player_list[j].select_card(),j))
    self.remove_player()
  def is_over(self):
    if len(self.player_list)==1:
      return True
    else:
      return False

card_value_list=['2','3','4','5','6','7','8','9','10','J','Q','K','A']
card_colour_list=['Hearts', 'Spades', 'Diamonds', 'Clubs']
game_deck=Deck(52)
for i in range(len(card_value_list)):
  for j in range(len(card_colour_list)):
    game_deck.add_card(card_value_list[i],card_colour_list[j])
game=Game(game_deck,2)
game.start_game(['FirstPlayer','SecondPlayer'])
while True:
  game.select_cards_()
  game.compare_and_collect()
  if game.condition==3:
    break

