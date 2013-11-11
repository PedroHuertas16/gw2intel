#!/usr/bin/python

import Tkinter as tk
import ttk
import time


class GW2Intel(object):
    def __init__(self, update_interval=10000):
        self.root = tk.Tk()
        self.api = {'34': 'red', '35': 'blue', '36': 'green'}
        self.content = {}
        self.timers = {}
        self.first_time = True
        self.update_interval = update_interval

        self.setup()

        self.create_content()
        self.update_content()
        self.update_timers()

    def setup(self):
        self.root.wm_title('GW2Intel')
        self.root.wm_attributes('-topmost', True)
        self.root.wm_geometry('+0+{}'.format(100))

        s = ttk.Style()
        s.configure('red.TLabel', foreground='red')
        s.configure('blue.TLabel', foreground='blue')
        s.configure('green.TLabel', foreground='green')
        #s.configure('timer.TLabel')
        s.configure('soon.TLabel', font='TkDefaultFont 9 bold')

    def create_content(self):
        self.content.clear()
        self.timers.clear()
        now = time.time()

        for row, (objective, owner) in enumerate(self.api.iteritems()):
            label = ttk.Label(text=objective, style=owner + '.TLabel')
            label.grid(column=0, row=row, sticky=(tk.W))

            timer = ttk.Label(text='', style='timer.TLabel')
            timer.grid(column=1, row=row, sticky=(tk.E))

            self.content[objective] = (label, timer, row)
            self.timers[objective] = (owner, now)

        self.first_time = now

    def update_content(self):
        for i, (objective, owner) in enumerate(self.api.iteritems()):
            olabel, timer, row = self.content[objective]
            last_owner = self.timers[objective][0]

            if owner != last_owner:
                olabel['style'] = owner + '.TLabel'
                self.timers[objective][1] = time.time()

        self.root.after(self.update_interval, self.update_content)

    def update_timers(self):
        now = time.time()
        if self.first_time and now - self.first_time > 300:
            self.first_time = False
            return
        for objective, (label, timer, row) in self.content.iteritems():
            delta = now - self.timers[objective][1]
            if delta < 300:
                label.grid(column=0, row=row, sticky=(tk.W))
                timer.grid(column=1, row=row, sticky=(tk.E))
                timer.configure(text=time.strftime('%M:%S', time.localtime(300 - delta)))
                if delta < 60:
                    timer['style'] = 'soon.TLabel'
                else:
                    timer['style'] = 'TLabel'

            else:
                timer.configure(text='')
                label.grid_forget()
        self.root.after(1000, self.update_timers)


if __name__ == '__main__':
    app = GW2Intel()
    app.root.mainloop()

