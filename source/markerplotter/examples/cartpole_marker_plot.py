# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""
Example script showing how to use the MarkerPositionPlotter with a cartpole environment.
This is based on the cartpole_marker.py script in the IsaacLab repository.
"""

import argparse
from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(description="Tutorial demonstrating the marker position plotter.")
parser.add_argument("--num_envs", type=int, default=16, help="Number of environments to spawn.")

# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import torch
import isaaclab.sim as sim_utils
from isaaclab.envs import ManagerBasedRLEnv
from isaaclab_tasks.manager_based.classic.cartpole.cartpole_env_cfg import CartpoleEnvCfg
from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg
from markerplotter import MarkerPositionPlotter


def define_markers() -> VisualizationMarkers:
    """Define markers with a sphere shape."""
    marker_cfg = VisualizationMarkersCfg(
        prim_path="/Visuals/myMarkers",
        markers={
            "sphere": sim_utils.SphereCfg(
                radius=0.1,
                visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 1.0, 0.0)),
            ),
        },
    )
    return VisualizationMarkers(marker_cfg)


def pole_end_position(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Get the position of the pole end.

    Args:
        env: The environment.

    Returns:
        The position of the pole end.
    """
    # Get the position and orientation of the pole
    pole_start_position = env.scene['robot'].data.body_state_w[:, 2, :3]
    pole_quat = env.scene['robot'].data.body_state_w[:, 2, 3:7]
    
    # Extract the pole length from the environment configuration
    pole_length = 1.0  # Assuming pole length is 1.0
    
    # For a cartpole with pole in z direction, we're concerned with rotation around Y axis
    # The quaternion format is [w, x, y, z]
    pole_angle = 2.0 * torch.acos(pole_quat[:, 0])
    pole_direction = torch.sign(pole_quat[:, 2])  # Use y-component to determine direction
    
    # Calculate the end position of the pole
    pole_end_position = torch.zeros_like(pole_start_position)
    pole_end_position[:, 0] = pole_start_position[:, 0]
    pole_end_position[:, 1] = pole_start_position[:, 1] + pole_length * torch.sin(pole_angle) * pole_direction
    pole_end_position[:, 2] = pole_start_position[:, 2] + pole_length * torch.cos(pole_angle)
    
    return pole_end_position


def main():
    """Main function."""
    # create environment configuration
    env_cfg = CartpoleEnvCfg()
    env_cfg.scene.num_envs = args_cli.num_envs
    # setup RL environment
    env = ManagerBasedRLEnv(cfg=env_cfg)

    # Add light to the scene
    cfg = sim_utils.DomeLightCfg(intensity=3000.0, color=(0.75, 0.75, 0.75))
    cfg.func("/World/Light", cfg)

    # create markers
    my_visualizer = define_markers()
    
    # Create the position plotter
    position_plotter = MarkerPositionPlotter(
        env=env,
        position_fn=pole_end_position,
        title="Cartpole Pole End Position",
        y_min=-2.0,
        y_max=2.0,
        labels=["X Position", "Y Position", "Z Position"]
    )

    # simulate physics
    count = 0
    try:
        while simulation_app.is_running():
            with torch.inference_mode():
                # reset
                if count % 300 == 0:
                    count = 0
                    env.reset()
                    position_plotter.clear_data()  # Clear the plot data on reset
                
                # sample random actions
                joint_efforts = torch.randn_like(env.action_manager.action)
                
                # step the environment
                obs, rew, terminated, truncated, info = env.step(joint_efforts)
                
                # update counter
                count += 1

                # visualize the marker
                pole_pos = pole_end_position(env)
                my_visualizer.visualize(pole_pos)
                
                # The plotter automatically updates through the event subscription
    finally:
        # Close the plotter when done
        position_plotter.close()
        # close the environment
        env.close()


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()