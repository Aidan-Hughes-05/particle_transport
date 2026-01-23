from materials import Material
import numpy as np


def step_magnitude(position, material):
    position[:] += exp_rand(material.mean_free_path, position.size)
    return None

def directional_step(position, material):
    position[:] += exp_rand(material.mean_free_path, position.size) * one_dimensional_direction(position.size)
    return None

def find_escaped(position, length) -> np.ndarray:
    return position >= length


def find_absorbed(alive, material) -> np.ndarray:
    temp = np.random.uniform(0, 1, alive.size)
    return temp > material.absorption_probability


def tally_killed(killed_particles, alive) -> int:
    if killed_particles.sum() == 0:
        return 0
    alive[killed_particles] = False
    return killed_particles.sum()


def transport_1d(particle_number, material, length) -> tuple[int, int, int]:

    absorbed_tally, escaped_tally, backscatter_tally = 0, 0, 0
    alive, position = np.ones(particle_number, dtype=bool), np.zeros(particle_number)

    step_magnitude(position, material)

    escape_positions = find_escaped(position, length)
    escaped_tally += tally_killed(escape_positions, alive)

    still_alive = alive.nonzero()
    absorbed_positions = find_absorbed(still_alive, material)
    absorbed_tally += tally_killed(absorbed_positions, alive)

    while alive.any():
        still_alive = alive.nonzero()

        directional_step(position, material)

    return absorbed_tally, escaped_tally, backscatter_tally
