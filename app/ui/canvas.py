from __future__ import annotations

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QLabel

from core.renderer import Renderer
from model.state import FractalState


class Canvas(QLabel):

    def __init__(self, state: FractalState, parent=None) -> None:
        super().__init__("Fractal Canvas", parent)
        self.state = state
        self.renderer = Renderer()
        self.last_pos = None
        self._generation = 0

        self._render_timer = QTimer(self)
        self._render_timer.setSingleShot(True)
        self._render_timer.timeout.connect(self.update_canvas)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            """
            background-color: black;
            color: white;
            font-size: 18px;
            """
        )
        width, height = self._render_size()
        self.qimg = self.renderer.black_image(width, height)
        self.update_canvas()

        self.state.changed.connect(self.update_canvas)
        self.update()

    def _render_size(self):
        width = max(1, self.width() // self.state.render_scale)
        height = max(1, self.height() // self.state.render_scale)
        return width, height

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.qimg)

    def update_canvas(self):
        width, height = self._render_size()
        self._generation += 1

        self.renderer.compute_async(
            width,
            height,
            self.state.center_x,
            self.state.center_y,
            self.state.zoom / self.state.render_scale,
            self.state.max_iter,
            self._generation,
            self._on_render_done,
        )

    def _on_render_done(self, qimg, generation):
        if generation != self._generation:
            return  # a newer render was requested before this one finished

        self.qimg = qimg
        self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        zoom_factor = 1.2

        if delta > 0:
            self.state.update(zoom=self.state.zoom * zoom_factor)
        else:
            self.state.update(zoom=self.state.zoom / zoom_factor)


    def mousePressEvent(self, event):
        self.last_pos = event.position()

    def mouseReleaseEvent(self, event):
        pos = event.position()

        dx = pos.x() - self.last_pos.x()
        dy = pos.y() - self.last_pos.y()

        self.state.update(center_x=self.state.center_x - dx / self.state.zoom)
        self.state.update(center_y=self.state.center_y - dy / self.state.zoom)


