# Marker Position Plotter

A simple extension for IsaacLab that allows you to plot the position of markers in real-time. This is useful for debugging and visualizing the movement of objects in your simulation.

## Features

- Real-time plotting of marker positions
- Separate plots for X, Y, and Z coordinates
- Simple API for integration with any IsaacLab environment
- Configurable plot settings

## Usage

```python
from markerplotter import MarkerPositionPlotter

# Create a plotter instance
plotter = MarkerPositionPlotter(env, calculate_position_function)

# Use in your main loop
while simulation_app.is_running():
    # Step your environment
    env.step(actions)
    
    # The plotter automatically updates
    
# Clean up when done
plotter.close()
```

## Examples

See the examples directory for more detailed usage examples.