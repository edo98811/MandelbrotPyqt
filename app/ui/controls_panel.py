from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
)

from model.state import FractalState


class ControlsPanel(QWidget):
    def __init__(self, state: FractalState, parent=None) -> None:
        super().__init__(parent)

        self.state = state

        control_layout = QVBoxLayout(self)

        title = QLabel("Controls")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        # ---- parameter inputs ----
        form = QFormLayout()

        self.center_x = QLineEdit()
        self.center_y = QLineEdit()
        self.zoom = QLineEdit()
        self.max_iter = QLineEdit()

        form.addRow("X center", self.center_x)
        form.addRow("Y center", self.center_y)
        form.addRow("Zoom", self.zoom)
        form.addRow("Max Iterations", self.max_iter)

        # ---- update button ----
        self.update_button = QPushButton("Update Fractal")
        self.update_button.clicked.connect(self.update_state)

        # ---- zoom + and - buttons ----
        self.zoom_in_button = QPushButton("+")
        self.zoom_out_button = QPushButton("-")
        # self.move_up_button = QPushButton("↑")
        # self.move_down_button = QPushButton("↓")
        # self.move_left_button = QPushButton("←")
        # self.move_right_button = QPushButton("→")

        self.zoom_in_button.clicked.connect(lambda: self.update_field("zoom", self.state.zoom * 1.1))
        self.zoom_out_button.clicked.connect(lambda: self.update_field("zoom", self.state.zoom / 1.1))
        # self.move_up_button.clicked.connect(lambda: self.update_field("center_y", self.state.center_y + 0.1))
        # self.move_down_button.clicked.connect(lambda: self.update_field("center_y", self.state.center_y - 0.1))
        # self.move_left_button.clicked.connect(lambda: self.update_field("center_x", self.state.center_x - 0.1))
        # self.move_right_button.clicked.connect(lambda: self.update_field("center_x", self.state.center_x + 0.1))

        self.zoom_in_button.setFixedWidth(50)
        self.zoom_out_button.setFixedWidth(50)

        buttons = QHBoxLayout()
        buttons.addWidget(self.zoom_out_button)
        buttons.addStretch()
        buttons.addWidget(self.zoom_in_button)


        # assemble panel
        control_layout.addWidget(title)
        control_layout.addLayout(form)
        control_layout.addWidget(self.update_button)
        control_layout.addLayout(buttons)

        control_layout.addStretch()

        self.refresh_fields()
        self.state.changed.connect(self.refresh_fields)

    def refresh_fields(self):
        self.center_x.setText(f"{self.state.center_x:.2f}")
        self.center_y.setText(f"{self.state.center_y:.2f}")
        self.zoom.setText(f"{self.state.zoom:.2f}")
        self.max_iter.setText(str(self.state.max_iter))

    def update_state(self):
        try:
            self.state.update(
                center_x=float(self.center_x.text()),
                center_y=float(self.center_y.text()),
                zoom=float(self.zoom.text()),
                max_iter=int(self.max_iter.text()),
            )
        except ValueError as e:
            self.state.new_message.emit(str(e))
        except Exception as e:
            self.state.new_message.emit(f"Unexpected error: {e}")
        finally:
            self.state.new_message.emit(f"Fractal parameters updated: {self.state.center_x:.2f}, {self.state.center_y:.2f}, zoom={self.state.zoom:.2f}, max_iter={self.state.max_iter}")
    
    def update_field(self, field_name: str, value: float):
        self.state.update(**{field_name: value})
    
 