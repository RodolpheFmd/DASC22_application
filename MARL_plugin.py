""" By Rodolphe Fremond - PhD Student, Cranfield University 2022
    Supervisor: Dr. Yan Xu, Dr. Gokhan Inalhan
    Tactical En-Route Solver : Model 1 trainer
    Multi-agent Reinforcement Learning :
    Advantage Actor Critic based on Proximal Policy Optimisation
"""

from Multi_agent.Airspace_scenario import generate_airspace, generate_route
from Multi_agent.env_info import Agent, reset, update_observation
import Multi_agent.settings as set
if set.device_spe:
    from Multi_agent.PPO_device import SuperAgent
else:
    from Multi_agent.PPO import SuperAgent
from datetime import datetime
import numpy as np
import random, os

AI = SuperAgent()
AI.memory.episode = 1
origin, destination = generate_airspace()

def init_plugin():
    global agents, step, start, traffic_flow, cnt_flow, agents_in_traf, origin, destination, ac_remaining, safeness, safeness_list
    traffic_flow, step, cnt_flow, ac_remaining, safeness, safeness_list = random.randint(15, 30), 0, 0, set.population-1, 0, []
    print(f'\nNew episode : {AI.memory.episode}')
    if set.scenario==1:
        agents = [Agent("UAS" + str(k + 1), random.randint(10, 35), origin[k%2], destination) for k in range(set.population)]
    if set.scenario==2:
        agents = [Agent("UAS" + str(k + 1), random.randint(10, 35), origin[k%2], destination[k%2]) for k in range(set.population)]
    if set.scenario==3:
        routes = [generate_route() for k in range(set.population)]
        agents = [Agent("UAS" + str(k + 1), random.randint(10, 35), routes[k][0], routes[k][1]) for k in range(set.population)]
    agents_in_traf = [agents[0]]
    start = datetime.now()
    agents_in_traf[-1].generate

    print(f'Simulation starts at {start}')
    config = {
        'plugin_name': 'MARL_plugin',
        'plugin_type': 'sim',
        'update_interval': 5,
        'update': update,
        'preupdate': preupdate}
    return config

def preupdate():
    pass

def update():
    global agents, start, step, traffic_flow, cnt_flow, agents_in_traf, ac_remaining, safeness, safeness_list

    step += 1
    cnt_flow += 1

    if cnt_flow == traffic_flow and ac_remaining!=0:
        cnt_flow, traffic_flow = 0, random.randint(15,30)
        agents_in_traf.append(agents[set.population-ac_remaining])
        agents_in_traf[-1].generate
        ac_remaining -= 1

    for agent in agents_in_traf:
        agent.update_info
    for agent in agents_in_traf:
        if agent.target_reached:
            AI.remember(agent)
            agent.delete_agent
            agents_in_traf.remove(agent)

    if (len(agents_in_traf)==0 and ac_remaining==0) or (step >= set.max_iteration):
        if step >= set.max_iteration:
            for agent in agents_in_traf:
                AI.remember(agent)
                agent.delete_agent
                agents_in_traf.remove(agent)
        if AI.memory.episode == set.max_episode:
            reset()
            if set.shut_down:
                os.system("shutdown /s /t 1")
            return

        print(f'Number of conflict : {AI.memory.conflicts}')
        print(f'Number of crash : {AI.memory.crashs}')
        print(f'Current safeness : {safeness} Nm without any collision')
        if len(safeness_list)>0:
            print(f'Model safeness : {1/(sum(safeness_list)/len(safeness_list))} collision/Nm')
        print(f'Operating time of the episode {AI.memory.episode} : {datetime.now()-start}')

        print(f'\nReinitialisation of the parameters')
        AI.memory.clear_memory
        init_plugin()
        return

    update_observation(agents_in_traf)

    for agent in agents_in_traf:
        agent.update_observation_state
        agent.tactical_mode_update
        AI.choose_action(agent)
        agent.perform_action
        agent.save_trajectory
        if np.prod(np.array([agent.safely_flown for agent in agents_in_traf])):
            safeness += sum([(agent.distflown-agent.last_distflown)/1852 for agent in agents_in_traf])
        else:
            safeness_list.append(safeness)
            safeness = 0
