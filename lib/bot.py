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

    def start_golden_timer(self, cc):
        has_alerted_golden = False
        has_alerted_reindeer = False
        while True:
            time.sleep(1)
            golden_life = cc.get_golden_life()
            reindeer_life = cc.get_reindeer_life()
            print str(golden_life) + str(has_alerted_golden)
            print str(reindeer_life) + str(has_alerted_reindeer)
            if golden_life == 0:
                has_alerted_golden = False
            elif golden_life > 0 and has_alerted_golden == False:
                self.irc.say('GOLDEN!!!')
                has_alerted_golden = True

            if reindeer_life == 0:
                has_alerted_reindeer = False
            elif reindeer_life > 0 and has_alerted_reindeer == False:
                self.irc.say('REINDEER!!!')
                has_alerted_reindeer = True

    def run(self, cc):
        self.game = Game(cc)
        last_start = time.time()

        
        reset_counter = 0
        reset_counter_max = self.config['reset_bar']['max']
        pledge_counter = 0
        pledge_counter_max = config['pledge_bar']['max']
        pop_counter = 0
        pop_counter_max = config['pop_bar']['max']
        next_golden = time.clock() + 5

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
                        try:
                            upgrade_ind = int(button[12])-1
                        except:
                            upgrade_ind = -1
                    else:
                        upgrade_ind = 0
                    upgrade_name = self.game.cc.get_upgrade_name(upgrade_ind)
                    if upgrade_name == 'undefined':
                        self.irc.say('Invalid Upgrade')
                    else:
                        numdivs = 0
                        upgrade_price = self.game.cc.get_upgrade_price(upgrade_ind)
                        if upgrade_price > 1000000:
                            upgrade_price = float(upgrade_price) / 1000000
                            numdivs += 1
                            while upgrade_price > 1000:
                                upgrade_price = float(upgrade_price) / 1000
                                numdivs += 1
                        if numdivs == 0:
                            pricesuffix = ''
                        elif numdivs == 1:
                            pricesuffix = ' M'
                        elif numdivs == 2:
                            pricesuffix = ' B'
                        elif numdivs == 3:
                            pricesuffix = ' T'
                        elif numdivs == 4:
                            pricesuffix = ' Qa'
                        elif numdivs == 5:
                            pricesuffix = ' Qi'
                        elif numdivs == 6:
                            pricesuffix = ' Sx'
                        elif numdivs == 7:
                            pricesuffix = ' Sp'
                        elif numdivs == 8:
                            pricesuffix = ' O'
                        short_price = "%.3f%s" % (upgrade_price, pricesuffix)
                        self.irc.say('UPGRADE' + str(upgrade_ind+1) + ': ' + upgrade_name + ' (' + short_price + ')')
                elif button == '!commands':
                    self.irc.say('Clickclick..., Golden, Reindeer, Dungeon, Up, Down, Left, Right, Stay, Upgrade1 - Upgrade5, Info UpgradeX, NoPledge, Santa, Cursor, Grandma, Farm, Factory, Mine, Shipment, Lab, Portal, Time, Antimatter, Prism, View, Scrolldown, Scrollup, Expand, Collapse, Reset, Continue')
                elif self.game.is_valid_button(button):
                    if button == 'pop' and config['pop_bar']['enable']:
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
                        name = self.game.cc.get_upgrade_name(upgrade_ind)
                        if config['pledge_bar']['enable'] and (name == 'Elder Pledge' or name == 'Elder Covenant' or name == 'Revoke Elder Covenant'):
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
