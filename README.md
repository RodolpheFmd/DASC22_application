# Application of an Autonomous Multi-agent System Using Proximal Policy Optimisation for Tactical deconfliction Within the Urban Airspace. 
## Digital Avionics Systems Conference 2022.
This paper complements the conference paper presented for the DASC22 by providing trained multi-agent reinforcement learning models highlighted through the experimental part. 
This program is shared for personal, academic or performance comparison purposes.

## Requirements
### BlueSky open-source software and packages
[BlueSky](https://github.com/TUDelft-CNS-ATM/bluesky) ATM environment hosts this application and its installation is required with a special attention to the different required Python [lbraries](https://github.com/TUDelft-CNS-ATM/bluesky/wiki/Installation) in addition to:
- random.
- torch.

### File management
1. *Multi_agent* folder in the original *bluesky-master* folder.
2. Move *MARL_plugin* python file to bluesky-master *plugins* folder.
3. Move *run_MARL* script file to bluesky-master *scenario* folder.

### Settings
From *settings* python file in *Multi_agent* folder, make settings modification by specifying the operating system, the population of aircraft to generate for each episode, the directory of bluesky simulator, the maximum of iteration and the scenario.

## Scenarios
### Reminder
The conference paper presents three case studies:
- **Case study 1** : 2 fixed routes toward a merging point.
- **Case study 2** : 2 fixed routes intersecting at half way of their respective route.
- **Case study 2'** : 2 non-fixed routes intersecting at half way of their respective route with the generation of random agent dynamic model.

*However, this case study 2' presents here only Mavic drone model in contrast to the paper and the results from different models highlighted in the set-up section*

### Choice of the scenario
From *settings* python file in *Multi_agent* folder, change the variable 'scenario' from the integer 1, 2 or 3 respectively.

### Run the scenario !
After completing the bullets from **Requirements**, start BlueSky.py and write the command *IC run_MARL* in the bluesky simulator stack window.

## Performance
### Data collection
Tensorboard can be easily integrated to extract performance such as the conflict number, crashes, or globally the safeness of the models
Another method is to collect the information in a csv or xlsx file.

### Assessment
From the provided version, the performance are shown in the terminal for each episode that includes:
- Number of conflicts : considers the cumulative number of conflict for each decision step (every 5seconds). The conflicting separation is set to 0.9Nm.
- Number of crashes : considers the cumulative number of crashes for each decision step (every 5seconds). The crashes is over-estimated to 0.3Nm.
- Safeness : How long (distance Nm) the agents are safely flying, this information is cumulating throughout the simulation and returns to 0 in case of unsafe separation. An additional information of the safeness is provided by giving a quantitative value of the robustness of the system highlighting the system failure (crash case) per Nm of flight.

