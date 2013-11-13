#!/usr/bin/python

import Tkinter as tk
import ttk
import time
import requests
from collections import OrderedDict
import Queue, threading

class API(object):
    _matches_url = 'https://api.guildwars2.com/v1/wvw/matches.json'
    _worlds_url = 'https://api.guildwars2.com/v1/world_names.json'
    _match_url = 'https://api.guildwars2.com/v1/wvw/match_details.json' # ?match_id=1-7
    _objectives_url = 'https://api.guildwars2.com/v1/wvw/objective_names.json'

    # worlds = requests.get(_worlds_url).json()
    # worlds = dict((i['id'], i['name']) for i in worlds)

    worlds = {
        '1001': ('Anvil Rock', 'AR'),
        '1002': ('Borlis Pass', 'BP'),
        '1003': ("Yak's Bend", 'Yak'),
        '1004': ('Henge of Denravi', 'Hod'),
        '1005': ('Maguuma', 'Mag'),
        '1006': ("Sorrow's Furnace", 'SF'),
        '1007': ('Gate of Madness', 'GoM'),
        '1008': ('Jade Quarry', 'JQ'),
        '1009': ('Fort Aspenwood', 'FA'),
        '1010': ('Ehmry Bay', 'EB'),
        '1011': ('Stormbluff Isle', 'SBI'),
        '1012': ('Darkhaven', 'DH'),
        '1013': ('Sanctum of Rall', 'SoR'),
        '1014': ('Crystal Desert', 'CD'),
        '1015': ('Isle of Janthir', 'IoJ'),
        '1016': ('Sea of Sorrows', 'SoS'),
        '1017': ('Tarnished Coast', 'TC'),
        '1018': ('Northern Shiverpeaks', 'NSP'),
        '1019': ('Blackgate', 'BG'),
        '1020': ("Ferguson's Crossing", 'FC'),
        '1021': ('Dragonbrand', 'DB'),
        '1022': ('Kaineng', 'KE'),
        '1023': ("Devona's Rest", 'DR'),
        '1024': ('Eredon Terrace', 'ET'),
        '2001': ('Fissure of Woe', 'FW'),
        '2002': ('Desolation', 'Des'),
        '2003': ('Gandara', 'Gan'),
        '2004': ('Blacktide', 'BT'),
        '2005': ('Ring of Fire', 'RoF'),
        '2006': ('Underworld', 'UW'),
        '2007': ('Far Shiverpeaks', 'FSP'),
        '2008': ('Whiteside Ridge', 'WSR'),
        '2009': ('Ruins of Surmia', 'RoS'),
        '2010': ("Seafarer's Rest", 'SR'),
        '2011': ('Vabbi', 'Vab'),
        '2012': ('Piken Square', 'PS'),
        '2013': ('Aurora Glade', 'AG'),
        '2014': ("Gunnar's Hold", 'GH'),
        '2101': ('Jade Sea [FR]', 'JS'),
        '2102': ('Fort Ranik [FR]', 'FR'),
        '2103': ('Augury Rock [FR]', 'AR'),
        '2104': ('Vizunah Square [FR]', 'VS'),
        '2105': ('Arborstone [FR]', 'AS'),
        '2201': ('Kodash [DE]', 'Kod'),
        '2202': ('Riverside [DE]', 'RS'),
        '2203': ('Elona Reach [DE]', 'ER'),
        '2204': ("Abaddon's Mouth [DE]", 'AM'),
        '2205': ('Drakkar Lake [DE]', 'DL'),
        '2206': ("Miller's Sound [DE]", 'MS'),
        '2207': ('Dzagonur [DE]', 'Dz'),
        '2301': ('Baruch Bay [SP]', 'BB')
    }


    #objectives = requests.get(_objectives_url).json()
    #objectives = dict((int(i['id']), i['name']) for i in objectives)

    objectives = {
        1: ("Overlook", "Overlook"),
        2: ("Valley", "Valley"),
        3: ("Lowlands", "Lowlands"),
        4: ("Golanta Clearing", "Golanta"),
        5: ("Pangloss Rise", "Pangloss"),
        6: ("Speldan Clearcut", "Speldan"),
        7: ("Danelon Passage", "Danelon"),
        8: ("Umberglade Woods", "Umberglade"),
        9: ("Stonemist Castle", "SM Castle"),
        10: ("Rogue's Quarry", "Rogue's"),
        11: ("Aldon's Ledge", "Aldon's"),
        12: ("Wildcreek Run", "Wildcreek"),
        13: ("Jerrifer's Slough", "Jerrifer's"),
        14: ("Klovan Gully", "Klovan"),
        15: ("Langor Gulch", "Langor"),
        16: ("Quentin Lake", "QL"),
        17: ("Mendon's Gap", "Mendon's"),
        18: ("Anzalias Pass", "Anzalias"),
        19: ("Ogrewatch Cut", "Ogrewatch"),
        20: ("Veloka Slope", "Veloka"),
        21: ("Durios Gulch", "Durios"),
        22: ("Bravost Escarpment", "Bravost"),
        23: ("Garrison", "Garrison"),
        24: ("Champion's demense", "Champion's"),
        25: ("Redbriar", "Redbriar"),
        26: ("Greenlake", "Greenlake"),
        27: ("Ascension Bay", "Bay"),
        28: ("Dawn's Eyrie", "Dawn's"),
        29: ("The Spiritholme", "Spirit"),
        30: ("Woodhaven", "Woodhaven"),
        31: ("Askalion Hills", "Hills"),
        32: ("Etheron Hills", "Hills"),
        33: ("Dreaming Bay", "Bay"),
        34: ("Victors's Lodge", "Victors's"),
        35: ("Greenbriar", "Greenbriar"),
        36: ("Bluelake", "Bluelake"),
        37: ("Garrison", "Garrison"),
        38: ("Longview", "Longview"),
        39: ("The Godsword", "Godsword"),
        40: ("Cliffside", "Cliffside"),
        41: ("Shadaran Hills", "Hills"),
        42: ("Redlake", "Redlake"),
        43: ("Hero's Lodge", "Hero's"),
        44: ("Dreadfall Bay", "Bay"),
        45: ("Bluebriar", "Bluebriar"),
        46: ("Garrison", "Garrison"),
        47: ("Sunnyhill", "Sunnyhill"),
        48: ("Faithleap", "Faithleap"),
        49: ("Bluevale Refuge", "Bluevale"),
        50: ("Bluewater Lowlands", "Bluewater"),
        51: ("Astralholme", "Astralholme"),
        52: ("Arah's Hope", "Arah's"),
        53: ("Greenvale Refuge", "Greenvale"),
        54: ("Foghaven", "Foghaven"),
        55: ("Redwater Lowlands", "Redwater"),
        56: ("The Titanpaw", "Titanpaw"),
        57: ("Cragtop", "Cragtop"),
        58: ("Godslore", "Godslore"),
        59: ("Redvale Refuge", "Redvale"),
        60: ("Stargrove", "Stargrove"),
        61: ("Greenwater Lowlands", "Greenwater"),
        62: ("Temple of Lost Prayers", "S Ruin"), # Ruins from here
        63: ("Battle's Hollow", "SW Ruin"),
        64: ("Bauer's Estate", "NW Ruin"),
        65: ("Orchard Overlook", "NE Ruin"),
        66: ("Carver's Ascent", "SE Ruin"),
        67: ("Carver's Ascent", "SE Ruin"),
        68: ("Orchard Overlook", "NE Ruin"),
        69: ("Bauer's Estate", "Ruin"),
        70: ("Battle's Hollow", "SW Ruin"),
        71: ("Temple of Lost Prayers", "S Ruin"),
        72: ("Carver's Ascent", "SE Ruin"),
        73: ("Orchard Overlook", "NE Ruin"),
        74: ("Bauer's Estate", "NW Ruin"),
        75: ("Battle's Hollow", "SW Ruin"),
        76: ("Temple of Lost Prayers", "S Ruin")
    }


    abbreviated_bl = OrderedDict((
        ('RedHome', 'R'),
        ('GreenHome', 'G'),
        ('BlueHome', 'B'),
        ('Center', 'EB')
    ))

    matches = requests.get(_matches_url).json()['wvw_matches']

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
    def __init__(self, world, _map, update_interval=10):
        self.root = tk.Tk()
        self.controls = ttk.Frame(self.root)
        self.frame = ttk.Frame(self.root)
        self.world = world
        self.map = tk.StringVar(value=API.abbreviated_bl.keys()[_map])
        self.match = API.get_match(self.world)

        self.content = {}
        self.timers = {}
        self.update_interval = update_interval
        self.ri_init = 300 #initial Righteous Indignation time

        self.data_queue = Queue.Queue()
        self.stop_thread = threading.Event()

        self.setup()
        self.data_thread = threading.Thread(target=self.update_data)
        self.data_thread.daemon = True
        self.data_thread.start()

    def setup(self):
        self.map_buttons = []
        for i, (_map, bl) in enumerate(API.abbreviated_bl.iteritems()):
            r = ttk.Radiobutton(self.controls, text=bl, variable=self.map, value=_map, command=self.change_map)
            r.configure(text=API.abbreviated_bl[_map], value=_map)
            r['style'] = _map + '.TRadiobutton'
            r.grid(column=i, row=0)

        self.controls.grid(column=0, row=0, sticky=(tk.W))
        self.frame.grid(column=0, row=1, sticky=(tk.N, tk.E, tk.S, tk.W))
        self.frame.grid_columnconfigure(0, minsize=90)

        self.root.wm_title('GW2Intel')
        self.root.overrideredirect(True)
        self.root.resizable(False, False)
        self.root.wm_attributes('-topmost', True)
        self.root.attributes("-alpha", 0.7)
        self.root.wm_geometry('+0+{}'.format(400))
        self.root.minsize(140, 1)

        DragBehavior(self.root, 'x')
        self.root.bind('<Control-ButtonRelease-3>', lambda e: self.root.destroy())
        #self.root.bind('<Button-2>', lambda e: self.root.wm_geometry(''))
        self.root.bind('<<DataFetch>>', self.create_content)
        self.root.bind('<Destroy>', lambda e: self.stop_thread.set())

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

    def change_map(self):
        for _map, objectives in self.content.iteritems():
            for _, (label, timer, _) in objectives.iteritems():
                self.hide(label, timer)
        self.update_timers()

    def create_content(self, _):
        for child in self.frame.winfo_children(): child.destroy()
        self.content.clear()
        self.timers.clear()
        row = 0

        for _map, objectives in self.data_queue.get().iteritems():
            self.content[_map] = {}

            for objective, owner in objectives.iteritems():
                objective_name = API.objectives[objective][1]

                if objective >= 62: continue #skip ruins

                label = ttk.Label(self.frame, text=objective_name, style=owner + '.TLabel')
                timer = ttk.Label(self.frame, text='', style='timer.TLabel')
                self.show(label, timer, row)

                self.content[_map][objective] = (label, timer, row)
                self.timers[objective] = [owner, False]
                row += 1

        self.separator = ttk.Separator(self.frame)
        self.separator.grid(columnspan=2)
        self.change_map()
        self.root.unbind('<<DataFetch>>')
        self.root.bind('<<DataFetch>>', self.update_content)

    def update_data(self):
        while not self.stop_thread.is_set():
            self.data_queue.put(API.get_objectives(self.match['wvw_match_id']))
            try:
                self.root.event_generate('<<DataFetch>>')
            except RuntimeError: #mainloop stopped, program ended
                break
            else:
                self.stop_thread.wait(self.update_interval)

    def update_content(self, _):
        now = time.time()
        for _map, objectives in self.data_queue.get().iteritems():
            for objective, owner in objectives.iteritems():
                if objective >= 62: continue #skip ruins

                label, timer, row = self.content[_map][objective]
                last_owner = self.timers[objective][0]

                if owner != last_owner:
                    label['style'] = owner + '.TLabel'
                    self.timers[objective][0] = owner
                    self.timers[objective][1] = now

    def update_timers(self, endless=True):
        now = time.time()

        for objective, (label, timer, row) in self.content[self.map.get()].iteritems():
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

        if endless:
            self.root.after(1000, self.update_timers)

    def hide(self, label, timer):
        label.grid_forget()
        timer.grid_forget()

    def show(self, label, timer, row):
        label.grid(column=0, row=row, sticky=(tk.W))
        timer.grid(column=1, row=row, sticky=(tk.E))

if __name__ == '__main__':
    app = GW2Intel(1006, 2)
    try:
        app.root.mainloop()
    except KeyboardInterrupt:
        app.root.destroy()

