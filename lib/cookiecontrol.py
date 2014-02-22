#!/usr/bin/env python

# Cookie Clicker Python Control module
# Author: starthal
# Version 1.0

# This requires the use of Firefox and the extension "Remote Control"
# https://addons.mozilla.org/en-US/firefox/addon/remote-control/
# Be sure to turn the remote on using the toolbar button!

# Cookie Clicker "API" reference: http://cookieclicker.wikia.com/wiki/Cheating

import socket
import json
import sys
import time


class CookieControl:
  TCP_IP = '127.0.0.1'
  TCP_PORT = 32000 # You can change this port in the FF Remote Control settings
  SCROLL_AMOUNT = 300 # Amount to scroll on scroll_up and scroll_down commands
  last_send = -10 #Arbitrary neg number as nothing has been sent yet

  # Dict of building IDs.
  BLDGS = {
    'cursor':     0,
    'grandma':    1,
    'farm':       2,
    'factory':    3,
    'mine':       4,
    'shipment':   5,
    'lab':        6,
    'portal':     7,
    'time':       8,
    'antimatter': 9,
    'prism':      10,
  }


  # Backs up the save string (use before a reset)
  def backup_save(self, save_str):
    save_f = open('twitch_cc_save_backup.txt', 'a')
    save_f.write(time.asctime() + '\n' + save_str + '\n\n')
    save_f.close()

  # Connect to FF-Remote
  def init_control(self):
    try:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.settimeout(0.5)
      self.sock.connect((self.TCP_IP, self.TCP_PORT))
      #Disable "One Mind" popup and autokill wrinklers every 5 hours
      self.send_js("Game.Upgrades['One mind'].clickFunction = null") 
      self.send_js("if (!wrinklerkiller) {wrinklerkiller = setInterval(function() { for (var i=0;i<10;i++) { if (Game.wrinklers[i].close==1) {Game.wrinklers[i].hp = 0}}}, 18000000);}")
    except:
      print('Could not connect. Make sure FF Remote Control is running on port 32000')
      self.sock.close()
      sys.exit(1)
    print('Connected to Firefox')

  def deinit_control(self):
    self.sock.close()

  def send_js(self, js_line):
    elapsedtime = time.clock() - self.last_send #Cannot send JS too fast, has to throttle
    if (elapsedtime < .1):
      time.sleep(.1 - elapsedtime)
    self.sock.send(js_line)
    self.last_send = time.clock()
    try:
      ret = self.sock.recv(4096)
    except:
      ret = ''
    return ret

  def click_cookie(self):
    self.send_js('Game.ClickCookie()')

  def click_golden(self):
    self.send_js('Game.goldenCookie.click()')
    
  def click_reindeer(self):
    self.send_js('Game.seasonPopup.click()')

  def buy_building(self, bldg_name):
    bldg_id = self.BLDGS[bldg_name]
    #print('Building id is {0}'.format(bldg_id))
    self.send_js('Game.ObjectsById[{0}].buy()'.format(bldg_id))

  def sell_building(self, bldg_name):
    bldg_id = self.BLDGS[bldg_name]
    #print('Building id is {0}'.format(bldg_id))
    self.send_js('Game.ObjectsById[{0}].sell()'.format(bldg_id))

  def buy_upgrade(self, upgrade_index):
    # First upgrade has index 0
    self.send_js('Game.UpgradesInStore[{0}].buy()'.format(upgrade_index))

  def upgrade_name(self, upgrade_index):
    jstr = self.send_js('Game.UpgradesInStore[{0}].name'.format(upgrade_index))
    try:
      name = json.loads(jstr)['result']
    except KeyError:
      name = 'x'
    return name

  def pop_all_wrinklers(self):
    self.send_js('Game.CollectWrinklers()')
    
  def scroll_down(self):
    self.send_js('document.getElementById("sectionMiddle").scrollTop+={0}'.format(self.SCROLL_AMOUNT))

  def scroll_up(self):
    self.send_js('document.getElementById("sectionMiddle").scrollTop-={0}'.format(self.SCROLL_AMOUNT))

  def toggle_stats(self):
    self.send_js('Game.ShowMenu("stats")')

  def expand_store(self):
    self.send_js('document.getElementById("upgrades").style.height="auto"')

  def collapse_store(self):
    self.send_js('document.getElementById("upgrades").style.height="60px"')
    
  def dunk_cookie(self):
    self.send_js('Game.Win("Cookie-dunker")')

  def soft_reset(self):
    # Export save.
    # The indexing [11:-3] strips the JSON wrapper
    jstr = self.send_js('Game.WriteSave(1)')
    save_str = json.loads(jstr)['result']
    self.backup_save(save_str)
    # Passing the argument 1 bypasses the confirmation dialog
    self.send_js('Game.Reset(1)')
    hc_calc_js = (  'var prestige=0;'
                    'if (Game.prestige.ready) prestige=Game.prestige["Heavenly chips"];'
                    'Game.prestige=[];'
                    'Game.CalculatePrestige();'
                    'prestige=Game.prestige["Heavenly chips"]-prestige;'
                    'if (prestige!=0) Game.Popup("You earn "+prestige+" heavenly chip"+(prestige==1?"":"s")+"!");')
    self.send_js(hc_calc_js)

  def __init__(self):
    self.init_control()

# Main routine for testing
if __name__ == "__main__":

  s = CookieControl()

  while True:
    try:
      print('Clicking cookie')
      s.click_cookie()
      time.sleep(2)
    
      #  print('Buying farm')
      #  buy_building(s, 'farm')
      #  time.sleep(5)

      print ('Scrolling down')
      s.scroll_down()
      time.sleep(2)
    except:
      s.deinit_control()
      sys.exit(0)
