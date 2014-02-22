#import win32api
#import win32con
import time
import cookiecontrol
from gui import set_pledge_bar
from config.config import config

class Game:

  BUTTONS = {
    'click',
    'upgrade',
    'upgrade1',
    'upgrade2',
    'upgrade3',
    'upgrade4',
    'upgrade5',
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
    'reindeer',
    'scrollup',
    'scrolldown',
    'view',
    'expand',
    'collapse',
    'restart',
    'continue',
    #'unwrinkle',
  }
  
  locked = False
  cc = cookiecontrol.CookieControl()
  pledge_counter = 0
  pledge_max = config['pledge_bar']['max']

  def get_valid_buttons(self):
      return [button for button in self.BUTTONS]

  def is_valid_button(self, button):
      return button in self.BUTTONS

  def push_button(self, button):
  
    if not self.locked :
      self.locked = True
      
    if button == 'restart': # Bot has decided it's time to soft reset
      self.cc.soft_reset()
    elif button == 'click':
      self.cc.click_cookie()
    elif button == 'golden':
      self.cc.click_golden()
    elif button == 'reindeer':
      self.cc.click_reindeer()
    elif button in self.cc.BLDGS:
      self.cc.buy_building(button)
    elif button[:7] == 'upgrade':
      # Last char of the button is the upgrade number, but array starts at 0
      if len(button) == 7:
        upgrade_ind = 0
      else:
          upgrade_ind = int(button[7])-1
      # Check if upgrade is pledge
      name = self.cc.upgrade_name(upgrade_ind)
      if name == 'Elder Pledge' or name == 'Elder Covenant':
        # Throttle pledges if necessary
        self.pledge_counter += 1
        if self.pledge_counter >= pledge_max:
          self.cc.buy_upgrade(upgrade_ind)
          self.pledge_counter = 0
        set_pledge_bar(self.pledge_counter)          
      else:
        self.cc.buy_upgrade(upgrade_ind)
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
    self.locked = False

