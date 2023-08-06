import inductiva
from inductiva import fluids
inductiva.api_key = "735d2e8d919a5358ad2cd478d5abd9805482cc4b087dac4a7f20a34993f6e411"

scenario = inductiva.fluids.scenarios.FluidBlock(density=fluids.WATER.density, kinematic_viscosity=fluids.WATER.kinematic_viscosity, dimensions=[0.1, 1, 1])
# gpu_start_time = time()
gpu_output = scenario.simulate(simulator=fluids.SPlisHSPlasH(), device="gpu", simulation_time=2., particle_radius=0.006)
# gpu_end_time = time()
# print(f"A SPH simulation takes %1.2fs on GPU." % (gpu_end_time - gpu_start_time))