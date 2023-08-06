from itertools import product

import gymnasium as gym
import numpy as np

from craft2d.render.render import HumanRenderer

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3
USE = 4

MAX_RESOURCE_COUNT = 3
RESOURCE_COUNTS = {
    "tree": 4,
    "stone": 2,
    "grass": 2,
    "gem": 1,
}
ENVIRONMENT_OBJECTS = (
    "tree",
    "stone",
    "grass",
    "crafting-table",
    "water",
    "gem",
    "bridge",
)
INVENTORY_OBJECTS = (
    "wood",
    "stone",
    "grass",
    "sticks",
    "rope",
    "bridge",
    "weapon-basic",
    "gem",
    "weapon-advanced",
)
TASKS = {
    "get-wood": 0,
    "get-stone": 1,
    "get-grass": 2,
    "make-sticks": 3,
    "make-rope": 4,
    "make-bridge": 5,
    "make-basic-weapon": 6,
    "get-gem": 7,
    "make-advanced-weapon": 8,
}


class Craft2dEnv(gym.Env):
    def __init__(
        self,
        n_rows: int,
        n_cols: int,
        render_mode: str = "human",
    ):
        super().__init__()
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.render_mode = render_mode
        self.n_env_objects = len(ENVIRONMENT_OBJECTS)
        self.n_inv_objects = len(INVENTORY_OBJECTS)

        self.action_space = gym.spaces.Discrete(5)

        # Oservation space is a tuple of: (environment, inventory, direction)
        self.observation_space = gym.spaces.Tuple(
            spaces=(
                gym.spaces.Box(
                    low=0,
                    high=max(self.n_rows, self.n_cols),
                    shape=(2,),
                ),
                gym.spaces.Box(
                    low=0,
                    high=MAX_RESOURCE_COUNT,
                    shape=(self.n_inv_objects,),
                ),
                gym.spaces.Box(
                    low=0,
                    high=1,
                    shape=(4,),
                ),
            )
        )
        self.reward_range = (0, 1)

        self.init_required = True

        if self.render_mode == "human":
            self.renderer = HumanRenderer(
                n_rows=self.n_rows,
                n_cols=self.n_cols,
                env_objects=ENVIRONMENT_OBJECTS,
                inv_objects=INVENTORY_OBJECTS,
                fps=24,
            )

    def reset(
        self,
        task: str = "get-wood",
        seed: int = None,
        options: dict[str, str] = None,
    ):
        super().reset(seed=seed)
        # Set task
        self.task = task
        # Reset number of steps taken in environment
        self.n_steps = 0

        # Object order specified in ENVIRONMENT_OBJECTS
        self.grid = np.zeros((self.n_rows, self.n_cols, self.n_env_objects))
        # Object order specified in INVENTORY_OBJECTS
        self.inventory = np.zeros((self.n_inv_objects,))

        # Initialize agent position and direction
        self.agent_position = (0, 0)
        self.direction = np.zeros((4,))

        if self.init_required:
            self.init_required = False

            # Add resources to environment
            self._initialize_environment()
            self.cached_grid = self.grid.copy()
        else:
            self.grid = self.cached_grid.copy()

        # Setup island
        self._initialize_island()
        return self._create_observation()

    def step(self, action: int):
        if action == USE:
            self._handle_use_action()
        else:
            self._update_agent_position(action)
            self._update_agent_direction(action)

        obs = self._create_observation()
        reward = 1 if self.inventory[TASKS[self.task]] == 1 else 0
        done = reward == 1

        return obs, reward, done

    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        if self.render_mode == "human":
            self.renderer.render(
                grid=self.grid,
                inventory=self.inventory,
                agent_position=self.agent_position,
                direction=self.direction,
            )

    def _create_observation(self):
        # Fill observation with out of bounds
        obs_grid = np.full((5, 5), fill_value=-1)

        for d_r, d_c in product(range(-2, 3), range(-2, 3)):
            n_r = self.agent_position[0] + d_r
            n_c = self.agent_position[1] + d_c

            # Test if out of bounds
            if (n_r >= self.n_rows or n_r < 0) or (n_c >= self.n_cols or n_c < 0):
                continue

            obs_grid[d_r + 2, d_c + 2] = np.argmax(self.grid[n_r, n_c])

        # return (
        #     .copy(),
        #     self.inventory.copy(),
        #     self.direction.copy(),
        # )

        return (
            np.array([self.agent_position[0], self.agent_position[1]]).copy(),
            self.inventory.copy(),
            self.direction.copy(),
        )

    def _sample_position(self):
        row = np.random.randint(1, self.n_rows - 1)
        col = np.random.randint(1, self.n_cols - 1)
        return row, col

    def _initialize_environment(self):
        used_positions = []

        for i, object_name in enumerate(ENVIRONMENT_OBJECTS):
            # Skip water and bridge
            if object_name in ("water", "bridge"):
                continue

            # Determine how many of each object to place
            if object_name in RESOURCE_COUNTS:
                count = RESOURCE_COUNTS[object_name]
            else:
                count = 1

            # Place required number of specified object
            for _ in range(count):
                row, col = self._sample_position()
                while (row, col) in used_positions:
                    row, col = self._sample_position()

                # Add padding around object
                for d_r, d_c in product(range(-1, 2), range(-1, 2)):
                    used_positions.append((row + d_r, col + d_c))
                self.grid[row, col, i] = 1

    def _initialize_island(self):
        # Get island position
        for r, c in product(range(self.n_rows), range(self.n_cols)):
            if self.grid[r, c, ENVIRONMENT_OBJECTS.index("gem")] == 1:
                island_row = r
                island_col = c
                break

        # Surround island with water
        for d_r, d_c in product(range(-1, 2), range(-1, 2)):
            n_r = island_row + d_r
            n_c = island_col + d_c

            if (
                (n_r == r and n_c == c)
                or (n_r >= self.n_rows or n_r < 0)
                or (n_c >= self.n_cols or n_c < 0)
            ):
                continue

            self.grid[n_r, n_c, ENVIRONMENT_OBJECTS.index("water")] = 1

    def _update_agent_position(self, action: int):
        self.last_position = self.agent_position
        row, col = self.agent_position

        if action == RIGHT:
            n_row = row
            n_col = col + 1 if col + 1 < self.n_cols else col
        elif action == LEFT:
            n_row = row
            n_col = col - 1 if col - 1 >= 0 else col
        elif action == UP:
            n_row = row - 1 if row - 1 >= 0 else row
            n_col = col
        elif action == DOWN:
            n_row = row + 1 if row + 1 < self.n_rows else row
            n_col = col

        # Update position if no collision or water
        if np.max(self.grid[n_row, n_col]) == 0:
            self.agent_position = (n_row, n_col)

        # Allow agent to cross water if bridge has been placed
        object_type = np.argmax(self.grid[n_row, n_col])
        object_name = ENVIRONMENT_OBJECTS[object_type]

        if object_name == "bridge":
            self.agent_position = (n_row, n_col)

    def _update_agent_direction(self, action: int):
        last_direction = self.direction
        self.direction = np.zeros((4,))

        if action == RIGHT:
            self.direction[0] = 1
        elif action == LEFT:
            self.direction[1] = 1
        elif action == UP:
            self.direction[2] = 1
        elif action == DOWN:
            self.direction[3] = 1
        elif action == USE:
            self.direction = last_direction

    def _handle_use_action(self):
        # Cell in front of agent
        itr_row, itr_col = self._get_interaction_cell()

        # Test if cell is empty
        if np.max(self.grid[itr_row, itr_col]) == 0:
            return

        # Get object type
        object_type = np.argmax(self.grid[itr_row, itr_col])
        object_name = ENVIRONMENT_OBJECTS[object_type]

        # Collect resources from environment
        if object_name == "tree":
            self._collect_tree(itr_row, itr_col)
        elif object_name == "stone":
            self._collect_stone(itr_row, itr_col)
        elif object_name == "grass":
            self._collect_grass(itr_row, itr_col)
        elif object_name == "gem":
            self._collect_gem(itr_row, itr_col)
        elif object_name == "water":
            self._handle_water_interaction(itr_row, itr_col)
        elif object_name == "crafting-table":
            self._handle_crafting_interaction()

    def _handle_crafting_interaction(self):
        if self.inventory[6] > 0 and self.inventory[7] > 0:
            # Advanced weapon
            self.inventory[8] += 1
            self.inventory[6] -= 1
            self.inventory[7] -= 1
        if self.inventory[3] > 0 and self.inventory[1] >= 2:
            # Weapon
            self.inventory[6] += 1
            self.inventory[3] -= 1
            self.inventory[1] -= 2
        elif self.inventory[3] > 0 and self.inventory[4] >= 1:
            # Bridge
            self.inventory[5] += 1
            self.inventory[3] -= 1
            self.inventory[4] -= 1
        elif self.inventory[0] > 1:
            # Sticks
            self.inventory[0] -= 2
            self.inventory[3] += 1
        elif self.inventory[2] > 1:
            # Rope
            self.inventory[2] -= 2
            self.inventory[4] += 1

    def _handle_water_interaction(self, itr_row, itr_col):
        # Place bridge on water if agent has bridge in inventory
        water_idx_env = ENVIRONMENT_OBJECTS.index("water")
        bridge_idx_env = ENVIRONMENT_OBJECTS.index("bridge")
        bridge_idx_inv = INVENTORY_OBJECTS.index("bridge")

        if self.inventory[bridge_idx_inv] > 0:
            self.grid[itr_row, itr_col, bridge_idx_env] = 1
            self.grid[itr_row, itr_col, water_idx_env] = 0
            self.inventory[bridge_idx_inv] -= 1

    def _collect_tree(self, itr_row, itr_col):
        tree_idx_env = ENVIRONMENT_OBJECTS.index("tree")
        wood_idx_inv = INVENTORY_OBJECTS.index("wood")
        self.inventory[wood_idx_inv] += 1
        self.grid[itr_row, itr_col, tree_idx_env] = 0

    def _collect_stone(self, itr_row, itr_col):
        stone_idx_env = ENVIRONMENT_OBJECTS.index("stone")
        stone_idx_inv = INVENTORY_OBJECTS.index("stone")
        self.inventory[stone_idx_inv] += 1
        self.grid[itr_row, itr_col, stone_idx_env] = 0

    def _collect_grass(self, itr_row, itr_col):
        grass_idx_env = ENVIRONMENT_OBJECTS.index("grass")
        grass_idx_inv = INVENTORY_OBJECTS.index("grass")
        self.inventory[grass_idx_inv] += 1
        self.grid[itr_row, itr_col, grass_idx_env] = 0

    def _collect_gem(self, itr_row, itr_col):
        gem_idx_env = ENVIRONMENT_OBJECTS.index("gem")
        gem_idx_inv = INVENTORY_OBJECTS.index("gem")
        self.inventory[gem_idx_inv] += 1
        self.grid[itr_row, itr_col, gem_idx_env] = 0

    def _get_interaction_cell(self):
        interaction_row = self.agent_position[0]
        interaction_col = self.agent_position[1]

        if self.direction[0] == 1:
            interaction_col += 1 if interaction_col + 1 < self.n_cols else 0
        elif self.direction[1] == 1:
            interaction_col -= 1 if interaction_col - 1 >= 0 else 0
        elif self.direction[2] == 1:
            interaction_row -= 1 if interaction_row - 1 >= 0 else 0
        elif self.direction[3] == 1:
            interaction_row += 1 if interaction_row + 1 < self.n_rows else 0
        return interaction_row, interaction_col
