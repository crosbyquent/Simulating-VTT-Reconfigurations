from vpython import vector
from vpython import cylinder 
from truss import Truss  

from vpython import rate

def merge_trusses(truss1, truss2, joint1_index, joint2_index, steps=50):
    # Get the positions of the joints to merge
    joint1_position = truss1.joints[joint1_index].position
    joint2_position = truss2.joints[joint2_index].position
    
    # Calculate the direction vector and the step size for each frame
    direction = joint1_position - joint2_position
    step_size = direction / steps
    
    # Animate the movement of joint2 to joint1
    for _ in range(steps):
        # Move joint2
        truss2.joints[joint2_index].position += step_size
        truss2.joints[joint2_index].vpython_obj.pos = truss2.joints[joint2_index].position
        
        # Update the display
        rate(30)  # Control the speed of the animation

    # After animation, update the trusses
    # Create the new list of joints by combining the two trusses
    new_joints = truss1.joints + truss2.joints

    # Create new connections (merging connections from both trusses)
    new_connections = truss1.connections
    offset = len(truss1.joints)  # Offset for the indices in truss2's connections
    for conn in truss2.connections:
        new_connections.append(
            (conn[0] + offset, conn[1] + offset)  # Re-index connections
        )

    # Return the new merged truss
    return Truss(new_joints, new_connections)
