from config.config import config
import cookiecontrol

class Timer():
    def __init__ (self, hour, minute, second):
        self.hour=hour
        self.minute=minute
        self.second=second+1

        self.update_time()

        self.cc = cookiecontrol.CookieControl()

    def update_time (self):
        hour = self.hour

        curr_time=hour*3600+self.minute*60+self.second
        update_time=curr_time-1
        if update_time < 0:
            self.cc.pop_all_wrinklers()
            update_time = (3600 * config['pop_timer']['hours']) + (60 * config['pop_timer']['minutes']) + config['pop_timer']['seconds']

        self.hour=update_time//3600
        self.minute=update_time%3600//60
        self.second=update_time%60
        
        if self.minute >= 10:
            minutestring = str(self.minute)
        else:
            minutestring = '0'+str(self.minute)
        if self.second >= 10:
            secondstring = str(self.second)
        else:
            secondstring = '0'+str(self.second)
        
        self.show_time='0'+str(self.hour)+':'+str(minutestring)+':'+str(secondstring)
        
        return self.show_time
