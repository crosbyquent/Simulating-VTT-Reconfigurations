from joint import Joint
from truss import Truss
from vpython import color, scene
import time

# Initialize the scene
scene.autoscale = True  # Automatically adjust the view to fit objects
scene.background = color.white

# Define joint points
joints1 = [
    Joint(-5, 0, 0),
    Joint(-4, 1, 0),
    Joint(-3, 0, 0),
    Joint(-4, -1, 0)
]

joints2 = [
    Joint(-2, 0, 0),
    Joint(-1, 1, 0),
    Joint(-1, -1, 0)
]

joints3 = [
    Joint(-1, 3, 0),
    Joint(0, 4, 0),
    Joint(0, 2, 0)
]

joints4 = [
    Joint(-1, -3, 0),
    Joint(0, -2, 0),
    Joint(0, -4, 0)
]

# Define connections and colors
quad_connections = [(0, 1), (1, 2), (2, 3), (3, 0)]
triang_connections = [(0, 1), (1, 2), (2, 0)]
colorful = [color.blue, color.red, color.green]

# Create trusses
truss1 = Truss(joints1, quad_connections)
truss2 = Truss(joints2, triang_connections, colors=colorful)
truss3 = Truss(joints3, triang_connections, colors=colorful)
truss4 = Truss(joints4, triang_connections, colors=colorful[::-1])

time.sleep(3)

# Step 1: Connect truss 2 to truss 1
truss2.extend_two_connections(
    conn1_index=2,
    conn2_index=0,
    final_position=(-3, 0, 0) 
)

# Step 2: Connect truss 3 to main truss
truss3.extend_two_connections(
    conn1_index=0,
    conn2_index=2,
    final_position=(-4, 1, 0)  
)

truss3.extend_two_connections(
    conn1_index=1,
    conn2_index=2,
    final_position=(-1, 1, 0)  
)

# Step 3: Connect truss 4 to main truss
truss4.extend_two_connections(
    conn1_index=0,
    conn2_index=2,
    final_position=(-4, -1, 0)  
)

truss4.extend_two_connections(
    conn1_index=0,
    conn2_index=1,
    final_position=(-1, -1, 0)  
)
