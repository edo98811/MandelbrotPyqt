# MandelbrotPyqt

A small PyQt6 starter project with a Docker-based development environment.

## Open in VS Code

1. Install the Dev Containers extension.
2. Open this folder in VS Code.
3. Run **Dev Containers: Reopen in Container**.

## Run locally inside the container

```bash
python app/main.py
```

The Docker setup is configured for containerized development. If you want to show the Qt window on macOS, you will usually need a host display setup such as XQuartz; otherwise the app can still be developed and tested in the container with `QT_QPA_PLATFORM=offscreen`.
