import argparse
from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(description="Tutorial on running the cartpole RL environment.")
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


def define_markers() -> VisualizationMarkers:
    """Define markers with various different shapes."""
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
    pole_start_position = env.scene['robot'].data.body_state_w[:, 2, :3]
    pole_quat = env.scene['robot'].data.body_state_w[:, 2, 3:7]
    
    # Extract the pole length from the environment configuration
    pole_length = 1.0  # Assuming pole length is 0.5, replace with actual value if available
    
    # For a cartpole with pole in z direction, we're concerned with rotation around Y axis
    # The quaternion format is [w, x, y, z]
    pole_angle = 2.0 * torch.acos(pole_quat[:, 0])
    pole_direction = torch.sign(pole_quat[:, 2])  # Use y-component to determine direction
    
    pole_end_position = torch.zeros_like(pole_start_position)
    # Since pole is in z direction, sin component affects x and cos affects z
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

    cfg = sim_utils.DomeLightCfg(intensity=3000.0, color=(0.75, 0.75, 0.75))
    cfg.func("/World/Light", cfg)

    # create markers
    my_visualizer = define_markers()

    # simulate physics
    count = 0
    while simulation_app.is_running():
        with torch.inference_mode():
            # reset
            if count % 300 == 0:
                count = 0
                env.reset()
                # print("-" * 80)
                # print("[INFO]: Resetting environment...")
            # sample random actions
            joint_efforts = torch.randn_like(env.action_manager.action)
            # step the environment
            obs, rew, terminated, truncated, info = env.step(joint_efforts)
            # print current orientation of pole
            # print("[Env 0]: Pole joint: ", obs["policy"][0][1].item())
            # update counter
            count += 1

            # visualize
            my_visualizer.visualize(pole_end_position(env))

    # close the environment
    env.close()


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
