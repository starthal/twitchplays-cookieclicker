#!/usr/bin/env python

# Twitch Plays
# Inpsired by http://twitch.tv/twitchplayspokemon
# Written by Aidan Thomson - <aidraj0 at gmail dot com>

from config.config import config
from threading import Thread
import lib.gui as gui
import lib.bot as bot
import time

thread1 = Thread(target = gui.run)
thread1.start()
time.sleep(.3)#hackish way to make sure global timer and timerpanel are initialized
thread1 = Thread(target = gui.start_timer)
thread1.start()
thread1 = Thread(target = bot.Bot().run)
thread1.start()

