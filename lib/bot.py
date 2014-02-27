import time

from config.config import config
from lib.irc import Irc
from lib.game import Game
from lib.misc import pbutton
from lib.gui import *

class Bot:

    def __init__(self):
        self.config = config
        self.irc = Irc(config)

        self.message_buffer = [{'username': '', 'button': ''}] * 10


    def set_message_buffer(self, message):
        chat_height = 10
        self.message_buffer.insert(chat_height - 1, message)
        self.message_buffer.pop(0)


    def run(self, cc):
        self.game = Game(cc)
        last_start = time.time()

        
        reset_counter = 0
        reset_counter_max = self.config['reset_bar']['max']
        pledge_counter = 0
        pledge_counter_max = config['pledge_bar']['max']
        pop_counter = 0
        pop_counter_max = config['pop_bar']['max']

        while True:
            new_messages = self.irc.recv_messages(1024)
            
            if not new_messages:
                continue

            for message in new_messages: 
                button = message['message'].lower()
                username = message['username'].lower()
                suffix = ''
                
                if button[:12] == 'info upgrade':
                    if len(button) > 12:
                        upgrade_ind = int(button[12])-1
                    else:
                        upgrade_ind = 0
                    upgrade_name = self.game.cc.upgrade_name(upgrade_ind)
                    self.irc.say('UPGRADE' + str(upgrade_ind+1) + ': ' + upgrade_name)
                elif self.game.is_valid_button(button):
                    if button == 'pop':
                        pop_counter += 1
                        if pop_counter >= pop_counter_max:
                            pop_counter = 0
                            self.game.push_button('unwrinkle')
                        set_pop_bar(pop_counter)
                    elif button == 'reset' or button == 'continue': 
                        if button == 'reset':
                            reset_counter += 5
                            if reset_counter >= reset_counter_max:
                                reset_counter = 0
                                self.game.push_button('reset')
                                pledge_counter = 0
                                set_pledge_bar(pledge_counter)
                        else:
                            reset_counter -= 5
                            if reset_counter < 0:
                                reset_counter = 0
                        suffix = '({0}/{1})'.format(reset_counter,reset_counter_max)
                    elif button[:7] == 'upgrade':
                        reset_counter -= 1
                        if reset_counter < 0:
                            reset_counter = 0
                        if len(button) == 7:
                            upgrade_ind = 0
                        else:
                            upgrade_ind = int(button[7])-1
                        name = self.game.upgrade_name(upgrade_ind)
                        if name == 'Elder Pledge' or name == 'Elder Covenant' or name == 'Revoke Elder Covenant':
                          # Throttle pledges if necessary
                          pledge_counter += 1
                          if pledge_counter >= pledge_counter_max:
                            self.game.push_button(button)
                            pledge_counter = 0
                          set_pledge_bar(pledge_counter)
                          button = 'pledge/cov'
                          suffix = '({0}/{1})'.format(pledge_counter,pledge_counter_max)
                        else:
                          self.game.push_button(button)
                    elif button == 'nopledge':
                        reset_counter -= 1
                        if reset_counter < 0:
                            reset_counter = 0
                        if pledge_counter > 0:
                            pledge_counter -= 1
                            set_pledge_bar(pledge_counter)
                        suffix = '({0}/{1})'.format(pledge_counter,pledge_counter_max)
                    else:
                        reset_counter -= 1
                        if reset_counter < 0:
                            reset_counter = 0
                        
                        print button

                        self.set_message_buffer({'username': username, 'button': button})

                        self.game.push_button(button)
                    command(username, button + suffix)
                    set_reset_bar(reset_counter)
                else:
                    numclicks = button.count("click")
                    if numclicks > 0:
                      if numclicks > 9:
                        numclicks = 9
                      reset_counter -= 1 #numclicks?
                      if reset_counter < 0:
                              reset_counter = 0
                      self.game.push_button("click%d" % numclicks)
                      command(username, "click(%d)" % numclicks)
                      set_reset_bar(reset_counter)                        
