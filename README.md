# Color Wars

Color Wars is a turn-based Pygame strategy game about placing dots, triggering chain explosions, and converting enemy territory on a 5x5 board. It supports local PvP and PvE matches with Easy, Medium, and Hard AI levels.

## Quick Start

### Requirements

- Python 3.10+
- Pygame 2.x

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
python -m src.main
```

### Test

```bash
pytest -v
```

## Controls

- Left Click: place or reinforce a valid cell
- M: toggle PvP / PvE mode
- R: restart the current match
- H: toggle tutorial overlay
- F11: toggle fullscreen
- Esc: go back or close overlays

## Gameplay Rules

- Empty cell capture adds 3 dots
- Reinforcing your own cell adds 1 dot
- A cell explodes at 4 dots
- Chain explosions convert adjacent cells to the exploding owner

## Project Structure

```text
asset/
  mp3/                  background music files
scripts/
  benchmark_ai.py       AI balance benchmark
src/
  main.py               application entrypoint
  game/core.py          core systems (scene, settings, audio wiring)
  controller.py         move application and win handling
  engine/               pure rules and explosion logic
  game/                 runtime state, loop, audio, analysis
  ai/                   difficulty-specific AI policies
  view/                 all Pygame rendering and UI
tests/
  ai/                   AI behavior tests
  game_logic/           rules and controller tests
  view/                 scene and HUD tests
```

## Architecture Notes

- The engine is pure and does not depend on Pygame surfaces.
- The controller owns state mutation and win detection.
- The view layer handles rendering only.
- AI reads board state and returns a move.

## Core Runtime Design

The project now has a clearer runtime core to avoid feature stacking without structure.

- `CoreSystems`: single app-level orchestrator for scene flow, audio, and settings.
- `AppSettings`: shared settings source of truth across home/game scenes.
- `MusicManager`: menu/game context music system with session-based playlist behavior.

### Scene Flow

1. `HOME` scene starts a new menu session and randomizes theme/game tracks.
2. User selects mode/difficulty from home flow.
3. Core transitions to `GAMEPLAY` with validated launch config.
4. Exiting gameplay transitions back to `HOME` while restoring theme track.

### Audio Flow

- On each new home session, one track is picked as menu theme.
- Gameplay uses the remaining tracks and alternates between them.
- Returning home switches immediately back to theme.
- Music toggle uses pause/resume (not stop/restart).

## AI Levels

- Easy: intentionally weak and beginner-friendly
- Medium: shallow heuristic search with light randomness
- Hard: alpha-beta search with evaluation and limited randomness

Run the AI benchmark with:

```bash
python scripts/benchmark_ai.py --games 200
```

## Screenshot

![Gameplay screenshot placeholder](docs/screenshot-placeholder.png)

## Notes

- Music supports multi-track session behavior (theme + alternating gameplay tracks)
- The game opens from the home menu first
- Tests are organized by subsystem for easier maintenance

## Project Health Check

Current core systems status:

- Audio system: centralized and context-aware (`menu` / `game`) with pause/resume semantics.
- Settings system: shared object across scenes (`AppSettings`) to prevent desync.
- Scene system: explicit high-level state machine in `CoreSystems`.

Recommended next milestones:

1. Move all UI strings into a dedicated localization table.
2. Introduce a typed event bus for scene-to-scene actions.
3. Add snapshot-based UI tests for key scene layouts in windowed mode.

## Testing (Optional)

```bash
# On Windows PowerShell
$env:PYTHONPATH='.'; pytest -q
```

## Additional Notes

- The runtime dependency is intentionally minimal for straightforward setup and play.
- AI and game rules share the same engine logic to keep behavior consistent.
