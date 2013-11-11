#!/usr/bin/python

import Tkinter as tk
import ttk
import time
import requests

class API(object):
    _matches_url = 'https://api.guildwars2.com/v1/wvw/matches.json'
    _worlds_url = 'https://api.guildwars2.com/v1/world_names.json'
    _match_url = 'https://api.guildwars2.com/v1/wvw/match_details.json' # ?match_id=1-7
    _objectives_url = 'https://api.guildwars2.com/v1/wvw/objective_names.json'

    worlds = requests.get(_worlds_url).json()
    worlds = dict((i['id'], i['name']) for i in worlds)

    matches = requests.get(_matches_url).json()['wvw_matches']

    objectives = requests.get(_objectives_url).json()
    objectives = dict((int(i['id']), i['name']) for i in objectives)

    @classmethod
    def get_match(cls, world_id):
        for i in cls.matches:
            if i['blue_world_id'] == world_id or i['red_world_id'] == world_id or i['green_world_id'] == world_id:
                return i
        return None

    @classmethod
    def get_map_objectives(cls, match_id, selected_map):
        match_details = requests.get(cls._match_url, params={'match_id': match_id}).json()
        map_objectives = match_details['maps'][selected_map]['objectives']
        map_objectives = dict((i['id'], i['owner']) for i in map_objectives)
        return map_objectives


class DragBehavior(object):
    ''' Makes a window dragable. '''

    def __init__ (self, parent, disable_axis=None, release_cb=None) :
        self.parent = parent
        self.disable_axis = disable_axis

        self.release_cb = release_cb

        self.parent.bind('<Button-1>', self.relative_position)
        self.parent.bind('<ButtonRelease-1>', self.drag_unbind)

    def relative_position (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        x = self.parent.winfo_x()
        y = self.parent.winfo_y()

        self.OriX = x
        self.OriY = y

        self.RelX = cx - x
        self.RelY = cy - y

        self.parent.bind('<Motion>', self.on_motion)

    def on_motion (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        d = self.disable_axis

        if d == 'x':
            x = self.OriX
            y = cy - self.RelY
        elif d == 'y':
            x = cx - self.RelX
            y = self.OriY
        else:
            x = cx - self.RelX
            y = cy - self.RelY

        if x < -100 :
            x = 0
        if y < -100 :
            y = 0

        self.parent.wm_geometry('+' + str(x) + '+' + str(y))

    def drag_unbind (self, event):
        self.parent.unbind('<Motion>')

        if self.release_cb:
            self.release_cb()

    def stop_drag_behavior (self):
        self.parent.unbind('<Button-1>')
        self.parent.unbind('<ButtonRelease-1>')
        self.parent.unbind('<Motion>')


class GW2Intel(object):
    def __init__(self, world, _map, update_interval=10000):
        self.root = tk.Tk()
        self.world = world
        self.map = _map
        self.match = API.get_match(self.world)
        
        self.content = {}
        self.timers = {}
        self.update_interval = update_interval

        self._orig = (-1, -1)
        self.setup()

        self.create_content()
        self.update_content()
        self.update_timers()

    def setup(self):
        self.root.wm_title('GW2Intel')
        self.root.overrideredirect(True)
        self.root.resizable(False, False)
        self.root.wm_attributes('-topmost', True)
        self.root.attributes("-alpha", 0.7)
        self.root.wm_geometry('+0+{}'.format(100))

        DragBehavior(self.root, 'x')
        self.root.bind('<Button-3>', lambda e: self.root.destroy())

        s = ttk.Style()
        s.configure('Red.TLabel', foreground='red')
        s.configure('Blue.TLabel', foreground='blue')
        s.configure('Green.TLabel', foreground='green')
        s.configure('Neutral.TLabel', foreground='black')
        s.configure('timer.TLabel', font='TkDefaultFont 9')
        s.configure('soon.TLabel', font='TkDefaultFont 9 bold')

    def create_content(self):
        self.content.clear()
        self.timers.clear()

        for row, (objective, owner) in enumerate(API.get_map_objectives(self.match['wvw_match_id'], self.map).iteritems()):
            objective_name = API.objectives[objective]
            if objective_name.startswith('(('): continue #skip ruins
            
            label = ttk.Label(text=objective_name, style=owner + '.TLabel')
            label.grid(column=0, row=row, sticky=(tk.W))

            timer = ttk.Label(text='', style='timer.TLabel')
            timer.grid(column=1, row=row, sticky=(tk.E))

            self.content[objective] = (label, timer, row)
            self.timers[objective] = [owner, False]

    def update_content(self):
        for i, (objective, owner) in enumerate(API.get_map_objectives(self.match['wvw_match_id'], self.map).iteritems()):
            if API.objectives[objective].startswith('(('): continue #skip ruins
            
            olabel, timer, row = self.content[objective]
            last_owner = self.timers[objective][0]

            if owner != last_owner:
                olabel['style'] = owner + '.TLabel'
                self.timers[objective][0] = owner
                self.timers[objective][1] = time.time()

        self.root.after(self.update_interval, self.update_content)

    def update_timers(self):
        now = time.time()
        for objective, (label, timer, row) in self.content.iteritems():
            obj_timer = self.timers[objective][1]
            if obj_timer:
                delta = now - obj_timer
                if delta < 300:
                    label.grid(column=0, row=row, sticky=(tk.W))
                    timer.grid(column=1, row=row, sticky=(tk.E))
                    timer.configure(text=time.strftime('%M:%S', time.localtime(300 - delta)))
                    if delta < 60:
                        timer['style'] = 'soon.TLabel'
                    else:
                        timer['style'] = 'timer.TLabel'
                else:
                    label.grid_forget()
                    timer.grid_forget()
                    timer.configure(text='')
            else:
                # label.grid_forget()
                # timer.grid_forget()
                timer.configure(text='')
        self.root.after(1000, self.update_timers)


if __name__ == '__main__':
    app = GW2Intel(1006, 2)
    app.root.mainloop()

