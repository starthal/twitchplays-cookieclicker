from Tkinter import *
#import tkFont
from config.config import config

def set_pledge_bar(pledge_counter):
    global pscroll
    pscroll.set(pledge_counter)

def set_reset_bar(reset_counter):
    global rscroll
    rscroll.set(reset_counter)

def command(username, command):
    global w4    
    w4.insert(END, '\n{0:<25s} {1:>24s}'.format(username[:25], command[:24]))
    w4.see(END)

def run():
    global w4
    global rscroll
    global pscroll
    
    master = Tk()
    w4 = Text (master, background='black', foreground='white', width=36, height=10)
    w4.insert(INSERT, "-----START-----")
    w4.pack(fill=BOTH, expand=1, side=LEFT)
    
    rscroll_max = config['reset_bar']['max']
    rscroll = Scale(master, from_=rscroll_max, to=0, borderwidth=0, background='black', foreground='white', troughcolor='white')
    rscroll.pack(fill=BOTH, expand=0, side=RIGHT)
    
    if config['pledge_bar']['enable']:
		pscroll_max = config['pledge_bar']['max']
		pscroll = Scale(master, from_=pscroll_max, to=0, borderwidth=0, background='black', foreground='white', troughcolor='blue')
		pscroll.pack(fill=BOTH, expand=0, side=RIGHT)
 
    mainloop()

