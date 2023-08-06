import importlib.util
from itertools import product
from pathlib import Path

import numpy as np
import pygame

PLAYER_IMGS_PATH = [
    "resources/agent/agent-right.png",
    "resources/agent/agent-left.png",
    "resources/agent/agent-up.png",
    "resources/agent/agent-down.png",
]
BACKGROUND_IMG_PATH = "resources/terrain/grass.png"
TREE_IMG_PATH = "resources/objects/tree.png"
WOOD_IMG_PATH = "resources/objects/wood.png"
STONE_IMG_PATH = "resources/objects/stone.png"
GRASS_IMG_PATH = "resources/objects/grass.png"
CRAFTING_TABLE_IMG_PATH = "resources/objects/crafting-table.png"
STICKS_IMG_PATH = "resources/objects/sticks.png"
ROPE_IMG_PATH = "resources/objects/rope.png"
BRIDGE_IMG_PATH = "resources/objects/bridge.png"
WEAPON_BASIC_IMG_PATH = "resources/objects/weapon-basic.png"
ISLAND_IMG_PATH = "resources/terrain/island.png"
WATER_IMG_PATH = "resources/terrain/water.png"
GEM_IMG_PATH = "resources/objects/gem.png"
WEAPON_ADV_IMG_PATH = "resources/objects/weapon-advanced.png"


def get_file_path(file_name):
    spec = importlib.util.find_spec("craft2d")
    if spec is None:
        raise ImportError("Package 'craft2d' not found.")

    package_path = Path(spec.origin)
    file_path = package_path.parent / file_name
    return str(file_path)


