#
# This file defines code to display a video poker screen.
#
# CMPS 5P
# Fall 2016
# Copyright 2016 by Ethan L. Miller
#
# Card images from https://code.google.com/archive/p/vector-playing-cards/
# Card back uses image from Baskin SOE.
#

import tkinter
import random
import sys
import re

VP_payoff_information = {
  "Royal flush" : 250,
  "Straight flush" : 50,
  "Four of a kind" : 25,
  "Full house" : 9,
  "Flush" : 6,
  "Straight" : 4,
  "Three of a kind" : 3,
  "Two pair" : 2,
  "Jacks or better" : 1
  }

class VPCard (object):
  def __init__ (self, vp, pos, window = None, card = '2C'):
    self.vp = vp
    self.pos = pos
    if window == None:
      window = vp.root
    self.button = tkinter.Button (window, command=self)
    self.button.grid (column=pos, row=1, padx=5, pady=10)
    self.heldlabel = tkinter.Label (window, text='')
    self.heldlabel.grid (column=pos, row=0, pady=5)
    self.setcard (card)
    self.disable ()
    self.side = 'front'

  # Necessary so that button clicks work properly
  def __call__ (self):
    if not self.enabled:
      return
    self.setheld (not self.held)

  # Set the card that the button is showing
  def setcard (self, card):
    card = card.upper()
    if card in self.vp.cardimages and card != 'back':
      self.card = card
    else:
      raise KeyError('Illegal card: "%s"' % (card))
    # New cards are not held and are showing front
    self.showside ('front')
    self.setheld (False)

  # Set the held banner above each card properly
  def setheld (self, is_held):
    assert type(is_held) == type (True)
    self.held = is_held
    if self.held:
      self.heldlabel.config (text='HELD')
    else:
      self.heldlabel.config (text='')

  # Show either the front or back of the card
  def showside (self, side):
    side = side.lower ()
    if side == 'back':
      self.button.config (image=self.vp.cardimages['back'])
      self.showing = side
    elif side == 'front':
      self.button.config (image=self.vp.cardimages[self.card])
      self.showing = side
    else:
      raise

  def disable (self):
    self.enabled = False
  def enable (self):
    self.enabled = True

class VPBetButton (object):
  '''
  This class displays a button that allows someone to bet n credits
  '''
  def __init__ (self, vp, n, pos, window = None):
    self.vp = vp
    self.credits = n
    self.pos = pos
    if window == None:
      window = vp.root
    self.button = tkinter.Button (window, command=self,
                                  text=('%d credits' % (self.credits)))
    self.button.grid (row=0, column=pos, padx=5)
    self.disable ()

  def __call__ (self):
    self.pressed = True
    self.button.quit ()

  def enable (self):
    self.pressed = False
    self.button.config (state=tkinter.NORMAL)
    self.button.update_idletasks()

  def disable (self):
    self.button.config (state=tkinter.NORMAL)
    self.button.config (state=tkinter.DISABLED)
    self.button.update_idletasks()


