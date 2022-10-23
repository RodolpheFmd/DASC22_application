# Application of an Autonomous Multi-agent System Using Proximal Policy Optimisation for Tactical deconfliction Within the Urban Airspace. 
## _Digital Avionics Systems Conference 2022_.
This attachment complements the conference paper presented for the DASC22 by providing trained multi-agent reinforcement learning models highlighted through the experimental part. 
This program is shared for personal, academic or performance comparison purposes.
Only the case studies I and II are showcased here. 

## Requirements
### BlueSky open-source software and packages
[BlueSky](https://github.com/TUDelft-CNS-ATM/bluesky) ATM environment hosts this application and its installation is required with a special attention to the different required Python [libraries](https://github.com/TUDelft-CNS-ATM/bluesky/wiki/Installation) in addition to:
- random.
- torch.

### File management
1. *Multi_agent* folder in the original *bluesky-master* folder.
2. Move *MARL_plugin* python file to bluesky-master *plugins* folder.
3. Move *run_MARL* script file to bluesky-master *scenario* folder.

### Settings
From *settings* python file in *Multi_agent* folder, make settings modification by specifying the operating system, the population of aircraft to generate for each episode, and the maximum of iteration and the scenario.

## Scenarios
### Reminder
The conference paper presents three case studies and two can be deployed here:
- **Case study 1** : 2 fixed routes toward a merging point.
- **Case study 2** : 2 fixed routes intersecting at half way of their respective route.

<img width="683" alt="scenario1resized" src="https://user-images.githubusercontent.com/92471439/197396184-e2ece68a-dd4c-40d3-9a6e-fd1cb808c21b.png">


### Choice of the scenario
From *settings* python file in *Multi_agent* folder, change the variable 'scenario' from the integer 1 or 2 for choosing the execution of case studies I and II respectively.

### Run the scenario !
After completing the bullets from **Requirements**, start BlueSky.py and write the command *IC run_MARL* in the bluesky simulator stack window.

## Policy Design
As a preliminary research stage, the policy is inspired from [Marc Brittain](https://github.com/marcbrittain) achievement about a hybrid Actor Critic model based on Proximal Policy Optimisation baseline.

![AC_architecture](https://user-images.githubusercontent.com/92471439/197394973-434b347c-f8e8-42b7-bf1c-2da0d74fb87f.png)

A reccurent neural network allows to process non-fixed vector input from encoded intruders' information. Once this information processed, it is concatenated with the ownship (i.e local) observation before passing through two fully connected neural networks: actor and critic. 
More information is provided in the conference paper.
Despite the similarity with the [mentioned author](https://github.com/marcbrittain), the presented research makes addtional contribution :
- Use UAS (Unmanned Aerial Systems) rotor wings aircraft models.
- Add uncertainty about the initial conditions : traffic flow entrance, speed, and even about the intersecting route angle.
- Proposes a new detection method that detects every single aircraft within an observation range.
- Tactical solver integrated into a unique synthetic co-simulation U-Space Services environment and demonstrated with [AMU-LED](https://amuledproject.eu/).

![LD_methodResized](https://user-images.githubusercontent.com/92471439/197396024-9aff13db-b510-4880-b28d-e88ffe589d27.png)

## Restrictions

This repertory does not contain the following contributions:
- Reinforcement Learning algorithm used for training. Only the trained model is shared which aims to perform only their specific scenarios I and II', their use in another scenario would make the model inefficient.
- UAS models used for the case study II'.
- The demonstration of the case study II'.

## Performance

### Data collection
Tensorboard can be easily integrated to extract performance such as the conflict number, crashes, or globally the safeness of the models
Another method is to collect the information in a csv or xlsx file.

### Assessment
From the provided version, the performance are shown in the terminal for each episode that includes:
- Number of conflicts : considers the cumulative number of conflict for each decision step (every 5seconds). The conflicting separation is set to 0.9Nm.
- Number of crashes : considers the cumulative number of crashes for each decision step (every 5seconds). The crashes is over-estimated to 0.3Nm considered as a Loss of Separation LOS.
- Safeness : How long (distance Nm) the agents are safely flying, this information is cumulating throughout the simulation and restarts to 0 in case of unsafe separation. An additional information of the safeness is provided by giving a quantitative value of the robustness of the system highlighting the system failure (crash case) per Nm of flight.

### Results
The following results highlight the model's performance throughout the training process.
