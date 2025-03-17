# Marker Position Plotter Extension for IsaacLab

A simple extension for IsaacLab that allows you to plot the position of markers in real-time. This is useful for debugging and visualizing the movement of objects in your simulation.

## Installation

To install this extension:

1. Clone the repository to your IsaacLab `source` directory (if you haven't already):
   ```bash
   cd /path/to/IsaacLab/source
   ```

2. Install the extension:
   ```bash
   # Navigate to the IsaacLab root directory
   cd /path/to/IsaacLab
   
   # Install the extension using the isaaclab.sh script
   ./isaaclab.sh --install
   ```

## Usage

Here's a simple example of how to use the extension:

```python
from markerplotter import MarkerPositionPlotter
import torch

# Define a function to get the position data
def get_position(env):
    # This function should return a tensor of shape [num_envs, 3]
    # containing the X, Y, Z coordinates you want to plot
    return env.some_position_data

# Create a plotter instance
plotter = MarkerPositionPlotter(
    env=env,
    position_fn=get_position,
    title="Object Position",
    y_min=-2.0,
    y_max=2.0
)

# The plotter will automatically update as the simulation runs

# In your cleanup code:
plotter.close()
```

For a complete example, see the `examples/cartpole_marker_plot.py` file.

## Features

- Real-time plotting of marker positions
- Separate plots for X, Y, and Z coordinates
- Configurable plot settings (y-axis limits, window size, etc.)
- Automatic plot updates synchronized with the simulation

## License

This extension is licensed under the BSD 3-Clause License. See the LICENSE file for details.