class Renderer:
    def __init__(
        self,
        n_rows: int,
        n_cols: int,
        env_objects: list[str],
        inv_objects: list[str],
        window_width: int = 600,
        window_height: int = 600,
    ):
        # Initialise attributes
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.env_objects = env_objects
        self.inv_objects = inv_objects
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = (
            self.window_width / (self.n_cols + 2),  # +2 for inventory
            self.window_height / self.n_rows,
        )

        # Load assets
        self.background_image = self._load_image(get_file_path(BACKGROUND_IMG_PATH))
        self.player_images = self._load_images(PLAYER_IMGS_PATH)
        self.tree_image = self._load_image(get_file_path(TREE_IMG_PATH))
        self.wood_image = self._load_image(get_file_path(WOOD_IMG_PATH))
        self.stone_image = self._load_image(get_file_path(STONE_IMG_PATH))
        self.grass_image = self._load_image(get_file_path(GRASS_IMG_PATH))
        self.crafting_table_image = self._load_image(
            get_file_path(CRAFTING_TABLE_IMG_PATH)
        )
        self.sticks_image = self._load_image(get_file_path(STICKS_IMG_PATH))
        self.rope_image = self._load_image(get_file_path(ROPE_IMG_PATH))
        self.bridge_image = self._load_image(get_file_path(BRIDGE_IMG_PATH))
        self.weapon_basic_image = self._load_image(get_file_path(WEAPON_BASIC_IMG_PATH))
        self.island_image = self._load_image(get_file_path(ISLAND_IMG_PATH))
        self.water_image = self._load_image(get_file_path(WATER_IMG_PATH))
        self.gem_image = self._load_image(get_file_path(GEM_IMG_PATH))
        self.weapon_advanced_image = self._load_image(
            get_file_path(WEAPON_ADV_IMG_PATH)
        )

        # Initialise pygame
        pygame.init()
        self.clock = pygame.time.Clock()

    def _render_background(self, grid):
        for r, c in product(range(self.n_rows), range(self.n_cols)):
            if np.max(grid[r, c]) == 0:
                self._render_cell(self.background_image, r, c)
            else:
                object_type = np.argmax(grid[r, c])
                object_name = self.env_objects[object_type]

                if object_name == "gem":
                    self._render_cell(self.island_image, r, c)
                elif object_name == "water":
                    self._render_cell(self.water_image, r, c)
                elif object_name == "bridge":
                    self._render_cell(self.water_image, r, c)
                    self._render_cell(self.bridge_image, r, c)
                else:
                    self._render_cell(self.background_image, r, c)

    def _render_env_objects(self, grid):
        for r, c in product(range(self.n_rows), range(self.n_cols)):
            if np.max(grid[r, c]) == 0:
                # Environmet cell is empty
                continue

            object_type = np.argmax(grid[r, c])
            object_name = self.env_objects[object_type]

            if object_name == "tree":
                self._render_cell(self.tree_image, r, c)
            elif object_name == "stone":
                self._render_cell(self.stone_image, r, c)
            elif object_name == "grass":
                self._render_cell(self.grass_image, r, c)
            elif object_name == "crafting-table":
                self._render_cell(self.crafting_table_image, r, c)
            elif object_name == "gem":
                self._render_cell(self.gem_image, r, c)

    def _render_player(self, agent_position, direction):
        self._render_cell(
            image=self.player_images[np.argmax(direction)],
            row=agent_position[0],
            col=agent_position[1],
        )

    def _render_inventory(self, inventory):
        for idx, count in enumerate(inventory):
            object_name = self.inv_objects[idx]

            if object_name == "wood":
                self._render_cell(image=self.wood_image, row=idx, col=self.n_cols)
                self._render_text(text="Wood", row=idx, col=self.n_cols, loc="top")
            elif object_name == "stone":
                self._render_cell(image=self.stone_image, row=idx, col=self.n_cols)
                self._render_text(text="Stone", row=idx, col=self.n_cols, loc="top")
            elif object_name == "grass":
                self._render_cell(image=self.grass_image, row=idx, col=self.n_cols)
                self._render_text(text="Grass", row=idx, col=self.n_cols, loc="top")
            elif object_name == "sticks":
                self._render_cell(image=self.sticks_image, row=idx, col=self.n_cols)
                self._render_text(text="Sticks", row=idx, col=self.n_cols, loc="top")
            elif object_name == "rope":
                self._render_cell(image=self.rope_image, row=idx, col=self.n_cols)
                self._render_text(text="Rope", row=idx, col=self.n_cols, loc="top")
            elif object_name == "bridge":
                self._render_cell(image=self.bridge_image, row=idx, col=self.n_cols)
                self._render_text(text="Bridge", row=idx, col=self.n_cols, loc="top")
            elif object_name == "weapon-basic":
                self._render_cell(
                    image=self.weapon_basic_image, row=idx, col=self.n_cols
                )
                self._render_text(text="Weapon", row=idx, col=self.n_cols, loc="top")
            elif object_name == "gem":
                self._render_cell(image=self.gem_image, row=idx, col=self.n_cols)
                self._render_text(text="Gem", row=idx, col=self.n_cols, loc="top")
            elif object_name == "weapon-advanced":
                self._render_cell(
                    image=self.weapon_advanced_image, row=idx, col=self.n_cols
                )
                self._render_text(
                    text="Weapon (Adv)", row=idx, col=self.n_cols, loc="top"
                )

            self._render_text(
                text="X " + str(int(count)), row=idx, col=self.n_cols + 1, size=20
            )

    def _render_text(self, text, row, col, size=20, loc="center"):
        font = pygame.font.Font(None, size)
        text = font.render(text, True, (255, 255, 255))

        if loc == "center":
            pos = (
                col * self.cell_size[0] + self.cell_size[0] / 2 - text.get_width() / 2,
                row * self.cell_size[1] + self.cell_size[1] / 2 - text.get_height() / 2,
            )
        elif loc == "top":
            pos = (
                col * self.cell_size[0] + self.cell_size[0] / 2 - text.get_width() / 2,
                row * self.cell_size[1],
            )

        self.window.blit(text, pos)

    def _render_cell(self, image, row, col):
        self.window.blit(
            image,
            (
                col * self.cell_size[0],
                row * self.cell_size[1],
            ),
        )

    def _load_image(self, path, size=None):
        return pygame.transform.scale(
            pygame.image.load(path),
            self.cell_size,
        )

    def _load_images(self, paths):
        images = []
        for path in paths:
            images.append(self._load_image(get_file_path(path)))
        return images


class HumanRenderer(Renderer):
    def __init__(
        self,
        n_rows: int,
        n_cols: int,
        env_objects: list[str],
        inv_objects: list[str],
        window_width: int = 600,
        window_height: int = 600,
        window_title: str = "Craft2D",
        fps: int = 60,
    ) -> None:
        super().__init__(
            n_rows=n_rows,
            n_cols=n_cols,
            env_objects=env_objects,
            inv_objects=inv_objects,
            window_width=window_width,
            window_height=window_height,
        )
        self.fps = fps

        pygame.display.set_caption(window_title)
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

    def render(self, grid, inventory, agent_position, direction):
        self.window.fill((0, 0, 0))
        self._render_background(grid)
        self._render_env_objects(grid)
        self._render_player(agent_position, direction)
        self._render_inventory(inventory)
        self._handle_events()

    def _handle_events(self):
        self.clock.tick(self.fps)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


class RgbRenderer(Renderer):
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self.window = pygame.Surface((self.window_width, self.window_height))
