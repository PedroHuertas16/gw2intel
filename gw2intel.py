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

    # worlds = requests.get(_worlds_url).json()
    # worlds = dict((i['id'], i['name']) for i in worlds)

    worlds = {
        '1001': 'Anvil Rock',
        '1002': 'Borlis Pass',
        '1003': "Yak's Bend",
        '1004': 'Henge of Denravi',
        '1005': 'Maguuma',
        '1006': "Sorrow's Furnace",
        '1007': 'Gate of Madness',
        '1008': 'Jade Quarry',
        '1009': 'Fort Aspenwood',
        '1010': 'Ehmry Bay',
        '1011': 'Stormbluff Isle',
        '1012': 'Darkhaven',
        '1013': 'Sanctum of Rall',
        '1014': 'Crystal Desert',
        '1015': 'Isle of Janthir',
        '1016': 'Sea of Sorrows',
        '1017': 'Tarnished Coast',
        '1018': 'Northern Shiverpeaks',
        '1019': 'Blackgate',
        '1020': "Ferguson's Crossing",
        '1021': 'Dragonbrand',
        '1022': 'Kaineng',
        '1023': "Devona's Rest",
        '1024': 'Eredon Terrace',
        '2001': 'Fissure of Woe',
        '2002': 'Desolation',
        '2003': 'Gandara',
        '2004': 'Blacktide',
        '2005': 'Ring of Fire',
        '2006': 'Underworld',
        '2007': 'Far Shiverpeaks',
        '2008': 'Whiteside Ridge',
        '2009': 'Ruins of Surmia',
        '2010': "Seafarer's Rest",
        '2011': 'Vabbi',
        '2012': 'Piken Square',
        '2013': 'Aurora Glade',
        '2014': "Gunnar's Hold",
        '2101': 'Jade Sea [FR]',
        '2102': 'Fort Ranik [FR]',
        '2103': 'Augury Rock [FR]',
        '2104': 'Vizunah Square [FR]',
        '2105': 'Arborstone [FR]',
        '2201': 'Kodash [DE]',
        '2202': 'Riverside [DE]',
        '2203': 'Elona Reach [DE]',
        '2204': "Abaddon's Mouth [DE]",
        '2205': 'Drakkar Lake [DE]',
        '2206': "Miller's Sound [DE]",
        '2207': 'Dzagonur [DE]',
        '2301': 'Baruch Bay [SP]'
    }

    matches = requests.get(_matches_url).json()['wvw_matches']

    #objectives = requests.get(_objectives_url).json()
    #objectives = dict((int(i['id']), i['name']) for i in objectives)

    objectives = {
        1: "Overlook",
        2: "Valley",
        3: "Lowlands",
        4: "Golanta Clearing",
        5: "Pangloss Rise",
        6: "Speldan Clearcut",
        7: "Danelon Passage",
        8: "Umberglade Woods",
        9: "Stonemist Castle",
        10: "Rogue's Quarry",
        11: "Aldon's Ledge",
        12: "Wildcreek Run",
        13: "Jerrifer's Slough",
        14: "Klovan Gully",
        15: "Langor Gulch",
        16: "Quentin Lake",
        17: "Mendon's Gap",
        18: "Anzalias Pass",
        19: "Ogrewatch Cut",
        20: "Veloka Slope",
        21: "Durios Gulch",
        22: "Bravost Escarpment",
        23: "Garrison",
        24: "Champion's demense",
        25: "Redbriar",
        26: "Greenlake",
        27: "Ascension Bay",
        28: "Dawn's Eyrie",
        29: "The Spiritholme",
        30: "Woodhaven",
        31: "Askalion Hills",
        32: "Etheron Hills",
        33: "Dreaming Bay",
        34: "Victors's Lodge",
        35: "Greenbriar",
        36: "Bluelake",
        37: "Garrison",
        38: "Longview",
        39: "The Godsword",
        40: "Cliffside",
        41: "Shadaran Hills",
        42: "Redlake",
        43: "Hero's Lodge",
        44: "Dreadfall Bay",
        45: "Bluebriar",
        46: "Garrison",
        47: "Sunnyhill",
        48: "Faithleap",
        49: "Bluevale Refuge",
        50: "Bluewater Lowlands",
        51: "Astralholme",
        52: "Arah's Hope",
        53: "Greenvale Refuge",
        54: "Foghaven",
        55: "Redwater Lowlands",
        56: "The Titanpaw",
        57: "Cragtop",
        58: "Godslore",
        59: "Redvale Refuge",
        60: "Stargrove",
        61: "Greenwater Lowlands",
        62: "Temple of Lost Prayers", # Ruins from here
        63: "Battle's Hollow",
        64: "Bauer's Estate",
        65: "Orchard Overlook",
        66: "Carver's Ascent",
        67: "Carver's Ascent",
        68: "Orchard Overlook",
        69: "Bauer's Estate",
        70: "Battle's Hollow",
        71: "Temple of Lost Prayers",
        72: "Carver's Ascent",
        73: "Orchard Overlook",
        74: "Bauer's Estate",
        75: "Battle's Hollow",
        76: "Temple of Lost Prayers"
    }

    abbrv_bl = {
        'RedHome': 'R',
        'GreenHome': 'G',
        'BlueHome': 'B',
        'Center': 'EB'
    }

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

    @classmethod
    def get_objectives(cls, match_id):
        match_details = requests.get(cls._match_url, params={'match_id': match_id}).json()
        objectives = {}
        for _map in match_details['maps']:
            objectives[_map['type']] = dict((i['id'], i['owner']) for i in _map['objectives'])
        return objectives


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
        self.controls = ttk.Frame(self.root)
        self.frame = ttk.Frame(self.root)
        self.world = world
        self.map = tk.IntVar(value=_map)
        self.match = API.get_match(self.world)

        self.content = {}
        self.timers = {}
        self.update_interval = update_interval
        self.ri_init = 300 #initial Righteous Indignation time

        self._orig = (-1, -1)
        self.setup()

        self.create_content()
        self.update_timers()

    def change_map(self):
        for i, (_map, objectives) in enumerate(self.content.iteritems()):
            if self.map.get() == i:
                for _, (label, timer, row) in objectives.iteritems():
                    self.show(label, timer, row)
            else:
                for _, (label, timer, _) in objectives.iteritems():
                    self.hide(label, timer)
        self.root.wm_geometry("")

    def setup(self):
        self.radiobuttons = (
            ttk.Radiobutton(self.controls, text='0', variable=self.map, value=0, command=self.change_map),
            ttk.Radiobutton(self.controls, text='1', variable=self.map, value=1, command=self.change_map),
            ttk.Radiobutton(self.controls, text='2', variable=self.map, value=2, command=self.change_map),
            ttk.Radiobutton(self.controls, text='3', variable=self.map, value=3, command=self.change_map),
        )
        for i, checkbox in enumerate(self.radiobuttons):
            checkbox.grid(column=i, row=0)

        self.controls.grid(column=0, row=0, sticky=(tk.W))
        self.frame.grid(column=0, row=1, sticky=(tk.N, tk.E, tk.S, tk.W))

        self.root.wm_title('GW2Intel')
        self.root.overrideredirect(True)
        self.root.resizable(False, False)
        self.root.wm_attributes('-topmost', True)
        self.root.attributes("-alpha", 0.7)
        self.root.wm_geometry('+0+{}'.format(300))
        self.root.minsize(180, 1)

        DragBehavior(self.root, 'x')
        self.root.bind('<Button-3>', lambda e: self.root.destroy())
        self.root.bind('<Button-3>', lambda e: self.root.wm_geometry(''))

        s = ttk.Style()
        s.configure('Red.TLabel', foreground='red')
        s.configure('Blue.TLabel', foreground='blue')
        s.configure('Green.TLabel', foreground='green')
        s.configure('Neutral.TLabel', foreground='black')
        s.configure('timer.TLabel', font='TkDefaultFont 9')
        s.configure('soon.TLabel', font='TkDefaultFont 9 bold')
        #s.configure('TButton', padding='')
        #s.configure('TFrame', background="#f3d847")
        s.configure('GreenHome.TRadiobutton', foreground='green')
        s.configure('BlueHome.TRadiobutton', foreground='blue')
        s.configure('RedHome.TRadiobutton', foreground='red')
        s.configure('Center.TRadiobutton', foreground='black')

    def create_content(self):
        self.content.clear()
        self.timers.clear()
        row = 0

        for i, (_map, objectives) in enumerate(API.get_objectives(self.match['wvw_match_id']).iteritems()):
            self.radiobuttons[i].configure(text=API.abbrv_bl[_map])
            self.radiobuttons[i]['style'] = _map + '.TRadiobutton'
            self.content[_map] = {}

            for objective, owner in objectives.iteritems():
                objective_name = API.objectives[objective]
                if objective >= 62: continue #skip ruins

                label = ttk.Label(self.frame, text=objective_name, style=owner + '.TLabel')
                label.grid(column=0, row=row, sticky=(tk.W))

                timer = ttk.Label(self.frame, text='', style='timer.TLabel')
                timer.grid(column=1, row=row, sticky=(tk.E))

                self.content[_map][objective] = (label, timer, row)
                self.timers[objective] = [owner, False]
                row += 1

        self.change_map()
        self.root.after(self.update_interval, self.update_content)

    def update_content(self):
        now = time.time()
        for _map, objectives in API.get_objectives(self.match['wvw_match_id']).iteritems():
            for objective, owner in objectives.iteritems():
                if objective >= 62: continue #skip ruins

                label, timer, row = self.content[_map][objective]
                last_owner = self.timers[objective][0]

                if owner != last_owner:
                    label['style'] = owner + '.TLabel'
                    self.timers[objective][0] = owner
                    self.timers[objective][1] = now

        self.root.after(self.update_interval, self.update_content)

    def update_timers(self):
        now = time.time()
        map_name = self.content.keys()[self.map.get()]

        for objective, (label, timer, row) in self.content[map_name].iteritems():
            obj_timer = self.timers[objective][1]
            
            if obj_timer is not False:
                ri_time = self.ri_init - (now - obj_timer)
                
                if ri_time > 0:
                    self.show(label, timer, row)
                    timer.configure(text=time.strftime('%M:%S', time.localtime(ri_time)))
                    if ri_time < 60: # one minute left
                        timer['style'] = 'soon.TLabel'
                    else:
                        timer['style'] = 'timer.TLabel'
                else:
                    self.hide(label, timer)
                    timer.configure(text='')
            else:
                self.hide(label, timer)
                timer.configure(text='')
        self.root.wm_geometry("")
        self.root.after(1000, self.update_timers)

    def hide(self, label, timer):
        label.grid_forget()
        timer.grid_forget()

    def show(self, label, timer, row):
        label.grid(column=0, row=row, sticky=(tk.W))
        timer.grid(column=1, row=row, sticky=(tk.E))

if __name__ == '__main__':
    app = GW2Intel(1006, 2)
    app.root.mainloop()

