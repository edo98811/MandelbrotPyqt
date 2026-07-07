ui/controls_panel.py — ControlsPanel(QWidget): the title, the 4 QLineEdit fields, and the update button (exposed as attributes so MainWindow can wire them up)
ui/canvas.py — Canvas(QLabel): paintEvent/wheelEvent/mousePressEvent/mouseMoveEvent/compute_mandelbrot, which previously lived on MainWindow even though they clearly belonged to the canvas widget
ui/main_window.py — MainWindow now just assembles Canvas + ControlsPanel and keeps on_update
core/renderer.py — new Renderer class; the QImage-building half of the old compute_mandelbrot moved here, Canvas.compute_mandelbrot now just calls it
model/state.py — new FractalState dataclass (xmin/xmax/ymin/ymax, center_x/center_y, zoom, max_iter), shared by Canvas
main.py — trimmed down to just QApplication + MainWindow bootstrap
Added empty __init__.py in ui/, core/, model/ so the packages import cleanly under python app/main.py.

One thing worth flagging: the original code already called self.render(...) in wheelEvent, mouseMoveEvent, and on_update, but no render method was ever defined anywhere — only compute_mandelbrot. That was a pre-existing bug, not something I introduced. Per your instructions I moved the code verbatim without adding new logic, so those self.render(...) calls still point at a method that doesn't exist (now in Canvas/MainWindow respectively). Let me know if you'd like me to wire that up next, or if you want to review the split first.