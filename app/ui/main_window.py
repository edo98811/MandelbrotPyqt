from __future__ import annotations

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QWidget

from model.state import FractalState
from ui.canvas import Canvas
from ui.controls_panel import ControlsPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MandelbrotPyqt")
        self.resize(960, 640)

        self.state = FractalState()

        # CENTRAL WIDGET
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)

        # LEFT: CANVAS AREA
        self.canvas = Canvas(self.state)
        main_layout.addWidget(self.canvas, stretch=3)

        # RIGHT: CONTROLS PANEL
        self.control_panel = ControlsPanel(self.state)
        main_layout.addWidget(self.control_panel, stretch=1)

        # STATUS BAR
        self.statusBar().showMessage("Ready")
        self.state.new_message.connect(self.update_status_bar)

    def update_status_bar(self, msg: str):
        self.statusBar().showMessage(msg)