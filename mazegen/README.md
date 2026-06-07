> *This project has been created as part of the 42 curriculum by [ialrandr](mailto:ialrandr@student.42antananarivo.mg) and [trakotoz](mailto:trakotoz@student.42antananarivo.mg).*

# MazeGen: Generate and Solve Mazes

MazeGen is a small, modular Python package for generating and solving mazes. It ships several generation algorithms and solver implementations, all wired together through a clean, config-driven interface. The package is suitable for learning maze algorithms, prototyping game levels, or embedding maze logic into larger projects.

---

## Contents

| Component     | Location                              | Description                                   |
|---------------|---------------------------------------|-----------------------------------------------|
| Core package  | `mazegen/`                            | Entry point, maze model, config, registry     |
| Generators    | `mazegen/generator/algorithms/`       | `backtracking_dfs`, `prims`, `wilsons`        |
| Solvers       | `mazegen/solver/algorithms/`          | `a_star`, `dijkstra`, `backtracking_bfs`      |
| Base classes  | `generator_base.py`, `solver_base.py` | Abstract contracts for algorithms             |
| Registry      | `maze_register.py`                    | Auto-registration for generators and solvers  |

---

## Key Features

- **Multiple generation algorithms** — recursive backtracking DFS, Prim's randomized, and Wilson's uniform spanning tree.
- **Several solver implementations** — A\* (heuristic), Dijkstra (shortest path), and backtracking BFS.
- **Perfect and imperfect mazes** — set `perfect=False` to carve random loops into the maze for multiple solution paths.
- **Config-driven creation** — all parameters (size, entry, exit, seed, perfection) live in a single `MazeConfig` dataclass.
- **Step-by-step iteration** — both generators and solvers expose a `_step` variant that yields intermediate states, ideal for visualization or animation.
- **Auto-registration** — any generator or solver subclass that sets `algorithm_name` is automatically registered and immediately discoverable.
- **Reproducible mazes** — pass an integer `seed` to get the same maze every time.
- **Dependency-free core** — only the Python standard library is required.

---

## Project Structure

```
mazegen/
├── __init__.py
├── Makefile
├── pyproject.toml
├── README.md
└── mazegen/
    ├── __init__.py
    ├── maze.py              # Maze model (grid, entry, exit, path marking)
    ├── maze_config.py       # MazeConfig dataclass
    ├── maze_register.py     # GeneratorRegistry / SolverRegistry
    ├── mazegen.py           # MazeGen static interface
    ├── generator/
    │   ├── __init__.py
    │   ├── generator_base.py          # Abstract MazeGenerator
    │   └── algorithms/
    │       ├── __init__.py
    │       ├── backtracking_dfs.py
    │       ├── prims.py
    │       └── wilsons.py
    └── solver/
        ├── __init__.py
        ├── solver_base.py             # Abstract MazeSolver
        └── algorithms/
            ├── __init__.py
            ├── a_star.py
            ├── backtracking_bfs.py
            └── dijkstra.py
```

---

## Design & Architecture

### Grid Format — `2x + 1`

The maze is internally represented as a `(2·width + 1) × (2·height + 1)` integer grid. Each logical cell at position `(col, row)` maps to grid coordinate `(2·col + 1, 2·row + 1)`, and the walls between cells occupy the even-indexed rows and columns. This layout keeps wall carving simple: removing the wall between two adjacent cells means setting the single grid cell between them to `0`.

```
Grid values:
  1 — wall (solid)
  0 — open path
  2 — protected / special cell (entry/exit area)
```

For a 3×3 logical maze the grid is 7×7; a 10×10 maze produces a 21×21 grid.

### Entry and Exit

The `Maze` class stores entry and exit as logical `(x, y)` coordinates and converts them to grid coordinates on demand via the `entry` and `exit` properties (`2x + 1`, `2y + 1`). Both `MazeGenerator` and `MazeSolver` operate in grid space, while callers work in logical space.

### Registry and Auto-Registration

`maze_register.py` defines two independent class-level registries:

- `GeneratorRegistry` — maps string names to `MazeGenerator` subclasses.
- `SolverRegistry` — maps string names to `MazeSolver` subclasses.

Registration is **automatic**: both base classes implement `__init_subclass__`, so any subclass that sets the class attribute `algorithm_name` is registered the moment it is imported. No explicit `register()` call is needed in user code.

```python
class MyGenerator(MazeGenerator):
    algorithm_name = "my_algo"   # registered automatically on import
    ...
```

This means you can extend the package by dropping a new file into `algorithms/` and importing it — the registry picks it up with zero boilerplate.

### Perfect vs. Imperfect Mazes

When `MazeConfig.perfect` is `True` (the default), the generator produces a **perfect maze**: a spanning tree where exactly one path exists between any two cells. When `perfect=False`, the base class post-processes the grid by randomly carving additional walls (`_add_loop` / `_add_loop_step`), introducing loops and multiple solution paths. The probability of each extra carve is controlled by `MazeGenerator._chance` (default `0.05`).

### Step-by-Step Generation and Solving

