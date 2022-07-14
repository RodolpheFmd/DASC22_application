from bluesky.tools.geo import latlondist, qdrdist
import Multi_agent.settings as set
from bluesky import stack, traf

class Agent:
    def __init__(self, name, speed, origin, destination):
        self.name = name

        self.color = 'Lime'
        self.tactical_mode = None
        self.conflicts  = 0
        self.crashs = 0
        
        self.obs_int_list = []
        self.obs_int_sep = []

        self.lat = origin[0]
        self.lon = origin[1]
        self.ini_speed = speed
        self.speed = self.ini_speed*0.51444
        self.hdg = None
        self.ax = 0
        self.alt = 800
        self.origin = origin
        self.destination = destination
        self.last_distflown = 0
        self.distflown = 0
        self.safely_flown = 1

        self.last_state = None
        self.state = None
        self.action_idx = None

        self.obs_int_list, self.obs_int_sep = [], []

    @property
    def ID(self):
        return traf.id2idx(self.name)
    
    @property
    def update_info(self):
        self.lat = traf.lat[self.ID]
        self.lon = traf.lon[self.ID]
        self.speed = traf.cas[self.ID]
        self.hdg = traf.hdg[self.ID]
        self.ax = traf.ax[self.ID]
        self.last_distflown = self.distflown
        self.distflown = traf.distflown[self.ID]

    @property
    def generate(self):
        self.hdg = qdrdist(self.origin[0], self.origin[1], self.destination[0], self.destination[1])[0]
        stack.stack(f'CRE {self.name} Mavic {self.lat} {self.lon} {self.hdg} {self.alt} {self.ini_speed}')
        stack.stack(f'ADDWPT {self.name} 52.07421700, -000.61079200')
        stack.stack(f'ADDWPT {self.name} {self.destination[0]} {self.destination[1]}')

    @property
    def delete_agent(self):
        stack.stack(f'DEL {self.name}')

    @property
    def update_observation_state(self):
        self.state = [[self.agent_to_destination/(2*1852*5), 
                       self.speed/45, 
                       self.ax/10,
                       self.hdg/360]]
        for intruder_idx, intruder in enumerate(self.obs_int_list):
            self.state.append([self.obs_int_sep[intruder_idx]/2,
                               (self.speed - intruder.speed)/45,
                               (self.ax - intruder.ax)/10,
                               qdrdist(self.lat, self.lon, intruder.lat, intruder.lon)[0]/360])
        if len(self.state) == 1:
           self.state.append([0]*4)

    @property
    def agent_to_destination(self):
        return latlondist(self.lat, self.lon, self.destination[0], self.destination[1])

    @property
    def perform_action(self):
        if self.speed/0.514444 + [-7, -5, -3, -1, 0, 1, 3, 5, 7][self.action_idx] >= 35:
            stack.stack(f'SPD {self.name} 35')
        elif self.speed/0.514444 + [-7, -5, -3, -1, 0, 1, 3, 5, 7][self.action_idx] <= 10:
            stack.stack(f'SPD {self.name} 10')
        else:
            stack.stack(f'SPD {self.name} {self.speed / 0.514444 + [-7, -5, -3, -1, 0, 1, 3, 5, 7][self.action_idx]}')

    @property
    def target_reached(self):
        return self.agent_to_destination <= 1852*0.05 + self.speed*5

    @property
    def save_trajectory(self):
        self.obs_int_list, self.obs_int_sep = [], []

    @property
    def tactical_mode_update(self):
        if len(self.obs_int_sep)>0:
            if not self.tactical_mode:
                self.tactical_mode = True
            if min(self.obs_int_sep) <= 0.30 and not self.color=='Red':
                self.color = 'Red'
                stack.stack(f'COLOR, {self.name}, Red')
            elif 0.30 < min(self.obs_int_sep) <= 0.9 and not self.color=='Orange':
                self.color = 'Orange'
                stack.stack(f'COLOR, {self.name}, Orange')
            elif min(self.obs_int_sep) > 0.9 and not self.color=='Yellow':
                self.color = 'Yellow'
                stack.stack(f'COLOR, {self.name}, Yellow')
        elif len(self.obs_int_sep)==0 and self.tactical_mode:
            self.tactical_mode, self.color = False, 'lime'
            stack.stack(f'COLOR, {self.name}, lime')

def separation2agents(agent1, agent2):
    return latlondist(agent1.lat, agent1.lon, agent2.lat, agent2.lon)/1852

def update_observation(agents):
    for agent_idx, agent in enumerate(agents):
        agent.safely_flown = 1
        for intruder_idx, intruder in enumerate(agents):
            if agent_idx!=intruder_idx:
                sep = separation2agents(agent, intruder)
                if 0.0 < sep <= 2:
                    if intruder not in agent.obs_int_list:
                        agent.obs_int_list.append(intruder)
                        agent.obs_int_sep.append(sep)
                    if 0.0 < sep <= 0.90:
                        agent.conflicts += 1
                        if 0.0 < sep <= 0.30:
                            agent.safely_flown = 0
                            agent.crashs += 1
                else:
                    if intruder in agent.obs_int_list:
                        index1 = agent.obs_int_list.index(intruder)
                        del agent.obs_int_list[index1]
                        del agent.obs_int_sep[index1]

def reset():
    print(f'The training is done')
    stack.stack("RESET")
            



