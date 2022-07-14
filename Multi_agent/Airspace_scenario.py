from bluesky.tools.geo import qdrpos
import Multi_agent.settings as set
from bluesky import stack
import random

def generate_airspace():
    if set.scenario==1:
        stack.stack(f'CIRCLE SIM 52.07421700 -000.61079200 5')

        lat1, lon1 = qdrpos(52.07421700, -000.61079200, 0, 5)
        lat2, lon2 = qdrpos(52.07421700, -000.61079200, 135, 5)
        lat3, lon3 = qdrpos(52.07421700, -000.61079200, 225, 5)

        stack.stack(f'LINE CRA_1 {52.07421700} {-000.61079200} {lat1} {lon1}')
        stack.stack(f'LINE CRA_2 {52.07421700} {-000.61079200} {lat2} {lon2}')
        stack.stack(f'LINE CRA_3 {52.07421700} {-000.61079200} {lat3} {lon3}')

        return [[lat2, lon2], [lat3, lon3]], [lat1, lon1]
    elif set.scenario==2:
        stack.stack(f'CIRCLE SIM {52.07421700} {-000.61079200} {5}')

        lat1, lon1 = qdrpos(52.07421700, -000.61079200, 10, 5)
        lat2, lon2 = qdrpos(52.07421700, -000.61079200, 190, 5)
        lat3, lon3 = qdrpos(52.07421700, -000.61079200, 100, 5)
        lat4, lon4 = qdrpos(52.07421700, -000.61079200, 280, 5)

        stack.stack(f'LINE CRA_2 {lat1} {lon1} {lat2} {lon2}')
        stack.stack(f'LINE CRA_3 {lat3} {lon3} {lat4} {lon4}')

        return [[lat1, lon1], [lat3, lon3]], [[lat2, lon2], [lat4, lon4]]
    elif set.scenario==3:
        stack.stack(f'CIRCLE SIM {52.07421700} {-000.61079200} {5}')
        return None, None

def generate_route():
    angle = random.choice([0, 30, 60, 90, 120, 150])
    lat1, lon1 = qdrpos(52.07421700, -000.61079200, angle, 5)
    lat2, lon2 = qdrpos(52.07421700, -000.6107920, (angle + 180) % 360, 5)
    return [lat1, lon1], [lat2, lon2]
