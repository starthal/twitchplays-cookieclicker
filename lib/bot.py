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
                    if button == 'restart' or button == 'continue': 
                        if button == 'restart':
                            reset_counter += 5
                            if reset_counter >= reset_counter_max:
                                reset_counter = 0
                                self.game.push_button('restart')
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
