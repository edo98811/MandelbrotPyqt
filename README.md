# MandelbrotPyqt

An interactive Mandelbrot set viewer built with PyQt6. Pan with the mouse, zoom with the scroll wheel, and tune the render precisely from the side panel.

## Features

- Pan by dragging, zoom with the mouse wheel
- Side panel for setting center coordinates, zoom level, and max iterations directly
- Rendering runs on a background thread pool so the UI stays responsive while a frame is being computed
- In-flight renders are superseded (not queued up) when the view changes again before they finish, so the canvas always converges on the latest requested view

## Requirements

- Python 3.12+
- PyQt6 (see `requirements.txt` for exact pinned versions)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
cd app
python main.py
```

## Docker

A `Dockerfile` is provided with the system libraries PyQt6 needs on Linux, plus `xvfb` for running headlessly:

```bash
docker build -t mandelbrot-pyqt .
docker run -it mandelbrot-pyqt
```

## Project structure

```
app/
  main.py              # QApplication bootstrap
  core/
    mandelbrot.py       # Mandelbrot escape-time computation (NumPy array in, iteration counts out)
    renderer.py          # Turns iteration counts into a QImage; owns the background QThreadPool
  model/
    state.py            # FractalState: center/zoom/max_iter, emits `changed` on updates
  ui/
    main_window.py       # Assembles Canvas + ControlsPanel
    canvas.py            # Renders the fractal, handles pan/zoom input
    controls_panel.py    # Manual parameter entry and zoom buttons
```

## Architecture notes

- `FractalState` is the single source of truth for view parameters (center, zoom, max iterations). Widgets read from it and write to it via `update()`, which emits a `changed` signal.
- `Canvas` debounces `changed` with a short single-shot `QTimer`: the first change in a burst renders immediately, and rapid follow-up changes (e.g. during a drag) coalesce into one trailing render instead of one per event.
- Each render request is tagged with a generation counter; if a newer render is requested before an older one finishes, the older result is discarded when it arrives.
- `Renderer` submits render jobs to a single-worker `QThreadPool` and keeps a reference to in-flight workers until they report completion, so results are delivered reliably back to the GUI thread via Qt signals.
