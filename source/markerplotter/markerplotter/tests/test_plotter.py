# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Test cases for the marker position plotter."""

import unittest
import torch
from unittest.mock import Mock, patch

class TestMarkerPositionPlotter(unittest.TestCase):
    """Test cases for the MarkerPositionPlotter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # These imports are conditionally skipped if the test is run outside of Omniverse
        try:
            from markerplotter import MarkerPositionPlotter
            self.MarkerPositionPlotter = MarkerPositionPlotter
        except ImportError:
            self.skipTest("MarkerPositionPlotter cannot be imported outside of Omniverse")
    
    @patch('omni.ui.Window')
    @patch('omni.kit.app.get_app_interface')
    def test_initialization(self, mock_get_app, mock_window):
        """Test initialization of the plotter."""
        # Mock environment and position function
        mock_env = Mock()
        mock_position_fn = Mock(return_value=torch.tensor([[[1.0, 2.0, 3.0]]]))
        
        # Create plotter with auto_enable=False to avoid creating the subscription
        plotter = self.MarkerPositionPlotter(
            env=mock_env,
            position_fn=mock_position_fn,
            auto_enable=False
        )
        
        # Check that window was created
        mock_window.assert_called_once()
        
        # Check properties were set correctly
        self.assertEqual(plotter.env, mock_env)
        self.assertEqual(plotter.position_fn, mock_position_fn)
        self.assertEqual(plotter.labels, ["X Position", "Y Position", "Z Position"])
        
    def test_update_config(self):
        """Test updating the configuration."""
        # Skip if not in Omniverse
        if not hasattr(self, 'MarkerPositionPlotter'):
            self.skipTest("MarkerPositionPlotter cannot be imported outside of Omniverse")
            
        # Mock environment and position function
        mock_env = Mock()
        mock_position_fn = Mock(return_value=torch.tensor([[[1.0, 2.0, 3.0]]]))
        
        # Create plotter with auto_enable=False
        with patch('omni.ui.Window'), patch('omni.kit.app.get_app_interface'):
            plotter = self.MarkerPositionPlotter(
                env=mock_env,
                position_fn=mock_position_fn,
                auto_enable=False
            )
            
            # Test updating configuration
            plotter.update_config(y_min=-5.0, y_max=5.0, max_datapoints=100)
            
            # Check that properties were updated
            self.assertEqual(plotter.y_min, -5.0)
            self.assertEqual(plotter.y_max, 5.0)
            self.assertEqual(plotter.max_datapoints, 100)