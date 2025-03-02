from isaaclab.app import AppLauncher
app_launcher = AppLauncher(headless=True)

import isaaclab.sim as sim_utils
simulation_app = app_launcher.app

# Import the correct module to access extensions
import omni.kit.app

# Get the list of enabled extensions
enabled_extension = omni.kit.app.get_app().get_extension_manager().get_extensions()

# Print the list of enabled extensions
print("Loaded Extensions:")
for ext in enabled_extension:
    if ext["enabled"]:
        print(f"{ext['name']} - {ext['path']}")

# import omni.physics.tensors.impl.api as physx
# print(physx)

sim = sim_utils.SimulationContext()
while simulation_app.is_running():
    sim.step()

simulation_app.close()