Both `MazeGenerator.generate_step()` and `MazeSolver.solve_step()` are Python generators that yield intermediate states. This makes it straightforward to render live animations:

```python
for maze_state in MazeGen.generate_step(BacktrackingDFS, config):
    render(maze_state)   # draw each carving step
```

The `MazeGen` façade wraps both the full and step variants for generators and solvers uniformly.

### Hex Grid Export

`Maze.grid_hex` converts the binary grid into a 2D list of hexadecimal strings. Each cell's value encodes its four open walls as a nibble: bit 0 = north, bit 1 = east, bit 2 = south, bit 3 = west. This compact format is useful for serialization or interfacing with external renderers.

---

## Installation

The provided `Makefile` builds the package into a distributable `.whl` / `.tar.gz` in the project root:

```bash
make build
```

This command:
1. Creates an isolated virtual environment (`.venv`).
2. Installs the `build` tool inside it.
3. Runs `python -m build --outdir .` to produce the distribution files.
4. Removes the virtual environment.

Install the resulting wheel into your own project:

```bash
pip install mazegen-0.1.0-py3-none-any.whl
```

Or install directly in development mode (editable install, no build step needed):

```bash
pip install -e .
```

---

## Quick Start

### Generate a maze

```python
from mazegen import MazeGen, MazeConfig
from mazegen.generator.algorithms import BacktrackingDFS

config = MazeConfig(
    width=10,
    height=10,
    entry_point=(0, 0),
    exit_point=(9, 9),
    perfect=True,
    seed=42,
)

maze = MazeGen.generate(BacktrackingDFS, config)
print(maze.width, maze.height)   # 21 21 (grid size)
print(maze.entry)                 # (1, 1)
print(maze.exit)                  # (19, 19)
```

### Solve a maze

```python
from mazegen import MazeGen
from mazegen.solver.algorithms import AStar

path = MazeGen.solve(AStar, maze, seed=0)
# path is a list of (x, y) grid coordinates from entry to exit
```

### Step-by-step generation (e.g. for animation)

```python
for state in MazeGen.generate_step(BacktrackingDFS, config):
    render(state.grid)   # your rendering function
```

### Step-by-step solving

```python
solution = yield from MazeGen.solve_step(AStar, maze)
# yields each visited coordinate, then returns the final path
```

### Use the registry

```python
from mazegen.maze_register import GeneratorRegistry, SolverRegistry

gen_cls = GeneratorRegistry.get("backtracking_dfs")
sol_cls = SolverRegistry.get("a_star")

print(GeneratorRegistry.available())   # {'backtracking_dfs': ..., 'prims': ..., 'wilsons': ...}
print(SolverRegistry.available())      # {'a_star': ..., 'dijkstra': ..., 'backtracking_bfs': ...}
```

### Export to hex

```python
hex_grid = maze.grid_hex
# [['F', '9', ...], ...]  — one hex char per logical cell
```

---

## Extending the Package

### Add a custom generator

```python
from mazegen.generator.generator_base import MazeGenerator
from mazegen.maze import Maze
from typing import Generator

class SideWinder(MazeGenerator):
    algorithm_name = "sidewinder"   # auto-registered

    def generate(self) -> Maze:
        # carve walls here using self._maze.set_path(x, y)
        return super().generate()   # handles loop injection if not perfect

    def generate_step(self) -> Generator[Maze, None, None]:
        # yield self._maze after each carve step
        yield from super().generate_step()
```

### Add a custom solver

```python
from mazegen.solver.solver_base import MazeSolver
from mazegen.maze import Maze
from typing import Generator

class WallFollower(MazeSolver):
    algorithm_name = "wall_follower"   # auto-registered

    def solve(self) -> list[tuple[int, int]]:
        ...

    def solve_step(self) -> Generator[tuple[int, int], None, list[tuple[int, int]]]:
        ...
```

Once imported, both are available via the registry and through `MazeGen.generate` / `MazeGen.solve`.

---

## Algorithm Overview

### Generators

| Name | Class | Strategy | Bias |
|---|---|---|---|
| `backtracking_dfs` | `BacktrackingDFS` | Recursive/iterative DFS with backtracking | Long winding corridors |
| `prims` | `Prims` | Randomized Prim's (frontier expansion) | Short passages, many dead-ends |
| `wilsons` | `Wilsons` | Loop-erased random walk (uniform spanning tree) | Statistically unbiased |

### Solvers

| Name | Class | Strategy | Optimal? |
|---|---|---|---|
| `a_star` | `AStar` | Heuristic search (Manhattan distance) | Yes (shortest path) |
| `dijkstra` | `Dijkstra` | Uniform-cost graph search | Yes (shortest path) |
| `backtracking_bfs` | `BacktrackingBFS` | BFS with backtracking | Yes (fewest steps) |

---

## Authors

| Name | Email |
|---|---|
| Ialimeva Rindraniaina | ialrandr@student.42antananarivo.mg |
| Teddy Andrianina | trakotoz@student.42antananarivo.mg |

---

*Built at 42 Antananarivo.*
