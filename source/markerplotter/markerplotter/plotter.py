# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""
A module for plotting marker positions in real-time in IsaacLab environments.
"""

import omni.ui
import omni.kit.app
import torch
import weakref
import carb
import numpy as np
from typing import Callable, Optional, List, Union
from isaaclab.ui.widgets.line_plot import LiveLinePlot
from isaacsim.core.api.simulation_context import SimulationContext


class MarkerPositionPlotter:
    """
    A plotter for visualizing marker positions in real-time.
    
    This class provides a UI window with real-time plots of the X, Y, and Z coordinates
    of marker positions calculated from an IsaacLab environment.
    """
    
    def __init__(
        self, 
        env: object, 
        position_fn: Callable,
        title: str = "Marker Position",
        window_width: int = 600,
        window_height: int = 400,
        plot_height: int = 150,
        max_datapoints: int = 200,
        y_min: float = -2.0,
        y_max: float = 2.0,
        labels: List[str] = None,
        colors: List[int] = None,
        auto_enable: bool = True
    ):
        """
        Initialize the marker position plotter.
        
        Args:
            env: The IsaacLab environment to get data from
            position_fn: A function that takes the environment and returns a tensor of positions
            title: The title of the plotting window
            window_width: The width of the plotting window in pixels
            window_height: The height of the plotting window in pixels
            plot_height: The height of each plot in pixels
            max_datapoints: The maximum number of data points to display in the plot
            y_min: The minimum value for the y-axis
            y_max: The maximum value for the y-axis
            labels: Custom labels for the plots (default: ["X Position", "Y Position", "Z Position"])
            colors: Custom colors for the plots
            auto_enable: Whether to automatically enable visualization on creation
        """
        self.env = env
        self.position_fn = position_fn
        self.title = title
        self.position_data = [[], [], []]  # X, Y, Z components
        self._debug_vis = False
        self._vis_frame = None
        self._vis_window = None
        self._term_visualizers = []
        self._debug_vis_handle = None
        self.plot_height = plot_height
        self.max_datapoints = max_datapoints
        self.y_min = y_min
        self.y_max = y_max
        self.labels = labels or ["X Position", "Y Position", "Z Position"]
        self.colors = colors
        self.window_width = window_width
        self.window_height = window_height
        
        # Create window for visualization
        self._create_ui()
        
        # Auto-enable if requested
        if auto_enable:
            self.set_debug_vis(True)
        
    def _create_ui(self):
        """Create the UI window and frame."""
        self._vis_window = omni.ui.Window(
            self.title, 
            width=self.window_width, 
            height=self.window_height
        )
        with self._vis_window:
            with omni.ui.VStack():
                self._vis_frame = omni.ui.Frame()
    
    def set_debug_vis(self, debug_vis: bool):
        """
        Enable or disable the visualization.
        
        Args:
            debug_vis: Whether to enable visualization
        """
        self._debug_vis = debug_vis
        
        if self._vis_frame:
            self._vis_frame.clear()
            self._term_visualizers = []
            
            if debug_vis:
                # Create subscription to update event
                if not self._debug_vis_handle:
                    app_interface = omni.kit.app.get_app_interface()
                    self._debug_vis_handle = app_interface.get_post_update_event_stream().create_subscription_to_pop(
                        lambda event, obj=weakref.proxy(self): obj._debug_vis_callback(event)
                    )
            else:
                # Remove subscription
                if self._debug_vis_handle:
                    self._debug_vis_handle.unsubscribe()
                    self._debug_vis_handle = None
                self._vis_frame.visible = False
                return
                
            self._vis_frame.visible = True
            
            # Create the visualization in the frame
            with self._vis_frame:
                with omni.ui.VStack():
                    # Create plots for X, Y, Z positions
                    for i, label in enumerate(self.labels):
                        plot = LiveLinePlot(
                            y_data=[[0]],  # Initial data
                            y_min=self.y_min,
                            y_max=self.y_max,
                            plot_height=self.plot_height,
                            show_legend=True,
                            legends=[label],
                            max_datapoints=self.max_datapoints,
                        )
                        self._term_visualizers.append(plot)
    
    def _debug_vis_callback(self, event):
        """
        Callback for the update event to refresh the plots.
        
        Args:
            event: The update event
        """
        # Skip if simulation is not running
        if not SimulationContext.instance().is_playing():
            return
            
        # Get the current position using the position function
        position = self.position_fn(self.env)
        
        # Skip if position data is invalid
        if not isinstance(position, torch.Tensor) or position.numel() == 0:
            return
            
        # Add data to the plots (using first environment's data)
        for i, plot in enumerate(self._term_visualizers):
            if i < len(self.labels) and i < position.shape[1]:
                plot.add_datapoint([position[0, i].item()])
    
    def update_config(
        self,
        y_min: Optional[float] = None,
        y_max: Optional[float] = None,
        max_datapoints: Optional[int] = None,
        plot_height: Optional[int] = None
    ):
        """
        Update the configuration of the plots.
        
        Args:
            y_min: New minimum value for the y-axis
            y_max: New maximum value for the y-axis
            max_datapoints: New maximum number of data points to display
            plot_height: New height for the plots
        """
        # Update configuration if specified
        if y_min is not None:
            self.y_min = y_min
        if y_max is not None:
            self.y_max = y_max
        if max_datapoints is not None:
            self.max_datapoints = max_datapoints
        if plot_height is not None:
            self.plot_height = plot_height
            
        # Rebuild visualization with new configuration
        if self._debug_vis:
            self.set_debug_vis(False)
            self.set_debug_vis(True)
    
    def clear_data(self):
        """
        Clear all data from the plots.
        """
        for plot in self._term_visualizers:
            if hasattr(plot, 'clear'):
                plot.clear()
    
    def close(self):
        """
        Clean up resources.
        
        This method should be called when the plotter is no longer needed,
        typically when the simulation is ending.
        """
        if self._debug_vis_handle:
            self._debug_vis_handle.unsubscribe()
            self._debug_vis_handle = None