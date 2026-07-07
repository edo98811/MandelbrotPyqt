from __future__ import annotations

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal
from PyQt6.QtGui import QImage

from core.mandelbrot import mandelbrot


class WorkerSignals(QObject):
    finished = pyqtSignal(QImage, int)


class MandelbrotWorker(QRunnable):
    def __init__(self, width, height, center_x, center_y, zoom, max_iter, generation):
        super().__init__()
        self.width = width
        self.height = height
        self.center_x = center_x
        self.center_y = center_y
        self.zoom = zoom
        self.max_iter = max_iter
        self.generation = generation
        self.signals = WorkerSignals()

    def run(self):
        img = mandelbrot(
            self.width, self.height,
            self.center_x, self.center_y,
            self.zoom, self.max_iter,
        )
        qimg = QImage(
            img.data,
            self.width,
            self.height,
            QImage.Format.Format_Grayscale8,
        ).copy()  # detach from the numpy buffer before `img` is freed
        self.signals.finished.emit(qimg, self.generation)


class Renderer:
    def __init__(self):
        self._pool = QThreadPool()
        self._pool.setMaxThreadCount(1)
        self._workers = []

    def compute(self, width, height, center_x, center_y, zoom, max_iter):
        img = mandelbrot(width, height, center_x, center_y, zoom, max_iter)

        return QImage(
            img.data,
            width,
            height,
            QImage.Format.Format_Grayscale8,
        )

    def compute_async(self, width, height, center_x, center_y, zoom, max_iter, generation, on_done):
        worker = MandelbrotWorker(width, height, center_x, center_y, zoom, max_iter, generation)
        self._workers.append(worker)

        def _cleanup(qimg, gen, w=worker):
            self._workers.remove(w)
            on_done(qimg, gen)

        worker.signals.finished.connect(_cleanup)
        self._pool.start(worker)

    def black_image(self, width, height):
        img = QImage(width, height, QImage.Format.Format_Grayscale8)
        img.fill(0)
        return img
