import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

# Parameters
diagonal = 4.0  
half_diag = diagonal / 2
center = np.array([0, 0, 0])
colors = ['red', 'blue', 'green', 'yellow']

# Initialize corners: two on x-axis and two on y-axis
original_corners = np.array([
    [half_diag, 0, 0],   # Corner on the positive x-axis
    [0, half_diag, 0],   # Corner on the positive y-axis
    [-half_diag, 0, 0],  # Corner on the negative x-axis
    [0, -half_diag, 0]   # Corner on the negative y-axis
])
corners = original_corners.copy()

# Global variables
is_paused = False  # For tracking Play/Pause state
current_position = half_diag  # Start position of the corner (x-coordinate)

# Plotting and animation setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)
ax.set_title("3D VTT Simulation")

# Functions for drawing lines and corners
def draw_lines(corner_index, corners, ax):
    """Draw lines between consecutive corners."""
    start_corner = corners[corner_index]
    end_corner = corners[(corner_index + 1) % len(corners)]
    
    ax.plot([start_corner[0], end_corner[0]], 
            [start_corner[1], end_corner[1]], 
            [start_corner[2], end_corner[2]], 
            color=colors[corner_index], lw=3)
    
    if corner_index < len(corners) - 1:
        draw_lines(corner_index + 1, corners, ax)

def draw_corners(corners, ax):
    """Draw black dots at each corner."""
    for corner in corners:
        ax.scatter(corner[0], corner[1], corner[2], color='black', s=50)

# Initialize plot
draw_lines(0, corners, ax)
draw_corners(corners, ax)

# Movement functions
def move_corner(corner_index, corners, step):
    """Move one corner and adjust adjacent corners to preserve the shape."""
    global current_position
    
    start_corner = corners[corner_index]
    left_neighbor = corners[(corner_index - 1) % len(corners)]
    right_neighbor = corners[(corner_index + 1) % len(corners)]
    
    # Move the selected corner outward along the x-axis
    current_position += step
    start_corner[0] = current_position
    
    # Adjust neighbors' y-coordinate to keep the square shape
    left_neighbor[1] -= step * (left_neighbor[0] / half_diag)
    right_neighbor[1] -= step * (right_neighbor[0] / half_diag)

def update(num):
    """Update function for animation. Move a corner gradually."""
    step = 0.05
    target_position = half_diag * 2
    
    if not is_paused and current_position < target_position:
        move_corner(0, corners, step)
    
    # Clear and redraw the updated plot
    ax.clear()  
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.set_title("3D VTT Simulation")
    
    draw_lines(0, corners, ax)
    draw_corners(corners, ax)

# Play/Pause button callback
def toggle_animation(event):
    global is_paused
    is_paused = not is_paused
    play_button.label.set_text("Pause" if not is_paused else "Play")

# Restart button callback
def restart_animation(event):
    global corners, current_position, is_paused
    corners = original_corners.copy()
    current_position = half_diag
    is_paused = False
    play_button.label.set_text("Pause")

# Create the animation
ani = FuncAnimation(fig, update, frames=100, interval=60, blit=False)

# Add Play/Pause and Restart buttons
ax_play = plt.axes([0.7, 0.05, 0.1, 0.075])
ax_restart = plt.axes([0.81, 0.05, 0.1, 0.075])
play_button = Button(ax_play, "Pause")
restart_button = Button(ax_restart, "Restart")

# Connect buttons to their callback functions
play_button.on_clicked(toggle_animation)
restart_button.on_clicked(restart_animation)

plt.show()
