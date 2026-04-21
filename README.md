# Color Wars

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-2E8B57)](https://www.pygame.org/)
[![Tests](https://img.shields.io/badge/tests-25%20passed-success)](#testing)
[![License](https://img.shields.io/badge/license-TBD-lightgrey)](#license)

Color Wars is a turn-based Pygame strategy game about placing dots, triggering chain explosions, and converting enemy territory on a 5x5 board. It supports local PvP and PvE matches with Easy, Medium, and Hard AI levels.

## Table of Contents

- [Why This Project](#why-this-project)
- [Quick Start](#quick-start)
- [Controls](#controls)
- [Gameplay Rules](#gameplay-rules)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Audio and Scene Behavior](#audio-and-scene-behavior)
- [Win Chance Model](#win-chance-model)
- [Media Preview](#media-preview)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Why This Project

- Demonstrate a compact turn-based strategy core with deterministic rules.
- Keep architecture clean as features grow (audio/settings/scene now have a shared runtime core).
- Provide both player-ready flow and testable subsystems for long-term maintainability.

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

## Architecture

Core architecture follows separation of concerns:

- Engine: pure game rules and chain explosion resolution
- Controller: state mutation and win detection
- View: rendering and UI only
- Runtime Core: scene flow, app settings, and music orchestration

Runtime components:

- `CoreSystems`: app-level orchestrator for scene flow and shared systems
- `AppSettings`: global settings source of truth
- `MusicManager`: context-aware music management for menu/gameplay
- shared UI helpers (`view/commons/ui_components.py`) for:
  - consistent hover/pressed button behavior across scenes
  - fitted text rendering for responsive screen sizes

Scene flow:

1. HOME starts a new menu session and randomizes theme/game tracks.
2. User picks mode and difficulty.
3. Core enters GAMEPLAY with LaunchConfig.
4. Exiting gameplay returns to HOME and restores theme track.

## Project Structure

```text
asset/
  aud/                  background music files
  img/                  backgrounds and UI images
  gameplay/             gameplay screenshots
src/
  main.py               application entrypoint
  controller.py         move application and win handling
  engine/               pure rules and explosion logic
  game/
    core.py             core systems (scene, settings, audio wiring)
    settings.py         shared app settings
    audio.py            music manager and audio controls
    loop.py             gameplay runtime loop
    analysis.py         win chance analysis
  ai/                   difficulty-specific AI policies
  view/                 all Pygame rendering and UI
tests/
  ai/                   AI behavior tests
  game_logic/           rules and controller tests
  view/                 scene and HUD tests
```

## Audio and Scene Behavior

- Music session behavior:
  - menu picks one random theme track
  - gameplay uses the remaining tracks and alternates them
  - returning to menu restores theme immediately
- Music toggle semantics: pause/resume (no forced stop/restart)
- Fullscreen behavior: controlled by user preference, no forced scene auto-fullscreen

## Asset Layout

Current asset locations:

- `asset/img/`: background, icon, and UI images
- `asset/aud/`: music tracks
- `asset/gameplay/`: screenshot assets and optional gameplay video

## UI Readability Standards

Recent polish rules applied across scenes:

- Visual hierarchy by section blocks (Title -> Description -> Controls -> Action).
- Shared interactive buttons with hover/pressed feedback.
- Responsive text fitting for resize-safe labels and headings.
- Home panel keeps 4 controls (Play, Quit, Tutorial, Settings), with labels on Play/Quit and icon actions on Tutorial/Settings.
- Choose mode panel now includes the heading `Chọn chế độ chơi`.
- Tutorial overlay uses a larger screen-relative window to avoid text clipping.
- Tutorial text-wall reduction:
  - numbered bullet format
  - keyword highlight (`nổ dây chuyền`, `4 chấm`, `combo`, `phím tắt`)
  - narrower line width for easier scanning

## Win Chance Model

Current model is lightweight but stronger than simple score heuristics:

- phase-aware weighting (early vs late game)
- normalized features:
  - territory control
  - dot pressure
  - mobility (valid moves)
  - near-explosion potential
- smoothed probability output with bounded confidence

## Media Preview

The repo currently ships preview assets under `asset/gameplay/`.

### Screenshots

- [Gameplay overview](asset/gameplay/gameplay.png)
- [End screen](asset/gameplay/win.png)

### Video

- [YouTube demo](https://www.youtube.com/watch?v=Ku6gNe-UeJE)

If you want a minimal README, keeping just the screenshots above is enough.

## Development Workflow

### Local Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run and Test

```bash
python -m src.main
pytest -q
```

### Local Demo Completion Check

When validating a local demo build, verify these UX points:

1. Hover and pressed states appear on all primary buttons (Home, Settings, Tutorial close, Win scene).
2. Text scales to stay inside button/panel bounds when resizing window.
3. Settings panel layout remains readable at 1280x720.
4. Fullscreen changes only when pressing `F11`.
5. PvP HUD does not show bot difficulty.

## Testing

- Current status: `25 passed`
- Test layout:
  - `tests/ai`: AI behavior
  - `tests/game_logic`: engine/controller correctness
  - `tests/view`: scene/HUD contracts
- Newly covered UI behaviors:
  - home menu icon placement and button labels
  - choose-mode heading rendering
  - settings scene copy cleanup and apply-mark removal
  - tutorial overlay minimum size constraints
- Remaining gaps:
  - no full integration tests for complete menu flow (`run_home_menu` event loop)
  - no automated visual regression/snapshot tests for real rendered frames
  - limited tests for audio manager runtime behavior

## Troubleshooting

- Music does not play:
  - verify `.mp3` files exist in `asset/aud/`
  - check audio device availability and mixer initialization
- Fullscreen toggles unexpectedly:
  - press `F11` to restore preference, then re-enter scene
- Text or panels overlap in small window:
  - increase window size; side HUD panels auto-reduce on narrow layouts
- Tests fail locally but pass before:
  - run from repo root and ensure dependencies from `requirements.txt` are installed

## Roadmap

1. Centralize all UI text into a localization table (vi/en).
2. Introduce typed runtime event bus for scene actions.
3. Add UI snapshot tests for responsive windowed layouts.
4. Improve AI explanation overlays for player learning.

## Contributing

Contributions are welcome.

- Keep architecture boundaries intact (engine/controller/view/runtime core).
- Add or update tests for behavioral changes.
- Prefer small, focused pull requests with clear scope.

Suggested PR checklist:

- [ ] tests pass locally (`pytest -q`)
- [ ] no architecture boundary violations
- [ ] README/docs updated if behavior changes

## License

License is currently `TBD`.

If you plan to open-source publicly, add a `LICENSE` file (MIT is common for game prototypes) and update this section.
