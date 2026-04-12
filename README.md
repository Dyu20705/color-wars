# Color Wars 🎮

**Color Wars** is a turn-based strategy game built with Python and Pygame.
Players place colored dots on a 5×5 board, trigger chain explosions, and convert enemy territory.
The project features both local PvP and PvE (vs AI) with three difficulty levels.

## 🎯 Game Overview

### Core Mechanics
- **Turn-based tactical gameplay** on a 5×5 board  
- **Chain-reaction explosion system** when cells reach 4 dots  
- **Territory conversion** after explosions: neighbors become your color  
- **Two game modes**: PvP (human vs human) or PvE (human vs AI)  
- **Three AI difficulties**: Easy (training-friendly), Medium (shallow lookahead), Hard (alpha-beta pruning)

### Win Condition
A player wins by:
1. Dominating the entire board, **OR**
2. Eliminating the opponent (reducing their cells to 0 after they had played)

### Dot Increment Rules
- **Empty cell capture**: +3 dots  
- **Reinforce owned cell**: +1 dot  
- **Explosion threshold**: 4 dots per cell (triggers cascade)

## 🚀 Quick Start

### Requirements
- Python 3.10+
- Pygame 2.5.0+

### Installation
```bash
pip install -r requirements.txt
```

### Run Game
```bash
python -m src.main
```

### Run Tests
```bash
# Windows PowerShell
$env:PYTHONPATH='.'; pytest -v

# Linux/macOS
PYTHONPATH=. pytest -v
```

## 🎮 Controls

| Control | Action |
|---------|--------|
| **Left Click** | Place/reinforce on valid cell |
| **M** | Toggle between PvP / PvE mode |
| **R** | Restart current match |
| **1 / 2 / 3** | Set AI difficulty (Easy / Medium / Hard) |
| **F11** | Toggle fullscreen |

## 📁 Project Structure

### Source Code (`src/`)

```
src/
├── main.py                  # Application entrypoint
├── controller.py            # Game state mutations & move validation
├── game/
│   ├── state.py            # GameState dataclass
│   └── loop.py             # Main frame loop & input handling
├── engine/
│   ├── rules.py            # Move legality & dot increment logic
│   └── explosion.py        # Chain reaction resolver
├── ai/
│   ├── ai.py               # AI router (dispatcher)
│   ├── ez_AI.py            # Easy difficulty (weak moves, 80% probability)
│   ├── med_AI.py           # Medium difficulty (shallow lookahead)
│   └── hard_AI.py          # Hard difficulty (alpha-beta pruning)
└── view/                   # Pygame rendering layer
    ├── constants.py        # Shared colors, sizes
    ├── layout.py           # Screen geometry & responsive layout
    ├── window.py           # Window/fullscreen management
    ├── base/               # Abstract base classes
    │   └── scene.py        # BaseScene, SceneController
    ├── commons/            # Reusable UI components
    │   └── ui_components.py # Button, Panel, TextLabel
    ├── gameplay_scene/     # Main board rendering
    │   ├── scene.py        # Scene composer
    │   ├── board.py        # Board grid & ownership rendering
    │   ├── hud.py          # Score badge & status display
    │   ├── effects.py      # Explosion animation overlay
    │   └── __init__.py     # Public API
    └── *_scene/            # Menu scenes
        ├── scene.py        # Scene-specific rendering
        └── flow.py         # Event handling & logic (if complex)
```

### Tests (`tests/`)

Tests are organized by module for easy discovery and scalability:

```
tests/
├── ai/                     # AI behavior tests
│   ├── test_ai_router.py   # Difficulty selector
│   └── test_hard_ai.py     # Hard AI strategy
├── game_logic/             # Engine tests
│   ├── test_rules.py       # Move legality & dot rules
│   └── test_explosion.py   # Chain reaction physics
└── view/                   # UI rendering tests
    ├── test_home_scene.py  # Menu layout
    └── test_hud.py         # HUD display
```

### Scripts (`scripts/`)

```
scripts/
└── benchmark_ai.py         # AI win-rate benchmarking across difficulty levels
```

## 🏗️ Architecture Principles

### Separation of Concerns
- **Engine** (`rules.py`, `explosion.py`): Pure game logic, no side effects  
- **Controller** (`controller.py`): Orchestrates moves, updates state  
- **View** (`src/view/`): Rendering only, no game logic  
- **AI** (`src/ai/`): Decision-making, uses only engine & rules  

### Scalability
- **BaseScene & SceneController**: Enables new menus/scenes without code duplication  
- **UI Components** (`Button`, `Panel`, `TextLabel`): Reusable across all scenes  
- **Shared Constants & Layout**: Consistent theming and responsive geometry  

### Testing
- **Organized by module**: Easy to find and add tests  
- **Engine heavily tested**: Rules engine is the source of truth  
- **Integration optional**: View & AI can be tested independently  

## 🤖 AI Levels

### Easy (~20% win rate vs Medium)
- Picks mostly weak moves for learning-friendly gameplay  
- 80% probability of selecting suboptimal moves  
- Safe for first-time players

### Medium (~50% win rate vs Hard)  
- Shallow lookahead (1-2 plys)  
- Controlled randomness to avoid perfect play  
- Good for intermediate players

### Hard (~80% win rate vs Medium)  
- Alpha-beta pruning with evaluation function  
- Adapts to game state  
- Challenges experienced players

Run `scripts/benchmark_ai.py` to verify balance:
```bash
python scripts/benchmark_ai.py --games 200
```

## 📋 Development Notes

- **Rendering loop runs at 60 FPS** with responsive window resizing  
- **AI runs on main thread** (blocking during turn); optimize if needed for multiplayer  
- **No external assets required** (pure Pygame drawing)  
- **Snake_case** for functions, CamelCase for classes, UPPER_CASE for constants  

## 📝 License & Contributing

This project is for educational and research purposes.

Contributions welcome! Please:
1. Write tests for new features
2. Follow the code style (type hints encouraged)
3. Update documentation

## 🐛 Known Issues & Future Work

See the production-readiness scorecard below for detailed assessment.

---

## 📊 Production-Readiness Assessment

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation and production checklist.


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
| `src/ai/ez_AI.py` | Easy bot policy. | Plays weakly by preferring lower-impact candidate moves. |
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

Home menu is shown first to choose game mode and (for bot mode) difficulty.

## Controls

- Left Click: place/reinforce on a valid cell.
- `M`: toggle `PVP` / `PVBOT`.
- `R`: restart current match.
- `F11`: toggle fullscreen.

Note: Difficulty is selected from the Home screen before starting a bot match.

## Testing (Optional)

```bash
# On Windows PowerShell
$env:PYTHONPATH='.'; pytest -q
```

## Notes

- The runtime dependency is intentionally minimal for straightforward setup and play.
- AI and game rules share the same engine logic to keep behavior consistent.
