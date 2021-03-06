#import win32api
#import win32con
import time
from config.config import config
from timer import Timer
from gui import start_timer

class Game:

  def __init__(self, cc):
    self.cc = cc

  BUTTONS = {
    'click',
    'upgrade',
    'upgrade1',
    'upgrade2',
    'upgrade3',
    'upgrade4',
    'upgrade5',
    'nopledge', # Only in bot
    'cursor',
    'grandma',
    'farm',
    'factory',
    'mine',
    'shipment',
    'lab',
    'portal',
    'time',
    'antimatter',
    'prism',
    'golden',
    'santa',
    'reindeer',
    'scrollup',
    'scrolldown',
    'view',
    'expand',
    'collapse',
    'reset',
    'continue', # Only in bot
    'dungeon',
    'up',
    'down',
    'left',
    'right',
    'stay',
    'dunk',
    'pop',
    #'unwrinkle',
  }
  
  locked = False

  def get_valid_buttons(self):
    return [button for button in self.BUTTONS]

  def is_valid_button(self, button):
    return button in self.BUTTONS

  def get_upgrade_name(self, upgrade_ind):
    return self.cc.get_upgrade_name(upgrade_ind)

  def push_button(self, button):
  
    if not self.locked :
      self.locked = True
      
      if button == 'reset': # Bot has decided it's time to soft reset
        self.cc.soft_reset()
      elif button[:5] == 'click':
        if len(button) == 5:
          self.cc.click_cookie()
        else:
          for x in range(0, int(button[5])):
            self.cc.click_cookie()
      elif button == 'golden':
        self.cc.click_golden()
      elif button == 'santa':
        self.cc.upgrade_santa()
      elif button == 'reindeer':
        self.cc.click_reindeer()
      elif button in self.cc.BLDGS:
        self.cc.buy_building(button)
      elif button[:7] == 'upgrade':
        if len(button) == 7:
          self.cc.buy_upgrade(0)
        else:
          self.cc.buy_upgrade(int(button[7])-1)
      elif button == 'scrollup':
        self.cc.scroll_up()
      elif button == 'scrolldown':
        self.cc.scroll_down()
      elif button == 'view':
        self.cc.toggle_stats()
      elif button == 'view':
        self.cc.toggle_stats()
      elif button == 'expand':
        self.cc.expand_store()
      elif button == 'collapse':
        self.cc.collapse_store()
      elif button == 'unwrinkle':
        self.cc.pop_all_wrinklers()
      elif button == 'dunk':
        self.cc.dunk_cookie()
      elif button == 'dungeon':
        self.cc.enter_dungeon()
      elif button == 'up':
        self.cc.move_up()
      elif button == 'down':
        self.cc.move_down()
      elif button == 'left':
        self.cc.move_left()
      elif button == 'right':
        self.cc.move_right()
      elif button == 'stay':
        self.cc.move_stay()     
      self.locked = False

