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
    w4.insert(END, '\n{0:<25s} {1:>14s}'.format(username[:25], command[:14]))
    w4.see(END)

def run():
    global w4
    global rscroll
    global pscroll
    
    master = Tk()
    master.configure(background='pink')
    w4 = Text (master, background='#1E506F', foreground='white', width=40, height=10)
    w4.insert(INSERT, "-----START-----")
    w4.grid(row=0, rowspan=2, column=0, sticky=W+E+N+S)
    
    rscroll_max = config['reset_bar']['max']
    rscroll = Scale(master, from_=rscroll_max, to=0, highlightthickness=0, activebackground='#1E506F', state=ACTIVE, borderwidth=0, background='black', foreground='white', troughcolor='#FF1144')
    rscroll.grid(row=0, column=1, sticky=W+E+N+S)
    
    if config['pledge_bar']['enable']:
		pscroll_max = config['pledge_bar']['max']
		pscroll = Scale(master, from_=pscroll_max, to=0, highlightthickness=0, activebackground='#1E506F', state=ACTIVE, borderwidth=0, background='black', foreground='white', troughcolor='white')
		pscroll.grid(row=0, column=2, sticky=W+E+N+S)

    rlabel = Label(master, text="Reset", background='black', foreground='#FF1144')
    rlabel.grid(row=1, column=1, sticky=W+E+N+S)

    plabel = Label(master, text="Pledge\nCov", background = 'black', foreground='white')
    plabel.grid(row=1, column=2, sticky=W+E+N+S)
 
    mainloop()

