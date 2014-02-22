import time

from config.config import config
from lib.irc import Irc
from lib.game import Game
from lib.misc import pbutton
from lib.gui import command, set_reset_bar

class Bot:

    reset_counter = 0

    def __init__(self):
        self.config = config
        self.irc = Irc(config)
        self.game = Game()

        self.message_buffer = [{'username': '', 'button': ''}] * 10


    def set_message_buffer(self, message):
        chat_height = 10
        self.message_buffer.insert(chat_height - 1, message)
        self.message_buffer.pop(0)


    def run(self):
        last_start = time.time()
        
        reset_counter_max = self.config['reset_bar']['max']
        reset_counter = 0

        while True:
            new_messages = self.irc.recv_messages(1024)
            
            if not new_messages:
                continue

            for message in new_messages: 
                button = message['message'].lower()
                username = message['username'].lower()
                suffix = ''
                if self.game.is_valid_button(button):
                    if button == 'reset' or button == 'continue': 
                        if button == 'reset':
                            reset_counter += 5
                            if reset_counter >= reset_counter_max:
                                reset_counter = 0
                                self.game.push_button('reset')
                        else:
                            reset_counter -= 5
                            if reset_counter < 0:
                                reset_counter = 0
                        suffix = '({0}/{1})'.format(reset_counter,reset_counter_max)
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
                      reset_counter -= numclicks
                      self.game.push_button("click%d" % numclicks)
                      command(username, "click(%d)" % numclicks)
                        
