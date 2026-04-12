# Color Wars

Color Wars is a turn-based strategy game built with Python and Pygame.
Players place and upgrade cells, trigger chain explosions, and convert adjacent enemy cells to control the board.

The project supports both local PvP and PvE (vs AI) with multiple bot difficulties.

## Highlights

- Turn-based tactical gameplay on a 5x5 board.
- Chain-reaction explosion system.
- Territory conversion mechanics after each explosion.
- Two game modes:
  - `PVP`: human vs human (same device).
  - `PVBOT`: human (Blue) vs AI (Red).
- Three AI levels:
  - `Easy`: mostly random with a tiny greedy chance.
  - `Medium`: shallow lookahead with controlled randomness.
  - `Hard`: adaptive alpha-beta with stronger evaluation.
- Responsive board rendering and fullscreen toggle.
- Explosion animation overlay for better move readability.

## Core Rules

- A move is valid only on:
  - an empty cell if the player has no owned cells yet (first entry move), or
  - one of the player's own cells afterward.
- Dot increment:
  - empty cell capture: `+3`
  - reinforce owned cell: `+1`
- Explosion threshold: `4`
  - when a cell reaches threshold, it explodes,
  - spreads dots to 4 orthogonal neighbors,
  - converts neighbors to the exploding player's color,
  - can trigger chain reactions.

## Win Condition

A player wins when they fully dominate the board, or when the opponent has been eliminated after previously entering the game.

## Project Structure

### High-Level Layout

- `src/`: all runtime game code (engine, game flow, AI, and rendering).
- `tests/`: unit tests for rules, explosions, and AI behavior.
- `scripts/`: utility scripts (benchmarking, experiments).

### Detailed File Guide (Beginner Friendly)

| File | What it contains | What it does in the game |
| --- | --- | --- |
| `README.md` | Project description, setup, controls, architecture notes. | Helps new contributors understand and run the project quickly. |
| `requirements.txt` | Python dependency list (`pygame`, etc.). | Ensures all machines install the same runtime packages. |
| `scripts/benchmark_ai.py` | Match simulator and win-rate reporter across AI levels. | Measures AI balance (for example target bands like 20/50/80). |
| `src/__init__.py` | Package marker for `src`. | Allows importing modules with `src.*` paths. |
| `src/main.py` | Application entrypoint. | Starts window, initializes game loop, and runs the app. |
| `src/controller.py` | Core gameplay actions at turn level. | Applies moves, updates score, checks win state, and switches turns. |
| `src/ai/__init__.py` | AI package marker. | Exposes AI modules as a clean package. |
| `src/ai/ai.py` | AI dispatcher/router. | Chooses which difficulty bot function (`easy/medium/hard`) is called. |
| `src/ai/ez_AI.py` | Easy bot policy. | Plays weakly (mostly random, with tiny immediate-gain bias). |
| `src/ai/med_AI.py` | Medium bot logic and heuristic evaluation. | Uses short lookahead and light randomness for human-like mistakes. |
| `src/ai/hard_AI.py` | Hard bot search + evaluation. | Uses alpha-beta search with adaptive depth and stronger board features. |
| `src/engine/__init__.py` | Engine package marker. | Groups pure rule/explosion mechanics. |
| `src/engine/rules.py` | Constants and legal-move rule helpers. | Defines who can move where and how many dots a move adds. |
| `src/engine/explosion.py` | Chain explosion resolver. | Processes cascades, ownership conversion, and propagation logic. |
| `src/game/__init__.py` | Game package marker. | Keeps runtime game modules organized. |
| `src/game/state.py` | Mutable `GameState` data container. | Stores board, dots, current player, mode, difficulty, and winner. |
| `src/game/loop.py` | Main frame loop and input/update/render orchestration. | Handles events, triggers AI turns, and keeps gameplay running. |
| `src/view/__init__.py` | View package marker. | Organizes all rendering/UI modules. |
| `src/view/constants.py` | UI colors, sizes, and visual constants. | Central place for visual tuning without touching logic code. |
| `src/view/layout.py` | Geometry and coordinate calculations. | Maps board cells to screen positions and responsive layout values. |
| `src/view/window.py` | Window/surface setup helpers. | Creates display surface and manages fullscreen/window modes. |
| `src/view/board.py` | Board and cell rendering routines. | Draws grid, ownership colors, and dot counts on each cell. |
| `src/view/hud.py` | Text overlays and top HUD elements. | Shows turn info, mode, difficulty, and score to player. |
| `src/view/effects.py` | Visual effect primitives. | Provides reusable animation/effect drawing logic. |
| `src/view/scene.py` | Scene composition entrypoint for rendering. | Combines board, HUD, and effects into a full frame. |
| `tests/test_rules.py` | Unit tests for legal moves and rule helpers. | Protects rule correctness against regressions. |
| `tests/test_explosion.py` | Unit tests for chain reaction behavior. | Verifies explosion propagation and ownership conversion are stable. |
| `tests/test_ai.py` | Generic AI validity tests. | Ensures bots return valid moves and do not crash. |
| `tests/test_hard_ai.py` | Focused hard-AI tests. | Guards hard bot decision logic and key edge cases. |

## Requirements

- Python 3.10+
- See `requirements.txt` for runtime dependency installation.

## Installation

```bash
pip install -r requirements.txt
```

## Run Game

```bash
python -m src.main
```

## Controls

- Left Click: place/reinforce on a valid cell.
- `M`: toggle `PVP` / `PVBOT`.
- `R`: restart current match.
- `1` / `2` / `3`: set AI difficulty (`Easy` / `Medium` / `Hard`).
- `F11`: toggle fullscreen.

## Testing (Optional)

```bash
# On Windows PowerShell
$env:PYTHONPATH='.'; pytest -q
```

## Notes

- The runtime dependency is intentionally minimal for straightforward setup and play.
- AI and game rules share the same engine logic to keep behavior consistent.
