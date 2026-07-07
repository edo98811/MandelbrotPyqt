
from PyQt6.QtCore import QObject, pyqtSignal

class FractalState(QObject):
    changed = pyqtSignal()
    new_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._center_x = 0.0
        self._center_y = 0.0
        self._zoom = 200.0
        self._max_iter = 100
        self._render_scale = 1  

    def update(self, 
               center_x: float = None, 
               center_y: float = None, 
               zoom: float = None, 
               max_iter: int = None,
               render_scale: int = None
               ) -> None:

        # Validate input
        if zoom is not None:
            zoom = float(zoom)
            if zoom <= 0:
                raise ValueError("Zoom must be positive")

        if max_iter is not None:
            max_iter = int(max_iter)
            if max_iter <= 0 or max_iter > 10_000:
                raise ValueError("max_iter must be 1-10000")
        
        if render_scale is not None:
            render_scale = int(render_scale)
            if render_scale <= 0 or render_scale > 100:
                raise ValueError("render_scale must be 1-100")

        # apply atomically
        self._center_x = float(center_x) if center_x is not None else self._center_x
        self._center_y = float(center_y) if center_y is not None else self._center_y
        self._zoom = zoom if zoom is not None else self._zoom
        self._max_iter = max_iter if max_iter is not None else self._max_iter
        self._render_scale = render_scale if render_scale is not None else self._render_scale

        # single notification
        self.changed.emit()

    @property
    def render_scale(self):
        return self._render_scale
    
    @property
    def center_x(self):
        return self._center_x

    @property
    def center_y(self):
        return self._center_y

    @property
    def zoom(self):
        return self._zoom

    @property
    def max_iter(self):
        return self._max_iter