class VideoPoker (object):
  def __init__ (self):
    self.root = tkinter.Tk ()
    # Generate the different regions of the screen
    self.payoff_frame = tkinter.Frame (self.root)
    self.hand_frame = tkinter.Frame (self.root)
    self.status_frame = tkinter.Label (self.root)
    self.bet_buttons_frame = tkinter.Frame (self.root)
    self.dealbutton = tkinter.Button (self.root, text='Deal!',
                                      state=tkinter.DISABLED,
                                      command=self.root.quit)
    self.quitbutton = tkinter.Button (self.root, text='Quit!',
                                      state=tkinter.NORMAL,
                                      command=sys.exit)
    self.continuebutton = tkinter.Button (self.root, text='Continue!',
                                          state=tkinter.DISABLED,
                                          command=self.root.quit)
    self.payoff_frame.grid (column=0, row=0, columnspan=2, padx=5, pady=5)
    self.hand_frame.grid (column=0, row=1, padx=5, pady=5)
    self.status_frame.grid (column=0, row=2, columnspan=2, padx=5, pady=5)
    self.bet_buttons_frame.grid (column=0, row=3, padx=5, pady=5)
    self.dealbutton.grid (column=1, row=1, padx=5)
    self.quitbutton.grid (column=1, row=3, padx=5)
    self.continuebutton.grid (column = 0, row=4)
    self.status_label = tkinter.Label (self.status_frame, text='', width=50)
    self.credits_label = tkinter.Label (self.status_frame,
                                        width=14, text='Credits: XXX')
    self.status_label.grid (column=0, row=0)
    self.credits_label.grid (column=1, row=0)
    # Generate the array of card images
    self.cardimages = {}
    self.cardnames = []
    self.cardimgs = re.split ('::::::\s+([A-Z0-9]+)\s+::::::', cardimagestrings_b64)
    for i in range (1, len(self.cardimgs), 2):
      card = self.cardimgs[i]
      self.cardimages[card] = tkinter.PhotoImage(data=self.cardimgs[i+1])
      self.cardnames.append (card)

    self.cardimages['back'] = tkinter.PhotoImage(data=backimagestring_b64)
    # Generate the cards on the screen
    self.cards = []
    randomhand = random.sample (self.cardnames, 5)
    for i in range(5):
      cb = VPCard (self, i, self.hand_frame, randomhand[i])
      cb.showside ('back')
      self.cards.append (cb)
    # Generate the betting buttons
    self.bet_buttons = []
    for i in range (5):
      self.bet_buttons.append (VPBetButton (self, i+1, i,
                                            self.bet_buttons_frame))
    self.display_payoff_info (self.payoff_frame)
    self.root.update_idletasks ()

  def display_payoff_info (self, frame):
    # Generate the labels for the payoff window
    self.payoff_labels = {}
    r = 0
    for i,txt in enumerate (['Hand'] +
                            ['%d credits' % (x) for x in range (1,6)]):
      self.payoff_labels[txt] = tkinter.Label (frame, text=txt)
      self.payoff_labels[txt].grid (row=r, column=i, padx=10)
    for v,k in sorted (zip (VP_payoff_information.values(),
                            VP_payoff_information.keys()), reverse=True):
      r += 1
      self.payoff_labels[k,0] = tkinter.Label (frame, text=k)
      self.payoff_labels[k,0].grid (row=r, column=0, padx=10, sticky='W')
      for credits in range (1,6):
        payoff = v * credits
        if payoff == 1250:
          payoff = 4000 # Royal flush for 5 credits is more!
        self.payoff_labels[k,credits] = tkinter.Label (frame,
                                                       text = str(payoff))
        self.payoff_labels[k,credits].grid (row=r, column=credits,
                                            sticky='E', padx=10)
  def get_all_cards (self):
    '''Returns a list of all of the current cards.'''
    cardlist = []
    for card in self.cards:
      cardlist.append (card.card)
    return (cardlist)

  def set_cards (self, cardlist):
    '''
    Sets all of the cards in the hand to the list passed
    '''
    if len (cardlist) != 5:
      raise
    for i, card in enumerate (cardlist):
      self.cards[i].setcard (card)
    self.root.update_idletasks()

  def get_credits_bet (self):
    '''
    Runs the GUI, and returns the number of credits bet once that button
    is clicked.  All other clickable items are disabled.
    '''
    for card in self.cards:
      card.showside ('back')
      card.disable ()
    self.dealbutton.config (state=tkinter.DISABLED)
    for btn in self.bet_buttons:
      btn.enable ()
    self.root.mainloop ()
    # Returns when a button is pushed
    for btn in self.bet_buttons:
      btn.disable ()
      if btn.pressed:
        credits = btn.credits
    self.root.update_idletasks()
    return credits

  def get_held_cards (self):
    '''
    Runs the GUI to allow the user to select the cards s/he wants to keep.
    Once "Deal" is pressed, this function returns a list (by position) of
    the cards that were held.
    '''
    for card in self.cards:
      card.enable()
    self.dealbutton.config (state=tkinter.NORMAL)
    self.root.update_idletasks()
    self.root.mainloop ()
    self.dealbutton.config (state=tkinter.NORMAL)
    self.root.update_idletasks()
    self.dealbutton.config (state=tkinter.DISABLED)
    cardlist = []
    for card in self.cards:
      card.disable()
      if card.held:
        cardlist.append (card.pos)
    self.root.update_idletasks()
    return (cardlist)

  def set_status (self, msg):
    '''
    Sets the status message to the text passed.  The text is clipped at
    60 characters to ensure that it fits.
    '''
    self.status_label.config (text=msg[:60])
    self.root.update_idletasks()

  def display_credits (self, credits):
    '''
    Display the number of credits the user has.  Note that this number has
    to be an integer.
    '''
    self.credits_label.config (text = 'CREDITS: %d' % (credits))
    self.root.update_idletasks ()

  def await_continue_button (self):
    '''
    Waits for the user to click the "Continue" button.
    '''
    for btn in self.bet_buttons:
      btn.disable ()
    for card in self.cards:
      card.disable ()
    self.dealbutton.config (state=tkinter.DISABLED)
    self.continuebutton.config (state=tkinter.NORMAL)
    self.root.mainloop ()
    self.continuebutton.config (state=tkinter.NORMAL)
    self.root.update_idletasks ()
    self.continuebutton.config (state=tkinter.DISABLED)
    self.root.update_idletasks ()
