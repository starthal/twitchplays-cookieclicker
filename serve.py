#!/usr/bin/env python

# Twitch Plays
# Inpsired by http://twitch.tv/twitchplayspokemon
# Written by Aidan Thomson - <aidraj0 at gmail dot com>

from config.config import config
from threading import Thread
import lib.gui as gui
import lib.bot as bot
from lib.timer import Timer
import time
import lib.cookiecontrol as cookiecontrol

cc = cookiecontrol.CookieControl()

thread1 = Thread(target = gui.run)
thread1.start()
botinst = bot.Bot()
thread1 = Thread(target = botinst.run, args=(cc,))
thread1.start()
thread1 = Thread(target = botinst.start_golden_timer, args=(cc,))
thread1.start()

timer = Timer(cc, config['pop_timer']['hours'],config['pop_timer']['minutes'],config['pop_timer']['seconds'])

thread1 = Thread(target = gui.start_timer, args=(timer,))
thread1.start()

