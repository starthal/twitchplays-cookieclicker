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
import thread


class CookieControl:
  TCP_IP = '127.0.0.1'
  TCP_PORT = 32000 # You can change this port in the FF Remote Control settings
  SCROLL_AMOUNT = 300 # Amount to scroll on scroll_up and scroll_down commands
  last_send = -10 #Arbitrary neg number as nothing has been sent yet
  dungeon_entered = False
  auto = False
  auto_start = time.clock()

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
      #Disable "One Mind" popup and enable dungeons
      self.send_js('Game.Objects["Factory"].unlockSpecial()')
      self.send_js('Game.Upgrades["One mind"].clickFunction = null')
      
      thread.start_new_thread(self.dungeon_auto, ()) #Start dungeon auto thread
    except:
      print('Could not connect. Make sure FF Remote Control is running on port 32000')
      self.sock.close()
      sys.exit(1)
    print('Connected to Firefox')

  def deinit_control(self):
    self.sock.close()

  def send_js(self, js_line):
    elapsedtime = time.clock() - self.last_send #Cannot send JS too fast, has to throttle
    if (elapsedtime < .05):
      time.sleep(.05 - elapsedtime)
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

  def upgrade_santa(self):
    query = (					'var moni=Math.pow(Game.santaLevel+1,Game.santaLevel+1);'
						'if (Game.cookies>moni && Game.santaLevel<14)'
						'{'
						'Game.Spend(moni);'
						'Game.santaLevel=(Game.santaLevel+1)%15;'
						'if (Game.santaLevel==14) {Game.Unlock("Santa\'s dominion");Game.Popup("You are granted<br>Santa\'s dominion.");}'
						'Game.santaTransition=1;'
						'var drops=[];'
                                                'for (var i in Game.santaDrops) {if (!Game.HasUnlocked(Game.santaDrops[i])) drops.push(Game.santaDrops[i]);}'
						'var drop=choose(drops);'
						'if (drop) {Game.Unlock(drop);Game.Popup("You find a present which contains...<br>"+drop+"!");}'
							
						'if (Game.santaLevel>=6) Game.Win("Coming to town");'
						'if (Game.santaLevel>=14) Game.Win("All hail Santa");'
						'}')
    self.send_js(query)

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
    self.dungeon_entered = False

  def enter_dungeon(self):
    # Dungeon can be entered without a factory, but it cannot be seen
    # before a factory is bought. Check for at least 1 factory
    jstr = self.send_js('Game.Objects["Factory"].amount')
    num_factories = json.loads(jstr)['result']
    if int(num_factories) > 0:
      self.send_js('Game.ObjectsById[3].setSpecial(1)')
      self.dungeon_entered = True

  def dungeon_auto(self):
    while True:
      if (self.dungeon_entered == True and self.auto == False and time.clock() >= self.auto_start):
        print str(self.dungeon_entered) + '\n' + str(self.auto) + '\n' + str(self.auto_start) + '\n\n\n'
        self.send_js('Game.Objects["Factory"].dungeon.auto=1;Game.Objects["Factory"].dungeon.timerWarmup=0;')
        self.auto = True

  def dungeon_manual(self):
    self.auto = False
    self.auto_start = time.clock() + 30

  # Should not move without being in the dungeon
  def move_up(self):
    if (self.dungeon_entered == True):
      self.send_js('Game.Objects["Factory"].dungeon.auto=0;Game.Objects["Factory"].dungeon.timerWarmup=-1;Game.Objects["Factory"].dungeon.hero.Move(0,-1)')
      self.dungeon_manual()

  def move_down(self):
    if (self.dungeon_entered == True):
      self.send_js('Game.Objects["Factory"].dungeon.auto=0;Game.Objects["Factory"].dungeon.timerWarmup=-1;Game.Objects["Factory"].dungeon.hero.Move(0,1)')
      self.dungeon_manual()

  def move_left(self):
    if (self.dungeon_entered == True):
      self.send_js('Game.Objects["Factory"].dungeon.auto=0;Game.Objects["Factory"].dungeon.timerWarmup=-1;Game.Objects["Factory"].dungeon.hero.Move(-1,0)')
      self.dungeon_manual()

  def move_right(self):
    if (self.dungeon_entered == True):
      self.send_js('Game.Objects["Factory"].dungeon.auto=0;Game.Objects["Factory"].dungeon.timerWarmup=-1;Game.Objects["Factory"].dungeon.hero.Move(1,0)')
      self.dungeon_manual()

  def move_stay(self):
    if (self.dungeon_entered == True):
      self.send_js('Game.Objects["Factory"].dungeon.auto=0;Game.Objects["Factory"].dungeon.timerWarmup=-1;Game.Objects["Factory"].dungeon.hero.Move(0,0)')
      self.dungeon_manual()
    
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
