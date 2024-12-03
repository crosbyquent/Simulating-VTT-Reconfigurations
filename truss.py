from vpython import *
from joint import Joint

class Truss:
    def __init__(self, joints, index_connections, colors=None):
        if not isinstance(joints, list) or not all(isinstance(c, Joint) for c in joints):
            raise TypeError("Joints must be a list of Joint objects.")
        self.joints = joints
        self.index_connections = index_connections

        # Validate and assign colors
        if colors is None:
            self.colors = [color.gray(0.5)] * len(index_connections)  # Default to gray if no colors provided
        elif len(colors) != len(index_connections):
            raise ValueError("The number of colors must match the number of connections.")
        else:
            self.colors = colors

        self.connections = self.make_connections(index_connections)

    def make_connections(self, index_connections):
        connections = []
        for idx, index_pair in enumerate(index_connections):
            if not (isinstance(index_pair, tuple) or isinstance(index_pair, list)) or len(index_pair) != 2:
                raise TypeError("Each connection must be a pair of indices (list or tuple of length 2).")
            if not all(isinstance(idx, int) and 0 <= idx < len(self.joints) for idx in index_pair):
                raise ValueError("Index in connection pair must refer to a valid joint index.")
            start_joint = self.joints[index_pair[0]]
            end_joint = self.joints[index_pair[1]]
            connections.append(
                cylinder(
                    pos=start_joint.position,
                    axis=end_joint.position - start_joint.position,
                    radius=0.05,
                    color=self.colors[idx]
                )
            )
        return connections

    def update_connections(self):
        """Refreshes the positions and axes of all connections based on current joint positions."""
        for i, index_pair in enumerate(self.index_connections):
            start_joint = self.joints[index_pair[0]]
            end_joint = self.joints[index_pair[1]]
            self.connections[i].pos = start_joint.position
            self.connections[i].axis = end_joint.position - start_joint.position

    def extend_connection(self, connection_index, moving_joint_index, final_position):
        """Moves a specified connection's joint to a target (x, y, z) position."""
        index_pair = self.index_connections[connection_index]
        fixed_joint_index = index_pair[1 - moving_joint_index]  # Choose the other joint as fixed
        moving_joint = self.joints[index_pair[moving_joint_index]]
        fixed_joint = self.joints[fixed_joint_index]

        # Calculate the movement vector and number of steps
        target_position = vector(*final_position)
        total_distance = mag(target_position - moving_joint.position)
        step_size = total_distance / 50.0  # Arbitrary animation steps
        direction_vector = norm(target_position - moving_joint.position)

        while mag(moving_joint.position - target_position) > step_size:
            moving_joint.sphere.pos += step_size * direction_vector
            self.update_connections()
            rate(30)

        # Ensure final position is exact
        moving_joint.sphere.pos = target_position
        self.update_connections()

    def extend_two_connections(self, conn1_index, conn2_index, final_position):
        """Moves the shared joint of two connections to a target (x, y, z) position."""
        conn1 = self.index_connections[conn1_index]
        conn2 = self.index_connections[conn2_index]

        # Find the shared joint
        shared_joint_index = set(conn1).intersection(set(conn2))
        if len(shared_joint_index) != 1:
            raise ValueError("The two connections must share exactly one joint.")
        shared_joint_index = list(shared_joint_index)[0]

        # Target position
        target_position = vector(*final_position)
        shared_joint = self.joints[shared_joint_index]

        # Calculate movement
        total_distance = mag(target_position - shared_joint.position)
        step_size = total_distance / 50.0  # Arbitrary animation steps
        direction_vector = norm(target_position - shared_joint.position)

        while mag(shared_joint.position - target_position) > step_size:
            shared_joint.sphere.pos += step_size * direction_vector
            self.update_connections()
            rate(30)

        # Ensure final position is exact
        shared_joint.sphere.pos = target_position
        self.update_connections()
